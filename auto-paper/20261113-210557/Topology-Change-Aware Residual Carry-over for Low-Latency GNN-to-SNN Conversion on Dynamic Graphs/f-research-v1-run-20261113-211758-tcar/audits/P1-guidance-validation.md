# P1 Guidance Validation

## Contract extraction

| Field | Value |
|---|---|
| `topic` | Low-latency GNN→SNN conversion on continuous-time dynamic graphs |
| `target_venue` | Neurocomputing (Elsevier) |
| `main_claim` | Conversion error accumulates along the event axis with a topology-change term; topology-change-gated residual carry-over improves low-latency fidelity at an event-bound recomputation cost |
| `method` | TCAR: graded differential IF conversion, label-free percentile calibration, cross-event residual carry-over on touched nodes, topology-change-gated base/threshold recomputation |
| `datasets` | Wikipedia (primary), MOOC, Enron; Reddit/LastFM optional; Zenodo 10.5281/zenodo.7213796, CC BY 4.0 |
| `baselines` | B0 ANN oracle, B1 EdgeBank, B2 Base3, C0 hard-reset IF, C1 SNNC-AP-light, C2 DCGS coder, C3 QCFS/FTBC, C4 CRPI-style global carry-over, D1 directly trained spiking control |
| `primary_metric` | `agreement@K` at the end of a 10,000-event window (higher is better) |
| `secondary_metrics` | MRR/AP retention, logit MSE/KL, `epsilon_k`, `||delta A_k||`, graded events, recalibration rate, local PyTorch latency |
| `expected_minimum` | T=4 agreement >= 95.0%, MRR retention >= 95.0%, teacher beats B1/B2 on validation |
| `expected_strong` | T=4 agreement >= 98.5%, MRR retention >= 99.0%, TCAR decay <= 0.5 pp vs C4 >= 2.0 pp with paired bootstrap CI excluding 0, recalibration <= 20% of events, replicated on 3 streams |
| `strong_result_entry_gate` | P5: all required experiments done and strong target met before P6 writing |
| `must_run_experiments` | B0-B2, C0-C4, M0, A1-A6, D1, S1/S2 sweeps, R1-R3, K1-K3, per-event bound instrumentation |
| `must_have_ablations` | six, each tied to a term of the bound or a design choice |
| `figure_table_decision_rules` | evidence-driven; framework figure generated directly with GPT image generation after the paper is understood; no fixed count |
| `experiment_traceability` | `experiment-traceability.md` updated before and after each batch; config+SHA, seed, command, raw JSONL, completion/failure marker |
| `citation_requirements` | primary sources only; DOI/arXiv verification and dedup at P12/P14 |
| `local_artifact_policy` | all deliverables under this run root |
| `page_length_policy` | official Neurocomputing limits at P20; no invented default |
| `central_question` | how conversion error accumulates along a CTDG event stream when the aggregation operator changes |
| `intended_reader` | SNN conversion / spiking graph / temporal graph researchers |
| `domain_design_bridge` | static-base caching assumes a fixed graph → derive a topology-change term → gate recalibration on measured neighbor-set change |
| `planned_claim` | stated in guidance; distinct from `observed_finding` |
| `observed_finding` | **unresolved_until_evidence** |
| `open_assumptions` | A1-A7 in `theoretical-feasibility-audit.md`; measured `rho`, clipping rate, novelty sweep, official venue limits |

## Checks performed

- `guidance.md` re-validated against `f-research-v1/references/guidance-file-spec.md`: all nine required sections, six canonical numbered sections, explicit expected results with minimum/strong/failure, datasets, baselines, metrics, experiment schedule, stopping criteria, hardware budget, traceability rows, citation scope.
- `validate_guidance.py --strict --packet ../ccfa-startup-packet` → `Guidance structure is valid.` (EXIT=0). Re-executed at P1 from the run root context; the guidance and packet files were unchanged since the guidance phase (hashes still match `../validation-report.md`).
- `../ccfa-startup-packet/startup-decision.md` = `proceed`; a packet marked anything else would block the run.
- The packet's `feasibility-contract.json` contains three claims, each hash-bound to the seven startup artifacts.

## P1 gate

Story, outline, expected results, datasets, baselines, metrics, experiment schedule, and startup decision are explicit and consistent. **P1 pass.**

No observed finding is recorded at P1. Every number in the contract above is a **planned target**, not a measurement.
