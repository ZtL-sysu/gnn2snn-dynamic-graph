# Theoretical Feasibility Audit

## 1 The mechanism, stated precisely

Let a continuous-time dynamic graph be an ordered event stream `e_1 … e_K`, `e_k = (u_k, v_k, t_k, f_k)`. A lightweight ANN teacher keeps a node-state vector `s_v ∈ R^d`. At event `k` it computes a message through a ReLU/clip MLP `φ`, updates the two endpoint states through a residual/GRU-like map `U`, and scores candidate destinations with a ReLU MLP `ψ`. The conversion replaces every ReLU layer in `φ`, `U`, `ψ` by an integrate-and-fire (IF) unit with soft (subtractive) reset and a label-free percentile calibration over training activations; graded/differential events encode the residual. Inference runs `T` micro-steps per event.

**Why this should help**: conversion error is not an i.i.d. per-event perturbation. The same node state that carries the error is the input to the next event. Therefore the error recurs along the event axis. In addition, the neighbor set entering the aggregation changes from event to event, which changes the linear operator applied to the state. Neither effect exists in static-graph conversion (one forward pass, fixed adjacency) nor in RL continuous control (fixed network, changing observations but no changing aggregation operator).

## 2 The bound

For a single layer, the standard rate-coded conversion identity is

`E^l_i = Σ_j w_ij E^{l−1}_j + (V^l_i(T) − V^l_i(0)) / T`,

i.e. local error is a weighted sum of upstream errors plus the un-emitted residual membrane potential divided by `T` (BayesianSpikeFusion, Frontiers 2024; SNNC-AP gives a second-order propagation view). Write `c/T` for the per-window quantization floor.

Lift this to the event axis. Let `ε_k = ‖ŝ_k − s_k‖` be the norm of the difference between converted and ANN node states after event `k`, `A_k` the (normalized) neighbor-aggregation operator induced by the event, `ρ` the Lipschitz constant of the state update `U` with respect to its state argument, `L_A` the Lipschitz constant with respect to the aggregation operator, and `η_k` the norm of the residual potential that is discarded at a hard reset. Then, under the assumptions listed in §3,

`ε_k ≤ ρ · ε_{k−1} + L_A · ‖A_k − A_{k−1}‖ · ‖s_{k−1}‖ + c/T + η_k`      (1)

and by unfolding,

`ε_K ≤ ρ^K ε_0 + Σ_{k=1..K} ρ^{K−k} ( L_A ‖ΔA_k‖ ‖s_{k−1}‖ + c/T + η_k )`.      (2)

The **topology-change term** `L_A ‖ΔA_k‖ ‖s_{k−1}‖` is the new quantity. It says: even with perfect per-window coding (`c/T → 0`, `η_k → 0`), a conversion that reuses a static base computed under `A_{k−1}` incurs an error that grows with the change in the aggregation operator. This is exactly the assumption violated when the `affine-base` static base `Wh₀+b` and shared residual prefix from the user's `gnn2snn` archive are carried into an evolving graph.

**Mechanism response (TCAR)**:
1. For any node touched by event `k`, carry the residual membrane potential into the next window instead of hard-resetting. This removes `η_k` for those nodes (a first-order correction, as in CRPI, but restricted to touched nodes and applied on a graph).
2. Track the relative neighbor-set change `δ_v(k) = |N_v(k) ⊖ N_v(k−1)| / max(|N_v(k−1)|, 1)`. Only when `δ_v(k) > gamma` do we recompute that node's static base and recalibrate its threshold and flush the shared residual prefix. Between such events the cached base is reused. This directly targets the `‖ΔA_k‖` term where it is large and avoids paying the recomputation cost where the operator is effectively unchanged.
3. Consequence to test: end-of-window disagreement should scale with the cumulative topology change, and TCAR should flatten that scaling; the number of recomputations should scale with the count of `δ_v(k) > gamma` events, not with `K`.

The bound is a **claim to be tested**, not an established theorem of this project. P4 must measure `ε_k`, `‖ΔA_k‖`, `δ_v(k)` and verify that (1) is not violated within numerical tolerance; if it is violated, the theoretical contribution is falsified and the correction loop reopens G3.

## 3 Assumptions (each is a possible falsifier)

