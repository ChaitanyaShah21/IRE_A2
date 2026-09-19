# Progress — Assignment 2

**Read this first in every session (R11).** Last updated: 2026-09-19

---

## Where we are right now

**Phase A1 complete** — the feature store now holds a 5% user sample of `ebnerd_large`
(D33): 1,219,746 EB-NeRD impressions against the demo's 24,724. 251 tests pass.
The A1 recall quiz is done, the numbers ledger (`reports/NUMBERS.md`) exists, and D34's
evidence is gathered. **D34 decided: option B** (symmetric core + EB-NeRD session). **D34a, D35 decided. Step A2.1 done:** `features/history.py`, the multi-scale decayed user vectors,
category shares and hours-since-last-click, with the boundary guard. 25 tests,
9 of 9 mutations caught. **Step A2.2 done:** `features/article.py`, freshness from the
earliest evidence (D34c) and label-free exposure share at 1 h / 24 h (D34b). **Phase A2 complete** (tag `a2-phase-2-complete`): all Q1 features, the Q9 quarantine,
and the leakage test extended. 304 tests pass. The A2 recall quiz is answered (2 of 3,
Q2 re-taught; see `LEARNING.md`).

**HANDOFF 2026-09-19. Chaitanya is continuing in a new chat. Start here:**
1. **Confirm the scoped schedule. It was PROPOSED, not agreed.** The deadline is
   2026-09-20 and ~15 h of phases remain. The proposal:
   - A3 re-ranker, trained on the supplied inview lists first.
   - A4 with MIND NRMS only (drop-order item 3), keeping the paired bootstrap CI.
   - A5 and A6 trimmed to spec. The ledger and audit already cover much of Q4.
2. **Teach (R1)** gradient-boosted trees and LambdaRank (versus scoring each candidate
   independently) before any A3 code.
3. **R6 forks for A3:** D36, which rows train the re-ranker (the train split? with
   what history snapshot?), and D37, the candidate regimes (supplied inview vs
   retrieved top-K). Landmine 4 applies: LambdaRank needs rows grouped contiguously
   by impression, which must be asserted.
4. **Explanation style:** plain problem first, then a worked example, then the term.
   Chaitanya asked for this on 2026-09-19 after a dense summary.

**Feature table entry point:** `features/assemble.build_feature_table(dataset, target,
all_impressions, history, articles, emb_ids, emb)`. Fixed cost ~35 s (MIND) / ~75 s
(EB-NeRD) per call. Build per split and cache to `data/processed/` (gitignored).
**Schedule: 2026-09-18, two days to the deadline, with ~19 h of phase budget unspent.
The pre-agreed drop order below is now live.**

A1 is finished and frozen at `/home/csharp/IRE/A1` (tag `phase-5-complete`). This repo is
a clone of it with full history and all six A1 tags, so every A1 module, decision and
error-log entry is available here. **240 A1 tests pass in this location** — verified after
the move, not assumed.

**Deadline: 20 September 2026.** Five days from the A0 session.

---

## What A1 delivered, as inherited context

Do not re-derive any of this. Full detail in `archive/A1_PROGRESS.md` and
`ARCHITECTURE.md`'s decision log D1–D32.

| | MIND | EB-NeRD |
|---|---|---|
| Codabench leaderboard (final A1 system: semantic, N=100) | **AUC 0.6191, rank 54/90** | **AUC 0.5396, rank 147/247** |
| Offline val AUC, same system | 0.6489 | 0.5413 |
| recall@200, available pool (semantic) | 5.41% | 8.57% |

**The finding A2 exists to act on.** BM25 and embedding retrieval are structurally blind
to time — no time term exists anywhere in either formula — while **92.7% (MIND) / 93.5%
(EB-NeRD) of real clicks are on fresh articles**. Three independent routes reached it:
BM25's freshness profile matching the corpus baseline, semantic reproducing that exactly,
and train-window popularity predicting EB-NeRD clicks in the *wrong* direction
(AUC 0.4647). A2's behavioural features are the fix — which is why Q3's "one principled
improvement" comes from A1's own measurements rather than from a hyperparameter hunt.

**The claim worth defending at a viva.** The offline harness was calibrated against both
leaderboards and held twice, in two different senses: MIND transferred a *delta*
(predicted +0.0151, delivered +0.0154) while its absolute levels differed by ~0.030;
EB-NeRD transferred the *absolute level* (val 0.5413 vs leaderboard 0.5396, 0.0017 apart)
on the dataset where the same harness says the honest signal is weakest.

