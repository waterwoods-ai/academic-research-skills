# Topic Verification Gate (Custom — Security Track)

> Twelve questions a research question must answer before method work starts.
> Run it between S2 (RQ chosen) and S3 (method), and again at S7 if the
> framing moved. Adapted from the researcher's own `verify-research-topic`
> skill; this file is the tool-independent part, usable on every runtime. The
> browser-driven blind second opinion lives in that skill
> (`topic_scouting_overlay.md` says when to use it).
>
> The gate exists because a topic that fails Q1, Q3 or Q11 costs months and
> cannot be rescued by a good method.

## How to run it

1. **Gather the evidence**: the RQ card, the gap registry, any design notes.
   A topic with no written design gets a one-paragraph design first.
2. **Answer all twelve yourself, then freeze the answers.** Each answer shows
   its evidence — a file and section, a verified paper, or `no evidence yet` —
   and a status: **pass** (all criteria met), **weak** (some met, or met only
   by assertion), **fail** (none met, or the evidence contradicts the claim).
3. **Get an independent second opinion** from a different model family that
   has not seen your answers, your worries or your prior-art list: give it
   only the design facts (problem setting, threat model, method, evaluation
   plan, scope). Agreement from a model you primed is not evidence.
4. **Resolve every disagreement against evidence** — the design, the ledger,
   the paper in question — never by asking which side is right. An issue both
   sides raised independently is high confidence. Re-grade against the
   criteria below only; do not soften or harden a status to match the other
   model.
5. **Record the verdict** (go / revise / stop) on the RQ card, with one action
   per `weak` or `fail` row. The researcher decides (human gate).

## The 12 questions, with pass criteria

| # | Question | Passes only if the answer… |
|---:|---|---|
| 1 | What exact security problem am I solving? | Names the **asset**, the **adversary** and the **security property violated**, in one or two sentences. It must be a failure an attacker can cause — not "X is hard" or "X is under-studied". |
| 2 | Why should the security community care? | Shows **deployed practice or a documented incident** affected, with a source. A citation count or a market trend alone is weak. |
| 3 | What is still unknown after the closest prior work? | Names the **closest 2–3 works** (verified) and the specific question they leave open. "Nobody has combined A and B" is weak unless the combination changes a result. |
| 4 | What exactly is my threat model, and is it realistic? | States capabilities, knowledge, goals and **what the attacker cannot do**; realism argued from a real delivery channel or incident. A defence must include an **adaptive attacker who knows the defence**, or it is at most weak. |
| 5 | What variable am I actually studying? | One **independent variable** and one **dependent variable**, with confounds held fixed. More than one manipulated factor must be a stated factorial design. |
| 6 | What evidence would prove or falsify my claim? | A **pre-stated outcome that would refute the claim**, with a threshold. A claim no result could refute fails. |
| 7 | Are my metrics measuring security, or merely a proxy? | The primary metric is an **attacker-outcome quantity** (e.g. attacks that get through on the real system), or the proxy's link to that outcome is shown. Accuracy / F1 on a benchmark alone is a proxy. |
| 8 | What alternative explanation could produce my result? | At least **two concrete alternatives** (dataset artefact, circularity between method and benchmark, tuning on the test set, a weak baseline) and the control that rules each out. |
| 9 | How realistic is my experimental environment? | Compares the environment with deployment on **data source, scale, attacker behaviour and engine**, and states each known gap. |
| 10 | What would the study still teach if my hypothesis is wrong? | Names what the design establishes **either way**, and why that matters. "We would learn something" is weak. |
| 11 | What will the security community know after this paper that it did not know before? | One or two **falsifiable statements** of new knowledge, not a list of artefacts built. |
| 12 | What are the three strongest reasons a reviewer could reject this paper? | Three **distinct** reasons, ranked, each with a pre-emption concrete enough to schedule. |

## Verdict rules (applied after the disagreements are resolved)

- **stop** — Q1, Q3 or Q11 is `fail`: there is no clear problem, no gap, or no
  new knowledge. Back to S2 for a different framing of the problem.
- **revise** — any other `fail`; or Q4, Q6 or Q7 is `weak`; or three or more
  questions are `weak`. Fix the design, then re-run the affected questions.
- **go** — everything else. Proceed to S3.

Summary form: go / revise / stop, one sentence with the deciding question.

## How the questions connect to the rest of the overlay

| Question | Deepened by |
|---|---|
| Q1, Q2, Q11 | `security_framing_protocol.md` (framing chain, "what does the community learn") |
| Q3 | S1 gap registry; `topic_scouting_overlay.md` (ancestor and adjacent-family queries) |
| Q4 | `threat_model_workbench.md` (11 fields, three stress tests) |
| Q5, Q6, Q8 | S4 Validation Plan and the pre-registration card (`research_integrity_protocol.md`) |
| Q7, Q9 | `knowledge_index.md` (the subfield's reviewer bar) |
| Q12 | `security_reviewer_personas.md` (rejection anchors) |

**Q10 and iron rule 6.** Q10 tests the design — a study worth running teaches
something whichever way it comes out. It is not permission to settle: when a
result does come out negative, the loop still digs for the root cause (S6).
