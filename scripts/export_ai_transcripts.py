"""Export Claude Code session transcripts to reports/ai_transcripts/ for Q7.4.

`AI_USAGE.md`'s prompt-log section promises these. Claude Code stores each session
as JSONL under ~/.claude/projects/<slugified-cwd>/; there is no CLI export flag,
and the in-session /export command covers only the conversation you are currently
in, which would miss the other eleven.

Default output is a PROMPT LOG: the prompts actually typed, in order, with a
one-line note of what the assistant did between them. The raw JSONL is ~15 MB of
tool inputs and outputs; dumping that is not a prompt log and no marker would read
it. `--full` additionally includes the assistant's prose replies.

Two filters matter for correctness:
  - `isSidechain` records are sub-agent conversations, not things anyone typed.
  - a `user` record whose content is a list of tool_result blocks is the harness
    feeding a tool's output back in, not a prompt. Counting those as prompts would
    inflate the log with machine chatter.

Redaction: transcripts of this project contain a message-queue URL with an embedded
password and pre-signed storage URLs carrying access signatures. They are third-party
and were published publicly by the competition organizers, but a submitted document
should not restate credentials, so they are masked.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "ai_transcripts"

REDACTIONS = [
    (re.compile(r"(pyamqp://)[^:@\s]+:[^@\s]+(@)"), r"\1<redacted>:<redacted>\2"),
    (re.compile(r"(amqp://)[^:@\s]+:[^@\s]+(@)"), r"\1<redacted>:<redacted>\2"),
    (re.compile(r"([?&](?:Signature|AWSAccessKeyId)=)[^&\s\"']+"), r"\1<redacted>"),
]


def redact(text: str) -> str:
    for pattern, repl in REDACTIONS:
        text = pattern.sub(repl, text)
    return text


def clip(text: str, max_lines: int, max_chars: int, max_line_chars: int = 400) -> str:
    """Shrink a long prompt: cap over-long individual lines, then elide the middle.

    Prompts here include pasted worker logs. What a prompt log must show is what was
    asked; the paste is context the reader already has from the surrounding documents.

    Line capping comes FIRST and is not optional. A pasted HTTP response body arrives
    as a single 30 KB line -- `b'...\n<!DOCTYPE html>...'` with escaped newlines, not
    real ones -- so line-count elision alone does nothing to it, and a character budget
    applied only to the head lets it through in the tail. Measuring "lines per block"
    is exactly the metric that hides this, which is how it was missed the first time.

    Head and tail both survive the elision because the actual question sits at one end
    or the other; a head-only clip would drop "what is my worker doing?" and keep the log.
    """
    def cap_line(line: str) -> str:
        if len(line) <= max_line_chars:
            return line
        return f"{line[:max_line_chars].rstrip()} […{len(line) - max_line_chars} chars elided…]"

    lines = [cap_line(ln) for ln in text.splitlines()]
    capped = "\n".join(lines)

    if len(lines) <= max_lines and len(capped) <= max_chars:
        return capped

    head, tail = lines[:max(max_lines - 8, 1)], lines[-6:]
    cut = len(lines) - len(head) - len(tail)
    out = "\n".join(head)
    if len(out) > max_chars:
        out = out[:max_chars].rstrip() + " …"
    marker = (f"[… {cut} lines elided — pasted output, see the surrounding docs …]"
              if cut > 0 else "[… pasted output elided …]")
    return "\n".join([out, "", marker, ""] + tail)


def blocks_to_text(content) -> str:
    """Message content is either a plain string or a list of typed blocks."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = [b.get("text", "") for b in content
             if isinstance(b, dict) and b.get("type") == "text"]
    return "\n".join(p for p in parts if p)


# Wrappers the harness injects as `user` records: slash-command echoes, the caveat
# banner, captured stdout, and context reminders. None were typed by anyone. Left in,
# they inflated the count by 12 across three sessions -- a prompt log whose count is
# wrong is worse than no count.
HARNESS_MARKERS = (
    "<local-command-caveat>",
    "<local-command-stdout>",
    "<command-name>",
    "<command-message>",
    "<command-args>",
    "<system-reminder>",
)


def is_real_prompt(rec: dict) -> bool:
    if rec.get("type") != "user" or rec.get("isSidechain"):
        return False
    content = rec.get("message", {}).get("content")
    if isinstance(content, list):
        # Harness feeding tool output back in is not a prompt.
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return False
    text = blocks_to_text(content).strip()
    if not text:
        return False
    # Strip harness wrappers, then ask whether anything a human wrote is left.
    stripped = text
    for marker in HARNESS_MARKERS:
        stripped = stripped.replace(marker, "").replace(marker.replace("<", "</"), "")
    return bool(re.sub(r"[\s\n]+", "", stripped)) and not text.startswith(HARNESS_MARKERS)