---

## Phase plan and budget

Budget ≈ 22 h across five days. Each phase ends: living-doc update (R12) → commit (R13)
→ tag. Recall quiz between phases (R5).

| Phase | What | Budget | Status |
|---|---|---|---|
| A0 | Migration & setup | 1 h | ✅ done — tag `a2-phase-0-complete` |
| A1 | Data scale-up: EB-NeRD subsample (D33) | 2 h | ✅ done — tag `a2-phase-1-complete` |
| A2 | Q1 — behavioural features + boundary contract (D34, D35) | 4 h | ✅ done (~4 h) — tag `a2-phase-2-complete` |
| A3 | Q2 — trained re-ranker, two candidate regimes (D36, D37) | 4 h | ⬜ **next** |
| A4 | Q3 — NRMS baseline, improvement, ablation, paired CI (D38–D40) | 5 h | ⬜ |
| A5 | Q4 serving/scale + Q5 extended eval + leaderboards | 3 h | ⬜ |
| A6 | Q6/Q7 — design note & deliverables | 3 h | ⬜ |

**Drop order if the schedule slips, agreed in advance 2026-09-15.**
1. Extra ablation arms beyond Q3.3's minimum.
2. Beyond-accuracy metrics for the retrieved-top-K regime.
3. EB-NeRD NRMS, keeping MIND NRMS.

**Not droppable:** the leakage test, the paired bootstrap CI, both leaderboard
submissions. These are named requirements, not depth.

---

## Done

### Phase A0 — migration & setup (2026-09-15)
- [x] `git clone /home/csharp/IRE/A1 /home/csharp/IRE/A2` — full history, all six A1 tags.
- [x] **Removed the inherited `origin` remote**, which the clone had pointed at A1. Left
      in place, a `git push` from A2 would have written into the frozen A1 repository.
      A2 gets its own remote when the Classroom repo exists.
- [x] Raw data **hardlinked** (`cp -al`), not copied: 7.1 GB available at zero disk cost,
      and raw data is never written. `data/processed` copied properly (5.0 GB) because A2
      rewrites it — this carries **43 minutes of one-off CPU embedding work** (both test
      article embedding sets and the N=100 user vectors) that would otherwise be redone.
- [x] `.venv` copied rather than re-resolved, saving a ~390 MB download over a connection
      that has already truncated one bundle on this project. **Its shebangs and the three
      `activate` scripts still pointed at A1** — left alone, `.venv/bin/pip install` in A2
      would have installed into *A1's* environment. Rewritten and verified against the
      thing that matters: `sys.prefix`, and where `pip --version` reports it lives.
- [x] **240 A1 tests pass from A2** in 12.4 s. Regression baseline established before any
      A2 code exists.
- [x] `A2.md` installed as the authoritative spec; `A1.md` kept because A2's Q2.1 reuses
      A1's candidate generator by name.
- [x] `CLAUDE.md` + `PROMPT.md` rewritten for A2 (§0 intro, §4 deliverables, §5
      environment, §6 traps, §7 pacing). Teaching rules R1–R14 carry over unchanged.
      Section replacement was done by a script that **fails loudly if a target string is
      absent or non-unique** rather than by `sed`, which would have silently matched
      nothing — the failure mode A1's error log records twice.
- [x] **LightGBM 4.7.0 pinned** after being verified twice over, not once: a native
      `manylinux2014_aarch64` wheel exists (3.3 MB, no new transitive dependencies), and
      then a planted-signal LambdaRank problem recovered the correct top-1 on **200/200**
      impressions against a random baseline of 20. Installing is not working — LightGBM
      needs an OpenMP runtime at import, and that is what the smoke test actually proves.
      The plan's "LightGBM aarch64 wheel fails" risk is retired.
- [x] A1's `PROGRESS.md` archived whole to `archive/A1_PROGRESS.md`; its **error log is
      carried forward inline below**, because R9 requires consulting it before debugging.

### Phase A1 — EB-NeRD data scale-up (2026-09-15)
1. ✅ **Checked:** `ebnerd_large/articles.parquet` and the testset's articles are
   **frame-equal** (same 125,541 rows and schema, compared after sorting). The embeddings
   in `data/processed/submission/embeddings_ebnerd.parquet` are reusable, which saves
   ~18 min of CPU.
