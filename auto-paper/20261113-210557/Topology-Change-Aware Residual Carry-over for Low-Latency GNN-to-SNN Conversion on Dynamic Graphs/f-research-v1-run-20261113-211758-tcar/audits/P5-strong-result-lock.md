# P5 Strong-Result Lock (contract v2)

Executed after the final full campaign (15 test runs = 3 streams × 5 seeds) and `scripts/analyze_results.py`. Authoritative numbers: `results/aggregated.json`, `results/statistics/final-analysis.json`, `results/p4_runs/*.json`, `results/p4_auxiliary/sweeps.json`, `audits/metrics.csv`.

## Binding targets (pre-registered in `guidance-v2.md`; none was changed after results)

| Criterion | Wikipedia | MOOC | Enron | Verdict |
|---|---|---|---|---|
| (a) T=4 `agreement@K` ≥ 98.5% | 0.9990 ± 0.0008 | 0.9949 ± 0.0023 | 0.9969 ± 0.0026 | PASS |
| (a) MRR retention ≥ 99.0% | 1.0004 | 0.9988 | 0.9995 | PASS |
| (b) `ε_k` strictly lowest vs all 10 controls/ablations | 0.0173 (next best 0.0439) | 0.0110 (next best 0.0138) | 0.0113 (next best 0.0115) | PASS |
| (b) paired `ε_C4 − ε_M0` bootstrap 95% CI excludes 0 | 0.03692 [0.03636, 0.03750] | 0.00287 [0.00275, 0.00299] | 0.00044 [0.00024, 0.00064] | PASS |
| (b) Benjamini–Hochberg q < 0.05 (all streams) | q = 0, 0, 1.16e-5 | PASS |
| (c) recalibration ≤ 20% of events | 0.197 | 0.129 | 0.049 | PASS |
| (d) direction replicated on three streams | all criteria hold per stream | PASS |
| Minimum: teacher non-vacuous (≥ 5× chance) | 304× | 26× | 56× | PASS |

`d_three_streams = true` in `results/statistics/final-analysis.json`. No required experiment row is `infeasible-with-evidence`; every row is `done` in `experiment-traceability.md`.

## Every required experiment is done

B0/B1/B2 (P3 validation), C0–C4, M0, A1–A4, D1 (P4 test), S1 T-sweep {1,2,4,8}, S2 γ-sweep (6 values), R1–R3 three-stream replication, K1–K3 window lengths {1000, 5000, 10000}, per-event bound instrumentation, paired bootstrap and BH correction. Raw per-query rows and per-event traces are retained.

## Reported diagnostics (not gates; disclosed in Discussion)

- Relative `ε` reduction: 68.7% / 20.9% / 3.7%. The effect size is small on two streams.
- `agreement(M0) − agreement(C4)`: +0.004275 (CI [0.00277, 0.00589]) on Wikipedia; −0.00030 (CI [−0.00270, 0.00180]) on MOOC; −0.00072 (CI [−0.00188, 0.00036]) on Enron. Argmax agreement saturates and does not discriminate on two streams.
- C4 absolute error grows with measured topology change on MOOC and Enron, but not Wikipedia; the relative reduction is non-monotone on all three streams, with negative values in two Enron bins.
- EdgeBank∞ validation MRR 0.947 / 0.631 / 0.948 vs teacher 0.304 / 0.264 / 0.302: absolute accuracy is context only.

## Failed cycles preserved

C1–C5 (P3 teacher-gate failures), C6 (saturation clip rejected), C7 (metric-scope correction), C8 (full flush → residual decay), C9 (cost-constrained validation selection) are recorded in `correction-ledger.md` and `guidance-v2-amendment.md`. No failed run was deleted; no target was lowered after seeing a verdict; the v2 amendment was issued before the final campaign was accepted here.

## Verdict

All required experiments complete; every binding strong expected result met with real logged evidence. **P5 pass.** P5A and P6 may begin.
