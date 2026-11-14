# Experiment Traceability (contract v3)

| Guidance requirement | Row | Required artifact | Status |
|---|---|---|---|
| 5 public streams, frozen splits | D0 | `results/p3_data/stream-summary.json`, `inputs/frozen-identities.json` | done (P2) |
| Real `A_k` and measured `||Delta A_k||` (E6) | G0 | `results/bound-check/*_trace.json` | pending |
| Baseline-first B0/B1/B2 + teacher non-vacuity | B0-B2 | `results/p3_baselines/*` | pending |
| 11 methods/controls/ablations x 5 streams x 5 seeds | M0-C4-A1-A5-D1 | `results/p4_runs/*`, `results/aggregated.json` | pending |
| T-curve {1,2,4,8,16} | S1 | `results/p4_auxiliary/sweeps_v3.json` | pending |
| Spike/firing-rate/SynOps statistics | S2 | `results/aggregated.json` per-method fields | pending |
| Error decomposition clipping/quant/residual | S3 | `results/aggregated.json` per-method fields | pending |
| Architecture ablations (depth, aggregator) | S4 | `results/p4_auxiliary/sweeps_v3.json` | pending |
| Calibration ablations (percentile) | S5 | `results/p4_auxiliary/sweeps_v3.json` | pending |
| Robustness (edge dropout, noise, dt perturbation) | S6 | `results/p4_auxiliary/sweeps_v3.json` | pending |
| Bound verification with real `A_k` | S7 | `results/bound-check/*_trace.json`, `results/statistics/final-analysis.json` | pending |
| Paired bootstrap + BH | S8 | `results/statistics/final-analysis.json` | pending |
| Latency-Pareto | S9 | `results/p4_auxiliary/sweeps_v3.json`, `paper/figures/*` | pending |
| >=21 pages, >=40 refs (E8) | W0 | `paper/main.pdf`, `paper/references.bib` | pending |