2. ✅ **D33 decided:** 5% of users, `user_id % 100 < 5` → 48,666 users, 597,348 train +
   622,398 validation impressions. Uniformity of the ID residues and the history
   completeness were both verified. Full record in `ARCHITECTURE.md`.
3. ✅ **Implemented.** `ingest_ebnerd.user_sample_filter` is applied to the raw numeric
   `user_id` before prefixing, and pushed down into the Parquet scan.
   `configs/ebnerd.yaml` now points at `ebnerd_large` with `user_sample_pct: 5`; this
   was Chaitanya's choice over a second config, and A1's demo store reproduces from tag
   `phase-5-complete`. The rebuild took **40 s at 3.3 GB peak**.
   `scripts/assemble_embeddings.py` builds `embeddings.parquet` from existing vectors in
   7 s (MIND 65,238 + EB-NeRD 125,541, IDs matching the store exactly, unit norms
   verified by the production loader).
4. ✅ **Verified at the new scale:**
   - `train_max < val_min` and `val_max < test_min` for both datasets.
   - EB-NeRD impressions: train 597,348 / val 435,677 / test 186,721, totalling exactly
     D33's 1,219,746.
   - No out-of-sample user, no duplicate impression or article IDs.
   - **0** (split, user) pairs with impressions but no history row.
   - 14,541 history rows have no impressions in their split. That is expected, not an
     orphan: the validation snapshot serves both val and test, and (39,420 − 36,402) +
     (39,420 − 27,897) = 14,541 exactly. Never joined, so harmless.
   - MIND unchanged.
5. ✅ **`tests/test_user_sample.py`**, 11 tests, mutation-verified with 4 of 4 caught.
   The first pass caught only 3: `% 10` in place of `% 100` survived, because every
   test ID left the same remainder under both. Fixed by adding user 110 (remainder 10
   vs 0).

### Phase A2 — Q1 behavioural features (2026-09-18, in progress)
1. ✅ **D34 = option B, D34a = label-free session features, D35 = multi-scale decay.**
2. ✅ **`src/newsrec/features/history.py`:**
   - `decay_weights`: ages measured from the newest click; refuses negative or
     non-finite ages.
   - `build_decayed_user_vectors`: at h = ∞ it equals A1's vectors, verified exactly on
     constructed data and on 3,000 real MIND users.
   - `user_category_shares`.
   - `hours_since_last_click`: the boundary guard. It raises on a tie, a future click or
     mixed splits. It runs clean on all three real EB-NeRD splits, so the store contains
     no history click dated after its impression.
   - N = 100 comes from D31. The library default of 10 (D12, tuned for retrieval) would
     have silently compared against the wrong A1.
3. ✅ **`tests/test_history_features.py`**, 25 tests, 9 of 9 mutations caught. The first
   pass left **two survivors, both test gaps**:
   - The 'long history' user cycled through the same six articles, so head and tail
     were the same set. The same shape as D33's `% 10` survivor.
   - Removing the division by Σw looked harmless, because the vector is re-normalised
     anyway. It is not harmless: the MIN_NORM guard judges the length *before*
     re-normalising, so a near-cancelling pair of clicks would slip past it. Added the
     near-cancellation case.
4. ✅ **D34b (popularity = label-free exposure share, 1 h and 24 h) and D34c (freshness
   from the earliest evidence)** were decided when A2.2 surfaced them. Three findings:
   - **Click popularity is unusable on the testset**, which has no labels.
   - **It would leak into training rows** through their own clicks.
   - **A raw count is scale-dependent.** A 5% sample against the full leaderboard
     population would be ~20× off, so the feature is a share.
   - Separately, **1,810 EB-NeRD candidate rows (11 articles) are shown before their
     `published_time`**, most likely a republication overwriting the original stamp.
5. ✅ **`src/newsrec/features/article.py`**: `candidate_rows`, `freshness_hours`,
   `exposure_shares`. Vectorised with `searchsorted` over an (article, second) key, and
   strictly before *T*.
6. ✅ **`tests/test_article_features.py`**, 13 tests. 8 of 9 mutations were caught
   directly. The 9th (removing the window clamp) is an **equivalent mutant**, because the
   padding in `span` independently prevents the cross-article spill. Proven by
   experiment: removing *both* guards fails the test, with 30 borrowed impressions
   instead of 0. Removing either guard alone passes.
