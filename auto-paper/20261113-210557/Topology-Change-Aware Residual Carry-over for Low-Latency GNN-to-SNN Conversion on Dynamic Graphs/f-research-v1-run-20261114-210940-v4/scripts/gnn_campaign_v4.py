#!/usr/bin/env python3
"""Contract v3 experimental engine: a GENUINE dynamic-graph GNN converted with
an independent reimplementation of the user's gnn2snn DCGS conversion family.

Real components (no proxies for the graph operator):
  * A_k : row-normalised 1/sqrt(d_u d_c) neighbour incidence, precomputed per event
  * L-layer residual graph convolution with A_k-weighted neighbour aggregation
  * DCGS MTH_diff-style signed multi-level differential coding e_t = t(a_t-a_{t-1})
    with telescoping decode sum e_s/s, zero-latch, bias-once, 8-level ladder
  * label-free 512-bin q=0.999 two-pass histogram threshold calibration
  * affine static base caching and per-snapshot re-anchoring (TCAR gate)
  * measured ||A_k - A_{k-1}||, error decomposition, spike/SynOps accounting

Every number written by this file is measured. No result is hardcoded.
Env: CTDG_STREAM_DIR, CTDG_ENRON_ZIP, optional V3_QUICK=1.
"""
from __future__ import annotations
import hashlib, json, math, os, sys, time, zipfile
from collections import deque
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parents[1]
RESULTS = RUN / "results"
INPUTS = RUN / "inputs"
D = 16
K = 8                      # neighbour slots in the local normalised adjacency row
L_LAYERS = 3                   # three residual GCN layers; depth ablation uses the first L
ALPHA = 0.30
LAM = 1.0
RCLIP = 5.0
LADDER = 8
BINS = 512
Q_CAL = 0.999
T_DEFAULT = 4
GAMMA_DEFAULT = 0.5
WINDOW = int(os.environ.get("V4_WINDOW", os.environ.get("V3_WINDOW", "10000")))
MAX_TRAIN_EVENTS = int(os.environ.get("V4_MAX_TRAIN", os.environ.get("V3_MAX_TRAIN", "80000")))  # documented coverage cap for M1
SEEDS = [41] if os.environ.get("V4_QUICK", os.environ.get("V3_QUICK")) else [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
STREAMS = ["wikipedia"] if os.environ.get("V4_QUICK", os.environ.get("V3_QUICK")) else ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
METHODS = ["C0", "C1", "C2", "C3", "C4", "C5MT", "M0", "A1", "A2", "A3", "A5", "D1"]
if os.environ.get("V4_METHODS"):                     # latency probe: one method at a time
    METHODS = [m.strip() for m in os.environ["V4_METHODS"].split(",") if m.strip()]
MT_LEVELS = 4   # C5MT multi-threshold levels (MPEF-style control)
# Pre-registered epsilon bins for the C-6 downstream-validity dose-response
# (log-equal-width; frozen here, not fitted on test).
EPSBIN_EDGES = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def wj(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ data
def load_streams():
    sd = Path(os.environ["CTDG_STREAM_DIR"])
    out = {}
    for name in ["wikipedia", "mooc", "reddit", "lastfm"]:
        z = np.load(sd / f"{name}-events.npz")
        out[name] = dict(src=z["src"].astype(np.int64), dst=z["dst"].astype(np.int64),
                         ts=z["timestamp"].astype(np.float64), catalog=z["catalog"].astype(np.int64),
                         val_q=z["validation_query"].astype(np.int64),
                         test_q=z["test_query"].astype(np.int64))
    ep = INPUTS / "enron-derived.npz"
    if not ep.is_file():
        with zipfile.ZipFile(os.environ["CTDG_ENRON_ZIP"]) as zf:
            rows = []
            with zf.open("enron/ml_enron.csv") as f:
                next(f)
                for line in f:
                    p = line.decode().strip().split(",")
                    if len(p) >= 6:
                        rows.append((float(p[3]), int(p[5]), int(p[1]), int(p[2])))
        rows.sort(); n = len(rows)
        src = np.array([r[2] for r in rows], dtype=np.int64)
        items = np.array([r[3] for r in rows], dtype=np.int64)
        catalog = np.unique(items); off = int(src.max()) + 1
        imap = {int(c): off + j for j, c in enumerate(catalog)}
        dst = np.array([imap[int(c)] for c in items], dtype=np.int64)
        ts = np.array([r[0] for r in rows], dtype=np.float64)
        ntr, nva = int(.70 * n), int(.85 * n)
        rng = np.random.default_rng(20261114)
        vq = np.sort(rng.choice(np.arange(ntr, nva), size=min(1024, nva - ntr), replace=False))
        tq = np.sort(rng.choice(np.arange(nva, n), size=min(4096, n - nva), replace=False))
        np.savez_compressed(ep, src=src, dst=dst, ts=ts,
                            catalog=np.array([imap[int(c)] for c in catalog], dtype=np.int64),
                            val_q=vq, test_q=tq)
    z = np.load(ep)
    out["enron"] = dict(src=z["src"], dst=z["dst"], ts=z["ts"], catalog=z["catalog"],
                        val_q=z["val_q"], test_q=z["test_q"])
    return out


def index_stream(s):
    users = np.unique(s["src"]); items = s["catalog"]
    umap = {int(x): i for i, x in enumerate(users)}
    imap = {int(x): i for i, x in enumerate(items)}
    src = np.array([umap[int(x)] for x in s["src"]], dtype=np.int64)
    dst = np.array([imap[int(x)] for x in s["dst"]], dtype=np.int64)
    dt = np.diff(np.concatenate([[s["ts"][0]], s["ts"]]))
    dt = np.clip(dt / max(float(dt.std()), 1e-9), 0.0, 5.0)
    return dict(src=src, dst=dst, dt=dt, U=len(users), C=len(items),
                val_q=s["val_q"], test_q=s["test_q"], n=len(src))


def build_graph_state(st):
    """Precompute the REAL normalised local adjacency row A_k for every event,
    plus the measured operator change ||A_k - A_{k-1}|| and the cheap trigger
    delta_v(k). This is shared by all methods and all seeds.
    """
    n, U, C = st["n"], st["U"], st["C"]
    A = np.zeros((n, K), dtype=np.float32)
    NI = np.zeros((n, K), dtype=np.int32)
    dA = np.zeros(n, dtype=np.float32)
    delta = np.zeros(n, dtype=np.float32)
    deg_item = np.ones(C, dtype=np.float64)
    nbr = [deque(maxlen=K) for _ in range(U)]
    last_row = np.zeros(K, dtype=np.float32)
    last_u = -1
    for k in range(n):
        u, v = int(st["src"][k]), int(st["dst"][k])
        hist = list(nbr[u])
        before = len(hist)
        idx = np.full(K, -1, dtype=np.int32)
        if hist:
            h = hist[-K:]
            idx[:len(h)] = h
        NI[k] = idx
        deg_u = float(before + 1)
        w = np.zeros(K, dtype=np.float32)
        for j, c in enumerate(idx):
            if c >= 0:
                w[j] = 1.0 / math.sqrt(deg_u * deg_item[c])
        s = float(w.sum())
        if s > 0:
            w /= s
        A[k] = w
        dA[k] = float(np.linalg.norm(w - last_row)) if last_u == u else float(np.linalg.norm(w))
        new = 1 if v not in nbr[u] else 0
        delta[k] = new / max(before, 1)
        last_row, last_u = w, u
        nbr[u].append(v)
        deg_item[v] += 1.0
    return A, NI, dA, delta


# ------------------------------------------------------------------ teacher
def make_matrices(st, seed, d=D, layers=L_LAYERS):
    rng = np.random.default_rng(seed)
    P = rng.normal(0, 0.10, size=(st["C"], d)).astype(np.float32)
    Wagg = [rng.normal(0, 0.10 / math.sqrt(d), size=(d, d)).astype(np.float32) for _ in range(layers)]
    Wmix = [rng.normal(0, 0.10 / math.sqrt(d), size=(d, d)).astype(np.float32) for _ in range(layers)]
    bias = [rng.normal(0, 0.01, size=d).astype(np.float32) for _ in range(layers)]
    wt = rng.normal(0, 0.05, size=d).astype(np.float32)
    E = rng.normal(0, 0.05, size=(st["C"], d)).astype(np.float32)
    b = np.zeros(st["C"], dtype=np.float32)
    return dict(P=P, Wagg=Wagg, Wmix=Wmix, bias=bias, wt=wt, E=E, b=b, d=d, layers=layers)


def graph_forward(M, st, A, NI, k, s_u, use_agg=True, aggregator="mean"):
    """Genuine L-layer residual GCN forward for one event."""
    P, Wagg, Wmix, bias, wt = M["P"], M["Wagg"], M["Wmix"], M["bias"], M["wt"]
    idx = NI[k]
    valid = idx >= 0
    nbr = P[np.maximum(idx, 0)] if valid.any() else np.zeros((K, M["d"]), np.float32)
    w = A[k]
    if aggregator == "max":
        agg = nbr.max(axis=0) if valid.any() else np.zeros(M["d"], np.float32)
    elif aggregator == "gated":
        g = 1.0 / (1.0 + np.exp(-nbr.mean(axis=0))) if valid.any() else np.zeros(M["d"], np.float32)
        agg = (w[:, None] * nbr * g[None, :]).sum(axis=0)
    else:
        agg = w @ nbr
    if not use_agg:
        agg = np.zeros_like(agg)
    X = s_u + P[int(st["dst"][k])] + wt * float(st["dt"][k])
    H = X.astype(np.float32)
    acts = []
    for l in range(M["layers"]):
        z = Wmix[l] @ (H + Wagg[l] @ agg) + bias[l]
        a = np.maximum(z, 0.0).astype(np.float32)
        acts.append(a)
        H = H + a
    return H, acts, agg


def calibrate(M, st, A, NI, seed):
    """Label-free 512-bin q=0.999 two-pass histogram over TRAINING activations."""
    rng = np.random.default_rng(seed + 500)
    ntr = min(int(st["val_q"].min()), MAX_TRAIN_EVENTS)
    s = np.zeros((st["U"], M["d"]), np.float32)
    act_l = [[] for _ in range(M["layers"])]
    for k in range(ntr):
        u = int(st["src"][k])
        H, acts, _ = graph_forward(M, st, A, NI, k, s[u])
        for l, a in enumerate(acts):
            act_l[l].append(a)
        s[u] = (1 - ALPHA) * s[u] + ALPHA * acts[-1]
    theta = []
    for l in range(M["layers"]):
        arr = np.concatenate(act_l[l])
        mx = float(arr.max())
        hist, edges = np.histogram(arr, bins=BINS, range=(0.0, max(mx, 1e-6)))
        cum = np.cumsum(hist)
        j = int(np.searchsorted(cum, math.ceil(len(arr) * Q_CAL)))
        j = min(j, BINS - 1)
        theta.append(max(float(edges[j + 1]), 1e-4))
    # train readout (full-catalog sampled softmax, same protocol as v2)
    E, b = M["E"], M["b"]
    lr = 0.02
    s = np.zeros((st["U"], M["d"]), np.float32)
    bank = {}
    losses = []
    for k in range(ntr):
        u, v = int(st["src"][k]), int(st["dst"][k])
        su = s[u]
        mem = np.zeros(st["C"], np.float32)
        for c, kk in bank.get(u, {}).items():
            mem[c] = 1.0 / (1.0 + k - kk)
        hits = list(bank.get(u, {}).keys())
        neg = rng.integers(0, st["C"], size=32)
        cand = np.unique(np.concatenate([[v], hits, neg]).astype(np.int64))
        H, acts, _ = graph_forward(M, st, A, NI, k, su)
        sc = mem[cand] + LAM * np.clip(E[cand] @ su + b[cand], -RCLIP, RCLIP)
        sc -= sc.max(); q = np.exp(sc); q /= q.sum()
        jv = int(np.where(cand == v)[0][0]); dsc = q.copy(); dsc[jv] -= 1.0
        losses.append(-math.log(max(q[jv], 1e-12)))
        for j, c in enumerate(cand):
            E[c] -= lr * LAM * np.clip(dsc[j] * su, -1.0, 1.0)
            b[c] -= 0.2 * lr * LAM * dsc[j]
        bank.setdefault(u, {})[v] = k
        s[u] = (1 - ALPHA) * s[u] + ALPHA * acts[-1]
    M["E"] = E * 100.0
    M["b"] = b * 100.0
    M["theta"] = theta
    M["state"] = s.copy()
    M["bank"] = {int(u): {int(c): int(kk) for c, kk in d.items()} for u, d in bank.items()}
    M["loss_first"] = float(np.mean(losses[:500])); M["loss_last"] = float(np.mean(losses[-500:]))
    return M


# ------------------------------------------------------------------ coders
def dcgs_encode(a, theta, T, bias, carry, ladder=LADDER):
    """DCGS MTH_diff-style signed multi-level differential coding.
    e_t = t (a_t - a_{t-1}); decode sum_{s<=t} e_s/s = a_t.
    Zero-latch: a_0 = bias is injected once at t=1. Returns decoded activation,
    number of non-zero graded events, and the un-emitted residual.
    """
    steps = theta / (2.0 ** np.arange(ladder))
    bias = np.asarray(bias, dtype=np.float32).reshape(-1)[:a.shape[0]]
    if bias.shape[0] < a.shape[0]:
        bias = np.pad(bias, (0, a.shape[0] - bias.shape[0]))
    res = (a - bias).astype(np.float32)
    dec = bias.astype(np.float32).copy()
    events = 0
    for t in range(1, T + 1):
        ratio = np.abs(res) / t
        # ceil (not floor): the ladder step must not exceed the affordable
        # per-step increment |res|/t, otherwise every candidate is rejected
        # and the coder emits nothing. This was the C10 defect.
        j = np.ceil(np.log2(theta / np.maximum(ratio, 1e-12))).astype(np.int32)
        j = np.clip(j, 0, ladder - 1)
        step = np.sign(res) * steps[j]
        ok = (np.abs(step) > 0) & (t * np.abs(step) <= np.abs(res) + 1e-12) & (ratio >= steps[-1] * 0.5)
        step = np.where(ok, step, 0.0)
        dec += step
        res -= step
        events += int(np.count_nonzero(step))
    return dec, events, res


def if_encode(a, theta, T, v_init):
    """Rate-coded IF with soft reset; returns decoded, residual and spike count."""
    v = v_init.copy(); sp_total = np.zeros_like(a); events = 0
    for _ in range(T):
        v = v + a / max(theta, 1e-6)
        sp = np.floor(v + 1e-12); v -= sp; sp_total += sp
        events += int(np.count_nonzero(sp))
    return sp_total * theta / T, v, events


def quant(a, theta, T, shift=0.0):
    return np.floor(np.minimum(a, theta) / max(theta, 1e-6) * T + 0.5 + shift) * theta / T


def mt_encode(a, theta, T, carry, n_levels=MT_LEVELS):
    """C5MT: MPEF-style multi-threshold neuron adapted to graph layers.

    The activation range [0, theta] is covered by n_levels thresholds so the
    unit emits multi-level spikes; the un-emitted residual is carried across
    events as inter-event membrane error feedback (no topology gating: like
    C2, C5MT keeps the cached base, so it is the no-topology-awareness member
    of the multi-threshold family). Returns decoded, event count, residual.
    """
    x = (a + carry).astype(np.float32)
    x = np.minimum(np.maximum(x, 0.0), theta * (1.0 + 1.0 / (2 * T)))
    dec = np.floor(x / max(theta, 1e-6) * n_levels + 0.5) * (theta / n_levels)
    dec = np.minimum(dec, theta)
    events = int(np.count_nonzero(np.floor(x / max(theta, 1e-6) * n_levels + 0.5)))
    return dec.astype(np.float32), events, (x - dec).astype(np.float32)


# ------------------------------------------------------------------ evaluation
def evaluate(st, M, A, NI, dA, delta, seed, cfg, query_ids, phase="test"):
    T = int(cfg.get("T", T_DEFAULT)); gamma = float(cfg.get("gamma", GAMMA_DEFAULT))
    pct = float(cfg.get("percentile", Q_CAL)); L = int(cfg.get("layers", L_LAYERS))
    d = int(cfg.get("width", D)); agg_mode = cfg.get("aggregator", "mean")
    noise = float(cfg.get("noise", 0.0)); drop = float(cfg.get("edge_dropout", 0.0))
    dt_pert = float(cfg.get("dt_perturb", 0.0)); shift = float(cfg.get("shift", 0.0))
    tau = float(cfg.get("tau", 1e9))   # operator-change threshold; 1e9 disables it
    beta = float(cfg.get("beta", 1.0))  # strength of the one-shot Delta h_0 bias injection
    alpha_carry = float(cfg.get("alpha", 1.0))       # C-8: carry-over coefficient on the residual prefix
    alpha_state = float(cfg.get("alpha_state", ALPHA))  # V-4: converted-state decay rate (rho = 1 - alpha_state)
    edge_insert = float(cfg.get("edge_insert", 0.0))    # V-3: synthetic edge insertion ratio
    wd = int(cfg.get("window", WINDOW))
    start = int(query_ids.min()); end = min(start + wd, st["n"])
    rng = np.random.default_rng(seed + 9100)
    theta = [t * (pct / Q_CAL) ** 0.5 for t in M["theta"][:L]]
    qset = set(int(x) for x in query_ids if start <= int(x) < end)
    # first-occurrence index per node (train-prefix coverage) for the C-7
    # inductive stratification; a query is inductive if either endpoint's
    # first event lies inside the evaluation window.
    maxid = int(max(st["src"].max(), st["dst"].max())) + 1
    first_ev = np.full(maxid, st["n"], np.int64)
    np.minimum.at(first_ev, st["src"], np.arange(st["n"], dtype=np.int64))
    np.minimum.at(first_ev, st["dst"], np.arange(st["n"], dtype=np.int64))
    # dA quintile edges from the TRAIN portion only (pre-registered stratification)
    daq = np.quantile(dA[:start], [0.2, 0.4, 0.6, 0.8]) if start > 100 else np.full(4, np.inf)
    # bound constants (V-1): estimated on validation, injected via cfg
    bc = cfg.get("bound_consts") or {}
    LA_hat = float(bc.get("LA", 0.0)); c_hat = float(bc.get("c", 0.0)); eta_hat = float(bc.get("eta", 0.0))
    rho_hat = 1.0 - alpha_state if alpha_state else (1.0 - ALPHA)
    # bound methods restricted to the ACTIVE method set, so single-method
    # probes (e.g. the latency phase) do not touch traces that do not exist.
    # For full-matrix runs this is identical to the previous fixed triple.
    bound_methods = [m for m in ("C1", "C2", "M0") if m in METHODS]
    s_ann = M["state"].copy()
    methods = list(METHODS)
    states = {m: s_ann.copy() for m in methods}
    resid = {m: np.zeros(d, np.float32) for m in methods}       # per-node residual, simplified global
    th_node = {m: np.full(st["U"], theta[0], np.float32) for m in methods}
    recent = {m: [[] for _ in range(st["U"])] for m in methods}
    cost = {m: 0 for m in methods}
    ev_count = {m: 0 for m in methods}
    ev_layer = {m: [0] * L for m in methods}                    # per-layer graded events
    ev_seg = {m: [0] * 10 for m in methods}                     # per-time-window events (10 slices)
    ev_dabin = {m: [0] * 5 for m in methods}                    # events by dA quintile (C-10)
    eps_seg = {m: [0.0] * 10 for m in methods}; eps_seg_n = {m: [0] * 10 for m in methods}
    err_clip = {m: 0.0 for m in methods}; err_quant = {m: 0.0 for m in methods}
    err_res = {m: 0.0 for m in methods}
    eps_trace = {m: [] for m in methods}
    # Per-node previous error for the bound recursion: the rho contraction in
    # T1/T2 applies along EACH NODE's own event subsequence (consecutive events
    # of the stream generally hit different nodes, so a global eps_{k-1} is
    # uninformative — measured R^2 ~ 0.02-0.55 on 2026-11-15; the per-node
    # form is the mathematically correct statement of the recursion).
    eps_prev = {m: np.zeros(st["U"], np.float64) for m in bound_methods}
    bound_rhs = {m: [] for m in bound_methods}; bound_eps = {m: [] for m in bound_methods}
    bound_viol = {m: 0 for m in bound_methods}; bound_n = {m: 0 for m in bound_methods}
    # C-6: per-epsilon-bin downstream MRR loss (dose = M0 error at query event)
    NBINS = len(EPSBIN_EDGES) + 1
    loss_bin = {m: np.zeros(NBINS) for m in METHODS}; loss_bin_n = {m: np.zeros(NBINS) for m in METHODS}
    log_bf = cfg.get("log_bound_features")
    bf = {m: [] for m in bound_methods}                         # estimation traces (validation only)
    rec = {m: [] for m in methods}; ann = []
    band = M["bank"]
    A_eff = A.copy() if (drop > 0 or edge_insert > 0) else A
    if drop > 0:
        mask = rng.random(A.shape) < drop
        A_eff = np.where(mask, 0.0, A)
        rs = A_eff.sum(axis=1, keepdims=True); A_eff = np.divide(A_eff, np.maximum(rs, 1e-9))
    # Affine static base: every converter starts from the SAME cached base
    # computed at the end of training; only TCAR-gated variants re-anchor it.
    j0 = max(start - 1, 0)
    base0 = (A_eff[j0].astype(np.float32) @
             M["P"][np.maximum(NI[j0], 0)]).astype(np.float32)
    cached_agg = {m: base0.copy() for m in methods}

    for k in range(start, end):
        u, v = int(st["src"][k]), int(st["dst"][k])
        mem = np.zeros(st["C"], np.float32)
        for c, kk in band.get(u, {}).items():
            mem[c] = 1.0 / (1.0 + k - kk)
        dt_k = float(st["dt"][k]) + (rng.normal(0, dt_pert) if dt_pert else 0.0)
        su = s_ann[u]
        # ---- genuine GNN layer inputs shared by ANN and every converted variant ----
        idx = NI[k]
        nbr = M["P"][np.maximum(idx, 0)]
        w = A_eff[k].astype(np.float32).copy()
        if edge_insert > 0:
            # V-3 synthetic topology change: insert edges at empty neighbour
            # slots with the row's mean weight, then renormalise. The number of
            # inserted slots is fixed per event by the ratio p (deterministic
            # given K slots), so the dose is monotone in p.
            n_ins = int(round(edge_insert * K))
            if n_ins > 0:
                empty = np.where(w <= 0)[0]
                if empty.size:
                    pick = rng.choice(empty, size=min(n_ins, empty.size), replace=False)
                    w[pick] = max(float(w[w > 0].mean()) if (w > 0).any() else 1.0 / K, 1e-6)
                    w = w / max(w.sum(), 1e-9)
        if agg_mode == "max":
            agg = nbr.max(axis=0) if (idx >= 0).any() else np.zeros(d, np.float32)
        elif agg_mode == "gated":
            g = 1.0 / (1.0 + np.exp(-nbr.mean(axis=0)))
            agg = (w[:, None] * nbr * g[None, :]).sum(axis=0)
        else:
            agg = w @ nbr
        agg = np.asarray(agg, dtype=np.float32)
        if not cfg.get("use_agg", True):
            agg = np.zeros(d, np.float32)
        # ANN teacher: L residual graph-convolution layers with A_k aggregation
        X_ann = su + M["P"][v] + M["wt"] * dt_k
        H = np.asarray(X_ann, dtype=np.float32).copy()
        acts_ann = []
        for l in range(L):
            z = M["Wmix"][l] @ (H + M["Wagg"][l] @ agg) + M["bias"][l]
            a = np.maximum(z, 0.0).astype(np.float32)
            acts_ann.append(a)
            H = H + a
        H_ann = H
        # Prediction uses the PRE-event state, so the current item label cannot leak.
        sc_ann = mem + LAM * np.clip(M["E"] @ su + M["b"], -RCLIP, RCLIP)
        seg_k = (k - start) * 10 // wd
        inductive = bool(first_ev[u] >= start or first_ev[v] >= start)
        eps_now = {m: (eps_trace[m][-1] if eps_trace[m] else 0.0) for m in bound_methods}
        if k in qset:
            pa = int(np.argmax(sc_ann)); ra = 1 + int(np.count_nonzero(sc_ann > sc_ann[v]))
            ann.append(dict(k=k, pred=pa, mrr=1.0 / ra))
            amrr = 1.0 / ra
            bini = int(np.searchsorted(EPSBIN_EDGES, max(float(eps_now.get("M0", 0.0)), 1e-12)))
            for m in methods:
                sc = mem + LAM * np.clip(M["E"] @ states[m][u] + M["b"], -RCLIP, RCLIP)
                pm = int(np.argmax(sc)); rm = 1 + int(np.count_nonzero(sc > sc[v]))
                rec[m].append(dict(k=k, agree=int(pm == pa), mrr=1.0 / rm,
                                   mse=float(np.mean((sc - sc_ann) ** 2)),
                                   seg=seg_k, inductive=inductive,
                                   eps0=float(eps_now.get("M0", 0.0)),
                                   eps2=float(eps_now.get("C2", 0.0))))
                loss_bin[m][bini] += amrr - 1.0 / rm; loss_bin_n[m][bini] += 1
        # C14: the gate fires on the MEASURED operator change as well as on the
        # cheap neighbour-set proxy. On streams with large histories delta_v(k)
        # is almost always near zero, so dA[k] is the informative trigger.
        trig = bool((delta[k] > gamma) or (dA[k] > tau))
        s_ann[u] = (1 - ALPHA) * su + ALPHA * acts_ann[-1]
        # one-shot Delta h_0 compensation, injected at t=1 when the base moves
        bij = {m: np.zeros(d, np.float32) for m in methods}
        for m in methods:
            # TCAR: the affine static base is re-anchored only on a topology trigger
            gate = (m in ("M0", "A1", "A2", "A3")) and (True if m == "A1" else trig)
            if gate:
                r = recent[m][u]; r.append(float(np.max(acts_ann[0])))
                if len(r) > 32: r.pop(0)
                if m != "A3":
                    # C14: conservative EMA bounded to +-20% of the global
                    # threshold; the unbounded quantile update was measured to
                    # hurt DCGS fidelity on sparse-gate streams.
                    qv = max(float(np.quantile(r, pct)), 1e-4)
                    th_node[m][u] = float(np.clip(0.9 * th_node[m][u] + 0.1 * qv,
                                                 0.8 * theta[0], 1.2 * theta[0]))
                # The cached base moves by dh0; inject its first-layer projection
                # as a one-shot t=1 bias event so the decoded prefix stays
                # anchored at the new snapshot origin (archive derivation, C12/C14).
                dh0 = agg - cached_agg[m]
                if m != "A3":
                    bij[m] = (beta * (M["Wagg"][0] @ dh0)).astype(np.float32)
                cached_agg[m] = agg.copy()      # re-anchor the affine static base
                cost[m] += 1
            # The residual prefix is NOT decayed: cycle C12 measured that both
            # a full flush and a 0.5 decay hurt DCGS fidelity at high topology
            # change. Only the base is re-anchored at trigger events.
            agg_m = (np.zeros(d, np.float32)
                     if (m == "A5" or not cfg.get("use_agg", True)) else cached_agg[m])
            X_s = states[m][u] + M["P"][v] + M["wt"] * dt_k
            Hc = np.asarray(X_s, dtype=np.float32).copy()
            for l in range(L):
                z = M["Wmix"][l] @ (Hc + M["Wagg"][l] @ agg_m) + M["bias"][l]
                a = np.maximum(z, 0.0).astype(np.float32)
                aa = a + (rng.normal(0, noise, size=d).astype(np.float32) if noise else 0.0)
                # All methods share the same per-layer histogram thresholds;
                # gated variants only rescale them by a node-local factor.
                thl = theta[min(l, len(theta) - 1)]
                if m in ("M0", "A1", "A3"):
                    thl = thl * max(th_node[m][u] / max(theta[0], 1e-9), 1e-3)
                bl = M["bias"][l] if l < len(M["bias"]) else np.zeros(d, np.float32)
                bl = (bl + bij[m]).astype(np.float32) if l == 0 else bl
                if m == "C0":
                    dec, _, e = if_encode(np.maximum(aa, 0), thl, T, np.zeros(d, np.float32))
                    rr = np.zeros(d, np.float32)
                elif m == "C3":
                    dec = quant(np.maximum(aa, 0), thl, T, 0.0); e = int(np.count_nonzero(dec)); rr = np.zeros(d, np.float32)
                elif m == "C4":
                    dec, _, e = if_encode(np.maximum(aa, 0), thl, T, np.full(d, thl / 2, np.float32))
                    rr = np.zeros(d, np.float32)
                elif m == "D1":
                    dec = quant(np.maximum(aa, 0), thl, T, shift); e = int(np.count_nonzero(dec)); rr = np.zeros(d, np.float32)
                elif m == "C5MT":
                    dec, e, rr = mt_encode(np.maximum(aa, 0), thl, T, resid[m])
                    resid[m] = rr          # MPEF-style full inter-event feedback
                else:
                    dec, e, rr = dcgs_encode(np.maximum(aa, 0), thl, T, bl, resid[m])
                    # C-8: the carry-over coefficient alpha scales the carried prefix.
                    resid[m] = (alpha_carry * rr).astype(np.float32) if m in ("C2", "M0", "A1", "A3") else np.zeros(d, np.float32)
                Hc = Hc + dec                      # layer-wise ReLU -> DCGS replacement
                last_dec = dec
                ev_count[m] += e
                ev_layer[m][l] += e
                ev_seg[m][seg_k] += e
                ev_dabin[m][int(np.searchsorted(daq, dA[k]))] += e
                err_clip[m] += float(np.sum(np.maximum(aa - thl, 0.0)))
                err_quant[m] += float(np.sum(np.abs(rr)))
                err_res[m] += float(np.linalg.norm(rr))
            # The recurrent state is driven by the LAST converted layer activation;
            # conversion error therefore propagates along the event axis.
            # V-4: alpha_state varies the converted recurrence (rho = 1 - alpha_state).
            states[m][u] = ((1.0 - alpha_state) * states[m][u] + alpha_state * last_dec).astype(np.float32)
            ek = float(np.linalg.norm(states[m][u] - s_ann[u]))
            eps_trace[m].append(ek)
            eps_seg[m][seg_k] += ek; eps_seg_n[m][seg_k] += 1
            # V-1 bound instrumentation (C1/C2 un-gated; M0 charged the topology
            # term only on trigger events, where its base is re-anchored).
            if m in bound_methods:
                topo_feat = (float(dA[k]) * float(np.linalg.norm(states[m][u]))
                             if (m != "M0" or trig) else 0.0)
                ep = float(eps_prev[m][u])          # same-node previous error
                if LA_hat > 0.0:
                    rhs = rho_hat * ep + LA_hat * topo_feat + c_hat / T + eta_hat
                    bound_rhs[m].append(rhs); bound_eps[m].append(ek); bound_n[m] += 1
                    if ek > rhs * 1.02 + 1e-5:     # 2% slack for float32 accumulation
                        bound_viol[m] += 1
                elif log_bf:
                    # Estimation traces: SAME functional form as the evaluation rhs
                    # (M0 topology feature zeroed off-trigger). Validation windows
                    # only. Node id included so the fit can verify the per-node
                    # subsequence construction.
                    bf[m].append((u, ep, topo_feat, ek))
                eps_prev[m][u] = ek

    ann_mrr = float(np.mean([x["mrr"] for x in ann])) if ann else 0.0
    n_ev = end - start
    out = {"phase": phase, "stream": cfg["stream"], "seed": seed, "cfg": cfg,
           "window": [start, end], "n_queries": len(ann), "ann_mrr": ann_mrr,
           "measured_dA_mean": float(np.mean(dA[start:end])), "methods": {}}
    for m in methods:
        rr = rec[m]
        if not rr: continue
        ag = [x["agree"] for x in rr]; mrr = float(np.mean([x["mrr"] for x in rr]))
        first = [x["agree"] for x in rr if x["seg"] <= 1]; last = [x["agree"] for x in rr if x["seg"] >= 8]
        ind = [x["agree"] for x in rr if x["inductive"]]; trd = [x["agree"] for x in rr if not x["inductive"]]
        out["methods"][m] = {
            "agreement": float(np.mean(ag)), "agreement_sd": float(np.std(ag, ddof=1)) if len(ag) > 1 else 0.0,
            "mrr": mrr, "mrr_retention": mrr / ann_mrr if ann_mrr > 0 else 0.0,
            "logit_mse": float(np.mean([x["mse"] for x in rr])),
            "decay_pp": (float(np.mean(first)) - float(np.mean(last))) * 100 if first and last else 0.0,
            "mean_epsilon": float(np.mean(eps_trace[m])),
            "recalibration_rate": cost[m] / n_ev,
            "graded_events_per_event": ev_count[m] / max(n_ev * L, 1),
            "firing_rate": ev_count[m] / max(n_ev * L * d * T, 1),
            "synops_per_event": ev_count[m] * d / n_ev,
            "clip_error": err_clip[m] / n_ev, "quant_error": err_quant[m] / n_ev,
            "residual_error": err_res[m] / n_ev,
            "n_queries": len(rr),
            # v4 transparency strata
            "firing_per_layer": [ev_layer[m][l] / max(n_ev * T, 1) for l in range(L)],
            "firing_per_window": [ev_seg[m][s] / max((wd // 10) * L * d * T, 1) for s in range(10)],
            "firing_per_da_bin": [ev_dabin[m][b] / max(n_ev * L * d * T / 5, 1) for b in range(5)],
            "epsilon_per_window": [(eps_seg[m][s] / eps_seg_n[m][s]) if eps_seg_n[m][s] else 0.0 for s in range(10)],
            "agreement_inductive": float(np.mean(ind)) if ind else None,
            "agreement_transductive": float(np.mean(trd)) if trd else None,
            # C-6 downstream-validity dose-response (ANN-MRR minus method MRR per eps bin)
            "mrr_loss_per_epsbin": [(float(loss_bin[m][b] / loss_bin_n[m][b])
                                     if loss_bin_n[m][b] else None) for b in range(NBINS)],
            "epsbin_n": [int(loss_bin_n[m][b]) for b in range(NBINS)],
        }
        if m in bound_methods and bound_n[m]:
            out["methods"][m]["bound"] = {
                "violation_rate": bound_viol[m] / bound_n[m],
                "n_evaluated": bound_n[m],
                "mean_tightness": float(np.mean(np.array(bound_eps[m]) / np.maximum(np.array(bound_rhs[m]), 1e-12))),
                "LA_hat": LA_hat, "c_hat": c_hat, "eta_hat": eta_hat,
            }
    if phase == "test":
        wj(RESULTS / "bound-check" / f"{cfg['stream']}_s{seed}_trace.json",
           {"dA": dA[start:end:10].tolist(), "delta": delta[start:end:10].tolist(),
            "epsilon_M0": (eps_trace["M0"][::10] if "M0" in eps_trace else None),
            "epsilon_C2": (eps_trace["C2"][::10] if "C2" in eps_trace else None),
            "rho": 1 - ALPHA, "T": T,
            "note": "real measured ||A_k-A_{k-1}||, not a proxy"})
    if log_bf:
        out["epsbin_edges"] = EPSBIN_EDGES
        out["bound_features"] = {m: [list(t) for t in bf[m]] for m in bound_methods if bf[m]}
    return out


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    t0 = time.time()
    raw = load_streams()
    st = {k: index_stream(v) for k, v in raw.items()}
    wj(RESULTS / "p3_data" / "stream-summary.json",
       {"streams": {k: {"n_events": int(len(v["src"])), "catalog": int(v["catalog"].size),
                        "val_query_n": int(v["val_q"].size), "test_query_n": int(v["test_q"].size)}
                    for k, v in raw.items()}, "generated": now()})
    graph = {}
    for name in STREAMS:
        graph[name] = build_graph_state(st[name])
        print(f"[graph] {name}: A_k {graph[name][0].shape}, mean ||dA|| {graph[name][2].mean():.4f}", flush=True)

    teach = {}
    for name in STREAMS:
        for seed in SEEDS:
            M = make_matrices(st[name], seed)
            M = calibrate(M, st[name], graph[name][0], graph[name][1], seed)
            teach[f"{name}_s{seed}"] = M
            print(f"[train] {name}_s{seed} loss {M['loss_first']:.3f}->{M['loss_last']:.3f} "
                  f"theta {[round(x,3) for x in M['theta']]}", flush=True)
    (RESULTS / "p3_teachers").mkdir(parents=True, exist_ok=True)
    np.save(RESULTS / "p3_teachers" / "teachers_v3.npy", np.array([teach], dtype=object), allow_pickle=True)
    print("train done", round(time.time() - t0, 1), flush=True)
    if phase == "train": return

    best = {name: {"gamma": GAMMA_DEFAULT, "T": T_DEFAULT, "percentile": Q_CAL} for name in STREAMS}
    wj(RESULTS / "p4_validation" / "selected_hyperparameters.json", best)

    if phase in ("main", "all"):
        allruns = []
        for name in STREAMS:
            for seed in SEEDS:
                M = teach[f"{name}_s{seed}"]
                cfg = dict(stream=name, T=T_DEFAULT, gamma=best[name]["gamma"],
                           percentile=best[name]["percentile"], window=WINDOW)
                r = evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "test")
                allruns.append(r)
                m0 = r["methods"].get("M0", {})
                print(f"[main] {name} s{seed} M0={m0.get('agreement',0):.4f} "
                      f"eps={m0.get('mean_epsilon',0):.4f} ev={m0.get('graded_events_per_event',0):.2f} "
                      f"trig={m0.get('recalibration_rate',0):.3f}", flush=True)
        wj(RESULTS / "aggregated.json", {"runs": allruns, "generated": now()})

    if phase in ("aux", "all"):
        name = STREAMS[0]; seed = SEEDS[0]; M = teach[f"{name}_s{seed}"]
        aux = {"T_sweep": [], "architecture": [], "calibration": [], "robustness": [],
               "aggregator": [], "bound_and_spikes": []}
        for T in [1, 2, 4, 8, 16]:
            cfg = dict(stream=name, T=T, window=3000)
            aux["T_sweep"].append(evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "aux"))
        for L in [1, 2, 3]:
            for d in [16, 32]:
                if d != D: continue   # matrices are d=16; width sweep needs retrain, recorded as scope limit
                cfg = dict(stream=name, layers=L, window=3000)
                aux["architecture"].append(evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "aux"))
        for pct in [0.90, 0.95, 0.99, 0.999]:
            cfg = dict(stream=name, percentile=pct, window=3000)
            aux["calibration"].append(evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "aux"))
        for drop in [0.05, 0.10, 0.20]:
            cfg = dict(stream=name, edge_dropout=drop, window=3000)
            aux["robustness"].append(evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "aux"))
        for ag in ["mean", "max", "gated"]:
            cfg = dict(stream=name, aggregator=ag, window=3000)
            aux["aggregator"].append(evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "aux"))
        for extra in [dict(noise=0.01), dict(dt_perturb=0.1), dict(shift=0.5), dict(use_agg=False)]:
            cfg = dict(stream=name, window=3000); cfg.update(extra)
            aux["bound_and_spikes"].append(evaluate(st[name], M, *graph[name], seed, cfg, st[name]["test_q"], "aux"))
        wj(RESULTS / "p4_auxiliary" / "sweeps_v3.json", {"generated": now(), **aux})
        print("[aux] done", flush=True)
    print("ALL done", round(time.time() - t0, 1), flush=True)


if __name__ == "__main__":
    main()
