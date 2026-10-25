"""Security-venue figure style: exact column widths, embedded editable fonts, export and checks.

Widths were measured on 2026-10-25 by compiling each venue's LaTeX class and printing
\\the\\columnwidth and \\the\\textwidth (TeX points, 72.27 per inch):
  ieee   IEEEtran [conference]: IEEE S&P; NDSS 2027 ships an identical IEEEtran.cls
  acm    acmart [sigconf]: ACM CCS
  usenix usenix2019_v3.sty: USENIX Security

Use:
    import sec_figstyle as sf
    sf.setup()
    fig = sf.figure("ieee", "column", height_in=2.2)
    ...  # draw; style series with sf.series_style(i, ours=...)
    sf.export(fig, "figures/fig_name", venue="ieee", span="column")

Run `python3 sec_figstyle.py` for the self-check.
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

PT_PER_IN = 72.27
VENUES = {  # (\columnwidth, \textwidth) in TeX points
    "ieee": (252.0, 516.0),
    "acm": (241.14749, 506.295),
    "usenix": (241.02039, 505.89),
}
ALIASES = {"sp": "ieee", "oakland": "ieee", "ndss": "ieee", "ccs": "acm", "usenix-security": "usenix"}

FONT_PT, SMALL_PT = 7.5, 6.0  # at final size; IEEE footnote text is 8 pt
OURS = "#0F4D92"                                      # signal colour for the proposed method
BASELINES = ["#7884B4", "#A8A8A8", "#484878", "#606060", "#B4C0E4"]  # one neutral family
ATTACK = "#B64342"                                    # attacker, attack window, breached threshold
GRID = "#D8D8D8"
LINESTYLES = [(0, (4, 1.5)), (0, (1.2, 1.2)), (0, (4, 1.2, 1.2, 1.2)), (0, (6, 2)), (0, (2, 2))]
MARKERS = ["s", "o", "^", "v", "P"]


def venue_key(venue: str) -> str:
    v = ALIASES.get(venue.lower(), venue.lower())
    if v not in VENUES:
        raise ValueError(f"unknown venue {venue!r}; use one of {sorted(VENUES) + sorted(ALIASES)}")
    return v


def width_in(venue: str, span: str = "column") -> float:
    col, text = VENUES[venue_key(venue)]
    if span not in ("column", "page"):
        raise ValueError("span is 'column' (\\columnwidth) or 'page' (\\textwidth, figure*)")
    return (col if span == "column" else text) / PT_PER_IN


def setup():
    # Agg keeps the exact figure width; the interactive macosx backend rounds it to whole
    # pixels at 100 dpi (a 7.140 in IEEE figure* came out 7.130 in).
    plt.switch_backend("Agg")
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": FONT_PT,
        "axes.titlesize": FONT_PT,
        "axes.labelsize": FONT_PT,
        "xtick.labelsize": SMALL_PT + 0.5,
        "ytick.labelsize": SMALL_PT + 0.5,
        "legend.fontsize": FONT_PT,
        "legend.frameon": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "lines.linewidth": 1.0,
        "svg.fonttype": "none",   # editable text in SVG
        "pdf.fonttype": 42,       # embedded TrueType, never Type 3
    })


def figure(venue: str, span: str = "column", height_in: float | None = None, **kw):
    w = width_in(venue, span)
    return plt.figure(figsize=(w, height_in if height_in else 0.72 * w), **kw)


def series_style(i: int, ours: bool = False) -> dict:
    """Ours: solid line in the signal colour. Baseline i: neutral colour, distinct dash and marker."""
    if ours:
        return {"color": OURS, "ls": "-", "marker": "D", "lw": 1.4}
    return {"color": BASELINES[i % len(BASELINES)], "ls": LINESTYLES[i % len(LINESTYLES)],
            "marker": MARKERS[i % len(MARKERS)], "lw": 1.0}


def mark_synthetic(fig):
    """Visible stamp for demo figures; real figures use ledger data and no stamp."""
    fig.text(0.995, 0.995, "SYNTHETIC DEMO DATA", ha="right", va="top", fontsize=SMALL_PT,
             color=ATTACK, fontweight="bold")


def check_pdf(path, venue: str, span: str = "column") -> dict:
    """Page width equals the venue width (within 0.5 bp) and every font is embedded, none Type 3."""
    pdf = Path(path).read_bytes()
    box = re.search(rb"/MediaBox \[\s*([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", pdf)
    w_bp = float(box.group(3)) - float(box.group(1))
    want_bp = width_in(venue, span) * 72
    problems = []
    if abs(w_bp - want_bp) > 0.5:
        problems.append(f"width {w_bp / 72:.3f} in, venue needs {want_bp / 72:.3f} in")
    if b"/Type3" in pdf:
        problems.append("Type 3 font present (set pdf.fonttype = 42)")
    if b"/FontFile" not in pdf and b"/Font" in pdf:
        problems.append("fonts not embedded")
    return {"width_in": round(w_bp / 72, 3), "height_in": round(float(box.group(4)) / 72, 3),
            "problems": problems}


def export(fig, stem, venue: str, span: str = "column", formats=("pdf", "svg", "png")):
    """Save at the exact physical size (no bbox_inches='tight'), then check the PDF."""
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        kw = {"dpi": 600, "pil_kwargs": {"compression": "tiff_lzw"}} if fmt == "tiff" else \
             {"dpi": 300} if fmt == "png" else {}
        fig.savefig(f"{stem}.{fmt}", **kw)
    if "pdf" in formats:
        res = check_pdf(f"{stem}.pdf", venue, span)
        if res["problems"]:
            raise RuntimeError(f"{stem}.pdf: " + "; ".join(res["problems"]))
        return res
    return None


def _selftest():
    setup()
    with tempfile.TemporaryDirectory() as d:
        for venue in VENUES:
            for span in ("column", "page"):
                fig = figure(venue, span, height_in=1.5)
                ax = fig.add_subplot(111)
                ax.plot([0, 1], [0, 1], **series_style(0, ours=True), label="Ours")
                ax.legend()
                res = export(fig, Path(d) / f"{venue}_{span}", venue, span, formats=("pdf",))
                plt.close(fig)
                assert not res["problems"], res
                print(f"ok  {venue:6} {span:6} {res['width_in']:.3f} in")
    try:
        width_in("nope")
        raise AssertionError("unknown venue must raise")
    except ValueError:
        pass
    print("selftest ok")


if __name__ == "__main__":
    _selftest()
