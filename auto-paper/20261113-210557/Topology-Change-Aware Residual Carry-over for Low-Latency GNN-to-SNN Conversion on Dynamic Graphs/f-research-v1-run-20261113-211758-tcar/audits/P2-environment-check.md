# P2 Environment and Prototype Check (real execution record)

Executed 2026-11-13 21:18–21:19 +0800 with `/Users/xhf/miniconda3/bin/python`.

## Environment probe (measured)

| Item | Value |
|---|---|
| Python | 3.14.6 |
| torch | 2.13.0 |
| MPS available | true |
| CUDA available | false |
| MPS matmul finite | true |
| MPS ReLU finite | true |
| CPU matmul | true |
| OS / CPU / RAM | macOS Darwin 24.6.0, Apple M1, 8 cores, 16 GiB (from `hardware_probe.py` at the guidance phase) |

## Frozen identities (measured)

| Stream | Events | validation query IDs | test query IDs | file SHA-256 prefix |
|---|---:|---:|---:|---|
| wikipedia | 157,474 | 1,024 | 4,096 | `4851f7bb3c21074d` |
| mooc | 411,749 | 1,024 | 4,096 | `739bea635f55ab15` |
| reddit | 672,447 | 1,024 | 4,096 | `cf6241560c42a763` |
| lastfm | 1,293,103 | 1,024 | 4,096 | `38ebd46df6f5b400` |

Full array-level SHA-256, shapes and dtypes are in `inputs/frozen-identities.json`. Raw `.npz` files are not uploaded.

## Prototype run 1 — FAILED evidence verification (preserved, not deleted)

`coverage: smoke/2000-events`, seed 41, hidden 16, T=4. Output: `agreement_hard_reset_fraction = 0.003`, `agreement_global_carry_over_fraction = 0.038`, `mean_epsilon_hard = 13.9905`, `mean_epsilon_carry = 10.7833`, `clipping_rate = 0.001`.

**Diagnosis**: the IF conversion helper did not actually integrate over `T` micro-steps (it performed one update) and divided the input current by an extra factor of `T`. Consequently almost no spikes were emitted and the decoded activation was near zero while the ANN activation was large. This is a **code defect**, not a scientific result.

## Prototype run 2 — repaired and re-run

Fix: integrate constant current `z_pos * scale` across `T` steps with subtractive reset, decode `spikes / (T * scale)`, and carry the residual potential across events for the C4-style control. Script SHA-256 after repair and path parameterization: `a2694bf951c9b425cd207331cd65788b7b528a11a9715fc9f726d4fdd80316d7`.

| Quantity | Run 1 (defective) | Run 2 (repaired) |
|---|---:|---:|
| wall clock (s) | 1.481 | 0.981 |
| `agreement_hard_reset_fraction` | 0.003 | 0.0755 |
| `agreement_global_carry_over_fraction` | 0.038 | 0.33 |
| `mean_epsilon_hard` | 13.9905 | 8.4969 |
| `mean_epsilon_carry` | 10.7833 | 3.4068 |
| `mean_delta_v` | 0.3723 | 0.3723 |
| `clipping_rate` | 0.001 | 0.001 |
| `calibration_theta` | 12.3018 | 12.3018 |
| `nodes_in_subset` | 643 | 643 |

The repaired run shows (i) a working conversion code path, (ii) measurable per-event `epsilon_k`, `delta_v(k)` and `||ΔA||` proxy, and (iii) a clear qualitative signal that cross-event residual carry-over reduces state error relative to hard reset (10.78→3.41, 8.50→3.41; agreement 0.038→0.33 and 0.003→0.0755). This **supports the instrumentation's discriminating power and is consistent with CRPI**, not a claim of TCAR superiority.

## What is NOT established by these numbers

- No claim about `expected_strong` (95% / 98.5%) is supported. The teacher is randomly initialized and untrained, the residual state accumulates toward its clip ceiling, and the candidate scoring is dominated by near-ties. Absolute agreement here is meaningless as a fidelity measurement.
- The topology-change gate (TCAR), C1-C3 conversion controls, EdgeBank/Base3, and all six ablations are not implemented yet.
- Clipping rate 0.001 is a **smoke-subset** value on an untrained teacher; assumption A4 must be re-checked on the trained teacher at P3.
- These numbers must never appear in the manuscript as findings, and are excluded from the formal `metrics.csv` at collaboration checkpoints.

## Runtime budget implication

One seed over 2,000 events completes in under one second on CPU. This satisfies the 30-minute prototype milestone by a wide margin, but it does **not** validate the 20-min/seed ceiling for a full 157k-event window with a trained teacher; that timing check is owed at P3 before the 12 h campaign ceiling is accepted.

## P2 gate

Protocols, environment checks, commands, accelerator decision, frozen identities, and artifact paths all exist in the run root; the code path defect was found and repaired before the gate was declared passed. **P2 pass**, with the P1B binding conditions carried into P3.
