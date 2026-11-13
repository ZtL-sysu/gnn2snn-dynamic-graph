# Guidance Pipeline State

- Run: `20261113-210557`
- Selected direction: Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs (TCAR)
- Target venue: Neurocomputing (Elsevier, CAS computer-science Tier 2, JCR AI Q1, non-OA by default)
- Canonical order: `CCFA-startup -> G0 -> G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 -> validation -> handoff`
- Allowed statuses: `pending`, `running`, `passed`, `blocked`, `superseded`. `skipped` is not valid.
- Structured authority: `pipeline-state.json` in this folder, whose `contract`, per-stage `inputs` and `evidence` are SHA-256 bound to real files in this run root. This Markdown is its readable view.

| Stage | Status | Started | Passed | Evidence / decision |
|---|---|---|---|---|
| CCFA-startup | passed | 2026-11-13T21:05+0800 | 2026-11-13T21:12+0800 | Startup packet decision `proceed`; eight artifacts including `feasibility-contract.json` hash-bound to the seven Markdown artifacts. Red-team F1-F8 each has a repair and score-change condition. |
| G0 | passed | 2026-11-13T21:02+0800 | 2026-11-13T21:07+0800 | Real web searches on conversion theory (SNNC-AP, CASC, BayesianSpikeFusion), cross-step error (CRPI ICML 2026, MPEF ICML 2026), CTDG baselines (TAMI NeurIPS 2025, HyperEvent, TGB leaderboard, DyGLib) and venue facts; `literature-baseline-matrix.md` separates direct-rerun from literature-context. |
| G1 | passed | 2026-11-13T21:00+0800 | 2026-11-13T21:05+0800 | Zenodo `10.5281/zenodo.7213796` HTTP 200, CC BY 4.0, direct file URLs; a file HEAD returned 200 with attachment disposition; four local frozen `.npz` streams opened with `numpy.load` and array shapes recorded. |
| G2 | passed | 2026-11-13T21:07+0800 | 2026-11-13T21:10+0800 | `evaluation-protocol.md`: chronological 70/15/15 with frozen query IDs, `agreement@K` primary metric, secondary retention/MSE/cost metrics, 5 seeds, paired bootstrap CI, BH correction, per-run artifacts. |
| G3 | passed | 2026-11-13T21:07+0800 | 2026-11-13T21:11+0800 | `theoretical-feasibility-audit.md`: event-axis error recursion with an explicit topology-change term, seven assumptions A1-A7, six falsifying ablations, and failure modes. |
| G4 | passed | 2026-11-13T21:02+0800 | 2026-11-13T21:08+0800 | No retrieved work combines ANN-to-SNN conversion with CTDG and a topology-change term. Closest threats CRPI/MPEF have no graph; SpikeNet/Dy-SIGN are direct-trained. Novelty confidence explicitly **moderate**, pending structured DOI/arXiv sweep at P12/P14. |
| G5 | passed | 2026-11-13T20:49+0800 | 2026-11-13T21:09+0800 | `hardware_profile.py` output: M1/8 cores/16 GiB/MPS/no CUDA/339 GB free. Plan scaled to <=100k parameters, <=15 MB streams, <=20 min per seed, <=120 runs, <=12 h. Static SuperPixel teacher line explicitly rejected as infeasible. P2 30-minute prototype is a binding condition. |
| G6 | passed | 2026-11-13T21:07+0800 | 2026-11-13T21:10+0800 | Four comparison classes; conversion-family baselines C1-C4 are direct reruns/adaptations; dynamic-prediction SOTA explicitly downgraded to literature-context with the 28,800 s predecessor timeout recorded; six mechanism-isolating ablations. |
| G7 | passed | 2026-11-13T21:11+0800 | 2026-11-13T21:12+0800 | `strong-result-feasibility-contract.md` binds each claim to mechanism, falsifying ablation, baselines, metric-calibrated min/strong/failure, code path, prototype, 5 seeds, <=24 search trials, 12 h/16 GiB budget, and stop-and-return conditions. Targets calibrated against measured three-seed static prior ranges, not a desired gain. |
| G8 | passed | 2026-11-13T21:11+0800 | 2026-11-13T21:12+0800 | `story-strength-audit.md` answers the six skeptical-reviewer questions, names CRPI as the strongest threat, specifies the discriminating experiments, states honest risks and the diagnostic fallback, and agrees with the feasibility contract. |
| validation | passed | 2026-11-13T21:13+0800 | 2026-11-13T21:14+0800 | `validate_guidance.py guidance.md --strict --packet ccfa-startup-packet` and `pipeline_state.py pipeline-state.json --complete` executed; exact outputs recorded in `validation-report.md`. |
| handoff | passed | 2026-11-13T21:14+0800 | 2026-11-13T21:15+0800 | `startup-decision.md` = `proceed`; `guidance.md` is the contract for `f-research-v1` P0. Direction appended to `auto-paper/generated-research-directions.md`. |

## Revisit Ledger

No stage has been revisited or superseded in this build. Rejected scenarios S1-S3 are recorded in `scenario-decision-log.md` as candidates screened before `CCFA-startup`; they are not gate revisits.

## Integrity note

Every `passed` row above is confirmed by the two validators named in the validation row; the structured ledger is authoritative. If a validator reports an error, this file and `pipeline-state.json` must be regenerated before any handoff claim is made. No experimental result is asserted anywhere in this guidance build.
