# Figure template map for security papers

Use this before making or revising any figure in a security paper. Pick the row whose
scenario matches what the figure must show, then build the figure from that row's template
on the shared venue style. It overrides the stock `academic-paper` visualization agent's APA
defaults (APA captions, Arial at 3.3 in, PNG) for security venues.

## Workflow (every figure)

1. **Contract first.** Write the one-sentence claim the figure supports, the evidence each
   panel carries, and the archetype (`nature-figure` skill, figure contract). A panel that
   carries no unique evidence is dropped.
2. **Pick the row** below by the claim and the data, not by the look you want.
3. **Build on `templates/figures/sec_figstyle.py`:** `setup()`, `figure(venue, span)`,
   `series_style(i, ours=...)`, `export(...)`. The venue comes from the project anchor;
   `span="column"` for `figure`, `"page"` for `figure*`.
4. **Data only from the ledger** (`research_integrity_protocol.md`). Synthetic values only
   in demos, stamped with `mark_synthetic()`, never in a paper.
5. **Check before it goes in:** `export()` fails unless the PDF is exactly the venue width
   with embedded, non-Type-3 fonts. Then look at the PNG at final size, and at a greyscale
   copy (most readers print).

## Venue sizes (measured 2026-10-25 from the LaTeX classes)

| Venue | Class | `\columnwidth` | `\textwidth` | Body font |
|---|---|---|---|---|
| IEEE S&P | IEEEtran `[conference]` | 252.0 pt = 3.487 in | 516.0 pt = 7.140 in | Times |
| NDSS (2027 template) | IEEEtran `[conference]`, identical class file | 3.487 in | 7.140 in | Times |
| ACM CCS | acmart `[sigconf]` | 241.15 pt = 3.337 in | 506.30 pt = 7.006 in | Linux Libertine 9 pt |
| USENIX Security | usenix2019_v3.sty | 241.02 pt = 3.335 in | 505.89 pt = 7.000 in | Times |

TeX points are 72.27 per inch. Re-measure when a venue ships a new template
(`\typeout{\the\columnwidth}` in a one-line document). In LaTeX, include figures at
`width=\columnwidth` or `width=\textwidth` (`security_paper_conventions.md`); because the
PDF already has that width, nothing is rescaled and the text stays at its set size.

## Scenario → template

Templates in **bold** live in `templates/figures/` (run any of them to regenerate its
preview in `templates/figures/previews/`). The others are drawing code in other installed
skills: reuse their drawing, but create the figure with `sf.figure()` and save it with
`sf.export()`, never at their own size or as PNG only.

