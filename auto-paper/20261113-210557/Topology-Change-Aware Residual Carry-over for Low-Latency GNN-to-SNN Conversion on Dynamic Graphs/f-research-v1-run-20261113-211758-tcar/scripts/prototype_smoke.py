#!/usr/bin/env python3
"""P2 smoke prototype: verify the full code path on a small Wikipedia event subset.

This is an ENVIRONMENT / PROTOCOL CHECK, not a scientific result. No claim in the
manuscript may cite these numbers. Coverage is explicitly `smoke/2000-events`.
It exercises: frozen stream loading, node-state recursion, conversion-friendly
ReLU teacher, rate-coded IF conversion with label-free percentile calibration,
cross-event residual carry-over, topology-change tracking, per-event error
instrumentation, MPS operator probing, and the R63-style artifact contract.
"""
from __future__ import annotations
import hashlib, json, os, time
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parents[1]
OUT = RUN / "results" / "p2-prototype"
OUT.mkdir(parents=True, exist_ok=True)

# Local frozen copy is supplied at run time via CTDG_FROZEN_STREAM so that no
# machine-specific path is baked into a file that is published to a public repo.
DATA = Path(os.environ.get("CTDG_FROZEN_STREAM", "inputs/wikipedia-events.npz"))

CONFIG = {
    "purpose": "P2 environment and protocol smoke check; NOT a reported scientific result",
    "stream": "Zenodo 10.5281/zenodo.7213796 wikipedia-events.npz; local frozen copy supplied via CTDG_FROZEN_STREAM",
    "coverage": "smoke/2000-events",
    "n_events": 2000,
    "hidden_dim": 16,
    "n_candidates": 64,
    "T_micro_steps": 4,
    "calibration_percentile": 0.999,
    "seed": 41,
    "device_policy": "MPS preferred for supported operators; main smoke loop on CPU; CPU fallback recorded",
    "split_policy": "no train/val/test split used; smoke subset only; P2 freezes real identities separately",
}
cfg_bytes = (json.dumps(CONFIG, sort_keys=True, ensure_ascii=False) + "\n").encode()
(OUT / "config.json").write_bytes(cfg_bytes)
(OUT / "config.sha256").write_text(hashlib.sha256(cfg_bytes).hexdigest() + "\n", encoding="utf-8")

t0 = time.time()
rng = np.random.default_rng(CONFIG["seed"])
D, C, T, N = CONFIG["hidden_dim"], CONFIG["n_candidates"], CONFIG["T_micro_steps"], CONFIG["n_events"]

if not DATA.is_file():
    raise SystemExit(f"frozen stream missing: {DATA}")
z = np.load(DATA)
src_all, dst_all, ts_all = z["src"], z["dst"], z["timestamp"]
src, dst, ts = src_all[:N].astype(np.int64), dst_all[:N].astype(np.int64), ts_all[:N].astype(np.float64)
uniq = np.unique(np.concatenate([src, dst]))
V = len(uniq)
src = np.searchsorted(uniq, src)
dst = np.searchsorted(uniq, dst)
catalog = np.arange(min(C, V), dtype=np.int64)

# Conversion-friendly ANN teacher: ReLU/clip only, no softmax, no BN at conversion time.
W = rng.normal(0, 0.15, size=(2 * D + 1, D)).astype(np.float64)
E = rng.normal(0, 0.15, size=(len(catalog), D)).astype(np.float64)
dt = np.diff(np.concatenate([[ts[0]], ts]))
dt = dt / max(float(dt.std()), 1e-6)
dt = np.clip(dt, 0.0, 5.0).reshape(-1, 1)

s_ann = np.zeros((V, D), dtype=np.float64)
s_snn_hard = np.zeros((V, D), dtype=np.float64)
s_snn_carry = np.zeros((V, D), dtype=np.float64)

# Label-free calibration: pass teacher activations once over the same subset.
acts = []
s_tmp = np.zeros((V, D), dtype=np.float64)
for k in range(N):
    u, v = int(src[k]), int(dst[k])
    x = np.concatenate([s_tmp[u], s_tmp[v], dt[k]])
    acts.append(np.maximum(x @ W, 0.0))
    m = acts[-1]
    s_tmp[u] = np.clip(s_tmp[u] + m, 0.0, 10.0)
    s_tmp[v] = np.clip(s_tmp[v] + m, 0.0, 10.0)
act_arr = np.concatenate(acts)
theta = max(float(np.quantile(act_arr, CONFIG["calibration_percentile"])), 1e-6)
scale = 1.0 / theta

neighbors: dict[int, set] = {}
v_carry = np.zeros(D, dtype=np.float64)

