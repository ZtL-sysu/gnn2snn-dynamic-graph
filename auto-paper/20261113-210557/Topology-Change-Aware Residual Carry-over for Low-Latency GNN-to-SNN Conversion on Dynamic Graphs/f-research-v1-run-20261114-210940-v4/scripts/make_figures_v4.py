#!/usr/bin/env python3
"""Generate v4 paper figures (PDF + PNG) from real campaign artefacts.
Sources: results/aggregated.json, results/final-analysis-v4.json,
results/theory/theory_arms.json, results/theory/bound_constants.json,
results/latency/latency_probe.json.
Every figure is skipped with a message (never faked) when its data is absent.
"""
from __future__ import annotations
import json
import traceback
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = Path(__file__).resolve().parents[1]
R = RUN / "results"
FIG = RUN / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

streams = ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
methods = ["C0", "C1", "C2", "C3", "C4", "C5MT", "M0", "A1", "A2", "A3", "A5", "D1"]
bound_methods = ["C1", "C2", "M0"]
CAP = {s: s.capitalize() for s in streams}

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
    "legend.fontsize": 7.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 110, "savefig.bbox": "tight",
})
C = {"C0": "#999999", "C1": "#88CCEE", "C2": "#44AA99", "C3": "#117733",
     "C4": "#332288", "C5MT": "#CC6677", "M0": "#882255", "A1": "#DDCC77",
     "A2": "#AA4499", "A3": "#EE7733", "A5": "#EE99AA", "D1": "#000000"}


def load(p, d=None):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return d if d is not None else {}


agg = load(R / "aggregated.json") or {}
runs = agg.get("runs", [])
an = load(R / "final-analysis-v4.json") or {}
arms = load(R / "theory" / "theory_arms.json") or {}
bc = load(R / "theory" / "bound_constants.json") or {}
lat = load(R / "latency" / "latency_probe.json") or {}
by = {(r["stream"], r["seed"]): r for r in runs}
done = []


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"{name}.{ext}", dpi=300)
    plt.close(fig)
    done.append(name)


def mmean(s, m, key, seeds=range(41, 51)):
    v = [by[(s, sd)]["methods"][m][key] for sd in seeds if (s, sd) in by]
    return np.array(v) if v else None


def main_table(s, m, key):
    v = mmean(s, m, key)
    return (v.mean(), v.std(ddof=1)) if v is not None and len(v) else (np.nan, np.nan)


def fig2_tcurve():
    arm = arms.get("T_sweep", [])
    if not arm:
        return
    Ts = [r["cfg"]["T"] for r in arm]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.6))
    for m, lab in (("C2", "C2 (DCGS)"), ("M0", "M0 (TCAR)")):
        agr = [r["methods"][m]["agreement"] for r in arm]
        eps = [r["methods"][m]["mean_epsilon"] for r in arm]
        a1.plot(Ts, agr, "o-", color=C[m], label=lab, lw=1.5, ms=4)
        a2.plot(Ts, eps, "o-", color=C[m], label=lab, lw=1.5, ms=4)
    for ax in (a1, a2):
        ax.set_xscale("log", base=2); ax.set_xticks(Ts); ax.set_xticklabels([str(t) for t in Ts])
        ax.set_xlabel("Simulation micro-steps $T$")
    a1.set_ylabel("Teacher--SNN agreement")
    a2.set_ylabel("Mean per-event $\\varepsilon_k$"); a2.set_yscale("log")
    a1.legend(frameon=False)
    fig.tight_layout()
    save(fig, "fig2_tcurve")


def fig3_main():
    if not runs:
        return
    s = "wikipedia"
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.7))
    xs = np.arange(len(methods))
    ag = [main_table(s, m, "agreement")[0] for m in methods]
    ep = [main_table(s, m, "mean_epsilon")[0] for m in methods]
    a1.bar(xs, ag, color=[C[m] for m in methods], width=0.72)
    for m in ("M0", "C2"):
        v = mmean(s, m, "agreement")
        if v is not None:
            j = methods.index(m)
            a1.scatter(np.full(len(v), j) + np.linspace(-0.16, 0.16, len(v)), v,
                       s=7, color="white", edgecolor="black", lw=0.4, zorder=5)
    a1.set_xticks(xs); a1.set_xticklabels(methods, rotation=45, ha="right")
    a1.set_ylabel("Agreement (Wikipedia)"); a1.set_ylim(0.9, 1.005)
    a2.bar(xs, ep, color=[C[m] for m in methods], width=0.72)
    a2.set_yscale("log")
    a2.set_xticks(xs); a2.set_xticklabels(methods, rotation=45, ha="right")
    a2.set_ylabel("Mean per-event $\\varepsilon_k$")
    fig.tight_layout()
    save(fig, "fig3_main")


