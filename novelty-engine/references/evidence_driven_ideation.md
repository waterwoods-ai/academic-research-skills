# Evidence-Driven Ideation

Use at topic scoping, candidate generation and screening. Treat this protocol
as a workflow recommendation, not a validated predictor of publication.

## 1. Build evidence before choosing a mechanism

Record a compact matrix of the core literature: question, threat model,
assumptions, mechanism, evidence actually reported, untested boundary and cost.
Attach section/equation/table locators and reading scope. Distinguish an
author-stated limitation from an experimentally confirmed failure. A search
that finds nothing is a bounded retrieval result, not proof of an open problem.

Choose every generation route whose inputs exist; record why others were not
used. Never invent inputs to fill a route or a candidate quota.

| Route | Input | Next action |
|---|---|---|
| A: assumption-breaking | Source-backed condition and meaningful breaking point | Compare mechanisms from adjacent and distant fields against that condition |
| B: limitation-driven | Confirmed baseline limitation and its source | Diagnose the cause and design a change that addresses it |
| C: observation-driven | Located replication anomaly, conflicting result, deployment obstacle, new trust boundary or measurement | Separate observation from explanation; design a discriminating probe and, when justified, a method |

Zero supported assumptions is valid. Label assumptions EXPLICIT,
SHARED-DEPENDENCY or HYPOTHESIS; only the first two can ground route A.
HYPOTHESIS items need a probe. Keep the filename `dogma_scan.md` for continuity.

## 2. Use observations without manufacturing conclusions

Accept an existing observation ledger or create
`03_hybrid_methods/observation_ledger.md` from the supplied evidence:

| Field | Required content |
|---|---|
| ID and provenance | Source locator or raw artifact path; setup/version; reading or execution scope |
| Observation | What was seen or reported, separate from interpretation |
| Status | reported / reproduced / unresolved / refuted, with evidence for the label |
| Security relevance | Asset, property, adversary, trust boundary and practical consequence |
| Candidate explanation | Proposed cause, supporting evidence and unresolved assumptions |
| Alternatives | At least one plausible competing explanation, such as implementation error, leakage, tuning, sampling or measurement bias |
| Discriminating probe | Manipulation/control, predicted outcomes under each explanation, acceptance and drop conditions, required resources |

For a newly documented architecture or deployment constraint, cite the
specification or observation supporting it; keep any predicted exploitability
unverified. Do not equate a toy reproduction with deployment evidence.

No artifact available: emit a data request or probe plan. Do not mark the
observation reproduced, launch an unapproved experiment, or invent results.
A causal explanation may remain a hypothesis while a candidate is shortlisted,
but its decisive test must distinguish it from the strongest alternative.
Refuted observations cannot support a candidate.

If the lead changes the selected problem or threat model, return it to S2 for
topic verification. If its contribution is measurement, analysis or SoK with
no new method, hand it to the security research loop's matching contribution
route; do not force it through mathematical method generation or invent a
theorem. A new dataset or setting needs a substantive knowledge delta.

## 3. Generate distinct mechanisms

Keep the research question and threat model fixed for a method comparison.
Use the following as prompts, not a requirement to add modules:

| Change | Question to answer |
|---|---|
| Information source | Which missing signal is needed, and why can it be trusted? |
| Constraint or representation | Which physical, protocol or program property constrains the failure? |
| Decision timing | Can prevention, runtime checking or selective expensive analysis address the bottleneck? |
| Cooperation | Which complementary failures justify combining methods, and what governs their switching? |
| Guarantee boundary | Under what explicit conditions is detection, rejection or a guarantee possible? |

For each mechanism state why it addresses the cause, what is borrowed, the
adaptation, extra assumptions, overhead and expected failures. Prefer the
smallest coherent mechanism. A distant analogy, extra module or larger model
does not itself establish a contribution. Deduplicate equivalent mechanisms
even when their names or generation routes differ.

## 4. Carry evidence into selection

Add to each existing candidate card: source IDs, evidence status, root-cause
hypothesis, alternative explanation, new assumptions/costs, borrowed components,
and the proposed delta from the nearest work. State 1-3 falsifiable claims and
their security consequences. A performance improvement needs an operational
meaning, such as coverage, alert burden, attack cost or deployment feasibility.

Search both the mechanism and the knowledge claim under older and adjacent
terminology. Record UNCERTAIN when retrieval is insufficient. Search novelty,
security framing and feasibility remain separate checks; uncertainty is not
a passed novelty gate. A supported INCREMENTAL delta may proceed with explicit
positioning. Drop a claim shown to be KNOWN, not every candidate using known
components.

Shortlist at most three eligible, substantively distinct candidates. Prefer
complementary explanations when equally supported; reserve no seats by route.
Use one frozen development screening plan, comparable implementation/tuning
budgets and per-candidate decisive tests before commitment. Log failed and
inconclusive runs, diagnose failure causes and keep the held-out data untouched.
Do not adjust pass criteria after observing results.

Append an evidence summary to `candidates.md` after generation and screening:
all proposed IDs, merges/drops with reasons, search status, eligible IDs,
tested IDs and ledger links, MET/UNMET/INCONCLUSIVE results, and the author's
selected ID or pending decision. Unrun tests are NOT RUN. These are pipeline
counts with their denominators, not scores or publication probabilities.
Never present a simulator's review or an LLM novelty rating as acceptance.

## 5. Basis and limits

- [Driller, NDSS 2016](https://www.ndss-symposium.org/wp-content/uploads/2017/09/driller-augmenting-fuzzing-through-selective-symbolic-execution.pdf): a published example of complementary fuzzing and symbolic execution; adjacent techniques can support a contribution.
- [TESSERACT, USENIX Security 2019](https://www.usenix.org/conference/usenixsecurity19/presentation/pendlebury): a published example of investigating deployment-relevant evaluation bias and designing an evaluation framework.
- [The Ideation-Execution Gap](https://arxiv.org/abs/2506.20803): a 43-researcher NLP execution study found that proposal-stage ratings did not preserve the apparent LLM advantage. Its scope does not establish cybersecurity success rates.
- [ScientistTwo, 2026 preprint](https://arxiv.org/abs/2609.19644): limitation-driven generation and subset-to-full execution are useful workflow precedents; reported results do not validate this project's implementation.

The route taxonomy and mechanism prompts above are project design choices.
Validate their usefulness on actual projects with source and execution evidence.
