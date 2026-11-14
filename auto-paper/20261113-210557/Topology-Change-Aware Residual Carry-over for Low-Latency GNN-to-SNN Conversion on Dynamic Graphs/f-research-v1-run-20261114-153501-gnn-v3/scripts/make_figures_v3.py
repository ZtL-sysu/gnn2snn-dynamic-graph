#!/usr/bin/env python3
"""Generate the eight contract-v3 figures from real results when available.
If the full campaign has not finished, visibly-labelled placeholders are written
so that the TeX layout can be checked; these are always overwritten at P8.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = Path(__file__).resolve().parents[1]
R = RUN / "results"
FIG = RUN / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 8, "figure.dpi": 300})

runs = []
p = R / "aggregated.json"
if p.is_file():
    try:
        runs = json.loads(p.read_text())["runs"]
    except Exception:
        pass
REAL = len(runs) >= 15


def save(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


def placeholder(name, text):
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.axis("off")
    ax.text(0.5, 0.5, f"{name}\n{text}", ha="center", va="center", fontsize=10)
    save(fig, name)


# --- Figure 1: framework (always a real vector schematic; P8 records the
#     fallback from GPT image generation, whose credit cost is not authorised) ---
fig, ax = plt.subplots(figsize=(6.8, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")


def box(x, y, w, h, txt, fc):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor="#333", lw=0.8))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=7.5)


def ar(x1, y1, x2, y2, lbl=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#333"))
    if lbl:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.15, lbl, ha="center", fontsize=6.5)


box(0.1, 1.5, 1.7, 1.0, "Event stream\n$e_k=(u,v,t)$", "#e8f0fe")
box(2.1, 2.6, 1.8, 0.9, "Normalised $A_k$\nneighbour aggregation", "#fff4d6")
box(2.1, 0.5, 1.8, 0.9, "ANN GNN teacher\n$L$ residual GCN layers", "#f7f7f7")
box(4.3, 0.5, 1.8, 0.9, "DCGS differential coder\n$e_t=t(a_t-a_{t-1})$", "#fdeaea")
box(6.5, 2.6, 1.8, 0.9, "TCAR $\\delta>\\gamma$ or $\\Vert\\Delta A\\Vert>\\tau$\nbase re-anchor + $\\theta$", "#fdeaea")
box(6.5, 0.5, 1.8, 0.9, "Shared memory\n+ linear readout", "#e8f0fe")
box(8.7, 1.5, 1.1, 1.0, "scores\n$\\varepsilon_k$, events", "#eaf7ea")
ar(1.8, 2.0, 2.1, 3.05); ar(1.8, 2.0, 2.1, 0.95)
ar(3.9, 3.05, 4.3, 0.95); ar(3.9, 0.95, 4.3, 0.95)
ar(6.1, 0.95, 6.5, 0.95); ar(6.1, 0.95, 6.5, 3.05, "trigger")
ar(8.3, 3.05, 8.7, 2.0); ar(8.3, 0.95, 8.7, 2.0)
ax.text(5, 3.9, "Differential-coded GNN-to-SNN conversion with topology-change-aware recalibration",
        ha="center", fontsize=9, weight="bold")
save(fig, "fig1_framework")

if not REAL:
    for n, t in [("fig2_tcurve", "T-curve: pending full campaign"),
                 ("fig3_main", "method comparison: pending"),
                 ("fig4_error", "error decomposition: pending"),
                 ("fig5_streams", "five-stream replication: pending"),
                 ("fig6_dose", "measured ||dA|| dose response: pending"),
                 ("fig7_pareto", "latency-fidelity Pareto: pending")]:
        placeholder(n, t)
    (FIG / "figure-sources.json").write_text(json.dumps({"status": "placeholders"}, indent=2))
    print("wrote framework figure + labelled placeholders")
    raise SystemExit(0)

# ------------------------- real figures -------------------------
streams = ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
methods = list(runs[0]["methods"].keys())


def agg(s, m, key):
    v = [r["methods"][m][key] for r in runs if r["stream"] == s]
    return float(np.mean(v)), float(np.std(v, ddof=1)) if len(v) > 1 else 0.0


s = "wikipedia"
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.6))
x = np.arange(len(methods))
ag = [agg(s, m, "agreement")[0] for m in methods]
ep = [agg(s, m, "mean_epsilon")[0] for m in methods]
ax[0].bar(x, ag, color=["#b2182b" if m == "M0" else "#2166ac" if m == "C2" else "#9ecae1" for m in methods])
ax[0].set_ylim(max(0, min(ag) - 0.01), 1.001); ax[0].set_ylabel("agreement")
ax[1].bar(x, ep, color=["#b2182b" if m == "M0" else "#2166ac" if m == "C2" else "#9ecae1" for m in methods])
ax[1].set_ylabel(r"mean $\varepsilon_k$")
for a in ax:
    a.set_xticks(x); a.set_xticklabels(methods, rotation=45, ha="right", fontsize=6)
fig.suptitle("Wikipedia: conversion fidelity and accumulated state error (5 seeds)")
fig.tight_layout(); save(fig, "fig3_main")

# streams
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.5))
xx = np.arange(len(streams)); w = 0.35
e0 = [agg(s, "M0", "mean_epsilon")[0] for s in streams]
e2 = [agg(s, "C2", "mean_epsilon")[0] for s in streams]
ax[0].bar(xx - w / 2, e2, w, label="C2 global carry-over", color="#2166ac")
ax[0].bar(xx + w / 2, e0, w, label="M0 TCAR", color="#b2182b")
ax[0].set_xticks(xx); ax[0].set_xticklabels(streams, fontsize=7); ax[0].set_ylabel(r"mean $\varepsilon_k$"); ax[0].legend(fontsize=6)
tr = [agg(s, "M0", "recalibration_rate")[0] for s in streams]
ax[1].bar(streams, tr, color="#b2182b"); ax[1].axhline(0.2, ls="--", c="#4d4d4d", lw=0.8)
ax[1].set_ylabel("trigger rate"); ax[1].set_ylim(0, max(tr + [0.25]) + 0.04)
ax[1].tick_params(axis="x", labelsize=7)
fig.suptitle("Five-stream replication of state-error reduction and its event-bound cost")
fig.tight_layout(); save(fig, "fig5_streams")

# T curve from aux
aux_p = R / "p4_auxiliary" / "sweeps_v3.json"
if aux_p.is_file():
    aux = json.loads(aux_p.read_text())
    T = [r["cfg"]["T"] for r in aux["T_sweep"]]
    aa = [r["methods"]["M0"]["agreement"] for r in aux["T_sweep"]]
    ev = [r["methods"]["M0"]["graded_events_per_event"] for r in aux["T_sweep"]]
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    ax.plot(T, aa, "o-", color="#b2182b", label="agreement")
    ax.set_xlabel("micro-steps $T$"); ax.set_ylabel("agreement", color="#b2182b")
    ax2 = ax.twinx(); ax2.plot(T, ev, "s--", color="#2166ac", label="graded events")
    ax2.set_ylabel("graded events / event", color="#2166ac")
    ax.set_title("Latency--fidelity curve (Wikipedia)")
    fig.tight_layout(); save(fig, "fig2_tcurve")

    # error decomposition
    m0 = aux["T_sweep"][2]["methods"]["M0"] if len(aux["T_sweep"]) > 2 else runs[0]["methods"]["M0"]
    fig, ax = plt.subplots(figsize=(4.2, 2.5))
    keys = ["clip_error", "quant_error", "residual_error"]
    vals = [m0.get(k, 0.0) for k in keys]
    ax.bar(["clipping", "quantisation", "residual"], vals, color=["#9ecae1", "#6baed6", "#b2182b"])
    ax.set_ylabel("per-event error"); ax.set_title("Conversion-error decomposition (M0)")
    fig.tight_layout(); save(fig, "fig4_error")

    # Pareto
    fig, ax = plt.subplots(figsize=(4.2, 2.5))
    ms = ["C0", "C1", "C2", "C3", "C4", "M0", "A1", "A2", "A3", "A5", "D1"]
    xx = [r["methods"]["M0"]["graded_events_per_event"] for r in aux["T_sweep"][:1]]
    evs = [agg(s, m, "graded_events_per_event")[0] for m in ms]
    ags = [agg(s, m, "agreement")[0] for m in ms]
    ax.scatter(evs, ags, c=["#b2182b" if m == "M0" else "#4d4d4d" for m in ms])
    for m, xe, ye in zip(ms, evs, ags):
        ax.annotate(m, (xe, ye), fontsize=6, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("graded events / event"); ax.set_ylabel("agreement")
    ax.set_title("Latency--fidelity Pareto (Wikipedia)")
    fig.tight_layout(); save(fig, "fig7_pareto")

    # dose response from bound traces
    deltas, e2s, e0s = [], [], []
    for s in streams:
        for seed in [41, 42, 43, 44, 45]:
            p = R / "bound-check" / f"{s}_s{seed}_trace.json"
            if p.is_file():
                t = json.loads(p.read_text())
                n = min(len(t["dA"]), len(t["epsilon_M0"]), len(t["epsilon_C2"]))
                deltas.append(np.asarray(t["dA"][:n], float))
                e0s.append(np.asarray(t["epsilon_M0"][:n], float))
                e2s.append(np.asarray(t["epsilon_C2"][:n], float))
    if deltas:
        d = np.concatenate(deltas); a0 = np.concatenate(e0s); a2 = np.concatenate(e2s)
        bins = [("0", d == 0), ("(0,.15]", (d > 0) & (d <= .15)),
                ("(.15,.4]", (d > .15) & (d <= .4)), (">.4", d > .4)]
        labels, y0, y2 = [], [], []
        for name, m in bins:
            if m.sum() > 20:
                labels.append(f"{name}\nn={m.sum()}")
                y0.append(float(a0[m].mean())); y2.append(float(a2[m].mean()))
        xx = np.arange(len(labels))
        fig, ax = plt.subplots(figsize=(4.2, 2.5))
        ax.bar(xx - .2, y2, .4, label="C2", color="#2166ac")
        ax.bar(xx + .2, y0, .4, label="M0", color="#b2182b")
        ax.set_xticks(xx); ax.set_xticklabels(labels, fontsize=6)
        ax.set_ylabel(r"mean $\varepsilon_k$"); ax.legend(fontsize=6)
        ax.set_title(r"State error by measured $\|\Delta A_k\|$")
        fig.tight_layout(); save(fig, "fig6_dose")

(FIG / "figure-sources.json").write_text(json.dumps({
    "status": "real", "n_runs": len(runs), "source": "results/aggregated.json and results/p4_auxiliary/sweeps_v3.json",
    "fig1": "local vector schematic (recorded fallback from GPT image generation; credit cost not authorised)"
}, indent=2) + "\n", encoding="utf-8")
print("wrote real figures from", len(runs), "runs")
