# Litmaps operating notes

Sources are docs.litmaps.com (articles updated Dec 2024 – Sep 2025) and live checks on 2026-09-18.
Tags: **[live]** = seen in the browser, **[docs]** = from the docs, **[code]** = inferred from the app bundle, **[verify]** = confirm on the first logged-in run.

## Access
- **App [live]:** `https://app.litmaps.com/`. It works in guest mode for search, single-seed Explore and bulk import.
- **Logged-out signal [live]:** the left sidebar shows "Welcome! Sign up for a free account…" with "Create Free Account" and "Sign In", and a yellow banner reads "You're in Guest Mode".
- **Sign-in methods [code]:** email + password, Google, ORCID, or institutional login.
- **Plans [docs]:**
  - Free: up to 20 inputs and 100 articles per map, with only 1–2 Litmaps allowed. Keep seeds at 15 or fewer and ask before creating a map beyond the free cap.
  - Pro: unlimited, plus advanced filters and the AI "Common Topics" analysis.
- **Page furniture [code]:** reCAPTCHA v3 and an Intercom chat bubble. If a click misses, the bubble may be covering the button.

## Key URLs [live unless noted]
- Search: `https://app.litmaps.com/search?q=<text>` [code]. Or type into the search box and press Enter.
- Bulk import by DOI: `https://app.litmaps.com/import/bulk`
- Single-seed preview map: `/preview/<id>` (you land here after "Explore Related Articles")
- Saved maps: `/map/<mapId>` and `/map/<mapId>/explore` [code]

## Search [live]
- **Search box:** the main input on the home page. Type the query and press Enter. The date chips are: Most Relevant | Since 2026 | Since 2025 | Since 2022 | Custom.
- **Result rows:** `Author, Year` / Title / Venue / `N REFERENCES` / `N CITATIONS`.
- **Title search is fuzzy [live]:** "Attention is all you need" did not return the Vaswani paper. **Seed by DOI** (bulk import) instead.
- **Operators [docs]:**
  - `"exact"`, `-exclude`, `( )` for grouping, `pre*`, `|` for OR, `+` for AND
  - Search DOI and title separately.

## Seeding from Elicit (preferred path) [live]
1. Go to `/import/bulk` and set Identifier Type = DOI.
2. Type the DOIs, comma-separated, into `textarea[placeholder^="Enter DOIs"]`.
3. Click `//button[normalize-space(.)='Parse']`.
4. Check the result tabs: **Results N | Missing N | Duplicates N**. Log any Missing DOIs and add those papers by title search instead.
5. Everything is pre-selected ("N Selected"). The action bar offers **Tags** and **Litmaps**. Use **Litmaps** to add the papers to a new Litmap named `scout <date> <slug>` [verify: wording of the create-new option].
- Alternative: "Import" also accepts BibTeX, RIS and PubMed files. The ID importer also takes arXiv IDs, PMIDs and OpenAlex IDs [docs].

## Explore [live + docs]
- **Waiting:** Explore shows "Searching thousands of citations and references… N%", and free accounts sit in a "Standard Queue". It took about 1–2 min. It has finished when the pagination text `1 - N of N` appears.
- **Reading results:** the list is plain DOM text (author-year, title, venue, reference and citation counts). Buttons: "More Like This" (adds the paper as an input), "Refine Search", and at the bottom "MORE CITATIONS" / "MORE RECENTLY PUBLISHED".
- **Algorithms [docs]:** click the algorithm icon (circle-of-dots button left of the filter bar) and choose one:
  - *Shared Citations & References* (default): the most interconnected papers.
  - *Common Authors*
  - *Similar Text*: similarity of title and abstract; it ignores citations. Use it to find **disconnected neighbours**.
- **Filters [docs]:** "Filter Date, Keyword, Journal, and more…". Date and keyword filters are free; journal, h-index, SJR quartile and author filters are Pro.
- **Growing the map [docs]:** "More Like This" on a suggestion, then "Refresh", runs Explore again with that paper as an input. The ignore icon removes a suggestion.

## The map (canvas) [docs + code]
- **The graph is drawn on an HTML `<canvas>`.** Its dots are not page elements. Take data from the list or a CSV export, and use screenshots only for the shape of the map.
- **Dots and sizes:** seed papers are dark dots and suggested papers are hollow. Dot size is the log of citation count by default.
- **Axes:** click an axis label to change it. The options are Cite Count, Ref Count, Publication Date, Momentum (with a recency slider) and Map Connectivity.
- **Axis recipes [docs]:**

  | Purpose | x | y | Where to look |
  |---|---|---|---|
  | Cutting edge | Momentum | Map Connectivity | top right |
  | High impact | Date | Cite Count | |
  | Most relevant | Date | Map Connectivity | |
  | Reviews | Date | Ref Count | top left |

- **Gap guidance from Litmaps [docs]:** a gap is often two fields that do not cite each other, for example because they use different words for the same concept. Compare the Similar Text results with the citation-based results to find them.

## Export and share [docs]
- **Export:** "Articles" (top right) → "Export All" → BibTeX / RIS / CSV.
- **Image:** screenshot icon (bottom right) → Export Figure.
- **Share:** "Share" → "Share with Link" makes the map **public**, so ask first.
- **Monitor:** "Monitor" → "Enable Monitor" sends email alerts, so ask first.

