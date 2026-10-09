---
name: find-research-topic
description: Find a novel, feasible academic research topic by driving Elicit (semantic search + gap extraction) and Litmaps (citation-network exploration) in a real Chrome window, with optional Zotero seeding and saving through their Zotero integrations. Use when the user asks to find/scout/choose a research topic, research gap, or thesis/paper direction with Elicit and/or Litmaps. It is the breadth pass of the literature stage (HOWTO Step 1a); besides the report it writes kept papers to literature.md and candidate gaps to gap_registry.md, so the systematic review (Step 1b) continues from them instead of searching again.
argument-hint: "<broad research area> [constraints]"
metadata:
  version: "1.1.0"
  last_updated: "2026-10-09"
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

You drive two web apps in Chrome through the `use_browser` tool (superpowers-chrome), then write a ranked, evidence-backed topic report.

**Place in the workflow.** This skill is the breadth pass of the literature stage (HOWTO Step 1a), used when the user has only a broad area. The depth pass (Step 1b, ARS `lit-review` on the chosen topic) continues from the files this skill writes, so the same ground is not searched twice. Always write the stage files in step 6, not only the report.
Load the `superpowers-chrome:browsing` skill first if its instructions are not already in context.

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
4. **Only cite papers you actually saw in a tool**, with their title, year and DOI. Label anything you inferred as `[inferred]`.
5. **CAPTCHA, Cloudflare, or login wall:** stop and ask the user to clear it in the window. Do not try to bypass it.

## Run folder

Set `RUN=runs/<YYYY-MM-DD>-<slug>` under the project root. Append to `$RUN/ledger.md` as you go: every query, its URL, the date, the papers kept and why. Context can be compacted, but the ledger survives. The final output is `$RUN/report.md`.

## Flow

### 0. Browser + login gate
1. Call `get_profile`. If the profile is not `research-scout`: `kill_chrome`, then `set_profile research-scout`.
2. Call `show_browser`, then confirm with `browser_mode` that it reports `"headless": false`. It reported headless at the start of both runs so far, so always check. Headed mode is required, because Cloudflare blocks headless Chrome on Elicit and the user needs a window to log in. A Chrome auto-restart (e.g. after `kill_chrome`) comes back headless, so check again after any restart.
3. Call `set_viewport {width:1440,height:900}`.
4. Open Elicit and Litmaps in two tabs and check whether each is logged in (the signals are in the references). If either is logged out, tell the user "please log in to X in the Chrome window, then reply 'done'" and wait.
5. Note each account's plan (Elicit: Basic/Plus/Pro; Litmaps: Free/Pro). The plan decides the column limits, map limits and filters in later steps. Litmaps' Zotero sync needs **Pro**; Elicit's table export needs **Plus**.
6. **Zotero (optional).** Check three things, each by its signal in [references/zotero.md](references/zotero.md):
   - Elicit is connected: the Library shows **Import from Zotero**.
   - Litmaps is connected: **Sync** offers **Create a new Zotero-synced Tag**.
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

### 3. Litmaps: citation topology
1. **Build the map.** Import the seed DOIs with Manual Bulk Import, select all, add them to a new Litmap, then run **Explore**. The default algorithm is *Shared Citations & References*. Wait for it to finish (1–3 min in the free queue).
   - **With a `scout` Zotero collection (Pro):**
     1. Sync → **Create a new Zotero-synced Tag** → choose that collection.
     2. Tag the seeds into it, which also saves them to Zotero.
     3. Open the Tag → **Explore Related Articles** to build the map from it.
     Papers you keep later go into the same Tag. **Never** sync a Tag to any other collection.
   - **Name the map after its real topic, at once.** Explore saves it as "(N articles)", which tells the user nothing. Name it for what the seed papers actually cover, as a short title a researcher would recognise: e.g. "Prompt-Injection Defenses for LLM Agents" or "Detection Deadlines for CBTC Attacks". No dates, run slugs or "scout" prefixes; the ledger keeps those. If the user already has a map with that name, add a short qualifier (the angle or the year). To rename: with the map open, hover its (highlighted) sidebar item, real-click its **⋮** button, choose **Rename**; in the **Rename Litmap** dialog select all, type the name and click **Done** (details in [references/litmaps.md](references/litmaps.md)). Renaming the run's own new map is allowed; never rename or touch other maps, and never choose **Duplicate** or **Delete Litmap** in that menu. Record the name, the map URL and the run date in the ledger.
