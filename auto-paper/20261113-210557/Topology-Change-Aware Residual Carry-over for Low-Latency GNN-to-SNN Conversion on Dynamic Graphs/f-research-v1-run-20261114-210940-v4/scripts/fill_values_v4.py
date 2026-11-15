#!/usr/bin/env python3
"""Fill v4_values.tex and generate tables_v4.tex from real v4 results.
Placeholders remain visibly PENDING until the campaign artefacts are present.
Sources (all inside this run root):
  results/aggregated.json          main matrix, 50 runs
  results/final-analysis-v4.json   locked-rule statistics + verdicts (scripts/analyze_v4.py)
  results/theory/theory_arms.json  V-arms (validation)
  results/theory/bound_constants.json
  results/theory/v6_toy.json
  results/latency/latency_probe.json
"""
from __future__ import annotations
import json
import re
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parents[1]
R = RUN / "results"
PAP = RUN / "paper"

streams = ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
cap = lambda s: s.capitalize()
methods = ["C0", "C1", "C2", "C3", "C4", "C5MT", "M0", "A1", "A2", "A3", "A5", "D1"]
bound_methods = ["C1", "C2", "M0"]
MLETTER = {"C0": "Czero", "C1": "COne", "C2": "Ctwo", "C3": "Cthree", "C4": "Cfour",
           "C5MT": "Cfivemt", "M0": "Mzero", "A1": "AOne", "A2": "ATwo",
           "A3": "AThree", "A5": "AFive", "D1": "DOne"}
TLETTER = {1: "one", 2: "two", 4: "four", 8: "eight", 16: "sixteen"}