## Observed changes
<!-- Append dated notes when the live UI differs from the above. -->
### 2026-09-18 — first logged-in run (Pro) [live]
- **Logged-in signal:** the sidebar shows "Default Workspace", LITMAPS, TAGS and the account email, with "Litmaps Pro" underneath.
- **After bulk import:** the "N Selected" bar has **Explore Related Articles**, which creates a *saved* map at `/map/<uuid>/explore` titled "(N articles)".
  - It once failed with "Your Litmap couldn't be generated — Failed to fetch". "Go back" and a second click worked.
  - Pro Explore takes about 10 s.
- **Algorithm menu:** real-click `[class*="DiscoverFilters__IconContainer"]` (a script-dispatched click does nothing). Wait for `//h4[normalize-space(.)='Similar Text']`, click it, then `//button[normalize-space(.)='Apply']`.
  - The Filter bar is a separate panel: year, keyword, author, journal, h-index.
  - "Advanced" is only the "Apply More Like This when tagging" toggle.
- **Similar Text is flaky:** "There were no results." on one map (twice), and it worked on another. Going to the next page runs a new search (sometimes in the Standard Queue) that can fail, so take page 1 as soon as it appears.
- **Shared Citations can return nothing** when the seeds are IEEE-conference-heavy (their reference lists are often not in open metadata). Treat that as a data gap, not a research gap.
- **Reading the list:** results are 10 per page and fill in gradually. Wait until the list stops changing, then parse with `/\n([^\n]+), (\d{4})\n([^\n]+)\n(?:([^\n]+)\n)?([\d.,k]+)\nREFERENCES?\n([\d.,k]+)\nCITATIONS?/g` (note that "1 CITATION" is singular). Next page = the last button in the parent of the "N - M of T" label.
- **Axes:** click the axis caption ("MORE CITATIONS" / "MORE RECENTLY PUBLISHED"), then `//h5[normalize-space(.)='Momentum']` or `'Map Connectivity'`. A panel opens with About / X Axis / Y Axis / Size / Advanced tabs.
- **Noise:** one seed's reference list can pull in off-topic papers (here: binary code-provenance papers and Tarjan 1972). Ignore them.
- **Keyword search for novelty checks:** `https://app.litmaps.com/search?q=<url-encoded text>` pre-fills and runs the search (confirmed). Then click `//*[normalize-space(text())='Since 2025']`.
  - Use plain phrases. Quoted or `+` operator queries returned junk (one run returned a single marine-biology paper).
  - Broad queries pull in unrelated "energy" documents.
  - Elicit is the more reliable novelty check; use Litmaps only to catch extra preprints.

### 2026-09-19 — second run [live]
- **Keyword search:** queries longer than ~6 words returned nothing. Short queries sometimes show "No results found from Google Scholar, Semantic Scholar. Trying Litmaps…" first; re-check after 10–20 s, when partial results arrive.
- **Similar Text worked on both maps this run.** It took about 10 s. Page 1 was enough.
- **Duplicate map from a failed Explore:** the "Failed to fetch" Explore on 2026-09-18 still created a map. The sidebar showed two "(10 articles)". Check the sidebar after a failure before retrying.

### 2026-09-26 — third run [live]
- **Similar Text failed again:** it stuck at "Searching… 99%" in the Priority Queue for over 2 minutes; after reloading the map it showed "There were no results." That is 2 failures in 3 runs. Budget for it failing; treat Elicit's semantic search as the text-similarity signal.
- **Keep each `eval` short on Litmaps pages.** A single eval that waited and paginated through several pages died with `Page session timeout: Runtime.evaluate`, and `await_text` did the same while Explore was running. The page does keep moving, so the timed-out eval can still have clicked "next". Parse **one page per call**, and read the "N - M of T" label to know where you are.
- **Keyword search needs a second read.** The first read after clicking "Since 2025" often returns 0 rows; re-reading 15–20 s later returned 15–17. Always re-read before recording "no results".
- **Bulk import keeps duplicate records** (e.g. 15 DOIs → "Results 20", with RulePilot and CTI-REALM twice). Harmless; dedupe when logging.
- **The citation canvas is itself a gap signal.** A screenshot of a mixed-seed map showed an older cluster with no citation links to the LLM cluster. That is a bridge-gap signal (step 4b), even when Similar Text fails.
- **The map title "(N articles)" is not click-to-edit.** No rename control was found in the time spent; log the map URL instead.

### 2026-10-06 — fourth run [live]
- **Explore card text changed:** now `refs\nREFERENCES\n[badge]\ncites\nCITATIONS\n[badge]` with extra badge numbers, so the old regex returns nothing. Parse by splitting the list text on `/\nTag\nAdd to Litmap/`, then take the first `Author, YYYY` line, the next line as title, and the line before `CITATIONS` as the count. Same split works on keyword-search results (start after the "Custom" date chip).
- **Similar Text failed again** (stuck "99% / Priority Queue (1st)" twice, including after reload): 3 failures in 4 runs. Go straight to the fallbacks; the seed-only canvas (all edges inside one cluster, other seeds isolated) was the usable bridge-gap signal.
- **Background tabs:** Litmaps search pages also fail to render when not in front (`Since 2025` chip not found). `close_tab` + `new_tab <url>` brings it front.
- **Browser WS can drop** mid-run ("Browser WS not connected") and `browser_mode` then reported `headless: true` with the same pid; a plain `eval` reconnected and the window stayed visible. Re-check visibility rather than restarting.
- **Axis panel:** clicking the bottom axis caption opens About / X Axis / Y Axis / Size / Advanced; `//h5[...='Momentum']` sets X, then click `Y Axis` text and `//h5[...='Map Connectivity']`.
- Keyword queries of 5–7 words worked this run; "time to physical impact LLM agent" returned only junk.
