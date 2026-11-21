---
name: update-research-topic
description: Use when the user asks to update, refresh or re-check a research topic, gap or paper idea that is already being worked on, to find out what has been published in the area since the last search, or whether someone else has already published the same idea (scooped, overtaken, concurrent work); also before a gate, before drafting, before a submission and before a resubmission.
argument-hint: "<project folder or topic> [since YYYY-MM-DD]"
metadata:
  version: "1.1.0"
  last_updated: "2026-11-21"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - security-track
    - find-research-topic
    - verify-research-topic
    - novelty-filter
---

# Update a Research Topic

<!-- routing-core:begin -->
**Step 0 — Escape hatch check (before any classification):** If the user's first message begins with `[direct-mode]` (case-insensitive byte-0 token, optionally preceded by whitespace/newlines that are stripped on parse), record this fact, strip the prefix and surrounding whitespace from the message, and skip directly to **Step 1 explicit-intent handling** on the stripped content. The literal `[direct-mode]` is NOT passed through to the dispatched agent. If the stripped message itself has no clear skill named, Step 1 falls through to Step 3 clarification (the escape hatch bypasses cross-phase clarification (Step 2), not all routing). When the token is honored and the named agent or skill needs inputs the message does not supply, read that agent's or skill's file and ask for what it requires, in its terms. Without the byte-0 token, naming an agent is not explicit intent: such a message goes through Steps 1-3 like any other, so cross-phase materials still get Step 2 clarification.

Otherwise, classify the user's input:

1. **Explicit clear intent** — user invokes a specific skill via `/ars-*` slash command, or uses an unambiguous trigger keyword that maps to a single skill (e.g., "lit-review this", "review my paper", "draft an abstract"):
   → Route directly; no clarification, no orchestrator detour.
   → The request stays explicit when the mode's usual input is absent or a word in it has other everyday senses. A revision request with no reviewer comments is revision mode's "feel certain sections need improvement" case, and "revisar artículo" is the reviewer's trigger. Route to that mode and let the mode handle what is missing; do not reopen the choice of workflow.

2. **Cross-phase materials detected** — user provides artifacts spanning ≥ 2 pipeline phases without naming a specific skill (e.g., pre-written abstract + pre-collected literature; full draft + reviewer comments + bibliography):
   → **Clarify**. Do NOT auto-route to a single-phase agent. List candidate workflows as a-d options in markdown body (NOT via AskUserQuestion tool). See `shared/references/intent_clarification_protocol.md` for the message template.
   → Reason: clarification is the safest action when materials don't unambiguously identify intent. (v3.10 active conductor (#134) will handle this via structured intake; v3.9.2 asks.)

3. **Ambiguous intent, no materials** — user provides no artifacts and no clear request:
   → Clarify per `shared/references/intent_clarification_protocol.md`.

**Screening boundary (sr-screener):** a request to screen records the user already has (database exports, pasted abstracts, full-text PDFs) against a review's eligibility criteria, or to build a screening protocol, pilot the screening, adjudicate screening conflicts, audit exclusions, or report the selection counts, routes to `sr-screener`. A request to write a literature review, or to run a systematic review, meta-analysis, or PRISMA report, does not route to `sr-screener`. Screening starts only when the user asks for it: `deep-research` `systematic-review` mode may mention `sr-screener`, but never hands over to it automatically.

