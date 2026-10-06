# Elicit operating notes

Sources are the Elicit help center (support.elicit.com, articles updated Aug–Sep 2026) and live checks on 2026-09-18.
Tags: **[live]** = seen in the browser, **[docs]** = from the help center, **[verify]** = not yet seen while logged in, so confirm on the first run.

## Access
- **Cloudflare [live]:** Elicit shows a "Just a moment…" check that never clears in headless Chrome. Always run headed.
- **Sign-in page [live]:** `https://elicit.com/users/auth?show=signin`.
  - Options: Email + Password, "Continue with Google", "Continue with Github", "Use single sign-on".
  - A cookie banner appears first; click "Reject Non-Essential" (or whatever the user prefers).
- **Logged-out signal [live]:** `https://elicit.com/` shows the marketing hero "AI for Scientific Research" with a Sign in link.
- **Logged-in signal [verify]:** the homepage is the app, with the Research Agent input box as the main field and a workflow dropdown next to it.
- **Remaining usage [docs]:** shown in Account Settings. One monthly pool covers Agent, Reports and Systematic Review. Find Papers and Chat keep working after the pool runs out.

## Workflows (reach them from the dropdown next to the main input, or from the left sidebar) [docs]
| Workflow | Plan | Use in this flow |
|---|---|---|
| Find Papers | all | Main tool. Returns 10 papers per page; **Load More** adds 10 at a time, up to 100. |
| Research Report | all (uses usage pool) | Optional. Use the **Research Gap Analysis** template. Takes 10–30 min and sends an email when done. |
| Research Agent | all | Avoid by default. Runs are long; Smartest/Extended Thinking uses usage. |
| Chat with Papers | all (4 papers Basic / 8 paid) | Compare the limitations of the chosen seeds. |
| Systematic Review, Extract Data, Alerts | Pro+ | Not needed. Ask before using. |

- Past work is saved as sessions under **Recents**. "Notebooks" and "credits" are old terms.

## Find Papers
- **Run and edit [docs]:** type a question (not keywords) and press Enter. To change it, click the query text, edit it and press Enter; the results are replaced.
  - Good: "What techniques allow language models to use longer context?"
  - Bad: "LLM long context"
- **Inline syntax [docs]** (put it in the query; there is no citation slider):
  - `+year:>2023`
  - `+citations:>100`
  - `+oa:true`
  - `+journal:"…"`, `+by:"…"`, `+title:"…"`, `+doi:"…"`
  - `-word` excludes a word
  - `+(citations:>50 year:>2023)` means OR
  - No quotes around `>100`.
- **Filter(s) button [docs]:** publication year, journal SJR quartile, study type (Review, Meta-Analysis, Systematic Review, RCT, Longitudinal), abstract keywords, and a **Has PDF** toggle.
- **Columns [docs]:** there is no Add Column button in the current Find Papers. Ask in the chat box instead, e.g. "Add a column: Limitations — the limitations the authors state, in ≤25 words".
  - Name each column with one phrase and write its instructions as you would for a human labeler.
  - Column limits by plan: Plus 5, Pro 20, Scale 30. The Basic limit is not documented [verify].
  - Columns read full text only when a PDF exists, so turn on **Has PDF** before relying on the gap columns.
- **Opening a paper [docs]:** click the title to open the detail view. Tables Elicit parsed from the PDF are at the bottom.
- **Export [docs]:** use the export button on the table (CSV/Excel; RIS/BIB for some tables). Needs Plus or higher. On Basic, read the table from the captured `.md` instead, scrolling if rows are virtualized.
- **Different answers between runs [docs]:** always write the query and date to the ledger.

## Research Report [docs]
1. Choose Report from the workflow dropdown, type the question, pick the **Research Gap Analysis** template and click the green arrow.
2. Choose the depth and click **Generate Report**.
3. You can leave the page while it runs. Come back through Recents.
- Export via the dropdown next to Save PDF (PDF or Word).

## Automation tips
- Selectors: Elicit class names are not stable. Use text XPath, e.g. `//button[normalize-space(.)='Load More']`, or read the captured screenshot.
- Wait for column cells to fill before extracting. Filling can take 30–90 s; empty cells or spinners mean it is still working.
- API/MCP alternative (Pro+): `https://elicit.com/api/mcp`, API keys at `elicit.com/developer`, limited to 100 requests/min. Consider it if browser driving becomes too brittle.

## Observed changes
<!-- Append dated notes when the live UI differs from the above. -->
### 2026-09-18 — first logged-in run [live]
- **Logged-in signal:** the left sidebar shows New / Search / Recents / Library / Alerts / PROJECTS, with the user's name at the bottom. The query box is `[contenteditable=true]` (aria "Research query").
- **Choosing a workflow:** click `//button[normalize-space(.)='Research agent']`, then `//*[@role='menuitem'][normalize-space(.)='Find papers']`.
  - Other menu items: Report, Systematic review, Chat with papers, Extract data.
  - After a fresh `navigate`, first `await_element [contenteditable=true]`; otherwise the menu click can land before the page is ready.