7. ✅ **`src/newsrec/features/session.py`**: session position (strictly earlier, ties
   shared), minutes since the session began, and device type. Label-free, EB-NeRD only.
   **Keyed by (user, session)**, because 1,032 `session_id`s are shared across users.
   Keyed by the ID alone, the longest 'session' is 14 days (two strangers merged). Keyed
   properly, the longest is 29 min. 37 real sessions cross the train/val boundary, so
   the features are computed across all splits.
8. ✅ **`tests/test_session_features.py`**, 8 tests, 6 of 6 mutations caught (including
   the session-ID-only key, and ties broken by file order).
9. ✅ **`features/assemble.py`**: one row per (impression, candidate). The explicit
   `FEATURES` allowlist has 10 features on MIND and 14 on EB-NeRD. The output columns
   are *asserted* to equal keys + label + allowlist. A1's scorers are features:
   `cos_inf` is A1's semantic score and `bm25` its lexical one. Smoke run on 200 val
   impressions:
   - MIND: 7,658 rows, label rate 4.0%, nulls only for the 281 rows with no user history.
   - EB-NeRD: 2,127 rows, label rate 9.4%, no nulls.
   - Fixed cost per build ~35 s (MIND) / ~75 s (EB-NeRD): the BM25 index plus three
     decayed-vector builds.
10. ✅ **`features/unavailable.py`**, the Q9 quarantine: `read_time`,
    `scroll_percentage`, `total_pageviews`, `future_exposure_share_24h`. A test asserts
    it is imported nowhere in the package.
11. ✅ **`tests/test_no_leakage.py` extended** with two properties, on real val data for
    **both** datasets:
    - *Future deletion:* delete every impression after τ; features at or before τ must
      be identical. The quarantined future feature *fails* the same check, which proves
      the check can see a leak.
    - *Label blindness:* shuffle the clicks; every feature must be identical.
    Mutation-verified with four realistic forward leaks planted in production code
    (forward exposure window, first_seen → last_seen, session start → last impression,
    a label-nudged feature). **All four are caught, but only after extending the test to
    MIND.** first_seen → last_seen survived on EB-NeRD alone, because there
    `published_time` almost always wins the min, so the first_seen path is exercised
    only on MIND.

---

## Next step

**Phase A2 — Q1 behavioural features (D34, D35).** The A1 recall quiz was answered
2026-09-15: 2 of 3 correct, the embedding-reuse check re-taught (see `LEARNING.md`).

**Waiting on Chaitanya: D34, the feature allowlist.** Evidence is gathered and three
options (symmetric core / + EB-NeRD session / + demographics) are written up in
`ARCHITECTURE.md`. Nothing is implemented until he picks one.
Then: teaching on exponential decay (R1), then the feature builders.
The EB-NeRD features must use the new store's `history_timestamps`. MIND's recency can
only use list position.

**Teaching owed before Phase A3 code** (R1, in chat): gradient-boosted decision trees and
why `lambdarank` differs from classifying each candidate independently.
**Before Phase A4:** NRMS's two attention layers, and what makes a bootstrap *paired*.

---

## Landmines — verified 2026-09-15 against the real files, carry into the code

1. **`total_pageviews` / `total_inviews` are already in our `articles.parquet` and contain
   the future.** They are whole-dataset aggregates. A feature builder that loops over
   article columns picks them up silently and nothing errors. → **the A2 feature set is an
   explicit allowlist, never a denylist.**
2. **"Present in the test file" ≠ "available at serving time."** EB-NeRD's test behaviors
   keeps `read_time`, `scroll_percentage`, `session_id`, `device_type` but drops
   `next_read_time` / `next_scroll_percentage`. `read_time` is measured *after* the
   impression is served, so Codabench accepting it does not make it honest. This is Q9's
   ablation arm, handed to us by the schema.
3. **MIND has no session or dwell fields, and `published_time` is null for every MIND
   article.** Freshness on MIND must come from `availability.first_seen_times` — already
   label-free, already a strict `<`. Recency decay on MIND can only use list position;
   EB-NeRD has real `history_timestamps`. Two different implementations, so per A1's
   AUC-rack-size and novelty-scale lessons **the two datasets' decay features are not
   comparable to each other**, and the design note must say so.
4. **LightGBM `lambdarank` requires rows grouped contiguously by impression.** A shuffle
   produces a model that trains happily and ranks garbage. Needs an assertion, not a
   comment.
