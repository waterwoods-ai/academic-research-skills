# Lab Orchestration Protocol (Custom — Security Track)

> How three AI agents share one research project as a small security lab, so
> that no critical result rests on a single agent. Run it WITH
> `research_loop_protocol.md`: that file says what each stage must produce;
> this one says who produces it, who checks it, and who may write which file.
> Role design: the researcher's `orchestration.md` (adopted 2026-10-05),
> reduced to three agents on 2026-10-06; roles reassigned by Tom the same
> day (Codex advisor and reviewer; Claude Code researcher and coordinator;
> GLM researcher and experimenter).

## Principles

1. **Planning, building and judging are split.** Codex plans and reviews but
   builds nothing: it writes no code, runs no experiment and writes no paper
   text. GLM builds and runs. Claude Code coordinates, verifies and writes.
   No agent is the only judge of its own work.
2. **No critical result has a single owner.** Every item has a primary agent
   and an independent checker (matrix below). A checker never checks its own
   contribution.
3. **Retrieval, not recollection.** A novelty or prior-art judgment counts only
   with a retrieved source (title, authors, year, identifier). "I know of no
   such work" from memory is a lead to search, never a verdict. In earlier
   rounds, reviewers judging novelty from memory missed published work twice.
4. **The reviewer stays out of creation.** Codex does not generate ideas,
   write code or write the paper, so its attacks on them are independent. Its
   own plan is checked by Claude, and the PI approves it.
5. **The PI decides.** Agents propose; the researcher has final authority over
   the research question, security scope, design freezes, compute launches,
   interpretation and claims.
6. **Files, not chat.** Every hand-off is a file. Each file has one writer.

## Roles

| Agent | Role | The questions it asks | Owns |
|---|---|---|---|
| **You** | Principal Investigator | What contribution are we actually trying to make? | Decisions: direction, scope, plan approval, freezes, compute go, claims |
| **Codex** | Advisor; Reviewer #2 | What is the full research plan? What is my professional opinion at this gate? Why should this paper be rejected? | The full research plan, written at the very start and revised once the research question is fixed; a professional opinion at every gate; attacks on novelty (with retrieved papers), threat model, methodology, statistics, evaluation and contribution; the review rounds; the reject-reasons register; the sentence-level citation audit; the final review before submission |
| **Claude Code** | Researcher; coordinator | How does the plan break into doable sub-plans? Is the method sound? Is it novel? What do the results show? | Sub-plans and task briefs; literature (scouting, systematic review, Elicit and Zotero APIs, retrieval subagents); its own ideas; methodology verification; novelty verification by retrieval; result analysis and the claims register; the research question, contribution card and paper; recording the PI's decisions |
| **GLM** (opencode) | Researcher; experimenter | What is the actual attacker/defender problem? What novel method solves it? Does it work? | Ideas; threat model and attack surface; novel-method proposals (`novelty-engine`); experiment plans until frozen; implementation, runs on gpu1 under the host resource limits, the run ledger, results, the method changelog, the artifact |

**Codex in one thread.** Codex works in a single thread (Tom, 2026-10-06:
VS Code opens one Codex window). It builds nothing, so it can review code
and results it did not produce. Review briefs are artifact-only: they name
the files under review, and each objection must cite the file and section it
rests on, plus a retrieved paper for any novelty objection. An objection
without a citation does not count.

**Final review (HOWTO Step 17).** Codex, in the same session (Tom's
decision, 2026-10-06). It has seen the review rounds, so it is a final check,
not a blind one, and its record says so.

**Two researchers, independent ideas.** Claude and GLM generate ideas
separately, each in its own file, so two model families explore the space.
Neither verifies the novelty of its own ideas: Claude verifies GLM's by
retrieval, Codex verifies Claude's.

**Model families.** Claude, GLM and OpenAI are three independent sources of
error; that independence is the point.

**Fewer tools.** Fold roles, never checks. With one tool, every check runs in a
fresh session that sees the artifact but not the producer's reasoning.

## Who writes which file

Use the research loop's file names; macOS treats `RESEARCH_QUESTION.md` and
`research_question.md` as one file, so never create upper-case duplicates.

| Writer | Files |
|---|---|
| Codex | `research_plan.md`; `reviews/` (`advisor_opinions.md`, `reject_reasons.md`); `ars-review/` rounds |
| Claude | `subplans/`, `decisions.md`, `research_question.md`, `contribution_card.md`, `claims.md`, `ideas_claude.md`, `verification/` (methodology and novelty reports), `gap_registry.md`, `literature.md`, `literature/`, `paper/` |
| GLM | `rq_cards.md`, `security/` (threat model, attack surface, defense assumptions, hypotheses, adversarial cases), `novelty_engine/`, `candidate_cards.md`, `screening_plan.md` and `validation_plan.md` until frozen, `method_changelog.md`, code (`src/`, `experiments/`), `tests/`, the run ledger (`ledger/`), `results/`, the artifact |

- **Direction files change only on a recorded decision.** `research_plan.md`,
  `research_question.md`, `contribution_card.md` and `claims.md` change only
  after Claude writes the PI's decision into `decisions.md` in the PI's own
  words, with the date and what it supersedes. Then the file's writer edits
  it. Other agents propose changes in their reports.