def load(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return default


runs = (load(R / "aggregated.json") or {}).get("runs", [])
an = load(R / "final-analysis-v4.json") or {}
arms = load(R / "theory" / "theory_arms.json") or {}
bc = load(R / "theory" / "bound_constants.json") or {}
v6 = load(R / "theory" / "v6_toy.json") or {}
lat = load(R / "latency" / "latency_probe.json") or {}
REAL = len(runs) == 50
by = {(r["stream"], r["seed"]): r for r in runs}


def agg(s, m, key):
    v = [r["methods"][m][key] for r in runs if r["stream"] == s]
    return float(np.mean(v)) if v else float("nan")


def sd(s, m, key):
    v = [r["methods"][m][key] for r in runs if r["stream"] == s]
    return float(np.std(v, ddof=1)) if len(v) > 1 else float("nan")


def f(x, n=4):
    if x is None:
        return "PENDING"
    return f"{x:.{n}f}" if np.isfinite(x) else "PENDING"


def f3(x):
    return f(x, 3)


def qtex(x, dollars=True):
    if x is None or not np.isfinite(x):
        return "PENDING"
    if x <= 0 or x < 1e-300:
        s = r"<10^{-300}"
    elif x < 0.001:
        mant, exp = f"{x:.1e}".split("e")
        s = rf"{mant}\times10^{{{int(exp)}}}"
    else:
        s = f"{x:.4g}"
    return f"${s}$" if dollars else s


vals = {}
for s in streams:
    cap = s.capitalize()
    vals[f"Agree{cap}"] = f(agg(s, "M0", "agreement"))
    vals[f"AgreeSd{cap}"] = f(sd(s, "M0", "agreement"), 5)
    vals[f"Ret{cap}"] = f(agg(s, "M0", "mrr_retention"))
    vals[f"EpsMzero{cap}"] = f(agg(s, "M0", "mean_epsilon"), 5)
    vals[f"EpsCtwo{cap}"] = f(agg(s, "C2", "mean_epsilon"), 5)
    vals[f"EpsCfivemt{cap}"] = f(agg(s, "C5MT", "mean_epsilon"), 5)
    vals[f"AgreeCfivemt{cap}"] = f(agg(s, "C5MT", "agreement"))
    vals[f"Trig{cap}"] = f3(agg(s, "M0", "recalibration_rate"))
    e0 = agg(s, "M0", "mean_epsilon"); e2 = agg(s, "C2", "mean_epsilon")
    vals[f"Red{cap}"] = f"{100 * (1 - e0 / e2):.1f}\\%" if np.isfinite(e2) and e2 > 0 else "PENDING"
    vals[f"EvMzero{cap}"] = f3(agg(s, "M0", "graded_events_per_event"))
    vals[f"EvCtwo{cap}"] = f3(agg(s, "C2", "graded_events_per_event"))
    vals[f"EvCfivemt{cap}"] = f3(agg(s, "C5MT", "graded_events_per_event"))
    vals[f"FiringMzero{cap}"] = f(agg(s, "M0", "firing_rate"), 5)
    tm = [r["ann_mrr"] for r in runs if r["stream"] == s]
    if tm:
        vals[f"TeacherMRR{cap}"] = f(float(np.mean(tm)), 4)
    # bound constants + E10
    if s in bc.get("streams", {}):
        c = bc["streams"][s]
        vals[f"Rho{cap}"] = f3(c["rho_hat"]); vals[f"LA{cap}"] = f3(c["LA_hat"])
        vals[f"CHat{cap}"] = f3(c["c_hat"]); vals[f"Eta{cap}"] = f3(c["eta_hat"])
        vals[f"BoundRtwo{cap}"] = f3(c["r2_mean_level"])
    for m in bound_methods:
        if (s, 41) in by and "bound" in by[(s, 41)]["methods"].get(m, {}):
            vr = [by[(s, sd)]["methods"][m]["bound"]["violation_rate"] for sd in range(41, 51) if (s, sd) in by]
            vals[f"Viol{MLETTER[m]}{cap}"] = f(np.mean(vr), 4) if vr else "PENDING"
            tight = [by[(s, sd)]["methods"][m]["bound"]["mean_tightness"] for sd in range(41, 51) if (s, sd) in by]
            vals[f"Tight{MLETTER[m]}{cap}"] = f(np.mean(tight), 3) if tight else "PENDING"

# locked-rule statistics (C-1)
c1 = an.get("c1_rule", {}).get("result", {})
for s in streams:
    cap = s.capitalize()
    row = c1.get(s, {})
    if row:
        ci = row.get("bca95", {}).get("ci95", [np.nan, np.nan])
        vals[f"CIDiff{cap}Lo"] = f"{ci[0]:.5f}"; vals[f"CIDiff{cap}Hi"] = f"{ci[1]:.5f}"
        vals[f"MeanDiff{cap}"] = f"{row.get('mean_diff', np.nan):.2e}"
        vals[f"BHq{cap}"] = qtex(row.get("bh_q", np.nan), dollars=False)
        vals[f"Dz{cap}"] = f(row.get("cohens_dz", np.nan), 2)
        vals[f"PoI{cap}"] = f(row.get("prob_improvement_C2_lower", np.nan), 3)
if c1:
    vals["DReplicationTenSeed"] = "true" if c1.get("d_replication_10seed") else "false"
    vals["AllFiveConjunction"] = "true" if c1.get("all_five_conjunction_also_required_for_claim") else "false"

# arms -> slope macros and curve values
def arm_metric(arm, method, field):
    return [r["methods"][method][field] for r in arms.get(arm, [])]


for meth, tag in (("C2", "Ctwo"), ("M0", "Mzero")):
    for arm, key, lv in (("alpha_state", "alpha_state", [0.1, 0.3, 0.5, 0.7]),
                         ("edge_insert", "edge_insert", [0.0, 0.02, 0.05, 0.10, 0.20]),
                         ("alpha_carry", "alpha", [0.0, 0.25, 0.5, 0.75, 1.0])):
        ys = arm_metric(arm, meth, "mean_epsilon" if arm != "alpha_carry" else "agreement")
        if len(ys) == len(lv):
            b, a = np.polyfit(lv, ys, 1)
            vals[f"Slope{key.replace("_", "")}{tag}"] = f(b, 5)
    tys = arm_metric("T_sweep", meth, "agreement")
    if len(tys) == 5:
        b, a = np.polyfit([1, 2, 4, 8, 16], tys, 1)
        vals[f"SlopeT{tag}"] = f(b, 5)
        for T, yv in zip([1, 2, 4, 8, 16], tys):
            vals[f"AgreeT{TLETTER[T]}{tag}"] = f(yv)

# robustness retention (state error; agreement is saturated at 1.0 under every dose)
for arm, tag in (("robust_noise", "Noise"), ("robust_dt", "Dt"), ("robust_drop", "Drop")):
    for meth, mtag in (("C2", "Ctwo"), ("M0", "Mzero")):
        ys = arm_metric(arm, meth, "mean_epsilon")
        if ys:
            vals[f"RobustClean{tag}{mtag}"] = f"{ys[0]:.2e}"
            vals[f"RobustMax{tag}{mtag}"] = f"{ys[-1]:.2e}"
            vals[f"RobustRet{tag}{mtag}"] = f(ys[-1] / max(ys[0], 1e-12), 4)

# energy + latency
for s in streams:
    cap = s.capitalize()
    e = (an.get("energy") or {}).get(s, {})
    for m, tag in (("M0", "Mzero"), ("C2", "Ctwo"), ("C5MT", "Cfivemt")):
        if m in e:
            vals[f"Energy{tag}{cap}"] = f3(e[m]["snj_per_event"])
            vals[f"EnergyRatio{tag}{cap}"] = f(e[m]["energy_ratio_vs_ann"], 4)
    if "_ann_reference_pj_per_event" in e:
        vals[f"AnnRef{cap}"] = f3(e["_ann_reference_pj_per_event"])
    if "TCAR_reanchor_overhead_pct" in e:
        vals[f"OverheadTcar{cap}"] = f(e["TCAR_reanchor_overhead_pct"], 3)
    if "C5MT_vs_C2_event_overhead_pct" in e:
        vals[f"OverheadCfivemt{cap}"] = f(e["C5MT_vs_C2_event_overhead_pct"], 2)
for m in methods:
    if m in (lat.get("methods") or {}):
        vals[f"Latency{MLETTER[m]}"] = f(lat["methods"][m]["ms_per_event_mean"], 3)

# strata / drift / downstream
for s in streams:
    cap = s.capitalize()
    st = (an.get("strata") or {}).get(s, {}).get("inductive", {})
    for m, tag in (("M0", "Mzero"), ("C2", "Ctwo"), ("C5MT", "Cfivemt")):
        if m in st and st[m].get("gap_pp") is not None:
            vals[f"IndGap{tag}{cap}"] = f(st[m]["gap_pp"], 2)
    d = (an.get("drift") or {}).get(f"{s}.M0", {})
    if d:
        vals[f"DriftRel{cap}"] = f(d.get("relative_drift", np.nan), 4)
    dn = (an.get("downstream") or {}).get(s, {})
    if dn.get("M0_loss_increases_with_eps_slope") is not None:
        vals[f"DownSlope{cap}"] = f(dn["M0_loss_increases_with_eps_slope"], 5)

# V-6
if v6:
    vals["VsixRho"] = f(v6.get("subtoy_A_rho", {}).get("fits", {}).get("0.3", {}).get("fitted_a_transient", np.nan), 3)
    vals["VsixRhoAnalytic"] = f(v6.get("subtoy_A_rho", {}).get("rho_analytic", np.nan), 2)
    vals["VsixB"] = f(v6.get("subtoy_B_topo", {}).get("fitted_b", np.nan), 4)
    vals["VsixCorr"] = f(v6.get("subtoy_B_topo", {}).get("corr_ek_topo", np.nan), 2)
    vals["VsixVerdict"] = v6.get("verdict", "PENDING")

vals["NRuns"] = str(len(runs)) if runs else "PENDING"
vals["NSeeds"] = "10" if REAL else "PENDING"
vals["NMethods"] = str(len(methods))
vals["NRefs"] = "50"          # finalized at P12 against the .bib
vals["MeanDeltaA"] = f(float(np.mean([r.get("measured_dA_mean", 0.0) for r in runs])), 3) if runs else "PENDING"
vals["TrainCoverage"] = "80,000"

vp = PAP / "v4_values.tex"
# Fresh write on every run: stale keys from earlier versions are purged so no
# out-of-date macro can silently compile.
lines = ["% Contract v4 measured-value macros (regenerated from real results;",
         "% this file is rewritten from scratch on every fill run)."]
lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in sorted(vals.items())]
vp.write_text("\n".join(lines) + "\n", encoding="utf-8")

