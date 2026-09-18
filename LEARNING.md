# Learning Log

One section per concept, added before the concept is used in code, plus every
comprehension-check answer and anything that needed re-teaching.

**Scope change, 2026-08-25 (R1 amendment).** Up to Phase 2 this file was "Required
Reading" — external sources with what to take from each. With two days to the deadline
Chaitanya dropped external reading; concepts are now taught in chat, plain-language first
and then built up to the technical statement. Earlier sections are kept as written.
The comprehension-check record continues unchanged — it is the part that matters.

---

## Phase 3 → Phase 4 recall check (2026-08-25)

Three questions: where a `-inf` → `0.0` "simplification" would be exposed; whether a high
freshness number would contradict "cosine has no time term"; and predicting intra-list
diversity. **One partial, one wrong, one right-answer-wrong-reasoning. A new session does
not need to repeat this quiz — but should be aware of the gaps below.**

**Q1 — principle right, application missing.** Correctly identified that 0.0 is mid-range
for cosine so masked articles outrank negative-scoring ones. Did not answer which run
exposes it. Taught: **EB-NeRD/available**, because it masks ~8,814 of 11,777 articles
(75%) into a surviving pool of ~2,478–3,385, so masked articles flood a 200-slot list —
whereas MIND/whole-corpus masks only ~15 of 65,238 and the bug is invisible. General rule
given: *a masking bug is exposed by the run that masks the most into the smallest
surviving pool*, so that is the configuration to check first, not the fastest one.

**Q2 — wrong, and re-taught in full.** Answered "yes, 60% fresh would contradict it". The
correct answer is **no**. Key distinction, which had not landed: *"cosine similarity
contains no time term" is a **structural** fact readable off the formula* — no empirical
measurement can contradict something verifiable by inspection. A 60% result would have
been **correlation**: a breaking story makes fresh articles topically similar to recent
reading, so cosine ranks them highly *because of topic*, with freshness riding along. Why
that matters practically: such an effect is accidental and unreliable — it holds when the
news cycle aligns and vanishes when it doesn't, so it cannot be tuned, controlled, or
reported as a property of the system. Terms also re-explained on request ("fresh",
"corpus baseline" as the what-you-get-without-trying number).

**Named as a rule rather than three anecdotes** (D19's random baseline, D11's stemming,
and this): **a number moving in the direction you wanted never tells you why it moved.**
Flagged as the most transferable idea in the project — belongs in the design note.

**Q3 — right answer ("worse"), reasoning argued for the opposite.** The stated reason
("BM25 gives articles with common words so they'd be similar") is an argument that *BM25*
is the less diverse one. Corrected mechanism: semantic ranks by proximity in a continuous
space, so near-duplicates are neighbours *of each other* as well as of the user vector and
one dense cluster fills the whole top-K (the Popeyes result); BM25 matches each article to
the *query*, so retrieved items need not resemble one another.

**Raised for Phase 4 as a decision point:** intra-list diversity is normally the average
pairwise distance between retrieved articles' **embeddings**. Measured in the same space
we retrieved with, semantic retrieval is graded by the quantity it explicitly minimises
and will look bad almost by construction. Not invalid, but it must be stated or the design
note reports a tautology as a finding.

---

## Phase 3 — Embeddings and nearest-neighbour search (2026-08-25)

**Taught in chat** (no external reading, per the amendment above): the warehouse analogy
— articles placed by position rather than filed by word, so synonyms sit on adjacent
shelves for free but exact rare terms have no drawer to look in; embeddings as a
fixed-length vector of real numbers; cosine similarity broken into dot product, norm, and
the division that strips magnitude out; L2 normalisation collapsing cosine into a plain
dot product so ranking becomes one matrix product; mean pooling as the user
representation Q3.3 asks for; ANN (Approximate Nearest Neighbour) as the aisle-signs
trade of exactness for speed.

**Comprehension check — 2 of 3 needed work.**

**Q1 (normalisation) — right, sharpened.** Answer correctly had "denominator becomes 1".
The imprecise half was *what* gets promoted without normalisation. Sharpened: write
`u·a = cos(u,a) × ‖u‖ × ‖a‖`. When ranking all articles for **one** user, `‖u‖` is the
same constant in every score, so it cannot reorder anything — **only the article norms
`‖a‖` distort the ranking**. Ranking by raw dot product is ranking by `cosine × ‖a‖`.
Second point added: the bias is *systematic*, promoting the same high-norm articles into
every user's top-K, which would surface in Q4's coverage and intra-list-diversity metrics
as a fake "lacks diversity" finding.

