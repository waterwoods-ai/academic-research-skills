# Single-Paper Dissection Protocol (Custom — Security Track)

> A deep-read instrument for **ONE paper at a time**. Input is a single
> paper; output is its full dissection. This is NOT a literature review —
> for multi-paper retrieval and coverage use
> `perspective_retrieval_protocol.md`; for a light triage scan use
> `/ars-3w`. Dissection is perusal, 3w is filtering, lit-review is breadth.
>
> Method premise: dissecting 10–15 papers closest to your work, one by one,
> beats skimming 100. The cross-paper comparison matrix is what *emerges*
> after several dissections — it is not this tool's mode of operation.

## Contract: one paper in → one dissection out

### 1. The 8-question skeleton (answer for this paper)

1. **Problem** — what security problem does it solve?
2. **Motivation** — why should the security community care?
3. **Threat Model** — what does the attacker know / can do / cannot do?
4. **Assumptions** — what does the paper depend on? **Keep this separate
   from the Threat Model** — conflating adversary model with system
   assumptions is the most common ML-to-security reading error.
5. **Gap** — why can prior work not solve it?
6. **Method** — the core attack/defense idea.
7. **Evaluation** — what experiments support the claims?
8. **Impact** — real-world security consequence if the attack succeeds.

### 2. Argument-chain reconstruction

Fill the venue's canonical chain link by link, then name the weakest link.

- Attack paper: *System believed secure under X → under threat model Y an
  overlooked weakness Z exists → we demonstrate/exploit Z via method M →
  experiments show M works under realistic conditions → existing security
  assumptions need reconsideration.*
- Defense paper: *attack surface / vulnerability → existing defenses
  insufficient → proposed defense → security argument → adaptive-attack /
  robustness evaluation → utility / performance cost.*

### 3. Introduction structure (label the paragraphs)

Mark this paper's Introduction as P1–P7:
P1 Context · P2 Security Problem · P3 Existing Gap · P4 Key Insight ·
P5 Approach · P6 Results · P7 Contributions. Not every paper is exactly
seven — extract the argument structure, not the sentence patterns. The
point is to learn the *reasoning order*, then reuse it, never to copy phrasing.

### 4. Evaluation cross-examination

Turn the reviewer personas' attack list back onto THIS paper: which
questions would a Big-4 reviewer raise about its evaluation (weaker/stronger
attacker, adaptive defense, baselines, real-world feasibility, stealthiness,
cost)? List them. This trains the eye that will later defend your own paper.

### 5. One-line record → dissections.md

Append one structured row to the project's `dissections.md`:
`Paper | Venue/Year | Threat Model | Capability | Knowledge | Assumption |
Attack Surface | Security Goal | Evaluation | Limitation`. After several
dissections this file *becomes* the comparison matrix that supports a
Related Work positioning table and a precise "what is still missing"
statement — but that is a downstream by-product, produced by
`perspective_retrieval_protocol.md` when you deliberately compare, not by
this single-paper tool.

## Invocation

`Dissect this paper: <path or title> — full single-paper dissection per
paper_dissection_protocol.md`. Triggers: dissect / peruse / deep-read a
paper, 精读, 拆解这篇论文, 解剖论文.

## Human appendix — 4-week training plan

| Week | Task | Goal |
|---|---|---|
| 1 | Dissect 8–10 papers closest to your direction | threat model + framing |
| 2 | Dissect only Introduction + Threat Model of each | security storytelling |
| 3 | Dissect Evaluation; list the reviewer questions each invites | evaluation instinct |
| 4 | Re-organize your own research in the same structure | technical work → security paper |
