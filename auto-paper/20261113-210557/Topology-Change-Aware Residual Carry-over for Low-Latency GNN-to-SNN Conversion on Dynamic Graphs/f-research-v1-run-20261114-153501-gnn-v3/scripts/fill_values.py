#!/usr/bin/env python3
"""Fill v3_values.tex and generate tables_v3.tex from real results.
Placeholders remain visibly PENDING until the full campaign is present.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
import numpy as np

RUN = Path(__file__).resolve().parents[1]
R = RUN / "results"
PAP = RUN / "paper"

runs = []
p = R / "aggregated.json"
if p.is_file():
    try:
        runs = json.loads(p.read_text())["runs"]
    except Exception:
        pass
REAL = len(runs) >= 15

streams = ["wikipedia", "mooc", "enron", "reddit", "lastfm"]
methods = ["C0", "C1", "C2", "C3", "C4", "M0", "A1", "A2", "A3", "A5", "D1"]


def agg(s, m, key):
    v = [r["methods"][m][key] for r in runs if r["stream"] == s]
    return float(np.mean(v)) if v else float("nan")


def f(x, n=4):
    return f"{x:.{n}f}" if np.isfinite(x) else "PENDING"


def qtex(x, dollars=True):
    """BH q-value in LaTeX maths; tiny underflow is reported as a bound."""
    if not np.isfinite(x):
        return "PENDING"
    if x <= 0 or x < 1e-300:
        s = r"<10^{-300}"
    elif x < 0.001:
        mant, exp = f"{x:.1e}".split("e")
        s = rf"{mant}\times10^{{{int(exp)}}}"
    else:
        s = f"{x:.2f}"
    return f"${s}$" if dollars else s


vals = {
    "AgreeWiki": f(agg("wikipedia", "M0", "agreement")), "AgreeMooc": f(agg("mooc", "M0", "agreement")),
    "AgreeEnron": f(agg("enron", "M0", "agreement")), "AgreeReddit": f(agg("reddit", "M0", "agreement")),
    "AgreeLastfm": f(agg("lastfm", "M0", "agreement")),
    "RetWiki": f(agg("wikipedia", "M0", "mrr_retention")), "RetMooc": f(agg("mooc", "M0", "mrr_retention")),
    "RetEnron": f(agg("enron", "M0", "mrr_retention")),
    "EpsMzeroWiki": f(agg("wikipedia", "M0", "mean_epsilon")), "EpsMzeroMooc": f(agg("mooc", "M0", "mean_epsilon")),
    "EpsMzeroEnron": f(agg("enron", "M0", "mean_epsilon")),
    "EpsCtwoWiki": f(agg("wikipedia", "C2", "mean_epsilon")), "EpsCtwoMooc": f(agg("mooc", "C2", "mean_epsilon")),
    "EpsCtwoEnron": f(agg("enron", "C2", "mean_epsilon")),
    "EpsAoneWiki": f(agg("wikipedia", "A1", "mean_epsilon")),
    "TrigWiki": f(agg("wikipedia", "M0", "recalibration_rate"), 3),
    "TrigMooc": f(agg("mooc", "M0", "recalibration_rate"), 3),
    "TrigEnron": f(agg("enron", "M0", "recalibration_rate"), 3),
    "TrigReddit": f(agg("reddit", "M0", "recalibration_rate"), 3),
    "TrigLastfm": f(agg("lastfm", "M0", "recalibration_rate"), 3),
    "EvMzero": f(agg("wikipedia", "M0", "graded_events_per_event"), 3),
    "EvCtwo": f(agg("wikipedia", "C2", "graded_events_per_event"), 3),
    "FiringMzero": f(agg("wikipedia", "M0", "firing_rate"), 5),
    "SynopsMzero": f(agg("wikipedia", "M0", "synops_per_event"), 2),
    "ClipMzero": f(agg("wikipedia", "M0", "clip_error"), 5),
    "QuantMzero": f(agg("wikipedia", "M0", "quant_error"), 5),
    "ResidMzero": f(agg("wikipedia", "M0", "residual_error"), 5),
    "MeanDeltaA": f(float(np.mean([r.get("measured_dA_mean", 0.0) for r in runs])), 3) if REAL else "PENDING",
    "NRuns": str(len(runs)) if REAL else "PENDING", "NMethods": str(len(methods)),
    "NRefs": "43", "TrainCoverage": "80,000",
}
for s in streams:
    e0 = agg(s, "M0", "mean_epsilon"); e2 = agg(s, "C2", "mean_epsilon")
    vals["Red" + s.capitalize()] = f"{100 * (1 - e0 / e2):.1f}\\%" if np.isfinite(e2) and e2 > 0 else "PENDING"

# paired bootstrap for Wikipedia epsilon
an = R / "statistics" / "final-analysis-v3.json"
if an.is_file():
    d = json.loads(an.read_text())
    b = d.get("bootstrap", {}).get("epsilon_C2_minus_M0_wikipedia", {})
    ci = b.get("ci", [0, 0])
    vals["CIWikiLo"] = f"{ci[0]:.5f}"; vals["CIWikiHi"] = f"{ci[1]:.5f}"
    q = d.get("bh", {}).get("epsilon_qvalues", [])
    qmap = dict(zip(streams, q)) if len(q) == len(streams) else {}
    vals["BHq"] = qtex(qmap.get("wikipedia", float("nan")), dollars=False)
    vals["BHqLastfm"] = qtex(qmap.get("lastfm", float("nan")), dollars=False)
    bl = d.get("bootstrap", {}).get("epsilon_C2_minus_M0_lastfm", {})
    vals["CILastfmLo"] = f"{bl.get('ci', [0, 0])[0]:.5f}"
    vals["CILastfmHi"] = f"{bl.get('ci', [0, 0])[1]:.5f}"
    vals["BoundViolation"] = str(d.get("bound_violation_rate", "PENDING"))
else:
    for k in ["CIWikiLo", "CIWikiHi", "BHq", "BHqLastfm", "CILastfmLo", "CILastfmHi"]:
        vals[k] = "PENDING"

aux_p = R / "p4_auxiliary" / "sweeps_v3.json"
if aux_p.is_file():
    try:
        a = json.loads(aux_p.read_text())["T_sweep"]
        tmap = {1: "AgreeTone", 2: "AgreeTtwo", 4: "AgreeTfour",
                8: "AgreeTeight", 16: "AgreeTsixteen"}
        for r in a:
            k = tmap.get(int(r["cfg"]["T"]))
            if k:
                vals[k] = f(r["methods"]["M0"]["agreement"])
    except Exception:
        pass
vals["RedWiki"] = vals.get("RedWikipedia", "PENDING")
for k in ["AgreeTone", "AgreeTtwo", "AgreeTfour", "AgreeTeight", "AgreeTsixteen"]:
    vals.setdefault(k, "PENDING")
# legacy key names used in the manuscript
bp = R / "p3_baselines" / "validation_mrr_v3.json"
if bp.is_file():
    b = json.loads(bp.read_text()).get("wikipedia", {})
    vals["EdgeBankWiki"] = f(b.get("B1", float("nan")), 3)
    vals["BaseThreeWiki"] = f(b.get("B2", float("nan")), 3)
else:
    vals["EdgeBankWiki"] = vals["BaseThreeWiki"] = "PENDING"
tw = [r["ann_mrr"] for r in runs if r["stream"] == "wikipedia"]
vals["TeacherMRRWiki"] = f(float(np.mean(tw)), 3) if tw else "PENDING"

vp = PAP / "v3_values.tex"
t = vp.read_text(encoding="utf-8")
for k, v in vals.items():
    # Greedy to the LAST brace on the line: values such as 3.9\times10^{-157}
    # contain nested brace groups, so [^}]* would truncate and leave a stray }.
    t = re.sub(r"(\\newcommand\{\\" + k + r"\})\{.*\}", lambda m: m.group(1) + "{" + v + "}", t)
vp.write_text(t, encoding="utf-8")

# ------------------------------- tables -------------------------------
def table(caption, label, header, rows, spec=None):
    spec = spec or "l" + "c" * (len(header) - 1)
    out = [f"\\begin{{table}}[t]", "\\centering", "\\small", f"\\caption{{{caption}}}",
           f"\\label{{{label}}}", f"\\begin{{tabular}}{{{spec}}}", "\\toprule",
           " & ".join(header) + " \\\\", "\\midrule"]
    out += [" & ".join(str(x) for x in row) + " \\\\" for row in rows]
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(out)


if not REAL:
    tabs = [
        table("Five public streams used in this study (sizes, catalogs, frozen split identifiers).", "tab:data",
              ["Stream", "Events", "Catalog", "Val / test queries", "Split"],
              [["Wikipedia", "157,474", "1,000", "1,024 / 4,096", "70/15/15"],
               ["MOOC", "411,749", "97", "1,024 / 4,096", "70/15/15"],
               ["Enron", "125,235", "184", "1,024 / 4,096", "70/15/15"],
               ["Reddit", "672,447", "984", "1,024 / 4,096", "70/15/15"],
               ["LastFM", "1,293,103", "1,000", "1,024 / 4,096", "70/15/15"]]),
    ]
    for cap, lab, hdr in [
        ("Wikipedia main comparison over controls and ablations (five seeds).", "tab:main", ["Method", "Agreement", "Retention", "$\\varepsilon_k$", "Events", "Trigger"]),
        ("Five-stream replication.", "tab:streams", ["Stream", "Agreement", "Retention", "$\\varepsilon_{M0}$", "$\\varepsilon_{C2}$", "Reduction", "Trigger"]),
        ("Timestep curve.", "tab:tcurve", ["$T$", "Agreement", "$\\varepsilon_k$", "Events/event"]),
        ("Spike activity and SynOps proxies.", "tab:spikes", ["Method", "Events/event", "Firing rate", "SynOps/event"]),
        ("Conversion-error decomposition.", "tab:decomp", ["Method", "Clipping", "Quantisation", "Residual"]),
        ("Mechanism ablations.", "tab:ablate", ["Variant", "Agreement", "$\\varepsilon_k$", "Trigger"]),
        ("Architecture ablations.", "tab:arch", ["Depth", "Aggregator", "Agreement", "$\\varepsilon_k$"]),
        ("Calibration ablations.", "tab:calib", ["Percentile", "Agreement", "$\\varepsilon_k$"]),
        ("Robustness.", "tab:robust", ["Perturbation", "Agreement", "$\\varepsilon_k$"]),
        ("Bound verification against measured $\\|\\Delta A_k\\|$.", "tab:bound", ["Bin", "$n$", "$\\varepsilon_{C2}$", "$\\varepsilon_{M0}$"]),
        ("Paired bootstrap and multiplicity correction.", "tab:stats", ["Stream", "Mean diff", "95\\% CI", "BH $q$"]),
    ]:
        tabs.append(table(cap, lab, hdr, [["PENDING"] * len(hdr)]))
    (PAP / "tables_v3.tex").write_text("% PLACEHOLDER tables; replaced at P8\n" + "\n".join(tabs), encoding="utf-8")
    print("placeholder values/tables written (full campaign not yet present)")
    raise SystemExit(0)

# ---- real tables ----
s = "wikipedia"
tabs = []
tabs.append(table("Five public streams used in this study (sizes, catalogs, frozen split identifiers).", "tab:data",
                  ["Stream", "Events", "Catalog", "Val / test queries", "Split"],
                  [["Wikipedia", "157,474", "1,000", "1,024 / 4,096", "70/15/15"],
                   ["MOOC", "411,749", "97", "1,024 / 4,096", "70/15/15"],
                   ["Enron", "125,235", "184", "1,024 / 4,096", "70/15/15"],
                   ["Reddit", "672,447", "984", "1,024 / 4,096", "70/15/15"],
                   ["LastFM", "1,293,103", "1,000", "1,024 / 4,096", "70/15/15"]]))
tabs.append(table("Wikipedia main comparison over controls and ablations (five seeds).", "tab:main",
                  ["Method", "Agreement", "Retention", "$\\varepsilon_k$", "Events", "Trigger"],
                  [[m, f(agg(s, m, "agreement")), f(agg(s, m, "mrr_retention")),
                    f(agg(s, m, "mean_epsilon")), f(agg(s, m, "graded_events_per_event"), 3),
                    f(agg(s, m, "recalibration_rate"), 3)] for m in methods]))
tabs.append(table("Five-stream replication.", "tab:streams",
                  ["Stream", "Agreement", "Retention", "$\\varepsilon_{M0}$", "$\\varepsilon_{C2}$", "Reduction", "Trigger"],
                  [[x.capitalize(), f(agg(x, "M0", "agreement")), f(agg(x, "M0", "mrr_retention")),
                    f(agg(x, "M0", "mean_epsilon")), f(agg(x, "C2", "mean_epsilon")),
                    vals["Red" + x.capitalize()], f(agg(x, "M0", "recalibration_rate"), 3)] for x in streams]))
tabs.append(table("Spike activity and SynOps proxies.", "tab:spikes",
                  ["Method", "Events/event", "Firing rate", "SynOps/event"],
                  [[m, f(agg(s, m, "graded_events_per_event"), 3), f(agg(s, m, "firing_rate"), 5),
                    f(agg(s, m, "synops_per_event"), 2)] for m in methods]))
tabs.append(table("Conversion-error decomposition (per event).", "tab:decomp",
                  ["Method", "Clipping", "Quantisation", "Residual"],
                  [[m, f(agg(s, m, "clip_error"), 5), f(agg(s, m, "quant_error"), 5),
                    f(agg(s, m, "residual_error"), 5)] for m in methods]))
tabs.append(table("Mechanism ablations.", "tab:ablate",
                  ["Variant", "Agreement", "$\\varepsilon_k$", "Trigger"],
                  [["M0 (full)", f(agg(s, "M0", "agreement")), f(agg(s, "M0", "mean_epsilon")), f(agg(s, "M0", "recalibration_rate"), 3)]] +
                  [[f"A{i}", f(agg(s, f"A{i}", "agreement")), f(agg(s, f"A{i}", "mean_epsilon")),
                    f(agg(s, f"A{i}", "recalibration_rate"), 3)] for i in [1, 2, 3, 5]]))

aux = {}
if aux_p.is_file():
    aux = json.loads(aux_p.read_text())
tabs.append(table("Timestep curve on Wikipedia.", "tab:tcurve",
                  ["$T$", "Agreement", "$\\varepsilon_k$", "Events/event"],
                  [[str(r["cfg"]["T"]), f(r["methods"]["M0"]["agreement"]),
                    f(r["methods"]["M0"]["mean_epsilon"]),
                    f(r["methods"]["M0"]["graded_events_per_event"], 3)] for r in aux.get("T_sweep", [])] or [["PENDING"] * 4]))
tabs.append(table("Architecture ablations on Wikipedia.", "tab:arch",
                  ["Depth $L$", "Aggregator", "Agreement", "$\\varepsilon_k$"],
                  [[str(r["cfg"].get("layers", 3)), r["cfg"].get("aggregator", "mean"),
                    f(r["methods"]["M0"]["agreement"]), f(r["methods"]["M0"]["mean_epsilon"])]
                   for r in aux.get("architecture", []) + aux.get("aggregator", [])] or [["PENDING"] * 4]))
tabs.append(table("Calibration ablations on Wikipedia.", "tab:calib",
                  ["Percentile", "Agreement", "$\\varepsilon_k$"],
                  [[f(r["cfg"]["percentile"], 3), f(r["methods"]["M0"]["agreement"]),
                    f(r["methods"]["M0"]["mean_epsilon"])] for r in aux.get("calibration", [])] or [["PENDING"] * 3]))
tabs.append(table("Robustness on Wikipedia.", "tab:robust",
                  ["Perturbation", "Agreement", "$\\varepsilon_k$"],
                  [[("edge dropout " + f(r["cfg"]["edge_dropout"], 2)) if r["cfg"].get("edge_dropout")
                     else ("noise" if r["cfg"].get("noise") else "dt perturb" if r["cfg"].get("dt_perturb") else "no aggregation"),
                    f(r["methods"]["M0"]["agreement"]), f(r["methods"]["M0"]["mean_epsilon"])]
                   for r in aux.get("robustness", []) + aux.get("bound_and_spikes", [])] or [["PENDING"] * 3]))

# dose table from traces
d_all, e0_all, e2_all = [], [], []
for st in streams:
    for seed in [41, 42, 43, 44, 45]:
        q = R / "bound-check" / f"{st}_s{seed}_trace.json"
        if q.is_file():
            z = json.loads(q.read_text())
            n = min(len(z["dA"]), len(z["epsilon_M0"]), len(z["epsilon_C2"]))
            d_all.append(np.asarray(z["dA"][:n], float)); e0_all.append(np.asarray(z["epsilon_M0"][:n], float))
            e2_all.append(np.asarray(z["epsilon_C2"][:n], float))
if d_all:
    d = np.concatenate(d_all); a0 = np.concatenate(e0_all); a2 = np.concatenate(e2_all)
    rows = []
    for name, m in [("$\\Delta A{=}0$", d == 0), ("$(0,0.15]$", (d > 0) & (d <= .15)),
                    ("$(0.15,0.4]$", (d > .15) & (d <= .4)), ("$>0.4$", d > .4)]:
        if m.sum() > 20:
            rows.append([name, str(int(m.sum())), f(float(a2[m].mean()), 4), f(float(a0[m].mean()), 4)])
    tabs.append(table("Bound verification: state error by measured $\\|\\Delta A_k\\|$.", "tab:bound",
                      ["Bin", "$n$", "$\\varepsilon_{C2}$", "$\\varepsilon_{M0}$"], rows))
else:
    tabs.append(table("Bound verification.", "tab:bound", ["Bin", "$n$", "$\\varepsilon_{C2}$", "$\\varepsilon_{M0}$"], [["PENDING"] * 4]))

if an.is_file():
    d = json.loads(an.read_text())
    rows = []
    for st in streams:
        b = d.get("bootstrap", {}).get(f"epsilon_C2_minus_M0_{st}", {})
        ci = b.get("ci", [0, 0])
        qmap = dict(zip(streams, d['bh'].get('epsilon_qvalues', []))) \
            if len(d['bh'].get('epsilon_qvalues', [])) == len(streams) else {}
        rows.append([st.capitalize(), f(b.get("mean_diff", 0), 5),
                     f"[{ci[0]:.5f},{ci[1]:.5f}]", qtex(qmap.get(st, float('nan')))])
    tabs.append(table("Paired bootstrap and Benjamini--Hochberg correction.", "tab:stats",
                      ["Stream", "Mean diff", "95\\% CI", "BH $q$"], rows))
else:
    tabs.append(table("Paired bootstrap.", "tab:stats", ["Stream", "Mean diff", "95\\% CI", "BH $q$"], [["PENDING"] * 4]))

(PAP / "tables_v3.tex").write_text("% Generated from real results; do not edit by hand.\n" + "\n".join(tabs), encoding="utf-8")
print("filled values and generated", len(tabs), "tables from", len(runs), "runs")