5. **EB-NeRD's validation history contains 99.52% of train-window clicks** (22,143/22,249
   — A1's recorded landmine). `history.parquet` holds all three snapshots keyed by
   `split`, and 1,217 EB-NeRD users have all three rows, so a join on `user_id` alone
   silently attaches the wrong one and **nothing errors**.
6. **The EB-NeRD article catalogue contains the future** (found 2026-09-18, from
   Chaitanya asking why the large and test article tables are identical). One catalogue
   covers the whole collection period and ships in every bundle. It runs to
   **2023-07-11**, a month after the test week ends. **2,148 articles** were published
   after the train week ended and **1,069** after the validation week ended. So:
   freshness = `impression_time - published_time`, only for articles already published
   at that moment. **No catalogue-wide statistic** (counts, category frequencies, "exists
   in catalogue") is ever a feature. A1's candidate pools are unaffected: they use
   `first_seen_times` from impressions, with a strict `<`.
7. **EB-NeRD `session_id` is not unique across users** (found 2026-09-18). 1,032 IDs are
   shared, so any session grouping must key on **(user_id, session_id)**. Keyed on the
   ID alone, the longest 'session' is 14 days; keyed properly, 29 minutes.
8. **A1 measured recall@200 at 2–8%.** A two-stage pipeline evaluated over *retrieved*
   candidates will therefore have low absolute numbers **by construction**. Expected, and
   framed rather than hidden — it is exactly why both leaderboards score the supplied
   inview list instead.

---

## Where the data lives

Raw data is **hardlinked** from A1, so these are the same bytes on disk, not copies.

| Dataset | Bundle | Path | Notes |
|---|---|---|---|
| MIND | small (train + dev) | `data/raw/mind/MINDsmall_{train,dev}/` | 51,282 / 156,965 train; 42,416 / 73,152 dev |
| MIND | large test | `data/raw/mind/MINDlarge_test/` | 2,370,727 impressions, 120,961 articles, unlabeled. 1.5 GB |
| EB-NeRD | demo | `data/raw/ebnerd/ebnerd_demo/` | 11,777 articles, 24,724 train behaviors, 1,590 users. Fast dev loop |
| EB-NeRD | large | `data/raw/ebnerd/ebnerd_large/` | 12,063,890 train + 12,566,385 val behaviors, 125,541 articles. 3.4 GB. **A2's training source (D33)** |
| EB-NeRD | testset | `data/raw/ebnerd/ebnerd_testset/ebnerd_testset/` | 13,536,710 impressions. Note the **doubled** directory name |
| — | feature store | `data/processed/{articles,impressions,history,embeddings}.parquet` | **Rebuilt in Phase A1 (D33).** Articles: MIND 65,238 + EB-NeRD 125,541. Impressions: MIND 230,117, EB-NeRD 1,219,746 (5% of `ebnerd_large` users). EB-NeRD history 39,260 / 39,420 / 39,420 (train/val/test). Rebuild: `build_pipeline.py` then `assemble_embeddings.py` |
| — | submission store | `data/processed/submission/` | 5.0 GB — test article stores, test embeddings, N=100 user vectors. Carries 43 min of CPU |

**MIND large train/dev are NOT downloaded** (only small + large-test). MIND-small's
156,965 impressions across 50,000 users is ample to train a re-ranker, so this is a
deliberate non-issue rather than a gap — recorded so it is not rediscovered as one.

Disk: 64 GB used, 892 GB free. Not a constraint.

**Environment:** `.venv/` (Python 3.12.3), pinned in `requirements.txt`. Rebuild with
`python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Machine is
**aarch64** (= arm64; Snapdragon X Plus, Windows on ARM), 11 GB RAM + 16 GB swap, no GPU.

---

## How A2 will be examined — shape of Quiz-1 (received 2026-09-15)

Quiz-1 spent 70/100 marks on "the system you built", and those answers are cross-checked
against this repo and the Codabench entries in oral evaluation. Expect the same for A2.
Every number must trace to a file and a command:
- **Inventory with sizes:** documents, vocabulary, average tokens, postings, and index
  size against raw corpus size.
- **Memory tier** at query time, with the code line that makes it so.
- **Latency:** p50/p99 per stage at a stated K. Harness throughput (impressions/s) and
  indexing throughput.
- **Little's law check:** X ≤ 1/R with N=1, and the mechanisms (batching, precomputed
  user vectors) with *measured* gains.
- **Metric formulas**, the ground-truth source, slices, and ablations.

Graded on consistency and mechanism, not on how good the numbers are. Unmeasured means a
labelled estimate with its reasoning.

## Open questions

- **D33's subsample size** — to be decided in Phase A1 against measured ingest time and
  the width of the resulting confidence interval, not guessed.
- **GitHub Classroom repo for A2** — invite link not yet located. A1's was never found
  either. Does not block any local work; only affects where this eventually gets pushed.
  A2 currently has **no git remote**, deliberately.

---

## Error log — inherited from A1, still live

Every error hit, its root cause, and the fix chosen. Consult before debugging anything —
we may have already solved it.

| Date | Error | Root cause | Fix chosen | Trade-off accepted |
|---|---|---|---|---|
| 2026-09-16 | A fresh latency audit of the A1 system disagreed with the committed benchmark by up to 4.7x (semantic p50 8.15 ms vs a recorded 1.73 ms), on the same code and byte-identical data | **Not a code or measurement bug: the machine is slower today.** Re-running A1's *own* `benchmark_engineering.py` unchanged reproduced the slow figures (BM25 p50 15.23 ms vs 10.10 recorded; semantic 5.70 vs 1.73), so both runs were honest and the difference is machine state - CPU frequency/core placement on a big.LITTLE ARM laptop under WSL2, whose RAM allocation also changed between the two dates | Quote latency **with the date it was taken**, and keep both runs in `reports/NUMBERS.md` rather than replacing the old number with the new one. Re-ran the original script as the control *before* writing either figure anywhere | Ratios survive (semantic still faster per query than BM25, batching still helps); absolute milliseconds do not travel. One recorded *conclusion* did not survive and was corrected in `SCALE_NOTES.md`: batching throughput regressing past batch 32 did not reproduce - today it rises monotonically to 256 |
| 2026-08-25 | After a mutation-testing run, `tests/test_ablation.py` kept failing even though the source file was byte-identical to its pre-mutation backup (`diff` clean, `grep` showed the correct line) | Stale `__pycache__`. The mutate→test→restore loop rewrites the `.py` with `cp`, and Python served the **mutated bytecode** rather than recompiling — the restored file's mtime did not look newer to the import cache's check | `find . -name __pycache__ -path '*/newsrec/*' -exec rm -rf {} +` before re-running. Recorded as a standing hazard of the mutation-testing workflow rather than a one-off | None. Worth noting the failure *direction* is benign: a stale cache during the mutation step makes a mutation look **survived** (tests pass), which reads as a test gap and gets investigated. Every mutation reported as *caught* in Phases 3–4 is therefore still valid, since caught means the tests actually failed |
| 2026-08-25 | `reports/bm25_recall_val_n10.csv` silently lost EB-NeRD's whole-corpus results — noticed only because the consolidated summary table was missing four rows | The output filename contained the split and `n_recent` but **not the dataset or the pool**, so `--datasets mind` wrote to the same path `--datasets ebnerd` had just written. No error, no warning; the numbers were still correct on screen, just gone from disk. The class of bug where output *looks* fine because the wrong thing was overwritten, not corrupted | Put every varying input in the filename: `bm25_recall_{datasets}_{split}_n{N}_{pool}{tag}.csv`, with a comment recording why. Re-ran the four configurations; regenerated numbers matched the originals exactly, which also confirmed reproducibility | None — strictly more correct. Cost ~15 min of re-running MIND. Worth noting the near-miss: had the summary script not existed, the missing rows would likely have gone unnoticed into the design note |
| 2026-08-25 | `test_first_seen_times_takes_the_minimum` failed with `ComputeError: cannot cast 'Object' type` | Test-construction error, not a code bug: the test passed `np.datetime64` values into `pl.DataFrame`, which Polars treats as opaque Python objects rather than recognising as timestamps | Used Python `datetime` objects, which Polars maps to its native `Datetime` type | None — the production code was never involved; only the fixture was wrong |
| 2026-08-23 | `python scripts/build_pipeline.py` run from a directory other than the repo root (e.g. `/tmp`) crashed with `FileNotFoundError: configs/mind.yaml` — found because Chaitanya questioned whether the script's `sys.path` fix really made it runnable "from anywhere" | The `sys.path.insert` fix only made the *import* of `newsrec.build` independent of the caller's working directory (via `__file__`, which always resolves to the script's real location). `Path("configs") / ...` and `OUTPUT_DIR = Path("data/processed")` were still plain relative paths, resolved against whatever the shell's cwd happened to be — an inconsistency between two parts of the same file | Introduced one `REPO_ROOT = Path(__file__).resolve().parent.parent` constant and anchored every path in the script to it — `src/`, `configs/`, `data/processed/`, and the `raw_root` value read out of each YAML config | None meaningful — this is strictly more correct with no added complexity; verified by re-running the exact `/tmp` invocation that first exposed it, plus re-checking the happy path and the failure-message path both still work |
| 2026-08-22 | Not our bug — a caveat about the provided notebook: its printed MIND train time range (`"11/10/2019 10:00 AM to 11/9/2019 9:59:58 AM"`) is chronologically wrong | The notebook computed it with plain Python `min()`/`max()` on the raw time **strings**, which compares them lexicographically (character by character), not chronologically — `"11/10/..."` sorts before `"11/9/..."` as text even though Nov 9 is earlier in time | None needed in our code — `ingest_mind.load_behaviors` already parses `time` into a real `Datetime` via `.str.strptime()`, so `.min()`/`.max()` on our `timestamp` column are correct (verified: MIND train is actually Nov 9–14, dev is Nov 15). Just don't trust the provided notebook's printed ranges at face value. | None — this only cost us noticing it before it fed into the temporal-split design |
| 2026-08-22 | `pl.concat([mind_articles_df, ebnerd_articles_df])` raised `type Float32 is incompatible with expected type Float64` (column `sentiment_score`), and the same for `impressions`' `read_time` | MIND's null placeholder columns default to `Float64` (`pl.lit(None, dtype=pl.Float64)`), but EB-NeRD's real `sentiment_score`/`read_time`/`scroll_percentage` columns are natively `Float32` in the source Parquet files - the two tables' schemas looked compatible by eye (both "float") but weren't bit-for-bit identical types | Cast all three EB-NeRD columns to `Float64` explicitly in `ingest_ebnerd.py` | None meaningful - Float64 is strictly more precise, so casting up loses nothing; found by actually running `pl.concat()` as an adversarial test (R10) rather than assuming matching column names implied matching dtypes |
| 2026-08-22 | Caught before running, not a runtime error: `ingest_mind.load_articles` originally joined `title_entities`/`abstract_entities` into one string with `pl.concat_str(..., separator="||")` | A stray literal `"||"` inside either JSON string (e.g. inside `SurfaceForms` text pulled from an article) would make a later split on `"||"` produce more than two pieces, silently corrupting that row's entity data — flagged by Chaitanya, not found by testing | Switched to `pl.concat_list([...])`, storing the two JSON strings as a genuine 2-element list column instead of a delimited string — no separator, so nothing to collide with | None meaningful — `list[str]` is the more natural Polars representation here anyway; no downside versus the string-join approach it replaced |
| 2026-08-21 | `wget`/anonymous download of MIND from `huggingface.co/datasets/yjw1029/MIND` returns HTTP 401, `x-error-code: GatedRepo` | The HF mirror is a gated repo — requires a logged-in, access-granted HuggingFace account, not just a public URL. Likely there to gate MIND's original license terms. | Chaitanya creates a free HF account, requests access (usually instant), generates a read-only access token; download resumes once shared. EB-NeRD-demo is unaffected (open S3 bucket, no gate). | Adds a manual step outside the pipeline's control before MIND ingestion can start; considered going to the official MIND site instead but that's gated the same way, so no trade-off actually avoided. — **resolved**, Chaitanya downloaded both files manually. |
| 2026-08-21 | `python -m zipfile` on the first `ebnerd_demo.zip` download raised `BadZipFile: File is not a zip file`, even though `file` identified it as a valid zip | Download was truncated mid-transfer over an unstable connection (actual size 21,187,446 bytes vs. the server's reported `Content-Length` of 21,499,083 — ~311 KB missing from the end, exactly where a zip's central directory lives). The backgrounded `wget` still reported exit code 0 despite this, so exit code alone wasn't a reliable success signal. | Chaitanya re-downloaded manually; new file's byte count matches `Content-Length` and opens cleanly with `zipfile`. | Considered `wget -c` (resume) to avoid re-pulling ~20 MB, but resume can silently fail to reconcile on an unstable connection — chose a clean re-download instead since the file is small enough that the cost difference is negligible. |
