# Strong-Result Feasibility Contract (v1)

Owner: `ccf-experiment-designer` spec at `/Users/xhf/.codex/skills/ccf-experiment-designer/SKILL.md`. Machine-checkable index: `feasibility-contract.json` in this packet. **This is a pre-experiment contract. No number below is a measured result of this project.** `planned_claim` is distinct from `observed_finding`, which is updated only at P5A/P6 from accepted evidence.

## Binding targets and their calibration

Calibration source: the user's own `ZtL-sysu/gnn2snn` archive contains **measured** three-seed static-graph conversion results — fixed GCN T=4/T=8 teacher agreement 99.28–99.98% (MNIST 91.05±0.26 vs teacher 91.02±0.27; CIFAR10 54.92±0.08 vs 54.94±0.07), GatedGCN CIFAR10 test T4 agreement 99.55±0.16%, T8 99.90±0.03% (`fixed-gcn-test-three-seed-summary-v1.md`, `gated-three-teacher-seed-summary-v1.md`). These are **static** numbers. A CTDG adds an event-recursive error and a topology-change term, so the contract uses a non-inferiority allowance rather than claiming the static ceiling.

| Target | Definition | Calibration basis |
|---|---|---|
| `minimum` | T=4 `agreement@K` ≥ 95.0% on Wikipedia; MRR retention ≥ 95.0%; teacher beats B1/B2 on validation | 5 pp non-inferiority margin below the static T=4 prior range; accounts for the additional topology term |
| `expected_strong` | (a) T=4 `agreement@K` ≥ 98.5% and MRR retention ≥ 99.0% on the primary stream; (b) over a 10k-event window, TCAR agreement decay ≤ 0.5 pp while C4 (global carry-over) decays ≥ 2.0 pp, paired bootstrap 95% CI excluding 0; (c) recalibration triggered on ≤ 20% of events; (d) the direction of (a)–(c) replicates on MOOC and Enron | (a) sits at the lower edge of the measured static prior range, not above it; (b) is an effect-size/non-inferiority criterion on a paired within-run comparison, so it does not depend on absolute teacher quality; (c) follows from the mechanism (recompute only on `δ_v(k) > gamma`), with the 20% level to be confirmed by the P4 `gamma` sweep |
| `failure` | T=8 `agreement@K` < 95%; or TCAR indistinguishable from C4 at matched recomputation budget (CI contains 0); or no monotone `‖ΔA‖` dose-response; or bound (1) empirically violated; or teacher fails the B1/B2 gate | explicit pre-registered failure signals |

**No arbitrary headline gain is used.** If P4 pilot evidence shows an `expected_strong` target is not reachable with the approved mechanism and resources, the authorized path is a versioned contract change under `f-research-v1/references/research-recovery.md` (reopen the earliest affected stage, record the trigger and replacement evidence), **not** a post-hoc lowering of the target.

## Claim-level contracts

### Claim C-1 (topology term exists)

- Mechanism: `ε_k ≤ ρ ε_{k−1} + L_A ‖ΔA_k‖ ‖s_{k−1}‖ + c/T + η_k`.
- Prerequisite assumptions: A1–A7 in `theoretical-feasibility-audit.md`; measured `ρ`; a well-defined normalized `A_k`; frozen event order.
- Falsifying ablation: A3 (frozen static base) and A5 (`‖ΔA‖` quartile stratification); bound-violation rate.
- Exact dataset/split: Wikipedia chronological 70/15/15, frozen `validation_query` 1024 and `test_query` 4096; 10k-event windows; test read once at P5.
- Primary metric and direction: slope of `ε_k` vs cumulative `‖ΔA_k‖` (higher = stronger topology dependence); bound-violation rate (lower).
- Baselines: simple C0; strongest feasible C4; matched B0.
- Minimum / strong / failure: non-zero slope with CI excluding 0 / monotone across quartiles on 3 streams and zero bound violations / slope CI contains 0 or bound violated.
- Implementation readiness: new `A_k` tracker + per-event error logging in the run root; missing components are the tracker and a CPU/MPS operator check; prototype milestone = one seed end-to-end in 30 min at P2.
- Reviewer question: "Why is this not static-graph conversion with more steps?"

