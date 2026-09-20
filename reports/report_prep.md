# Report preparation — scaffolding for Chaitanya to write from

> **This file contains no prose for the report.** That is deliberate. The TA's condition
> (2026-09-20) is that the report "must reflect your findings/learnings and should be
> written by you", and a document of ready-made sentences would defeat that however it was
> labelled. What is here: the Q6 requirements, the numbers with their provenance, the
> questions to answer in your own words, and the claims **not** to make.
>
> **How to use it.** Take one section at a time. Answer its questions out loud or in chat
> first — if you cannot say it, you cannot write it, and that is the signal to ask for
> re-teaching rather than to start typing. Then write the section. Claude's job is to check
> each claim against `NUMBERS.md` and flag anything unsupported, not to supply wording.
>
> Everything below traces to `reports/NUMBERS.md`. Regenerate any figure with the command in
> section J or `scripts/diagnostics/README.md`.

---

## What Q6 actually asks for

Four bullets, 6 pages target (guideline, not a cap), 11pt, 1-inch margins. References and
appendices do not count.

1. What you built and key design choices — re-ranker architecture, features.
2. Baseline vs improved results, with ablation and CI.
3. Serving and scale analysis findings.
4. Where the system breaks at 10x.

Q7.2 repeats it for Moodle: "what you built, choices, observations, where it breaks at 10x".
**Note what is absent: leaderboard rank.** CLAUDE.md §4 and the spec both grade pipeline
correctness, system design, ablation rigour, scale analysis, and clarity.

---

## Section 1 — What you built, and why

**Numbers available:** two datasets (MIND 65,238 articles / 230,117 impressions; EB-NeRD
125,541 / 1,219,746 from a 5% user sample of `ebnerd_large`, D33). Feature allowlist: 10
common + 4 EB-NeRD-only (D34), plus 20 rack columns (D42). 354 tests.

**Questions to answer in your own words:**
1. Why is the feature set an **allowlist** rather than a denylist? What specifically goes
   wrong with a denylist here? (Landmine 1: `total_pageviews` is already sitting in
   `articles.parquet` and contains the future.)
2. What is the difference between "present in the test file" and "available at serving
   time"? Give the EB-NeRD example.
3. Why is popularity a **share** and not a count? (D34b — what breaks at submission time?)
4. A1's BM25 and embedding scorers became *features* of the re-ranker rather than being
   replaced. Why does that make the "before and after" comparison meaningful?

**Do not claim:** that the two datasets' decay features are comparable to each other. They
are not — MIND has no history timestamps, so its decay uses list position while EB-NeRD uses
real time (Landmine 3).

---

## Section 2 — Baseline vs improved, ablation, CI

**This is the section with the most content and the strongest story. Two separate results.**

**(a) Q3's pre-registered change — the time term in NRMS.** MIND +both −0.0002 [−0.0011,
0.0008] (spans zero); EB-NeRD +both +0.0864 [0.0852, 0.0877]. +freshness alone is
+0.0013 MIND / +0.1141 EB-NeRD. 6-epoch MIND re-run changed no conclusion.

**(b) D42's rack normalisation — measured this week.** Paired vs the shipped model, test
split, 1,000 resamples:

| | MIND | EB-NeRD |
|---|---|---|
| AUC | +0.0223 [0.0195, 0.0250] | +0.0202 [0.0194, 0.0210] |
| MRR | +0.0220 [0.0193, 0.0247] | +0.0234 [0.0222, 0.0245] |
| nDCG@5 | +0.0240 [0.0215, 0.0265] | +0.0225 [0.0215, 0.0235] |
| nDCG@10 | +0.0204 [0.0182, 0.0226] | +0.0210 [0.0202, 0.0219] |

Validation ablation (how the arm was chosen): base / +pct / +z / +both — NUMBERS K.2.

**Questions:**
1. What does **paired** mean, and why can two overlapping unpaired intervals still hide a
   real gain? (Taught 2026-09-19/20; recall check still owed.)
