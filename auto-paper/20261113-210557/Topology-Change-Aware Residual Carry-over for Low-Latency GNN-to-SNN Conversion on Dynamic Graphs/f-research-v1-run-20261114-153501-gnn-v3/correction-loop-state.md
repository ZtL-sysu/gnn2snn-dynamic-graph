# Correction Loop State (contract v3)

Created at the first v3 gate review. The v2 run's nine cycles C1-C9 remain in the v2 run root as evidence; v3 starts a fresh ledger because the user changed the method family and added three success criteria.

| Cycle | Trigger | Class | Earliest stage | Repair | Verdict |
|---|---|---|---|---|---|
| V3-1 | smoke: unbounded state recurrence inflated theta to ~1e20 | `implementation` | P2 | state driven by last converted layer activation instead of full residual chain | pass after re-smoke |
| V3-2 | smoke: missing `results/p3_teachers` directory | `implementation` | P2 | create parent directories before save | pass |

No target was lowered. All failed runs are preserved.

## Post-P5 correction cycles (contract v3)

| Cycle | Trigger | Class | Earliest stage | Repair | Verdict |
|---|---|---|---|---|---|
| C10 | DCGS emitted no graded events; P5 false on all streams | `implementation` | P4/P5 | ladder index floor -> ceil | pass after smoke |
| C11 | gate inactive on 4/5 streams | `evidence` | P3A/P4 | per-stream validation gamma with a cost band | pass after re-run |
| C12 | no cached base; residual decay hurt DCGS | `mechanism` | P4/P5 | real static-base caching + re-anchoring; no residual decay | pass after re-run |
| C13 | Enron trigger 0.26 > 0.20 hard ceiling | `implementation` | P3A/P4 | cost-ceiling-respecting fallback; comparator-class clarification | pass after re-run |
| C14 | gate inactive on large-history streams; P5 still false on 3 of 5 streams | `mechanism` | P4/P5 | trigger on measured `||Delta A_k||` with validation-selected tau; conservative threshold EMA | pass after pilot + full re-run |

No binding target was lowered in C10-C14. All cycles repaired the implementation or the mechanism; the v3 `expected_strong` conditions are unchanged. The pre-repair full campaign remains in the run log as negative evidence.
| C15 | no validation operating point inside the cost band on bimodal LastFM | `implementation` | P3A/P4 | refined pre-registered tau grid | pass after full re-run |
| C16 | LastFM paired interval covers zero;稿件/审计仍描述 C12 前的机制并声称五流全显著 | `evidence` + `integrity` | P5/P6-P21 | evidence-bounded claim narrowing + mandatory null-result disclosure + manuscript/audit consistency repair; original verdict kept false | pass on narrowed claim; original all-five condition remains FAILED |

C15 repaired a selection-grid resolution only. C16 did **not** lower any numeric binding value; it narrowed the claim scope after a genuine null result and added a disclosure obligation. The original all-five-stream verdict `d_replication: false` is preserved verbatim. No failed run was deleted.