def tool_names(rec: dict) -> list[str]:
    content = rec.get("message", {}).get("content")
    if not isinstance(content, list):
        return []
    return [b.get("name", "?") for b in content
            if isinstance(b, dict) and b.get("type") == "tool_use"]


def read_session(path: Path) -> dict:
    events, title = [], None
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") == "ai-title" and not title:
                title = rec.get("aiTitle")
            if rec.get("isSidechain"):
                continue
            if is_real_prompt(rec):
                events.append(("prompt", rec.get("timestamp"),
                               blocks_to_text(rec["message"]["content"])))
            elif rec.get("type") == "assistant":
                events.append(("reply", rec.get("timestamp"),
                               blocks_to_text(rec.get("message", {}).get("content")),
                               tool_names(rec)))
    stamps = [e[1] for e in events if e[1]]
    return {"path": path, "title": title, "events": events,
            "start": min(stamps) if stamps else "", "end": max(stamps) if stamps else ""}


def fmt(ts: str) -> str:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts or "?"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    # A2 lives in its own project directory, so both must be exported or the
    # prompt log silently covers A1 only - which is what happened first.
    ap.add_argument("--source", type=Path, nargs="+",
                    default=[Path.home() / ".claude" / "projects" / "-home-csharp-IRE-A1",
                             Path.home() / ".claude" / "projects" / "-home-csharp-IRE-A2"],
                    help="one or more directories of session .jsonl files")
    ap.add_argument("--full", action="store_true",
                    help="also include the assistant's prose replies")
    ap.add_argument("--max-prompt-lines", type=int, default=25,
                    help="clip prompts longer than this (0 disables clipping)")
    ap.add_argument("--max-prompt-chars", type=int, default=1500,
                    help="character cap applied alongside --max-prompt-lines")
    args = ap.parse_args()

    files = []
    for src in args.source:
        if not src.is_dir():
            sys.exit(f"FATAL: {src} not found")
        found = sorted(src.glob("*.jsonl"))
        print(f"source    : {src}  ({len(found)} sessions)")
        files += found
    if not files:
        sys.exit(f"FATAL: no .jsonl sessions in {args.source}")

    sessions = [s for s in (read_session(p) for p in files) if s["events"]]
    sessions.sort(key=lambda s: s["start"])

    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*.md"):
        stale.unlink()

    index, total_prompts = [], 0
    for n, s in enumerate(sessions, 1):
        prompts = [e for e in s["events"] if e[0] == "prompt"]
        total_prompts += len(prompts)
        name = f"{n:02d}_{s['start'][:10]}_{s['path'].stem[:8]}.md"

        lines = [f"# Session {n} — {fmt(s['start'])} to {fmt(s['end'])}", ""]
        if s["title"]:
            lines += [f"*{s['title']}*", ""]
        lines += [f"`{s['path'].name}` · {len(prompts)} prompts", "", "---", ""]

        pending: list[str] = []
        for ev in s["events"]:
            if ev[0] == "prompt":
                if pending:
                    uniq = sorted(set(pending))
                    lines += [f"> *(assistant: {len(pending)} tool calls — "
                              f"{', '.join(uniq)})*", ""]
                    pending = []
                body = redact(ev[2].strip())
                if args.max_prompt_lines:
                    body = clip(body, args.max_prompt_lines, args.max_prompt_chars)
                lines += [f"### {fmt(ev[1])} — prompt", "",
                          "```text", body, "```", ""]
            else:
                pending += ev[3]
                if args.full and ev[2].strip():
                    lines += [redact(ev[2].strip()), ""]
        if pending:
            uniq = sorted(set(pending))
            lines += [f"> *(assistant: {len(pending)} tool calls — {', '.join(uniq)})*", ""]

        (OUT / name).write_text("\n".join(lines), encoding="utf-8")
        index.append((n, name, s, len(prompts)))

    idx = ["# AI transcripts — prompt log", "",
           "Exported by `scripts/export_ai_transcripts.py` for Q7.4. One file per Claude",
           "Code session, oldest first. Each entry is a prompt as typed; assistant tool",
           "activity is summarised between prompts rather than reproduced. Message-queue",
           "credentials and pre-signed URL signatures are masked.", "",
           "| # | Session | Date | Prompts | Topic |", "|---|---|---|---|---|"]
    for n, name, s, count in index:
        topic = (s["title"] or "").replace("|", "/")[:60]
        idx.append(f"| {n} | [{name}]({name}) | {fmt(s['start'])} | {count} | {topic} |")
    idx += ["", f"**{len(sessions)} sessions, {total_prompts} prompts.**"]
    (OUT / "index.md").write_text("\n".join(idx), encoding="utf-8")

    size = sum(f.stat().st_size for f in OUT.glob("*.md"))
    print(f"sessions  : {len(sessions)}")
    print(f"prompts   : {total_prompts}")
    print(f"written   : {OUT.relative_to(ROOT)}/  ({size / 1024:.0f} KB, "
          f"{len(list(OUT.glob('*.md')))} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
