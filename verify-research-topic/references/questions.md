# The 12 questions, with pass criteria

Every answer must show the evidence it rests on: a file and section, a verified paper, or `no evidence yet`.
Status per question: **pass** (all criteria met), **weak** (some met, or met only by assertion), **fail** (none met, or the evidence contradicts the claim).

| # | Question | Passes only if the answer… |
|---:|---|---|
| 1 | What exact security problem am I solving? | Names the **asset**, the **adversary**, and the **security property violated**, in one or two sentences. It must be a failure an attacker can cause, not "X is hard" or "X is under-studied". |
| 2 | Why should the security community care? | Shows **deployed practice or a documented incident** affected, with a source. A citation count or a market trend alone is weak. |
| 3 | What is still unknown after the closest prior work? | Names the **closest 2–3 works** (verified) and states the specific question they leave open. "Nobody has combined A and B" is weak unless the combination changes a result. |
| 4 | What exactly is my threat model, and is it realistic? | States capabilities, knowledge, goals and **what the attacker cannot do**. Realism is argued from a real delivery channel or incident. **A defence paper must include an adaptive attacker who knows the defence**, or it is at most weak. |
| 5 | What variable am I actually studying? | One **independent variable** (what you manipulate) and one **dependent variable** (what you measure), with the confounds held fixed. More than one manipulated factor must be a stated factorial design. |
| 6 | What evidence would prove or falsify my claim? | A **pre-stated outcome that would refute the claim**, with a threshold. A claim with no possible refuting result fails. |
| 7 | Are my metrics measuring security, or merely a proxy? | The primary metric is an **attacker-outcome quantity** (e.g. attacks that get through, measured on the real system), or the proxy's link to that outcome is shown. Accuracy / F1 on a benchmark alone is a proxy. |
| 8 | What alternative explanation could produce my result? | Names at least **two concrete alternatives** (e.g. dataset artefact, circularity between method and benchmark, tuning on the test set, a weak baseline) and the control that rules each out. |
| 9 | How realistic is my experimental environment? | Compares the environment with deployment on **traffic/telemetry source, scale, attacker behaviour and engine**, and states each known gap. |
| 10 | What result would still be interesting if my hypothesis is wrong? | Names a **negative or null result that is still publishable**, and why. "We would learn something" is weak. |
| 11 | What will the security community know after this paper that it did not know before? | One or two **falsifiable statements** of new knowledge, not a list of artefacts built. |
| 12 | What are the three strongest reasons a reviewer could reject this paper? | Three **distinct** reasons, ranked, each with a pre-emption that is concrete enough to schedule. |

## Verdict rules (applied after resolution in step 6)
- **stop:** Q1, Q3 or Q11 is `fail`. There is no clear problem, no gap, or no new knowledge.
- **revise:** any other `fail`; or Q4, Q6 or Q7 is `weak`; or three or more questions are `weak`.
- **go:** everything else.

Q12's reasons and every `weak`/`fail` row must each produce at least one action in the report.
