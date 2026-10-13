---
name: find-research-topic
description: Find a novel, feasible academic research topic by driving Elicit (semantic search + gap extraction) in a real Chrome window and Litmaps (citation-network exploration) through its MCP server, with optional Zotero seeding and saving through their Zotero integrations. Use when the user asks to find/scout/choose a research topic, research gap, or thesis/paper direction with Elicit and/or Litmaps. It is the breadth pass of the literature stage (HOWTO Step 1a); besides the report it writes kept papers to literature.md and candidate gaps to gap_registry.md, so the systematic review (Step 1b) continues from them instead of searching again.
argument-hint: "<broad research area> [constraints]"
metadata:
  version: "1.3.0"
  last_updated: "2026-10-13"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - security-track
    - verify-research-topic
    - novelty-filter
    - novelty-engine
---

# Find a Research Topic with Elicit + Litmaps

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

You drive Elicit in Chrome through the `use_browser` tool (superpowers-chrome) and Litmaps through its MCP tools (`mcp__litmaps__*`), then write a ranked, evidence-backed topic report.

**Place in the workflow.** This skill is the breadth pass of the literature stage (HOWTO Step 1a), used when the user has only a broad area. The depth pass (Step 1b, ARS `lit-review` on the chosen topic) continues from the files this skill writes, so the same ground is not searched twice. Always write the stage files in step 6, not only the report.
Load the `superpowers-chrome:browsing` skill first if its instructions are not already in context. Litmaps needs no browser: its MCP tools are deferred, so load them in one `ToolSearch` (`select:` all `mcp__litmaps__*` tools you need) before step 3.

- Elicit operating notes: [references/elicit.md](references/elicit.md)
- Litmaps operating notes: [references/litmaps.md](references/litmaps.md)
- Zotero integrations (Elicit import, Litmaps two-way sync, local read API): [references/zotero.md](references/zotero.md)

Read the reference for a tool before touching it. When the UI differs from the notes, trust the screen: read the auto-captured `.png`/`.md`, adapt, and log the difference in the run log (step 7).

## Hard rules

1. **Never type, store, or echo passwords.** The user logs in themselves in the visible Chrome window. Session cookies persist in the `research-scout` profile, so this is normally one-time.
2. **Ask before spending paid usage or anything outward-facing:**
   - paid usage: Elicit Research Report, Research Agent on "Smartest"/Extended Thinking, Systematic Review;
   - outward-facing: Litmaps Monitor, Elicit Alerts, public share links.
3. **Never delete or edit the user's existing Elicit sessions, Litmaps, Tags, or Zotero collections.** Create new ones named `scout <YYYY-MM-DD> <slug>`, except Litmaps maps, which are named after their real topic (step 3.1).
   - **Litmaps' Zotero sync is two-way:** adding or removing an article in a synced Tag adds or removes it in the user's Zotero. Sync only to an empty collection the user created for this run, never remove articles from a synced Tag, and never delete the synced collection. Details: [references/zotero.md](references/zotero.md).
   - Elicit's Zotero import is one-way and never writes to Zotero.
   - **Litmaps MCP write tools:** use only `create_litmap` (one map per run, named by its topic), `add_articles_to_litmap` (that map only) and `add_articles_to_collection` (only the Tag the user named for this run; adding to a synced Tag also adds to Zotero). Never call `annotate_litmap` with groups (a group creates or extends a Tag, which may sync to Zotero), `update_read_later`, or `create_collection` unless the user asks.
4. **Only cite papers you actually saw in a tool**, with their title, year and DOI. Label anything you inferred as `[inferred]`.
5. **CAPTCHA, Cloudflare, or login wall:** stop and ask the user to clear it in the window. Do not try to bypass it.

## Run folder

Set `RUN=runs/<YYYY-MM-DD>-<slug>` under the project root. Append to `$RUN/ledger.md` as you go: every query, its URL, the date, the papers kept and why. Context can be compacted, but the ledger survives. The final output is `$RUN/report.md`.

## Flow