rows = []
for k in range(N):
    u, v = int(src[k]), int(dst[k])
    x = np.concatenate([s_ann[u], s_ann[v], dt[k]])
    z_ann = np.maximum(x @ W, 0.0)

    # rate-coded IF conversion with soft (subtractive) reset, T micro-steps.
    # Constant current z*scale is integrated T times against threshold 1;
    # decoding spikes/(T*scale) recovers z. Residual potential is carried across
    # events for the CRPI-style control and hard-reset for the C0-style control.
    z_pos = np.maximum(z_ann, 0.0)

    def if_convert(residual):
        v = residual.copy()
        spikes = np.zeros(D, dtype=np.float64)
        for _ in range(T):
            v = v + z_pos * scale
            s = np.floor(v + 1e-12)
            v = v - s
            spikes += s
        return spikes / (T * scale), v

    snn_hard, _ = if_convert(np.zeros(D, dtype=np.float64))
    snn_carry, v_carry = if_convert(v_carry)

    s_ann[u] = np.clip(s_ann[u] + z_ann, 0.0, 10.0)
    s_ann[v] = np.clip(s_ann[v] + z_ann, 0.0, 10.0)
    s_snn_hard[u] = np.clip(s_snn_hard[u] + snn_hard, 0.0, 10.0)
    s_snn_hard[v] = np.clip(s_snn_hard[v] + snn_hard, 0.0, 10.0)
    s_snn_carry[u] = np.clip(s_snn_carry[u] + snn_carry, 0.0, 10.0)
    s_snn_carry[v] = np.clip(s_snn_carry[v] + snn_carry, 0.0, 10.0)

    # topology-change tracker over node neighbour sets
    nu, nv = neighbors.setdefault(u, set()), neighbors.setdefault(v, set())
    before_u, before_v = len(nu), len(nv)
    nu.add(v); nv.add(u)
    delta_v = (abs(len(nu) - before_u) + abs(len(nv) - before_v)) / max(before_u + before_v, 1)
    delta_a_proxy = delta_v  # normalised neighbour-set change as an operator-change proxy

    ann_score = s_ann[u] @ E.T
    hard_score = s_snn_hard[u] @ E.T
    carry_score = s_snn_carry[u] @ E.T
    rows.append({
        "event": k, "u": u, "v": v,
        "epsilon_hard": float(np.linalg.norm(s_snn_hard[u] - s_ann[u])),
        "epsilon_carry": float(np.linalg.norm(s_snn_carry[u] - s_ann[u])),
        "delta_v": float(delta_v), "delta_a_proxy": float(delta_a_proxy),
        "agree_hard": int(np.argmax(hard_score) == np.argmax(ann_score)),
        "agree_carry": int(np.argmax(carry_score) == np.argmax(ann_score)),
    })

with (OUT / "raw_results.jsonl").open("w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# MPS / CPU operator probe (separate from the smoke loop)
probe = {"python": os.sys.version.split()[0]}
try:
    import torch
    probe["torch"] = torch.__version__
    probe["mps_available"] = bool(torch.backends.mps.is_available())
    probe["cuda_available"] = bool(torch.cuda.is_available())
    if probe["mps_available"]:
        a = torch.randn(32, D, device="mps")
        probe["mps_matmul"] = bool(torch.isfinite(a @ torch.randn(D, D, device="mps")).all().item())
        probe["mps_relu"] = bool(torch.isfinite(torch.relu(a)).all().item())
    probe["cpu_matmul"] = True
except Exception as exc:  # record honestly, never fabricate a capability
    probe["torch_error"] = f"{type(exc).__name__}: {exc}"

metrics = {
    "status": "smoke_completed",
    "coverage": CONFIG["coverage"],
    "events_processed": int(N),
    "nodes_in_subset": int(V),
    "candidate_catalog_size": int(len(catalog)),
    "calibration_theta": theta,
    "calibration_activation_max": float(act_arr.max()),
    "clipping_rate": float((act_arr > theta).mean()),
    "agreement_hard_reset_fraction": float(np.mean([r["agree_hard"] for r in rows])),
    "agreement_global_carry_over_fraction": float(np.mean([r["agree_carry"] for r in rows])),
    "mean_epsilon_hard": float(np.mean([r["epsilon_hard"] for r in rows])),
    "mean_epsilon_carry": float(np.mean([r["epsilon_carry"] for r in rows])),
    "mean_delta_v": float(np.mean([r["delta_v"] for r in rows])),
    "wall_clock_seconds": round(time.time() - t0, 3),
    "device_probe": probe,
    "note": "Smoke numbers are NOT scientific results and must never appear in the manuscript as findings.",
}
(OUT / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "environment.json").write_text(json.dumps(probe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "END_OF_RUN_OK").write_text(
    f"completed smoke prototype at {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n", encoding="utf-8"
)
print(json.dumps(metrics, ensure_ascii=False, indent=2))
