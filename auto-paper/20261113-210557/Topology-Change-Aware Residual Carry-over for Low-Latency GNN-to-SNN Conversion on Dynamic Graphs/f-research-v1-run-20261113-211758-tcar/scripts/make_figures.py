#!/usr/bin/env python3
"""P8 data figures: every point is read from real results, nothing is invented."""
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

runs = json.loads((R / "aggregated.json").read_text())["runs"]
streams = ["wikipedia", "mooc", "enron"]
methods = ["C0", "C1", "C2", "C3", "C4", "A1", "A2", "A3", "A4", "M0"]
colors = {"M0": "#b2182b", "C4": "#2166ac", "C0": "#4d4d4d"}
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "figure.dpi": 300})


def agg(s, m, key):
    vals = [r["methods"][m][key] for r in runs if r["stream"] == s]
    return float(np.mean(vals)), float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0


# Figure 2: agreement and state error across methods (primary stream)
s = "wikipedia"
fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.5))
ag = [agg(s, m, "agreement")[0] for m in methods]
ep = [agg(s, m, "mean_epsilon")[0] for m in methods]
x = np.arange(len(methods))
ax[0].bar(x, ag, color=[colors.get(m, "#9ecae1") for m in methods])
ax[0].set_ylim(min(ag) - 0.004, 1.001)
ax[0].set_ylabel("teacher-to-SNN agreement")
ax[0].set_xticks(x); ax[0].set_xticklabels(methods, rotation=45, ha="right")
ax[0].axhline(0.985, ls="--", lw=0.8, color="#b2182b")
ax[1].bar(x, ep, color=[colors.get(m, "#9ecae1") for m in methods])
ax[1].set_ylabel(r"mean $\epsilon_k$ (state error)")
ax[1].set_xticks(x); ax[1].set_xticklabels(methods, rotation=45, ha="right")
fig.suptitle("Wikipedia: conversion fidelity and accumulated state error (5 seeds)")
fig.tight_layout()
fig.savefig(FIG / "fig2_methods.pdf", bbox_inches="tight")
fig.savefig(FIG / "fig2_methods.png", bbox_inches="tight")
plt.close(fig)

# Figure 3: three-stream epsilon reduction and cost
fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.4))
w = 0.35; xx = np.arange(len(streams))
e0 = [agg(s, "M0", "mean_epsilon")[0] for s in streams]
e4 = [agg(s, "C4", "mean_epsilon")[0] for s in streams]
ax[0].bar(xx - w / 2, e4, w, label="C4 global carry-over", color="#2166ac")
ax[0].bar(xx + w / 2, e0, w, label="M0 TCAR", color="#b2182b")
ax[0].set_xticks(xx); ax[0].set_xticklabels(streams)
ax[0].set_ylabel(r"mean $\epsilon_k$"); ax[0].legend(fontsize=7)
tr = [agg(s, "M0", "recalibration_rate")[0] for s in streams]
ax[1].bar(streams, tr, color="#b2182b")
ax[1].axhline(0.20, ls="--", lw=0.8, color="#4d4d4d")
ax[1].set_ylabel("recalibration trigger rate")
ax[1].set_ylim(0, 0.25)
fig.suptitle("Cross-stream replication of the error reduction and its event-bound cost")
fig.tight_layout()
fig.savefig(FIG / "fig3_streams.pdf", bbox_inches="tight")
fig.savefig(FIG / "fig3_streams.png", bbox_inches="tight")
plt.close(fig)

# Figure 4: topology-change dose response (fixed, pre-registered bins)
fig, ax = plt.subplots(figsize=(3.3, 2.4))
d_all, e4_all, e0_all = [], [], []
for s in streams:
    for seed in [41, 42, 43, 44, 45]:
        p = R / "bound-check" / f"{s}_s{seed}_trace.json"
        if p.is_file():
            t = json.loads(p.read_text())
            m = min(len(t["delta"]), len(t["epsilon_C4"]), len(t["epsilon_M0"]))
            d_all.append(np.asarray(t["delta"][:m], float))
            e4_all.append(np.asarray(t["epsilon_C4"][:m], float))
            e0_all.append(np.asarray(t["epsilon_M0"][:m], float))