### 0. Browser + login gate
1. Call `get_profile`. If the profile is not `research-scout`: `kill_chrome`, then `set_profile research-scout`.
2. Call `show_browser`, then confirm with `browser_mode` that it reports `"headless": false`. It reported headless at the start of both runs so far, so always check. Headed mode is required, because Cloudflare blocks headless Chrome on Elicit and the user needs a window to log in. A Chrome auto-restart (e.g. after `kill_chrome`) comes back headless, so check again after any restart.
3. Call `set_viewport {width:1440,height:900}`.
4. Open Elicit in a tab and check that it is logged in (signals in the reference). If it is logged out, tell the user "please log in to Elicit in the Chrome window, then reply 'done'" and wait.
   **Litmaps through the MCP:** call `mcp__litmaps__list_workspaces` and keep the Default Workspace id. If the tools are missing or return an authentication error, ask the user to run `/mcp`, choose litmaps and authenticate, then retry. Use the browser notes in [references/litmaps.md](references/litmaps.md) only if the MCP stays unavailable.
5. Note each account's plan (Elicit: Basic/Plus/Pro; Litmaps: Free/Pro). The plan decides the column limits, map limits and filters in later steps. Litmaps' Zotero sync needs **Pro**; Elicit's table export needs **Plus**.
6. **Zotero (optional).** Check three things, each by its signal in [references/zotero.md](references/zotero.md):
   - Elicit is connected: the Library shows **Import from Zotero**.
   - Litmaps is connected to Zotero: the MCP cannot see sync status, so ask the user whether their Litmaps account has Zotero sync set up (Sync → Create a new Zotero-synced Tag in the app).
   - The agent's local read access works: `http://localhost:23119` answers, via the `zotero-literature` script.
   If one fails, run without it and say so. Zotero is never required for the flow.

### 1. Scope intake (single checkpoint with the user)
1. Ask for any of these the user hasn't given:
   - broad area;
   - discipline and methods they can use;
   - data or compute access. Ask explicitly whether they have **physical devices**; never assume a hardware testbed;
   - time horizon (course paper / MSc / PhD / grant);
   - anything to avoid, including overlap with their existing Elicit projects and Litmaps (list them from the sidebars and ask).
   - **Zotero, only if step 0.6 passed:**
     - *Prior reading:* is there a Zotero collection of papers they already know? If yes, read it with the local API (read-only). Use it to seed, and to mark candidates the user already has.
     - *Saving:* should kept papers be saved to Zotero? If yes, ask them to create an **empty** collection `scout <YYYY-MM-DD> <slug>` in Zotero now. Litmaps cannot create one, and this is the only collection the run may write to.
2. Turn the answers into **3 framing questions**, written as research questions rather than keywords. Include one "mechanism" question, one "method/measurement" question, and one "application/population" question.
3. Show the questions to the user. Adjust them once based on the reply, then proceed without asking again.

