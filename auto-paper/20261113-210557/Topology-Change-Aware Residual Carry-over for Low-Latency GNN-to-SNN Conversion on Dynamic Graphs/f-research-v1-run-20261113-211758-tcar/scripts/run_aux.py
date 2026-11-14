#!/usr/bin/env python3
"""P4 auxiliary rows: S1 T-sweep, S2 gamma-sweep, K1-K3 window-length checks.
All numbers come from evaluate_window on real frozen streams.
"""
from __future__ import annotations
import importlib.util, json, os, sys, time
from pathlib import Path
import numpy as np

RUN = Path(__file__).resolve().parents[1]
RESULTS = RUN / "results"
spec = importlib.util.spec_from_file_location("campaign", RUN / "scripts" / "run_campaign.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

d = C.load_streams()
st = {k: C.index_stream(v) for k, v in d.items()}
teachers = np.load(RESULTS / "p3_teachers" / "teachers.npy", allow_pickle=True).item()
best = json.loads((RESULTS / "p4_validation" / "selected_hyperparameters.json").read_text())
name = "wikipedia"
seed = 41
tch = teachers[f"{name}_s{seed}"]


def one(T, gamma, pct, window):
    C.WINDOW = window
    cfg = dict(stream=name, T=T, gamma=gamma, percentile=pct)
    r = C.evaluate_window(st[name], tch, seed, cfg, st[name]["test_q"], "aux")
    m0, c4 = r["methods"]["M0"], r["methods"]["C4"]
    return {"T": T, "gamma": gamma, "percentile": pct, "window": window,
            "n_queries": r["n_queries"],
            "M0_agreement": m0["agreement"], "C4_agreement": c4["agreement"],
            "M0_epsilon": m0["mean_epsilon"], "C4_epsilon": c4["mean_epsilon"],
            "M0_mrr_retention": m0["mrr_retention"],
            "M0_trigger_rate": m0["recalibration_rate"]}


t0 = time.time()
out = {"generated_at": C.now(), "stream": name, "seed": seed,
       "S1_T_sweep": [], "S2_gamma_sweep": [], "K_window_robustness": []}
g0, p0 = best[name]["gamma"], best[name]["percentile"]

for T in [1, 2, 4, 8]:
    out["S1_T_sweep"].append(one(T, g0, p0, 10000))
    print("[S1]", out["S1_T_sweep"][-1]["T"], round(out["S1_T_sweep"][-1]["M0_agreement"], 4), flush=True)
for g in C.GAMMA_GRID:
    out["S2_gamma_sweep"].append(one(4, g, p0, 10000))
    print("[S2]", g, round(out["S2_gamma_sweep"][-1]["M0_trigger_rate"], 3), flush=True)
for K in [1000, 5000, 10000]:
    out["K_window_robustness"].append(one(4, g0, p0, K))
    print("[K]", K, out["K_window_robustness"][-1]["n_queries"], flush=True)

C.WINDOW = 10000
C.write_json(RESULTS / "p4_auxiliary" / "sweeps.json", out)
print("done", round(time.time() - t0, 1))
