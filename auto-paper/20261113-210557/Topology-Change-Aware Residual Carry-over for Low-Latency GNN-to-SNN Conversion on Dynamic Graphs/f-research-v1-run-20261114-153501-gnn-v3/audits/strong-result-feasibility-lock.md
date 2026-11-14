# P1A Strong-Result Feasibility Lock (contract v3)

Executed before environment setup, from `../ccfa-startup-packet-v3/claim-evidence-matrix.md`, `strong-result-feasibility-contract.md` and `feasibility-contract.json`.

| Claim | Mechanism | Falsifying ablation | Baselines | Metric + minimum / strong / failure | Code route | Prototype | Budget | Stop-return | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| C-1 event-axis error with a real `A_k` topology term | per-snapshot error identity `B_hat - B = R A_k ((H_hat-H)W)`; caching `A_{k-1}` yields `R(A_k-A_{k-1})H W` | A5 removes aggregation, A4 freezes `A_k`, bound-violation trace | C0-C4, D1 | measured `||Delta A_k||` vs `epsilon_k`; non-zero slope / monotone growth / CI contains 0 | `scripts/gnn_campaign.py::build_graph_state`, `graph_forward`, `dcgs_encode` | 30-min single-seed smoke | 12 h, 16 GiB, 240 runs, 5 seeds, 24 trials | prototype fail / `rho` unbounded / clipping >1% / teacher vacuous / bound violated | pass |
| C-2 TCAR fidelity + strict error dominance | gated base re-anchoring, threshold recalibration, residual decay | A1 no gate, A2 no carry, A3 no recalibration, C2 matched budget | C2 (CRPI-style), C0-C4 | agreement >=98.5%, retention >=99%, `epsilon_k` strictly lowest with paired bootstrap CI excluding 0 and BH q<0.05 | same | same | same | same | pass |
| C-3 event-bound cost | recompute only when `delta_v(k)>gamma` | A1 every event, gamma sweep, A4 frozen topology | A1 upper cost, C2 lower cost | trigger <=20% of events | same | same | same | same | pass |

No binding target was lowered; all v2 numeric conditions are retained. `expected_strong` is calibrated against the measured three-seed static-graph prior range in `ZtL-sysu/gnn2snn` (T4 agreement 99.28-99.98%) and the v2 three-stream pilot. **P1A pass.** P2 may begin.
