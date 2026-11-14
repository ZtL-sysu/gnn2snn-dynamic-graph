# P5A Pre-Draft Integrity Audit (`ccf-integrity-auditor`, full mode)

Scope: every claim/result/table/figure-source mapping in the accepted P5 evidence package. This is real evidence, not the planned-evidence audit of P1B.

| Check | Result |
|---|---|
| Claim → evidence | each of C-1/C-2/C-3 maps to `results/p4_runs/*.json` + `results/statistics/final-analysis.json`; no claim lacks a raw artifact |
| Number → raw data | all values in Tables 1–2 of `main.tex` are means/SDs over the five per-seed rows in `results/p4_runs/`; verified against `final-analysis.json` |
| Units and metric direction | `agreement`, `mrr_retention`, `recalibration_rate` are fractions; `logit_mse` is MSE; `decay_pp` is percentage points; `mean_epsilon` is a norm. `audits/metrics.csv` uses these exact units; no fraction/percent mixing |
| Splits and seeds | validation for selection, test read once; all 5 seeds retained; `inputs/frozen-identities.json` hashes the query arrays |
| Table/figure ↔ text | Table 1 described in §4.2, Table 2 in §4.2, Figs. 1–2 in §4.2, Fig. 4 in §4.3; captions state only measured quantities |
| Planned vs observed | `guidance-v2.md` targets are labelled as targets; `main.tex` reports only measured values; no target is presented as a measurement |
| Citation existence | `audits/reference-dedup-audit.md`; all 18 entries verified against Crossref/arXiv; two wrong candidate identifiers explicitly rejected |
| Failed evidence | C1–C9 failures preserved in `correction-ledger.md`; no failed run deleted or rewritten |
| Cost evidence | `recalibration_rate` from `run_campaign.py` cost counters; graded-event and latency claims limited to what was measured |

No unsupported item was repaired by invention. **Full integrity audit pass.**
