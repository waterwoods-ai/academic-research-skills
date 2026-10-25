"""ROC for detectors on a log-scale FPR axis (scenario 8 in figure_template_map.md).

Security detectors are judged at low false-positive rates, where a linear axis hides every
difference. Rules: log FPR axis down to the operating range; report AUC and TPR at the stated
FPR budgets in the legend; mark those budgets; keep the chance line for reference.
"""
import sys
from pathlib import Path

import numpy as np

import sec_figstyle as sf


def roc_curve(y_true, scores):
    """FPR and TPR at every threshold (higher score = more likely malicious), numpy only."""
    y = np.asarray(y_true, bool)
    order = np.argsort(-np.asarray(scores, float), kind="stable")
    tp = np.cumsum(y[order])
    fp = np.cumsum(~y[order])
    if tp[-1] == 0 or fp[-1] == 0:
        raise ValueError("need both positive and negative samples")
    return np.r_[0.0, fp / fp[-1]], np.r_[0.0, tp / tp[-1]]


def tpr_at(fpr, tpr, budget):
    """Best TPR reachable with FPR <= budget."""
    ok = fpr <= budget
    return float(tpr[ok].max()) if ok.any() else 0.0


def roc_plot(ax, curves, ours=None, budgets=(1e-3, 1e-2), fpr_min=1e-4):
    """curves: {name: (fpr, tpr)}. The legend reports AUC and TPR at the largest budget."""
    for b in budgets:
        ax.axvline(b, color=sf.GRID, lw=0.6, zorder=0)
        ax.text(b, 1.01, f"{b * 100:g}% FPR", transform=ax.get_xaxis_transform(), va="bottom",
                ha="center", fontsize=sf.SMALL_PT, color="#808080")
    xs = np.logspace(np.log10(fpr_min), 0, 200)
    ax.plot(xs, xs, color="#A8A8A8", lw=0.6, ls=(0, (1, 1.5)), zorder=1, label="Chance")
    baseline_i = 0
    for name, (fpr, tpr) in curves.items():
        is_ours = name == ours
        st = sf.series_style(baseline_i, ours=is_ours)
        baseline_i += 0 if is_ours else 1
        auc = float(np.trapezoid(tpr, fpr))
        b = max(budgets)
        ax.step(np.clip(fpr, fpr_min, 1), tpr, where="post", color=st["color"], ls=st["ls"], lw=st["lw"],
                zorder=4 if is_ours else 3,
                label=f"{name} (AUC {auc:.3f}; TPR@{b * 100:g}% {tpr_at(fpr, tpr, b):.2f})")
    ax.set_xscale("log")
    ax.set_xlim(fpr_min, 1)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("False positive rate (log scale)")
    ax.set_ylabel("True positive rate")
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.2), fontsize=sf.SMALL_PT, handlelength=2.4)


if __name__ == "__main__":  # demo with SYNTHETIC scores
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "previews"
    rng = np.random.default_rng(7)
    y = np.r_[np.ones(2000, bool), np.zeros(20000, bool)]
    curves = {}
    for name, sep in (("Signature rules", 1.6), ("Anomaly score", 2.2), ("Ours", 3.4)):
        s = np.r_[rng.normal(sep, 1, 2000), rng.normal(0, 1, 20000)]
        curves[name] = roc_curve(y, s)
    sf.setup()
    fig = sf.figure("ieee", "column", height_in=3.0)
    ax = fig.add_axes([0.15, 0.33, 0.8, 0.6])
    roc_plot(ax, curves, ours="Ours")
    sf.mark_synthetic(fig)
    print(sf.export(fig, out / "roc", "ieee", "column", formats=("pdf", "png")))
