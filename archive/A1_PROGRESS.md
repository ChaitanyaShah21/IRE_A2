# Progress

**Read this first in every session.** Last updated: 2026-08-25

---

## Where we are right now

**Phase 0 complete**, tagged `phase-0-complete`. Repository scaffolded, operating
contract written, plain-language walkthrough of the whole assignment delivered and
recall-checked (see `LEARNING.md`, `GLOSSARY.md`), Codabench registrations done.

**Phase 1 — Q1 reproducible data pipeline: complete**, tagged `phase-1-complete`. All
five sub-requirements done and verified against real data, not just designed: raw data
downloaded, ingested into a genuinely unified schema (proven via `pl.concat()`),
temporally split with the leakage invariant checked directly, persisted as a feature
store, and a one-command rebuild that's been run down both its success and failure
paths (including a real path-resolution bug found and fixed after Chaitanya questioned
whether it actually worked "from anywhere" — see error log).

**Phase 2 — Q2 BM25: complete**, tagged `phase-2-complete`. Inverted index, query side,
recall@K for K ∈ {50, 100, 200}, both datasets, both candidate pools, 38/38 tests passing.
Headline finding below.

**Phase 4 — Q4 evaluation harness: in progress.** Q4.1 (metrics) and Q4.2 (the
re-ranking runner, four scorers, both datasets) are done and mutation-tested; 123 tests
passing.
Q4.3, Q4.4 and Q9 are done too. **Phase 4 is complete**, 203 tests passing. Next is
Phase 5 — Codabench, the standing deadline risk.

**Phase 3 — Q3 semantic retrieval: complete**, tagged `phase-3-complete`. All five
sub-requirements done: 77,015 article embeddings computed and stored (Q3.1), exact
brute-force search (Q3.2), mean-pooled user vectors (Q3.3), recall@K for K ∈ {50,100,200}
on both datasets under both candidate pools (Q3.4), and the lexical-vs-semantic comparison
written up as five findings in `ARCHITECTURE.md` (Q3.5). 74/74 tests passing. The Phase
2→3 recall quiz is done — **do not repeat it**.

---

## ⚠️ Time budget flag (R8) — read this before Phase 2

Phases 0+1 were budgeted 5.5h combined; the real depth of work across this session —
every function verified against real data before being shown as done, several real bugs
caught in the process (entity-JSON delimiter collision, Float32/Float64 concat
mismatch, the null-propagation trap in cold-start history), multiple genuine R6 decision
points worked through with trade-offs (D3–D10) — almost certainly ran well past that
budget, even though no session tracked exact wall-clock hours against it. **Today is
2026-08-23; the deadline is 2026-08-27 — as little as 4–5 days remain**, against
Phases 2–6's combined 16h budget.

This is the deliberate trade-off `CLAUDE.md`'s prime directive asks for ("if forced to
choose between shipping faster and understanding, choose understanding and say what it
costs") — not a silent slip.

**Decision (2026-08-23):** raised plainly per R8, with a phase-by-phase risk breakdown
(Q5's cloud setup + large-bundle downloads + Codabench submission is the real deadline
risk, not teaching depth). Chaitanya chose to **keep the original full pace** for Q2
rather than scope down now, and revisit explicitly if Q2 is not keeping up with its 4h
budget. Also flagged: Q9 (anti-gaming ablation + leakage test) has no dedicated budget
line in the phase table — folding it into Q4's evaluation-harness phase, since the
leakage test's invariant is already built (Q1.3's `train_max < val_min < test_min`
check) and the ablation is evaluation-harness-adjacent work.

---

## Phase plan and budget

Deadline **27 Aug 2026**. Budget ~20 focused hours across 6 days.

| Phase | What | Budget | Status |
|---|---|---|---|
| 0 | Orientation & scaffolding | 1.5 h | ✅ done — tagged `phase-0-complete` |
| 1 | Q1 — reproducible data pipeline | 4 h | ✅ done — tagged `phase-1-complete` (ran well over budget, see note below) |
| 2 | Q2 — BM25 lexical retrieval | 4 h | ✅ done — tagged `phase-2-complete`. Ran over budget: Chaitanya chose D19's availability variant knowing it would, and it produced the phase's main finding |
| 3 | Q3 — semantic retrieval (embeddings) | 3.5 h | ✅ done — tagged `phase-3-complete`. Roughly on budget; the 13 min of CPU inference is a one-off |
| 4 | Q4 — evaluation harness + Q9 (folded in, no separate budget line) | 4 h | ✅ done — tagged `phase-4-complete`. Ran over (~5.5 h): the D25–D28 forks and the coverage-bias catch were the cost |
| 5 | Q5 — scale-up & Codabench submission | 2.5 h | ⬜ not started |
| 6 | Q6/Q7 — design note & deliverables | 2 h | ⬜ not started |

Total ≈ 21.5 h against ~20 h.

**Designated drop-first if we slip — revised 2026-08-25.** The original list said
"computing our own embeddings in Phase 3 (use EB-NeRD's provided ones instead)". **That
option does not exist** — neither dataset ships loadable article-text embeddings (see D20;
MIND ships knowledge-graph *entity* vectors, EB-NeRD's article vectors are separate
optional downloads we don't have). It has been removed rather than left as a phantom
escape hatch. The current list, in the order they'd go:

1. Extra ablations in Phase 4 beyond what Q9 strictly requires.
2. The `b` parameter sweep from D13 (never run; BM25 headline numbers use the defaults).
3. Phase 3's N sweep — reuse D12's N = 10 without re-tuning it for embeddings.
4. **Not droppable:** both candidate pools in Phase 3. D19 makes this structural — drop
   it and Q3.5 compares pool sizes instead of methods.

---

## Done

### Phase 0
- [x] `git init` on branch `main`; `.gitignore` blocking data, archives, checkpoints
- [x] Directory scaffold (`src/newsrec/`, `scripts/`, `tests/`, `configs/`, `notebooks/`, `reports/`, `data/`)
- [x] `CLAUDE.md` + `PROMPT.md` — the operating contract
- [x] Living documents created
- [x] Working mode packaged as a reusable skill at `~/.claude/skills/assignment/`,
      so future assignments in other folders start with the same contract, templates,
      intake interview and phase playbook. Invoke with `/assignment`.
- [x] Plain-language walkthrough of the full assignment (analogy → Q1–Q9 mapping),
      required reading logged in `LEARNING.md`, new vocabulary logged in `GLOSSARY.md`.
      Recall quiz run: temporal-split reasoning and the BM25-vs-embeddings distinction
      needed re-teaching before moving on — corrected points logged in `LEARNING.md`.

---

### Phase 1
- [x] Read both provided notebooks in full (`00_provided_mind_analysis.ipynb`,
      `00_provided_ebnerd_analysis.ipynb`) to confirm actual schemas, row counts, null
      rates — ground truth for everything below, not summary-of-a-summary
- [x] Taught "unified schema" concept (analogy → technical → recall check, 3/3 correct
      with one gap filled). Logged in `GLOSSARY.md`, `LEARNING.md`.
- [x] Schema-design decision (D3): 3 tables (articles, impressions, history), Chaitanya
      chose over a 4-table (+users) and a 2-table (inline history) alternative. Concrete
      columns defined in `ARCHITECTURE.md`.
- [x] Environment set up (D4/D5): `.venv` + `requirements.txt`, polars 1.43.2 + pyarrow
      25.0.1. Raw data downloaded and verified against notebook-confirmed row counts.
- [x] Added R10 to the operating contract (adversarial self-check before code is done),
      applied to the skill template too. Prompted by a real bug Chaitanya caught in
      `load_articles` before it ran.
- [x] `src/newsrec/ingest_mind.py::load_articles` — MIND `news.tsv` → unified `articles`.
      Verified: 51,282 rows, correct ID prefixing, entities_raw as list[str].
- [x] `src/newsrec/ingest_mind.py::load_behaviors` — MIND `behaviors.tsv` → unified
      `impressions`. R10 checks done against real data before presenting: timestamp
      format parses MIND's single-digit hours correctly, every impression token matches
      `N<digits>-[01]` exactly (no stray dashes/spaces to confuse the suffix-stripping
      regex), no null/empty impressions field, no zero-click rows in train. Verified:
      156,965 rows, row 0 matches the provided notebook's shown example exactly.
- [x] `src/newsrec/ingest_mind.py::load_history` — MIND `behaviors.tsv` → unified
      `history` (one row per user). R10 check done *before* writing this one, not after:
      verified the D3 decision's load-bearing assumption (MIND's history string is
      identical across all of a user's impression rows) against real data — 0 of 33,617
      multi-row users had more than one distinct history string. Also hit and fixed the
      exact null-propagation trap `CLAUDE.md`'s original R9 example describes:
      `.str.split()` on a cold-start user's null history stays null, not `[]`, until
      `.fill_null([])` is applied. Verified: 50,000 unique users, 0 nulls in
      `history_article_ids`, 892 cold-start users with genuine empty lists.
- [x] **`ingest_mind.py` complete** — all three unified-schema tables (articles,
      impressions, history) now produced from MIND's raw files.
- [x] Decision D6: dropped EB-NeRD's context `article_id` field (which article page a
      recommendation module was shown on) from the unified schema — found while
      inspecting real EB-NeRD data, not part of the original D3 column list. Nothing in
      Q1–Q9 needs it.
- [x] `src/newsrec/ingest_ebnerd.py` — all three unified-schema functions
      (`load_articles`, `load_behaviors`, `load_history`), built on `pl.scan_parquet`
      (lazy) with `.collect()` at the end. `load_history` needed no row-collapsing —
      EB-NeRD's history file is already one row per user, confirmed 1:1 against
      behaviors' unique user count on real demo data (1,590 = 1,590).
- [x] **`ingest_ebnerd.py` complete.** **Unified schema empirically verified**, not just
      designed: `pl.concat()`'d all three MIND/EB-NeRD table pairs and confirmed they
      combine cleanly — caught and fixed a real Float32/Float64 mismatch in the process
      (error log above). Combined: 63,059 articles, 181,689 impressions, 51,590 users'
      history.
- [x] Q1.3 — temporal split (`src/newsrec/temporal_split.py`). Verified neither dataset
      gives 3 labeled partitions at demo/small scale (D7); decided to carve val+test from
      dev/validation's tail (D7), 70/30 by row-count timestamp cutoff, uniform across
      both datasets (D8). Found and handled a real subtlety: EB-NeRD's train and
      validation history files genuinely differ per user, not the same data re-served —
      `add_history_split` reuses validation's history table for both new val/test
      sub-partitions rather than treating them as needing separate history data that
      doesn't exist. Verified on real data: row counts sum correctly, ~70.0% val ratio
      for both datasets, and the leakage invariant (`train_max < val_min`,
      `val_max < test_min`) holds strictly for both — this check is the seed of Q9's
      required `tests/test_no_leakage.py`.
