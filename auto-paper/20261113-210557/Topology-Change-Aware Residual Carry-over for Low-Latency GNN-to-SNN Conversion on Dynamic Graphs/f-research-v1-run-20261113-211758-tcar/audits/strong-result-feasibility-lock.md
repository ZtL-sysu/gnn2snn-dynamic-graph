# Strong-Result Feasibility Lock (P1A)

Executed **before any environment setup**, using `../ccfa-startup-packet/claim-evidence-matrix.md`, `../ccfa-startup-packet/strong-result-feasibility-contract.md` and `../ccfa-startup-packet/feasibility-contract.json`. The packet exists, so no local-equivalent reconstruction was needed; its absence would have been recorded instead.

| Claim | Mechanism present | Falsifying ablation | Simple / strong / matched baseline path | Metric + direction | `minimum` / `expected_strong` / `failure` | Code / adaptation route | Prototype milestone | Compute / memory / runtime | Seeds / search | Stop-and-return | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-1 topology term | yes: event-axis recursion with `L_A‖ΔA_k‖‖s‖` | A3, A5, A4, bound-violation rate | C0 / C4 / B0 | slope of `epsilon_k` vs cumulative `‖ΔA‖` (higher); violation rate (lower) | non-zero slope / monotone quartiles on 3 streams + zero violations / CI contains 0 or bound violated | new `A_k` tracker + per-event logging, plain PyTorch | one seed end-to-end <=30 min at P2 | 12 h, 16 GiB, <=20 min/run | 5 seeds, <=24 trials | P2 prototype fail, `rho` unbounded, clipping >1%, teacher gate fail, bound violated | **pass** |
| C-2 low-latency fidelity | yes: carry-over removes `eta_k`, gate attacks `‖ΔA‖` | A2, A1, C4 matched budget, S1 T sweep | C0 / C1-C4 / B0 | `agreement@K` (higher), MRR retention | 95.0% / 98.5% + decay contrast + 3-stream replication / T=8 <95% or CI contains 0 | differential coder reimplemented, calibration reused | same | same | same | same | **pass** |
| C-3 event-bound cost | yes: recompute only when `delta_v(k) > gamma` | A1, S2 gamma sweep, A4 static control | A1 / C4 / B0 | recalibration trigger rate (lower) | <=50% / <=20% with no accuracy loss / no trade-off | event loop instrumented | same | same | same | same | **pass** |

## Integrity checks on the lock

- `expected_strong` is **unchanged** from the guidance contract. No target was lowered, no result invented, and no proposed-method training was started before P2.
- Targets are baseline-calibrated against measured three-seed static-graph prior ranges (T=4 teacher agreement 99.28–99.98%) plus a paired within-run effect-size criterion; they are not desired headline gains.
- Test identity isolation is explicit: `inputs/frozen-identities.json` hashes the four streams and the 1024 validation / 4096 test query arrays. Validation alone selects hyperparameters; test is read once at P5. The IDs are disclosed as non-blind.
- Every claim has a mechanism, a falsifying ablation, a direct baseline path, a code route, a prototype, a finite budget, and a stop-and-return condition.

## P1A gate

All three binding claims `pass`. Only an all-pass plan enters P2. **P1A pass.**

P1A does **not** grant permission to relax P5: the approved strong result must still be met with real logged evidence before any drafting.
