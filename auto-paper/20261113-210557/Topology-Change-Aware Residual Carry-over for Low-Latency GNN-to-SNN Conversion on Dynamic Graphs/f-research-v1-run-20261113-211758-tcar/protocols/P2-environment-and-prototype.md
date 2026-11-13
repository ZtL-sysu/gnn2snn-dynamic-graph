# P2 Protocol: Environment, Accelerator and Prototype

## Environment decision

- Python: `/Users/xhf/miniconda3/bin/python` (3.14.6), torch 2.13.0. A project-specific Conda environment is **not** created in this phase; the smoke prototype needs only `numpy` and `torch`, both already present. If P3 requires additional packages, a project-specific environment is created then and recorded in `audits/P2-environment-check.md` as an addendum. No global Conda configuration is changed.
- Accelerator: `torch.backends.mps.is_available() = true`, `cuda_available = false`, `recommended_device = mps`. Operator-level probe at P2: MPS matmul and MPS ReLU both finite; CPU matmul available. Per-operator fallback is recorded rather than assumed; the main smoke loop runs on CPU for determinism and speed at this scale.
- Remote execution: not used, not authorized.

## Frozen identities

`inputs/frozen-identities.json` records, for each of the four Zenodo-derived frozen streams, the file SHA-256, event count, and the shape/dtype/SHA-256 of `validation_query`, `test_query` and `catalog`. Validation IDs alone select `T`, `gamma` and calibration percentile; test IDs are read once at P5. The file explicitly records that these IDs were used in a predecessor local project and are therefore **non-blind**.

## Runnable commands

```bash
export CTDG_FROZEN_STREAM=/path/to/local/wikipedia-events.npz
/Users/xhf/miniconda3/bin/python scripts/prototype_smoke.py
```

The script writes `results/p2-prototype/config.json`, `config.sha256`, `metrics.json`, `environment.json`, `raw_results.jsonl` and `END_OF_RUN_OK`. It takes the data path from the environment so that no machine-specific path is embedded in a published artifact.

## What the prototype checks

Frozen stream loading; node-ID compaction; conversion-friendly ReLU/clip teacher with an event-recursive node state; label-free 99.9th-percentile activation calibration; rate-coded IF conversion with soft reset over `T` micro-steps; a hard-reset control (C0-style) and a CRPI-style global carry-over control; neighbor-set topology-change tracking; per-event `epsilon_k`, `delta_v(k)`, `||ΔA||` proxy and agreement instrumentation; MPS/CPU operator probing; and the R63-style artifact contract.

## What the prototype deliberately does NOT do

It does not train a teacher, does not use a train/val/test split, does not evaluate the 4096 test queries, does not implement TCAR's topology-change gate, does not implement C1-C3 baselines, and does not produce any number that may appear in the manuscript. Its `coverage` is `smoke/2000-events`.

## Gate to advance to P3

Runnable protocol, local environment checks, commands, accelerator decision, frozen identities, and artifact paths all exist inside the run root. **P2 passes structurally**, with the P1B-added binding condition that P3 must first train a non-vacuous teacher and add state normalization before any conversion claim is made.
