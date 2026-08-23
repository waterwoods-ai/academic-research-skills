# Security Framing Protocol (Custom — Security Track)

> The entry gate for any research idea targeting a security venue. Runs at
> S0/S2/S3 and whenever a new idea appears. Answers ONE question before any
> writing begins: **Why is this a security paper — and not an ML / NLP /
> networking paper with a security story attached?**

## The framing chain (fill top to bottom; a broken link is the finding)

```
System / Asset          — what exists and matters
   ↓
Security property        — confidentiality / integrity / availability /
                           authenticity / privacy (name it)
   ↓
Adversary                — who threatens the property (→ threat_model_workbench.md)
   ↓
Attack surface           — where the property can be reached
   ↓
Security failure         — what breaks when the adversary acts
   ↓
Impact                   — real-world consequence, for whom
   ↓
Existing gap             — why current work does not prevent/handle this
   ↓
Research contribution    — what this work adds
```

If any arrow does not follow, that gap is the thing to fix before writing.

## SECURITY FRAMING RISK test (run it explicitly, report the verdict)

> **Remove every security term from the contribution. Is the core still
> basically an ML / NLP / networking method?**

- If **yes** → emit `SECURITY FRAMING RISK` and stop to reframe: the paper
  will read as an applications paper with security keywords, and a Big-4
  panel will reject it on fit (rejection anchor: "engineering contribution
  without a security research question").
- If **no** → the security content is load-bearing; proceed.

## Novelty is not one thing — classify it

Tag the contribution's novelty type(s); do not conflate them:

- technical novelty · security novelty · empirical novelty
- system novelty · attack novelty · defense novelty

Three rules that catch the most common overclaims:

- a new **algorithm** ≠ a security contribution
- a higher **attack success rate** ≠ a security contribution
- a new **dataset** ≠ automatically a security contribution

## The ultimate question (the delta statement must answer it)

> **What does the security community learn from this work that it did not
> know before?**

Answer it in the community's own terms. If the honest answer is "a better
number on an existing task," the security novelty is thin regardless of the
technical novelty.

## Taxonomy & definition provenance (before you classify or define anything)

Introducing a taxonomy (D1/D2/D3…), a classification of attacks/defenses, a
named category, or a formal definition is a prime reviewer attack surface.
Before inventing one:

1. **Search** for an established taxonomy/definition in academia or industry.
2. If one exists and fits → **ADOPT and CITE it**, and map your work onto it.
   Do NOT reinvent — a self-made classification with no lineage invites
   "why this scheme, when prior work already uses Y?"
3. If established ones exist but none fits your axis → state *why* they don't
   fit, then **EXTEND** the closest one with explicit lineage.
4. Only **define your own** when none exists — and justify the gap; expect
   scrutiny.

Naming ≠ novelty: a new label on an existing category or mechanism is a
rename, not a contribution. (The same discipline for a *method* born in the
improvement or review-response loop: `method_change_provenance.md`.)

## Weak-motivation anti-pattern (do not open a paper like this)

```
AI is widely used...
However AI has security problems...
We propose XXX...
```

This is a generic template, not a motivation. A strong opening names the
specific system, the specific overlooked weakness, and why the security
community should care now. (Introduction argument structure P1–P7 lives in
`security_paper_conventions.md`.)
