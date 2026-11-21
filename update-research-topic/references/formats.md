# Formats: watch profile and update report

## `topic_watch.json` (project root)

```json
{
  "topic": "one line naming the topic",
  "core_claim": "the core claim from the gap card; for the reader, never sent to a service",
  "ring": ["claims that may be cut"],
  "queries": [
    {"id": "topic", "text": "keywords of the topic", "why": "the topic's own vocabulary"},
    {"id": "alt-control", "text": "the control community's name", "why": "alternative name"},
    {"id": "ancestor", "text": "the problem without today's buzzwords", "why": "deep-dive query"}
  ],
  "seeds": [
    {"id": "10.1145/1234567.1234568", "role": "closest"},
    {"id": "arXiv:2501.01234", "role": "pre-mortem"},
    {"id": "10.1109/SP.2024.00012", "role": "anchor"}
  ],
  "arxiv_categories": ["cs.CR"],
  "venues": ["target venue", "venues of the closest papers"],
  "last_check": "2026-09-14",
  "log": [
    {"date": "2026-09-14", "window_start": "2026-08-01", "new": 41, "near": 2, "status": "MOVED", "run": "runs/2026-09-14-update-slug"}
  ]
}
```

Rules:

- `queries[].text` holds keywords only: short, in public vocabulary. A query of more than about six words returns little; split it.
- `seeds[].id` is a DOI or an arXiv id. Role `closest` also turns on the author watch for that paper.
- `last_check` is the date of the last completed run, or of the gap deep-dive before the first run. It moves only when a run finishes with its report written.
- `core_claim`, `ring`, `venues` and `log` are read by people and by the agent; the sweep script uses `queries`, `seeds`, `arxiv_categories` and `last_check`.

## `ledger.md` (run folder)

One line per search, including the ones that returned nothing:

```
<date> | <index or site> | <query or seed> | window <from> | returned <n> | new <n> | near <n> | note
```

Screening labels follow, one line per new record: `<id> | <title> | unrelated / background / near | reason in a few words`.

## Overlap card (run folder, one per near paper)

Use the card of `security-track/references/paper_dissection_protocol.md` § Overlap perusal, and end it with:

```
version read: <venue version or arXiv vN, date>
touches: <which of our claims: core / ring item / baseline / none>
their evidence: systems <...> | scale <...> | threat model <...> | baselines <...>
ours on the same rows: <from evidence_bar.md>
outcome: NONE | COMPARE | USE | RING | PARTIAL | FILLED
what remains ours: <the part of the claim their paper does not deliver, or "nothing">
```

## `update.md` (run folder)

1. **Status:** `CLEAR` / `MOVED` / `CONTESTED` / `OVERTAKEN`, in one sentence, with the search it rests on (queries, indexes, window, date).
2. **Near papers:** table: paper (title, date, id, version read) | touches | outcome | what changes for us.
3. **Changes made to the project files:** baselines added, scope ledger entries, registry line.
4. **What the project must do before the next gate.**
5. **Decision for the PI,** if the status is `CONTESTED` or `OVERTAKEN`: the options (continue with the difference in evidence as the contribution, re-centre on what remains, replace the gap, stop), each with its cost.
6. **Pace:** near papers per window, this run and the earlier ones.
7. **Search record:** counts per source, sources that gave no answer, what was not searched and why.
8. **Next look:** the date, 30 days on or the next trigger if sooner.
