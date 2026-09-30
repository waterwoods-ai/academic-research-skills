# Security Research Loop Protocol (Custom — Security Track)

> Extends the overlay from literature-and-review into the FULL research
> loop: topic → gap → research question → method proposal (or deep
> evaluation of the user's method) → novelty & contribution sharpening →
> experiment design → execution → bounded improvement iterations →
> adversarial stress test → paper. Runs on both runtimes: Claude Code
> (where the suite's `novelty-engine` skill supplies stages S0–S4 machinery) and
> Codex (where this protocol + the suite's experiment-agent workflow carry
> the loop inline). Security-conference calibration applies at every stage.

## IRON RULES (loop-wide)

1. **Novelty claims are always search-bounded** — "no prior work within
   our search (strategy: …)" — never absolute. Verified against Big-4 +
   tier-2 literature via real retrieval, never model memory.
2. **Numbers come from execution logs only.** No experimental result may
   be reported that does not trace to an actual run's output. Negative
   results are recorded and reportable, never deleted.
3. **Success criteria freeze at design time (S4).** Improvement
   iterations change the METHOD, never the definition of success. This is
   the same frozen-rubric principle that governs review.
4. **Human gates** at S0 (go/no-go), S4 (design freeze), every S6
   iteration checkpoint, and S8 (submission). The agent proposes; the
   researcher decides.
5. **Every method must be formalized** — mathematics or explicit
   algorithm (pseudocode with complexity), plus a threat model. A method
   that cannot be formalized is not yet a method. **For algorithm-heavy work,
   check every claim against the underlying mathematical theory** —
   correctness, complexity, convergence, and the assumptions the theory
   requires are proven or cited, not asserted. **Any hypothesis must state its
   fundamentals** — WHY it should hold, from first principles or known results
   — then be **decomposed into its constituent sub-claims with each part
   verified** (a proof, a derivation, or a targeted experiment). A hypothesis
   is never assumed whole; an unstated or unverified assumption is a hole a
   reviewer will find.
6. **Constructive stance + dig, don't settle (the researcher's default).**
   The aim is novelty and *improving* existing methods — prior work is the
   baseline to beat and build on, cited respectfully, never a target to
   discredit or an exercise in exposing others' faults. A negative / unmet
   experimental result is a lead to INVESTIGATE: find the root cause and
   improve, or rigorously establish whether the approach is genuinely
   unworkable — NEVER settle for "let's just honestly report the negative."
   Digging deeper never licenses fabrication, goalpost-moving, or
   cherry-picking (`research_integrity_protocol.md`): change the disposition,
   not the integrity rules.

## Stage map and runtime routing

| Stage | Output | Claude Code | Codex |
|---|---|---|---|
| S0 Topic viability | go / no-go verdict | novelty-engine Phase 0a (topic_verifier) | deep-research quick + this protocol §S0 |
| S1 Gap registry | evidenced gap list | `/ars-lit-review` + perspective protocol + gap_analyzer | `ars-lit-review` + perspective protocol, gaps per §S1 |
| S2 RQ generation | ranked candidate RQs | gap_analyzer + dogma_extractor | this protocol §S2 |
| S3 Method / evaluation | candidate cards → screening → Contribution Card | cross_domain_synthesizer + limitation_resolver + novelty_verifier + math_formalizer | the same `novelty-engine` roles, run one at a time + this protocol §S3 |
| S4 Validation design | frozen validation plan (type-aware) | experiment_falsifier (defense/AI); proof obligation for crypto | experiment-agent WORKFLOW planning + §S4 table |
| S5 Execution | provenance ledger | experiment_coder + session runs code | Codex writes & runs code + §S5 ledger |
| S6 Improvement loop | method changelog M-v1→M-vN | this protocol §S6 (both runtimes) | same |
| S6a Ablation & simplification | source-of-gain breakdown + final method | this protocol §S6a (always runs once criteria are MET) | same |
| S7 Stress test | hardened method + results | `/ars-reviewer` w/ security contract | `ars-reviewer` w/ security contract |
| S8 Paper → submission | venue-ready paper | `/ars-full` + provenance intake + Phase-0 | `ars-full` same |

## S0 — Topic viability (go / no-go)

Before any investment: is the topic saturated, misframed, or viable?
Retrieve the 5–10 most-cited and most-recent Big-4/tier-2 papers on the
topic; verdict with evidence: SATURATED (recent top-venue work occupies
the space — name the papers), MISFRAMED (the interesting question is
adjacent — restate it), or VIABLE (name the open territory). HUMAN GATE:
the researcher decides to proceed, pivot, or stop.

Search front-ends for S0–S3 (Elicit, Litmaps, blind second opinions) and the
rules that bind their output: `topic_scouting_overlay.md`. Their verdicts are
scan-level leads; this stage's verdict still needs the named papers.

## S1 — Gap registry

Run the literature review with the perspective-retrieval protocol (six
security lenses + moderator round). Each candidate gap is an ABSENCE
claim and must carry: (a) the search that failed to fill it (queries +
indexes + date), (b) the nearest-miss papers and why each falls short,
(c) a security relevance statement (what attack/defense/measurement
question the gap blocks). Gaps without (a) are hunches, not gaps.

Two queries are mandatory before a gap is recorded (both learned from real
misses — `topic_scouting_overlay.md`): an **ancestor query** with no year
filter and the current buzzwords removed, and an **adjacent-method-family
query** regardless of application domain. A gap also needs at least two
independent signals, not one tool's silence.

## S2 — Research question generation (课题延伸)

From the gap registry, generate candidate RQs. Each RQ card states:
threat-model sketch (adversary, assets, trust boundary), contribution
type (attack / defense / measurement / analysis-SoK — note CCS bans SoK),
target venue fit (which Big-4/tier-2 and why, per venue profiles),
feasibility (data/testbed/device access YOU actually have), and the
dogma it challenges, if any (shared assumption in prior work — e.g.,
"defenders assume the attacker cannot influence training data"; breaking
a named dogma is the strongest novelty source). Rank by
impact × feasibility × freshness. HUMAN selects.

**Distinctness rule (before ranking):** discard any candidate RQ that
collapses to the SAME threat-model delta as a higher-ranked one — present
the human genuinely distinct framings, not near-duplicates. This is diverse
ideation + prune-the-redundant; it is NOT auto-pruning by a quality score
(writing has no automatic scalar — selection stays human-gated).

**Abandoned-Approaches Ledger:** RQs the human rejects here are appended to
`abandoned.md` (per project) with a one-line reason, so a long engagement
never re-proposes a dead end. It also collects, later, methods the S6/S8
provenance guard rules RENAME or ADOPT+CITE, and reviewer objections already
resolved. This is the "what was tried-and-killed" record; the S6 changelog
records "what changed". Both feed the S8.5 retrospective.

**Topic verification gate (before S3).** The selected RQ answers the twelve
questions in `topic_verification_gate.md` — answers frozen first, then an
independent second opinion from a different model family, disagreements
resolved against evidence. Verdict go / revise / stop: `stop` returns to a
different framing here in S2; `revise` fixes the design first; only `go`
proceeds to S3. The researcher confirms.

## S3 — Method proposal OR deep evaluation (novelty & contribution focus)

Two entry modes, same output artifact:

- **Propose mode**: design a new method for the chosen RQ. Generate
  candidates with the `novelty-engine` skill in two modes, and run both when
  their inputs exist:
  - *Assumption-breaking* (Phases 1 → 2 → 3A): name an assumption prior work
    shares, pre-check it, import a mechanism from a distant field.
    Cross-domain transplantation is encouraged (control theory → CPS anomaly
    detection, etc.) but the transplant must be justified against the threat
    model.
  - *Limitation-driven* (Phase 3B): start from a **limitation ledger** of the
    strongest baseline — extract its limitations and check the list covers
    what a reviewer would name (ScientistTwo, arXiv:2609.19644 §3.1) — and
    propose mechanisms that remove their causes. One mechanism may resolve
    several limitations; one patch per limitation is a checklist, not a
    method. `novelty-filter` can build the ledger (Claude Code); any tool can
    supply one directly.

  **Common candidate checks (Phase 3.5), both modes.** Every candidate gets a
  candidate card: the mechanism, its own falsifiable claims, the security
  consequence (what the community would learn), the nearest prior work, and
  its cheapest decisive test with a pass criterion stated in advance. The
  mechanism itself is novelty-checked again after generation — an unexplored
  assumption does not make the method built on it new. A candidate is
  *eligible* only if it passes that novelty re-check, the security framing
  check and a feasibility check. **Shortlist at most three eligible
  candidates.** When both modes have eligible candidates, one slot is
  reserved for each; an ineligible candidate is never carried to represent
  its mode, and no single novelty score decides the list. The rest stay as
  the exploration pool for S6.

  **Screening before commitment.** The shortlisted candidates share one
  **screening plan**, frozen before the first candidate runs: the development
  data, the strongest baseline to reproduce, the comparison criterion, and
  the same implementation and tuning budget for every candidate. Each
  candidate runs its cheapest decisive test on development data only, under
  the S5a rules (reproduce the baseline first; GOOD / ENGINEER / BAD; a BAD
  candidate gets a root-cause note). Select ONE on development evidence by the
  frozen criterion; the researcher confirms; the runners-up and their results
  are logged and reportable. If none is GOOD, do not lower the bar: return to
  generation with the failure causes. The Contribution Card is written for
  the selected method, and the development data used here can never become
  the held-out (`research_integrity_protocol.md` §2).
- **Evaluate mode**: the user brings their own method; the loop deepens
  it rather than replacing it.

Both entry modes MUST end in the **Contribution Card** — the artifact the
whole loop optimizes. In propose mode it is written for the ONE method that
screening selected:

```
CONTRIBUTION CARD — <method name> (M-v1)
1. Claims: 3–5 falsifiable claims (each maps to a validation in S4 — an
   experiment, or a proof obligation for theory claims)
2. Novelty status per claim: NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN
   — verdict from real retrieval against Big-4 + tier-2 literature,
   with the nearest prior work cited for every claim
3. Positioning table: this method vs the 3–5 closest published methods,
   dimension by dimension (threat model, assumptions, overhead, eval)
4. Delta statement: one paragraph — what a Big-4 reviewer would call
   the contribution, in the community's own terms
5. Formalization: math or algorithm (iron rule 5) + threat model
6. Honest weaknesses: what the skeptic persona (R4) would attack first
7. Security framing check: the framing chain filled + SECURITY FRAMING
   RISK verdict, and each claim's novelty type(s) tagged
   (technical/security/empirical/system/attack/defense) — per
   `security_framing_protocol.md`. A claim whose only novelty is
   technical/empirical is not yet a security contribution.
8. Taxonomy/definition provenance: any classification, taxonomy, named
   category, or definition introduced (D1/D2/D3…) is checked against
   established ones — adopt+cite, or extend with lineage, never a
   self-invented scheme with no provenance (`security_framing_protocol.md`).
```

Any claim graded KNOWN is dropped or reworked NOW — before a single
experiment is designed. INCREMENTAL claims survive only with an explicit
positioning argument.

> **Caution (AAR, 2026):** a higher novelty score, more method complexity, or
> a larger dataset does not by itself make a stronger contribution — in the
> AAR study, method complexity tracked proposal order rather than benefit,
> larger training sets did not improve scores, and greater novelty did not
> guarantee generalization. Let the contribution be judged by the delta a
> reviewer can name (item 4), not by how novel or elaborate it looks.

## S4 — Validation design (refutation-shaped, by paper type)

The validation goal is to SHOW THE CLAIM IS RIGHT — but at a Big-4 venue a
claim is only believed once it has survived the specific attempt at
refutation its subfield demands. Confirmatory demonstrations ("we ran our
method and it worked") fail everywhere; surviving the community's standard
attack on the claim wins everywhere. The form of that attack differs by
paper type — verified against the 2020–2025 Big-4 best-paper corpus
(`References/security top 4 best paper.xlsx`), where attack papers are the
plurality (~40%), followed by crypto/formal-proof (~15%),
measurement/empirical (~13%), defense/AI-security (~17%), and
fuzzing/tool + usability the remainder. Pick the row that fits the claim:

| Paper / claim type | What "validation" means | The refutation you must survive |
|---|---|---|
| **Attack / offensive** | The paper IS a refutation of someone's security claim. Validation = the attack works END-TO-END on a REAL target (not a lab toy), with impact quantified and responsible disclosure. | "This only works in your idealized setup / preconditions already imply game-over." → demonstrate on real deployed systems, real CVEs, realistic attacker position. |
| **Defense / AI-security** | The method resists attack. | ADAPTIVE adversary aware of the defense; strongest published attacks as correctly-tuned baselines; no gradient masking / security-by-obscurity (Carlini checklist). |
| **Measurement / empirical** | The finding reflects reality, not method. | "Your result is a measurement artifact." → rule out alternative explanations, multiple vantage points, ground-truth validation, robustness to methodology choices. |
| **Fuzzing / bug-finding / tool** | The tool finds real, deeper defects. | "You only beat baselines on toys." → real-world targets, comparison vs strongest existing tools, real bugs triaged (ideally reported/fixed). |
| **CPS** | The attack/defense holds on real cyber-physical dynamics. | Real testbed or hardware-in-the-loop, or an explicit simulation-fidelity argument; PHYSICAL consequence measured, not packet-level success. |
| **IoT** | The result generalizes past one device. | Device/vendor diversity matched to the breadth of the claim; root cause is a vulnerability CLASS, not one vendor's bug. |
| **ML-for-security detection** | The detector works at deployment scale. | Realistic base rates, temporally-split datasets (no future leakage), false-positive cost at scale. |
| **Crypto / formal / theory** | The construction is correct. | **This is the exception: validation is a PROOF, often machine-checked — not an experiment.** "Refutation" = soundness of the proof + cryptanalytic effort against the construction; empirical work here is performance benchmarking, not correctness validation. If your contribution is a theorem, S4/S5 are a proof obligation and (optionally) a performance study, not a falsification run. |

Whichever row applies, pre-register the frozen **Validation Plan**: per
claim — the experiment(s) OR proof obligation, metrics, numeric success
criteria, baselines/comparators, ablations, statistical plan (seeds,
repetitions, tests), and the artifact/open-science plan. The unifying
discipline is not "try to break your own method" literally — for an attack
or measurement paper that makes no sense — it is: **name, in advance, the
refutation a Big-4 reviewer of THIS paper type will attempt, and design the
validation to survive exactly that.** DESIGN FREEZE (human gate): after
approval the success criteria are immutable for the life of the loop.

### Per-type evaluation checklists (fold into the plan for the matching row)

The refutation table names the *bar*; these are the concrete experiments a
hostile reviewer will ask for. Include the ones that apply, or state why not.

- **Attack paper:** attack effectiveness · strongest baselines · multiple
  targets/models/systems · varied attacker knowledge · varied capability ·
  budget/cost · **stealthiness / detectability** · transferability ·
  robustness · real-world feasibility · vs existing defenses · **vs adaptive
  defenses** · ablation · failure cases.
- **Defense paper:** everything above, PLUS **adaptive (defense-aware)
  attacker** · bypass analysis · security–utility tradeoff · false-positive
  rate at deployment scale · performance overhead · deployment cost.

Closing question to force before freeze: **"What experiment would a hostile
reviewer request?"** — then add it, or record why it is out of scope.

### Evaluation integrity (all types — fold into every Validation Plan)

Three anti-gaming rules (`research_integrity_protocol.md` §2, from the AAR
paper's geometric-mean / capability-verdict / held-out mechanisms):

- **No cherry-pick across the benchmark set** — report all testbeds /
  datasets / devices / targets, not the winning subset; a regression on any
  is disclosed, not hidden.
- **Utility / functionality non-regression gate** — a defense/system must not
  push the protected system's primary utility below baseline; state the
  metric + tolerance in the pre-registration card *before* running.
- **A held-out that selection never touches** — development data and the
  final evidence set are disjoint; the split is fixed at pre-registration
  (generalizes the ML-detection temporal split to every type).

### Pre-registration gate (S4→S5 boundary — the artifact form of iron rule #3)

After DESIGN FREEZE and before the first run, freeze a results-free
**pre-registration card** into the ledger — the method, the Validation Plan,
the numeric success criteria, the statistical plan (seeds/reps/tests), and the
held-out split — with a content hash + timestamp
(`research_integrity_protocol.md` §1). Every number S8 reports must cite that
hash. Moving a criterion/metric/threat-model *after* seeing results is HARKing:
it is a documented, human-gated RE-FREEZE (never a silent edit), and a
mechanism change additionally runs `method_change_provenance.md`.

## S5 — Execution

The coding agent implements and RUNS the experiments in the user's
environment (this is the researcher's own execution, assisted — the
paper's methods section must stay honest about tooling). Every run
appends to the **Provenance Ledger** (ARS experiment-provenance
compatible): experiment id → claim id, planned vs executed (deviations
named), raw output location, result vs pre-registered criterion
(MET / UNMET / INCONCLUSIVE), negative results and surprises. The ledger
is the ONLY source S8 may cite numbers from.

**S5a — Reproduce the strongest baseline first, then screen cheaply**
(adapted from ScientistTwo §3.2, arXiv:2609.19644). S3 screening uses these
same rules on the development data to choose among the shortlisted
candidates; here they apply to the selected method and any later variants:

1. **Reproduce the strongest baseline in YOUR environment** — same testbed /
   devices / firmware / dataset split / metric code — and log it in the ledger
   before any comparison. Every gain is measured against this reproduced
   number, never against a number copied from the baseline's paper (a
   different setup makes that comparison meaningless). If the baseline does not
   reproduce, that discrepancy is itself a ledger entry to explain.
2. **Screen on a development subset** (never the held-out split, per
   `research_integrity_protocol.md` §2) before committing to full runs. Triage
   each candidate: **GOOD** (consistently beats the reproduced baseline → scale
   to the full set) / **ENGINEER** (promising, needs tuning → bounded budget) /
   **BAD** (clearly worse after that budget). A BAD candidate needs a
   root-cause note in `abandoned.md` before it is dropped (iron rule 6) — the
   *candidate* is dropped, the *problem* is kept.
3. Only GOOD candidates get full-set runs; those full runs are what S8 cites.
4. **If more than one candidate is GOOD, select ONE before the held-out run.**
   Choose by the pre-registered metric on development data; on a tie prefer
   the simpler method or the one with weaker assumptions. Record the choice,
   the reason, and the runners-up in the ledger (the runners-up are reportable
   as alternatives, not hidden). The held-out split is then run once, for the
   selected method only — picking the winner by its held-out score is
   selection on the held-out (`research_integrity_protocol.md` §2). The
   researcher confirms the choice.

## S6 — Bounded improvement loop (the anti-dead-loop core)

Enter only if ≥1 pre-registered criterion is UNMET. Per iteration
(M-v1 → M-v2 → …):

1. **Diagnose the root cause** — not just which claim/criterion is UNMET, but
   WHY it failed: a bug, a mis-tuned baseline, a wrong assumption, an
   insufficient signal, a mechanism gap? Read the actual logs/artifacts. A
   negative result is a lead to investigate, never a stopping point. Read the
   failed traces as closely as the successful ones (ledger + `abandoned.md`):
   in ScientistTwo most of the best final ideas were evolved from earlier
   failures (§3.3).
2. **One targeted change** to the method, with the mechanism hypothesis
   ("criterion X fails because Y; change Z addresses Y").
2a. **Provenance guard (IRON RULE — the anti-偷梁换柱 rule).** If the change
   introduces a new *mechanism* (not mere tuning), it must pass
   `method_change_provenance.md` BEFORE the experiments re-run: (i) scenario
   fidelity — does the substitute still solve the ORIGINAL problem at the
   same point in the pipeline, or did it silently redefine the problem into
   an easier one? (ii) prior-art identity — strip the new name and search;
   a rescue method that matches published prior art once renamed is a RENAME
   (e.g., a "new" OTA signing scheme = in-toto / SLSA / TUF / Uptane), not a
   contribution; (iii) honest outcome — ADOPT+CITE (novelty claim dropped)
   or GENUINE-DELTA re-verified NOVEL-WITHIN-SEARCH. A method born under
   experiment-failure pressure gets the SAME topic-selection + novelty
   verification as the S3 proposal — no exemptions.
3. **Re-run only the affected experiments** (+ regression-check any
   previously-MET criterion the change could plausibly break).
4. **Changelog entry**: M-vN, change, rationale, results delta. Update the
   Contribution Card to the same version — it always describes the current
   method (the same holds when S6a replaces the method).
5. **Criteria stay frozen** (iron rule 3). If the criteria themselves
   were wrong, that is a human decision to RE-FREEZE at a documented
   checkpoint — never a silent adjustment.
6. **Hard bound: 3 iterations**, then a MANDATORY human checkpoint. Default
   disposition: KEEP DIGGING — pursue the root cause and improve, or prove the
   approach genuinely unworkable. Options: continue (re-authorize 3 more),
   pivot (back to S3/S2 with lessons — replace an unpromising *approach*, do
   not abandon the *problem*; the next candidate comes first from the ranked,
   still-unevaluated S3 ideas, so the search does not stay stuck around one
   early idea), or — ONLY after the root cause is understood
   and a fix is either found or shown out of reach — report what works and
   what does not. "Just honestly report the negative" is NOT a first-line
   exit; it is earned by evidence of unworkability, never reached by giving
   up. Integrity holds throughout (iron rule 6): numbers from the ledger,
   criteria frozen, no cherry-picking.

## S6a — Ablation and simplification (ALWAYS runs once the criteria are MET)

This stage runs for every method whose criteria are MET — whether they were
met on the first S5 run (S6 never entered) or after S6 iterations. It is not
optional and not part of the S6 entry condition (ScientistTwo §3.4: the
Analyzer follows every successful full-set experiment).

1. **Run the ablations** pre-registered in the S4 Validation Plan: remove or
   replace one component at a time and log each result in the ledger. The
   output is the source-of-gain breakdown the paper's ablation table cites.
2. **Simplify under a strict-improvement gate.** A component that does not
   contribute (or hurts) is a candidate for removal. The simplified or
   modified method REPLACES the current best only if it is strictly better —
   or equal and simpler — on development data under the pre-registered
   metric. Otherwise keep the previous best. Any mechanism change still
   passes the S6 provenance guard (step 2a).
3. **If the method was replaced, re-run the ablations on the new method**
   before moving on — the ablation table must describe the method that is
   actually submitted. Bound: 2 replace-and-re-ablate rounds, then a human
   checkpoint.

## S7 — Adversarial stress test (pre-paper)

Before writing, run the reviewer simulation on the METHOD + LEDGER
package (not a drafted paper): security personas + security sprint
contract + the standard rejection anchors. Purpose: surface the fatal
objection while it is still cheap to fix. Findings route back as one
S6-style bounded round; criteria-bound re-check, no re-litigation.

Triage every weakness the panel raises into exactly one class (adapted from
ScientistTwo's rebuttal loop, §3.5–3.6):

- **TEXT** — a clarity/framing/positioning fix → handled in writing (S8).
- **EXPERIMENT** — needs evidence → becomes a planned supplementary run,
  executed under S5 ledger rules; the answer is the run, not a paragraph.
- **IDEA-LEVEL** — the method itself is weak → back to S6 (or S3); after the
  fix, ablation and drafting are redone downstream.

**Held-out reviewer rule:** the reviewer used to iterate a draft is
*in-distribution* — its rising score is not evidence of readiness (ScientistTwo:
7.5 on the reviewer it was tuned against, 5.7 on a held-out one). The go /
no-go judgement comes from a reviewer never used during revision — a different
model family, reading blind (HOWTO Step 17; `research_integrity_protocol.md` §2).

**Optional S7 output — Top-4 Readiness scorecard.** For a quick self-check
at this pre-paper stage (NOT a substitute for a venue decision), the panel
may emit:

```
TOP-4 READINESS (self-check, pre-paper — not a venue verdict)
Security significance   : ?/5      Threat model            : ?/5
Novelty                 : ?/5      Evaluation completeness : ?/5
Technical soundness     : ?/5      Practical relevance     : ?/5
Writing / framing       : ?/5
Major weaknesses: ...
Likely reviewer objections: ...
Missing experiments: ...
Overall: Strong Reject / Reject / Borderline / Accept / Strong Accept
```

This scorecard is a formative instrument for S7 only. The formal venue
simulation (S8 / HOWTO Step 14) MUST use the target venue's exact decision
vocabulary from `major_revision_playbook.md` §1 — never this 5-point scale.

## S8 — Paper and submission loop

`ars-full` with the security conventions (threat model section, ethics,
numeric citations, page budget), Contribution Card as the claims spine,
Provenance Ledger through experiment-provenance intake (claim→experiment
alignment). Then Phase-0 compliance check, reviewer simulation with the
target venue's vocabulary, and the multi-round submission lifecycle per
`major_revision_playbook.md`. Venue choice + deadline from the live
calendar; work-back schedule from the deadline.

**Review findings after a draft exists use the same three classes as S7** —
TEXT / EXPERIMENT / IDEA-LEVEL — in every round, including the final blind
review. An **IDEA-LEVEL** finding (the method itself is weak, not its
write-up or its evidence) is never patched in prose:

1. Back to S6 with the finding as the named deficiency (root cause, one
   targeted change, provenance guard).
2. **Keep-the-better rule:** the revised method replaces the current one only
   if it is strictly better on development data under the pre-registered
   metric. If it is not, keep the current method and answer the objection
   honestly as a stated limitation or a narrowed claim.
3. If the method changed: re-run S6a (the ablations), redraft the affected
   sections (Design, Evaluation, and any claim in the Abstract/Introduction
   that moved), then re-review.

Bound: 2 idea-level rounds after the first draft, then a human checkpoint
(ScientistTwo §3.6 meta-review loop, with the human as the meta-reviewer).

**Before submission — audit and package (both outputs, paper AND artifact):**

- Run the **pre-submission 4-check audit**
  (`research_integrity_protocol.md` §3): score re-verification from a clean
  checkout, specification compliance, reference + CVE/ATT&CK id verification,
  method-code alignment. Log the result in the ledger; a failed check blocks
  submission until fixed.
- **Package the artifact**: the code as run, scripts that regenerate every
  table and figure from the ledger's raw outputs, a README with exact
  commands and environment, anonymized per the venue's double-blind and
  open-science rules (`big4_venue_profiles.md`). The artifact is the second
  deliverable, not an afterthought.

## S8.5 — Retrospective Takeaway (the L2 knowledge-evolution engine)

Fires after a submission decision AND after each significant review round.
Adapted from AIBuildAI-2's L2 Builder (arXiv:2605.27873): distill the loop
into durable, structured knowledge so the system gets sharper each project
instead of relearning from scratch. Both successes and FAILURES are captured
— a dead-end teaches as much as a win.

Produce a bounded takeaway (append to `knowledge_notes/<project>.md`):

1. **What framing survived, at which venue** — the Contribution Card version
   that reached Accept-level, and the one(s) that did not.
2. **Which reviewer/rejection anchor actually fired** — the concrete
   objections that landed (map to the anchors in `security_reviewer_personas.md`).
3. **What was ruled out and why** — RQs abandoned (S2), methods judged
   RENAME/ADOPT+CITE (`method_change_provenance.md`), evaluations that did
   not convince, dead-end literature searches.
4. **Subfield lesson** — one line, tagged `provisional`, phrased as a
   candidate row/edit for `knowledge_index.md` (which subfield, what bar or
   best practice the project revealed).
5. **Integrity self-audit** — run the cheating-taxonomy self-check
   (`research_integrity_protocol.md` §3): did any number come from a best
   single run instead of the seed distribution? any tuning on the reported
   test set? any held-out/test-data use left undisclosed? does the released
   artifact match the paper's method? Record any near-miss (the AAR post-hoc
   trajectory monitor, applied to our own project).
6. **Next-frontier seed** — the accepted method becomes the next baseline:
   list its residual limitations (from the ablations and the reviews) as the
   limitation ledger that seeds the next S2 round (ScientistTwo's iterative
   frontier expansion: each cycle's method became the next cycle's baseline).

Then emit a PROPOSED additive edit to `knowledge_index.md` (a new row, or a
sharpened bar) — **proposed, never auto-applied**: it is surfaced to the
human gate. A lesson from ONE project is a hypothesis; mark it `provisional`
and promote it into the L1 cards only when a second project confirms it,
citing both projects + venues. This keeps the knowledge layer evolving
without letting a single noisy result rewrite the standard.

Iron rules carried in: numbers/claims in the takeaway trace to the
Provenance Ledger and the actual review artifacts (`ars-review/`), never to
memory; the takeaway records what happened, it never inflates a result.

## Knowledge streams (two, keep them named)

The overlay's knowledge evolves on two streams (AIBuildAI-2 dual-update
shape, arXiv:2605.27873):
- **External / field-tracking:** `deadlines_current.md` (refreshed via
  `fetch_deadlines.py` under the >7-day iron rule) + `perspective_retrieval_
  protocol.md` (pulls new attack papers / SoKs). A periodic pass should also
  refresh per-venue CFP idiosyncrasies (page limits, ethics/open-science
  status) into `big4_venue_profiles.md`.
- **Internal / own-experience:** the S8.5 retrospective → `knowledge_notes/`
  → promotions into `knowledge_index.md`. This is the stream that did not
  exist before and is why the overlay now sharpens per project.

## State-Diagnosis Router (advisory — agent proposes, human decides)

When you are mid-loop and unsure where to re-enter, the agent reads the
current artifact and RECOMMENDS a stage (it never auto-jumps — the S0/S4/S6/
S8 human gates remain the arbiter):

| Symptom in the current artifact | Recommended re-entry |
|---|---|
| Framing weak or ML-shaped; SECURITY FRAMING RISK | S3 (`security_framing_protocol.md`) |
| A claim lacks nearest-prior support / novelty unverified | S1 lit-search + `knowledge_index.md` bar |
| An RQ is chosen but nobody has tested whether it is worth committing to | Topic verification gate (`topic_verification_gate.md`) |
| A pre-registered criterion is UNMET | S6 bounded improvement |
| All criteria MET but no ablation results in the ledger | S6a ablation & simplification |
| A reviewer says the method itself is weak (after a draft exists) | S8 IDEA-LEVEL route → S6 → S6a → redraft |
| Paper converged but no audit result / no packaged artifact | S8 pre-submission audit + artifact packaging |
| A rescue/substitute method proposed | S6 step 2a (`method_change_provenance.md`) |
| Over page budget / format non-compliant / missing ethics | S8 R0 Phase-0 check |
| Decision received / review round done | S8.5 retrospective |

Because writing has no scalar progress signal, the router only classifies
the artifact's state; it cannot self-schedule the way an auto-ML loop does.

## Invocation

Say what stage you are at; the protocol meets you there. Examples:
- "帮我从这批文献找 gap 并延伸课题" → S1–S2
- "评估我的方法的 novelty 和 contribution" → S3 evaluate mode
- "为这个方法设计证伪实验" → S4
- "跑实验/结果不达标，改进方法" → S5–S6
- Full loop from scratch: state the topic → S0 onward.
  On Claude Code, prefer the `novelty-engine` skill's richer S0–S4 agents
  (shipped in this suite; this protocol supplies the security calibration
  on top). On Codex the same skill runs role by role without subagents, or
  this protocol + experiment-agent WORKFLOW carry every stage.