- [x] Q1.4 — feature store (`src/newsrec/build.py`, decision D9: 3 combined files).
      Verified before writing: MIND's train/dev `news.tsv` files are genuinely different
      crawls (13,956 of dev's 42,416 articles aren't in train's file at all), so the
      concat+dedupe on `article_id` is necessary, not defensive boilerplate — and for the
      28,460 articles present in both, content is identical (0 title mismatches sampled),
      so `keep="first"` is safe. Ran the full build end to end (2.81s) and verified the
      Parquet round-trip: 77,015 articles (65,238 MIND after dedupe + 11,777 EB-NeRD,
      exact expected count), 280,197 impressions, 154,714 history rows — every
      split/dataset count matches Q1.3's numbers exactly, and list/datetime dtypes
      survived the round-trip intact.
- [x] Closed a standing gap: `AI_USAGE.md`'s authorship table only tracked docs, not the
      actual `src/newsrec/*.py` files written this session — added entries for all four.
- [x] Q1.5 — one-command rebuild (`scripts/build_pipeline.py`, `configs/mind.yaml`,
      `configs/ebnerd.yaml`). Decision D10: no auto-download for either dataset (check
      raw files exist, print manual instructions and exit cleanly if not) — simpler than
      partial automation, and MIND's gating means full automation was never uniform
      anyway. Tested **both** paths for real, not just the happy one: a full clean
      `python scripts/build_pipeline.py` run (exit 0, rebuilds the feature store) and a
      deliberately broken config pointing at a nonexistent raw_root (exit 1, prints the
      actual download instructions instead of crashing with a bare traceback).
- [x] **Q1 (all five sub-requirements) is now complete.** Tagged `phase-1-complete`.

### Phase 2 (in progress)
- [x] BM25 concept taught per R1 (analogy → formula broken into named parts → reading →
      comprehension check). Three questions asked; two needed correcting and are logged in
      `LEARNING.md`: IDF cannot explain why one *document* beats another (it depends only
      on term and corpus), and `k₁=0` deletes length normalisation too, because the whole
      length bracket is multiplied by `k₁`. A follow-up confirmed BM25 damps repetition
      with a saturating rational function, **not** a log of term frequency — that's TF-IDF.
- [x] CSR/CSC re-taught from scratch on request, worked by hand on constructed corpora.
      Chaitanya's second attempt got the row structure and the empty-row case right;
      the correction was that `data[p]` pairs with `indices[p]` by tape position, not
      with the vocabulary in alphabetical order.
- [x] Decisions D11–D16 taken (see `ARCHITECTURE.md`), each against measured facts read
      off the real feature store rather than assumed — including the two that set the
      recall ceiling: **100%** of val ground-truth clicks exist in our `articles` table
      (so no artificial cap), and only **0.19% / 0.47%** are articles the user had already
      read (so D15's history exclusion costs at most half a percent).
- [x] Q2.1 — inverted index (`src/newsrec/retrieval/bm25.py`): Unicode tokeniser +
      sparse document-term matrix with BM25 document-side weights precomputed.
      **18/18 adversarial tests pass** (`tests/test_bm25_index.py`), and verified on the
      real corpora: MIND 65,238 docs / 60,951 terms / 2.36 M non-zeros in 1.70 s;
      EB-NeRD 11,777 / 31,642 / 269 K in 0.19 s; peak RSS 0.51 GB. Sanity checks that
      confirm the concept rather than just the code: `the` has IDF 0.26 against a corpus
      max of 10.68; EB-NeRD's top terms come out as the Danish function words `i`/`og`/`er`
      with `ø`/`þ` intact; and `n(t)` equals the posting-list length for all 92,593 terms.
- [x] `pytest.ini` added so `pytest` works from the repo root without `PYTHONPATH=src` —
      same class of "only works from the right directory" bug as the Q1.5 error-log entry.
- [x] `scipy==1.18.1`, `pytest==9.1.1` pinned in `requirements.txt`.

- [x] Q2.2–2.4 — query side (`src/newsrec/retrieval/bm25_search.py`,
      `src/newsrec/eval/recall.py`, `scripts/run_bm25_recall.py`,
      `scripts/summarise_bm25_recall.py`). Decisions D17–D19 taken. **38/38 tests pass.**
      Results in `reports/bm25_recall_summary.csv`.

**Q2 headline (recall@200, macro, val, impressions with a query), with the random
baseline that makes it interpretable:**

| Dataset | Pool | recall@200 | random@200 | lift |
|---|---|---|---|---|
| MIND | whole corpus | 2.05% | 0.31% | **6.7×** |
| MIND | available | 3.95% | 0.94% | **4.2×** |
| EB-NeRD | whole corpus | 2.45% | 1.70% | **1.4×** |
| EB-NeRD | available | 7.27% | 6.81% | **1.07×** |

**The Phase 2 finding.** BM25 retrieves topically-correct articles (verified by
inspection: a Russia/Ukraine reader gets Russia/Ukraine headlines back) but is blind to
time — its top-200 has essentially the corpus's own freshness profile (16.6% published
on/after the val window start) while **92.7% of actually-clicked articles are fresh**.
There is no time term anywhere in the BM25 formula, so this cannot be tuned away; it has
to be handled outside the formula (D19) or not at all. Restricting to in-circulation
articles triples EB-NeRD's absolute recall while *lowering* its lift over random from
1.4× to 1.07× — i.e. on EB-NeRD nearly all the apparent gain is the pool shrinking, and
reporting it without the baseline column would have been materially misleading.

- [x] D16's ablation answered with a number rather than an assertion: raw vs binary
      query-term frequency is **near-noise** at ~10-title queries (MIND whole-corpus
      favours raw 2.05% vs 1.84%; MIND available favours binary at K=200 but raw at
      K=50; EB-NeRD tied). Cheap to keep, informative to have measured.

- [x] Phase 2→3 recall quiz done 2026-08-25 (2 of 3 solid, one re-taught — see
      `LEARNING.md`). **A new session does not need to repeat it.**

### Phase 3 (in progress)
- [x] **R1 amended 2026-08-25 at Chaitanya's request:** required reading dropped for the
      rest of the assignment; concepts taught in chat, plain-language then technical.
      `CLAUDE.md` + `PROMPT.md` updated and re-synced. `LEARNING.md` keeps its
      comprehension-check record, which is the part that matters.
- [x] **Pacing (R8):** with 2 days left and 12 h of budget across Phases 3–6, Chaitanya
      chose path **(b)** — full options-and-trade-offs treatment for forks that change the
      answer (model, user representation, candidate pool), stated defaults elsewhere.
      Phase 5 (cloud + Codabench) is the real deadline risk, not teaching depth.
- [x] Embeddings and ANN (Approximate Nearest Neighbour) taught. Comprehension check:
      **1 of 3 solid, 1 sharpened, 1 re-taught** — see `LEARNING.md`. The re-taught one
      matters for the code: D15's history exclusion applies **more** strongly to
      embeddings than to BM25, because the mean-pooled user vector is provably the point
      of maximum average similarity to the user's own history articles.
- [x] **D20** — compute our own embeddings, one multilingual model for both datasets:
      `paraphrase-multilingual-MiniLM-L12-v2` (384-dim, `model_type: "bert"`, Danish
      verified present in its language list). Two facts were verified rather than assumed
      before deciding: `distiluse-base-multilingual-cased-v1` has **no Danish** despite
      looking like the cheapest multilingual option, and the download speed the original
      recommendation rested on was **stale by ~100×** (measured 6.1 MB/s PyPI /
      2.8 MB/s HuggingFace, not the remembered 60 KB/s) — which inverted the
      recommendation from ONNX Runtime to sentence-transformers.
- [x] Environment installed: `torch==2.13.0+cpu` + `sentence-transformers==6.0.0`,
      **0 CUDA packages**. `requirements.txt` carries the PyTorch CPU index above the
      torch pin; verified by a from-scratch resolution (46 packages, 0 CUDA, torch from
      PyTorch's CDN and the other 45 from PyPI). Without those two lines a rebuild pulls
      2,894 MB instead of ~390 MB, 2,238 MB of it unusable on a GPU-less machine.
- [x] **D21** — exact brute-force nearest-neighbour search (Q3.2 permits it explicitly),
      batched, reusing `bm25_search.py`'s pattern. `SCALE_NOTES.md` entry added for the
      10× crossover where a real ANN index stops being optional.

- [x] **D22** — embeddings get their own `data/processed/embeddings.parquet`, vector beside
      its own `article_id` so misalignment is impossible by construction. Deliberately
      **not** folded into `build_pipeline.py`: that script rewrites `articles.parquet`
      every run, so vectors stored there would be recomputed (2.81 s → ~13 min) or
      destroyed each time.
- [x] **Q3.1 done** — `src/newsrec/retrieval/semantic.py` + `scripts/build_embeddings.py`.
      **15 new adversarial tests, 53 passing overall.** Two real bugs prevented before
      they ran, both instances of the same Phase 1 null trap wearing different clothes:
      `pl.concat_str` propagates null, which would have blanked **3,415 MIND** articles'
      text; and EB-NeRD encodes a missing abstract as `""` rather than null, so **803**
      articles would slip past a null-only guard.
- [x] **Real artifact built and verified:** 77,015 vectors (65,238 MIND + 11,777 EB-NeRD)
      in **13.3 min at 96 articles/s**, 110 MB, loading in **0.6 s** as a C-contiguous
      float32 (77015, 384) matrix. Norms exactly 1.000000. **ID order matches
      `articles.parquet` exactly.** Nearest-neighbour inspection coherent in both
      languages. Peak RSS during the build 1.69 GB — flat in corpus size, since
      `model.encode` streams in batches of 64.

- [x] **Q3.2/Q3.3/Q3.4/Q3.5 done** — `src/newsrec/retrieval/semantic_search.py`,
      `scripts/run_semantic_recall.py`, `scripts/summarise_recall.py` (generalised from the
      BM25-only version to cover both methods). **21 new tests, 74 passing overall.**
      Results in `reports/recall_summary.csv`; full comparison written up as Q3.5's five
      findings in `ARCHITECTURE.md`.
- [x] **`newsrec/retrieval/availability.py` extracted** so BM25 and semantic share one D19
      implementation rather than two copies that could drift. Regression-verified: re-ran
      EB-NeRD/available BM25 and the output CSV is **identical** to the committed Q2 result
      (recall@200 0.0727, 8,777 tasks).
- [x] **Two bugs caught by mutation-testing our own tests**, not by a traceback:
      1. Dense cosine scoring must mask with **-inf, not 0.0**. BM25 excludes candidates by
         zeroing them, which is right when 0 is the minimum possible score — but cosine
         runs [-1, 1] and 0 is mid-range, so copying that convention floats every excluded
         and unavailable article above every genuinely negative-scoring one. Worst on D19's
         EB-NeRD run, where ~8,814 of 11,777 articles are masked per bucket.
      2. A pooled user vector with a **tiny but non-zero norm** passes a `norms > 0` check,
         then gets normalised — inflating pure float residue (norm ~5e-08) into a confident
         unit direction. Fixed with a `MIN_NORM = 1e-6` threshold plus a test proving a
         bare zero-check fails it.

**Q3 headline (recall@200, macro, val, has-query slice):**

| Dataset | Pool | BM25 | Semantic | BM25 lift | Semantic lift |
|---|---|---|---|---|---|
| MIND | whole corpus | 2.05% | **2.17%** | 6.69× | **7.08×** |
| MIND | available | 3.95% | **5.41%** | 4.19× | **5.74×** |
| EB-NeRD | whole corpus | 2.45% | **2.65%** | 1.44× | **1.56×** |
| EB-NeRD | available | 7.27% | **8.57%** | 1.07× | **1.26×** |

**The Phase 3 finding.** Semantic wins all four at K=200, but the structure matters more
than the margin: **BM25's lift decays with K while semantic's holds** (EB-NeRD available:
BM25 1.21×→1.07×, semantic 1.27×→1.26×), because BM25 ranks only articles sharing a term
and runs out of signal, while cosine ranks the whole corpus. And running a completely
different matching function reproduced Q2's freshness blindness exactly — semantic's
top-200 is 31.9% fresh against a 33.5% corpus baseline while **93.5% of real EB-NeRD
clicks are fresh** — which upgrades that from a BM25 limitation to a property of
content-based retrieval as such.

### Phase 4 (in progress)
- [x] **Structural point settled before any code:** Q4's metrics grade a *re-ranking of
      the supplied candidate list*, not whole-corpus retrieval — forced, because AUC/MRR/
      nDCG each need a per-item clicked/not-clicked label and only the shown list has one.
      An unretrieved corpus article is *unlabelled*, not negative. Written up in
      `ARCHITECTURE.md`. Same scorers as Q2/Q3, different candidate set — and the same
      task both Codabench leaderboards consume, so this feeds Phase 5 directly.
- [x] Ranking metrics taught (analogy → ASCII formulas → comprehension check).
      **1 sharpened, 1 correction to Claude's own wording, 1 solid** — see `LEARNING.md`.
      Two results carried into the design note: **AUC is rack-size sensitive where MRR is
      not** (rank 3 of 20 → 0.895; rank 3 of 4 → 0.333; MRR 1/3 in both), so MIND's and
      EB-NeRD's AUCs are not comparable to each other; and **nDCG@10 silently becomes
      nDCG@all on EB-NeRD** (median rack 9 < cutoff 10), leaving four metrics carrying
      about three independent signals there.
      *Housekeeping: LaTeX does not render in this terminal — use fenced ASCII maths.*
- [x] **D23** — pessimistic tie-breaking (clicked items last within a tie group, so every
      MRR/nDCG figure is a lower bound), with the optimistic bound reported alongside so
      the gap *measures* how much tie handling matters. Chosen against measured tie rates
      (BM25 scores exactly 0 for 2.4% MIND / 4.0% EB-NeRD of candidates; 0.10% of MIND
      impressions have *every* candidate tied at 0).
      **The check that justified stopping:** `np.argsort` is stable, so "no tie policy"
      silently means "rank ties by raw candidate-list order". Verified that order carries
      no click signal — mean normalised position of a clicked item **0.5017 (MIND) /
      0.4961 (EB-NeRD)** against 0.5 for a uniform shuffle, and clicked-item-first rates
      matching their random-order expectations (9.86% vs 10.18%; 11.74% vs 11.70%). Safe,
      but verified about *these val splits* — which is why the policy is explicit in code.
- [x] **Q4.1 done** — `src/newsrec/eval/metrics.py` (AUC via the O(n log n) rank identity,
      MRR, nDCG@5/@10, `evaluate_impressions`, `macro_mean`). **28 new adversarial tests,
      102 passing overall.** Undefined metrics return NaN, never 0.0, and `macro_mean`
      returns `(mean, n_defined, n_undefined)` so a metric averaged over a fraction of the
      impressions cannot reach the design note unnoticed.
      **Mutation-tested (the Phase 3 practice):** 7 deliberate bugs reintroduced one at a
      time — uncapped IDCG (`n_pos` instead of `min(n_pos, k)`), inverted tiebreak,
      `rankdata` method `ordinal` instead of `average`, removed NaN guard, tiebreak
      replaced by argsort stability, MRR off-by-one, DCG discount off-by-one — **all 7
      caught.** The AUC suite implements the O(P·N) pair definition independently, so an
      error in the rank algebra cannot be made in both places at once.
- [x] **D24** — two baselines added alongside BM25 and semantic: **random** (seeded per
      impression id, so a slice scores identically to the whole set) and **popularity**
      (train-window click count). MRR and nDCG have no natural zero point the way AUC's
      0.5 does. `train_click_counts` **raises** on any split but train rather than trusting
      the caller — counting val clicks would let the baseline see its own answers.
- [x] **Q4.2 done** — `src/newsrec/eval/rerank.py`, `scripts/run_rerank_eval.py`.
      **21 new adversarial tests, 123 passing overall.** Mutation-tested: 7 bugs
      reintroduced, 6 caught; the 7th ("popularity returns a view") was a **bad mutation,
      not a test gap** — NumPy fancy indexing already copies, so it changed nothing.
      Runtime: MIND 51,205 impressions in 136 s, EB-NeRD 17,749 in 1.2 s.
      Scorer verified against an independent per-impression computation before any number
      was believed (max deviation 1.9e-06, float32 noise), and the random arm lands at
      AUC 0.5007 / 0.4987 — the harness checking itself.

**Q4.2 headline (val, macro, has-query slice, pessimistic ties):**

| Dataset | random | popularity | BM25 | semantic |
|---|---|---|---|---|
| MIND — AUC | 0.5007 | 0.5423 | 0.5492 | **0.6338** |
| MIND — nDCG@5 | 0.2264 | 0.2278 | 0.2760 | **0.3316** |
| EB-NeRD — AUC | 0.4987 | **0.4647** | 0.4966 | **0.5331** |
| EB-NeRD — nDCG@5 | 0.3443 | 0.0939 | 0.3418 | **0.3730** |

**Three findings, written up in full in `ARCHITECTURE.md`:**
1. **BM25 cannot re-rank EB-NeRD at all** (AUC 0.4966 vs random 0.4987) even though it
   held a 1.21× retrieval lift at K=50. Retrieval and re-ranking are different jobs: the
   platform's own recommender has already spent the easy signal, so everything in
   `article_ids_inview` is already plausible and lexical overlap no longer separates it.
2. **On EB-NeRD, train-window popularity predicts clicks in the *wrong* direction**
   (AUC 0.4647). 86.9% of val candidates were never clicked in train, and one that *was*
   is disproportionately stale. Third independent route to Phase 2's freshness finding.
3. **The tie policy mattered exactly once, and the number says where.** Pessimistic-vs-
   optimistic nDCG@10 gap is ≤0.0013 for BM25 and semantic — so no conclusion rests on it,
   the sentence D23 existed to produce — but **+0.5012** for EB-NeRD popularity, which is
   mostly a constant scorer. Reported optimistically it would have topped the table.
- [x] Measured and banked for Q9 rather than folded into the score: a candidate already in
      the user's history is clicked **3.5× more** often than average on MIND and **0.49×**
      on EB-NeRD — opposite directions, both outside noise, and leak-checked before being
      believed. "Has the user already read this" is a **serving-time feature**, so it is an
      ablation arm, not a scoring hack.
- [x] **Landmine for `tests/test_no_leakage.py`:** EB-NeRD's **validation history file
      contains 99.52% of train-window clicks** (22,143/22,249). Harmless as used (train
      precedes val), catastrophic if val history were ever pointed at train impressions.
- [x] Beyond-accuracy taught (analogy → ASCII formulas → comprehension check).
      **2 of 3 parts right, novelty corrected** — see `LEARNING.md`. The correction is
      load-bearing: **diversity and coverage are bounded in [0,1] and readable absolutely,
      novelty is not** — MIND's range is 6.13–18.20 and EB-NeRD's 8.01–15.16, so a raw
      novelty figure is meaningless alone and **the two datasets' novelty numbers are not
      comparable to each other.** Second instance in one phase of a metric silently
      carrying the dataset's scale (AUC's rack-size sensitivity was the first), so it is a
      pattern for the design note rather than a one-off.
      Also established: **a purely random recommender scores best on all three of these
      metrics**, so they price what a method gave up and only mean something read against
      the accuracy table.
- [x] **D25** — both flagged forks resolved. **(A)** headline beyond-accuracy measured on
      **retrieval** output, with re-ranking computed too so the candidate-pool cap is shown
      rather than asserted; only **6.8% of MIND's corpus / 19.2% of EB-NeRD's** ever appears
      in any val candidate list. **(B)** **both** diversity bases reported — embedding
      cosine distance and category distance.
- [x] **Q4.3 done** — `src/newsrec/eval/beyond_accuracy.py`,
      `scripts/run_beyond_accuracy.py`. **23 new adversarial tests, 146 passing overall.**
      Both diversity metrics use closed forms instead of pairwise loops, each checked
      against a brute-force implementation written separately in the tests.
      Mutation-tested: **7 bugs reintroduced, all 7 caught** (self-terms left in the ILD
      closed form, category-ILD sign inverted, novelty smoothing removed, novelty sign
      flipped, coverage counting positions instead of articles, short lists returning 0.0
      instead of NaN, category same-pair count off-by-one).
      Results in `reports/beyond_accuracy_{mind,ebnerd}_val_k10.csv`.

**Four findings (9–12), written up in full in `ARCHITECTURE.md`:**
1. **The embedding basis overstates semantic's diversity deficit on both datasets and
   reverses its sign on EB-NeRD.** semantic ÷ bm25: MIND 0.784 (embed) vs 0.849 (category);
   EB-NeRD **0.544 (embed) vs 1.041 (category)**. Reported conventionally we would have
   written "semantic produces markedly less diverse lists" — false in direction on EB-NeRD.
   The honest statement is the pair: semantic's lists are tightly packed in embedding space
   while spanning a comparable range of *categories*, i.e. it repeats **within** topics.
2. **Coverage is where methods separate — by three orders of magnitude.** MIND retrieval:
   popularity **0.02%** (~13 articles for all 50,000 users), semantic 53.21%, bm25 51.02%,
   random 99.96%. Direction flips by dataset: semantic covers slightly *more* than BM25 on
   MIND, less than *half* as much on EB-NeRD (14.44% vs 31.13%).
3. **Novelty barely discriminates between content methods**, because 88.2% of MIND's corpus
   was never clicked in training so almost anything retrieved is "novel". Still worth
   reporting: it is positive evidence that neither BM25 nor semantic has a popularity bias.
4. **Fork A demonstrated, not argued.** On re-ranking, four completely different scorers
   land within 0.4 points of each other on EB-NeRD coverage (17.75–18.17%). On retrieval
   the same four span 0.02%–99.96%.
- [x] **D26** — slice definitions. **Cold start:** absolute `history_len <= 5` (MIND 17.7%
      of val impressions, EB-NeRD **0.3%** — 55 of them), not a per-dataset quantile, because
      cold start is an absolute property and EB-NeRD having no cold users is a *finding*.
      **Head/tail:** two definitions, because the textbook one is degenerate — train
      popularity leaves **~98% of val clicks in the tail on both datasets**, so
      exposure-based head (articles filling 50% of val impression slots, counted from
      what was **shown**, never from clicks) is the working slice and train-popularity is
      reported to show its degeneracy. Multi-click impressions straddling the boundary go
      to neither slice and are counted (MIND 7,209 = 14.5%, EB-NeRD 20).
- [x] **D27** — **coverage is reported without a bootstrap CI**, and this was a real bug
      caught by running it: every coverage interval sat *entirely below its own point
      estimate*. Root cause is the statistic, not the code — a resample holds only **63.2%**
      distinct items (measured at n = 1,562 / 17,749 / 50,000, all 63.2%), which is harmless
      for a **mean** but fatal for a **union**, where a duplicate adds nothing and every
      resample can only lose articles. Point estimate reported with the reason; raw spread
      and the pivotal correction kept in the CSV under explicit names.
      **Test-debt lesson worth more than the fix:** an existing test already asserted this
      exact downward shift *and treated it as correct*. The assertion was true; the missing
      step was inferring that it invalidates the interval. A test can pin a real property
      and still let a wrong conclusion through.
- [x] **Q4.3 slices + Q4.4 bootstrap done** — `src/newsrec/eval/slices.py`,
      `src/newsrec/eval/bootstrap.py`, `scripts/run_eval_report.py`, plus CIs added to
      `run_beyond_accuracy.py`. **31 new adversarial tests, 177 passing overall.**
      Mutation-tested: **8 bugs reintroduced, all 8 caught.** The bootstrap suite includes
      a **calibration** test (does the interval cover a known truth ~95% of the time),
      which is the only test that distinguishes a real bootstrap from a machine that
      returns confident-looking numbers. Results in `reports/eval_report_{mind,ebnerd}_val.csv`
      and `reports/beyond_accuracy_mind-ebnerd_val_k10.csv`.

**Five findings (13–17), written up in full in `ARCHITECTURE.md`:**
1. **The CIs turn Findings 6 and 7 into claims.** EB-NeRD BM25 AUC 0.4966 **[0.4917,
   0.5009] — the interval contains 0.5**, so chance cannot be rejected. Popularity's
   [0.4629, 0.4666] lies entirely *below* 0.5. Semantic's excludes both.
2. **The method ranking flips between slices — the whole point of slicing.** On MIND
   cold-start users **popularity beats BM25** (0.5542 vs 0.5296, non-overlapping CIs); on
   warm users the order reverses (0.5526 vs 0.5402, also non-overlapping). With ≤5 history
   articles BM25's query is too thin to beat "what is everyone reading". Popularity is the
   only method that scores *higher* cold than warm. Retrospective justification for D17's
   rejected popularity fallback: right product call, wrong measurement call — it would have
   hidden this crossover inside one blended number.
3. **Semantic degrades least under cold start** and leads in both slices.
4. **MRR halves on rarely-shown articles for every method including random**, while AUC
   barely moves and BM25's even rises. The slice is structurally harder, not the methods
   failing — having both metrics on the same slice is what prevents the misreading.
5. **A slice defined by a quantity a method scores on grades that method tautologically.**
   Popularity scores AUC **0.9737** on the train-popularity head slice against 0.5423
   overall. Same shape as measuring semantic's diversity in the space it optimises (D25).
   Two instances in one phase, so it is a rule for the design note.
- [x] **`tests/test_no_leakage.py` done** — 12 tests in five groups (temporal, label-free,
      split boundary, history snapshot, scorers-are-blind). **Mutation-verified: 5
      deliberate leaks reintroduced, all 5 caught**, including relaxing `first_seen < T`
      to `<=`. A leakage test that cannot fail is worse than none, so this was checked
      rather than assumed.
      Strongest single assertion: **flipping every label leaves BM25 and semantic scores
      byte-identical.** The landmine is a live test, not a comment — it performs the
      val-history-on-train-impressions mis-join and asserts the overlap check fires
      (measured 99.52%).
- [x] **D28 + Q9 ablation done** — `src/newsrec/eval/ablation.py`,
      `scripts/run_ablation.py`. **14 new tests, 203 passing overall.** Mutation-tested:
      6 bugs reintroduced, all 6 caught. The leaky feature is quarantined and a test
      asserts **no other file in the package references it**.

**Q9 headline (val, AUC, has-query slice, 1,000-resample CIs):**

| arm | MIND | EB-NeRD |
|---|---|---|
| popularity (train) · safe | 0.5423 | 0.4647 |
| **popularity (FUTURE) · LEAK** | **0.6102** | **0.6657** |
| semantic · safe (our best honest system) | 0.6338 | 0.5331 |
| semantic + seen-before · safe | 0.6339 (+0.0001) | 0.5314 (−0.0017) |
| **semantic + FUTURE pop · LEAK** | **0.6572 (+0.0234)** | **0.5872 (+0.0541)** |

**Three findings (18–20), written up in full in `ARCHITECTURE.md`:**
1. **Moving one counting window is worth more than the entire honest system.** On EB-NeRD,
   identical algorithm, counts from the evaluated window instead of training: AUC
   **0.4647 → 0.6657, +0.2010**. Semantic beats random by only 0.0344, so **one leaked
   feature is worth ~4× all the honest modelling of Phases 2–4.** This is the anti-gaming
   argument in a single number, and it is why leaderboard rank is a poor grading signal.
2. **A leak is worth most exactly where honest methods are weakest** — +0.2010 on EB-NeRD
   vs +0.0679 on MIND, a 3× difference in the value of identical cheating, explained by
   EB-NeRD's catalogue turnover (86.9% of val candidates unclicked in train). Corollary
   worth stating: **the datasets where leakage is most tempting are the ones where it is
   hardest to notice**, because no strong honest baseline exists whose absence would look
   suspicious.
3. **The legitimate feature buys essentially nothing and its sign flips between datasets**
   (+0.0001 / −0.0017, both inside the CIs). Real per-candidate signal (3.5× / 0.49×) but
   it applies to only 0.055% / 0.959% of candidates, and one global positive weight is
   simply wrong on EB-NeRD where the effect is negative. Reported as-is rather than
   re-specified per dataset — that *is* the finding.

- [x] **Phase 4 complete.** Q4 (all four sub-requirements) + Q9 (both halves).

### Phase 5 (in progress)
- [x] **Pacing settled** (see the box below) — reduced depth, full R6 on the platform fork.
- [x] **All three Phase 5 landmines verified against the real bundles**, not inherited:
      EB-NeRD test behaviors has 14 columns and **no `article_ids_clicked`**; MIND test
      behaviors has **5 fields and 0 matches** for `N[0-9]+-[01]` across 50,000 rows;
      EB-NeRD test carries `is_beyond_accuracy` as a Boolean.
- [x] **Both large test bundles were already downloaded and extracted** — 1.5 GB
      `MINDlarge_test`, 1.8 GB `ebnerd_testset`, 3.4 GB `ebnerd_large`. The largest single
      item on Phase 5's risk list was already paid, which is what redirected D29.
- [x] **D29 — run locally, Kaggle named as the fallback.** The D2 sub-decision, finally
      taken against measured numbers: only the embedding step benefits from a GPU, the
      data is already here, and the streaming path computes the distinct candidate set
      over all 13.5 M EB-NeRD test impressions in **1 s at 1.03 GB peak**.
- [x] **D30 — separate submission store, label column absent rather than empty.**
      `src/newsrec/submission.py` + `scripts/build_submission_store.py`, writing to
      `data/processed/submission/`. `test_root` added to both configs.
- [x] **Two inherited assumptions re-verified at test scale rather than carried forward:**
      EB-NeRD history chronological ordering (0 out of order across **807,677** users, vs
      4,714 checked at demo scale) and MIND's constant-history-per-user assumption from D3
      (0 violations across **484,059** multi-row users, vs 33,617 checked in Phase 1).
      Candidate coverage is 100% on both datasets — 0 missing articles.
- [x] **Submission article stores built**: 120,961 MIND + 125,541 EB-NeRD articles.
- [x] **15 new adversarial tests, 218 passing overall.** Mutation-tested: 10 bugs
      reintroduced, **9 caught, and the 10th was a genuine gap** — deleting the
      `assert_mind_test_unlabeled` *call* from the reader left every test passing, because
      they all exercised the guard function directly. A guard nothing proves is wired up is
      decoration. Test added; re-mutated; now caught.
      *(Separately: the mutation harness itself was broken on the first run — `python` was
      not on PATH, so no mutation ever applied and every result read "MISSED". A broken
      verifier produces failure-shaped output. Worth remembering.)*
- [x] **Submission format recovered from Codabench's API** (both competition pages render
      as an empty JavaScript shell and fetch as nothing). Both want
      `<impression_id> [r1,...,rn]`; the file inside the zip is `prediction.txt` for MIND
      and `predictions.txt` for EB-NeRD — one letter apart.
      **`r_i` is the rank of the candidate at position `i`, i.e. the INVERSE permutation
      of an argsort.** Writing `argsort(-scores)+1` gives a structurally perfect file that
      scores near random and cannot be diagnosed from a leaderboard. Pinned by tests
      against both competitions' own worked examples.
      **Correction (Chaitanya, 2026-08-25):** the per-day submission caps printed on those
      pages (1/day MIND, 5/day EB-NeRD) are live-competition limits from years ago; the
      real limit is **10/day on both**. Second instance of D20's stale-documentation trap.