### Claim C-2 (TCAR improves fidelity at low T)

- Mechanism: residual carry-over on touched nodes plus topology-gated base/threshold refresh removes `η_k` and attacks `‖ΔA_k‖`.
- Assumptions: conversion-friendly teacher (ReLU/clip, folded BN), consistent threshold/gauge, calibration coverage.
- Falsifying ablations: A2 (no carry-over), A1 (no gate), C4 matched-budget comparison.
- Dataset/split/metric: as above; primary `agreement@K` (higher), secondary MRR retention and logit MSE (lower).
- Baselines: B1/B2 simple; C0 matched; C1–C4 method-family, with C4 the strongest.
- Minimum / strong / failure: 95.0% / 98.5% + the decay contrast / T=8 < 95% or CI contains 0 vs C4.
- Implementation readiness: reimplement differential coder independently (archive has no blanket license), reuse the archive's calibration procedure; prototype at P2; 5 seeds; hyperparameter search ≤24 (T,gamma) combinations; reproducibility artifacts = config+SHA, raw jsonl, END_OF_RUN_OK.
- Reviewer question: "Is your gain just CRPI?"

### Claim C-3 (cost bounded by topology changes)

- Mechanism: recompute only when `δ_v(k) > gamma`.
- Falsifying ablation: A1 recompute-every-event vs M0 at matched accuracy; S2 gamma sweep.
- Metric: recalibration trigger rate (lower), graded events/event, local PyTorch ms/event (CPU and MPS recorded separately).
- Baselines: A1 upper-cost, C4 lower-cost, B0 ANN inference.
- Minimum / strong / failure: ≤50% / ≤20% with no accuracy loss vs A1 / no cost–accuracy trade-off.
- Implementation readiness: event loop already instrumented; no new dependency.
- Reviewer question: "Is it affordable, or accurate only because it recomputes everything?"

### Claim C-4 (topology-driven, not depth-driven)

- Falsifying ablation: A4 static-graph control on frozen neighbor sets.
- Strong check: `(TCAR − C4)` advantage on frozen topology has CI containing 0 while the dynamic-stream advantage excludes 0.
- Reviewer question: "Would the same trick help on a static graph?"

## Compute / memory / runtime budget (finite, not permission to buy compute)

- Machine: Apple M1, 8 cores, 16 GiB unified memory, MPS available, no CUDA. Disk free 339 GB.
- Per run: ≤20 min wall clock; total ≤120 seed-level runs; total ≤12 h.
- Seeds: 5 for every main comparison; each per-seed value retained.
- Hyperparameter search: ≤24 combinations (T ∈ {1,2,4,8} × gamma grid ≤6); all trials logged; test IDs frozen before tuning.
- Model: ≤100k trainable parameters; streams ≤15 MB.
- Remote compute: not authorized, not used. If the budget is exhausted, the autonomous correction loop may reduce optional streams but may not drop the six ablations or the seed count on the primary stream.

## Reviewer-question coverage

Each main experiment, each of the six ablations, each robustness/stratification test, and each efficiency measurement above is tagged with the reviewer question it answers in `claim-evidence-matrix.md`. No experiment is included solely to fill a table.

## Explicit stop-and-return conditions (return to scenario/method design before P2, not train toward an implausible target)

1. P2 prototype cannot complete one seed end-to-end within 30 minutes, or required MPS operators are unsupported with no CPU fallback within the ceiling → reopen G5 with evidence-preserving scaling.
2. Measured `ρ ≥ 1` with no bounded-horizon repair, or `A_k` cannot be defined for the chosen aggregation → reopen G3 (theory).
3. Calibration clipping rate on validation >1% with no percentile repair → reopen G3/A3.
4. ANN teacher fails to beat EdgeBank/Base3 on validation → return to method design; fidelity on a vacuous teacher is not a contribution.
5. CRPI-style control cannot be implemented, or its public code/mechanism proves materially different from the adapted control → reopen G4/G6; the strongest discriminator cannot be missing.
6. Structured novelty sweep at P12 finds a directly overlapping paper → reopen G4 and narrow or replace the claim.
7. Any binding target is missed at P5 → do not write; enter the authorized correction loop with a versioned replacement contract, preserving all negative evidence.
