#!/usr/bin/env python3
"""P3-P5 experimental campaign for TCAR (contract v2).

Every reported number is produced by actually running this file on the frozen
public event streams. No result is hardcoded.

Design (contract v2):
  * FIXED random nonlinear message dynamics (a reservoir-style ReLU path) is
    the object that is converted to spikes. It is shared by ANN and SNN.
  * A learned linear readout plus an exact discrete historical-edge memory
    feature produce the candidate scores. The memory lookup is an integer
    index, shared identically by ANN and SNN, and is NOT converted.
  * The primary metric is conversion fidelity (teacher-to-SNN decision
    agreement), NOT absolute predictive MRR. See guidance-v2.md.

Phases: prepare / train / p3 / validate / test / all
Env: CTDG_STREAM_DIR, CTDG_ENRON_ZIP, TCAR_QUICK=1 for a 1-seed 1-stream iteration.
"""
from __future__ import annotations
import hashlib, json, math, os, sys, time, zipfile
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parents[1]
RESULTS = RUN / "results"
INPUTS = RUN / "inputs"
D = 16
ALPHA = 0.30                 # state update coefficient; rho = 1 - ALPHA = 0.70
LAM = 1.00                   # state readout strength (substantive, not a tie-break)
READOUT_GAIN = 100.0         # makes the learned state term comparable to the memory term
RCLIP = 5.0                  # bounded readout to keep scores finite
SEEDS = [41] if os.environ.get("TCAR_QUICK") else [41, 42, 43, 44, 45]
STREAMS = ["wikipedia"] if os.environ.get("TCAR_QUICK") else ["wikipedia", "mooc", "enron"]
WINDOW = 10000
GAMMA_GRID = [0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
T_GRID = [1, 2, 4, 8]
PCT_GRID = [0.90, 0.95, 0.99]
METHODS = ["C0", "C1", "C2", "C3", "C4", "M0", "A1", "A2", "A3", "A4", "D1"]


def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- data
def load_streams():
    sd = Path(os.environ["CTDG_STREAM_DIR"])
    out = {}
    for name in ["wikipedia", "mooc"]:
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
                    if len(p) < 6:
                        continue
                    rows.append((float(p[3]), int(p[5]), int(p[1]), int(p[2])))
        rows.sort()
        n = len(rows)
        src = np.array([r[2] for r in rows], dtype=np.int64)
        items = np.array([r[3] for r in rows], dtype=np.int64)
        catalog = np.unique(items)
        off = int(src.max()) + 1
        imap = {int(c): off + j for j, c in enumerate(catalog)}
        dst = np.array([imap[int(c)] for c in items], dtype=np.int64)
        ts = np.array([r[0] for r in rows], dtype=np.float64)
        ntr, nva = int(0.70 * n), int(0.85 * n)
        rng = np.random.default_rng(20261114)
        val_q = np.sort(rng.choice(np.arange(ntr, nva), size=min(1024, nva - ntr), replace=False))
        test_q = np.sort(rng.choice(np.arange(nva, n), size=min(4096, n - nva), replace=False))
        np.savez_compressed(ep, src=src, dst=dst, ts=ts,
                            catalog=np.array([imap[int(c)] for c in catalog], dtype=np.int64),
                            val_q=val_q, test_q=test_q)
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


# --------------------------------------------------------- fixed message dynamics
def fixed_dynamics(st, W, P, upto):
    """Pre-compute PRE-event states for the training prefix and the end state.
    W and P are FIXED, so this trajectory is identical for ANN and SNN and does
    not depend on the learned readout (stable training, no leakage).
    """
    s = np.zeros((st["U"], D))
    S_pre = np.zeros((upto, D), dtype=np.float64)
    acts = np.zeros(upto, dtype=np.float64)
    acts_u = np.zeros(upto, dtype=np.int32)
    for k in range(upto):
        u, v = int(st["src"][k]), int(st["dst"][k])
        su = s[u]
        S_pre[k] = su
        a = np.maximum(W @ np.concatenate([su, P[v], [st["dt"][k]]]), 0.0)
        acts[k] = float(np.max(a)); acts_u[k] = u
        s[u] = np.clip((1 - ALPHA) * su + ALPHA * a, 0.0, 4.0)
    return S_pre, s.copy(), acts, acts_u


def train_readout(st, W, P, seed):
    """Learn only the linear readout E,b on top of the FIXED dynamics.
    Candidate set = target + all memory-hit items + sampled negatives, so the
    training competitors match the evaluation competitors.
    """
    rng = np.random.default_rng(seed)
    ntr = int(st["val_q"].min())
    S_pre, state_end, acts, acts_u = fixed_dynamics(st, W, P, ntr)
    E = rng.normal(0, 0.05, size=(st["C"], D))
    b = np.zeros(st["C"])
    bank = {}
    lr = 0.02
    losses = []
    for k in range(ntr):
        u, v = int(st["src"][k]), int(st["dst"][k])
        su = S_pre[k]
        mem = np.zeros(st["C"])
        for c, kk in bank.get(u, {}).items():
            mem[c] = 1.0 / (1.0 + (k - kk))
        hits = list(bank.get(u, {}).keys())
        neg = rng.integers(0, st["C"], size=32)
        cand = np.unique(np.concatenate([[v], hits, neg]).astype(np.int64))
        sc = mem[cand] + LAM * np.clip(E[cand] @ su + b[cand], -1.0, 1.0)
        sc -= sc.max()
        q = np.exp(sc); q /= q.sum()
        jv = int(np.where(cand == v)[0][0])
        dsc = q.copy(); dsc[jv] -= 1.0
        losses.append(-math.log(max(q[jv], 1e-12)))
        for j, c in enumerate(cand):
            E[c] -= lr * LAM * np.clip(dsc[j] * su, -1.0, 1.0)
            b[c] -= 0.2 * lr * LAM * dsc[j]
        bank.setdefault(u, {})[v] = k
    # Rescale the learned readout so that the converted state materially
    # influences the candidate ranking; otherwise the discrete memory term
    # dominates and conversion fidelity is trivially 1 for every method.
    E = E * READOUT_GAIN
    b = b * READOUT_GAIN
    return dict(W=W, P=P, E=E, b=b, state=state_end,
                acts=acts, acts_u=acts_u,
                bank={int(u): {int(c): int(kk) for c, kk in d.items()} for u, d in bank.items()},
                loss_first=float(np.mean(losses[:500])), loss_last=float(np.mean(losses[-500:])))


def make_fixed_matrices(st, seed):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.12, size=(D, 2 * D + 1))
    P = rng.normal(0, 0.12, size=(st["C"], D))
    return W, P


