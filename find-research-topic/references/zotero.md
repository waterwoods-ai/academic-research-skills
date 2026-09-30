# Zotero operating notes (Elicit + Litmaps integrations)

Sources are the Elicit help center and Litmaps docs, read 2026-09-27, plus live checks.
Tags: **[docs]** = from the vendor docs, **[live]** = seen in this environment, **[verify]** = confirm on the first run.

The two integrations work in **opposite directions**, and that difference is the whole point of this file:

| | Elicit | Litmaps |
|---|---|---|
| Direction | **One-way import**, Zotero → Elicit Library | **Two-way sync**, Zotero Collection ↔ Litmaps Tag |
| Can it write to the user's Zotero? | **No** | **Yes.** Adding or removing an article in a synced Tag adds or removes it in Zotero |
| Plan | all plans [docs] | **Litmaps Pro** |
| Refresh | re-import the collection by hand | automatic, both ways |

## Safety rules (they extend SKILL.md hard rule 3)

1. **Never touch an existing Zotero collection through Litmaps.** Only sync to a collection **the user created for this run**, named `scout <YYYY-MM-DD> <slug>`. Litmaps cannot create Zotero collections — "Litmaps Tags can only sync to existing Zotero Collections" [docs] — so the user creates it in Zotero, empty, before step 3.
2. **Never remove an article from a synced Tag.** Removal propagates to the user's Zotero. To drop a paper, record it in the ledger instead.
3. **Never delete or rename the synced Zotero collection.** "Deleting the Zotero Collection removes all articles from the Litmaps Tag" [docs]. Deleting the Litmaps *Tag* is harmless to Zotero, but leave it: it is the run's record.
4. **Reading the user's library is fine; dumping it is not.** Read only the collection the user named. Never paste its full contents into the ledger or chat; record only the items you use.
5. Zotero items are the user's own curation. Their metadata can still be wrong, so hard rule 4 applies: cite a Zotero item only with a title, year and DOI checked against a registry or a tool page.

## Checking connection (step 0)

- **Elicit** [docs]: Settings → **Integrations** → **Connect** (log in to Zotero, "accept default permissions"). Connected = the Library shows an **Import from Zotero** button. [verify: button location on the current Library page]
- **Litmaps** [docs]: sidebar **Sync** → "Authenticate a new Zotero Account" → Zotero login → **Accept Defaults** → **Return to Litmaps**. Connected = Sync offers **"Create a new Zotero-synced Tag"**. The sidebar shows **IMPORT** and **SYNC** [live, 2026-09-26]. Changing the Zotero permissions afterwards breaks the sync [docs].
- **Local read access for the agent** [live, 2026-09-27]: Zotero desktop exposes a read-only local API at `http://localhost:23119` (HTTP 200 when the app is running). The `zotero-literature` skill's script wraps it:
  ```bash
  Z="$HOME/.claude/plugins/zotero-literature/skills/zotero-literature/scripts/zotero_api.py"
  python3 $Z find-collection "<name>"          # → collection key
  python3 $Z list-items <KEY>                  # item keys, dates, titles
  python3 $Z search-items <KEY> "<query>"
  python3 $Z export-bibtex <KEY> [out.bib]
  ```
  It cannot write. That suits verification: it lets you confirm what the Litmaps sync actually put into Zotero. If it is unreachable, ask the user to open Zotero desktop, or skip verification and say so.
  - `find-collection` does a **case-insensitive substring** match and prints each match's `Items:` count, which is the number the report needs. Always pass the full `scout <date> <slug>` name; a bare `scout` matches every run. A miss prints "No collection matching …" and exits 1 [live, 2026-09-27].
  - The local API returned all 38 of the user's collections with no `limit` parameter, so there is no pagination problem at this size [live, 2026-09-27]. Recheck if the library grows past ~100 collections.

## Elicit: importing a Zotero collection [docs]

- **How:** Library → **Import from Zotero** → choose a collection. Papers land in the Elicit Library.
- **What it is good for:** the Research Agent "searches your Library and the collections you have access to", so importing the user's prior reading lets agent runs see it. The docs do not say whether Find papers, Extract data or Chat can draw on Library papers [verify].
- **Limits, verbatim where it matters:**
  - "a one-way import, rather than a sync". New Zotero items need a re-import; items deleted in Zotero are *not* removed from Elicit on re-import.
  - "We can't import from shared Zotero collections" — group libraries are out.
  - "Nested collections are flattened out into a single list".
  - PDFs import only "when those PDFs are available for file syncing"; greyed-out attachments in Zotero's web UI will not come across. Elicit imports every PDF attachment, so the PDF count can differ from the item count.
- **Going back to Zotero:** there is no direct export. The Find papers table exports CSV / Excel / RIS / BIB, **Plus or higher**; the Library exports **RIS** only. The user then imports the file into Zotero. Offer the file; do not import it for them.

## Litmaps: syncing a Zotero collection [docs]

- **Create the synced Tag:** Sync → **"Create a new Zotero-synced Tag"** → choose the collection → **Create Tag**. Big collections "may take a few minutes to fully load". All libraries on the connected account appear in that menu, and several Zotero accounts can be connected.
- **What syncs:** adding and removing articles, and metadata edits, both ways. **Not synced:** Tag/Collection renames, notes and PDF files. Some Zotero item types never show in Litmaps.
- **Seed a map from the Tag:** open the Tag → **Explore Related Articles** at the top. This replaces the DOI bulk-import step when the seeds already live in Zotero.
- **Keep a paper:** tag it into the synced Tag from the Explore list or the map, and it appears in the Zotero collection. The Explore "Advanced" toggle "Apply More Like This when tagging" makes tagging also grow the map; turn it off if you only want to save [live, 2026-09-18].
- **Other exports:** "Export All" → BibTeX / RIS / CSV from a Litmap or Tag.

## Observed changes
<!-- Append dated notes when the live UI differs from the above. -->
### 2026-09-27 — first read of the docs
- A live check of Litmaps' Sync page did not complete: the browser tool hung for about 30 min on `app.litmaps.com/sync`. The Sync menu labels above are therefore [docs] until seen live.