**Anti-pattern (caused #133):** Receiving ambiguous cross-phase materials and silently auto-routing to a single-phase agent based on which phase the materials "look closest to." This bypasses orchestrator-level reconciliation and lets the subagent inherit the full ambiguity without independent oversight.

**Security-first default (this suite):** every research or paper task targets a security venue — the Big 4 (IEEE S&P, NDSS, ACM CCS, USENIX Security) or a tier-2 venue — unless the opt-out rule in the `security-track` skill (§ Activation) holds. Before configuring any ARS skill or agent for such a task, load `security-track` and apply its § Overrides of stock ARS defaults: IEEE/ACM numeric citations instead of APA 7.0; the security chapter structure with an explicit Threat Model and Ethics Considerations instead of IMRaD, sized by the venue's page limit; the five security reviewer personas with the target venue's decision vocabulary; double-blind anonymity; and conference deadlines only from its `deadlines_current.md`.
<!-- routing-core:end -->

Find out what appeared in the topic since the project last looked, read the papers that come close, and say what each one does to the project's gap and claims.

**Place in the workflow.** `find-research-topic` finds the gap before the work starts and `verify-research-topic` checks the idea before the project commits to it. Both are a picture of the literature on one date. A project then runs for months while other groups publish. This skill is the repeat look during the work: it reuses the searches the project already ran, limited to the time since the last look, and feeds the result into the gap registry, the evidence bar and the direction check (`security-track/references/gap_deep_dive_protocol.md` Parts A to C).

- Watch profile and report formats: [references/formats.md](references/formats.md)
- Sweep script: `scripts/sweep.py` (OpenAlex and arXiv, standard library only)
- Elicit API client, in the sibling skill: `find-research-topic/scripts/elicit_api.py` (`check`, `search`)
- Tool notes for Elicit and Litmaps: `find-research-topic/references/elicit.md`, `find-research-topic/references/litmaps.md`

## When to run

| Trigger | Why |
|---|---|
| **30 days** since the `last_check` of an ACTIVE project | preprints appear every week; a month is the longest a project should work without looking |
| Before Gate 1, before the build starts, and before every direction check | a GO given on an old picture of the literature is not a GO |
| When the headline result exists, before drafting | the related-work and baseline sections are written from the current state |
| In the **7 days before a submission** | reviewers know last month's preprints |
| When a real review comes back, and before a resubmission | reviewers name the papers the project missed; months have passed |
| After a Big-4 or tier-2 venue publishes its accepted-paper list or program | accepted papers are visible there weeks or months before any index has them |
| Whenever someone mentions a paper that sounds close | read it now, with the overlap card, not at the next scheduled look |

The first run on a project starts its window at the date of the gap deep-dive (or, without one, at the date of the project's last literature search).

## Hard rules

1. **A paper changes the project only after its perusal.** Title and abstract select what to read. The effect on a claim is decided from the full text with the overlap card (`security-track/references/paper_dissection_protocol.md` § Overlap perusal). When the full text cannot be obtained, write `not perused: <reason>` and treat the paper as an open risk, not as cleared.
2. **Only papers seen in a tool enter the report,** with title, date and DOI or arXiv id. A paper someone mentioned is looked up first.
3. **"Nothing new" is a statement about a search.** Write it as "no new work that touches the core claim in N queries across <indexes>, window <from> to <date>". A request that failed is no answer; it is not zero results. Papers under review and unindexed preprints are invisible to every tool.
4. **Queries are keywords and alternative names.** Never paste the project's unpublished claim, abstract, results or draft text into a search service or an LLM tool.
5. **Preprints count.** A reviewer who has read an arXiv paper will raise it. Record its version and date. Whether a venue treats it as concurrent work comes from that venue's call for papers, never from memory.
6. **The verdict on the topic is the PI's.** Claude reports, Codex checks every overlap card with outcome PARTIAL or FILLED, the PI decides. Do not continue building on a claim marked PARTIAL or FILLED while the decision is open.
7. **Ask before anything paid or outward-facing:** Elicit paid runs, Litmaps Monitor, Elicit Alerts (rules of `find-research-topic`). Never delete or edit the user's existing maps, tags or collections.
8. **Do not weaken the claim to keep it.** A new paper that covers part of the claim leads to a logged scope change with its evidence (`gap_deep_dive_protocol.md` Part B), a direction check, or a replacement gap. Rewording the claim so that the new paper no longer touches it is none of these.

## Files

- `topic_watch.json` in the project root: the watch profile (what to search, which papers to follow, when the last look was). Format in [references/formats.md](references/formats.md).
- `RUN=runs/<YYYY-MM-DD>-update-<slug>` under the project root: `sweep.json`, `sweep.md`, `ledger.md` (every query with its index, date and counts, including the ones that returned nothing), the overlap cards, and `update.md` (the report).

## Flow

### 1. Load or build the watch profile

Read `topic_watch.json`. If the project has none, build it from what the project already holds, show it to the user and save it:

- **Core claim and ring**, from the gap card (`gap_registry.md`: `core`, `ring`) or the contribution card. Kept in the profile for the reader; never sent to a service.
- **Queries**: the topic query, each alternative name of the gap (card field `alternative names`), and the five mandatory deep-dive queries from the deep-dive ledger (ancestor, adjacent method family, other-domain same problem, grey literature, citing papers of the nearest misses).
- **Seeds**: the anchors, the three closest papers of the deep-dive (role `closest`) and the three papers of the pre-mortem. The sweep follows who cites each seed and, for `closest`, what their first and last authors publish next: the group that wrote the nearest paper is the group most likely to write the one that fills the gap.
- **Venues**: the target venue and the venues the closest papers appeared in.
- `last_check`: the deep-dive date.

A project with no gap card and no contribution card has nothing to compare new papers with. Say so and offer the gap deep-dive first.

### 2. Sweep the indexes

```bash
source ~/.venv/bin/activate
python3 <skill dir>/scripts/sweep.py --profile topic_watch.json --known literature.md gap_registry.md abandoned.md --out "$RUN"
```

It asks OpenAlex and arXiv for new papers per query, new papers citing each seed, and new papers by the watched authors, from 30 days before `last_check`, and removes what the project already holds. Read `sweep.md`: a query marked truncated is split or narrowed and run again; every error is a source that gave no answer and is run again or named in the report.

### 3. Search what the script does not reach

Log each in `ledger.md`.

- **Litmaps** (if its MCP is connected): `find_related_articles` on the seeds with `start_date` set to the window start, `strategy="citation_connected"` and again `strategy="similar_text"`. Similar text finds the paper that solves the same problem and cites none of the seeds.
- **Elicit** through its API, for every query of the profile: `python3 <suite>/find-research-topic/scripts/elicit_api.py search "<query text>" --since <window start> -n 50 -o RUN/elicit/<query id>.json`, in a login shell so the key loads. Its semantic search returns papers that share no keyword with the query, which the script's indexes miss. Drop the papers the project already holds, by DOI or arXiv id. Exit code 1 means no answer: log the query as not searched.
- **Accepted-paper lists and programs** of the profile's venues that were published inside the window: scan the titles for the topic's names. Add workshop programs co-located with those venues.
- **Grey literature**: standards and drafts, CVEs and advisories, tool and dataset repositories, vendor documentation, and talks at practitioner conferences. Security gaps are often closed by practice before a paper says so.
- **The other communities' names** (control, networking, formal methods, software engineering, HCI), when the script's queries used only the security vocabulary.

### 4. Screen

Every new record gets one label from its title and abstract, written in the ledger:

- `unrelated`: dropped, counted.
- `background`: same area, does not touch the core claim or the ring. Goes to `literature.md`.
- `near`: touches the problem, the method, the threat model, the data or the systems of the core claim or the ring.

When in doubt, `near`. The three closest records are perused even if none looked `near`, so that the report rests on at least three full reads.

### 5. Peruse the near papers

One overlap card per `near` paper, from the full text: what it claims, on which systems and data, under which threat model, at what scale, what it leaves untested. Then the outcome for each of our claims it touches:

| Outcome | Meaning | What follows |
|---|---|---|
| `NONE` | related, no claim of ours is affected | cite it |
| `COMPARE` | a method, dataset or result that a reviewer will expect us to compare with | add it to the baselines in `evidence_bar.md`; reproduce it before claiming an advantage |
| `USE` | an artifact, dataset, finding or stated limitation that helps the project | record what is used; its untested limitations are sliced like any anchor claim |
| `RING` | delivers part of the ring; the core claim stands | scope ledger entry with direction and evidence (Part B) |
| `PARTIAL` | delivers part of the core claim, or the core at smaller depth | Codex checks the card; direction check (Part C); PI decides |
| `FILLED` | delivers the core claim at comparable depth | Codex checks the card; the gap goes to `abandoned.md` with the filling paper; replacement loop (Part A3); PI decides |

"Comparable depth" is judged on the rows of the evidence bar: systems, scale, baselines, adversary. A paper that makes the same claim on weaker evidence is `PARTIAL`, and the difference in evidence is then what the project has to deliver.

### 6. State the topic's status

| Status | When |
|---|---|
| `CLEAR` | no outcome above `USE` |
| `MOVED` | at least one `COMPARE` or `RING`: related work, baselines or the ring change; the core stands |
| `CONTESTED` | at least one `PARTIAL` |
| `OVERTAKEN` | at least one `FILLED` |

Also report the **pace**: the number of `near` papers in this window and in each earlier one (from the profile's log). A rising count means the project is in a race, and the PI may move the headline date or the target venue.

### 7. Write the results into the project

- `update.md` in the run folder (format in [references/formats.md](references/formats.md)).
- `literature.md`: every `background` and `near` paper, role `update`, with the run date.
- `gap_registry.md`: one line appended to the gap's entry: `update: <date>, status, <n> near, outcomes, run <path>`.
- `evidence_bar.md`: new baselines from `COMPARE`.
- `decisions.md`: an open item for the PI when the status is `CONTESTED` or `OVERTAKEN`.
- `topic_watch.json`: new `last_check`, a log entry (date, window, counts, status), and the `near` papers added to the seeds, since they are now the nearest work.

### 8. Report

Give the user: the status in one sentence with the search it rests on; each `near` paper with its outcome and what it changes; what the project must do before the next gate; the decision that is the user's; the date of the next look.

## Common mistakes

| Mistake | Fix |
|---|---|
| "No one has published this" | State the queries, indexes and window; preprints and papers under review are invisible |
| Calling a topic overtaken from an abstract | Peruse first; abstracts overstate, and the systems and scale decide the overlap |
| Calling a topic clear because the usual query returned nothing | Run the alternative names, the citing-paper and author searches and the accepted-paper lists |
| Searching only the security vocabulary | The gap may be filled under another community's name |
| Rewording the claim until the new paper misses it | Log a scope change with evidence, run the direction check, or replace the gap |
| Ignoring a preprint because it is not peer reviewed | Reviewers read arXiv; record it and its version |
| A failed request counted as zero results | Run it again or name the source as unanswered |
| Looking only when a deadline is near | 30 days, and the events in the trigger table |
| Reading a new paper only as a threat | Record what it gives: a baseline, a dataset, a limitation to slice, evidence that the problem matters |

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 1.1.0 |
| Last Updated | 2026-11-21 |
| Maintainer | Tom |
| Dependent Skills | security-track (gap deep-dive protocol, evidence bar), find-research-topic (tool notes, ledgers) |
| Role | Repeat look at a topic during the work: what is new, and what it does to the gap |
