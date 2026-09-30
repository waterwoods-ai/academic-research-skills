# ChatGPT operating notes (chatgpt.com in Chrome)

Tags: **[live]** = seen in the browser (2026-09-27 unless dated), **[verify]** = assumed, confirm on first use and update this file.

## Access
- Use the headed `research-scout` Chrome profile, the same gate as `find-research-topic` step 0 (`browser_mode` must report `"headless": false`; it has silently reverted to headless several times). No Cloudflare challenge appeared in headed mode [live].
- **The user logs in themselves.**
  - Logged-out signal: several "Log in" / "Sign up for free" buttons. A guest composer still shows, so don't use the composer as the login check [live].
  - Logged-in signal: no login buttons, and a `button[aria-label="Open profile menu"]` [live].
- The start page shows suggestion cards drawn from the user's **ChatGPT memory**. Temporary Chat keeps that memory out of the run. Never record what the cards say.

## Starting a clean chat
- **Open `https://chatgpt.com/?temporary-chat=true`** for each pass [live]. It is the simplest way to get a fresh Temporary Chat. Alternatively, click `button[aria-label="Temporary chat"]` on the start page.
- **Confirm Temporary Chat is on before pasting.** Any one of these is enough, and all three were seen [live]:
  - the URL contains `temporary-chat=true` (it stays on after the chat gets a `/c/<id>` URL);
  - the toggle's label reads "Turn off temporary chat";
  - the page heading reads "Temporary chat".
- **Model:** `button[aria-label="Select ChatGPT model"]`; its text is the current model (it showed "Instant"). Record it. **Ask the user before switching** to a reasoning model or to Deep Research or agent mode, because they are quota-limited.

## Sending a long prompt
- **Composer:** `div.ProseMirror[contenteditable=true]` (placeholder "Ask ChatGPT"), inside a `form` [live]. `#prompt-textarea` did **not** exist.
- **Enter sends**, so never use the `type` action for multi-line text. Insert it as one edit [live, 4-line test]:
  ```js
  (() => { const el = document.querySelector('.ProseMirror');
    el.focus(); document.execCommand('insertText', false, TEXT); return el.innerText.length; })()
  ```
  - Replace `TEXT` with a JS string literal of the approved brief (escape quotes and backslashes; `\n` becomes a paragraph).
  - Each line becomes its own `<p>`, and nothing is sent. `innerText.length` comes out slightly above the source length, about +1 per line break, so compare lengths approximately.
- **Send:** click `button[aria-label="Send"]` [live]. It has no `data-testid`.

## Knowing the answer is finished
- **While generating,** Send is replaced by `button[aria-label="Stop"]` [live].
- **Finished** = `button[aria-label="Stop"]` is gone, `button[aria-label="Send"]` is back, and the last reply's text has stopped changing [live].
- **Poll with short `eval` calls** (one check per call, about 10 s apart). A single eval that loops for 45 s died with `Page session timeout: Runtime.evaluate` [live].
- **Messages** [live]; `[data-message-author-role]` does **not** exist:
  - user turns: `[data-user-message-bubble="true"]`;
  - assistant replies: `[data-markdown-text-style="assistant-message"]`. Read the **last** one's `innerText` and save it verbatim.
  - Turn containers carry `data-content-search-unit-key="…:N:user"` / `"…:N:assistant"` if you need ordering.
- **"Continue generating"** did not appear for a 120-line reply [live]. If it appears on a long review, click it and re-read [verify].

## Observed changes
<!-- Append dated notes when the live UI differs from the above. -->
### 2026-09-27 — first live checks
- **Logged out:** the first auto-capture after opening the tab timed out (`Page.captureScreenshot`); a plain `eval` right after worked. The page is heavy on first load, so wait before acting.
- **Logged in, Temporary Chat, harmless test prompts only.**
  - A 4-line message was inserted via `execCommand` and sent as one turn. ChatGPT answered "3", which was correct, confirming no early Enter.
  - A "count to 120" prompt showed the Stop button mid-answer and a clean 120-line finish.
  - Several guessed selectors were wrong: `#prompt-textarea`, `data-testid="send-button"`, `data-testid="stop-button"`, `data-message-author-role`. The live ones are above.

### 2026-09-27 — first real run (two passes, Latest / Extra High, Temporary) [live]
- **Model menu:** the button text shows the *effort* ("Extra High"), not the model name. The menu lists the effort level, then "Latest", "GPT-5.6 Sol", and older models. Model items open nested effort submenus: one agent click switched the user's effort from Extra High to High. **Don't click it; the user sets it.**
- **Changing the model can drop Temporary Chat** (the URL reverted to plain `chatgpt.com/`). Re-check the Temporary signals after any settings change.
- **Other tabs steal focus.** A user-started claude.ai sign-in and a Google OAuth popup became the active tab mid-run, and claude.ai also has a `.ProseMirror` composer. The hostname guard in every paste step caught this twice. `switch_tab` needs a URL or title substring, not a tab id.
- **Thinking shows as interim blocks.** While Extra High is thinking, several `[data-markdown-text-style="assistant-message"]` blocks appear with progress text. They collapse into one answer block once writing starts. **Read only after `Stop` is gone and `Send` is back.**
- **Timing:** both passes took about 4–5 min at Extra High. Running the two passes in **two tabs at once works**; the background tab finished and its DOM held the full reply without a reload. **Don't reload a Temporary Chat** to refresh it, because it may not come back.
- **Saving long replies:** extract from the auto-captured `NNN-eval.html` snapshot (parse the assistant-message element) instead of returning 20k+ characters through `eval`. Then compare the head and tail with a short `eval` to confirm nothing was cut.