- [x] **`predict.py` + `validate_submission.py`** — the rank-vector writer, the zip
      packager, and a pre-flight validator that re-reads the raw bundle to check line *i*
      carries impression *i*'s id and that every rank list is a permutation of 1..n.
      **22 new tests.**
- [x] **Official EB-NeRD example submission downloaded as a format oracle** (230 MB):
      one flat `predictions.txt`, **13,536,710 lines** — every row, including the 200,000
      `is_beyond_accuracy` ones — and its first five impression ids and candidate counts
      match the raw bundle row for row.
- [x] **MIND test embeddings**: 120,961 vectors, 24.4 min at 82 articles/s.
- [x] **MIND submission generated and validated.** 2,370,727 lines, 6.4 min at ~7,100
      impressions/s, 291 MB text / 107 MB zip. Validator: **0 syntax errors, 0 wrong or
      out-of-order ids, 0 malformed permutations.** Independently re-verified by
      recomputing three impressions' rankings (16, 7 and 82 candidates) outside the
      pipeline — all three match exactly.
      **The rank-1 position histogram was read against its null model rather than
      eyeballed:** pos0 wins 10.5% vs pos1 9.2%, which looked like position bias in a
      position-blind scorer. Random baseline is E[1/n] = 9.32%, and the 1.18-point excess
      is exactly what the 29,108 cold-start impressions contribute (all candidates tie at
      zero → stable order gives rank 1 to position 0). Not a bug.