2. MIND's base model early-stops at **18 trees**; with rack columns it runs to **209**. What
   does that tell you about what the 18-tree model could and could not express?
3. Why is `bm25` the worst offender (0.738 between-rack variance) rather than popularity,
   which §10 had blamed? What is it about BM25's *absolute level* that varies per user?
4. The slice table: head-exposure went −0.0127 → +0.0162 and cold −0.0113 → +0.0185, and
   these are the **largest** gains. Why does that matter more than the headline +0.0223?
5. Why was the arm chosen on **validation** and not on test? What would choosing on test
   have repeated? (A1's Finding 5.)

**Do not claim:** that rack normalisation is a new idea discovered this week. It is D40's
option B, rejected in September because Q3 needed a change to the *official baseline*, and
it was named in §10 of the first design note. Say that — it is stronger, not weaker.

---

## Section 3 — Serving and scale

**Numbers:** MIND feature stage p50 252.16 → 3.18 ms, total p99 509.67 → 30.53 ms, 19.5x /
16.7x. EB-NeRD p50 speedup 27.6–33.9x. Footprint 283 MB / 476 MB. Profiles: 50,000 MIND
users in 18.7 s (0.37 ms/user) vs ~30 ms/user per request — **81x**. Cost per 1,000 queries
$0.003078 → $0.000162 (MIND).

**The honest framing, which is the interesting part (D44b):**

| p99, ms | warm | cold |
|---|---|---|
| retrieve (stage 1, unchanged by this work) | 24.38 | 121.49 |
| online features (what changed) | 6.70 | 6.76 |
| online total | 48.93 | 125.47 |

**Questions:**
1. Why is 66 Polars collections per request a *design* problem rather than a tuning problem?
2. What is the difference between batch throughput and serving latency, and why is a system
   tuned for one usually mis-shaped for the other?
3. The nightly profile job moves work off the request path. What does the system lose, on a
   dataset where 92.7% of clicks are on fresh articles?
4. A replica scaling out under load starts cold. Why is that the worst possible moment, and
   what is the fix?

**Do not claim:** "the pipeline now meets a p99 < 100 ms SLA". It does warm and does not
cold, and the failure is in a stage this work never touched. Claim instead that the
**feature stage** is no longer the bottleneck (6.7–8.3 ms across every run and both memory
states) and that the remaining risk is cold-start page faults.

---

## Section 4 — Where it breaks at 10x

**Numbers in `SCALE_NOTES.md`:** exposure key array 2 G int64 = 16 GB at 10x (first wall);
per-user profile building ~8M users x 3.4 ms ≈ 7.5 h; wall clock ~26 h; embedding matrix
193 MB grows with the corpus, so cold-start pre-faulting gets worse while the SLA does not.

**Questions:**
1. Which component hits its limit *first*, and is that an algorithmic or a provisioning
   problem?
2. Why does the batch path degrade differently from the per-request path at 10x?
3. Why does the corpus tier not sharded by user, while tiers 2 and 3 do?

---

## Section 5 — Anti-gaming (Q9), if you keep it as its own section

MIND honest 0.6144 vs leaky 0.5994, paired −0.0150 — **cheating made it worse**, and the
reason is mechanical: the forward window is clipped by the end of the log, so
`future_exposure_share_24h` inflates 3.2x at test time. EB-NeRD is the number to quote for
the real price: +0.0162 [0.0153, 0.0172].

**Question:** why is the MIND result *not* evidence that leaks are harmless?

---

## A theme worth a paragraph, in your own words

Three separate times this week a measurement was disbelieved and re-run, and twice the
re-run changed the conclusion:

- A 665x serving speedup that was partly a contended machine (run 1 vs run 2).
- A 14–22 s batch tail that was mostly memory state (run 3 on a fresh VM: 2.7 s).
- An SLA claim that held warm and failed cold — **stated to you, then withdrawn**.

The generalisation, from this project's own error log: *on this machine a latency measured
once is not a measurement*. You have three concrete instances. That paragraph is the kind
of thing a viva rewards and no generated report contains, because it requires having been
there.
