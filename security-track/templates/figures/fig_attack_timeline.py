"""Physical process under attack, with the detector below it (scenario 12 in figure_template_map.md).

CPS papers show what the attack does to the plant and when the defense reacts. Rules: one
shared time axis; shade the attack window; mark the detection time and give the delay in the
legend or a label; draw thresholds and setpoints; units on every y-axis.
"""
import sys
from pathlib import Path

import numpy as np

import sec_figstyle as sf


def first_alarm(t, detector, threshold, start):
    """First time at or after `start` when the detector exceeds the threshold, or None."""
    hit = np.flatnonzero((np.asarray(t) >= start) & (np.asarray(detector) > threshold))
    return float(t[hit[0]]) if hit.size else None


def attack_timeline(fig, t, process, detector, attack, detected_at=None, threshold=None,
                    process_label="", detector_label="Detector score", t_label="Time (s)"):
    """process: {name: series} (e.g. measured, true, setpoint); detector: series;
    attack: (start, end); detected_at: time or None; threshold: detector alarm level."""
    top, bottom = fig.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [2, 1], "hspace": 0.12})
    for ax in (top, bottom):
        ax.axvspan(*attack, color=sf.ATTACK, alpha=0.10, lw=0, zorder=0)
        if detected_at is not None:
            ax.axvline(detected_at, color=sf.ATTACK, lw=0.8, ls=(0, (3, 1.5)), zorder=2)
    styles = [{"color": "#272727", "ls": "-", "lw": 1.0}, {"color": sf.OURS, "ls": (0, (4, 1.5)), "lw": 1.0},
              {"color": "#A8A8A8", "ls": (0, (1.2, 1.2)), "lw": 0.9}]
    for st, (name, y) in zip(styles, process.items()):
        top.plot(t, y, label=name, **st)
    top.set_ylabel(process_label)
    lo, hi = top.get_ylim()
    top.set_ylim(lo, hi + 0.18 * (hi - lo))  # headroom for the event labels
    y_lab = top.get_ylim()[1]
    top.text((attack[0] + attack[1]) / 2, y_lab, "attack", color=sf.ATTACK, fontsize=sf.SMALL_PT,
             va="top", ha="center")
    if detected_at is not None:
        top.text(detected_at, y_lab, f"detected (+{detected_at - attack[0]:g} s) ", color=sf.ATTACK,
                 fontsize=sf.SMALL_PT, va="top", ha="right")
    top.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=len(process), fontsize=sf.SMALL_PT,
               handlelength=2.4, columnspacing=1.0, borderaxespad=0)
    bottom.plot(t, detector, color=sf.OURS, lw=1.0)
    if threshold is not None:
        bottom.axhline(threshold, color="#606060", lw=0.7, ls=(0, (4, 1.5)))
        bottom.text(t[0], threshold, "threshold", fontsize=sf.SMALL_PT, color="#606060", va="bottom")
    bottom.set_ylabel(detector_label)
    bottom.set_xlabel(t_label)
    return top, bottom


if __name__ == "__main__":  # demo with SYNTHETIC signals: false data injection on a tank level
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "previews"
    rng = np.random.default_rng(5)
    t = np.arange(0, 300, 0.5)
    setpoint = np.full_like(t, 50.0)
    true = 50 + 0.6 * np.sin(t / 9) + rng.normal(0, 0.15, t.size)
    attack = (120, 210)
    inside = (t >= attack[0]) & (t <= attack[1])
    drift = np.where(inside, np.minimum((t - attack[0]) * 0.12, 9), 0.0)  # the plant drifts
    end = drift[inside][-1]
    after = t > attack[1]
    drift[after] = end * np.exp(-(t[after] - attack[1]) / 12)             # and recovers after it
    true += drift
    measured = true.copy()
    measured[inside] = 50 + 0.6 * np.sin(t[inside] / 9) + rng.normal(0, 0.15, inside.sum())  # spoofed
    score = np.abs(rng.normal(0.2, 0.08, t.size))
    score += drift / 7.5
    sf.setup()
    fig = sf.figure("ieee", "column", height_in=2.6)
    fig.subplots_adjust(left=0.14, right=0.97, top=0.86, bottom=0.15)
    attack_timeline(fig, t, {"True level": true, "Reported level": measured, "Setpoint": setpoint},
                    score, attack, detected_at=first_alarm(t, score, 0.6, attack[0]), threshold=0.6,
                    process_label="Tank level (cm)")
    sf.mark_synthetic(fig)
    print(sf.export(fig, out / "attack_timeline", "ieee", "column", formats=("pdf", "png")))