d = np.concatenate(d_all); a4 = np.concatenate(e4_all); a0 = np.concatenate(e0_all)
bins = [("no change", (d == 0)), ("0--0.25", (d > 0) & (d <= 0.25)),
        ("0.25--0.6", (d > 0.25) & (d <= 0.6)), (">0.6", (d > 0.6))]
labels, reds, ns = [], [], []
for name, m in bins:
    if m.sum() > 20:
        labels.append(f"{name}\n(n={m.sum()})")
        reds.append(1.0 - float(a0[m].mean()) / max(float(a4[m].mean()), 1e-12))
        ns.append(int(m.sum()))
ax.bar(range(len(labels)), reds, color="#b2182b")
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=7)
ax.set_ylabel(r"relative $\epsilon_k$ reduction")
ax.axhline(0.5, ls="--", lw=0.8, color="#4d4d4d")
ax.set_ylim(0, max(reds + [0.55]) + 0.08)
fig.suptitle("Error reduction by measured topology-change magnitude")
fig.tight_layout()
fig.savefig(FIG / "fig4_dose.pdf", bbox_inches="tight")
fig.savefig(FIG / "fig4_dose.png", bbox_inches="tight")
plt.close(fig)

# Figure 1: overall framework (local vector equivalent; see P8 audit for the
# recorded fallback from GPT image generation, which needs extra credits).
fig, ax = plt.subplots(figsize=(6.8, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")


def box(x, y, w, h, text, fc, fs=8):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor="#333333", lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#333333"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.16, label, ha="center", fontsize=6.5, color="#333333")


box(0.15, 1.5, 1.7, 1.0, "Timestamped\nevent stream\n$e_k=(u,v,t,f)$", "#e8f0fe")
box(2.25, 2.5, 1.9, 0.9, "ANN teacher\nfixed ReLU message\nstate $s_v(k)$", "#f7f7f7")
box(2.25, 0.5, 1.9, 0.9, "Converted SNN\ngraded IF path\nstate $\\hat{s}_v(k)$", "#fdeaea")
box(4.65, 1.5, 1.8, 1.0, "Topology-change\ntracker $\\delta_v(k)$,\n$\\|\\Delta A_k\\|$", "#fff4d6")
box(6.85, 2.5, 1.9, 0.9, "Gate: $\\delta_v>\\gamma$\nrecalibrate $\\theta_v$,\ndecay residual", "#fdeaea")
box(6.85, 0.5, 1.9, 0.9, "Shared discrete\nmemory + readout\n$b+E s$", "#e8f0fe")
box(8.95, 1.5, 0.9, 1.0, "scores\nMRR / $\\varepsilon_k$", "#eaf7ea")
arrow(1.85, 2.0, 2.25, 2.95); arrow(1.85, 2.0, 2.25, 0.95)
arrow(4.15, 2.95, 4.65, 2.0); arrow(4.15, 0.95, 4.65, 2.0)
arrow(6.45, 2.0, 6.85, 2.95, "trigger")
arrow(6.45, 2.0, 6.85, 0.95)
arrow(4.15, 2.95, 6.85, 0.95, "ANN state")
arrow(4.15, 0.95, 6.85, 0.95, "SNN state")
arrow(8.75, 2.95, 8.95, 2.0); arrow(8.75, 0.95, 8.95, 2.0)
ax.text(5.0, 3.85, "TCAR: topology-change-aware residual carry-over for GNN→SNN conversion",
        ha="center", fontsize=9, weight="bold")
fig.tight_layout()
fig.savefig(FIG / "fig1_framework.pdf", bbox_inches="tight")
fig.savefig(FIG / "fig1_framework.png", bbox_inches="tight")
plt.close(fig)

(FIG / "figure-sources.json").write_text(json.dumps({
    "fig1": "Local vector schematic; P8 records the fallback from GPT image generation (extra credit cost not in the user's authorization list).",
    "fig2": "results/p4_runs/*.json (agreement, mean_epsilon, 5 seeds, Wikipedia)",
    "fig3": "results/p4_runs/*.json (mean_epsilon, recalibration_rate, 3 streams)",
    "fig4": "results/bound-check/*_trace.json (delta, epsilon_M0, epsilon_C4; fixed pre-registered bins)",
    "note": "Every plotted value is read from real run artifacts; no target value is plotted as a measurement."
}, indent=2) + "\n", encoding="utf-8")
print("wrote figures:", [p.name for p in sorted(FIG.glob("fig*"))])