def fig4_error():
    if not runs:
        return
    s = "wikipedia"
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    xs = np.arange(len(methods))
    parts = [("clip_error", "clipping"), ("quant_error", "quantisation"), ("residual_error", "residual")]
    bottoms = np.zeros(len(methods))
    cols = ["#DDCC77", "#88CCEE", "#CC6677"]
    for (k, lab), col in zip(parts, cols):
        v = np.array([main_table(s, m, k)[0] for m in methods])
        ax.bar(xs, v, bottom=bottoms, color=col, label=lab, width=0.72)
        bottoms += np.nan_to_num(v)
    ax.set_xticks(xs); ax.set_xticklabels(methods, rotation=45, ha="right")
    ax.set_ylabel("Error component (norm)"); ax.legend(frameon=False)
    fig.tight_layout()
    save(fig, "fig4_error")


def fig5_streams():
    c1 = (an.get("c1_rule") or {}).get("result", {})
    if not c1:
        return
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    for i, s in enumerate(streams):
        row = c1.get(s, {})
        ci = row.get("bca95", {}).get("ci95", [np.nan, np.nan])
        md = row.get("mean_diff", np.nan)
        ax.plot([0, 0], [-0.6, len(streams) - 0.4], color="#bbbbbb", lw=0.8, zorder=0)
        perseed = row.get("paired_eps_diff_C2_minus_M0") or []
        if perseed:
            ax.scatter(perseed, np.full(len(perseed), i) + np.linspace(-0.13, 0.13, len(perseed)),
                       s=10, color="#44AA99", edgecolor="black", lw=0.3, zorder=4)
        ax.plot(ci, [i, i], color="#882255", lw=2, zorder=3)
        ax.plot(md, i, "o", color="#882255", ms=5, zorder=5)
    ax.set_yticks(range(len(streams))); ax.set_yticklabels([CAP[s] for s in streams])
    ax.set_xlabel("Paired per-seed difference $\\varepsilon_{C2}-\\varepsilon_{M0}$")
    ax.set_xscale("symlog", linthresh=1e-4)
    fig.tight_layout()
    save(fig, "fig5_streams")


def fig6_dose():
    def arm_xy(arm, m, key):
        a = arms.get(arm, [])
        return ([r["cfg"].get({"alpha_state": "alpha_state", "edge_insert": "edge_insert",
                               "alpha_carry": "alpha"}[arm]) for r in a],
                [r["methods"][m][key] for r in a])
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.4))
    specs = [("alpha_carry", "agreement", "carry-over dose $\\alpha$", "Agreement"),
             ("alpha_state", "mean_epsilon", "state decay $\\alpha_s$", "Mean $\\varepsilon_k$"),
             ("edge_insert", "mean_epsilon", "edge insertion rate $p$", "Mean $\\varepsilon_k$")]
    for ax, (arm, key, xl, yl) in zip(axs, specs):
        for m in ("C2", "M0"):
            x, y = arm_xy(arm, m, key)
            if x and all(v is not None for v in x):
                ax.plot(x, y, "o-", color=C[m], label=m, lw=1.4, ms=4)
        ax.set_xlabel(xl); ax.set_ylabel(yl)
        if arm == "alpha_carry":
            ax.legend(frameon=False)
    fig.tight_layout()
    save(fig, "fig6_dose")


