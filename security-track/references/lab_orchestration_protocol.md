# Lab Orchestration Protocol (Custom — Security Track)

> How three AI agents share one research project as a small security lab, so
> that no critical result rests on a single agent. Run it WITH
> `research_loop_protocol.md`: that file says what each stage must produce;
> this one says who produces it, who checks it, and who may write which file.
> Role design: the researcher's `orchestration.md` (adopted 2026-10-05),
> reduced to three agents on 2026-10-06.

## Principles

1. **The Director manages the research; it does not do all of it.** Claude
   Code is never the sole programmer, statistician, or reviewer of its own
   paper, and its literature and novelty findings are always checked by
   another agent.
2. **No critical result has a single owner.** Every item has a primary agent
   and an independent checker (matrix below). A checker never checks its own
   contribution.
3. **Retrieval, not recollection.** A novelty or prior-art judgment counts only
   with a retrieved source (title, authors, year, identifier). "I know of no
   such work" from memory is a lead to search, never a verdict. In earlier
   rounds, reviewers judging novelty from memory missed published work twice.
4. **The reviewer stays out of creation.** Reviewer #2 does not take part in
   generating the idea or writing the paper, so its attacks are independent.
5. **The PI decides.** Agents propose; the researcher has final authority over
   the research question, security scope, design freezes, compute launches,
   interpretation and claims.
6. **Files, not chat.** Every hand-off is a file. Each file has one writer.

## Roles

| Agent | Role | The questions it asks | Owns |
|---|---|---|---|
| **You** | Principal Investigator | What contribution are we actually trying to make? | Decisions: direction, scope, freezes, compute go, claims |
| **Claude Code** | Research Director; literature and novelty | Are we answering the right scientific question? Has somebody already answered it? | Research question, hypothesis decomposition, roadmap, task assignment, evidence tracking, decisions, paper architecture and writing, disagreement resolution, gates; systematic review and novelty reports by retrieval (Elicit and Zotero APIs, the scouting skills, retrieval subagents) |
| **GLM** (opencode) | Security scientist | What is the actual attacker/defender problem? | Threat model, attack surface, defense assumptions, hypotheses, adversarial cases, experiment proposals; candidate generation (`novelty-engine`); independent checker of implementation and interpretation |
| **Codex** | Research engineer; Reviewer #2 | Can we prove this experimentally and reproduce it? Why should this paper be rejected? | Experiment framework, runs on gpu1, reproducibility manifests, statistical pipeline, regression tests, artifact. As Reviewer #2: attacks on novelty (with retrieved papers), threat model, design and paper; review rounds; the reject-reasons register |

**Codex has two roles in one thread.** Engineering and Reviewer #2 work run in
the same Codex thread (Tom's decision, 2026-10-06: VS Code opens one Codex
window). Three rules keep the review honest without a fresh context:

1. As Reviewer #2 it never reviews its own code or results: GLM checks the
   implementation and the Director checks statistics and reproducibility.
2. Every review brief is artifact-only. It names the files under review, and
   each objection must cite the file and section it rests on, plus a retrieved
   paper for any novelty objection. An objection without a citation does not
   count.
3. Review records say the review ran in the engineering thread, not a fresh
   context. The fully independent check is the final blind review in a fresh
   GLM session.

**Model families.** Claude, GLM and OpenAI are three independent sources of
error; that independence is the point. The final blind review (HOWTO Step 17)
runs in a fresh GLM session: GLM did not write the paper or run the review
rounds.

**Fewer tools.** Fold roles, never checks. With one tool, every check runs in a
fresh session that sees the artifact but not the producer's reasoning, and the
final review still needs a different model family where one is available.

## Who writes which file

Workers' files hold drafts and evidence. The Director's files hold what the
project has decided. Use the research loop's file names; macOS treats
`RESEARCH_QUESTION.md` and `research_question.md` as one file, so never create
upper-case duplicates.

