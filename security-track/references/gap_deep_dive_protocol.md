# Gap deep-dive protocol (S1.5) and scope-direction ledger

Two failures this protocol closes (Tom, 2026-11-03):

1. A gap is found only in the papers we were given, and nothing is built on it until
   it has been researched as its own topic. The corpus that revealed the gap is the
   corpus of the *topic*; the gap has its own literature, usually under other names
   and in other communities, and that literature decides whether the gap is real,
   where its edges are, and what a paper on it must contain.
2. Each review round narrows the claim. Reviewers only ever ask "didn't X do this?",
   so every round removes scope and none adds it back. After several rounds the paper
   is smaller than the gap it set out to fill. Scope must change in a logged direction
   with evidence, never by accumulation.

**Iron rule 8** (`research_loop_protocol.md`): a gap enters S2 only with status
DEEPENED; a claim's scope changes only through the scope-direction ledger, and a
narrowing closes nothing by itself: it names what replaces the removed scope.

## Part A: Gap deep-dive (between S1 and S2)

Run it for every gap the PI keeps after S1 (`gap_registry.md`, status LEAD or
GAP). Claude runs it; Codex checks the card; the PI decides what survives.

### A1. Restate the gap as a topic

Write the gap as a one-sentence research question with its own vocabulary, not the
corpus's. List three or more **alternative names** the same problem may carry in
other communities (the control, networking, database, formal-methods, HCI or
software-engineering name; the industrial name; the pre-ML name). The gap deep-dive
searches under all of them.

### A2. Search the gap, not the topic

Run `find-research-topic <gap statement>` scoped to the gap (its steps 2–7: anchors,
counter-literature, debate map, slicing), with these queries mandatory and logged in
the run ledger:

| Query | Why |
|---|---|
| **Ancestor** (no year filter, buzzwords removed) | the gap was often studied before the current vocabulary existed |
| **Adjacent method family** (the generic method, any domain) | the method that would fill the gap is usually mature elsewhere |
| **Other-domain same problem** (each alternative name from A1) | the gap may be filled under another name |
| **Grey literature** (standards, CVEs/advisories, vendor docs, tool repos, talks) | security gaps are often filled by practice before papers |
| **Citing papers of the nearest misses** (Litmaps `citations`) | whoever cites the nearest miss may have filled the gap |

Depth bar before the gap can be DEEPENED:
- at least **15 papers not in the topic corpus**, from at least **3 of the queries**
  above (fewer only if the ledger shows the queries ran and returned nothing);
- the **3 closest** papers inside the gap perused with the overlap card
  (`paper_dissection_protocol.md` § Overlap perusal), not read from abstracts;
- one **practitioner check**: does any deployed system, standard or tool already do
  this? If yes, cite it; the gap may still stand for the research question it leaves open.

### A3. Gap card v2

Append to the gap's entry in `gap_registry.md`:

```
deep-dive: <date>, ledger <path>
alternative names: <A1 list>
papers inside the gap: <n new>, closest 3 perused: <ids, overlap outcome each>
boundary: what IS done (with citations) | what is NOT done (the search that failed, queries + indexes + date)
sub-gaps: <the gap split by the evidence basis: data/sample, parameters, unit of analysis, threat model, metric>
practice: <standards, tools, products that touch it>
status: DEEPENED | RESHAPED | FILLED
```

- **DEEPENED**: the gap stands; its boundary is now known from the gap's own
  literature. S2 may generate RQs from it, and must cite the boundary.
- **RESHAPED**: the gap exists but not where the corpus put it (wider, narrower or
  shifted). Rewrite the gap statement, keep the old one beside it, and run A2 again
  on the new statement if the new one has not been searched.
- **FILLED**: the closest papers deliver it at comparable depth (overlap card). Move
  the gap to `abandoned.md` with the filling papers. The *problem* may still yield a
  gap one level up or down (iron rule 6): record that as a new LEAD.

### A4. Checks

- Codex checks each card: were the five queries run, do the 3 perusals support the
  outcome, is the boundary stated from the gap's literature rather than the topic's?
- A gap that reaches S2 as LEAD or GAP (not DEEPENED or RESHAPED→DEEPENED) is a
  protocol failure: S2 refuses it and returns it to S1.5.
- `research_question.md` (Step 4) cites the gap card v2's boundary line; the
  Contribution Card and Gate 4 cite it again as "what was unknown before".

## Part B: Scope-direction ledger (every claim change, S3 → submission)

Every change to a claim's scope is logged in `claims.md` with a direction and the
evidence that justifies it:

```
C03 | scope v1 (Gate 4): <wording> | scope now: <wording>
    | direction: NARROW | WIDEN | RESHAPE | evidence: <overlap card / ledger run / deep-dive>
    | decided by: PI, decisions.md <entry> | replaces: <limitation line, future-work claim, or new claim id>
```

Rules:

1. **Narrowing is a decision, not a disposition.** A review item never narrows a
   claim by itself. The path is: peruse the paper raised (iron rule 7) → if the
   overlap card shows comparable delivery, run the deep-dive (Part A) on the
   *objection*, because the objection may show the framing was too small rather than
   too large → the PI decides NARROW / WIDEN / RESHAPE in `decisions.md`.
2. **A NARROW names its replacement.** The removed scope becomes a Limitation line
   plus a future-work claim, or a new claim id; the removed wording goes to
   `abandoned.md` with the reason, so no later round narrows the same claim again
   for the same reason.
3. **Widening is allowed and expected.** When the deep-dive or a review round shows
   the claim covers more than the paper says (a sub-gap also closed by the evidence,
   a stronger attacker the results already withstand), log WIDEN with the evidence.
   Widening without new evidence is an overclaim; log it as REJECTED-WIDEN.
4. **Scope-drift report, every round.** With the net word change (`major_revision_playbook.md`
   §6), report the net scope change: claims narrowed, widened, reshaped this round,
   with ids. Two consecutive rounds that only narrow trigger a PI check: is the
   paper still the paper that fills the gap card v2, or has it become a corner of it?
5. **Scope-drift check at the cold read (Step 16.5).** The fresh agent compares the
   abstract's and introduction's claims with `claims.md` scope v1 (Gate 4) and the gap
   card v2 boundary, and lists every claim that is now smaller than the gap it was
   written to fill. The PI decides for each: restore (with evidence), keep narrowed
   (then the Limitations line says what is left open), or send the paper back to the
   gap.

## Who does what

| Step | Does | Checks | Decides |
|---|---|---|---|
| A1–A3 deep-dive | Claude | Codex (card) | PI (DEEPENED / RESHAPED / FILLED) |
| B1 narrowing path | Claude peruses, runs the deep-dive on the objection | Codex | PI |
| B4 drift report | Claude, each round | Codex, in the round's review | PI at two narrowing rounds |
| B5 cold-read drift check | fresh Claude subagent | — | PI per claim |