def fig7_pareto():
    if not runs or not lat:
        return
    en = an.get("energy") or {}
    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    ref = None
    for s in streams:
        if "_ann_reference_pj_per_event" in en.get(s, {}):
            ref = en[s]["_ann_reference_pj_per_event"]; break
    for m in methods:
        xs, ys = [], []
        for s in streams:
            e = en.get(s, {}).get(m)
            v = mmean(s, m, "agreement")
            if e and v is not None:
                xs.append(e["snj_per_event"]); ys.append(v.mean())
        if xs:
            ax.scatter(xs, ys, color=C[m], label=m, s=22, edgecolor="black", lw=0.4)
    if ref:
        ax.axvline(ref, color="#999999", ls="--", lw=1)
        ax.text(ref * 1.05, ax.get_ylim()[0] + 0.01, "ANN reference", rotation=90, fontsize=7, color="#666666")
    ax.set_xscale("log"); ax.set_xlabel("Op-count energy (pJ/event)")
    ax.set_ylabel("Agreement"); ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    save(fig, "fig7_pareto")


def fig8_ladder():
    if not runs:
        return
    s = "wikipedia"
    ladder = [("C0", "naive rate"), ("C1", "+ differential"), ("C2", "+ threshold iteration"),
              ("C5MT", "+ multi-threshold"), ("M0", "+ TCAR gating")]
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    xs = np.arange(len(ladder))
    vs = [main_table(s, m, "mean_epsilon")[0] for m, _ in ladder]
    bars = ax.bar(xs, vs, color=[C[m] for m, _ in ladder], width=0.66)
    for x, v in zip(xs, vs):
        ax.text(x, v * 1.15, f"{v:.2e}", ha="center", fontsize=7)
    ax.set_yscale("log")
    ax.set_xticks(xs); ax.set_xticklabels([lab for _, lab in ladder], rotation=20, ha="right")
    ax.set_ylabel("Mean per-event $\\varepsilon_k$ (Wikipedia)")
    fig.tight_layout()
    save(fig, "fig8_ladder")


def fig9_bound():
    if not bc or not runs:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.6))
    xs = np.arange(len(streams)); w = 0.26
    for j, m in enumerate(bound_methods):
        vr = []
        for s in streams:
            v = mmean(s, m, "bound")
            vr.append(np.mean([d["violation_rate"] for d in v]) if v is not None else np.nan)
        a1.bar(xs + (j - 1) * w, np.array(vr) * 100, width=w, color=C[m], label=m)
    a1.axhline(5.0, color="black", ls="--", lw=1)
    a1.text(len(streams) - 0.5, 5.3, "5% ceiling (E10)", fontsize=7, ha="right")
    a1.set_xticks(xs); a1.set_xticklabels([CAP[s] for s in streams], rotation=20, ha="right")
    a1.set_ylabel("Bound violation rate (%)"); a1.legend(frameon=False)
    for j, m in enumerate(bound_methods):
        tg = []
        for s in streams:
            v = mmean(s, m, "bound")
            tg.append(np.mean([d["mean_tightness"] for d in v]) if v is not None else np.nan)
        a2.bar(xs + (j - 1) * w, tg, width=w, color=C[m], label=m)
    a2.set_xticks(xs); a2.set_xticklabels([CAP[s] for s in streams], rotation=20, ha="right")
    a2.set_ylabel("Mean bound tightness $\\bar e_k/\\mathrm{rhs}_k$"); a2.legend(frameon=False)
    fig.tight_layout()
    save(fig, "fig9_bound")


def fig10_robust():
    specs = [("robust_noise", "noise $\\sigma$"), ("robust_dt", "time shift $\\delta_t$"),
             ("robust_drop", "edge drop $p$")]
    if not any(arms.get(a) for a, _ in specs):
        return
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.4))
    for ax, (arm, xl) in zip(axs, specs):
        a = arms.get(arm, [])
        if not a:
            continue
        x = [r["cfg"].get({"robust_noise": "noise", "robust_dt": "dt", "robust_drop": "drop"}[arm]) for r in a]
        for m in ("C2", "M0"):
            ax.plot(x, [r["methods"][m]["mean_epsilon"] for r in a], "o-", color=C[m], label=m, lw=1.4, ms=4)
        ax.set_xlabel(xl); ax.set_ylabel("Mean $\\varepsilon_k$"); ax.set_yscale("log")
    axs[0].legend(frameon=False)
    fig.tight_layout()
    save(fig, "fig10_robust")