| # | Assumption | Why needed | How it is checked / what breaks it |
|---|---|---|---|
| A1 | `U` is Lipschitz in state with constant `ρ < 1` (or `ρ ≈ 1` with bounded horizon) | gives a non-explosive recursion | estimate `ρ` empirically on training events; if `ρ > 1` the bound grows exponentially and the long-window claim must be narrowed to bounded horizons |
| A2 | aggregation is a linear/normalized operator `A_k` with bounded `‖A_k‖` and finite `‖ΔA_k‖` | defines the topology term | log the neighbor-set snapshots; if message passing is nonlinear in a way that makes `A_k` ill-defined, replace with a Jacobian-based measure and record the change |
| A3 | teacher nonlinearities are conversion-friendly (ReLU/clip, no softmax, no unfused BN) | the layer recursion applies | code review at P2; any BN must be folded before calibration, following the user's archive procedure |
| A4 | label-free percentile calibration on training activations covers the test activation range | bounds clipping error | measure clipping rate on validation; if >1%, widen the percentile or record the violation |
| A5 | graded/differential events are decoded consistently with the calibrated threshold/gauge | otherwise a systematic bias mimics `η_k` | reuse the archive's gauge-consistency regression checks (`check_*.py` ideas, reimplemented) |
| A6 | event order is fixed and the neighbor-set history is reproducible | `δ_v(k)` must be well-defined | freeze stream hashes and split IDs before tuning; log every trial |
| A7 | `T` is small (1–8) and each window has enough events to estimate rates | `c/T` is the dominant controllable term | T-sweep ablation; if T=8 still fails the minimum, the low-latency claim is falsified |

Supporting works for these assumptions: the layer recursion and threshold/calibration origin (Rueckauer-type normalization, BayesianSpikeFusion 2024, SNNC-AP 2022), conversion bounds (CASC 2024), and cross-step error correlation (CRPI 2026). The *graph* extension is this project's proposed contribution, not a cited result.

## 4 Falsifying ablations (each kills a specific part)

| Ablation | What it removes | Prediction if the mechanism is real | What would falsify it |
|---|---|---|---|
| A1 no-topology-gate (recompute every event) | the event-triggering policy | similar accuracy, **much higher** recomputation count | identical accuracy *and* identical recomputation count → the gate does nothing |
| A2 no-carry-over (hard reset every window) | `η_k` suppression | faster error growth along the window | no difference in end-of-window disagreement (CI contains 0) → carry-over is not the cause |
| A3 frozen static base (no recalibration) | the base/threshold refresh | degradation concentrated in high-`‖ΔA‖` strata | no degradation anywhere → the topology term is negligible and the central claim fails |
| A4 static-graph control (freeze topology) | `‖ΔA_k‖` entirely | TCAR advantage shrinks toward zero | TCAR advantage is unchanged → the gain is not topology-driven |
| A5 `‖ΔA‖` stratification | dose-response | disagreement gap grows monotonically with topology-change quartile | no monotone trend / reversal → bound does not describe the data |
| A6 `gamma` and `T` sweeps | cost/accuracy trade-off | a Pareto frontier between recomputation rate and disagreement | no trade-off → the cost claim is unsupported |

Additionally, a **CRPI-style global carry-over** control (residual carried at every step for every node, no topology gate) is the strongest single discriminator: if TCAR does not beat it at matched recomputation budget, the paper is incremental.

## 5 Failure modes that would make this unsuitable for Neurocomputing

- The topology term is empirically negligible: the work collapses into "CRPI on a graph" (incremental).
- The ANN teacher is too weak to be a meaningful conversion target (e.g. near-chance MRR); then fidelity numbers are vacuous. Mitigation: require the teacher to beat the simple EdgeBank/Base3 controls on validation before P4.
- Test identifiers were used in a previous local project, so the evaluation is not blind. Mitigation: freeze IDs, disclose honestly in Discussion, and treat absolute MRR as context rather than the main claim.
- The bound is derived but not empirically checkable with the instrumentation budget. Mitigation: log `ε_k`, `‖ΔA_k‖`, `δ_v(k)` per event from the prototype onward.
- No neuromorphic hardware: any energy statement would be unsupported. Mitigation: report graded-event counts, recomputation counts, parameter counts, and local PyTorch wall-clock latency only, framed as positive evidence boundaries.