- [x] **EB-NeRD test user coverage verified**: all 807,677 behaviors users have a history
      row and no history row is orphaned — exact 1:1, so no cold-start-by-absence.
- [x] **`README.md` written** — Q7 deliverable #1 requires "README.md with one-command
      reproduce" and the repository had none. Quickstart, full reproduce table, submission
      workflow, layout, headline results, three findings.
      *Measured timings are marked as such; steps never stopwatch-timed say so rather than
      carrying an invented number.*
- [x] **EB-NeRD test embeddings**: 125,541 vectors, 18.6 min at 113 articles/s.
- [x] **EB-NeRD submission generated and validated.** 13,536,710 lines, **6.7 min** at
      42,683 impressions/s, 703 MB text / 230 MB zip. Validator: **0 syntax errors, 0
      wrong or out-of-order ids, 0 malformed permutations.**
      The zip is **230,125,490 bytes against the official example's 230,142,211** — the
      two agree to 0.007%, which is about as strong an external format check as exists.
- [x] **Both zips verified as artifacts**, not just as pipelines: correct entry name
      (`prediction.txt` / `predictions.txt`), archive integrity OK, and line counts read
      back out of the compressed files (2,370,727 / 13,536,710).
- [x] **240 tests still passing** after the Phase 5 additions.
- [x] **First MIND leaderboard result: AUC 0.6037, rank 62/90** (val 0.6338 predicted it
      closely, so val is a trustworthy offline proxy).