- **Frozen plans** change only through a logged RE-FREEZE decided by the PI.
- **An unexplained change** to any file is an incident: find the writer before
  trusting the file (`ide-agent-orchestration` coordination notes list where
  each agent's tool calls are logged).
- **Existing projects** keep their layout; record each folder's writer in the
  project's `AGENTS.md`.

## Independent-check matrix

| Item | Primary | Independent checker | The check must contain |
|---|---|---|---|
| Full research plan | Codex | Claude | Feasibility against the resources and compute budget; a testable success criterion per phase; then PI approval |
| Sub-plans | Claude | Codex | Every plan item covered; nothing added that the plan does not ask for |
| Literature search | Claude | Codex | Missing-paper attack with retrieved citations |
| Novelty of GLM's ideas and candidates | Claude (retrieval) | Codex | An attempt to invalidate it with a retrieved paper; no citation, no objection |
| Novelty of Claude's ideas | Codex (retrieval) | GLM | A second, independent retrieval |
| Threat model | GLM | Claude | The 11 fields and three stress tests of `threat_model_workbench.md` |
| Method and formalization | GLM | Claude | Correctness, complexity and convergence proven or cited (iron rule 5) |
| Hypotheses | GLM | Claude | Fundamentals stated, decomposed into sub-claims (iron rule 5) |
| Experiment design | GLM | Claude | Feasibility, statistics, fairness to every baseline and candidate, disjoint held-out |
| Implementation | GLM | Claude | Code read against the method and threat model; the pre-run checks of S5 |
| Result analysis and statistics | Claude | Codex | Recomputed from raw outputs in the ledger, not from summaries |
| Result interpretation | Claude | Codex | Each claim challenged against its evidence in `claims.md` |
| Related work | Claude | GLM | Every cited difference checked against the cited paper |
| Paper writing | Claude | Codex | Sentence-level citation audit: SUPPORTED / PARTIALLY SUPPORTED / UNSUPPORTED |
| Review simulation | Codex | GLM | A second reading of the same draft; disagreements listed |
| Reproducibility | GLM | Claude | Clean-checkout re-run of the 4-check audit |
| Final review | Codex, same session | PI | The record states that it saw the review rounds |

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
Codex's own plan is confirmed by Claude instead. No serious reason may be
OPEN at submission. Once a draft exists, `ars-review/` rounds carry the
review and this register keeps the open items.

## Stages, owners and gates

The lab's stages run the research loop; the HOWTO step numbers are in brackets.

| Lab stage | Loop | Primary | Check / gate |
|---|---|---|---|
| Research plan [0.5] | — | Codex writes `research_plan.md`; Claude breaks Phase A into sub-plans | Claude checks the plan; PI approves |
| 0 Problem selection [1a] | S0 | Claude, with the PI | — |
| 1 Systematic literature review [1b] | S1 | Claude | Codex |
| 2 Ideas [2] | S1–S2 | GLM and Claude, independently | — |
| 3 Novelty and gap verification [3] | S1–S2 | Claude for GLM's ideas, Codex for Claude's; Codex's opinion | **Gate 1** |
| 4 Threat model [2–4] | S2 | GLM | Claude — **Gate 2** |
| 5 Research question [4] | S2–S3 | Claude writes `research_question.md` on the PI's decision | — |
| Plan revision [4.5] | — | Codex revises `research_plan.md`; Claude writes the sub-plans for Phases B–C | Claude checks; PI approves |
| 6 Method proposal [5a–5b] | S3 | GLM; Claude may add candidates | Claude (methodology, novelty); Codex |
| 7 Experiment design [5b, 8] | S3–S4 | GLM | Claude |
| 8 Scientific review [6, 9] | S3–S4 | Codex (Reviewer #2 and opinion) | PI freezes |
| 9 Implementation and pilot [7.5, 10] | S5–S5a | GLM | Claude |
| 10 Confirmatory experiments [10–12.5] | S5–S6a | GLM | **Gate 3** |
| 11 Result analysis [12, 12.5] | S6–S7 | Claude | Codex; `claims.md` |
| 12 Paper writing [13] | S8 | Claude | Codex — **Gate 4** first |
| 13 Reviewer #2 attack [14, 16] | S8 | Codex | GLM |
| 14 Additional experiments [15] | S8 | GLM | Claude |
| 15 Artifact and reproducibility [17.2] | S8 | GLM | Claude |
| Final review [17] | S8 | Codex, same session | PI |

The HOWTO keeps Scientific review (Steps 6 and 9) before any GPU time, so a
flawed plan is caught before it costs compute.

**Gates.** No stage advances because an agent says it is done.

- **Gate 1 — novelty, before implementation:** more than 30 directly relevant
  papers checked; the closest 5 identified; the difference from each
  documented; Codex unable to invalidate the novelty with a retrieved paper.
  Also `topic_verification_gate.md` and the Phase 3.5 mechanism re-check.
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
  first (`security_framing_protocol.md`); Codex's professional opinion. If
  these have no convincing answer, do not start writing.

## When an agent refuses

A refusal is never retried verbatim on another model, and never rephrased to
get past it. Claude reads what was refused and routes each part:

| Blocked portion | Route |
|---|---|
| Literature, explanation | Claude |
| Threat model, attack-surface analysis | GLM |
| Defensive implementation | GLM |
| Analysis, statistics | Claude |
| Planning, review | Codex |
| Potentially sensitive execution, or anything outside `AUTHORIZED_RESEARCH.md` | **stop — PI review** |

Claude records the refusal, the routing and the PI's decision in
`decisions.md`.

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
  never another agent's opinion of them.
- With the `ide-agent-orchestration` skill installed, Claude sends each brief
  through that agent's bridge and reads results from the files.