def fig11_drift():
    dr = an.get("drift") or {}
    keys = [k for k in dr if k.endswith(".M0")]
    if not keys:
        return
    fig, axs = plt.subplots(1, len(streams), figsize=(7.2, 2.3), sharey=True)
    for ax, s in zip(axs, streams):
        d = dr.get(f"{s}.M0", {})
        sl = d.get("mean_epsilon_per_slice") or []
        if not sl:
            continue
        xs = list(range(1, len(sl) + 1))
        ax.plot(xs, sl, "o-", color=C["M0"], ms=3, lw=1.2, label="M0")
        d2 = dr.get(f"{s}.C2", {})
        sl2 = d2.get("mean_epsilon_per_slice") or []
        if sl2:
            ax.plot(xs, sl2, "s--", color=C["C2"], ms=3, lw=1.2, label="C2")
        ax.set_title(CAP[s], fontsize=8); ax.set_xlabel("Window decile")
    axs[0].set_ylabel("Mean $\\varepsilon_k$ (per decile)"); axs[0].legend(frameon=False)
    fig.tight_layout()
    save(fig, "fig11_drift")


def fig12_downstream():
    if not runs:
        return
    edges = ["$<10^{-5}$", "$10^{-5}$", "$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$"]
    xs = np.arange(6)
    means = {}
    for s in streams:
        for m in ("M0", "C2"):
            v = mmean(s, m, "mrr_loss_per_epsbin")
            if v is None:
                continue
            mean = np.nanmean(np.stack([np.array(x, dtype=float) for x in v]), axis=0)
            if np.isfinite(mean).any():
                means[(s, m)] = mean
    if not means:
        return
    allfin = np.concatenate([m[np.isfinite(m)] for m in means.values()])
    lo, hi = float(allfin.min()), float(allfin.max())
    pad = max((hi - lo) * 0.15, 1e-9)
    fig, axs = plt.subplots(1, len(streams), figsize=(7.2, 2.3))
    for ax, s in zip(axs, streams):
        for m, mk in (("M0", "o-"), ("C2", "s--")):
            mean = means.get((s, m))
            if mean is None:
                continue
            mean = np.array(mean, dtype=float)
            mean[~np.isfinite(mean)] = np.nan
            ax.plot(xs, mean, mk, color=C[m], ms=3, lw=1.2, label=m)
        ax.set_ylim(lo - pad, hi + pad)
        ax.set_title(CAP[s], fontsize=8); ax.set_xticks(xs)
        ax.set_xticklabels(edges, rotation=60, ha="right", fontsize=6)
    axs[0].set_ylabel("MRR loss (ANN $-$ SNN)"); axs[0].legend(frameon=False)
    axs[2].set_xlabel("Per-event $\\varepsilon_k$ bin")
    save(fig, "fig12_downstream")


def fig13_strata():
    if not runs:
        return
    fig, axs = plt.subplots(1, len(streams), figsize=(7.2, 2.3), sharey=True)
    for ax, s in zip(axs, streams):
        v = mmean(s, "M0", "firing_per_da_bin")
        if v is None:
            continue
        mean = np.nanmean(np.stack([np.array(x, dtype=float) for x in v]), axis=0)
        xs = np.arange(len(mean))
        ax.bar(xs, mean, color=C["M0"], width=0.7)
        ax.set_title(CAP[s], fontsize=8); ax.set_xticks(xs)
        ax.set_xticklabels([f"b{i}" for i in xs], fontsize=7)
    axs[0].set_ylabel("Firing rate"); axs[2].set_xlabel("Measured $\\|\\Delta A_k\\|$ bin (C-10 strata)")
    fig.tight_layout()
    save(fig, "fig13_strata")


for fn in (fig2_tcurve, fig3_main, fig4_error, fig5_streams, fig6_dose, fig7_pareto,
           fig8_ladder, fig9_bound, fig10_robust, fig11_drift, fig12_downstream, fig13_strata):
    try:
        fn()
    except Exception:
        print(f"[skip] {fn.__name__}:")
        traceback.print_exc(limit=2)
print("figures written:", ", ".join(done) if done else "NONE (data pending)")
