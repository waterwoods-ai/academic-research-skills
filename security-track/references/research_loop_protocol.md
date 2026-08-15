# Security Research Loop Protocol (Custom — Security Track)

> Extends the overlay from literature-and-review into the FULL research
> loop: topic → gap → research question → method proposal (or deep
> evaluation of the user's method) → novelty & contribution sharpening →
> experiment design → execution → bounded improvement iterations →
> adversarial stress test → paper. Runs on both runtimes: Claude Code
> (where the novelty-engine plugin supplies stages S0–S4 machinery) and
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
   that cannot be formalized is not yet a method.

## Stage map and runtime routing

| Stage | Output | Claude Code | Codex |
|---|---|---|---|
| S0 Topic viability | go / no-go verdict | novelty-engine Phase 0a (topic_verifier) | deep-research quick + this protocol §S0 |
| S1 Gap registry | evidenced gap list | `/ars-lit-review` + perspective protocol + gap_analyzer | `ars-lit-review` + perspective protocol, gaps per §S1 |
| S2 RQ generation | ranked candidate RQs | gap_analyzer + dogma_extractor | this protocol §S2 |
| S3 Method / evaluation | Contribution Card | novelty_verifier + cross_domain_synthesizer + math_formalizer | this protocol §S3 |
| S4 Experiment design | frozen falsification plan | experiment_falsifier | experiment-agent WORKFLOW planning + §S4 bars |
| S5 Execution | provenance ledger | experiment_coder + session runs code | Codex writes & runs code + §S5 ledger |
| S6 Improvement loop | method changelog M-v1→M-vN | this protocol §S6 (both runtimes) | same |
| S7 Stress test | hardened method + results | `/ars-reviewer` w/ security contract | `ars-reviewer` w/ security contract |
| S8 Paper → submission | venue-ready paper | `/ars-full` + provenance intake + Phase-0 | `ars-full` same |

## S0 — Topic viability (go / no-go)

Before any investment: is the topic saturated, misframed, or viable?
Retrieve the 5–10 most-cited and most-recent Big-4/tier-2 papers on the
topic; verdict with evidence: SATURATED (recent top-venue work occupies
the space — name the papers), MISFRAMED (the interesting question is
adjacent — restate it), or VIABLE (name the open territory). HUMAN GATE:
the researcher decides to proceed, pivot, or stop.

## S1 — Gap registry

Run the literature review with the perspective-retrieval protocol (six
security lenses + moderator round). Each candidate gap is an ABSENCE
claim and must carry: (a) the search that failed to fill it (queries +
indexes + date), (b) the nearest-miss papers and why each falls short,
(c) a security relevance statement (what attack/defense/measurement
question the gap blocks). Gaps without (a) are hunches, not gaps.

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

## S3 — Method proposal OR deep evaluation (novelty & contribution focus)

Two entry modes, same output artifact:

- **Propose mode**: design a new method for the chosen RQ. Cross-domain
  transplantation is encouraged (control theory → CPS anomaly detection,
  etc.) but the transplant must be justified against the threat model.
- **Evaluate mode**: the user brings their own method; the loop deepens
  it rather than replacing it.

Both modes MUST produce the **Contribution Card** — the artifact the
whole loop optimizes:

```
CONTRIBUTION CARD — <method name> (M-v1)
1. Claims: 3–5 falsifiable claims (each will map to experiments in S4)
2. Novelty status per claim: NOVEL-WITHIN-SEARCH / INCREMENTAL / KNOWN
   — verdict from real retrieval against Big-4 + tier-2 literature,
   with the nearest prior work cited for every claim
3. Positioning table: this method vs the 3–5 closest published methods,
   dimension by dimension (threat model, assumptions, overhead, eval)
4. Delta statement: one paragraph — what a Big-4 reviewer would call
   the contribution, in the community's own terms
5. Formalization: math or algorithm (iron rule 5) + threat model
6. Honest weaknesses: what the skeptic persona (R4) would attack first
```

Any claim graded KNOWN is dropped or reworked NOW — before a single
experiment is designed. INCREMENTAL claims survive only with an explicit
positioning argument.

## S4 — Experiment design (falsification-first, security bars)

Design experiments to REFUTE each claim, not confirm it. Every design
must satisfy the same bars the review contract (D2) will later judge:

- Defense/AI-security claims → evaluated against ADAPTIVE adversaries
  aware of the method; strongest published attacks as baselines,
  correctly tuned.
- CPS claims → real testbed or hardware-in-the-loop, or an explicit
  simulation-fidelity argument; physical consequence measured.
- IoT claims → device/vendor diversity matched to the claim's breadth.
- ML-for-security detection claims → base rates realistic, datasets
  temporally split, false-positive cost at deployment scale.

Pre-register in the frozen **Falsification Plan**: per claim — the
experiment(s), metrics, numeric success criteria, baselines, ablations,
statistical plan (seeds, repetitions, tests), and the artifact/open-
science plan. DESIGN FREEZE (human gate): after approval the success
criteria are immutable for the life of the loop.

## S5 — Execution

The coding agent implements and RUNS the experiments in the user's
environment (this is the researcher's own execution, assisted — the
paper's methods section must stay honest about tooling). Every run
appends to the **Provenance Ledger** (ARS experiment-provenance
compatible): experiment id → claim id, planned vs executed (deviations
named), raw output location, result vs pre-registered criterion
(MET / UNMET / INCONCLUSIVE), negative results and surprises. The ledger
is the ONLY source S8 may cite numbers from.

## S6 — Bounded improvement loop (the anti-dead-loop core)

Enter only if ≥1 pre-registered criterion is UNMET. Per iteration
(M-v1 → M-v2 → …):

1. **Name the deficiency**: which claim, which criterion, what the
   ledger shows.
2. **One targeted change** to the method, with the mechanism hypothesis
   ("criterion X fails because Y; change Z addresses Y").
3. **Re-run only the affected experiments** (+ regression-check any
   previously-MET criterion the change could plausibly break).
4. **Changelog entry**: M-vN, change, rationale, results delta.
5. **Criteria stay frozen** (iron rule 3). If the criteria themselves
   were wrong, that is a human decision to RE-FREEZE at a documented
   checkpoint — never a silent adjustment.
6. **Hard bound: 3 iterations**, then a MANDATORY human checkpoint with
   exactly three options: continue (re-authorize 3 more), pivot (back to
   S3/S2 with lessons recorded), or accept-and-report (an honest paper
   about what works and what does not — negative results at the bar of
   iron rule 2 are publishable content, not failure).

## S7 — Adversarial stress test (pre-paper)

Before writing, run the reviewer simulation on the METHOD + LEDGER
package (not a drafted paper): security personas + security sprint
contract + the eight rejection anchors. Purpose: surface the fatal
objection while it is still cheap to fix. Findings route back as one
S6-style bounded round; criteria-bound re-check, no re-litigation.

## S8 — Paper and submission loop

`ars-full` with the security conventions (threat model section, ethics,
numeric citations, page budget), Contribution Card as the claims spine,
Provenance Ledger through experiment-provenance intake (claim→experiment
alignment). Then Phase-0 compliance check, reviewer simulation with the
target venue's vocabulary, and the multi-round submission lifecycle per
`major_revision_playbook.md`. Venue choice + deadline from the live
calendar; work-back schedule from the deadline.

## Invocation

Say what stage you are at; the protocol meets you there. Examples:
- "帮我从这批文献找 gap 并延伸课题" → S1–S2
- "评估我的方法的 novelty 和 contribution" → S3 evaluate mode
- "为这个方法设计证伪实验" → S4
- "跑实验/结果不达标，改进方法" → S5–S6
- Full loop from scratch: state the topic → S0 onward.
  On Claude Code with the novelty-engine plugin installed, prefer its
  richer S0–S4 agents (this protocol supplies the security calibration
  on top); on Codex, this protocol + experiment-agent WORKFLOW carry
  every stage.
