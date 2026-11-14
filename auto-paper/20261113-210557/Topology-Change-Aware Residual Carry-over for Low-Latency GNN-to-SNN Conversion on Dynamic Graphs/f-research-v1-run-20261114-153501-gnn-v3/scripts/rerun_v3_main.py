#!/usr/bin/env python3
"""Contract v3, correction cycle C10/C11: reuse the cached calibrated teachers,
select gamma per stream on VALIDATION under a pre-registered cost band, then
re-run the full main matrix and auxiliary sweeps with the repaired DCGS coder.
No teacher is retrained; no result is reused from the pre-repair campaign.
"""
from __future__ import annotations
import importlib.util, json, os, sys, time
from pathlib import Path
import numpy as np

RUN = Path(__file__).resolve().parents[1]
R = RUN / "results"
spec = importlib.util.spec_from_file_location("gc", RUN / "scripts" / "gnn_campaign.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

STREAMS = ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
SEEDS = [41, 42, 43, 44, 45]
GAMMAS = [0.5]            # cheap delta trigger is kept but nearly inactive
TAUS = [0.20, 0.28, 0.32, 0.35, 0.37, 0.40, 0.42, 0.45, 0.48, 0.50, 0.60, 0.80, 1e9]  # C15 finer grid for bimodal ||dA|| streams

t0 = time.time()
raw = G.load_streams()
st = {k: G.index_stream(v) for k, v in raw.items()}
graph = {k: G.build_graph_state(st[k]) for k in STREAMS}
teach = np.load(R / "p3_teachers" / "teachers_v3.npy", allow_pickle=True).item()
print("loaded", len(teach), "cached teachers", flush=True)

# ---------------- validation gamma selection with a cost band ----------------
sel = {}
for name in STREAMS:
    seed = 41
    M = teach[f"{name}_s{seed}"]
    cand = []
    for gamma in GAMMAS:
        for tau in TAUS:
            cfg = dict(stream=name, T=4, gamma=gamma, tau=tau,
                       percentile=0.999, window=1500)
            r = G.evaluate(st[name], M, *graph[name], seed, cfg, st[name]["val_q"], "validation")
            m0 = r["methods"]["M0"]
            cand.append({"gamma": gamma, "tau": tau, "agreement": m0["agreement"],
                         "epsilon": m0["mean_epsilon"], "trigger": m0["recalibration_rate"]})
    band = [c for c in cand if 0.05 <= c["trigger"] <= 0.20]
    if band:
        chosen = max(band, key=lambda c: (c["agreement"], -c["epsilon"]))
    else:
        # The 20% cost ceiling is a HARD constraint, not a preference: when no
        # candidate falls inside the 5-20% band, pick the most active candidate
        # that still respects the ceiling. (C11b repair.)
        eligible = [c for c in cand if c["trigger"] <= 0.20]
        chosen = (max(eligible, key=lambda c: c["trigger"]) if eligible
                  else min(cand, key=lambda c: c["trigger"]))
    sel[name] = {"gamma": chosen["gamma"], "tau": chosen["tau"], "T": 4,
                 "percentile": 0.999,
                 "validation_agreement": chosen["agreement"],
                 "validation_trigger_rate": chosen["trigger"],
                 "cost_band": "5%-20% of events, pre-registered on validation",
                 "trigger_definition": "delta_v(k) > gamma OR ||Delta A_k|| > tau (C14)",
                 "candidates": cand}
    print(f"[select] {name}: gamma={chosen['gamma']} tau={chosen['tau']} "
          f"trig={chosen['trigger']:.3f} agree={chosen['agreement']:.4f}", flush=True)
G.wj(R / "p4_validation" / "gamma_selection_v3.json", sel)

# ---------------- main matrix ----------------
allruns = []
for name in STREAMS:
    for seed in SEEDS:
        M = teach[f"{name}_s{seed}"]
        cfg = dict(stream=name, T=4, gamma=sel[name]["gamma"],
                   tau=sel[name]["tau"], percentile=sel[name]["percentile"], window=10000)
        r = G.evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "test")
        allruns.append(r)
        m0 = r["methods"]["M0"]
        print(f"[main] {name} s{seed} M0={m0['agreement']:.4f} eps={m0['mean_epsilon']:.4f} "
              f"ev={m0['graded_events_per_event']:.2f} trig={m0['recalibration_rate']:.3f}", flush=True)
G.wj(R / "aggregated.json", {"runs": allruns, "generated": G.now(),
                             "contract": "v3, cycles C10-C14, repaired DCGS ladder + measured operator-change gate"})

# ---------------- auxiliary sweeps ----------------
name = "wikipedia"; seed = 41; M = teach[f"{name}_s{seed}"]
g0 = sel[name]["gamma"]; tau0 = sel[name]["tau"]
aux = {"T_sweep": [], "architecture": [], "calibration": [], "robustness": [],
       "aggregator": [], "bound_and_spikes": []}
for T in [1, 2, 4, 8, 16]:
    aux["T_sweep"].append(G.evaluate(st[name], M, *graph[name], seed,
                                     dict(stream=name, T=T, gamma=g0, tau=tau0, window=3000),
                                     st[name]["test_q"], "aux"))
for L in [1, 2, 3]:
    aux["architecture"].append(G.evaluate(st[name], M, *graph[name], seed,
                                          dict(stream=name, layers=L, gamma=g0, tau=tau0, window=3000),
                                          st[name]["test_q"], "aux"))
for pct in [0.90, 0.95, 0.99, 0.999]:
    aux["calibration"].append(G.evaluate(st[name], M, *graph[name], seed,
                                         dict(stream=name, percentile=pct, gamma=g0, tau=tau0, window=3000),
                                         st[name]["test_q"], "aux"))
for drop in [0.05, 0.10, 0.20]:
    aux["robustness"].append(G.evaluate(st[name], M, *graph[name], seed,
                                        dict(stream=name, edge_dropout=drop, gamma=g0, tau=tau0, window=3000),
                                        st[name]["test_q"], "aux"))
for ag in ["mean", "max", "gated"]:
    aux["aggregator"].append(G.evaluate(st[name], M, *graph[name], seed,
                                        dict(stream=name, aggregator=ag, gamma=g0, tau=tau0, window=3000),
                                        st[name]["test_q"], "aux"))
for extra in [dict(noise=0.01), dict(dt_perturb=0.1), dict(shift=0.5), dict(use_agg=False)]:
    cfg = dict(stream=name, gamma=g0, tau=tau0, window=3000); cfg.update(extra)
    aux["bound_and_spikes"].append(G.evaluate(st[name], M, *graph[name], seed, cfg,
                                              st[name]["test_q"], "aux"))
G.wj(R / "p4_auxiliary" / "sweeps_v3.json", {"generated": G.now(), **aux})
print("[aux] done", flush=True)
print("ALL done", round(time.time() - t0, 1), flush=True)