| Writer | Files |
|---|---|
| Director | `research_question.md`, `contribution_card.md` (contributions, threat model as adopted, limitations), `claims.md`, `decisions.md`, `method_changelog.md`, `paper/`; `gap_registry.md`, `literature.md`, `literature/` |
| GLM | `rq_cards.md`, `security/` (threat model, attack surface, defense assumptions, hypotheses, adversarial cases), `novelty_engine/`, `candidate_cards.md`, `screening_plan.md` and `validation_plan.md` until frozen |
| Codex | code (`src/`, `experiments/`), `tests/`, the run ledger (`ledger/`), `results/`, the artifact; as Reviewer #2: `reviews/` (including `reject_reasons.md`) and `ars-review/` rounds |

- **Direction files change only on a recorded decision.** The Director writes
  the PI's decision into `decisions.md` in the PI's own words, with the date and
  what it supersedes, then edits the file. Other agents propose changes in
  their reports.
- **Frozen plans** change only through a logged RE-FREEZE decided by the PI.
- **An unexplained change** to any file is an incident: find the writer before
  trusting the file (`ide-agent-orchestration` coordination notes list where
  each agent's tool calls are logged).
- **Existing projects** keep their layout; record each folder's writer in the
  project's `AGENTS.md`.

## Independent-check matrix

| Item | Primary | Independent checker | The check must contain |
|---|---|---|---|
| Literature search | Director | Codex | Missing-paper attack with retrieved citations |
| Novelty of the RQ and of each candidate | Director (retrieval) | Codex | An attempt to invalidate it with a retrieved paper; no citation, no objection |
| Threat model | GLM | Director | The 11 fields and three stress tests of `threat_model_workbench.md` |
| Hypotheses | GLM | Director | Fundamentals stated, decomposed into sub-claims (iron rule 5) |
| Experiment design | GLM | Codex | Feasibility, statistics, fairness to every baseline and candidate, disjoint held-out |
| Implementation | Codex | GLM | Code read against the method and threat model; the pre-run checks of S5 |
| Statistics | Codex | Director | Recomputed from raw outputs, not from summaries |
| Result interpretation | Director | GLM | Each claim challenged against its evidence in `claims.md` |
| Related work | Director | GLM | Every cited difference checked against the cited paper |
| Paper writing | Director | Codex | Sentence-level citation audit: SUPPORTED / PARTIALLY SUPPORTED / UNSUPPORTED |
| Review simulation | Codex | GLM | A second reading of the same draft; disagreements listed |
| Reproducibility | Codex | Director | Clean-checkout re-run of the 4-check audit |

## Claims register (`claims.md`)

One line per claim the paper will make, from the Contribution Card to
submission:

```
C01 | <the claim, as it will read in the paper>
    | evidence: <ledger run ids; table or figure; statistical test>
    | status: PROPOSED / PILOT-SUPPORTED / CONFIRMED / NARROWED / REFUTED / DROPPED
    | checked by: <agent, date> | limitations: <what the evidence does not cover>
```

- CONFIRMED needs ledger evidence and a check by an agent that did not
  produce it.
- Every claim in the abstract, introduction and conclusion maps to a
  CONFIRMED id; a sentence with no id is removed, or registered and checked.
- REFUTED stays with its root cause (iron rule 6); NARROWED keeps the original
  wording beside the new one, so the paper cannot drift back.

## Reject-reasons register (`reviews/reject_reasons.md`)

Reviewer #2 writes its objections here from Stage 2 onward:

```
R01 | <reason to reject> | dimension: novelty / threat model / methodology / statistics / evaluation / contribution
    | raised: <agent, date> | status: OPEN / FIXED / REBUTTED / LIMITATION | cleared: <agent, date>
```

FIXED and REBUTTED need evidence (a ledger run, a retrieved source, a proof).
LIMITATION needs the PI's approval and goes into the paper. Reviewer #2
confirms each clearance; the agent that fixed it cannot. A reason about
Codex's own code or results is confirmed by GLM instead. No serious reason may
be OPEN at submission. Once a draft exists, `ars-review/` rounds carry the
review and this register keeps the open items.

## Stages, owners and gates

The lab's stages run the research loop; the HOWTO step numbers are in brackets.

| Lab stage | Loop | Primary | Check / gate |
|---|---|---|---|
| 0 Problem selection [1a] | S0 | Director, with the PI | — |
| 1 Systematic literature review [1b] | S1 | Director | Codex |
| 2 Novelty and gap verification [3] | S1–S2 | Director | Codex — **Gate 1** |
| 3 Threat model [2] | S2 | GLM | Director — **Gate 2** |
| 4 Research hypotheses [2–4] | S2–S3 | GLM; the Director writes `research_question.md` on the PI's decision | Director |
| 5 Experiment design [5a–5b, 8] | S3–S4 | GLM | Codex |
| 6 Implementation [7.5, 10] | S5 | Codex | GLM |
| 7 Pilot experiments [7.5] | S5a | Codex | GLM |
| 8 Scientific review [6, 9] | S3–S4 | Director, Codex as Reviewer #2 | PI freezes |
| 9 Confirmatory experiments [10–12.5] | S5–S6a | Codex | **Gate 3** |
| 10 Evidence and statistics [12, 12.5] | S6–S7 | Codex, Director | `claims.md` |
| 11 Paper writing [13] | S8 | Director | Codex — **Gate 4** first |
| 12 Reviewer #2 attack [14, 16] | S8 | Codex | GLM |
| 13 Additional experiments [15] | S8 | Codex | GLM |
| 14 Artifact and reproducibility [17.2] | S8 | Codex | Director |
| Final blind review [17] | S8 | A fresh GLM session | PI |

The HOWTO keeps Scientific review (Steps 6 and 9) before any GPU time, so a
flawed plan is caught before it costs compute.

**Gates.** No stage advances because an agent says it is done.

- **Gate 1 — novelty, before implementation:** more than 30 directly relevant
  papers checked; the closest 5 identified; the difference from each
  documented; Reviewer #2 unable to invalidate the novelty with a retrieved
  paper. Also `topic_verification_gate.md` and the Phase 3.5 mechanism re-check.
- **Gate 2 — threat model, before experiments:** attacker goal, knowledge,
  capability and budget; defender assumptions; success criteria
  (`threat_model_workbench.md`).
- **Gate 3 — experimental validity, before a claim is CONFIRMED:** appropriate
  baselines, multiple seeds, confidence intervals, ablation, sensitivity
  analysis, no leakage, fair hyper-parameters (S4 checklists,
  `research_integrity_protocol.md` §2, S5 pre-run checks).
- **Gate 4 — contribution, before polishing the paper:** why does the security
  community care; what was unknown before; is this a technique, measurement,
  system, dataset, attack, defense or finding; what would Reviewer #2 attack
  first (`security_framing_protocol.md`). If these have no convincing answer,
  do not start writing.

## When an agent refuses

A refusal is never retried verbatim on another model, and never rephrased to
get past it. The Director reads what was refused and routes each part:

| Blocked portion | Route |
|---|---|
| Literature, explanation | Director |
| Threat model, attack-surface analysis | GLM |
| Defensive implementation | Codex |
| Analysis, statistics | Codex |
| Potentially sensitive execution, or anything outside `AUTHORIZED_RESEARCH.md` | **stop — PI review** |

Record the refusal, the routing and the PI's decision in `decisions.md`.

Every project that runs attacks, even on a testbed, keeps an
`AUTHORIZED_RESEARCH.md` (template in `templates/`): environment, permitted,
not permitted, data handling, disclosure, approver and date. Agents work only
inside it; the paper's Ethics Considerations section is written from it.

## Briefing the agents

- All three agents load the ARS and security-track skills (Claude Code and
  Codex through their plugins, opencode through the links in its skills
  folder), so a brief can name a skill or a reference file directly.
- **The suite is security-first** (routing core; opt-out only under
  security-track § Activation), so a brief does not restate the security
  conventions. It names the target venue, which sets the template, page
  limit, ethics requirements and decision terms.
- **Every brief states:** the role, the files the agent may write (its own
  only), the stop point, and a short numbered reply format.
- **Reviewer #2 gets artifacts, not conclusions:** the plan, draft or results,
  never the Director's opinion of them, and never its own code or results to
  judge.
- With the `ide-agent-orchestration` skill installed, the Director sends each
  brief through that agent's bridge and reads results from the files.