- **Find papers is now a chat plus a table.** URLs look like `/agent/<uuid>`.
  - The first answer takes about 1–2 min and auto-generates columns (Include, Focus, Relevance, plus columns tailored to the question) and a summary with citations.
  - It is finished when a "Follow-ups" block appears under the answer.
  - Follow-up requests in the chat ("Add columns … then add 15 more papers from 2023+") take 3–6 min.
- **Parallel runs:** separate tabs run independent sessions on the server. Switch tabs by title substring, because indices shift.
- **Background tabs don't render.** A tab that is not in front reports `document.visibilityState === 'hidden'`: the grid won't render new rows when scrolled, and mouse/wheel actions time out.
  - Fine for starting runs; the server keeps working.
  - To read a table: `close_tab` the background copy, `new_tab <session URL>` (new tabs open in front), `switch_tab <uuid>`, `await_text "rows · V"`, click `//*[text()[contains(., 'rows · V2')]]` to open the table panel, then run the extractor.
- **Table:** ag-grid with virtualized rows. There is a Download button above it. Abstract-only rows answer "Not stated in the available abstract." for Limitations/Future research. Read the table with this `eval`, which scrolls the grid and merges the rows:
  ```js
  (async () => { const rows = {}; const vp = document.querySelector('.ag-body-viewport');
    const grab = () => document.querySelectorAll('.ag-row').forEach(r => { const i = r.getAttribute('row-index'); rows[i] = rows[i] || {};
      r.querySelectorAll('.ag-cell').forEach(c => { const id = c.getAttribute('col-id'); rows[i][id] = c.innerText.replace(/\s*Show more\s*/g, ' ').trim().slice(0, 400);
        const a = [...c.querySelectorAll('a')].map(a => a.href).filter(h => /doi\.org/.test(h)); if (a.length) rows[i].doi = a[0]; }); });
    for (let y = 0; y <= vp.scrollHeight; y += 400) { vp.scrollTop = y; await new Promise(r => setTimeout(r, 250)); grab(); }
    return JSON.stringify(Object.values(rows)); })()
  ```

### 2026-09-19 — second run [live]
- **One message is enough.** Put the gap columns and the paper target in the first Find-papers message, e.g. `Collect about 25 papers, at least half 2023+. Include table columns "Limitations" (… max 25 words) and "Future research" (…)`. It works and saves a 3–6 min follow-up round.
- **Column keys vary in case.** The ag-grid `col-id` can be `Limitations` / `Future research` (as typed) or `limitations` / `future_research`. Match them case-insensitively, e.g. `Object.keys(row).find(k => /^limitation/i.test(k))`.
- **Asking for a custom classification column works well for novelty checks**, e.g. `"Direct match? (yes/partial/no)"` or `"Tests cross-dataset shift? (yes/no)"`. Elicit fills it per paper, and its summary states outright when nothing matched.
- **Background tabs:** the progress text goes stale, but the finished summary is readable. For the table, reopen the session with `new_tab` (see above).

### 2026-09-26 — third run [live]
- **Everything above worked as documented:** two Find-papers runs in parallel tabs, one message each with columns plus a paper target; both finished in about 2–3 minutes.
- **Tab indices shift on every `new_tab`** ("Active tab is now 0"). Once, a `switch_tab 1` landed on an Elicit session tab instead of Litmaps and the navigate replaced it. The session survives server-side, so log each `/agent/<uuid>` URL as soon as it appears, and switch by URL substring.
- **Custom classification columns can come back in a different key order** from the one requested. Match by `col-id` regex, not by position.

### 2026-10-06 — fourth run (Pro plan) [live]
- **"Find papers" moved out of the workflow menu.** The `Research agent` dropdown now lists only Research agent / Report / Systematic review. Find papers is a **chip under the input** (`//button[normalize-space(.)='Find papers']`) that inserts a "Find papers" token into the agent box; then type the question and press Enter. Mode shows "Balanced".
- **Find-papers runs draw from the paid usage pool.** After 3 runs a banner read "You've used 82% of your monthly usage limit" with "Enable extra usage" / "Upgrade to Scale". Treat each run as paid: ask before running more than the 3 framing questions, batch novelty checks (several sub-questions + one "Direct match A/B/C" column each worked well), never click "Enable extra usage".
- **Plan detection:** Settings → Subscription shows "Downgrade" on lower tiers and "Your current plan" on the active one; Zotero integration shows "Disconnect" when connected.
- **Tables can omit the year column** (FQ1 table had `name, doi, text_available, attack_vectors, physical_pathway, …` and no `year`); take years from arXiv IDs or the detail view.
- **Elicit misses some 2026 ICS papers Litmaps keyword search finds** (Shahid 2026 SOCSentinel, NRT-Bench, Gong 2026). Keep the Litmaps keyword pass in step 5.
- Runs took ~3–5 min each; all three framing runs in parallel tabs finished within ~6 min.