# ------------------------------------------------------------------- calibration
_CAL = {}


def calibration(st, tch, key, pct):
    ck = (key, pct)
    if ck in _CAL:
        return _CAL[ck]
    acts, acts_u = tch["acts"], tch["acts_u"]
    theta_global = max(float(np.quantile(acts, pct)), 1e-4)
    theta_node = np.full(st["U"], theta_global)
    order = np.argsort(acts_u, kind="stable")
    counts = np.bincount(acts_u, minlength=st["U"])
    offs = np.concatenate([[0], np.cumsum(counts)])
    sa = acts[order]
    for u in range(st["U"]):
        seg = sa[offs[u]:offs[u + 1]]
        if seg.size:
            theta_node[u] = max(float(np.quantile(seg, pct)), 1e-4)
    _CAL[ck] = (theta_global, theta_node)
    return _CAL[ck]


# ------------------------------------------------------------------- conversion
def if_encode(a, theta, v, T):
    # Soft-reset IF rate coding with residual carry-over. The pilot showed that
    # clipping at theta hurts the (smaller) node-local thresholds more than the
    # global one, so clipping is removed; see correction-ledger.md cycle C7.
    v = v + 0.0
    spikes = np.zeros_like(a)
    for _ in range(T):
        v = v + a / max(theta, 1e-6)
        sp = np.floor(v + 1e-12)
        v = v - sp
        spikes += sp
    return spikes * theta / T, v


def quantize(a, theta, T):
    return np.floor(a / max(theta, 1e-6) * T + 0.5) * theta / T