| # | Section | What the figure must show | Figure type | Template | Must-have rules |
|---|---|---|---|---|---|
| 1 | Intro / Overview | What the system or attack does end to end | Architecture schematic | draw.io (`drawio` skill); layout ideas in `nature-figure` Pattern 12 | Component names match the text; the attacker in the attack colour; numbered steps match the section's numbering |
| 2 | Threat model | Who the attacker is and what they control | Schematic with trust boundaries | draw.io | Trusted vs attacker-controlled parts marked, boundaries dashed; capabilities stated in the text, not only drawn |
| 3 | Design / Attack | The pipeline or algorithm stages | Flow diagram | draw.io, or TikZ for short flows | Stage names = subsection names; inputs and outputs labelled |
| 4 | Motivation / Case study | A concrete example (prompt transcript, adversarial input, packet trace) | Annotated example panel | LaTeX box (`tcolorbox`) or draw.io | Redact identifying data; mark the malicious part; say the example is real or constructed |
| 5 | Evaluation: main result | Few methods × few datasets or attacks | Grouped bars with hatch | `nature-figure` Patterns 6 + 11 (demo `figure_ImmunoStruct/plot_bars.py`); `plot-from-data` `bar_grouped_hatch` | Zero baseline; error bars with n and their definition in the caption; ours in the signal colour; hatch keeps greyscale readable |
| 6 | Evaluation: main result | Few methods × many benchmarks or attack families (≥ 5) | Radar | **`fig_radar.py`** | One 0–100 scale on every spoke, outer is better (plot 100 − ASR); no per-spoke rescaling; else use a table |
| 7 | Evaluation: robustness | ASR or accuracy against attack budget (ε, queries, poison rate, turns) | Lines with confidence bands | `plot-from-data` `line_confidence_band`; `nature-figure` Pattern 9 | Log x when the budget spans orders of magnitude; bands = CI across seeds, n stated; include the adaptive attack |
| 8 | Evaluation: detection | Detector quality at realistic false-positive rates | ROC, log FPR | **`fig_roc.py`** | Log FPR axis; AUC and TPR at the stated FPR budgets in the legend; with a low base rate, add a precision–recall curve |
| 9 | Measurement study | Distribution of a measured quantity across groups (latency, time to patch, devices per vendor) | ECDF | **`fig_ecdf.py`** | Every observation, not means; n per group; log x for heavy tails; medians marked |
| 10 | Evaluation: overhead | Runtime, memory, energy, bandwidth cost | Bars with error bars, or box plots for distributions | `nature-figure` Pattern 11; box plots drawn on `sf` | Units and hardware stated; baseline = no defense; relative overhead (%) in labels |
| 11 | Evaluation: transfer / confusion | Source × target matrix (model, dataset, device), confusion matrix | Annotated heatmap | `nature-figure` heatmap demos (`figure_RNAGenScape`, `figure_ophthal_review`) | Values printed in cells; single-hue sequential colormap, no rainbow; diagonal marked when it means same-domain |
| 12 | Evaluation: CPS attack | What the attack does to the physical process and when the defense reacts | Stacked time series with attack window | **`fig_attack_timeline.py`** | Shared time axis; attack window shaded; detection time computed from the detector data (`first_alarm`), delay labelled; thresholds, setpoints, units |
| 13 | Evaluation: ablation | Contribution of each component | Paired bars with deltas | `plot-from-data` `bar_paired_delta` | Deltas against the full system; same metric and seeds as the main result |
| 14 | Evaluation: training | Convergence or training dynamics | Line plot | `plot-from-data` `line_training_curve`; `nature-figure` demo `figure_VIGIL/plot_posttraining.py` | Smoothing stated (or raw shown faintly); seeds as bands |
| 15 | Analysis | Separation of benign and malicious samples in a representation | t-SNE / UMAP scatter | `plot-from-data` `scatter_tsne_cluster` | Qualitative only: back any separability claim with a metric; fix and state the seed |
| 16 | Measurement / SoK | Trend over time (CVEs per year, incidents per month) | Line or bar trend | `nature-figure` demo `figure_ophthal_review/plot_trend.py` | Data source and cut-off date in the caption; partial final period marked |
| 17 | SoK / Taxonomy | Categories and where prior work falls | Table first; tree only if the hierarchy is the point | LaTeX table; draw.io tree | Every category defined in the text; each work placed by a stated criterion |

No row fits: use the closest row's rules, build on `sec_figstyle.py`, and add the new
template and a row here once it has been used in a paper.

## Rules for every figure

- **Size and fonts:** the venue width from the table; text 7.5 pt (6 pt minimum) at final
  size; Arial, embedded TrueType (`pdf.fonttype = 42`), editable SVG text. Diagrams from
  draw.io: compute the final font size as the draw.io size × (column width ÷ exported width)
  and keep it at 7 pt or more.
- **Colour:** ours in the signal colour (`sf.OURS`), baselines in one neutral family,
  attacker and attack events in `sf.ATTACK`. Every series also differs by line style or
  marker, so the figure survives greyscale printing; no rainbow colormaps.
- **Honest axes:** bars start at zero; one scale per comparison; log axes labelled as
  such; no truncated axis that exaggerates a gap.
- **Statistics:** n, the centre, and the spread (and what it is) are in the caption or
  legend; a single run is labelled as a single run.
- **Captions** are below the figure in LaTeX (IEEE and ACM style), not inside the image.
  The image carries only axis labels, legends, panel tags `(a)`, `(b)`, and necessary
  in-panel labels.
- **AI-generated images:** schematics made with an image model are disclosed per the
  venue's AI policy; data figures are never generated by an image model.
