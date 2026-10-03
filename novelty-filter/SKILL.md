---
name: novelty-filter
description: This skill should be used when the user gives a paper (PDF path, DOI, arXiv id or URL) and asks to "find the gap in this paper", "extend this paper", "what could I build on this paper", "find problems with the authors' method", "improve on this method", "is this idea already published", "novelty-check these ideas", or "check nobody else is working on this method". Builds a confirmed limitation list for one paper (own read + ChatGPT/Claude.ai Projects in Chrome), maps references, citing work and related work (Elicit, Litmaps), and filters candidate improvements against prior work with an open / narrow / saturated verdict. A filter, not a generator - it does not develop a method; to generate and formalize one use novelty-engine. Not for plain summaries.
argument-hint: "<paper: PDF path | DOI | arXiv id | URL> [field / constraints]"
metadata:
  version: "1.0.0"
  last_updated: "2026-10-06"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - security-track
    - find-research-topic
    - verify-research-topic
    - novelty-engine
---

# Novelty Filter: one paper's limitations, and whether an improvement is already published

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

Take one paper. Find what is wrong with it or missing from it, confirm those weaknesses against the text, collect candidate improvements that remove them, and check whether each is already published. This skill does not develop a method: it produces no formal specification, no code and no experiment.

**Stance.** The weaknesses are inputs to an improvement, never the contribution. The output is a better method built on the paper, which is cited as the baseline to beat; it is not a paper about the authors' faults.

**What this skill is, and is not.** It is a reliable novelty *filter*, not an idea *generator*. The candidates it drafts itself in step 6 are the obvious improvements, and on a recent, heavily-followed paper those are usually already published (in two real runs on such papers, no candidate came back `open`). For real generation use the sibling [novelty-engine](../novelty-engine/SKILL.md) skill (one mode breaks a shared assumption and imports a mechanism from a distant field; the other takes this skill's `weaknesses.md` and proposes mechanisms that remove the limitations' causes), then bring its candidates here to be filtered.

**Reuse the sibling skills' operating notes.** Read the notes for a tool before touching it:
- Chrome gate, Elicit, Litmaps: [find-research-topic](../find-research-topic/SKILL.md) step 0, plus [elicit.md](../find-research-topic/references/elicit.md) and [litmaps.md](../find-research-topic/references/litmaps.md).
- ChatGPT composer mechanics: [chatgpt.md](../verify-research-topic/references/chatgpt.md).
- Projects on ChatGPT and Claude.ai: [references/llm-projects.md](references/llm-projects.md).
- Prompt texts P1–P4: [references/prompts.md](references/prompts.md).
- Critique lens, candidate spec, novelty verdicts, scoring: [references/critique.md](references/critique.md).

Load `superpowers-chrome:browsing` if it is not in context.