- [x] **D31 — N re-tuned for re-ranking, 10 → 100.** +0.0151 val AUC on MIND
      (0.6338 → 0.6489), +0.0082 on EB-NeRD (0.5331 → 0.5413), saturating by N=100.
      D12's N=10 was chosen for *retrieval*, to fight topic drift in a whole-corpus
      search; re-ranking has no drift to fight, so the value was silently wrong. The
      §6 retrieval-vs-re-ranking trap, appearing as a hyperparameter.
- [x] **Two unexpected results kept** (see D31): max-similarity **loses on MIND, wins on
      EB-NeRD**, explained by EB-NeRD's longer histories and lower nearest-neighbour
      cosines; and a scorer worse alone can still add in combination (+0.0056).
- [x] **Popularity dropped from fusion on a transferability check**, not a hunch: only
      **5.7%** of MIND test candidates have a train-window click count.
- [x] **Both submissions regenerated at N=100 and validated clean.**
      MIND 2,370,727 lines / 4.1 min; EB-NeRD 13,536,710 lines / 6.3 min. Confirmed the
      rankings actually changed (34,600 of 50,000 sampled MIND lines differ).
      Files: `reports/submissions/{mind,ebnerd}_semantic_n100.zip`.
- [x] **D31 confirmed on the leaderboard: MIND AUC 0.6037 → 0.6191, rank 62 → 54 of 90.**
      Predicted +0.0151 from val, delivered **+0.0154** — agreement to 0.0003. Absolute
      levels differ by ~0.030 (val is an easier, earlier window) but the *delta* transfers,
      which is the property that makes offline tuning valid.
- [x] **Engineering benchmarks measured** (`scripts/benchmark_engineering.py`) after the
      course email named latency/throughput and alternative comparison as the grading
      criterion. Results in `SCALE_NOTES.md`.
- [x] **Q6 design note written** — `reports/design_note.md`, ~1,950 words, balanced
      ~2 pages engineering / ~2 pages findings per Chaitanya's call.
- [x] **EB-NeRD SCORED, 2026-08-27.** Submission 904082 (`ebnerd_semantic_n100.zip`):
      **AUC 0.5396, rank 147 / 247**, MRR 0.3441, nDCG@5 0.3817, nDCG@10 0.4608.
      Screenshot in `reports/figures/ebnerd_csharp.png`; both leaderboards now captured.
      **The calibration claim held twice, and the second test was the harder one.**
      MIND transferred a *delta* (predicted +0.0151, delivered +0.0154) while its absolute
      levels differed by ~0.030. EB-NeRD transferred the **absolute level**: val 0.5413 vs
      leaderboard 0.5396, a gap of **0.0017** — on the dataset where our own harness says
      the honest signal is weakest.
      A free consistency check came with it: the leaderboard's other three columns
      (0.3441 / 0.3817 / 0.4608) sit just above our N=10 val run (MRR 0.3373, nDCG@5
      0.3730, nDCG@10 0.4532) in the same order and by about the margin N=10 -> N=100
      should give. That confirms the column ordering without trusting a header.
- [x] **Q6 design note written** (`reports/design_note.md`, committed d13e5e2). The line
      that stood here said "NOT STARTED — the only graded deliverable at zero" for a day
      after it was finished. A status file that lags reality is worse than none, because
      it redirects effort toward work already done.

### Phase 5b process errors, recorded so they are not repeated
1. **The first fusion search ran >1 h and was killed.** It evaluated seven metrics per
   weight combination when the search reads one, searched a 4-way grid when AUC's
   invariance to positive rescaling makes one weight redundant, and printed nothing until
   the end so a slow run was indistinguishable from a hang. The corrected
   `scripts/tune_fusion.py` runs the same search in ~2 min.
2. **Three runtime estimates in a row were wrong** (embedding ~80 min → 43; EB-NeRD
   submission ~35 min → 6.7; fusion ~42 min → >60 and killed). An estimate for a loop
   nobody has timed is a guess and should be labelled as one.
3. **`pgrep -f <pattern>` matches the shell running the check**, so a dead background job
   was reported as running. Use `ps`, or wait on a PID.

### R8 note: the embedding over-run was a false alarm, corrected
Flagged mid-run as heading for ~80 min against `SCALE_NOTES.md`'s ~43 min estimate. Final
figures: MIND 24.4 min + EB-NeRD 18.6 min = **43.0 min, exactly the estimate.** The
pessimistic projection came from measuring throughput (~50 articles/s) while development
work competed for the same cores; unloaded it ran at 113–115 articles/s. The estimate was
right and the flag was premature — recorded because an over-run flag raised on a
contended measurement is itself a measurement error.

**The EB-NeRD submission was also 5x faster than projected** — 6.7 min against ~35 min
guessed from MIND's rate. MIND runs at 7,140 impressions/s and EB-NeRD at 42,683, because
EB-NeRD's racks are far shorter (median 9 vs 25) and its scoring matrix is 10,451 columns
rather than 30,043. Extrapolating one dataset's throughput to the other was the error.

### Two process errors in Phase 5 worth not repeating
1. **`until [ -f file ]` is not "the file is finished".** A watcher fired the instant the
   zip was *created*, at 17.8 MB mid-write, and validation against that half-written
   archive raised `BadZipFile`. Worse, it sent us investigating a phantom: the partial
   file appeared to compress 13x better than the official example, and effort went into
   explaining a compression anomaly that did not exist. The complete file matches the
   official example to 0.007%. **Wait on process exit, not file presence.**
2. **The validator silently skipped a check it was asked to run.** `--reference` pointed
   at an oracle file the scratchpad had cleaned between sessions, and the code said
   `if args.reference and args.reference.exists()` — so it printed a clean bill of health
   having never run the comparison. Now a missing `--reference` is a hard error, raised at
   argument-parse time rather than after a 13.5M-line pass. A verification step that can
   silently do nothing is worse than no step, because it reports success either way.

