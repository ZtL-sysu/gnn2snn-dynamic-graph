#!/usr/bin/env python3
"""Contract v4 analysis (P5): executes the locked C-1 decision rule exactly once,
computes effect sizes, bound/E10 verdicts, theory-arm slope tests, strata, energy
accounting, and exports paper-ready tables. Every claim number is traceable to
results/aggregated.json (main matrix) or results/theory/*.json (arms).

Integrity checks at startup (ledger A2/A4/A5):
  * the locked C-1 rule sentence is found verbatim inside guidance-v4-amendment.md
  * bound-constants protocol hash matches the hash recorded at estimation time
  * v3 evidence manifest (audits/v3-evidence-hashes.json) still matches v3 files
"""
from __future__ import annotations
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parents[1]
R = RUN / "results"
GD = RUN.parent
V3 = GD / "f-research-v1-run-20261114-153501-gnn-v3"
STREAMS = ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
METHODS = ["C0", "C1", "C2", "C3", "C4", "C5MT", "M0", "A1", "A2", "A3", "A5", "D1"]
BOUND_METHODS = ["C1", "C2", "M0"]
D, L_LAYERS = 16, 3
E_AC_pJ, E_MAC_pJ = 0.9, 4.6          # Horowitz 2014, 45nm (constant table)
ANN_MACS_PER_EVENT = L_LAYERS * 2 * D * D
BOOT = 4000

LOCKED_RULE_SENTENCE = (
    "Estimator: per-seed mean epsilon_k per method per stream, seeds 41–50, paired within seed. "
    "Test: paired BCa bootstrap with 4,000 resamples on the per-seed paired differences epsilon_C2 "
    "minus epsilon_M0, plus a sign-flip permutation test; multiplicity control by Benjamini–Hochberg "
    "across the five streams at q less than 0.05."
)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def wj(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ------------------------------------------------------------- statistics
def bca_ci(d: np.ndarray, n_boot: int = BOOT, seed: int = 20261114):
    """BCa 95% CI for the mean of paired differences d (len 10)."""
    d = np.asarray(d, dtype=np.float64)
    n = len(d)
    theta = float(np.mean(d))
    rng = np.random.default_rng(seed)
    boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(n_boot)])
    z0 = _norm_ppf(float((boots < theta).mean()) or 1.0 / (2 * n_boot))
    jk = np.array([np.delete(d, i).mean() for i in range(n)])
    jk_mean = jk.mean()
    acc = float(((jk_mean - jk) ** 3).sum() / (6.0 * max(((jk_mean - jk) ** 2).sum(), 1e-18) ** 1.5))
    q = [0.025, 0.975]
    z = [_norm_ppf(x) for x in q]
    adj = [_norm_cdf(z0 + (z0 + zi) / (1 - acc * (z0 + zi))) for zi in z]
    lo, hi = (float(np.quantile(boots, a)) for a in adj)
    return {"theta": theta, "ci95": [lo, hi], "excludes_zero": bool(lo > 0 or hi < 0),
            "direction": "negative" if hi < 0 else ("positive" if lo > 0 else "straddles")}


