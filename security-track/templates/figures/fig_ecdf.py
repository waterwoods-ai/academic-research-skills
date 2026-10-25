"""ECDF of a measured quantity across groups (scenario 9 in figure_template_map.md).

Measurement studies (time to patch, latency, devices per vendor) have skewed, heavy-tailed
data, where a bar of means misleads. Rules: plot the step ECDF of every observation; give n
per group in the legend; use a log x-axis when the data span orders of magnitude; mark
medians when they carry the comparison.
"""
import sys
from pathlib import Path

import numpy as np

import sec_figstyle as sf


def ecdf_plot(ax, samples, logx=False, mark_median=True, highlight=None):
    """samples: {group: 1-D array}. highlight: a group drawn in the signal colour (optional)."""
    i = 0
    for name, x in samples.items():
        x = np.sort(np.asarray(x, float))
        if x.size == 0 or not np.all(np.isfinite(x)):
            raise ValueError(f"{name}: need finite observations")
        y = np.arange(1, x.size + 1) / x.size
        st = sf.series_style(i, ours=name == highlight)
        i += 0 if name == highlight else 1
        ax.step(np.r_[x[0], x], np.r_[0, y], where="post", color=st["color"], ls=st["ls"], lw=st["lw"],
                label=f"{name} (n = {x.size:,})")
        if mark_median:
            ax.plot(np.median(x), 0.5, marker=st["marker"], color=st["color"], markersize=3.5,
                    markeredgewidth=0, zorder=5)
    ax.axhline(0.5, color=sf.GRID, lw=0.6, zorder=0)
    if logx:
        ax.set_xscale("log")
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Fraction of observations (ECDF)")
    ax.legend(loc="lower right", fontsize=sf.SMALL_PT, handlelength=2.4)


if __name__ == "__main__":  # demo with SYNTHETIC measurements
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "previews"
    rng = np.random.default_rng(3)
    samples = {"Vendor A": rng.lognormal(3.0, 0.9, 412),
               "Vendor B": rng.lognormal(4.1, 1.1, 287),
               "Vendor C": rng.lognormal(5.0, 0.8, 133)}
    sf.setup()
    fig = sf.figure("ieee", "column", height_in=2.3)
    ax = fig.add_axes([0.15, 0.18, 0.8, 0.74])
    ecdf_plot(ax, samples, logx=True)
    ax.set_xlabel("Days from disclosure to patch (log scale)")
    sf.mark_synthetic(fig)
    print(sf.export(fig, out / "ecdf", "ieee", "column", formats=("pdf", "png")))
