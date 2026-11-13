# Validation Report — f-guidance-builder-v1

Executed 2026-11-13, from `/Users/xhf/code/phd-project/phd-gnn2snn-dynamic-graph`, with `/Users/xhf/miniconda3/bin/python`. Run folder: `auto-paper/20261113-210557/Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs/`.

## Commands and exact stdout

```
/Users/xhf/miniconda3/bin/python _probe/build_state.py "<RUN>"
built feasibility-contract.json and pipeline-state.json
packet evidence files: 7 claims: 3 stages: 12

/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/validate_guidance.py \
  "<RUN>/guidance.md" --strict --packet "<RUN>/ccfa-startup-packet"
Guidance structure is valid.
EXIT=0

/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py \
  "<RUN>/pipeline-state.json" --complete
PASS: ordered, current evidence; scientific/visual gate judgment remains required.
EXIT=0

/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py \
  "<RUN>/pipeline-state.json" --before G0
PASS: ordered, current evidence; scientific/visual gate judgment remains required.
EXIT=0
```

## What was actually checked

- `validate_guidance.py --strict`: all eight required `##` sections present with non-thin bodies; a `Figure/Table Decision Rules` section present; required terms (dataset access, baselines, primary/secondary metrics, failure signal, hardware budget, traceability) present; canonical six-section numbered outline present and no prohibited top-level section; no unresolved placeholder patterns.
- `--packet`: all seven CCFA startup Markdown artifacts present and non-empty; `feasibility-contract.json` has `schema_version: 1`, `decision: proceed`, three claims with all nineteen substantive string fields, valid `metric_direction`, HTTP(S) `dataset_url`, and positive finite `runtime_hours`/`memory_gb` plus integer `seeds`/`search_trials`; every required artifact is SHA-256 bound inside the packet and every hash matches the file on disk.
- `pipeline_state.py --complete`: canonical stage order `CCFA-startup, G0..G8, validation, handoff`; every stage `passed` with `gate_verdict: pass`, matching `contract_version`, non-empty and hash-valid `inputs` and `evidence`, no gap before a passed stage; `history` matches the passed stages in order; `contract` is non-empty and hash-valid.
- `--before G0`: all predecessors of G0 passed.

## Limits of these validators (explicit)

- They check **structure, ordering, and hash binding**, not scientific validity. The validators themselves print "scientific/visual gate judgment remains required."
- No experiment was run. No `expected_strong` value has been observed. `planned_claim` remains distinct from `observed_finding`.
- Novelty confidence remains moderate and requires the P12/P14 structured duplicate sweep.
- The official Neurocomputing guide-for-authors limits are not yet verified; `submission-constraints.md` is created at P20, not here.

## Handoff

`ccfa-startup-packet/startup-decision.md` = `proceed`. This `guidance.md` is the authoritative contract for `f-research-v1` P0. All local process files and deliverables of that run must stay inside a `f-research-v1-run-*` root inside this folder.