2. **Record the Explore list** in the ledger. Use the list, not the canvas; the canvas cannot be read from the DOM.
3. **Switch to Similar Text** and run Explore again. List the papers that appear here but did not appear in step 2. These are **disconnected neighbours**: work that is close in meaning but not linked by citations. They usually come from different communities or different vocabulary, and they are the strongest bridge-gap signal.
   - Similar Text is flaky and can return "There were no results." If it fails twice, use two substitutes: the Map Connectivity axis (low-connectivity seeds are the weakly linked periphery), and papers that Elicit's semantic search returned but that are missing from Litmaps' citation list.
   - Seeds that are mostly IEEE conference papers may show no citation links at all, because their reference lists are often missing from open metadata. Treat that as a data gap, not a research gap.
4. **Look for cutting-edge papers.** Set the axes to x = Momentum, y = Map Connectivity and take a screenshot. Papers in the top right are cutting edge; recent papers in the bottom right have high momentum but few links to the map. Read titles from the list and use the screenshot only for the shape of the map.
5. **Check whether foundations have been followed up.** For 2–3 foundational seeds, use "More Like This" and "MORE RECENTLY PUBLISHED". A highly cited older paper with few recent follow-ups is a possible stale-foundation gap.
6. **Leave the map as a list.** The sidebar reopens each map in the view last used, and a map left in Explore (`/map/<id>/explore`) re-runs "Searching thousands of citations and references…" every time the user opens it. Before leaving Litmaps, open `/map/<id>` (no `/explore`) and wait until its article list has loaded; a navigation that leaves before the list appears is not remembered.

### 4. Candidate synthesis
- **What counts as a candidate:** a topic needs **at least 2 independent signals** out of:
  - (a) at least 2 Elicit papers naming the same limitation or future work;
  - (b) a bridge gap from the Similar Text disconnect;
  - (c) an emerging high-momentum cluster that has not yet been applied to the user's population or method;
  - (d) a stale foundation;
  - (e) contradictory findings across the Elicit results.
- **Output:** draft 3–7 candidates. Phrase each as a research question and tag it with its signals and evidence papers.

### 5. Novelty check (every candidate)
1. **Elicit.** Run the candidate as a Find Papers query with `+year:>{current_year-3}`. If 3 or more papers already answer it directly, it is **saturated**: narrow it (population, method or setting) or drop it.
   - **Also run an adjacent-community query.** Name the generic ML or security *method family* the candidate belongs to (e.g. "test-time adaptation", "backdoor detection", "federated learning robustness") and ask Elicit for its best-known methods and benchmarks, regardless of application domain.
     - A candidate whose only difference is "same method, new domain" or "same method, on hardware" is at most `narrow`.
     - (Lesson from the 2026-09-18 run: domain-phrased queries missed NOTE, RoTTA, SAR, TTAB, ROID, TinyTTA and FORGE.)
   - "Not found in this scan" is never evidence that nobody has done it. Write verdicts as "no direct match found in N queries", not "open".
2. **Litmaps.** Run a keyword search on the candidate with the "Since {last_year}" filter to catch preprints Elicit might miss.
3. **Ledger.** Record the verdict (`open` / `narrow` / `saturated`) with the papers that justify it.

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
  If saving was declined, offer a BibTeX file instead (Litmaps **Export All**, or Elicit's table export on Plus).
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
| Skill Version | 1.1.0 |
| Last Updated | 2026-10-09 |
| Maintainer | Tom |
| Dependent Skills | security-track (topic scouting overlay), academic-paper lit-review (stage 1b) |
| Role | Topic scouting with Elicit and Litmaps; literature stage 1a |