### 2. Elicit: landscape + stated gaps
For each framing question:
1. **Find Papers.** Run the question, then run it again with `+year:>{current_year-3}` to get the recent slice.
2. **Load results.** Load More until you have about 30 results, or until they stop being relevant.
3. **Add columns** (by chat, in this priority order, up to your plan's column limit):
   - `Limitations`
   - `Future research directions stated by the authors`
   - `Main findings`
   - `Methodology`
   Turn on **Has PDF** so columns read full text rather than abstracts.
4. **Record in the ledger:** each paper's title, year, DOI, citations, and a short summary of its Limitations and Future research columns.

**If the user named a prior-reading collection:** optionally import it into the Elicit Library (**Import from Zotero**), so Research Agent runs can see it. It is one-way, shared (group) collections cannot be imported, nested collections are flattened, and PDFs come across only if file-synced in Zotero. Never import into Elicit without saying so; it adds to their Library.

Then pick **8–15 seed papers** across all three questions:
- 2–4 foundational papers (high citations; use `+citations:>100`);
- 4–8 recent papers from the last 3 years;
- papers whose future-work statements point at the same open problem.

Optional, and only if the user approves the usage: a **Research Report** with the *Research Gap Analysis* template on the strongest framing question. It takes 10–30 minutes, and Elicit emails the user when it is done. Do other steps while it runs.

### 3. Litmaps: citation topology (through the MCP)
Use the Litmaps MCP tools; parameters and known quirks are in [references/litmaps.md](references/litmaps.md) § MCP. The browser steps in that file are the fallback for when the MCP is unavailable.

1. **Resolve the seeds.** `get_articles_by_doi` with the seed DOIs (up to 100 per call). Litmaps often holds one paper twice, as an arXiv record and a publisher record, sometimes under two different DOIs: deduplicate by arXiv id, then by normalised title, keeping the record that has a `referenceCount`. Log the DOIs Litmaps does not know. Keep at most 20 seeds (the Explore limit).
2. **Create the map, named after its real topic.** `create_litmap(name, workspace_id, article_ids=<seeds>)`. Name it for what the seed papers actually cover, as a short title a researcher would recognise, e.g. "Prompt-Injection Defenses for LLM Agents" or "Detection Deadlines for CBTC Attacks". No dates, run slugs or "scout" prefixes; the ledger keeps those. If `list_litmaps` already shows that name, add a short qualifier (the angle or the year). One map per run. Record the name, the `litmap_id` and `https://app.litmaps.com/map/<id>` in the ledger.
   - **With a `scout` Zotero collection:** ask the user to create the Zotero-synced Tag in the Litmaps app (Sync → Create a new Zotero-synced Tag → that collection) and tell you its name. Find its id with `list_collections`, and add the seeds, and later the papers you keep, with `add_articles_to_collection` to that Tag only. **Never** use any other Tag.
3. **Explore the connected neighbourhood.** `find_related_articles(seed_article_ids=<seeds>, strategy="citation_connected", limit=100)`, deduplicated the same way, recorded in the ledger (title, year, DOI, citations). Scores fall in a narrow band, so read the list as the connected neighbourhood, not as a strict ranking; with fewer than about 8 seeds the scores barely differ at all.
   - Seeds that are mostly IEEE conference papers may show few citation links, because their reference lists are often missing from open metadata. Treat that as a data gap, not a research gap.
4. **Find disconnected neighbours.** The same seeds with `strategy="similar_text"`. Papers that appear here but not in step 3 are close in meaning but not linked by citations. They usually come from a different community or vocabulary, and they are the strongest bridge-gap signal. Litmaps' Similar Text queue often stalls (twice for over 2 minutes on 2026-10-13; it also failed in 4 of 5 browser runs): try it once, and if it stalls, use the papers that Elicit's semantic search returned but that are missing from step 3's list.
5. **Identify the key teams.** The same seeds with `strategy="common_authors"`: the groups behind the area, for the related-work positioning and to notice when one group dominates it.
6. **Cutting edge and stale foundations.**
   - *Cutting edge:* among step 3's results from the last 2 years, rank by citations per year since publication. The MCP has no momentum or map-connectivity field, so label this ranking approximate.
   - *Stale foundations:* for 2–3 foundational seeds, `find_related_articles(seed_article_ids=[that seed], strategy="citations", limit=100)` and count the citing papers by year. A highly cited older paper with few citing papers in the last 2 years is a possible stale-foundation gap.

### 4. Candidate synthesis
- **What counts as a candidate:** a topic needs **at least 2 independent signals** out of:
  - (a) at least 2 Elicit papers naming the same limitation or future work;
  - (b) a bridge gap: a disconnected neighbour from step 3.4 (Similar Text, or its Elicit fallback);
  - (c) an emerging cluster (step 3.6's recent, fast-cited papers) that has not yet been applied to the user's population or method;
  - (d) a stale foundation;
  - (e) contradictory findings across the Elicit results.
- **Output:** draft 3–7 candidates. Phrase each as a research question and tag it with its signals and evidence papers.

### 5. Novelty check (every candidate)
1. **Elicit.** Run the candidate as a Find Papers query with `+year:>{current_year-3}`. If papers seem to answer it directly, the candidate is only **saturated-pending**: peruse the closest 1–3 of them (the overlap perusal (`security-track/references/paper_dissection_protocol.md` § Overlap perusal)) and let the overlap card decide. A paper that mentions the idea, or treats it without the depth the candidate rests on, keeps the candidate (KEEP or SHARPEN); only comparable delivery narrows or drops it.
   - **Also run an adjacent-community query.** Name the generic ML or security *method family* the candidate belongs to (e.g. "test-time adaptation", "backdoor detection", "federated learning robustness") and ask Elicit for its best-known methods and benchmarks, regardless of application domain.
     - A candidate whose only difference is "same method, new domain" or "same method, on hardware" is at most `narrow`.
     - (Lesson from the 2026-09-18 run: domain-phrased queries missed NOTE, RoTTA, SAR, TTAB, ROID, TinyTTA and FORGE.)
   - "Not found in this scan" is never evidence that nobody has done it. Write verdicts as "no direct match found in N queries", not "open".
2. **Litmaps.** To catch recent work Elicit might miss, take the candidate's 3–5 closest papers as seeds and run `find_related_articles(strategy="citation_connected", start_date=<1 January of last year>)`. Litmaps' keyword search (`search_articles`) is noisy (an irrelevant forum post ranked first on 2026-10-13); use it only as a last resort and discard rows without a DOI or venue.
3. **Ledger.** Record the verdict (`open` / `narrow` / `saturated`) with the papers that justify it, and for `narrow` or `saturated` the overlap card's path and outcome (KEEP / SHARPEN / NARROW / DROP).

### 6. Score and report
Score the surviving candidates with the rubric below. Write `$RUN/report.md` containing:
- the scope and the framing questions;
- a ranked table with columns: topic | score | signals | verdict;
- for each topic:
  - a rationale paragraph;
  - 3–6 evidence papers (title, year, DOI, and which tool they came from);
  - the closest existing work and how this topic differs from it;
  - a feasible first study design, using only resources the user confirmed. Check the proposed dataset's actual format (raw signals vs extracted features, labels, size) before building the design on it;
  - the main risk;
- the Elicit session URLs and the Litmap URL (private; do not create public links without asking);
- **Zotero, if used:**
  - the `scout` collection name, and its item count **as read back through the local API**, not as assumed from the sync;
  - any ledger paper missing from it, noted as such;
  - which evidence papers were already in the user's prior-reading collection.
  If saving was declined, offer a BibTeX file instead (Litmaps **Export All** in the app, since the MCP has no export, or Elicit's table export on Plus).
- limitations of this scan (plan limits hit, paywalled PDFs, Elicit results vary between runs).

**Stage files** (project root; append under a dated heading, never overwrite what is there):
- `literature.md`: one line per kept paper — citation, one-line finding, the candidate it bears on, the tool that found it, `source: scout <date>`.
- `gap_registry.md`: for each candidate, its gap as `status: LEAD`, with the signals, the evidence papers, and the queries and dates from the ledger. A LEAD is not yet a gap: Step 1b completes it (nearest misses and why each falls short, the security question it blocks, the ancestor and adjacent-method-family queries) or drops it with the reason.

<!-- TODO(user): define how candidate topics are scored — see "Scoring rubric" below. -->
#### Scoring rubric
Default (used until the user defines their own): score each 1–5, with equal weights.
- **Novelty:** the Step 5 verdict and how close the nearest existing work is.
- **Evidence of gap:** the number and independence of signals.
- **Feasibility:** fit with the user's methods, data and time horizon.
- **Impact:** citation momentum of the surrounding cluster.

Drop any candidate that scores 1 on Novelty or Feasibility.

### 7. Wrap-up
- Summarise the top 3 topics in chat (one line each) and give the report path.
- Give the next step: the user picks a candidate, then Step 1b runs `ars-lit-review` on it, corpus first from `literature.md`.
- Add any UI differences you hit to the matching `references/*.md` under "Observed changes", with the date, so the next run is faster.

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 1.3.0 |
| Last Updated | 2026-10-13 |
| Maintainer | Tom |
| Dependent Skills | security-track (topic scouting overlay), academic-paper lit-review (stage 1b) |
| Role | Topic scouting with Elicit and Litmaps; literature stage 1a |
