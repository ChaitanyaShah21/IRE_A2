# AI Usage Log

Required by assignment Q7.4: all prompts, chat history, and marking of AI-generated
versus human-written code.

## Tool used
Claude Code (Anthropic), operating under the contract in `CLAUDE.md`. Model varies by
session (Opus 5 for Phase 0 scaffolding, Sonnet 5 from the Phase 1 session onward per
Chaitanya's `/model` choice) — noted per-commit in git history, not tracked here.

## Authorship marking

| File | Authorship | Notes |
|---|---|---|
| `CLAUDE.md` | AI-generated from human specification | Chaitanya specified every rule (incl. R10, added 2026-08-22 after he asked how to catch such bugs automatically); wording is AI |
| `PROMPT.md` | AI-generated | Verbatim copy of `CLAUDE.md` |
| `ARCHITECTURE.md` | AI-generated, human-decided | All decisions chosen by Chaitanya |
| `PROGRESS.md` | AI-maintained | |
| `GLOSSARY.md` | AI-generated | |
| `LEARNING.md` | AI-generated | Reading list + recall-check outcomes |
| `.gitignore` | AI-generated | |
| `requirements.txt` | AI-generated, human-decided | Chaitanya chose venv+requirements.txt over Poetry/conda (D4) |
| `notebooks/00_provided_*.ipynb` | **Supplied with the assignment** | Not our work; reference only |
| `data/raw/**`, `data/processed/**` | Not authored — downloaded/generated data | Gitignored, never committed |
| `src/newsrec/ingest_mind.py` | AI-generated, human-decided | Every schema/design choice (D3, D5) chosen by Chaitanya; one bug (entity-JSON delimiter collision) and one type fix (subcategory) caught by Chaitanya before/while running |
| `src/newsrec/ingest_ebnerd.py` | AI-generated, human-decided | Context-`article_id` inclusion (D6) decided by Chaitanya |
| `src/newsrec/temporal_split.py` | AI-generated, human-decided | Split-source and split-ratio decisions (D7, D8) chosen by Chaitanya |
| `src/newsrec/build.py` | AI-generated, human-decided | Feature-store layout (D9) chosen by Chaitanya |
| `scripts/build_pipeline.py` | AI-generated, human-decided | No-auto-download design (D10) chosen by Chaitanya |
| `configs/mind.yaml`, `configs/ebnerd.yaml` | AI-generated | Raw-data paths, per D10/the Phase 0 "no hardcoded paths" layout decision |
| `src/newsrec/retrieval/bm25.py` | AI-generated, human-decided | Tokenisation, parameters, implement-vs-import, and query-term weighting (D11, D13, D14, D16) chosen by Chaitanya |
| `tests/test_bm25_index.py` | AI-generated | R10 adversarial suite, 18 tests; the Danish-tokenisation case was recorded as a requirement in D11 before the code existed |
| `pytest.ini` | AI-generated | Puts `src/` on the path so `pytest` works from the repo root |
| `src/newsrec/retrieval/bm25_search.py` | AI-generated, human-decided | Query construction, cold-start handling, and the availability variant (D12, D15, D16, D17, D19) chosen by Chaitanya, who also challenged whether D19 was permitted by the spec — the compliance argument now in D19 exists because he asked |
| `src/newsrec/eval/recall.py` | AI-generated, human-decided | Macro-vs-micro averaging (D18) chosen by Chaitanya |
| `tests/test_bm25_search.py` | AI-generated | R10 adversarial suite, 20 tests, batch-invariance included |
| `scripts/run_bm25_recall.py` | AI-generated | Thin entry point for Q2.4 |
| `scripts/summarise_bm25_recall.py` | AI-generated | Adds the random-baseline column without which the D19 comparison misleads |
| `reports/bm25_recall_*.csv` | Generated output | Not authored; reproducible via the two scripts above |
| `requirements.txt` (Phase 3 additions) | AI-generated, human-decided | D20's route chosen by Chaitanya, who asked the question that settled it — whether using a library here conflicts with the assignment. The CPU-index lines exist because the naive install was *measured* at 2,894 MB, 2,238 MB of it unusable CUDA |
| `src/newsrec/retrieval/semantic.py` | AI-generated, human-decided | Model, search method and storage layout (D20, D21, D22) chosen by Chaitanya; the library-vs-implement question was raised by him and the compliance argument in D20 exists because he asked it |
| `tests/test_semantic_embeddings.py` | AI-generated | R10 adversarial suite, 15 tests. The two null-representation cases (MIND null vs EB-NeRD blank) were found by checking the real store before writing the code, not after a traceback |
| `scripts/build_embeddings.py` | AI-generated | Thin entry point for Q3.1; kept out of build_pipeline.py per D22 |
| `data/processed/embeddings.parquet` | Generated output | Not authored; reproducible via the script above. Gitignored |
| `src/newsrec/retrieval/semantic_search.py` | AI-generated, human-decided | Q3.3 mean pooling and the D19 two-pool constraint follow Chaitanya's earlier decisions; the -inf masking fix and the MIN_NORM threshold were found by mutation-testing the tests, not by a failure |
| `tests/test_semantic_search.py` | AI-generated | R10 adversarial suite, 21 tests, built so the wrong implementation visibly fails - verified by deliberately reintroducing each bug and confirming the tests catch it |
| `src/newsrec/retrieval/availability.py` | AI-generated | D19 logic extracted from run_bm25_recall.py so both retrievers share one implementation; regression-verified against the committed Q2 numbers |
| `scripts/run_semantic_recall.py` | AI-generated | Thin entry point for Q3.4, deliberately the same shape as the BM25 runner so Q3.5 compares methods not harnesses |
| `scripts/summarise_recall.py` | AI-generated, human-edited history | Was `summarise_bm25_recall.py`; generalised to both methods for Q3.5. The random-baseline column it adds exists because Chaitanya's D19 discussion established that absolute recall alone misleads |
| `reports/semantic_recall_*.csv`, `reports/recall_summary.csv` | Generated output | Not authored; reproducible via the scripts above |
| `CLAUDE.md` / `PROMPT.md` (R1 amendment) | AI-written, human-directed | Chaitanya directed the change: drop required reading, teach in chat plain-to-technical. Rationale and stated cost written by Claude |

| `src/newsrec/eval/metrics.py` | AI-generated, human-decided | Q4.1 AUC/MRR/nDCG. The tie policy (D23) was chosen by Chaitanya from measured tie rates; AUC uses the rank identity rather than the O(P·N) pair loop |
| `tests/test_metrics.py` | AI-generated | R10 adversarial suite, 28 tests. Verified by mutation testing: 7 deliberate bugs reintroduced (uncapped IDCG, inverted tiebreak, `rankdata` tie method, removed NaN guard, argsort-stability tiebreak, MRR off-by-one, DCG discount off-by-one) and every one was caught |

| `src/newsrec/eval/rerank.py` | AI-generated, human-decided | Q4.2 four scorers. D24's baselines chosen by Chaitanya. The decisions NOT to apply D15/D19 here, and to bank the seen-before signal for Q9 instead of folding it into the score, follow his earlier D17 reasoning |
| `tests/test_rerank.py` | AI-generated | R10 adversarial suite, 21 tests, alignment-focused. Mutation-tested: 7 bugs reintroduced, 6 caught, and the 7th identified as a no-op mutation rather than a test gap |
| `scripts/run_rerank_eval.py` | AI-generated | Thin entry point for Q4.2; filename carries every varying input per the Q2 overwrite error-log entry |
| `reports/rerank_*.parquet` | Generated output | Not authored; gitignored, regenerable via the script above |

| `src/newsrec/eval/beyond_accuracy.py` | AI-generated, human-decided | Q4.3. D25's two forks (which output to measure, which diversity basis) chosen by Chaitanya. Both diversity metrics use closed forms; the tests keep brute-force versions to check them against |
| `tests/test_beyond_accuracy.py` | AI-generated | R10 adversarial suite, 23 tests. Mutation-tested: 7 bugs reintroduced, all 7 caught |
| `scripts/run_beyond_accuracy.py` | AI-generated | Thin entry point for Q4.3; runs both the retrieval and re-ranking outputs so D25's candidate-pool cap is shown rather than asserted |
| `reports/beyond_accuracy_*.csv` | Generated output | Not authored; reproducible via the script above |

| `src/newsrec/eval/slices.py` | AI-generated, human-decided | Q4.3 slicing. D26's two definitions chosen by Chaitanya against measured distributions; the exposure-from-candidates-never-clicks rule follows his D19 reasoning |
| `src/newsrec/eval/bootstrap.py` | AI-generated, human-decided | Q4.4. D27 (coverage reported without a CI) decided by Chaitanya after asking for the bias to be explained in plain terms and for the A-vs-B trade-off, which is what surfaced that option B does not remove the need for the explanation |
| `tests/test_bootstrap.py` | AI-generated | R10 adversarial suite, 31 tests covering both modules, including a calibration test. Mutation-tested: 8 bugs reintroduced, all 8 caught |
| `scripts/run_eval_report.py` | AI-generated | Thin entry point for Q4.3 slices + Q4.4 CIs over the re-ranking metrics |
| `reports/eval_report_*.csv` | Generated output | Not authored; reproducible via the script above |

| `src/newsrec/eval/ablation.py` | AI-generated | Q9's serving-time ablation (D28). Contains a deliberately leaky function, quarantined and asserted un-imported by a test |
| `tests/test_ablation.py` | AI-generated | R10 adversarial suite, 14 tests. Mutation-tested: 6 bugs reintroduced, all 6 caught |
| `src/newsrec/ingest_ebnerd.py` (A2, D33 sample filter) | AI-generated, human-decided | Sample size and the `user_id % 100` mechanism chosen by Chaitanya from measured options |
| `src/newsrec/build.py`, `scripts/build_pipeline.py` (A2, D33) | AI-generated, human-decided | Repoint-the-existing-config over a second config, chosen by Chaitanya |
| `configs/ebnerd.yaml` (A2) | AI-generated, human-decided | `raw_root` → `ebnerd_large`, `user_sample_pct: 5` per D33 |
| `tests/test_user_sample.py` | AI-generated | R10 suite, 11 tests. Mutation-tested: 4 bugs reintroduced; the first run caught 3, and the survivor (`% 10` for `% 100`) exposed a gap in the test data, fixed by adding user 110 |
| `src/newsrec/features/history.py` | AI-generated, human-decided | Q1.1 decay features. D34/D34a/D35 chosen by Chaitanya. His answer to the negative-Δt check question is the reason the guard raises rather than clips |
| `tests/test_history_features.py` | AI-generated | R10 suite, 25 tests. 9 of 9 mutations caught after two test-data gaps were closed |
| `src/newsrec/features/article.py` | AI-generated, human-decided | Q1.3 freshness and exposure popularity. D34b and D34c chosen by Chaitanya |
| `tests/test_article_features.py` | AI-generated | R10 suite, 13 tests. 8 of 9 mutations caught; the 9th proven equivalent by removing both guards |
| `src/newsrec/features/session.py` | AI-generated, human-decided | Q1.2 session features; D34a (label-free) chosen by Chaitanya |
| `tests/test_session_features.py` | AI-generated | R10 suite, 8 tests, 6 of 6 mutations caught |
| `src/newsrec/features/assemble.py` | AI-generated, human-decided | Q1 feature table; the allowlist reflects D34/D34a/D34b/D34c/D35, all chosen by Chaitanya |
| `src/newsrec/features/unavailable.py` | AI-generated | Q9 quarantine arm; never imported by production code (asserted) |
| `tests/test_feature_table.py` | AI-generated | Allowlist and quarantine assertions |
| `tests/test_no_leakage.py` (A2 extension) | AI-generated | Future-deletion and label-blindness properties on both datasets; 4 of 4 planted forward leaks caught after extending to MIND |
| `reports/NUMBERS.md` | AI-generated, human-directed | Chaitanya asked for a single numbers ledger after Quiz-1 showed answers are cross-checked against the repo. Values are measured or marked as estimates; provenance recorded per row |
| `tests/test_no_leakage.py` | AI-generated | The Q9 deliverable. Mutation-verified: 5 deliberate leaks reintroduced, all 5 caught, including relaxing D19's strict inequality. The EB-NeRD history landmine it tests was found by Chaitanya's earlier D19 discussion insisting availability be label-free as well as temporal |
| `scripts/run_ablation.py` | AI-generated | Thin entry point for Q9 |
| `reports/ablation_*.csv` | Generated output | Not authored; reproducible via the script above |

| `src/newsrec/submission.py` | AI-generated, human-decided | Phase 5 / Q5 readers for the two unlabeled leaderboard bundles (D30). The platform fork it sits under (D29) was chosen by Chaitanya against measured numbers. Handles all three Phase 5 landmines, each verified against the real bundles first |
| `scripts/build_submission_store.py` | AI-generated | Thin entry point; checks every requested bundle before writing any of them, so a missing second dataset does not surface after the first is on disk |
| `tests/test_submission.py` | AI-generated | R10 adversarial suite, 15 tests, all on constructed files the real bundles do not contain. Mutation-tested: 10 bugs reintroduced, 9 caught and **the 10th a genuine gap** (the guard's *call site* was untested) — test added, re-mutated, now 10/10 |
| `configs/{mind,ebnerd}.yaml` | AI-generated, human-edited | `test_root` added in Phase 5, kept as a separate key from `raw_root` so the leaderboard test set cannot be confused with D7's local test split |
| `data/processed/submission/*` | Generated output | Not authored; gitignored, reproducible via the scripts above |

_Appended as files are created._

## Assignment 2 — authorship

A2 is nominally a team assignment for two and is being done **solo**, which the spec
permits. Every file below is therefore Chaitanya's work with AI assistance under the
`CLAUDE.md` contract — there is no second human author to distinguish from.

Everything inherited from A1 keeps the authorship marking recorded in the table above;
the A2 rows cover only what A2 adds or changes.

| File | Authorship | Notes |
|---|---|---|
| `A2.md` | Course-provided | The assignment specification, unmodified |
| `CLAUDE.md`, `PROMPT.md` | AI-edited, human-decided | A2 sections §0/§4/§5/§6/§7 rewritten; rules R1–R14 unchanged from A1. The four planning-stage choices (repo layout, NRMS route, EB-NeRD scale, pacing) were put as options with trade-offs and chosen by Chaitanya |
| `PROGRESS.md` | AI-maintained | Rewritten for A2; A1's archived to `archive/A1_PROGRESS.md` with its error log carried forward inline |
| `ARCHITECTURE.md` | AI-generated, human-decided | A2 section appended from D33; D1–D32 unchanged |
| `requirements.txt` | AI-edited | `lightgbm==4.7.0` added, verified on aarch64 before pinning |

_(Rows are added as each A2 file is written, per R14 — reconstructing authorship after
the fact is exactly what this section exists to avoid.)_

---

## Prompt log
Exported to `reports/ai_transcripts/` — **12 sessions, 155 prompts**, 21–27 August 2026.
Start at `reports/ai_transcripts/index.md`.

Each file is one Claude Code session, oldest first, containing the prompts as typed.
Assistant tool activity is summarised between prompts rather than reproduced, and long
pasted terminal output inside a prompt is clipped to its head and tail with an explicit
elision marker. Both choices serve the same end: the raw session logs are ~15 MB of tool
inputs and outputs, which is not a prompt log and would bury the thing being logged. The
log is 112 KB. Regenerate with:

```bash
python scripts/export_ai_transcripts.py                      # prompt log (default)
python scripts/export_ai_transcripts.py --full               # also include assistant prose
python scripts/export_ai_transcripts.py --max-prompt-lines 0 # no clipping
```

Two things the exporter deliberately excludes, both of which would otherwise misrepresent
the record: sub-agent (`isSidechain`) conversations, which nobody typed, and harness-
injected `user` records — slash-command echoes, caveat banners, captured stdout. The
latter had inflated the count by 9 before they were filtered. Message-queue credentials
and pre-signed URL signatures appearing in pasted terminal output are masked.

| `src/newsrec/predict.py` | AI-generated | Q5 rank-vector writer and zip packager. The inverse-permutation trap it exists to prevent was found by reading both competitions' published worked examples out of Codabench's API, not by inspection |
| `tests/test_predict.py` | AI-generated | R10 adversarial suite, 22 tests, pinned against BOTH competitions' own worked examples plus a derived round-trip check so a mis-transcribed example cannot validate a wrong implementation |
| `scripts/run_submission.py` | AI-generated | Chunked, streaming submission generator; never materialises the split, user vectors go to an on-disk memmap, scoring matrix restricted to articles that can actually be candidates |
| `scripts/validate_submission.py` | AI-generated | Pre-flight validator. Exists because a submission cannot be debugged from a leaderboard - it returns one number and no diagnostics |
| `README.md` | AI-generated, human-decided | Q7 deliverable #1 ("README.md with one-command reproduce"), which the repository was missing entirely until Phase 5. Results tables are copied from measured runs; step timings that were never stopwatch-timed are marked as such rather than estimated |
| `reports/submissions/*` | Generated output | Not authored; gitignored, reproducible via the scripts above |

| `src/newsrec/eval/rerank_variants.py` | AI-generated | Phase 5b: max-similarity user representation, per-impression normalisation, weighted fusion. Kept separate from `rerank.py` so the four scorers behind every Q4 number stay untouched |
| `scripts/tune_rerank.py` | AI-generated | The N sweep (D31). Its fusion stage was mis-designed - seven metrics per combination, a redundant 4-way grid, no progress output - and was killed after an hour; superseded by `tune_fusion.py` |
| `scripts/tune_fusion.py` | AI-generated | The corrected fusion search: AUC only, one weight pinned, popularity dropped on a measured transferability check. ~2 min for the same answer |
| `scripts/run_submission.py` (`--n-recent`) | AI-generated, human-decided | Chaitanya asked how to improve the leaderboard result, which is what prompted the N re-tune; output filenames now carry N so a retuned run cannot overwrite an earlier submission |

| `reports/design_note.md`, `reports/design_note.pdf` | AI-generated, human-decided | The Q6 deliverable. Chaitanya chose the balance (~2 pages engineering / ~2 pages findings) and directed what to cut when it ran a page over. Every number in it traces to a measurement in `ARCHITECTURE.md` or `SCALE_NOTES.md`; none were written from memory |
| `scripts/build_design_note_pdf.py` | AI-generated | Renders the note and **reads the page count out of the PDF's own page tree** rather than estimating from word count. Written because Q6's 4-page cap is a property of the rendered document and was never being checked — the first run found it at 5 pages. Fixed by typography alone, so no content was cut |
| `reports/figures/mind_csharp.png`, `reports/figures/ebnerd_csharp.png` | **Not authored** — leaderboard screenshots captured by Chaitanya | Q5/Q7 evidence. The EB-NeRD score was obtained by attaching a self-hosted worker to the competition queue per the organizers' documented procedure; the scoring program, hidden reference data and metrics are the organizers' own and unmodified |
| `scripts/benchmark_engineering.py` | AI-generated | Latency/throughput/footprint measurements after the course email named these as grading criteria. Results in `SCALE_NOTES.md`; every figure in the design note's engineering section comes from here rather than from an estimate |
| `SCALE_NOTES.md` | AI-maintained | "Where this breaks at 10×" observations, recorded as they occurred rather than reconstructed |
| `requirements-dev.txt` | AI-generated | Test/lint tooling, kept separate so the reproduce path does not install it |
| `src/newsrec/__init__.py`, `src/newsrec/{eval,retrieval}/__init__.py` | AI-generated | Package markers, empty |
| `A1.md` | **Supplied with the assignment** | The specification. Not our work; quoted from, never edited |
| `AI_USAGE.md` | AI-maintained | This file |
| `.claude/settings.local.json` | AI-generated | Local tool-permission settings; no project logic |
| `scripts/export_ai_transcripts.py` | AI-generated | Produces this file's prompt log (Q7.4). There is no CLI export flag and the in-session `/export` covers only the current conversation, which would have missed 11 of the 12 sessions |
| `reports/ai_transcripts/*` | Generated output | Not authored; reproducible via the script above |
| `codabench/` (removed) | AI-generated | Tooling written on 2026-08-27 to get the EB-NeRD submission scored after the competition's own compute workers were retired. **Removed from the repository** as infrastructure rather than pipeline work; it remains in git history. Recorded here because it was authored during the project even though it is no longer part of it |

### Assignment 2, Phase A3 (2026-09-19). Written while Chaitanya was away, at his request to "do anything that you can do on your own first"

| File | Authorship | Notes |
|---|---|---|
| `src/newsrec/rank/gbdt.py` | AI-generated | Q2's LambdaRank re-ranker. Landmine 4 (contiguous groups) is enforced from the ids, not trusted |
| `tests/test_gbdt.py` | AI-generated | 9 tests. The first version of the planted-signal test failed, which is how the "trees read absolute values" property recorded under D36 was found |
| `src/newsrec/eval/bootstrap.py` (`paired_bootstrap_diff`) | AI-generated | Q3.4's paired CI. NaN is dropped jointly, so the pairing cannot silently dissolve |
| `src/newsrec/features/assemble.py`, `article.py` (context/rows split, `ExposureIndex`) | AI-generated | Refactor for the 206M-row leaderboard. Verified by rebuilding the cached tables: EB-NeRD byte-identical, and MIND differed, which exposed the reused-id bug |
| `src/newsrec/submission.py` (session columns) | AI-generated | Leaderboard loader now carries `session_id` and `device_type`, cast as in the training store |
| `scripts/build_feature_tables.py`, `run_reranker.py`, `run_retrieved_regime.py`, `run_submission_lgbm.py` | AI-generated | Cache the feature tables, run Q2 in both regimes, and produce the leaderboard submission |
| `src/newsrec/rank/nrms.py`, `tests/test_nrms.py`, `scripts/run_nrms.py` | AI-generated | Q3's NRMS over frozen sentence embeddings (D39, provisional), plus the time-term improvement hook |
| `reports/rerank_*.csv` | Generated output | From `run_reranker.py` |
| `reports/figures/{mind,ebnerd}_a2_leaderboard.png` | **Not authored** — Codabench screenshots captured by Chaitanya, 2026-09-20 | Q5/Q7 evidence for the A2 submissions: MIND 0.6181 (sub 934561), EB-NeRD 0.7397 (sub 934124). The EB-NeRD score was produced by a self-hosted worker built from upstream's own source, following the organisers' documented procedure; their scoring program, hidden reference data and metrics are unmodified |
| `src/newsrec/features/rack.py`, `tests/test_rack_features.py` | AI-generated, **AI-decided** | D42, extension week. Chaitanya was sitting examinations and asked for the work to proceed without him, with the decisions reviewed together afterwards — so unlike every row above, the choice of normalisation (percentile **and** z-score, base features kept, ten of the fourteen columns) was made by Claude under R8, not by him. `ARCHITECTURE.md` records the alternatives rejected so the review is possible. 19 tests, 13 of 13 mutations caught |
| `src/newsrec/rank/words.py`, `scripts/build_word_vocab.py` | AI-generated, **AI-decided** | D43. Vocabulary, GloVe loading and title tokenisation for the faithful NRMS news encoder. `TITLE_LEN = 20` is set from a measurement of MIND's title lengths (p99 = 21, 98.9% of titles kept whole), not from the paper's 30 |
| `src/newsrec/rank/nrms.py` (`WordNewsEncoder`) | AI-generated, **AI-decided** | D43. Added beside the existing encoder, which stays the default, so every NRMS number already reported is unaffected |
| `src/newsrec/serving.py`, `tests/test_serving.py` | AI-generated, **AI-decided** | D44. The online request path, written after profiling showed 66 Polars collections per request. Its licence to exist is the equality test against `assemble.build_rows` on real requests from both datasets |
| `src/newsrec/features/assemble.py` (empty-history guard) | AI-generated | Fix for a latent `IndexError` the D44 test surfaced in shipped code; see the error log |
| `data/raw/glove/glove.6B.*` | **Not authored** — downloaded (Stanford GloVe, 6B tokens, via the HuggingFace mirror) | Gitignored. Verified byte-exact against the server's `Content-Length` before use |
| `scripts/diagnostics/*` + its README | AI-generated, **AI-decided** | The measurement scripts behind `NUMBERS.md` section K. Recreated in the repository after the originals were lost with `/tmp` when WSL restarted; the mutation suite (13/13) and the variance table were re-run and reproduce exactly, so these are verified rather than reconstructed from memory |
| `scripts/compare_rack.py` | AI-generated, **AI-decided** | D42's paired comparison of the rack model against the shipped one |
| `scripts/run_nrms.py` (checkpointing, resume, column pruning, `--word-level`, `--tag`, `--val-impressions`) | AI-generated, **AI-decided** | Per-epoch checkpoints written temp-then-rename; resume verified by forging a checkpoint back an epoch |
| `scripts/run_reranker.py` (`--features rack`), `run_extended_eval.py` (`--extra-models`), `benchmark_serving.py` (`--online`, `--model-tag`), `run_submission_lgbm.py` (widened allowlist guard) | AI-generated, **AI-decided** | Extension-week arms routed through the deliverable scripts rather than scratch ones, so every reported figure has a committed command |
| `tests/test_feature_table.py` (allowlist contract), `tests/test_nrms.py` (word-level learning) | AI-generated | The allowlist test was updated to D42's contract keeping exact equality including order, not relaxed to a subset; the NRMS addition proves the word-level encoder learns a signal carried only by token ids |
| `reports/report_prep.md` | AI-generated **scaffolding**, contains no report prose | Q6 requirements, figures with provenance, questions for Chaitanya to answer in his own words, and the claims not to make. Written this way on purpose: the TA requires the report to be his, so this supplies facts and questions only |
| `reports/rack_vs_base_*.csv`, `extended_eval_*_rack.csv`, `serving_benchmark_*_rack.json`, `rerank_*_rack.csv` | Generated output | From B2–B5 in the README |