def _norm_ppf(p):
    from math import erfc
    # Acklam's rational approximation (inverse normal CDF), sufficient for BCa
    if p <= 0 or p >= 1:
        p = min(max(p, 1e-12), 1 - 1e-12)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d_ = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
          3.754408661907416e+00]
    p_low, p_high = 0.02425, 1 - 0.02425
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d_[0] * q + d_[1]) * q + d_[2]) * q + d_[3]) * q + 1)
    if p > p_high:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
                ((((d_[0] * q + d_[1]) * q + d_[2]) * q + d_[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def _norm_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))


def signflip_p(d: np.ndarray):
    """Exact two-sided paired sign-flip p (enumerate 2^n patterns)."""
    d = np.asarray(d, dtype=np.float64)
    n = len(d)
    t_obs = abs(d.sum())
    signs = np.ones((2 ** n, n))
    for i in range(2 ** n):
        signs[i] = [1 if (i >> j) & 1 else -1 for j in range(n)]
    t = np.abs((signs * d).sum(axis=1))
    return float((t >= t_obs - 1e-15).mean())


def bh_adjust(pvals):
    p = np.asarray(pvals, dtype=np.float64)
    order = np.argsort(p)
    m = len(p)
    q = np.empty(m)
    prev = 1.0
    for rank in range(m, 0, -1):
        idx = order[rank - 1]
        prev = min(prev, p[idx] * m / rank)
        q[idx] = prev
    return q.tolist()


def cohens_dz(d):
    d = np.asarray(d, dtype=np.float64)
    return float(d.mean() / d.std(ddof=1)) if d.std(ddof=1) > 0 else 0.0


def prob_improvement(d, n_boot=BOOT, seed=20261114):
    d = np.asarray(d, dtype=np.float64)
    rng = np.random.default_rng(seed + 1)
    boots = np.array([d[rng.integers(0, len(d), len(d))].mean() > 0 for _ in range(n_boot)])
    return float(boots.mean())


def slope(xs, ys):
    xs = np.asarray(xs, dtype=np.float64); ys = np.asarray(ys, dtype=np.float64)
    b, a = np.polyfit(xs, ys, 1)
    return {"slope": float(b), "intercept": float(a)}


# ------------------------------------------------------------------ load
def main():
    t0 = time.time()
    integrity = {}
    amend = GD / "guidance-v4-amendment.md"
    atext = amend.read_text(encoding="utf-8")
    integrity["locked_rule_present_verbatim"] = " ".join(LOCKED_RULE_SENTENCE.split()) in " ".join(atext.split())
    integrity["amendment_sha256"] = sha(amend)
    bc = json.loads((R / "theory" / "bound_constants.json").read_text())
    proto = RUN / "protocols" / "bound-constants-protocol.md"
    integrity["bound_protocol_hash_matches"] = (bc["protocol_sha256"] == sha(proto))
    manifest = json.loads((RUN / "audits" / "v3-evidence-hashes.json").read_text())
    v3_ok, v3_bad = True, []
    for rel, meta in manifest["files"].items():
        if sha(V3 / rel) != meta["sha256"]:
            v3_ok, v3_bad = False, v3_bad + [rel]
    integrity["v3_evidence_byte_preserved"] = v3_ok
    integrity["v3_evidence_mismatch"] = v3_bad
    repro = json.loads((RUN / "audits" / "reproduction-check.json").read_text())
    print("[analyze] integrity:", json.dumps(integrity), flush=True)
    if not (integrity["locked_rule_present_verbatim"] and integrity["bound_protocol_hash_matches"] and v3_ok):
        raise SystemExit("INTEGRITY CHECK FAILED — analysis refuses to run (ledger A2/A5).")

    agg = json.loads((R / "aggregated.json").read_text())
    runs = agg["runs"]
    assert len(runs) == 50, f"main matrix incomplete: {len(runs)}/50 runs"
    by = {(r["stream"], r["seed"]): r for r in runs}
    for k in [(n, s) for n in STREAMS for s in range(41, 51)]:
        assert k in by, f"missing run {k}"

    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "integrity": integrity,
           "reproduction_check_verdict": repro["verdict"],
           "streams": {}, "c1_rule": {"locked_sentence": LOCKED_RULE_SENTENCE,
                                       "boot_resamples": BOOT, "bh_q": 0.05},
           "dominance": {}, "energy": {}, "strata": {}, "downstream": {},
           "drift": {}, "perseed_scatter": {}}

    # ------------------------------------------------ C-1 locked rule (E9)
    c1 = {}
    pvals, order = [], []
    for name in STREAMS:
        d_eps = np.array([by[(name, s)]["methods"]["C2"]["mean_epsilon"]
                          - by[(name, s)]["methods"]["M0"]["mean_epsilon"] for s in range(41, 51)])
        ci = bca_ci(d_eps)
        p_sf = signflip_p(d_eps)
        pvals.append(p_sf); order.append(name)
        c1[name] = {"paired_eps_diff_C2_minus_M0": [float(x) for x in d_eps],
                    "mean_diff": float(d_eps.mean()), "bca95": ci,
                    "signflip_p": p_sf,
                    "cohens_dz": cohens_dz(d_eps),
                    "prob_improvement_C2_lower": prob_improvement(-d_eps)}
    qs = bh_adjust(pvals)
    for name, q in zip(order, qs):
        c1[name]["bh_q"] = q
    lastfm = c1["lastfm"]
    literal_verdict = bool(lastfm["bca95"]["excludes_zero"] and lastfm["bh_q"] < 0.05)
    conjunction = bool(all(c1[n]["bca95"]["excludes_zero"] and c1[n]["bh_q"] < 0.05 for n in STREAMS)
                       and len({c1[n]["bca95"]["direction"] for n in STREAMS}) == 1)
    c1["d_replication_10seed"] = literal_verdict
    c1["all_five_conjunction_also_required_for_claim"] = conjunction
    c1["interpretation_note"] = ("Locked verdict mapping keys on LastFM (v3 swing stream). "
                                 "The restored five-stream claim additionally requires the "
                                 "all-five conjunction; disagreement would trigger the P5 "
                                 "disclosure path rather than an edited claim.")
    out["c1_rule"]["result"] = c1
    print(f"[analyze] C-1: d_replication_10seed={literal_verdict} "
          f"all-five={conjunction} LastFM q={lastfm['bh_q']:.4f}", flush=True)

    # ------------------------------------- C-4 effect sizes + strict dominance
    dom = {}
    for name in STREAMS:
        rows = {}
        for m in METHODS:
            if m == "C2":
                continue
            d_agr = np.array([by[(name, s)]["methods"]["C2"]["agreement"]
                              - by[(name, s)]["methods"][m]["agreement"] for s in range(41, 51)])
            rows[m] = {"mean_diff_pp": float(d_agr.mean() * 100),
                       "min_diff_pp": float(d_agr.min() * 100),
                       "cohens_dz": cohens_dz(d_agr),
                       "prob_C2_better": prob_improvement(d_agr),
                       "signflip_p": signflip_p(d_agr),
                       "all_10_seeds_positive": bool((d_agr > 0).all())}
        dom[name] = rows
    out["dominance"]["C2_vs_others_agreement"] = dom
    weakest = min(r["mean_diff_pp"] for n in STREAMS for r in dom[n].values())
    out["dominance"]["weakest_mean_margin_pp"] = weakest
    out["dominance"]["strict_all_streams_all_controls_mean"] = bool(weakest > 0)

    # ------------------------------------------------- E10 bound + theory arms
    arms = json.loads((R / "theory" / "theory_arms.json").read_text())
    v6 = json.loads((R / "theory" / "v6_toy.json").read_text())
    bound = {}
    for name in STREAMS:
        bound[name] = {}
        for m in BOUND_METHODS:
            vr = [by[(name, s)]["methods"][m]["bound"]["violation_rate"] for s in range(41, 51)]
            tight = [by[(name, s)]["methods"][m]["bound"]["mean_tightness"] for s in range(41, 51)]
            bound[name][m] = {"violation_rate_mean": float(np.mean(vr)),
                              "violation_rate_max": float(np.max(vr)),
                              "within_5pct_ceiling": bool(np.mean(vr) <= 0.05),
                              "mean_tightness": float(np.mean(tight))}
    out["e10_bound"] = {"per_stream": bound,
                        "ceiling": 0.05,
                        "verdict": bool(all(bound[n][m]["within_5pct_ceiling"]
                                            for n in STREAMS for m in BOUND_METHODS))}
    def arm_metric(arm, method, field):
        return [r["methods"][method][field] for r in arms[arm]]
    checks = {}
    for meth in ("C2", "M0"):
        checks[f"alpha_state_eps_slope_{meth}"] = slope([0.1, 0.3, 0.5, 0.7],
                                                        arm_metric("alpha_state", meth, "mean_epsilon"))
        checks[f"edge_insert_eps_slope_{meth}"] = slope([0.0, 0.02, 0.05, 0.10, 0.20],
                                                        arm_metric("edge_insert", meth, "mean_epsilon"))
        checks[f"alpha_carry_agr_slope_{meth}"] = slope([0.0, 0.25, 0.5, 0.75, 1.0],
                                                        arm_metric("alpha_carry", meth, "agreement"))
        checks[f"T_agr_slope_{meth}"] = slope([1, 2, 4, 8, 16],
                                              arm_metric("T_sweep", meth, "agreement"))
    expected = {"alpha_state_eps_slope": "negative", "edge_insert_eps_slope": "positive",
                "alpha_carry_agr_slope": "positive", "T_agr_slope": "positive"}
    v_arm_verdicts = {}
    for k, direction in expected.items():
        for meth in ("C2", "M0"):
            s = checks[f"{k}_{meth}"]["slope"]
            v_arm_verdicts[f"{k}_{meth}"] = {"slope": s, "expected": direction,
                                             "pass": (s < 0 if direction == "negative" else s > 0)}
    v_arm_verdicts["v6_toy"] = {"verdict": v6["verdict"], "checks": v6["checks"],
                                "fitted_rho_transient": v6["subtoy_A_rho"]["fits"]["0.3"]["fitted_a_transient"],
                                "rho_analytic": v6["subtoy_A_rho"]["rho_analytic"],
                                "fitted_b": v6["subtoy_B_topo"]["fitted_b"],
                                "corr_ek_topo": v6["subtoy_B_topo"]["corr_ek_topo"]}
    out["theory_validation"] = {"slopes": checks, "verdicts": v_arm_verdicts,
                                "v6": v6}

    # ------------------------------------------- C-9 robustness + drift strata
    rob = {}
    for arm, levels in (("robust_noise", [0.0, 0.005, 0.01, 0.02, 0.04]),
                        ("robust_dt", [0.0, 0.05, 0.10, 0.20, 0.40]),
                        ("robust_drop", [0.0, 0.05, 0.10, 0.15, 0.20])):
        entry = {}
        for meth in ("C2", "M0"):
            agr = arm_metric(arm, meth, "agreement")
            entry[meth] = {"clean": agr[0], "max_level": agr[-1],
                           "retention": agr[-1] / max(agr[0], 1e-12),
                           "slope": slope(levels, agr)}
        rob[arm] = entry
    out["robustness"] = rob
    drift, firing_strata = {}, {}
    for name in STREAMS:
        for meth in ("C2", "M0"):
            per_seed = np.array([by[(name, s)]["methods"][meth]["epsilon_per_window"] for s in range(41, 51)])
            mean_slices = per_seed.mean(axis=0)
            drift[f"{name}.{meth}"] = {"mean_epsilon_per_slice": [float(x) for x in mean_slices],
                                       "first3_minus_last3": float(mean_slices[:3].mean() - mean_slices[-3:].mean()),
                                       "relative_drift": float((mean_slices[-3:].mean() - mean_slices[:3].mean())
                                                                / max(mean_slices.mean(), 1e-12))}
            fr = np.array([by[(name, s)]["methods"][meth]["firing_per_window"] for s in range(41, 51)]).mean(axis=0)
            lo, hi = np.quantile(fr, [1 / 3, 2 / 3])
            firing_strata[f"{name}.{meth}"] = {"slice_firing_mean": [float(x) for x in fr],
                                               "low_share": float((fr <= lo).mean()),
                                               "strata_edges": [float(lo), float(hi)]}
    out["drift"] = drift
    out["firing_stratification_3level"] = firing_strata

    # --------------------------------------- C-3 energy (op-count convention)
    for name in STREAMS:
        e = {}
        for m in METHODS:
            ac_per_event = np.mean([by[(name, s)]["methods"][m]["graded_events_per_event"]
                                    for s in range(41, 51)]) * L_LAYERS
            e[m] = {"acs_per_event": float(ac_per_event),
                    "snj_per_event": float(ac_per_event * E_AC_pJ),
                    "trig_rate": float(np.mean([by[(name, s)]["methods"][m]["recalibration_rate"]
                                                for s in range(41, 51)]))}
        ann_pj = ANN_MACS_PER_EVENT * E_MAC_pJ
        e["_ann_reference_macs_per_event"] = ANN_MACS_PER_EVENT
        e["_ann_reference_pj_per_event"] = float(ann_pj)
        for m in METHODS:
            e[m]["energy_ratio_vs_ann"] = e[m]["snj_per_event"] / ann_pj
        e["TCAR_reanchor_overhead_pct"] = float(e["M0"]["trig_rate"] * D * D
                                                / ANN_MACS_PER_EVENT * 100)
        e["C5MT_vs_C2_event_overhead_pct"] = float(
            (e["C5MT"]["acs_per_event"] - e["C2"]["acs_per_event"])
            / max(e["C2"]["acs_per_event"], 1e-12) * 100)
        e["M0_vs_C2_event_overhead_pct"] = float(
            (e["M0"]["acs_per_event"] - e["C2"]["acs_per_event"])
            / max(e["C2"]["acs_per_event"], 1e-12) * 100)
        out["energy"][name] = e
    lat_path = R / "latency" / "latency_probe.json"
    if lat_path.is_file():
        out["latency"] = json.loads(lat_path.read_text())["methods"]

    # --------------------------- C-6 downstream dose + C-7 inductive strata
    for name in STREAMS:
        d6 = {}
        for m in ("C2", "M0", "C5MT"):
            bins = np.array([by[(name, s)]["methods"][m]["mrr_loss_per_epsbin"] for s in range(41, 51)],
                            dtype=np.float64)
            ns = np.array([by[(name, s)]["methods"][m]["epsbin_n"] for s in range(41, 51)],
                          dtype=np.float64)
            weighted = np.nansum(bins * ns, axis=0) / np.maximum(np.nansum(ns, axis=0), 1)
            d6[m] = {"mean_mrr_loss_per_bin": [None if not np.isfinite(x) else float(x) for x in weighted],
                     "bin_query_mass": [float(x) for x in ns.sum(axis=0)]}
        bins_arr = np.array([x if x is not None else np.nan for x in d6["M0"]["mean_mrr_loss_per_bin"]])
        valid = np.isfinite(bins_arr)
        mono = None
        if valid.sum() >= 3:
            mono = slope(np.arange(len(bins_arr))[valid], bins_arr[valid])["slope"]
        d6["M0_loss_increases_with_eps_slope"] = mono
        out["downstream"][name] = d6
        c7 = {}
        for m in METHODS:
            def _ms(key):
                v = [by[(name, s)]["methods"][m][key]
                     for s in range(41, 51) if by[(name, s)]["methods"][m][key]]
                return float(np.mean(v)) if v else float("nan")
            ind, trd = _ms("agreement_inductive"), _ms("agreement_transductive")
            c7[m] = {"inductive": None if not np.isfinite(ind) else float(ind),
                     "transductive": None if not np.isfinite(trd) else float(trd),
                     "gap_pp": None if not (np.isfinite(ind) and np.isfinite(trd)) else float((ind - trd) * 100)}
        out["strata"][name] = {"inductive": c7}

    # ------------------------------------------------ per-seed scatter export
    for name in STREAMS:
        sc = {}
        for m in ("C2", "M0", "C5MT"):
            sc[m] = {"agreement": [by[(name, s)]["methods"][m]["agreement"] for s in range(41, 51)],
                     "mean_epsilon": [by[(name, s)]["methods"][m]["mean_epsilon"] for s in range(41, 51)]}
        out["perseed_scatter"][name] = sc

    # --------------------------------------------- feasibility contract verdicts
    out["feasibility_contract"] = {
        "CL1_engine_reproduction": {"verdict": repro["verdict"],
                                    "max_rel_eps_diff": repro["max_rel_eps_diff"],
                                    "criteria_failed": {k: len(v.get("failed", v.get("hard_failed", [])))
                                                        for k, v in repro["criteria"].items()},
                                    "seed46_outside_ranges": repro["seed46_range_check"]["n_outside"]},
        "CL2_ten_seed_replication": {"d_replication_10seed": c1["d_replication_10seed"],
                                     "all_five_conjunction": conjunction,
                                     "lastfm_bh_q": lastfm["bh_q"]},
        "CL3_theory_package": {
            "v6_pass": v6["verdict"] == "PASS",
            "e10_bound_ceiling_pass": out["e10_bound"]["verdict"],
            "expected_direction_slopes_pass": int(sum(1 for v in v_arm_verdicts.values()
                                                      if isinstance(v, dict) and v.get("pass"))),
            "expected_direction_slopes_total": 8},
        "CL4_c5mt_included": {"in_matrix": all("C5MT" in by[(n, s)]["methods"] for n in STREAMS
                                               for s in range(41, 51)),
                              "c5mt_fidelity": {n: float(np.mean([by[(n, s)]["methods"]["C5MT"]["agreement"]
                                                                  for s in range(41, 51)])) for n in STREAMS}},
    }
    wj(R / "final-analysis-v4.json", out)
    print(f"[analyze] done in {time.time()-t0:.0f}s -> results/final-analysis-v4.json", flush=True)
    return out


if __name__ == "__main__":
    main()