# ------------------------------- tables -------------------------------
def table(caption, label, header, rows, spec=None):
    spec = spec or "l" + "c" * (len(header) - 1)
    out = ["\\begin{table}[t]", "\\centering", "\\small", f"\\caption{{{caption}}}",
           f"\\label{{{label}}}", f"\\begin{{tabular}}{{{spec}}}", "\\toprule",
           " & ".join(header) + " \\\\", "\\midrule"]
    out += [" & ".join(str(x) for x in row) + " \\\\" for row in rows]
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(out)


P = "PENDING"
tabs = []
tabs.append(table("Five public streams used in this study (sizes, catalogs, frozen split identifiers).", "tab:data",
                  ["Stream", "Events", "Catalog", "Val / test queries", "Split"],
                  [["Wikipedia", "157,474", "1,000", "1,024 / 4,096", "70/15/15"],
                   ["MOOC", "411,749", "97", "1,024 / 4,096", "70/15/15"],
                   ["Enron", "125,235", "184", "1,024 / 4,096", "70/15/15"],
                   ["Reddit", "672,447", "984", "1,024 / 4,096", "70/15/15"],
                   ["LastFM", "1,293,103", "1,000", "1,024 / 4,096", "70/15/15"]]))

if REAL:
    s = "wikipedia"
    tabs.append(table("Main comparison on Wikipedia (10 seeds; mean over seeds). C5-MT is the multi-threshold control.", "tab:main",
                      ["Method", "Agreement", "Retention", "$\\varepsilon_k$", "Events", "Trigger"],
                      [[m, f(agg(s, m, "agreement")), f(agg(s, m, "mrr_retention")),
                        f(agg(s, m, "mean_epsilon"), 5), f3(agg(s, m, "graded_events_per_event")),
                        f3(agg(s, m, "recalibration_rate"))] for m in methods]))
    tabs.append(table("Five-stream replication with locked-rule statistics (10 seeds per stream). "
                      "Reduction is $\\varepsilon$ improvement of M0 over C2; $q$ is BH-adjusted.", "tab:streams",
                      ["Stream", "Agree (M0)", "$\\varepsilon_{M0}$", "$\\varepsilon_{C2}$", "Red.", "Trig.", "BH $q$"],
                      [[x.capitalize(), f(agg(x, "M0", "agreement")), f(agg(x, "M0", "mean_epsilon"), 5),
                        f(agg(x, "C2", "mean_epsilon"), 5), vals[f"Red{x.capitalize()}"],
                        f3(agg(x, "M0", "recalibration_rate")), vals.get(f"BHq{x.capitalize()}", P)]
                       for x in streams]))
    if c1:
        rows = []
        for x in streams:
            row = c1.get(x, {})
            ci = row.get("bca95", {}).get("ci95", [np.nan, np.nan])
            rows.append([x.capitalize(), f(row.get("mean_diff", np.nan), 5),
                         f"[{ci[0]:.5f}, {ci[1]:.5f}]", qtex(row.get("signflip_p", np.nan)),
                         vals.get(f"BHq{x.capitalize()}", P), f(row.get("cohens_dz", np.nan), 2),
                         f(row.get("prob_improvement_C2_lower", np.nan), 3)])
        rows.append(["$d_{\\mathrm{replication}}^{10\\mathrm{seed}}$", vals.get("DReplicationTenSeed", P),
                     "", "", "", "", ""])
        tabs.append(table("Locked C-1 decision rule, executed once: paired per-seed $\\varepsilon$ differences "
                          "(C2$-$M0), BCa 4000, exact sign-flip, BH across streams.", "tab:stats",
                          ["Stream", "Mean diff", "95\\% CI", "sign-flip $p$", "BH $q$", "$d_z$", "PoI"],
                          rows))
    if bc:
        rows = []
        for x in streams:
            c = bc["streams"].get(x, {})
            rows.append([x.capitalize(), f3(c.get("rho_hat", np.nan)), f3(c.get("LA_hat", np.nan)),
                         f3(c.get("c_hat", np.nan)), f3(c.get("eta_hat", np.nan)),
                         f3(c.get("r2_mean_level", np.nan)),
                         vals.get(f"ViolCOne{x.capitalize()}", P), vals.get(f"ViolCtwo{x.capitalize()}", P),
                         vals.get(f"ViolMzero{x.capitalize()}", P)])
        tabs.append(table("Bound constants (validation-estimated, locked) and single locked test evaluation: "
                          "violation rates per method (mean over 10 seeds; ceiling 5\\%).", "tab:bound",
                          ["Stream", "$\\hat\\rho$", "$\\hat L_A$", "$\\hat c$", "$\\hat\\eta$", "$R^2$",
                           "Viol C1", "Viol C2", "Viol M0"], rows))
    # V-arms
    slope_rows = [
        ["V-2 $T$ dose-response", "$T\\in\\{1,2,4,8,16\\}$", "fidelity $\\uparrow$ with $T$",
         f"{vals.get('SlopeTCtwo', P)} / {vals.get('SlopeTMzero', P)}"],
        ["V-3 edge insertion", "$p\\in\\{0,..,0.20\\}$", "$\\varepsilon$ $\\uparrow$ with $p$",
         f"{vals.get('SlopeedgeinsertCtwo', P)} / {vals.get('SlopeedgeinsertMzero', P)}"],
        ["V-4 state decay", "$\\alpha_s\\in\\{0.1,..,0.7\\}$", "$\\varepsilon$ $\\downarrow$ with $\\alpha_s$",
         f"{vals.get('SlopealphastateCtwo', P)} / {vals.get('SlopealphastateMzero', P)}"],
        ["V-5 carry-over", "$\\alpha\\in\\{0,..,1\\}$", "agreement $\\uparrow$ with $\\alpha$",
         f"{vals.get('SlopealphaCtwo', P)} / {vals.get('SlopealphaMzero', P)}"],
        ["V-6 controlled toy", "Sec.~\\ref{sec:bound}", "$\\rho$ recovered",
         f"{vals.get('VsixRho', P)} vs {vals.get('VsixRhoAnalytic', P)}"],
    ]
    tabs.append(table("Theory validation arms (slopes; C2 / M0; validation windows).", "tab:varms",
                      ["Arm", "Dose", "Expected direction", "Measured slope"], slope_rows))
    # robustness (state error; agreement is saturated at 1.0 under every dose)
    rows = []
    for arm, tag, dose in (("robust_noise", "Noise", "$\\sigma{=}0.04$"), ("robust_dt", "Dt", "$\\delta_t{=}0.4$"),
                           ("robust_drop", "Drop", "$p{=}0.20$")):
        for meth, mtag, name in (("C2", "Ctwo", "C2"), ("M0", "Mzero", "M0")):
            ys = arm_metric(arm, meth, "mean_epsilon")
            if ys:
                rows.append([f"{tag.lower()} {name}", dose, f"{ys[0]:.2e}", f"{ys[-1]:.2e}",
                             f(ys[-1] / max(ys[0], 1e-12), 4)])
    tabs.append(table("Robustness, five-level sweeps (validation): mean per-event state error $\\varepsilon_k$ "
                      "at the clean and strongest dose, with the max/clean ratio. Argmax agreement is saturated "
                      "at 1.0 under every dose for both methods and is therefore not the informative view.", "tab:robust",
                      ["Perturbation", "Dose", "Clean $\\varepsilon$", "Max $\\varepsilon$", "Ratio"], rows))
    # energy
    rows = []
    for x in streams:
        e = (an.get("energy") or {}).get(x, {})
        rows.append([x.capitalize(),
                     vals.get(f"EnergyMzero{x.capitalize()}", P), vals.get(f"EnergyCtwo{x.capitalize()}", P),
                     vals.get(f"EnergyCfivemt{x.capitalize()}", P), vals.get(f"AnnRef{x.capitalize()}", P),
                     vals.get(f"OverheadTcar{x.capitalize()}", P)])
    tabs.append(table("Op-count energy per event (pJ; Horowitz 2014 45nm constants, SGNNBench convention): "
                      "ACs $\\times$ 0.9\\,pJ vs ANN MAC reference ($1536\\times$ 4.6\\,pJ); "
                      "last column is the TCAR re-anchoring overhead share of the ANN reference.", "tab:energy",
                      ["Stream", "M0", "C2", "C5-MT", "ANN ref", "TCAR OH\\%"], rows))
    # latency
    rows = [[m, vals.get(f"Latency{m}", P)] for m in methods]
    tabs.append(table("Per-event wall time (ms, mean of 3 reps; single-method isolation; includes the shared "
                      "teacher forward, identical across methods).", "tab:latency",
                      ["Method", "ms/event"], rows))
    # T curve
    rows = []
    teps = {m: arm_metric("T_sweep", m, "mean_epsilon") for m in ("C2", "M0")}
    for i, (T, tname) in enumerate(zip([1, 2, 4, 8, 16], ["one", "two", "four", "eight", "sixteen"])):
        e2 = f"{teps['C2'][i]:.2e}" if len(teps["C2"]) == 5 else P
        e0 = f"{teps['M0'][i]:.2e}" if len(teps["M0"]) == 5 else P
        rows.append([str(T), vals.get(f"AgreeT{tname}Ctwo", P), vals.get(f"AgreeT{tname}Mzero", P), e2, e0])
    tabs.append(table("Timestep dose-response on the validation window: agreement (saturated) and mean "
                      "per-event state error $\\varepsilon_k$ for C2 and M0.", "tab:tcurve",
                      ["$T$", "C2 agree", "M0 agree", "C2 $\\varepsilon$", "M0 $\\varepsilon$"], rows))
    # strata
    rows = []
    for x in streams:
        st = (an.get("strata") or {}).get(x, {}).get("inductive", {})
        rows.append([x.capitalize(),
                     f(st.get("M0", {}).get("inductive", np.nan)), f(st.get("M0", {}).get("transductive", np.nan)),
                     f(st.get("C2", {}).get("inductive", np.nan)), f(st.get("C2", {}).get("transductive", np.nan)),
                     f(st.get("C5MT", {}).get("inductive", np.nan))])
    tabs.append(table("Inductive vs transductive agreement (10-seed mean). Inductive: at least one query endpoint "
                      "first appears inside the evaluation window.", "tab:strata",
                      ["Stream", "M0 ind", "M0 trd", "C2 ind", "C2 trd", "C5MT ind"], rows))
    # downstream
    rows = []
    for x in streams:
        dn = (an.get("downstream") or {}).get(x, {})
        m0 = dn.get("M0", {}).get("mean_mrr_loss_per_bin", [])
        c2 = dn.get("C2", {}).get("mean_mrr_loss_per_bin", [])
        rows.append([x.capitalize()] + [f"{a}/{b}" if a is not None and b is not None else P
                                        for a, b in zip(m0, c2)])
    tabs.append(table("Downstream validity dose-response: mean per-query MRR loss (ANN $-$ converted) by "
                      "$\\varepsilon$ bin (edges $10^{-5}..10^{-1}$; M0/C2 per cell).", "tab:downstream",
                      ["Stream"] + [f"bin{i}" for i in range(6)], rows))