**Q2 (does D15's exclusion argument still apply?) — answered "less strongly", the answer
is MORE strongly. Re-taught.** The reasoning given — "embeddings are approximations, not
exact matches" — is true of embedding matching in general but misses that the user vector
is not an approximation *of* the history articles, it is **built out of them**. Exact
argument: maximising `Σᵢ cos(u, aᵢ)` over unit `u` gives `u ∝ Σᵢ aᵢ`, i.e. the normalised
mean. So **the mean-pooled user vector is precisely the point in the whole space with the
highest average similarity to that user's own history**. The self-match falls out of the
arithmetic. With BM25 it was merely emergent — a bag of words from those titles, which
another article sharing a rare high-IDF term can genuinely outrank. D15 therefore carries
*more* weight in Q3 than it did in Q2, at unchanged measured cost (0.19% MIND / 0.47%
EB-NeRD of ground-truth clicks).

**Q3 (English-only model on Danish) — first half right, second half not attempted.**
Mechanism sharpened: it would not refuse the text. An English tokeniser fragments Danish
into subwords and returns 384 well-formed numbers with sensible norms and no warning —
confident nonsense. The unanswered half is the one that matters: **why silent degradation
beats a crash in danger.** Because the number still looks like a number. EB-NeRD semantic
recall@200 would land somewhere plausible next to BM25's genuine 2.45%, and we would write
*"semantic underperforms lexical on Danish"* — reading as a **finding about methods** when
it is a **bug in our setup**, corrupting Q3.5 specifically. A crash costs an hour; a wrong
number gets submitted.

**This is now a three-time pattern worth naming in the design note**, not three anecdotes:
D11 rejected per-language stemming because divergent processing would poison the
cross-dataset comparison; D19's random-baseline column caught EB-NeRD's "3× improvement"
that was really a shrinking pool; and here. **And it was not hypothetical** — the
smallest, fastest-looking multilingual model on the menu,
`distiluse-base-multilingual-cased-v1`, turned out to have no Danish in its language list.
The trap was in the menu.

---

## Phase 0 — Orientation: the assignment as a whole

Read before we started building anything, to ground the plain-language walkthrough in
the actual papers rather than a summary of a summary.

| Source | What to take from it | Time |
|---|---|---|
| MIND paper — Wu et al. 2020, §3 (Dataset) | How impressions, click history, and behaviors are structured — this is the schema Q1 unifies into | ~15 min |
| EB-NeRD paper — Kruse et al. 2024, §3 (Dataset) | Same, for the Danish dataset; note the structural differences from MIND — feeds the Q3.5 cross-dataset comparison | ~15 min |
| `notebooks/00_provided_*.ipynb` (both, skim) | Actual column names, dtypes, row counts — ground truth for what gets coded against | ~15 min |
| Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond* (2009), §1–2 | Where BM25 comes from and why it beats raw word-counting — needed before Phase 2's BM25 implementation, not before | ~20 min |

**Recall check (end of Phase 0):** three questions asked on why temporal (not random)
splitting is required, what distinguishes Q2 (BM25) from Q3 (embeddings), and why Q4
grades ranking metrics on top of Q2/Q3's recall@K. First two answers needed re-teaching
before Phase 0 closed — logged in the decision log / error log as a gap, not an error,
since nothing broke; corrected via re-explanation, not code. Points to remember:
- Temporal split isn't just "test on later dates" — it exists so the offline test matches
  what the model will actually know at serving time (only the past, never the future).
- BM25 and embeddings differ in *matching mechanism* (literal words vs. meaning), not in
  speed or in one being objectively better — which one wins is the empirical question
  Q3.5 asks us to answer, likely differently per slice.

---

## Phase 1 → Phase 2 recall check (2026-08-23)

Three questions before starting Phase 2: why dataset-prefix every ID, why not
random-shuffle both datasets into one split, why raw data can't be deleted once the
feature store exists. All three answered correctly on the first pass — Q2 and Q3 got a
small addition each (mixing two datasets' unrelated timelines is a second problem beyond
plain leakage; raw data is the only *irreplaceable* thing in the pipeline, since
processed data is fully derived and rebuildable from it). No re-teaching needed.

---

## Phase 2 — BM25 (Best Match 25) and the inverted index

Issued 2026-08-23, before any Phase 2 code. Read in this order — each one assumes the
previous.

| Source | What to take from it | Time |
|---|---|---|
| Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, §1.1–1.2 (free online) | What an inverted index *is* as a data structure — the term → posting-list mapping, and why you never score a query by scanning every document. Stop once you can draw the index for a 3-document toy corpus. | ~15 min |
| Same book, §6.2 (term frequency & weighting) then §11.4.3 (Okapi BM25) | Why raw term counts are a bad relevance score, how inverse document frequency fixes part of it, and then the exact BM25 formula with `k1` and `b`. §11.4.3 is two pages — that's the core of Q2. | ~25 min |
| Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond* (2009), §1–2 | Where BM25 comes from — that it's a *probabilistic* model of relevance, not a hand-tuned heuristic that happens to work. Read for the intuition, not the derivations. | ~20 min |

Concepts taught before this reading was issued (analogy → technical definition → check):
term frequency saturation, inverse document frequency, document-length normalisation,
`k1`/`b`, and the retrieval-vs-re-ranking distinction restated in BM25 terms.

**Comprehension check (2026-08-24), three questions.** Right conclusions, wrong
mechanisms twice — both corrected with worked arithmetic before any code was written:

- **IDF cannot explain why one *document* outranks another.** Its formula contains only
  `N` and `n(t)` — corpus and term, no `D` at all — so for a given query term it is one
  constant multiplying every document's score equally. IDF differentiates between
  *terms*, not between documents. What separated the two documents in the question was
  the length bracket: three mentions in 12 tokens scores 1.72, three in 60 tokens scores
  1.10 (`avgdl`=20, `k1`=1.5, `b`=0.75) — same numerator, all the difference in the
  denominator.
- **`k1 = 0` deletes length normalisation as well as saturation.** The whole length
  bracket is multiplied by `k1`, so zeroing it makes `b` unreachable. The score collapses
  to `sum of IDF(t)` over query terms present: length-blind and repetition-blind, not
  "shorter documents win".
- **BM25 does not take a log of term frequency — that's TF-IDF.** BM25 damps repetition
  with a saturating rational function `f(k1+1)/(f + k1*...)`, which has a hard ceiling of
  `k1+1`; a log grows forever, just slowly. The only logarithm in BM25 is in IDF. Worked:
  3x the mentions buys 1.44x, and infinite mentions would buy only 1.84x.
- The third question (why a 300-title query retrieves worse than a 10-title one) was not
  attempted, and is not derivable from the formula — which was the point of asking. Taught
  instead: **BM25 contains no time term of any kind**, so topic drift cannot be tuned
  away and must be handled in query construction or not at all. This became D12.

**CSR/CSC re-taught from scratch on request (2026-08-24)**, worked by hand on constructed
corpora rather than described. The second attempt got the row structure and the empty-row
case right; the correction was that `data[p]` pairs with `indices[p]` **by tape
position**, not with the vocabulary in alphabetical order. Three arrays, three jobs:
`data` = what, `indices` = which column, `indptr` = which row. Points to remember:
- `indptr` holds **positions into `data`/`indices`**, never column numbers, and has one
  more entry than there are rows — n regions need n+1 boundaries.
- Document numbers repeat freely across `indices`; each term's run is an independent list.
- `indptr[j+1] - indptr[j]` is the posting-list length, which **is** `n(t)`, which feeds
  IDF — the data structure and the formula describing the same thing from two directions.

---

## Phase 2 → Phase 3 recall check (2026-08-25)

Three questions: what breaks if queries used title+abstract like the index does; why
EB-NeRD's 2.45% → 7.27% is not a 3× improvement; and the two leak-safety properties of
`first_seen < T`. **Two solid, one re-taught.**

**Q1 — needed re-teaching.** Answer had the mechanism ("longer query") but framed the
consequence as diminishing returns and "not significant". The correction: it undoes
**D12**, and the failure mode is **topic drift**, not dilution — diminishing returns means
extra input stops helping, drift means it actively points somewhere wrong. Measured on our
own corpus: mean title 11.2 tokens vs mean abstract 36.1 on MIND, so a 10-article query
goes **112 → 472 tokens, 4.2×**. Those extra tokens are peripheral entities and
boilerplate from the same articles, so the query stops describing what the user wants and
starts describing everything adjacent to what they read. And because **BM25 has no time
term**, no parameter can undo it afterwards. Stated explicitly at the time: this is
mechanism, not evidence — we did not run the ablation, and saying "it is worse" without
the run would be overclaiming.

**Q2 — correct**, including the key standard: to claim a 3× improvement, the *lift over
random* would have had to triple. One causal link tightened: the random baseline rose
because the **pool shrank** (11,777 → ~2,963; random recall@200 is just `200/pool_size`),
not directly because clicks are recent. Keeping those separate matters — the baseline
would rise identically for any filter that shrank the pool, including a useless one, which
is exactly why the baseline column is the check.

**Q3 — (a) correct, (b) half.** (a) sharpened: the problem with `<=` isn't only that the
article "wasn't there before", it's that our *knowledge it exists* comes from the very
impression being predicted — circular. (b) had the temporal half (the predicate only
admits facts true before T) but missed the second, which is the one Q9 actually grades:
`first_seen` is computed from `candidate_article_ids` — what was **shown** — and never
from `clicked_article_ids`. Availability derived from clicks would still satisfy "only
uses the past" and still be leakage, because the pool would be pre-selected by the
answers. **Both conditions are required: temporal AND label-free.** Argue only the first
in the design note and a careful grader will ask about the second.

---

## Phase 1 — Unified schema

Required reading for this concept was done directly against ground truth rather than
external sources: both provided notebooks (`notebooks/00_provided_*.ipynb`) were read in
full to confirm actual column names, types, row counts, and null rates before teaching
the schema-unification concept.

**Recall check:** three questions on splitting MIND's `impressions` string, why
duplicated per-dataset logic is a problem, and which dataset needs reshaping for a
per-user history table. All three answered correctly; Q2's answer needed a concrete bug
scenario added (a tokenizer fix applied to one duplicated pipeline but not the other,
silently corrupting the Q3.5 cross-dataset comparison) — logged here, not re-taught from
scratch. Confirmed structural facts to remember:
- MIND TSVs have no header row — column names are supplied by code, not the file.
- EB-NeRD Parquet is self-describing and lazily scannable, which is how the 12M+ row
  behaviors files get explored without exhausting RAM.
- The unified schema is a **superset**: dataset-unique columns (sentiment, body text,
  entity embeddings) stay in, null for the dataset that lacks them — nothing is dropped.

---

## Phase 4 — ranking metrics (AUC, MRR, nDCG)

**Taught in chat** per R1's 2026-08-25 amendment: newsagent-rack analogy → each metric's
formula broken into named parts → comprehension check. Formulas were initially written in
LaTeX and **did not render in the terminal**; re-issued as plain-text/ASCII maths at
Chaitanya's request. Practical note for the rest of the assignment: *no LaTeX in chat
output — use fenced ASCII formula blocks.*

**Comprehension check — 1 sharpened, 1 correction to Claude's own wording, 1 solid.**

**Q1 — correct mechanism, number added.** RR = 1/3 ✓, and the AUC reasoning ("only the
pairs with the two items above it are wrong") was exactly right. Sharpened by putting a
number on it: 19 pairs, 2 wrong, AUC = 17/19 = 0.895. The extension taught from it is the
one that matters: **the same rank 3 gives AUC 0.895 in a rack of 20 and 0.333 in a rack of
4, while MRR is 1/3 in both.** AUC normalises by how many items you could have beaten;
MRR does not. Consequence for the design note: MIND's and EB-NeRD's AUCs are **not
comparable to each other**, because their rack sizes differ (median 22 vs 9).

**Q2 — right diagnosis; Claude's word "vacuous" was wrong and was corrected.** Chaitanya
correctly identified that EB-NeRD's median rack of 9 puts the whole list inside a `@10`
cutoff, and correctly preferred nDCG@5 there. The correction was to Claude's phrasing: a
rack fully inside the cutoff does **not** score 1.0 for everyone — the position discount
still runs. What actually happens is that **nDCG@10 stops being a top-k metric and
silently becomes nDCG@all**, a full-list ordering measure close to what AUC already
reports. So on EB-NeRD we report four metrics carrying roughly three independent signals.
Logged because the corrected version is the one that goes in the design note.

**Q3 — solid.** "Only candidates shown are marked; the other 200 retrieved are not shown"
is exactly the point. The phrase to keep: **unshown is not the same as not-clicked.**
Treating the ~65,000 unretrieved corpus articles as negatives would invent that many facts
per impression the log never recorded. This is the `CLAUDE.md` §6 retrieval-vs-re-ranking
trap, and Chaitanya identified it unprompted.

**Concept taught alongside, not quizzed: tie handling (D23).** The load-bearing idea is
that a default can be non-neutral — `np.argsort` is *stable*, so "not choosing" a tie
policy silently chooses "rank by position in the raw candidate list". Verified that order
carries no click signal (0.5017 / 0.4961 against a uniform 0.5) rather than assuming it.
Generalises the Phase 3→4 lesson: **a number coming out fine is not evidence the mechanism
is sound** — here, a fine-looking MRR would have been produced by a leaky tiebreak just as
readily as by a good ranker.

---

## Phase 4 — Q4.2, what re-ranking measures that retrieval does not

Not a quizzed concept; recorded because the result reframed something we thought we
already knew.

Phases 2 and 3 concluded "BM25 is weak on EB-NeRD" (1.07–1.21× lift over random). Q4.2
found something stronger and different: **BM25 is at exactly chance when re-ranking**
(AUC 0.4966 against random's 0.4987). Those are not the same statement, and the gap
between them is the idea worth keeping:

> Retrieval and re-ranking are different jobs on different pools. Finding the right
> neighbourhood among 11,777 articles is a task lexical overlap can partly do. Ordering
> the ~9 the platform *already selected* is a task where the easy signal has been spent —
> everything in `article_ids_inview` is plausible for that user by construction, so
> "similar to what they read" no longer separates plausible from clicked.

Generalised: **a candidate generator upstream of you changes what your own signal is worth.**
A method's score on a pool it didn't choose says little about its score on a pool someone
else pre-filtered in its favour.

**Verification habit reinforced.** The result was checked before it was believed, in two
independent ways: the scorer was compared against a per-impression computation written
separately (max deviation 1.9e-06), and the random arm was confirmed to land on AUC 0.5007
/ 0.4987. The second is the cheap one worth remembering — **a baseline whose correct value
you know in advance is a test of the whole harness**, not just of the baseline. Had random
come out at 0.62, every other row would have been unreadable.

Related, and the same shape as the Phase 3→4 quiz lesson: EB-NeRD's popularity baseline
scores *below* chance (0.4647). The tempting reading is "the baseline is broken". The
measured cause is that 86.9% of val candidates were never clicked in train, so surviving
train popularity is a staleness marker. **A number moving the wrong way is a finding when
you can name the mechanism, and a bug when you cannot** — the direction alone does not
distinguish them.

---

## Phase 4 — Q4.3, beyond-accuracy metrics

**Taught in chat:** newsagent-rack analogy → ASCII formulas for intra-list diversity,
novelty and coverage → comprehension check. Motivated by a failure already in hand rather
than a hypothetical: Phase 3's Finding 4, where semantic retrieval returned five Popeyes
chicken-sandwich articles to a user who read three political stories, and every accuracy
metric would have called that a good list.

**Comprehension check — 2 of 3 parts right, 1 corrected; second question solid.**

**Q1 (a degenerate system: the single most-clicked article, repeated).** ILD = 0 ✓ and
coverage ≈ 0 ✓ (precisely 1/65,238 = 0.0015%). **Novelty was answered as 1 and is not.**
The direction was right — it is the *minimum* achievable — but the minimum is **5.78 on
MIND's real train counts** (6.13 after smoothing), not 0 or 1, because `p` is the article's
share of *all* clicks and in a 65,238-article corpus even a runaway hit takes 1.8% of them.

The generalisation, which is the part that matters:
> **Diversity and coverage are bounded in [0, 1] and can be read absolutely. Novelty is
> unbounded, and its scale is a property of the corpus.** MIND's range is 6.13–18.20 and
> EB-NeRD's is 8.01–15.16, so a raw novelty figure means nothing alone and **the two
> datasets' novelty numbers are not comparable to each other.**

Same trap as AUC's sensitivity to candidate-list length in Q4.1 — a metric that looks
absolute while silently carrying the dataset's scale. Second instance in one phase, so it
is a pattern rather than a coincidence, and worth a line in the design note.

**Q2 (semantic scoring 0.15 category-ILD against BM25's 0.55).** Answered correctly:
semantic traded topical range for cosine proximity, and that is bad in cases like this one
but not always. Two sharpenings added:
- On the *category* basis, 0.15 means **85% of all pairs share a category** — not "less
  variety within a topic" but a collapse to essentially one topic.
- Pushing "not always worse" to its conclusion: **a purely random recommender scores best
  on all three beyond-accuracy metrics.** So read alone they do not merely fail to rank
  systems, they rank the worst one first. They price what a method *gave up*, and only
  mean something read against the accuracy table — which is why D24's random arm is run
  through this module too.

---

## Phase 4 — Q9, what leakage is actually worth

Not a quizzed concept; recorded because the measurement reframed the whole phase.

The abstract version — "don't leak future information" — was already understood. What the
ablation added is a **price**:

> On EB-NeRD, the *same* popularity algorithm scores AUC 0.4647 counting training-window
> clicks and 0.6657 counting the evaluated window. Our best honest system (semantic)
> scores 0.5331, and beats random by 0.0344. **One leaked feature is worth about four
> times the entire honest modelling effort of Phases 2–4.**

Three ideas worth carrying past this assignment:

1. **Leakage is the only bug whose symptom is a better number.** Every other failure here
   announced itself — a traceback, a NaN, an implausible figure. A leak announces itself
   with success, which is the one result nobody investigates. That is why Q9 demands a
   *test* rather than a check: it has to be asserted, because it cannot be noticed.

2. **A leak is worth most exactly where honest methods are weakest.** Identical cheating
   buys +0.2010 AUC on EB-NeRD and +0.0679 on MIND, because 86.9% of EB-NeRD's val
   candidates were never clicked in training so nothing legitimate predicts them. The
   corollary is the uncomfortable one: the settings where leakage is most tempting are
   the settings where its absence is hardest to spot, since there is no strong honest
   baseline whose absence would look suspicious.

3. **A test that pins a real property can still let a wrong conclusion through.** Twice in
   this phase. The coverage bootstrap had a test asserting its exact downward bias and
   treating it as correct (D27). And a leakage test that cannot fail is worse than no test,
   because it provides false assurance — which is why all five deliberate leaks were
   reintroduced and confirmed caught, rather than the suite being trusted because it was
   green.

**Also learned, mechanically:** the mutate→test→restore loop can be poisoned by a stale
`__pycache__` — see the error log. The failure direction is benign (a stale cache makes a
mutation look *survived*, which reads as a test gap and gets investigated) but it cost
fifteen minutes of hunting a bug that was not in the code.

---

## Phase 5 — Q5, scale-up and Codabench submission

### Concept: the rank vector (the inverse-permutation trap)
**Taught 2026-08-25**, in chat per R1's amended form: plain-language framing (a dog-show
judge writing *collar numbers on dogs standing in line*, versus writing *a list of winners
in order*), then the technical statement, then the check. Full entry in `GLOSSARY.md`.

**Comprehension check.** Candidates `[A, B, C]`, scores A = 0.2, B = 0.9, C = 0.5. What
line do we write, and what would the buggy `argsort + 1` spelling have written?

**Chaitanya's answer: `3,1,2` — correct**, on the part that matters. B wins so its rank is
1, C is 2, A is 3, written into each candidate's own position. He did not give the second
half; the buggy spelling would have produced `[2,3,1]`, because `argsort(-scores)` is
`[1,2,0]` ("candidate 1 came first, candidate 2 came second, candidate 0 came third") and
adding one converts *identities* into what merely looks like ranks.

**Why this one earned a check under reduced-depth pacing.** Both answers are permutations
of 1..3. Both have the right length. Both pass every structural test that can be written
against a submission file. The only symptom of choosing wrong is a leaderboard score near
random, on a channel that returns a single number and no diagnostics — so it is the one
concept in Phase 5 where being confidently wrong is invisible rather than loud.

**Generalisation worth carrying to the design note**, and the third instance of the same
shape in this project: *a value can be well-formed, in-range, and of the correct type
while meaning something entirely different from what the consumer expects.* The earlier
two were the Float32/Float64 concat mismatch (Phase 1) and the -inf-versus-0.0 masking
convention for cosine (Phase 3, where 0 is mid-range rather than minimal). In all three
the type system, the tests-as-written, and casual inspection all pass.

### Diagnostic read rather than assumed: the rank-1 position histogram
Not a taught concept, but a worked reasoning step worth recording. The MIND submission's
rank-1 winner sits at candidate position 0 for **10.5%** of impressions, against **9.2%**
for position 1 — which looks like position bias leaking into a position-blind scorer.

Resolved by computing the actual random baseline instead of eyeballing it: for a uniform
ranking, P(position 0 wins) is **E[1/n] = 9.32%**, not 1/mean(n). The 1.18-point excess is
then fully accounted for by the **29,108 cold-start impressions (1.2%)** whose candidates
all score a flat zero, where stable ordering hands rank 1 to position 0 every time:
1.2% x (1 - 0.093) = 1.1 points. Position 1 sitting exactly on 9.2% confirms it.

The habit being practised: **an anomaly is not evidence until its null model has been
computed.** Phase 3's "a number moving in the direction you wanted never tells you why"
is the same lesson from the opposite side.

---

# Assignment 2

## Phase A1 — data scale-up (2026-09-15)

### Taught in chat, while deciding D33
- **CI width scales with 1/√n.** Used to turn A1's measured ±0.005 on 17,749 EB-NeRD
  impressions into estimates for each candidate sample size (±0.0016 / ±0.001 / ±0.0006).
  Also that a *paired* bootstrap is narrower than an unpaired one, because both systems
  are scored on the same impressions. Stated only; taught fully before Phase A4.
- **User-level versus impression-level sampling**, and why only the first keeps a user's
  history consistent with their impressions.
- **Seeded random sample versus `user_id % 100 < p`.** Reproducibility across library
  versions, and nesting.

**Chaitanya chose** 5% and modulo selection, both the recommended options.

The R5 recall quiz on A0 was skipped, because A0 was migration mechanics with no new
concept.

**Comprehension check (asked after committing D33).**
1. *How could `user_id % 100 < 5` fail?* Chaitanya: "if the last two digits are linked
   to some user info, like age, it will not be random." **Correct.** Added: a composite
   ID such as `sequence × 100 + region code` is the realistic mechanism. Also that χ²
   only proves the residue groups are equal in *size*, and the in/out behaviour table is
   what proves they are alike in *kind*. Two checks, two different claims.
2. *Why does 3× data narrow the CI by only ~1.7×?* Chaitanya: "not a linear relation;
   more data gives diminishing returns." **Right direction, imprecise.** Re-taught the
   exact law: width ∝ 1/√n, so 3× → √3 ≈ 1.73, halving needs 4×, and a tenth needs 100×.
   Worth re-checking before Phase A4, where the paired bootstrap depends on it.

### Recall quiz on Phase A1 (answered 2026-09-15)
1. *Why user-level rather than impression-level sampling?* Chaitanya: "it would favour
   users with larger history, so it won't be completely random." **Partly right** — that
   bias is real (impression-level sampling over-represents heavy users). Added the reason
   we actually ruled it out: a user's history row describes all their clicks, so keeping
   some impressions and dropping others makes history and impressions describe different
   things. Inconsistent, not merely skewed.
2. *Why isn't val/test 50/50?* "Because we split the data 70/30." **Correct** (D8, by row
   count over the validation week).
3. *What was checked before reusing the embeddings?* "idk." **Re-taught:** the two article
   tables were compared and found frame-equal first. Without that, a store article could
   have had no vector, or a vector built from different text under the same id — wrong
   numbers with no error. This is why `assemble_embeddings.py` refuses to write unless the
   ids match exactly. **Re-check this one before Phase A4**; it is the same
   "well-formed but meaning something else" shape as the rank-vector trap.

### Follow-up question from Chaitanya (2026-09-18)
*"Why are the large and test article tables the same, if large is much bigger?"*
Taught with the newsagent analogy: one **catalogue** binder, and separate piles of **till
receipts** per week. "Large" versus "test" means different weeks of receipts, i.e.
behaviour logs. The catalogue is shared, so every week's candidates have content. Also
corrected the premise: the testset is not small (13.5M impressions for one week, about
the same as each of large's weeks). It only lacks the labels.

**The question surfaced a real landmine** (now PROGRESS Landmine 6): the shared catalogue
runs a month past the test week, so any catalogue-wide statistic leaks the future.
Recorded as Chaitanya's catch.