## Hard rules
1. **Approval before anything unpublished leaves the machine.**
   - The public paper and prompts P1–P3 need **one** approval, together with project creation.
   - **P4 contains the user's unpublished method ideas.** Show its exact text and send nothing until the user says yes.
   - **Novelty-search queries are exempt.** Short search phrases (up to 6 words for Litmaps, one question for Elicit) are how prior work is found. Never paste a full candidate spec into a search tool.
   - If the paper itself is unpublished (under review, or the user's own draft), ask before uploading it anywhere.
2. **Never paste** credentials, file paths, hostnames, private data or Zotero contents. The user logs in to every site themselves.
3. **Never click model or effort menus.** The user sets the model and effort in each project. Read the button text only, and record it.
4. **Create; never modify.**
   - New Projects, Elicit sessions and Litmaps are named `novelty-filter <YYYY-MM-DD> <slug>`.
   - Never edit or delete the user's existing ones.
   - Ask before paid usage (Elicit Reports or Research Agent on Smartest) and before anything outward-facing (share links, Monitor).
5. **LLMs never adjudicate.**
   - A weakness counts only once it is checked against the paper text (§ / Eq. / Tab.).
   - A paper an LLM names counts only once Elicit (`+title:"…"` / `+doi:"…"`), a Litmaps search, or the publisher/arXiv page confirms its title, authors and year. Otherwise list it as `claimed by <tool>, not found`.
6. **Blind first.**
   - Freeze `analysis.md` before any LLM pass.
   - P1–P3 carry nothing from it.
   - Claude.ai shares the agent's model family, so only ChatGPT agreement counts as independent confirmation.
7. **Never claim "nobody works on this".** State what was searched, where, when, and that nothing directly matched.

## Run folder
`RUN=runs/<YYYY-MM-DD>-method-<slug>`.

| File | Contents |
|---|---|
| `paper.pdf`, `paper.txt` | The paper and its text |
| `analysis.md` | Your read, frozen at the end of step 2 |
| `references.md` | The paper's bibliography, parsed from `paper.txt` |
| `citing.md` | Follow-up work found in Litmaps and Elicit (step 2) |
| `candidates.md` | Draft candidate specs (step 6); P4 is built from it |
| `ledger.md` | Every query, URL and date, and the papers kept, appended as you go |
| `chatgpt-p1-3.md`, `claude-p1-3.md`, `chatgpt-p4.md`, `claude-p4.md` | Transcripts, verbatim |
| `weaknesses.md` | The confirmed weaknesses table |
| `method-proposal.md` | Final output |

The ledger survives context compaction; anything not written there is lost.

## Flow

### 0. Intake and gates
1. Resolve the paper to a PDF in `$RUN/paper.pdf`: the local path, arXiv `/pdf/<id>`, or an open-access link.
   - Paywalled: ask the user for the PDF.
   - Extract the text to `paper.txt` (`pdftotext -layout`, or the `pdf` / `markitdown` skills).
2. Ask only what is missing:
   - the field;
   - the user's compute and data (default compute: gpu1);
   - the time horizon;
   - any direction the user already favours. Record it, but keep it out of P1–P3.
3. Run the Chrome gate (headed `research-scout` profile, 1440×900).
4. Open four tabs: Elicit, Litmaps, chatgpt.com and claude.ai. Check each is logged in. If one is not: "please log in to X, then reply 'done'".

### 1. Close read
Write `analysis.md` using items 1–8 of the critique lens in [references/critique.md](references/critique.md) §1. Cite a paper location for every point. Item 9 is written in step 2.

### 2. References and follow-ups (paper text + Litmaps + Elicit)
1. **References.** Parse the bibliography from `paper.txt` into `references.md` (title, year, and a DOI or arXiv id where printed). Tag each entry `baseline` (compared against in the experiments), `foundation`, or `related`.
2. **Litmaps map.** Follow [litmaps.md](../find-research-topic/references/litmaps.md).
   - Bulk import the target's DOI (or arXiv id) plus up to 14 `baseline`/`foundation` references that have identifiers. Add any reference without one by title search.
   - Check that the target paper appears under **Results**, not **Missing**.
   - Run **Explore** with *Shared Citations & References*. Write the list to the ledger.
3. **Follow-ups (`citing.md`).** Anyone improving this method almost certainly cites it.
   - **Litmaps:** on the map, click **MORE RECENTLY PUBLISHED** and set the date filter to "Since {current_year-2}". Take papers newer than the target that are linked to it.
   - **Elicit:** run a Find papers query: "Which papers extend, improve on, or critique <title> (<year>)?" with `+year:>{target_year}`. Add the column `Builds on <short name>? (yes/partial/no)`.
   - Skim both for anyone already fixing the same weaknesses.
4. **Reference audit.** Write item 9 of the critique lens in `analysis.md`, then **freeze it**. From here on, corrections go in `weaknesses.md`.
- **Coverage is partial.** IEEE-heavy reference lists often have no links in Litmaps' metadata. An empty list is a lead, never evidence.

### 3. LLM projects (ChatGPT + Claude.ai)
1. **Show the user once and get one yes for all of:** the project name, the instructions block, P1–P3 and the fact that the PDF will be uploaded.
2. **Create one Project on each site.** Upload the PDF, set the instructions and ask the upload check. Details are in [references/llm-projects.md](references/llm-projects.md).
3. **Ask the user to set the model and effort in each tab.** Record the button text.
4. **Send P1, P2 and P3 in one chat per tool,** in order, each after the previous reply finishes.
   - Run both tools in parallel tabs.
   - Every paste is guarded by the hostname and project check.
5. **Save each reply verbatim** to the transcript files.

### 4. Landscape: Elicit + Litmaps
**Elicit.** Follow [elicit.md](../find-research-topic/references/elicit.md). Use one Find papers message per query, with the columns and the paper target in that message.
- **Problem query:** the paper's research question, `+year:>{current_year-3}`. Columns: `Limitations`, `Future research`, and `Addresses <paper short name>'s weakness? (which/no)`.
- **Method-family query:** the generic family of the paper's method, regardless of domain. This catches work that domain-phrased queries miss.

**Litmaps** (on the step 2 map).
1. Switch Explore to *Similar Text*. Papers close in meaning to the target but not linked to it by citations are candidate bridge ideas. Budget for Similar Text failing.
2. Set the axes to Momentum × Map Connectivity and screenshot.

Log every kept paper in the ledger with title, year, DOI and why it was kept.

### 5. Confirm weaknesses
Merge `analysis.md`, the P2 answers from both tools, the Elicit Limitations columns and the reference audit into `weaknesses.md`, following [references/critique.md](references/critique.md) §2.
- Check every item against `paper.txt` and give it a status.
- Verify every paper either tool named (rule 5).
- Mark the items raised by both you and ChatGPT as high confidence.

### 6. Collect candidate improvements
1. **Write the candidates into `candidates.md`** with the spec in [references/critique.md](references/critique.md) §3. Take first the ones the user or `novelty-engine` already produced; if there are none, run `novelty-engine`'s limitation-driven mode on `weaknesses.md`, or draft 2–4 quick ones here if that skill is not available. Each must remove at least one `confirmed` weakness.
2. **Draw on every idea source:** P3 answers, Litmaps bridges (Similar Text neighbours the paper never cites), stale foundations, and methods from the adjacent community. Record each candidate's source.
3. **Prefer mechanism changes over "same method, new domain".** A domain transfer alone is at most `narrow`.

### 7. Novelty check (every candidate)
1. **Run checks (a)–(d)** (check (e) is P4, next) from [references/critique.md](references/critique.md) §4.
2. **Write P4** from `candidates.md` and **get the user's approval of the exact text** (rule 1).
3. **Send P4 in a new chat inside each project.**
4. **Verify every paper P4 names.** Assign the verdict `open`, `narrow` or `saturated` with the justifying papers, and log it in the ledger.
5. **Sharpen or drop.** A `narrow` candidate gets one sharpening round: change the mechanism, then re-run all of (a)–(e), with P4 in a new chat and approved again. A `saturated` candidate is dropped.

### 8. Report
Score the survivors with §5 of the critique reference. Write `method-proposal.md`:
1. **Paper summary:** the claims, and the method in five lines.
2. **Confirmed weaknesses:** the table from `weaknesses.md`, sorted by severity.
3. **Ranked candidates:** a table with columns candidate | score | weakness removed | verdict.
4. **Per candidate:** the full spec, the closest existing work and how the candidate differs, the novelty evidence (queries, tools, date), the P4 attacks and the answer to each.
5. **Recommended next step:** hand the top surviving candidate to `novelty-engine` Phase 4 for formalization (definitions, assumptions, algorithm, a theorem or bound), then the minimal experiment, with its compute target.
6. **Record:**
   - the model and effort used in each tool, and the project URLs (private);
   - the Elicit session URLs and the Litmap URL;
   - the list of `claimed by <tool>, not found` papers;
   - the limits of the scan (missing citation metadata, preprints and in-review work are invisible, plan limits).

Then, in chat, give the top candidate, its verdict, the single biggest risk and the report path.
Append any UI differences to the matching reference's "Observed changes", with the date.

## Common mistakes
| Mistake | Fix |
|---|---|
| Reading the ChatGPT/Claude critique before writing your own | Freeze `analysis.md` first |
| P1–P3 hint at your suspected weakness | Send the prompt texts verbatim; no hints |
| Treating Claude.ai agreeing with you as confirmation | Only blind ChatGPT agreement is independent |
| A candidate with no confirmed weakness behind it | Drop it or find the weakness first |
| "No results" from one tool taken as "novel" | Run all of (a)–(e); word the verdict as searched-and-not-found |
| Pasting P4 before approval | P4 carries unpublished ideas; approve the exact text first |
| Target lands in Litmaps "Missing" and you carry on | Re-add it by arXiv id or title search before exploring |

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 1.0.0 |
| Last Updated | 2026-10-06 |
| Maintainer | Tom |
| Dependent Skills | novelty-engine, security-track |
| Role | One paper's confirmed limitations and a novelty check of candidate improvements |