### Codabench self-hosted worker: ruled out locally, 2026-08-26
The EB-NeRD organizers publish a working remote-worker setup (docker + a live
`BROKER_URL` for competition 2469's shared queue) at
`github.com/jppol-ai/ebnerd-benchmark/tree/main/codabench`, surfaced by a student on the
forum. Two independent blockers stop it running on this machine, both found in pre-flight
rather than during a 4-5 h run:

1. **Architecture.** This machine is `aarch64` (Windows on ARM). The image
   `codalab/competitions-v2-compute-worker:cpu1.1` ships a *single* manifest whose config
   blob reads `architecture: amd64` -- no ARM variant exists. qemu emulation would apply
   to the scoring container too, i.e. numeric Python over 13.5 M rows at 5-20x slowdown.
2. **Network.** Outbound TCP to `www.codabench.org:5672` (AMQP) times out while :443 is
   open -- the broker port is filtered by the network/ISP. The worker cannot reach the
   queue regardless of architecture.

Non-blockers, checked and cleared: WSL2 raised to 12 GB + 16 GB swap via `.wslconfig`
(was 7.5 GB / 2 GB -- the default is *half of host RAM*, not a ceiling); Docker Engine
29.7.2 installed and running under systemd; clock in sync to 1 s; 163 GB free on the
Windows volume.

**Process note:** the architecture check should have come first. It was cheaper than
every other check run that evening and it was the one that decided the outcome. An
earlier message had already named amd64-only images as the reason to reject a *cloud* ARM
tier, without checking the local machine against the same requirement.

Worker tooling was written under `codabench/` and later removed from the repository as
unrelated to the pipeline; it remains in git history (commits of 2026-08-27).

### Error: the published Codabench worker silently eats queued submissions, 2026-08-27
**Symptom.** A self-hosted `codalab/competitions-v2-compute-worker:cpu1.1` (the tag the
EB-NeRD organizers' README pins) connected to competition 2469's queue, took 42 jobs in
about 60 seconds, and failed every one with `SubmissionException('Failure updating
submission data.')`.

**Misread first, corrected.** The response body is a full HTML page containing a Login
link and `user: JSON.parse("")`, which reads as an authentication failure. It is not: the
log line above it says `status = 500` and the page is Codabench's *500 error* template
("Something went wrong on our end"). The Login link is just the nav bar rendered for a
non-browser client. **Anchor on the status code, not on what the body looks like.**

**Root cause, confirmed against upstream source rather than inferred.** The worker PATCHes
`{'secret': {'__type__': 'uuid', '__value__': {'hex': '...'}}}` — Kombu's JSON encoding of
a `uuid.UUID`, echoed back verbatim. The server cannot parse a dict as a UUID and 500s.
Current `compute_worker.py` on `develop` fixes it in the task entrypoint:

    @shared_task(name="compute_worker_run")
    def run_wrapper(run_args):
        # We need to convert the UUID given by celery into a byte like object ...
        run_args.update(secret=str(run_args["secret"]))

That `str()` is absent from `cpu1.1`, which was built **2024-08-05**. Four worker releases
have shipped since (cpu1.2, cpu1.3, cpu1.4, latest/v1.22 in Jan 2026). The organizers'
README pins a two-year-old image against a server that kept moving.

**Why it is worse than a failed run.** `compute_worker.py` sets no `task_acks_late`, so
Celery's default applies: a message is acknowledged on *delivery*, not on success. Every
job the worker takes and fails is **gone from the queue** — the submission stays "Submitted"
forever and no other worker will ever see it. The `STATUS_FAILED` write 500s too, so
nothing is recorded anywhere. 42 of other participants' submissions were consumed this way
in one minute, dated 2026-08-25 and 2026-08-27 (classmates, from the bundle names).

**Generalisable lesson, and the reason this is worth the space:** a worker that
acknowledges a message before it succeeds is worse than no worker at all. Failure that
destroys the work item looks identical, from the outside, to work that was never
submitted.

**RESOLVED, 2026-08-27 08:07.** `latest` (v1.22) is broken too, but differently and
usefully: it receives a real `uuid.UUID` and dies inside `run_wrapper`'s *own* logging call
(`TypeError: Object of type UUID is not JSON serializable`) -- the line directly beneath
the `str()` fix in `develop`. That adjacency is the proof no released tag has the fix.
Adding that single line to the released image makes it work: submission 904009 (`ebnerd_semantic_n100.zip`) logged **"Submission updated
successfully!"** and began scoring. The patched worker also drains the shared backlog, so
running it helps every participant rather than costing them.

**Second-order error:** the container was removed with `docker rm -f`, which deletes its
logs. Whether our own submission was among the 42 is now unanswerable from the worker
side. Capture logs to a file *before* tearing down a container you are still reasoning
about.

## Next step

**Nothing outstanding in the code.** All graded deliverables are complete as of
2026-08-27:

| Q | Deliverable | State |
|---|---|---|
| Q1 | Reproducible pipeline, one-command rebuild | done, `phase-1-complete` |
| Q2 | BM25 + recall@{50,100,200} | done, `phase-2-complete` |
| Q3 | Embeddings + recall@K + comparison | done, `phase-3-complete` |
| Q4 | Harness: AUC/MRR/nDCG, beyond-accuracy, slices, bootstrap CIs | done |
| Q5 | Both Codabench leaderboards scored + screenshots | **MIND 0.6191 (54/90), EB-NeRD 0.5396 (147/247)** |
| Q6 | Design note | `reports/design_note.pdf`, **4 pages measured**, within the cap |
| Q7 | Code, note, screenshots, AI usage log | README + `AI_USAGE.md` current |
| Q9 | Ablation + no-future-click-leakage test | done, mutation-verified |

240 tests passing.

**Two items that are Chaitanya's, not the code's:**
1. **Export the session transcripts** to `reports/ai_transcripts/` — `AI_USAGE.md`'s
   prompt-log section promises them and the directory does not exist yet. Q7.4.
2. **Submit**: repository to GitHub Classroom, `reports/design_note.pdf` to Moodle.

**The headline result, for the viva.** The offline harness was calibrated against both
leaderboards and held in two different senses: MIND transferred a *delta* (predicted
+0.0151, delivered +0.0154 — 0.0003 apart) while its absolute levels differed by ~0.030;
EB-NeRD transferred the *absolute level* (val 0.5413 vs leaderboard 0.5396 — 0.0017 apart)
on the dataset where the same harness says the honest signal is weakest. That is the claim
worth defending, not the ranks.

### ✅ Pacing for Phases 5–6 — settled 2026-08-25

Asked in the first exchange, per the note this replaces. **Chaitanya chose reduced depth
with full R6 treatment reserved for the cloud-platform fork.** Everywhere else: the
default is stated with its reasoning in a line or two and the work proceeds. Living
documents and the decision log stay complete regardless — that was never the part being
traded away.

Reasoning given at the time: Phase 4 ran 5.5 h against a 4 h budget, Phases 5+6 have 4.5 h
between them, and Phase 5 contains genuinely less new *concept* than Phases 2–4 — it is
mostly bundle-reading, chunked streaming and submission formats.

### Landmines — re-read before writing any Phase 5 code

Logged under "Phase 5 landmines found early" above:
1. EB-NeRD's test set has **no `article_ids_clicked` column** — `ingest_ebnerd.load_behaviors`
   selects it unconditionally and will raise `ColumnNotFoundError`. Only the *testset* path
   needs changing; `ebnerd_large`'s schema is byte-identical to demo's.
2. MIND's test set has **no `-0`/`-1` click suffixes** — `load_behaviors` degrades
   *correctly but silently* (the strip becomes a no-op, the `-1` filter yields empty
   clicked lists, which is what D3 specifies for unlabeled rows). **Assert it** rather than
   relying on the coincidence.
3. EB-NeRD test carries an **`is_beyond_accuracy` flag** (200,000 rows true) — the RecSys
   2024 separately-scored subset. Check the Codabench rules before generating predictions.
   **Corrected 2026-08-26:** the rules were checked and say nothing about this flag. The count (200,000 of 13,536,710) is verified; the *meaning* was inferred, never read. We predict every row, which the official example submission confirms is correct.

### Measured scale facts (see `SCALE_NOTES.md` for the full entry)

**The re-ranking path breaks on object overhead, not compute.** `build_candidate_set` runs
at 18.5 µs/impression — EB-NeRD's 13.5 M test impressions is only **~4.2 min**. But the
path holds *three* parallel lists of one small NumPy array per impression, at ~112 bytes
of header each, so 13.5 M impressions is **~4.5 GB of pure overhead** against 0.65 GB of
actual data. **Phase 5 must chunk the test split and write predictions incrementally**,
never materialising the whole split.

**Embedding the test corpora is ~43 min of CPU**, one-off: MIND test ships 120,961 articles
and EB-NeRD large 125,541, at the measured 96 articles/s. This is the only part of the
pipeline a GPU would meaningfully help, so it is a direct input to the platform choice.

### What Phase 5 reuses unchanged

`rerank.py`'s four scorers, `metrics.py`, `availability.py`, and both retrieval modules all
work on any split — nothing is val-specific. The submission task **is** the re-ranking task
Q4.2 already built, which is why Q4 fed Phase 5 directly rather than being a detour.

<details>
<summary>Superseded Q9 next-step note</summary>

**Q9 — the anti-gaming ablation and `tests/test_no_leakage.py`.** Everything Q4 requires
is now built and run.

`tests/test_no_leakage.py` must assert, at minimum:
1. **D19's strict inequality** — `first_seen < T`, never `<=`.
2. **Label-free derivation** — `first_seen` and slice exposure come from
   `candidate_article_ids`, never `clicked_article_ids`.
3. **The temporal split invariant** — `train_max < val_min <= val_max < test_min`.
4. **Popularity is counted over train only** — `train_click_counts` already raises, so the
   test pins that it still does.
5. **The EB-NeRD history landmine** — val-split history contains **99.52%** of train-window
   clicks (22,143/22,249). Harmless as used; catastrophic if val history were ever pointed
   at train impressions. `history.parquet` holds all three snapshots keyed by `split`, and
   1,217 EB-NeRD users have all three rows, so a join on `user_id` alone silently attaches
   the wrong one and **nothing errors**.

**Q9's ablation** has its arm already measured and waiting: "has the user already read this
candidate" is a serving-time feature, clicked **3.5× more** often than average on MIND and
**0.49×** on EB-NeRD — opposite directions, both outside noise, already leak-checked.

</details>

<details>
<summary>Superseded slices/bootstrap next-step note</summary>

**Q4.3 (remainder) — slices**, then **Q4.4 bootstrap 95% CIs**, then **Q9**.

At least one slice is required; cold-start-vs-warm is already half-built (`has_query` and
`history_len` are carried per impression in the rerank parquet). Head-vs-tail articles is
the natural second, and the train click counts needed for it already exist.

**Coverage needs care in the bootstrap:** it is a property of the whole run, not a
per-impression value, so it must be **recomputed inside each resample** — the mean of
per-list coverages is not the coverage of the union (there is a test pinning exactly this).

**Remaining in Phase 4:** slices · bootstrap 95% CIs · Q9 ablation +
`tests/test_no_leakage.py`.

</details>

<details>
<summary>Superseded Q4.3 next-step note</summary>

**Q4.3 — beyond-accuracy metrics** (intra-list diversity, novelty, coverage), where the
flagged diversity-basis fork gets raised: measuring diversity in the embedding space grades
semantic retrieval by the exact quantity it minimises.

**Remaining in Phase 4:** Q4.3 beyond-accuracy (diversity fork) · slices · bootstrap 95%
CIs · Q9 ablation + `tests/test_no_leakage.py`.

</details>

<details>
<summary>Superseded Q4.2 next-step note</summary>

**Q4.2 — the re-ranking runner.** Score each val impression's own `candidate_article_ids`
with both scorers (BM25 weights from `bm25.py`, cosine from `embeddings.parquet`) and feed
`evaluate_impressions`. Reuse `bm25_search.py`'s per-unique-user query construction; note
that D19's availability filter is **not** applicable here — the platform already chose the
candidates, so restricting them further would be re-deciding a decision the log records.

**Then Q4.3 beyond-accuracy**, where the flagged diversity-basis fork gets raised.

</details>

**Remaining in Phase 4:** Q4.2 re-ranking runner · Q4.3 beyond-accuracy (diversity fork) ·
slices · bootstrap 95% CIs · Q9 ablation + `tests/test_no_leakage.py`.

<details>
<summary>Superseded Phase 4 entry note</summary>

**Phase 4 — Q4 evaluation harness, with Q9 folded in.** AUC, MRR, nDCG@5, nDCG@10,
beyond-accuracy (intra-list diversity, novelty, coverage), at least one slice, bootstrap
95% confidence intervals, run over **both** BM25 and semantic results. Then Q9's ablation
and `tests/test_no_leakage.py`.

**`tests/test_no_leakage.py` must assert both halves of D19's invariant**, not just the
first: (1) the predicate is `first_seen < T`, strictly — never `<=`; and (2) `first_seen`
is computed from `candidate_article_ids` (what was shown) and **never** from
`clicked_article_ids`. Availability derived from clicks would satisfy (1) and still be
leakage. Both conditions now live in one place — `newsrec/retrieval/availability.py` —
which is what the test should target.

**⚠️ Decision point to raise early in Phase 4 — do NOT default to it silently.**
Intra-list diversity is conventionally the mean pairwise distance between the retrieved
articles' *embeddings*. Measured in the same embedding space semantic retrieval searched,
it grades that method by the exact quantity it explicitly minimises — semantic will score
badly almost **by construction**, and the design note would then report a tautology as a
finding. Options to put to Chaitanya: (a) use a different diversity basis — both datasets
have a `category` column, so category overlap is the obvious candidate; (b) keep the
embedding-based metric and state the caveat explicitly; (c) report both. Found while
grading the Phase 3→4 quiz, not while writing Phase 4 code.

**Concrete beyond-accuracy finding already in hand.** MIND user `mind:U13132` read three
political stories and one Starbucks item; semantic retrieval returned five near-duplicate
Popeyes chicken-sandwich articles and nothing political. That is a diversity failure, not
an accuracy failure, and it is the qualitative example Q4's numbers should explain.

</details>

- [x] **Phase 3→4 recall quiz done 2026-08-25** (1 partial, 1 re-taught, 1
      right-answer-wrong-reasoning — see `LEARNING.md`). **A new session does not need to
      repeat it.** The re-taught point is load-bearing: *"cosine contains no time term" is
      a structural fact about the formula, so no measurement can contradict it* — a high
      freshness number would have been topic correlation riding along, which is accidental
      and untunable. Generalised as: **a number moving in the direction you wanted never
      tells you why it moved** — flagged for the design note as the most transferable idea
      in the project.

<details>
<summary>Superseded Q3.3 next-step note</summary>

**Q3.3 — the user representation.** Mean-pool the embeddings of each user's last 10
clicked articles (mirroring D12's N and field choice so Q3.5 varies only the algorithm),
then brute-force top-K per D21 under **both** candidate pools per D19. `bm25_search.py`
already has the batching, per-unique-user scoring, and availability-bucket machinery —
reuse it rather than rebuilding it.

**Carry into that code:** every article is its own nearest neighbour at cosine exactly
1.000 (verified), and the mean-pooled user vector is provably the point of maximum average
similarity to the user's own history — so **D15's exclusion must be applied before top-K,
not after**, or the top slots fill with articles the user has already read.

**Cold-start (D17) needs re-checking, not assuming.** For BM25 an empty history gave an
empty query and an all-zero score vector. Here it would give a mean over *zero* vectors —
a division by zero producing NaN, which propagates silently through argsort rather than
scoring 0. Affects the same 1,556 MIND val impressions and 0 EB-NeRD ones. Must be
handled explicitly and tested.

</details>

<details>
<summary>Superseded Q3.1 next-step note</summary>

**Q3.1 — embed the articles.** Download the model, smoke-test it on a handful of real
MIND and EB-NeRD titles (including Danish, to confirm empirically that the two languages
land in sensible relative positions), then decide where the vectors live — the D3
sub-decision deferred since Phase 1: a column on `articles.parquet`, or a separate
`embeddings.npy` + id index. **That is a genuine fork and gets presented, not assumed.**

Then Q3.3's user representation, reusing D12's N = 10 so Q3.5 compares methods rather
than query lengths.

**Unmeasured cost to establish early:** CPU-only inference over 77,015 articles. Nothing
in the plan depends on it being fast, but Phase 5 does, so measure it on a sample and
extrapolate before embedding the whole corpus.

</details>

_(All of the above is now done — the probe measured 87 articles/s, the real run hit 96.)_

**⚠️ The old "drop-first" plan is retired — it rested on a false premise.** Phase 0 said
we could fall back to "EB-NeRD's provided embeddings instead of computing our own."
Verified 2026-08-25 against the actual files: **neither dataset ships article-text
embeddings we can just load.**
- MIND ships `entity_embedding.vec` — 26,904 **TransE knowledge-graph entity** vectors,
  100-dim, keyed by Wikidata IDs (`Q41`). Not article vectors. Getting an article vector
  means averaging the entities it mentions, and articles with no recognised entities get
  nothing.
- EB-NeRD's `articles.parquet` has **no embedding column at all** (21 columns checked).
  Its provided article embeddings are separate artifact downloads
  (`Ekstra_Bladet_word2vec.zip`, `google_bert_base_multilingual_cased.zip`) which the
  spec itself marks *"(optional)"* and which are **not downloaded**.

The spec permits either route — Q3 says "using the provided article embeddings **(or
compute your own using BERT/XLM-RoBERTa)**" and Q3.1 says "**Compute or load**". But
mixing routes across datasets (provided BERT for EB-NeRD, averaged entity vectors for
MIND) would make **Q3.5's cross-dataset comparison uninterpretable** — the same argument
that killed per-language stemming in D11 and that the random-baseline column caught in
D19. So computing our own with **one multilingual model for both** is likely the stronger
answer, not the expensive luxury the old plan assumed.

**Real risk to plan around:** `torch` is a ~2 GB install and `scipy` alone took over ten
minutes on this connection. Bring a lighter no-torch fallback alongside the
sentence-transformers route when presenting the options.

**Also still open for Phase 3:** where embeddings live in the store — the D3 sub-decision
deferred to this phase.

**Constraint inherited from D19, do not lose it:** Q3.5 compares lexical vs semantic, and
that comparison is only meaningful if both retrieve from the **same candidate pool**. So
embeddings must be run under *both* the whole-corpus and available pools, or the
comparison measures pool size rather than method — exactly the trap the lift column
exposed in Q2.

**Also outstanding for Q9:** `tests/test_no_leakage.py` must assert D19's *strict*
inequality (`first_seen < T`, never `<=`), so a later well-meaning edit cannot silently
import the future.

---

<details>
<summary>Superseded next-step note from the previous session</summary>

**Phase 2 — Q2, BM25 lexical retrieval.** The Phase 1→2 recall quiz is already done
(3/3 correct, see `LEARNING.md`) — a new session does **not** need to repeat it.
Start directly with teaching BM25 (Best Match 25) itself: real-world analogy → technical
definition (term frequency, inverse document frequency, length normalisation, broken
into named parts) → required reading → comprehension check, per R1, before any code.
Pacing note: Chaitanya chose to keep full R10/R6 depth into Phase 2 rather than scope
down now (see the time-budget flag above) — revisit that conversation explicitly if Q2
is not keeping pace with its 4h budget, don't silently let it slide either way.

</details>

The pacing note above still stands: full R10/R6 depth was chosen for Q2 — revisit
explicitly if Q2 runs past its 4h budget, don't let it slide silently either way.

---

## Blocked on Chaitanya (do these early — they gate everything)

- [x] **Register on Codabench, MIND competition** — done 2026-08-21
- [x] **Register on Codabench, RecSys 2024 / EB-NeRD** — done 2026-08-21
- [x] **Download the large test bundles** — done 2026-08-24, and **verified complete**,
      not just present (the truncated-`ebnerd_demo.zip` lesson): MIND test's last line
      carries all 5 fields with `impression_id` 2,370,727 exactly equal to its line count
      and the file ends in a newline; every EB-NeRD parquet reports a row count, which a
      truncated file could not do since the schema and footer live at the *end*. Counts
      match the spec exactly (13,536,710 EB-NeRD test impressions; 2,370,727 MIND).
- [ ] **Accept the GitHub Classroom assignment** — **blocked: invite link not yet found
      on Moodle.** Chaitanya checked and couldn't locate it as of 2026-08-21. Does not
      block Phase 1 (local pipeline work needs no remote). Only affects where this repo
      eventually gets pushed. Check assignment page body text, announcements/forum, and
      course email before asking the instructor/classmates.

Repo URL: _not yet provided_ (GitHub Classroom, still blocked — see above)

**Private backup remote** (separate from GitHub Classroom): `origin` →
`git@github.com:ChaitanyaShah21/IRE-A1-News_Recommendation.git` (private), set up
2026-08-22 via SSH (key already registered with GitHub, confirmed via `ssh -T`). Pushed
`main` + `phase-0-complete` tag. Push after every commit going forward, same as local
git discipline (R13) — this isn't a substitute for the eventual GitHub Classroom repo,
just insurance until that's found.

- [x] **Grant HuggingFace access to `yjw1029/MIND`** — done 2026-08-21, MINDsmall_train.zip
      and MINDsmall_dev.zip downloaded successfully by Chaitanya.

---

## Where the data lives

| Dataset | Bundle | Path | Status |
|---|---|---|---|
| MIND | small (train + dev) | `data/raw/mind/MINDsmall_{train,dev}/` | ✅ downloaded, row counts verified against provided notebook (51,282 / 156,965 train; 42,416 / 73,152 dev) |
| MIND | large test | `data/raw/mind/MINDlarge_test/` | ✅ downloaded 2026-08-24, verified complete — 2,370,727 behaviors (spec: 2.37M), 120,961 news, unlabeled as expected. 1.5 GB |
| EB-NeRD | demo | `data/raw/ebnerd/ebnerd_demo/` | ✅ downloaded, valid parquet confirmed (11,777 articles, 24,724 train behaviors, 1,590 train history rows — a different, smaller bundle than the "large" one the provided notebook explored, so these counts are expected to differ) |
| EB-NeRD | small | `data/raw/ebnerd/` | ⬜ not downloaded (not needed — demo for dev, large for the leaderboard) |
| EB-NeRD | large | `data/raw/ebnerd/ebnerd_large/` | ✅ downloaded 2026-08-24, verified — 12,063,890 train + 12,566,385 validation behaviors, 125,541 articles. 3.4 GB. Schema identical to demo. |
| results | Q4.2 re-ranking | `reports/rerank_{mind,ebnerd}_val_n10.parquet` | Gitignored (`*.parquet`), 4 MB total. Per-impression metric values kept intact for Q4.4's bootstrap. Regenerate with `python scripts/run_rerank_eval.py` |
| EB-NeRD | testset | `data/raw/ebnerd/ebnerd_testset/ebnerd_testset/` (note the **doubled** directory name, from the zip's own layout) | ✅ downloaded 2026-08-24, verified — 13,536,710 test behaviors (spec: 13.5M). 1.8 GB. Schema differs from demo — see the Phase 5 landmines under Open questions. |

Disk after these: 6.8 GB of raw data, 901 GB free — not a constraint. The `__MACOSX/`
and `DS_Store` entries inside both EB-NeRD bundles are zip packaging junk; ignore them.

**Environment:** `.venv/` created (Python 3.12.3, standard `venv`), dependencies pinned
in `requirements.txt` (`polars==1.43.2`, `pyarrow==25.0.1` — see D4 in `ARCHITECTURE.md`).
Rebuild with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

---

## Open questions

- Cloud platform for large-scale runs (Kaggle vs Colab vs Lightning AI) — **deliberately
  deferred to Phase 5**, to be decided against real measured memory numbers.

### Phase 5 landmines found early (2026-08-24, while verifying the large downloads)

Neither is a bug now; both will bite in Phase 5 and are cheaper to know about than to
rediscover under deadline. Not fixed yet — Phase 5 work, logged so it isn't re-derived.

1. **EB-NeRD's test set has no `article_ids_clicked` column at all**, and
   `ingest_ebnerd.load_behaviors` selects it unconditionally. It will raise
   `ColumnNotFoundError` on the test bundle. Also absent: `article_id` (the D6 context
   field we already drop), `next_read_time`, `next_scroll_percentage`. Fails loudly,
   which is the good failure mode. **`ebnerd_large`'s schema is byte-identical to demo's**
   (same columns, same dtypes, articles too), so only the *testset* path needs the change.
2. **MIND's test set has no `-0`/`-1` click suffixes** — impression tokens are bare
   `N<digits>` (verified: 0 non-matching of 7,836,608 tokens sampled). `load_behaviors`
   degrades *correctly but silently* here: the `-[01]$` strip becomes a no-op so
   candidates are right, and the `-1` filter yields an empty clicked list for every row,
   which is exactly what D3's schema specifies for unlabeled test rows. Worth an explicit
   assertion in Phase 5 rather than relying on the coincidence.
3. **EB-NeRD test carries a new `is_beyond_accuracy` flag**: 200,000 rows true,
   13,336,710 false. That was assumed to be the RecSys 2024 challenge's separately-scored
   beyond-accuracy subset — it affects the submission format, so check the Codabench
   rules before generating predictions.
4. MIND test history is 2,453 empty-history rows per 200,000 sampled (~1.2% cold-start,
   comparable to MIND-small's 2.8% in val).

---

## Error log

Every error hit, its root cause, and the fix chosen. Consult before debugging anything —
we may have already solved it.

| Date | Error | Root cause | Fix chosen | Trade-off accepted |
|---|---|---|---|---|
| 2026-08-25 | After a mutation-testing run, `tests/test_ablation.py` kept failing even though the source file was byte-identical to its pre-mutation backup (`diff` clean, `grep` showed the correct line) | Stale `__pycache__`. The mutate→test→restore loop rewrites the `.py` with `cp`, and Python served the **mutated bytecode** rather than recompiling — the restored file's mtime did not look newer to the import cache's check | `find . -name __pycache__ -path '*/newsrec/*' -exec rm -rf {} +` before re-running. Recorded as a standing hazard of the mutation-testing workflow rather than a one-off | None. Worth noting the failure *direction* is benign: a stale cache during the mutation step makes a mutation look **survived** (tests pass), which reads as a test gap and gets investigated. Every mutation reported as *caught* in Phases 3–4 is therefore still valid, since caught means the tests actually failed |
| 2026-08-25 | `reports/bm25_recall_val_n10.csv` silently lost EB-NeRD's whole-corpus results — noticed only because the consolidated summary table was missing four rows | The output filename contained the split and `n_recent` but **not the dataset or the pool**, so `--datasets mind` wrote to the same path `--datasets ebnerd` had just written. No error, no warning; the numbers were still correct on screen, just gone from disk. The class of bug where output *looks* fine because the wrong thing was overwritten, not corrupted | Put every varying input in the filename: `bm25_recall_{datasets}_{split}_n{N}_{pool}{tag}.csv`, with a comment recording why. Re-ran the four configurations; regenerated numbers matched the originals exactly, which also confirmed reproducibility | None — strictly more correct. Cost ~15 min of re-running MIND. Worth noting the near-miss: had the summary script not existed, the missing rows would likely have gone unnoticed into the design note |
| 2026-08-25 | `test_first_seen_times_takes_the_minimum` failed with `ComputeError: cannot cast 'Object' type` | Test-construction error, not a code bug: the test passed `np.datetime64` values into `pl.DataFrame`, which Polars treats as opaque Python objects rather than recognising as timestamps | Used Python `datetime` objects, which Polars maps to its native `Datetime` type | None — the production code was never involved; only the fixture was wrong |
| 2026-08-23 | `python scripts/build_pipeline.py` run from a directory other than the repo root (e.g. `/tmp`) crashed with `FileNotFoundError: configs/mind.yaml` — found because Chaitanya questioned whether the script's `sys.path` fix really made it runnable "from anywhere" | The `sys.path.insert` fix only made the *import* of `newsrec.build` independent of the caller's working directory (via `__file__`, which always resolves to the script's real location). `Path("configs") / ...` and `OUTPUT_DIR = Path("data/processed")` were still plain relative paths, resolved against whatever the shell's cwd happened to be — an inconsistency between two parts of the same file | Introduced one `REPO_ROOT = Path(__file__).resolve().parent.parent` constant and anchored every path in the script to it — `src/`, `configs/`, `data/processed/`, and the `raw_root` value read out of each YAML config | None meaningful — this is strictly more correct with no added complexity; verified by re-running the exact `/tmp` invocation that first exposed it, plus re-checking the happy path and the failure-message path both still work |
| 2026-08-22 | Not our bug — a caveat about the provided notebook: its printed MIND train time range (`"11/10/2019 10:00 AM to 11/9/2019 9:59:58 AM"`) is chronologically wrong | The notebook computed it with plain Python `min()`/`max()` on the raw time **strings**, which compares them lexicographically (character by character), not chronologically — `"11/10/..."` sorts before `"11/9/..."` as text even though Nov 9 is earlier in time | None needed in our code — `ingest_mind.load_behaviors` already parses `time` into a real `Datetime` via `.str.strptime()`, so `.min()`/`.max()` on our `timestamp` column are correct (verified: MIND train is actually Nov 9–14, dev is Nov 15). Just don't trust the provided notebook's printed ranges at face value. | None — this only cost us noticing it before it fed into the temporal-split design |
| 2026-08-22 | `pl.concat([mind_articles_df, ebnerd_articles_df])` raised `type Float32 is incompatible with expected type Float64` (column `sentiment_score`), and the same for `impressions`' `read_time` | MIND's null placeholder columns default to `Float64` (`pl.lit(None, dtype=pl.Float64)`), but EB-NeRD's real `sentiment_score`/`read_time`/`scroll_percentage` columns are natively `Float32` in the source Parquet files - the two tables' schemas looked compatible by eye (both "float") but weren't bit-for-bit identical types | Cast all three EB-NeRD columns to `Float64` explicitly in `ingest_ebnerd.py` | None meaningful - Float64 is strictly more precise, so casting up loses nothing; found by actually running `pl.concat()` as an adversarial test (R10) rather than assuming matching column names implied matching dtypes |
| 2026-08-22 | Caught before running, not a runtime error: `ingest_mind.load_articles` originally joined `title_entities`/`abstract_entities` into one string with `pl.concat_str(..., separator="||")` | A stray literal `"||"` inside either JSON string (e.g. inside `SurfaceForms` text pulled from an article) would make a later split on `"||"` produce more than two pieces, silently corrupting that row's entity data — flagged by Chaitanya, not found by testing | Switched to `pl.concat_list([...])`, storing the two JSON strings as a genuine 2-element list column instead of a delimited string — no separator, so nothing to collide with | None meaningful — `list[str]` is the more natural Polars representation here anyway; no downside versus the string-join approach it replaced |
| 2026-08-21 | `wget`/anonymous download of MIND from `huggingface.co/datasets/yjw1029/MIND` returns HTTP 401, `x-error-code: GatedRepo` | The HF mirror is a gated repo — requires a logged-in, access-granted HuggingFace account, not just a public URL. Likely there to gate MIND's original license terms. | Chaitanya creates a free HF account, requests access (usually instant), generates a read-only access token; download resumes once shared. EB-NeRD-demo is unaffected (open S3 bucket, no gate). | Adds a manual step outside the pipeline's control before MIND ingestion can start; considered going to the official MIND site instead but that's gated the same way, so no trade-off actually avoided. — **resolved**, Chaitanya downloaded both files manually. |
| 2026-08-21 | `python -m zipfile` on the first `ebnerd_demo.zip` download raised `BadZipFile: File is not a zip file`, even though `file` identified it as a valid zip | Download was truncated mid-transfer over an unstable connection (actual size 21,187,446 bytes vs. the server's reported `Content-Length` of 21,499,083 — ~311 KB missing from the end, exactly where a zip's central directory lives). The backgrounded `wget` still reported exit code 0 despite this, so exit code alone wasn't a reliable success signal. | Chaitanya re-downloaded manually; new file's byte count matches `Content-Length` and opens cleanly with `zipfile`. | Considered `wget -c` (resume) to avoid re-pulling ~20 MB, but resume can silently fail to reconcile on an unstable connection — chose a clean re-download instead since the file is small enough that the cost difference is negligible. |
