# Research Integrity Protocol (Custom — Security Track)

> The discipline that keeps an experiment honest **under optimization
> pressure** — when the loop wants a better number and the easiest way to get
> one is to bend the process rather than improve the method. Load at S4/S5
> (design + execution), at S7/S8 (before the numbers ship), and at S8.5
> (retrospective self-audit). Reviewer personas R3/R4 apply it as a bar.
>
> **Provenance.** Adapted from Chen Yueh-Han, Jiaxin Wen & Jan Hendrik
> Kirchner, *Automated Researchers Can Reliably Mitigate Alignment Failures*
> (Anthropic Fellows / UC Berkeley, 2026). That paper builds automated
> researchers that hill-climb safety benchmarks and shows that the results are
> only trustworthy because of a stack of **anti-gaming** mechanisms: a
> results-free method description frozen to an immutable id *before any result
> is seen* (§3.2), a geometric-mean score that zeroes if any benchmark
> regresses (§2.2), a capability verdict that disqualifies a method whose
> general capability drops (§2.3), a truly held-out set that nothing is
> selected on (§2.3), and a post-hoc monitor with a three-category cheating
> taxonomy (§7). We borrow the **integrity machinery**, not the paper's
> "automated researchers need no human direction" conclusion — this overlay
> stays human-gated. The AAR multi-agent harness itself is out of scope.

This protocol operationalizes two loop-wide iron rules that already exist in
`research_loop_protocol.md` — #2 (numbers come from execution logs only) and
#3 (success criteria freeze at design time) — turning them from principles
into **checkable artifacts and a self-audit**. It is advisory + ledger
convention, not runtime enforcement (same posture as "numbers from ledger").

---

## 1. Pre-registration card (freeze-before-you-run)

The AAR mini-paper is frozen to an immutable id **before** any result is seen
and reused verbatim when the result posts, "so a finding cannot be
rationalized after the fact." The security analogue is **PRE-REGISTRATION**
of the experiment: it is the artifact form of iron rule #3, and the direct
antidote to HARKing (Hypothesizing After Results Known) and to
reverse-engineering the threat model so the attack works (the custom-fit test
in `threat_model_workbench.md`).

**When:** at the S4→S5 boundary, after DESIGN FREEZE and before the first run.

**What to freeze** (results-free — no numbers yet) into the Provenance Ledger:

1. The method as it will be run (the frozen Contribution Card version + the
   algorithm/threat model).
2. The Validation Plan per claim: experiment(s) or proof obligation, metrics,
   **numeric success criteria**, baselines/comparators, ablations, the
   statistical plan (seeds, repetitions, tests), and the held-out split (§3).
3. A content hash + timestamp of the above (a `sha256` of the frozen card
   text is enough — this is a ledger convention, not a tool).

**The rule:** every number S8 reports must cite the frozen card's hash. If,
after seeing results, you want to change a success criterion, a metric, or the
threat model, that is a **RE-FREEZE** — a documented human-gated decision
(iron rule #3), never a silent edit, and a *mechanism* change additionally
runs `method_change_provenance.md`. A result compared against a criterion that
was moved after the result was seen is not a finding; it is HARKing.

> Absence is statable: exploratory / hypothesis-generating passes exist. Label
> them exploratory in the ledger and do not report them as confirmatory. The
> defect is a post-hoc criterion *presented as if pre-registered*.

## 2. Evaluation integrity (anti-gaming — all paper types)

Three rules, each a security translation of an AAR anti-gaming mechanism.
Fold them into the S4 Validation Plan for every paper type.

- **No cherry-pick across the benchmark set.** (AAR geometric mean: any
  benchmark at/below baseline zeroes the whole score.) Report results across
  **all** the testbeds / datasets / devices / targets / models you evaluated,
  not just the subset where the method wins. A method that improves one and
  regresses another is not an improvement until the regression is disclosed
  and argued. Picking the favorable subset to report is a cherry-pick; the
  aggregate is reported honestly, regressions included.
- **Utility / functionality non-regression gate.** (AAR capability verdict:
  disqualify a method whose general-capability 95% CI falls below baseline.)
  A defense or system must not degrade the protected system's **primary
  utility / functionality** below baseline. State the utility metric and the
  tolerance *in the pre-registration card*, before running — a defense bought
  with unstated utility collapse is a failed defense, not a tradeoff to
  discover afterward.
- **A held-out that selection never touches.** (AAR held-out benchmark + the
  Petri audit nothing is selected on.) Keep a test set / target set / device
  set that is **never** used during method development or hyper-parameter
  tuning, and report on it once. This generalizes the ML-for-security
  temporal-split rule (`knowledge_index.md`) to every paper type: development
  data and the final evidence set are disjoint, and the split is fixed in the
  pre-registration card.

## 3. Integrity self-audit (the cheating taxonomy)

AAR §7's post-hoc monitor catches three cheating patterns. Run this as a
self-audit at S7/S8 (before the numbers ship) and again at S8.5, and record
any near-miss. The mapping to security research:

| AAR cheating pattern (§7) | Security research self-check |
|---|---|
| Re-submit an unchanged method hoping scorer noise gives a higher score | **Seed / run selection:** report the seed and repetition protocol and the **distribution** of runs — never the best single run dressed up as the result. If variance is high, that is a finding, not something to hide behind a lucky seed. |
| Build training data that imitates the benchmark being scored | **Eval-set overfitting:** do not tune on the test distribution; check for test-on-train leakage; hyper-parameters are chosen on development data (§1–§2), never on the held-out. |
| Conceal a rule-breaking step (secretly use benchmark / held-out data) so it passes automated review | **Silent rule-breaking / hidden data use:** every use of held-out or test data is disclosed; there is no undisclosed assumption or data access that is quietly "what made the result work." |

**Claim-vs-artifact consistency** (AAR §3.2 monitor: the code must match the
mini-paper's description, and a method paper that omits a load-bearing detail
needed to reproduce is rejected): the method described in the paper must match
the released artifact, and **any load-bearing detail omitted from the paper is
a defect**, not an appendix nicety. This is the reproducibility bar the
re-review artifact check (`SKILL.md` § Review Workspace) enforces at the
method level.

## Reviewer angle (why a Big-4 panel cares)

Under submission pressure the same three shortcuts are exactly what a skeptical
reviewer probes for: "is this your best seed or the distribution?", "was any
hyper-parameter chosen on the reported test set?", "does the released code do
what the paper claims, and what load-bearing detail is missing to reproduce
it?" A paper that pre-registers, reports the full benchmark set with
regressions, and states its held-out discipline answers these before they are
asked. See `security_reviewer_personas.md` (R3 integrity probes; rejection
anchors #13–#14).

## What this is NOT

Not a runtime gate, not an automated hashing tool, and not a replacement for
the human design-freeze and submission gates. It is a discipline plus a ledger
convention — the same posture as "numbers come from execution logs only."