def evaluate_window(st, tch, seed, cfg, query_ids, phase):
    W, P, E, b = tch["W"], tch["P"], tch["E"], tch["b"]
    T = int(cfg["T"]); gamma = float(cfg["gamma"]); pct = float(cfg["percentile"])
    start = int(query_ids.min()); end = min(start + WINDOW, st["n"])
    theta_global, theta_node = calibration(st, tch, f"{cfg['stream']}_s{seed}", pct)
    s_ann = tch["state"].copy()

    qset = set(int(x) for x in query_ids if start <= int(x) < end)
    methods = list(METHODS)
    states = {m: s_ann.copy() for m in methods}
    resid = {m: np.zeros(D) for m in methods}
    resid_node = {m: np.zeros((st["U"], D)) for m in methods}
    th_node = {m: np.full(st["U"], theta_global) for m in methods}
    for m in ["C1", "M0", "A1", "A2", "A3", "A4"]:
        th_node[m] = theta_node.copy()
    recent = {m: [[] for _ in range(st["U"])] for m in methods}
    neighbors = {u: set() for u in range(st["U"])}
    bank = {int(u): {int(c): int(kk) for c, kk in d.items()} for u, d in tch["bank"].items()}

    records = {m: [] for m in methods}
    ann_rec, cost = [], {m: 0 for m in methods}
    eps_trace = {m: [] for m in methods}
    delta_trace, a_trace = [], []

    for k in range(start, end):
        u, v = int(st["src"][k]), int(st["dst"][k])
        dt = st["dt"][k]
        su = s_ann[u]
        mem = np.zeros(st["C"])
        for c, kk in bank.get(u, {}).items():
            mem[c] = 1.0 / (1.0 + (k - kk))

        if k in qset:
            sc_ann = mem + LAM * np.clip(E @ su + b, -RCLIP, RCLIP)
            pred_ann = int(np.argmax(sc_ann))
            rank_ann = 1 + int(np.count_nonzero(sc_ann > sc_ann[v]))
            ann_rec.append(dict(k=k, pred=pred_ann, mrr=1.0 / rank_ann))
            for m in methods:
                sc = mem + LAM * np.clip(E @ states[m][u] + b, -RCLIP, RCLIP)
                pred = int(np.argmax(sc))
                rank = 1 + int(np.count_nonzero(sc > sc[v]))
                records[m].append(dict(k=k, agree=int(pred == pred_ann), mrr=1.0 / rank,
                                       mse=float(np.mean((sc - sc_ann) ** 2)),
                                       seg=(k - start) * 10 // WINDOW))

        nu = neighbors[u]; before = len(nu); nu.add(v)
        delta = (len(nu) - before) / max(before, 1)
        delta_trace.append(float(delta))
        triggered = delta > gamma

        a_ann = np.maximum(W @ np.concatenate([su, P[v], [dt]]), 0.0)
        a_trace.append(float(np.max(a_ann)))
        s_ann[u] = np.clip((1 - ALPHA) * su + ALPHA * a_ann, 0.0, 4.0)

        for m in methods:
            x = np.concatenate([states[m][u], P[v], [dt]])
            z = np.maximum(W @ x, 0.0)
            if m == "C0":
                dec, _ = if_encode(z, theta_global, np.zeros(D), T)
            elif m == "C1":
                dec, _ = if_encode(z, th_node[m][u], np.zeros(D), T)
            elif m == "C2":
                dec = quantize(z, th_node[m][u], T)
            elif m == "C3":
                dec = np.clip(quantize(np.minimum(z, th_node[m][u]), th_node[m][u], T), 0, None)
            elif m == "C4":       # CRPI-style per-node residual carry-over, no flush
                dec, resid_node[m][u] = if_encode(z, theta_global, resid_node[m][u], T)
            elif m == "D1":
                dec = quantize(z, theta_global, T)
            else:
                gate = triggered if m != "A1" else True
                if m == "A4":
                    gate = False                      # frozen topology: gate never fires
                if gate:
                    r = recent[m][u]
                    r.append(float(np.max(z)))
                    if len(r) > 32:
                        r.pop(0)
                    if m != "A3":
                        th_node[m][u] = max(float(np.quantile(r, pct)), 1e-4)
                    # Recalibrate the base/threshold and DECAY (not discard) the
                    # shared residual prefix. A full flush was piloted and made
                    # M0 worse at high delta; see correction-ledger.md cycle C8.
                    resid_node[m][u] = resid_node[m][u] * 0.5
                    cost[m] += 1
                v_in = np.zeros(D) if m == "A2" else resid_node[m][u]
                dec, resid_node[m][u] = if_encode(z, th_node[m][u], v_in, T)
            states[m][u] = np.clip((1 - ALPHA) * states[m][u] + ALPHA * dec, 0.0, 4.0)
            eps_trace[m].append(float(np.linalg.norm(states[m][u] - s_ann[u])))

        bank.setdefault(u, {})[v] = k

    out = {"phase": phase, "stream": cfg["stream"], "seed": seed, "cfg": cfg,
           "window": [start, end], "n_queries": len(ann_rec),
           "theta_global": theta_global, "methods": {}}
    ann_mrr = float(np.mean([r["mrr"] for r in ann_rec])) if ann_rec else 0.0
    out["ann_mrr"] = ann_mrr
    for m in methods:
        rr = records[m]
        if not rr:
            continue
        ag = [r["agree"] for r in rr]
        mrr = float(np.mean([r["mrr"] for r in rr]))
        first = [r["agree"] for r in rr if r["seg"] <= 1]
        last = [r["agree"] for r in rr if r["seg"] >= 8]
        out["methods"][m] = {
            "agreement": float(np.mean(ag)), "mrr": mrr,
            "mrr_retention": mrr / ann_mrr if ann_mrr > 0 else 0.0,
            "logit_mse": float(np.mean([r["mse"] for r in rr])),
            "decay_pp": (float(np.mean(first)) - float(np.mean(last))) * 100 if first and last else 0.0,
            "mean_epsilon": float(np.mean(eps_trace[m])),
            "recalibration_rate": cost[m] / (end - start),
            "n_queries": len(rr),
        }
        if phase == "test":
            write_json(RESULTS / f"p4_{m}" / f"{cfg['stream']}_s{seed}_queries.json",
                       [{"k": r["k"], "agree": r["agree"], "mrr": r["mrr"], "seg": r["seg"]} for r in rr])
    if phase == "test":
        write_json(RESULTS / "bound-check" / f"{cfg['stream']}_s{seed}_trace.json",
                   {"delta": delta_trace[::10], "act": a_trace[::10],
                    "epsilon_M0": eps_trace["M0"][::10], "epsilon_C4": eps_trace["C4"][::10],
                    "rho": 1 - ALPHA, "T": T, "note": "1:10 downsampled per-event instrumentation"})
    return out


# ------------------------------------------------------------------- baselines
def baselines(st, tch, query_ids):
    W, P, E, b = tch["W"], tch["P"], tch["E"], tch["b"]
    s_ann = tch["state"].copy()
    start = int(query_ids.min()); end = start + min(WINDOW, st["n"] - start)
    qset = set(int(x) for x in query_ids if start <= int(x) < end)
    bank = {int(u): {int(c): int(kk) for c, kk in d.items()} for u, d in tch["bank"].items()}
    seen = {int(u): set(d.keys()) for u, d in bank.items()}   # faithful EdgeBank_infty
    last10 = {}
    rows = {"B0": [], "B1": [], "B2": []}
    for k in range(start, end):
        u, v = int(st["src"][k]), int(st["dst"][k])
        mem = np.zeros(st["C"])
        for c, kk in bank.get(u, {}).items():
            mem[c] = 1.0 / (1.0 + (k - kk))
        if k in qset:
            sc0 = mem + LAM * np.clip(E @ s_ann[u] + b, -RCLIP, RCLIP)
            rows["B0"].append(1.0 / (1 + int(np.count_nonzero(sc0 > sc0[v]))))
            sc1 = np.zeros(st["C"])
            for c in seen.get(u, set()):
                sc1[c] = 1.0
            rows["B1"].append(1.0 / (1 + int(np.count_nonzero(sc1 > sc1[v]))))
            cnt = np.zeros(st["C"])
            hist = last10.get(u, [])
            for j, c in enumerate(hist):
                cnt[c] += (len(hist) - j)
            rows["B2"].append(1.0 / (1 + int(np.count_nonzero(cnt > cnt[v]))))
        su = s_ann[u]
        a = np.maximum(W @ np.concatenate([su, P[v], [st["dt"][k]]]), 0.0)
        s_ann[u] = np.clip((1 - ALPHA) * su + ALPHA * a, 0.0, 4.0)
        seen.setdefault(u, set()).add(v)
        bank.setdefault(u, {})[v] = k
        last10.setdefault(u, []).append(v)
        if len(last10[u]) > 10:
            last10[u].pop(0)
    return {m: (float(np.mean(r)) if r else 0.0) for m, r in rows.items()}


# ------------------------------------------------------------------------- main
def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    t0 = time.time()
    d = load_streams()
    st = {k: index_stream(v) for k, v in d.items()}
    write_json(RESULTS / "p3_data" / "stream-summary.json",
               {"created_at": now(), "streams": {k: {
                   "n_events": int(len(s["src"])), "catalog": int(s["catalog"].size),
                   "val_query_n": int(s["val_q"].size), "test_query_n": int(s["test_q"].size)}
                   for k, s in d.items()}})

    if phase in ("train", "all", "p3"):
        teachers = {}
        for name in STREAMS:
            for seed in SEEDS:
                W, P = make_fixed_matrices(st[name], seed)
                tch = train_readout(st[name], W, P, seed)
                teachers[f"{name}_s{seed}"] = tch
                write_json(RESULTS / "p3_teachers" / f"{name}_s{seed}.json",
                           {"stream": name, "seed": seed,
                            "loss_first": tch["loss_first"], "loss_last": tch["loss_last"]})
                print(f"[train] {name}_s{seed} loss {tch['loss_first']:.4f} -> {tch['loss_last']:.4f}", flush=True)
        np.save(RESULTS / "p3_teachers" / "teachers.npy", np.array([teachers], dtype=object), allow_pickle=True)
    if phase == "train":
        print("done", round(time.time() - t0, 1)); return
    teachers = np.load(RESULTS / "p3_teachers" / "teachers.npy", allow_pickle=True).item()

    if phase in ("p3", "all"):
        gate = {}
        for name in STREAMS:
            gate[name] = {f"s{seed}": baselines(st[name], teachers[f"{name}_s{seed}"], st[name]["val_q"])
                          for seed in SEEDS}
        write_json(RESULTS / "p3_baselines" / "validation_mrr.json", gate)
        print("[p3]", json.dumps(gate, ensure_ascii=False), flush=True)
        if phase == "p3":
            print("done", round(time.time() - t0, 1)); return

    if phase in ("validate", "all"):
        best = {}
        for name in STREAMS:
            cand = []
            for gamma in GAMMA_GRID:
                for pct in PCT_GRID:
                    vals, trig = [], []
                    for seed in SEEDS[:2]:
                        tch = teachers[f"{name}_s{seed}"]
                        r = evaluate_window(st[name], tch, seed,
                                            dict(stream=name, T=4, gamma=gamma, percentile=pct),
                                            st[name]["val_q"], "validation")
                        m0 = r["methods"].get("M0", {})
                        vals.append(m0.get("agreement", 0.0))
                        trig.append(m0.get("recalibration_rate", 1.0))
                    cand.append((float(np.mean(vals)), gamma, 4, pct, float(np.mean(trig))))
            # The contract's cost ceiling (<=20% of events) is a pre-registered
            # selection constraint, so inadmissible configurations are removed
            # on VALIDATION before ranking by fidelity. Test is still read once.
            eligible = [c for c in cand if c[4] <= 0.20]
            if not eligible:
                raise SystemExit(f"no gamma/percentile satisfies the 20% cost ceiling on {name}")
            eligible.sort(reverse=True)
            all_sorted = sorted(cand, reverse=True)
            best[name] = {"gamma": eligible[0][1], "T": 4, "percentile": eligible[0][3],
                          "validation_agreement": eligible[0][0],
                          "validation_trigger_rate": eligible[0][4],
                          "top5": [list(map(float, c)) for c in all_sorted[:5]]}
            print("[validate]", name, json.dumps(best[name], ensure_ascii=False), flush=True)
        write_json(RESULTS / "p4_validation" / "selected_hyperparameters.json", best)
        if phase == "validate":
            print("done", round(time.time() - t0, 1)); return

    if phase in ("test", "all"):
        best = json.loads((RESULTS / "p4_validation" / "selected_hyperparameters.json").read_text())
        allruns = []
        for name in STREAMS:
            cfg = dict(stream=name, T=4, gamma=best[name]["gamma"], percentile=best[name]["percentile"])
            for seed in SEEDS:
                tch = teachers[f"{name}_s{seed}"]
                r = evaluate_window(st[name], tch, seed, cfg, st[name]["test_q"], "test")
                allruns.append(r)
                write_json(RESULTS / "p4_runs" / f"{name}_s{seed}.json", r)
                m0 = r["methods"].get("M0", {}); c4 = r["methods"].get("C4", {})
                print(f"[test] {name} s{seed} M0={m0.get('agreement',0):.4f} "
                      f"C4={c4.get('agreement',0):.4f} decayM0={m0.get('decay_pp',0):.2f} "
                      f"decayC4={c4.get('decay_pp',0):.2f} trig={m0.get('recalibration_rate',0):.3f}",
                      flush=True)
        write_json(RESULTS / "aggregated.json", {"runs": allruns, "generated_at": now()})
    print("done", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
