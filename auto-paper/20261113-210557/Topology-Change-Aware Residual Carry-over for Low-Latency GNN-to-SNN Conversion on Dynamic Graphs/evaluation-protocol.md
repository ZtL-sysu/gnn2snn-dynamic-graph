# Evaluation Protocol (pre-registered at guidance time)

This protocol is inherited from the local predecessor's chronological CTDG protocol and is frozen here before any tuning. Any change requires a versioned contract update recorded in `collaboration/PROJECT.md` and the run root.

## Data identity

- Streams: Wikipedia (primary), MOOC, Enron (replication); Reddit/LastFM optional robustness.
- Source: Zenodo `10.5281/zenodo.7213796`, CC BY 4.0. Local frozen `.npz` copies carry `src, dst, timestamp, edge_id, original_row`, node label arrays, `catalog`, and pre-frozen `validation_query` (1,024) / `test_query` (4,096) with weights and bins.
- Freeze action at P2: compute SHA-256 of every `.npz` and of the query-ID arrays; write `inputs/frozen-identities.json`. No trial may read test queries before P5.

## Split

Chronological 70/15/15 by event timestamp. Training events: teacher training **and** label-free activation histogram calibration. Validation queries: select `T`, `gamma`, calibration percentile, and early stopping. Test queries: single final evaluation at P5 after the contract is locked. The test IDs are **not blind** (used in a predecessor local project); this is disclosed in the manuscript.

## Primary metric

**End-of-window teacher→SNN decision agreement** (`agreement@K`): fraction of evaluation queries in the last segment of a `K`-event window (default `K = 10,000`) where the argmax over the candidate catalog of the converted SNN logits equals that of the frozen ANN teacher. Higher is better. Reported per seed, then mean ± sample SD with N=5, plus paired bootstrap 95% CI for differences.

Rationale: the claim is about conversion fidelity, not leaderboard ranking. Agreement is invariant to the teacher's absolute quality and directly measures the accumulated error that the bound describes.

## Secondary metrics

- **MRR retention**: SNN MRR / ANN teacher MRR on the same queries (higher is better), plus AP/AUC as supporting context.
- **Logit MSE** and teacher→SNN KL on the candidate score vector (lower is better).
- **Error-state norm** `ε_k = ‖ŝ_k − s_k‖`, **topology change** `‖ΔA_k‖`, and relative neighbor-set change `δ_v(k)`, logged per event for bound checking.
- **Cost**: graded-event count per event, number of base/threshold recalibrations, recalibration trigger rate, parameter count, wall-clock ms per event on local PyTorch (CPU/MPS recorded separately).
- **Statistical checks**: 5 seeds; paired bootstrap 95% CI over queries for every main comparison; BH correction across the ablation family; every per-seed value retained in `results/` and in `metrics.csv` at the collaboration checkpoints.

## Required experiment rows (mirrors `guidance.md`)

| ID | Condition | Purpose |
|---|---|---|
| B0 | ANN teacher (oracle upper bound) | reference for all retention numbers |
| B1 | EdgeBank / recent popularity | simple baseline sanity |
| B2 | Base3 k=10 | second simple baseline |
| C0 | same teacher + rate-coded IF, hard reset, no calibration | matched internal control |
| C1 | SNNC-AP-light calibration (no carry-over) | calibration-only control |
| C2 | DCGS `MTH_diff` graded differential coder | coder-family control |
| C3 | QCFS/FTBC clipped conversion | low-latency conversion control |
| C4 | CRPI-style **global** carry-over (no topology gate) | strongest discriminator |
| M0 | TCAR full | main method |
| A1–A6 | six ablations in `theoretical-feasibility-audit.md` | mechanism isolation |
| R1–R3 | three streams | replication |
| S1 | T ∈ {1,2,4,8} sweep | latency/fidelity frontier |
| S2 | `gamma` sweep | cost/accuracy frontier |
| D1 | directly trained spiking encoder, matched size | parallel control, not oracle |

## Runtime accounting

Every run writes `config.json`, `config.sha256`, `metrics.json`, `raw_results.jsonl`, an `END_OF_RUN_OK` marker (or an explicit failure marker), the hardware profile, the seed, and the exact command. Failed runs are preserved as evidence and are never deleted or rewritten. This follows the predecessor's `R63-results/` artifact pattern.

## Stopping criteria

- Stop the campaign when all required rows are `done`, the strong-result lock is satisfied, and the budget (≤120 runs, ≤12 h) has not been exceeded.
- Stop and return to guidance design if: the P2 30-minute prototype cannot complete one seed; the ANN teacher fails to beat B1/B2 on validation; assumption A1 (`ρ`) or A4 (clipping rate) fails; or the bound (1) is empirically violated. These are `strong-result-feasibility-contract.md` stop-and-return conditions, not negotiable thresholds.