else:
    hdrs = [["Method", "Agreement", "Retention", "$\\varepsilon_k$", "Events", "Trigger"],
            ["Stream", "Agree", "Ret", "$\\varepsilon_{M0}$", "$\\varepsilon_{C2}$", "Red.", "Trig.", "BH $q$"],
            ["Stream", "Mean diff", "95\\% CI", "sign-flip $p$", "BH $q$", "$d_z$", "PoI"],
            ["Stream", "$\\hat\\rho$", "$\\hat L_A$", "$\\hat c$", "$\\hat\\eta$", "$R^2$", "Viol C1", "Viol C2", "Viol M0"],
            ["Arm", "Dose", "Expected", "Slope"], ["Perturbation", "Dose", "Clean", "Max", "Ratio"],
            ["Stream", "M0", "C2", "C5-MT", "ANN ref", "TCAR OH\\%"], ["Method", "ms/event"],
            ["$T$", "C2 agree", "M0 agree", "C2 $\\varepsilon$", "M0 $\\varepsilon$"],
            ["Stream", "M0 ind", "M0 trd", "C2 ind", "C2 trd", "C5MT ind"],
            ["Stream"] + [f"bin{i}" for i in range(6)]]
    labels = [("Wikipedia main comparison (10 seeds).", "tab:main"),
              ("Five-stream replication with locked-rule statistics.", "tab:streams"),
              ("Locked C-1 decision rule, executed once.", "tab:stats"),
              ("Bound constants and single locked test evaluation.", "tab:bound"),
              ("Theory validation arms.", "tab:varms"), ("Robustness, five-level sweeps.", "tab:robust"),
              ("Op-count energy per event.", "tab:energy"), ("Per-event wall time.", "tab:latency"),
              ("Timestep dose-response (validation).", "tab:tcurve"),
              ("Inductive vs transductive agreement.", "tab:strata"),
              ("Downstream validity dose-response.", "tab:downstream")]
    for (cap, lab), hdr in zip(labels, hdrs):
        tabs.append(table(cap, lab, hdr, [[P] * len(hdr)]))

(PAP / "tables_v4.tex").write_text("% Generated from real v4 results; do not edit by hand.\n" + "\n".join(tabs), encoding="utf-8")
print("filled", len(vals), "values and", len(tabs), "tables; REAL =", REAL)
