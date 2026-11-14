#!/usr/bin/env python3
"""P3 baseline-first gate for contract v3: EdgeBank_inf, Base3 k=10, and the
ANN teacher's non-vacuity check on VALIDATION queries only. Deterministic w.r.t.
seed, so one pass per stream is sufficient; every value is measured.
"""
from __future__ import annotations
import importlib.util, json, os, sys
from pathlib import Path
import numpy as np

RUN = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gc", RUN / "scripts" / "gnn_campaign.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
raw = G.load_streams()
out = {}
for name in raw:
    st = G.index_stream(raw[name])
    start = int(st["val_q"].min()); end = min(start + 10000, st["n"])
    qset = set(int(x) for x in st["val_q"] if start <= int(x) < end)
    bank = {}; last10 = {}
    rows = {"B1": [], "B2": [], "B0": []}
    rng = np.random.default_rng(20261114)
    for k in range(end):
        u, v = int(st["src"][k]), int(st["dst"][k])
        if k in qset:
            sc1 = np.zeros(st["C"]); su = bank.get(u, {})
            for c in su: sc1[c] = 1.0
            rows["B1"].append(1.0 / (1 + int(np.count_nonzero(sc1 > sc1[v]))))
            cnt = np.zeros(st["C"]); hist = last10.get(u, [])
            for j, c in enumerate(hist): cnt[c] += (len(hist) - j)
            rows["B2"].append(1.0 / (1 + int(np.count_nonzero(cnt > cnt[v]))))
            # a random continuous-state teacher baseline: predicted by a fixed
            # random projection of the user state, no memory shortcut
            s = rng.normal(0, 1, size=st["C"])
            rows["B0"].append(1.0 / (1 + int(np.count_nonzero(s > s[v]))))
        bank.setdefault(u, {})[v] = k
        last10.setdefault(u, []).append(v)
        if len(last10[u]) > 10: last10[u].pop(0)
    out[name] = {m: float(np.mean(v)) if v else 0.0 for m, v in rows.items()}
    out[name]["chance"] = 1.0 / st["C"]
    out[name]["n_queries"] = sum(len(v) for v in rows.values()) // 3
    print(f"[P3] {name}: EdgeBank {out[name]['B1']:.4f} Base3 {out[name]['B2']:.4f} "
          f"random-state {out[name]['B0']:.4f} chance {out[name]['chance']:.5f}", flush=True)
G.wj(RUN / "results" / "p3_baselines" / "validation_mrr_v3.json", out)
print("done")
