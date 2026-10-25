"""Radar: a few methods across many benchmarks or attack families (scenario 6 in figure_template_map.md).

Rules this template enforces: every spoke shares one 0-100 scale and outer is better
(plot 100 - ASR for attack spokes), so polygon areas are comparable; no per-spoke rescaling
and no truncated radial axis. Methods differ by line style and marker as well as colour.
"""
import sys
from pathlib import Path

import numpy as np

import sec_figstyle as sf


def _closed(a):
    return np.append(a, a[0])


def radar(fig, labels, series, ours, italic=(), note=None, rect=(0.2, 0.235, 0.6, 0.62)):
    """labels: spoke labels; series: {method: values in 0..100, outer = better}; ours: the
    proposed method's name; italic: indices of spokes in a second metric group; note: footnote."""
    n = len(labels)
    for name, v in series.items():
        v = np.asarray(v, dtype=float)
        if v.shape != (n,) or np.any((v < 0) | (v > 100)):
            raise ValueError(f"{name}: need {n} values in [0, 100]")
    step = 2 * np.pi / n
    ang = np.arange(n) * step
    ax = fig.add_axes(rect, projection="polar")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 100)
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for r in (25, 50, 75):
        ax.plot(_closed(ang), np.full(n + 1, r), color=sf.GRID, lw=0.5, zorder=1)
    ax.plot(_closed(ang), np.full(n + 1, 100), color="#606060", lw=0.7, zorder=1)
    for a in ang:
        ax.plot([a, a], [0, 100], color=sf.GRID, lw=0.5, zorder=1)
    for r in (25, 50, 75, 100):  # ring values in the first sector, clear of the spokes
        ax.text(step / 2, r * np.cos(step / 2) + 2, f"{r}", fontsize=sf.SMALL_PT, color="#808080",
                ha="center", va="bottom", zorder=6)
    baseline_i = 0
    for name, v in series.items():
        is_ours = name == ours
        st = sf.series_style(baseline_i, ours=is_ours)
        baseline_i += 0 if is_ours else 1
        ax.plot(_closed(ang), _closed(np.asarray(v, float)), color=st["color"], ls=st["ls"], lw=st["lw"],
                marker=st["marker"], markersize=3.2, markevery=range(n), markeredgewidth=0,
                zorder=4 if is_ours else 3, label=name)
        if is_ours:
            ax.fill(_closed(ang), _closed(np.asarray(v, float)), color=st["color"], alpha=0.10, lw=0, zorder=2)
    for i, (a, text) in enumerate(zip(ang, labels)):
        s, c = np.sin(a), np.cos(a)  # screen x, y on a clockwise axis starting north
        ax.text(a, 108, text, ha="left" if s > 0.15 else "right" if s < -0.15 else "center",
                va="bottom" if c > 0.15 else "top" if c < -0.15 else "center", fontsize=sf.FONT_PT,
                linespacing=1.05, clip_on=False, style="italic" if i in italic else "normal")
    fig.legend(loc="lower center", bbox_to_anchor=(0.5, 0.075), ncol=len(series), handlelength=2.6,
               columnspacing=1.4)
    if note:
        fig.text(0.5, 0.008, note, ha="center", va="bottom", fontsize=sf.SMALL_PT, color="#606060",
                 linespacing=1.25)
    return ax


if __name__ == "__main__":  # demo with SYNTHETIC data
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "previews"
    sf.setup()
    fig = sf.figure("ieee", "column", height_in=3.45)
    labels = ["Direct\nprompt injection", "Indirect\nprompt injection", "Tool-output\npoisoning",
              "Memory\npoisoning", "Multi-turn\njailbreak", "Adaptive\nattack", "Utility\n(suite A)",
              "Utility\n(suite B)"]
    series = {"No defense": [41, 28, 33, 38, 45, 12, 91, 86],
              "Input filter": [72, 55, 49, 52, 63, 21, 78, 71],
              "Ours": [88, 84, 81, 79, 77, 64, 87, 84]}
    radar(fig, labels, series, ours="Ours", italic=(6, 7),
          note="Upright axes: 100 − attack success rate (%).\nItalic axes: benign task success (%). Outer is better.")
    sf.mark_synthetic(fig)
    print(sf.export(fig, out / "radar", "ieee", "column", formats=("pdf", "png")))
