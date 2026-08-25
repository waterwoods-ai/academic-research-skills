# Knowledge Notes (L2 store) — Custom, Security Track

> Per-project retrospective takeaways distilled by the S8.5 step of
> `research_loop_protocol.md` (the L2 knowledge-evolution engine, adapted
> from AIBuildAI-2, arXiv:2605.27873). One file per project:
> `<project-slug>.md`. These are the raw, `provisional` lessons; a lesson
> confirmed by a second project is promoted into the L1 cards of
> `knowledge_index.md` with citations to both originating projects + venues.

## Why this exists

Without it, everything you learn per paper (which framing survived at NDSS,
which rejection anchor actually fired, which method was a RENAME) is lost the
moment the session ends. This store is the durable memory that makes the
security-track sharper each project instead of static.

## Takeaway file format (one per project)

```
# <Project name> — retrospective

- Venue / decision: <e.g. NDSS 2027 / Major Revision → Accept>
- Framing that survived: <the Contribution Card version that worked>
- Framings that did NOT: <and why>
- Rejection anchors that fired: <anchor # / persona, verbatim objection>
- Ruled out: <RQs abandoned; methods judged RENAME/ADOPT+CITE; evals that
  did not convince; dead-end searches>
- Subfield lesson (provisional): <subfield → candidate bar/best-practice
  row for knowledge_index.md>
- Proposed knowledge_index.md edit: <exact new row or sharpened bar —
  PROPOSED, awaiting human promotion + a second confirming project>
```

## Companion file: `abandoned.md` (per project)

The Abandoned-Approaches Ledger (S2 + S6 + S8): one running list per project
of dead ends — rejected RQs, methods ruled RENAME/ADOPT+CITE by the
provenance guard, reviewer objections already resolved — each with a one-line
reason. It stops a long engagement from re-proposing what was already killed,
and feeds the S8.5 retrospective's failure side. Lives in the project's own
tree next to `<project-slug>.md`.

## Rules

- Provisional by default; promote to L1 only on a second confirming project.
- Numbers/claims trace to the Provenance Ledger + `ars-review/` artifacts,
  never to memory (loop iron rule 2).
- Capture failures, not only successes — a dead-end is a durable lesson.
- This directory is user-owned per-project data; it is NOT shipped content.
  The plugin ships this README as the format spec; projects write their own
  `<slug>.md` files into their own working tree.
