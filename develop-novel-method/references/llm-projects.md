# ChatGPT + Claude.ai Projects in Chrome

Tags: **[live]** = seen in the browser, **[verify]** = assumed, so confirm on the first run and move the note to "Observed changes".

Composer, send and finished-answer mechanics for chatgpt.com are in [../../verify-research-topic/references/chatgpt.md](../../verify-research-topic/references/chatgpt.md). Read that first. This file adds **Projects** and the **claude.ai** side.

## Why Projects, not Temporary Chat
A Project keeps the paper PDF, the instructions and every pass in one place. Later passes (P4) then run against the same context without re-uploading. The cost is that chats persist in the user's account. That is why rule 1 in SKILL.md asks before anything unpublished is sent.

## Shared rules
- **Guard every paste** with a hostname check: `location.hostname === 'chatgpt.com'` or `=== 'claude.ai'`. Both sites use a `.ProseMirror` composer, and focus moves between tabs without warning [live, chatgpt.md].
- **Before pasting,** also check the page is inside the run's project: its name is visible in the header or breadcrumb.
- **Never click a model or effort menu.** Ask the user to set the model (the strongest reasoning model and effort they want) in each project's chat. Then only *read* the button text, and record it.
- **Switch tabs by URL substring** (`chatgpt.com/g/`, `claude.ai/project/`), never by index.
- **Poll with short `eval`s** about 10 s apart. Long waits inside one `eval` time out.
- **Save long replies** from the auto-captured `NNN-eval.html` snapshot, not through `eval` return values. Then compare the reply's head and tail with a short `eval`.

## ChatGPT Projects [verify]
- **Create:** sidebar → **Projects** → **New project**. Name it `novel-method <YYYY-MM-DD> <slug>`.
  - If a memory option is offered, choose **Project-only memory**. It keeps the user's general ChatGPT memory out of the analysis and this analysis out of their general memory.
- **Project page:** URL like `chatgpt.com/g/g-p-<id>/project`.
  - **Add files:** upload the PDF with `file_upload` on the page's `input[type=file]`. Only if that fails, ask the user to drag the PDF in.
  - **Instructions:** paste the project-instructions block from `prompts.md`.
- **Start a chat** from the project page's own composer, so the chat belongs to the project. The URL should stay under `/g/g-p-…/c/<id>`.
- **Upload check:** before P1, ask "List the section headings of the attached paper." If the headings are wrong or missing, the file did not attach.

## Claude.ai Projects [verify]
- **Logged-in signal:** the left sidebar shows Chats / Projects with the account name. Logged out, it redirects to `/login`. The user logs in; never type credentials.
- **Create:** `https://claude.ai/projects` → **Create project**. Enter the name `novel-method <YYYY-MM-DD> <slug>` and a one-line description, then click **Create project**.
- **Project page:** URL like `claude.ai/project/<uuid>`.
  - **Project knowledge** → **+** / **Upload from device**: use `file_upload` on its `input[type=file]`.
  - **Set project instructions:** paste the instructions block.
- **Start a chat** from the composer on the project page.
- **Composer and messages** [verify]:
  - composer: `div.ProseMirror[contenteditable=true]`;
  - send: `button[aria-label="Send message"]`;
  - while generating: `button[aria-label="Stop response"]`;
  - replies: the last element with class `font-claude-response` (fallback: `[data-is-streaming]`; finished when it is `false`).
  - **Enter sends,** so insert multi-line text with `document.execCommand('insertText', …)`, exactly as on ChatGPT.
- **Extended thinking** is a user setting next to the model menu. The user sets it; don't click it.
- **Independence caveat:** Claude.ai is the same model family as the agent running this skill. Its agreement with `analysis.md` is weak confirmation. **Only ChatGPT counts as the independent second opinion.**

## Observed changes
<!-- Append dated notes when the live UI differs from the above. -->

### 2026-09-28 — first live run (FragFuse) [live]
**ChatGPT Projects**
- Create: sidebar `button[aria-label="Add new project"]` (the "+" next to Projects) → modal "Create project". Name input placeholder is "Copenhagen Trip". Memory: a "Default memory" button opens a menu with **Project-only memory** — choose it. Then "Create project".
- Project URL: `chatgpt.com/g/g-p-<id>/project`. File input exists on the page → `file_upload input[type=file]` attached the PDF (thumbnail renders after a few s). A new chat under the project keeps the file (project-scoped).
- **Instructions UI was flaky:** the inline "Project actions" button threw "Could not open project actions"; only "Project settings"/"Pin project" showed, no instructions field surfaced cleanly. **Workaround that worked: fold the grounding instructions into the top of P1.** Model/effort selector reads e.g. "5.6 Extra High" (user-set).
- Start a new chat in the project by navigating to `/g/g-p-<id>/project` (fresh composer); send moves it to `/g/g-p-<id>-<slug>/c/<id>`.

**Claude.ai Projects**
- Create: `claude.ai/projects` → "New project" → dialog with `input[placeholder="Name your project"]` and `textarea[placeholder^="Describe your project"]` → "Create project". URL `claude.ai/project/<uuid>`.
- **PDF uploaded via `file_upload input[type=file]` lands on the COMPOSER (chat-scoped), not project Context.** It persists across P1–P3 in that one thread, but a *new* chat (P4) does not see it — re-attach to the P4 composer, or add to the right-panel **Context** ("+") for project-wide persistence. Instructions panel (right) is clean if you prefer it over folding into P1.
- Composer `div.ProseMirror[contenteditable=true]`; send `button[aria-label="Send message"]`; streaming flagged by `[data-is-streaming="true"]` / `button[aria-label="Stop response"]`; replies in `.font-claude-response` (last real block is the answer; a trailing 32-char block is the project chip). Model reads e.g. "Opus 5.5 Medium".

**Both**
- `execCommand('insertText', …)` populates both ProseMirror composers; Enter would send, so always insert then click Send.
- Save long replies from the captured `NNN-eval.html`; anchor extraction on the last line of your own prompt (echoed before the answer) to skip sidebar/nav text.
- `switch_tab "claude.ai"` matches a stale Google-OAuth tab whose URL contains claude.ai in params — switch by chat/title substring instead.
- Elicit contenteditable ignores `execCommand`? No — it worked here (`[aria-label="Research query"]`); but Enter did **not** submit, use `button[aria-label="Submit"]`. Set workflow to Find papers first: click `//button[normalize-space(.)='Research agent']` → menuitem "Find papers".
