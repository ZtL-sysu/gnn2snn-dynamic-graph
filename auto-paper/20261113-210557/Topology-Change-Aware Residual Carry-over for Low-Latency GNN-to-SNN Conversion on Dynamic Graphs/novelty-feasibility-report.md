# Novelty And Feasibility Report

## Input

- User technique: lightweight GNN→SNN conversion (training-free weight/activation mapping, threshold balancing, differential or graded event coding, conversion-error bounds).
- User-provided application scenario: dynamic graphs as the broad direction; scenario narrowed here to continuous-time dynamic graph (CTDG) event streams with an explicit conversion-fidelity task.
- Hardware: Apple M1 / 8 cores / 16 GiB / MPS / 339 GB free; no CUDA; project-local Conda environment to be created at P2.
- Constraints: Neurocomputing target; local compute only; no neuromorphic energy measurement; user's `gnn2snn` archive is static-graph and paused; historical dynamic-graph SNN and sparse-execution routes are closed.

## Candidate Scenario Screening

| Scenario | Dataset access | Task validity | Theoretical fit | Novelty | Hardware | Baselines | Story | Decision |
|---|---|---|---|---|---|---|---|---|
| S1 new lightweight spiking dynamic-graph architecture | Zenodo direct | valid | medium | **FAIL** (SpikeNet / Dy-SIGN / Lite-SDGN / SGNNBench) | feasible | crowded | thin | Rejected at G4 |
| S2 spike-proxy sparse execution / energy Pareto | Zenodo direct | valid | **FAIL** (no neuromorphic hardware) | **FAIL** (predecessor 2.54/5 CLOSE) | infeasible | unavailable | weak | Rejected at G3/G8 |
| S3 dynamic-link-prediction robustness / sampler correction | Zenodo direct | valid | medium | **FAIL** (logQ law falsified locally, prior art covers it) | feasible | crowded | thin | Rejected at G4/G7 |
| **S4 topology-change-aware residual carry-over for ANN→SNN conversion on CTDG** | Zenodo direct, HTTP 200 verified | valid with frozen split | **strong** (cross-event error recursion + topology term) | **distinct with positioning** (CRPI/MPEF have no graph; SpikeNet is direct-trained) | feasible after explicit scaling | four classes, two direct-rerun conversion controls | mechanistic + bounded + cost result | **Selected** |

## Selected Scenario

- Scenario: convert a lightweight, conversion-friendly CTDG ANN teacher into a low-latency SNN and suppress the accumulation of conversion error along the event stream; the mechanism is a topology-change-gated residual membrane-potential carry-over with base/threshold recalibration, triggered only when a node's neighbor set changes materially.
- Reason for selection: it is the only candidate that passes all hard gates, uses directly public small data, avoids the two routes closed by the user's own prior audits, reuses the user's verified conversion machinery, and produces a mechanism-level claim (a bound and a falsifiable gate) rather than a benchmark-table delta.
- Main risk: CRPI (ICML 2026) already established cross-step error amplification and residual carry-over. If the topology-change gate is not demonstrably better than global carry-over, the paper is incremental.
- Fallback scenario: if the gate fails, the honest lower-tier story is a **measurement/diagnostic** paper: quantify how conversion error scales with `‖ΔA_k‖` and event-window length on public CTDG streams, with the bound as the contribution and no method-superiority claim. This fallback is recorded here, not used to soften the current contract.

## Dataset Access Audit

| Dataset | Source URL | License/terms | Direct public? | Friction | Decision |
|---|---|---|---|---|---|
| Wikipedia / MOOC / Enron | `https://zenodo.org/api/records/7213796/files/<name>.zip/content` | CC BY 4.0 | yes (HTTP 200, attachment) | none | accept |
| Reddit / LastFM | same pattern | CC BY 4.0 | yes | none; larger | optional |
| Four local frozen `.npz` | local copies of the above | CC BY 4.0 upstream | n/a (local) | none; `numpy.load` verified | accept as derived input |
| SuperPixel MNIST/CIFAR10 | user archive | no blanket license | n/a | teacher training infeasible | reject |
| TGB 2.0 large variants | public | varies | yes | exceeds memory/time | reject on G5 |

## Novelty Audit

| Paper | Year | Source | Method | Task/domain | Dataset | Overlap level | Decision |
|---|---:|---|---|---|---|---|---|
| CRPI, arXiv:2601.21778 | 2026 | ICML 2026 / arXiv | cross-step residual potential initialization | ANN→SNN conversion, RL continuous control | MuJoCo, DMC | **high on mechanism, low on setting** | Differentiate: no graph, no neighbor-set change, no `‖ΔA‖` term, no GNN teacher. Include as `must-rerun` adapted control. |
| Spiking DiTs MPEF | 2026 | ICML 2026 | membrane-potential error feedback across denoising steps | diffusion generation | ImageNet | medium on mechanism | Literature context; no graph. |
| SNNC-AP, arXiv:2205.10121 | 2022 | arXiv | layer-wise parameter calibration, second-order error propagation | image classification / detection | ImageNet, CIFAR, COCO | medium on calibration | Adapted control; ours is label-free, event-triggered. |
| CASC | 2024 | Information Sciences | consistent activation mapping, conversion bounds | image classification/detection | CIFAR | low (theory support) | Theory context. |
| SpikeNet | 2023 | AAAI | directly trained spiking dynamic graph model | dynamic graph | temporal graphs | low on method family, high on domain | Domain positioning; not a conversion comparator. |
| Dy-SIGN | 2024 | AAAI | spiking dynamic graph | dynamic graph | temporal graphs | same | Domain positioning. |
| `ZtL-sysu/gnn2snn` archive | 2026 | user public repo | DCGS/affine-base ANN→SNN conversion | **static** SuperPixel graphs | MNIST/CIFAR10 SuperPixel | **high on conversion machinery, zero on time axis** | Prior-range source and code reference; explicitly static, so its affine static-base cache is the assumption this work relaxes. |
| Local RiskSet-DyG predecessor | 2026 | local, unpublished | negative-sampling-robust CTDG scoring | CTDG link prediction | Wikipedia et al. | low (different claim) | Reusable data/protocol; its failed `−log q` law must not be reused. |

**Novelty conclusion**: no retrieved work combines (a) ANN→SNN conversion, (b) continuous-time dynamic graphs, (c) a topology-change term in the conversion-error recursion, and (d) an event-triggered recalibration whose cost is bounded by topology-change events. Confidence: **moderate**. Searches covered public web results and the local predecessor corpus; a structured Scopus/arXiv/IEEE sweep with DOI-level deduplication is mandatory at P12 and may downgrade the novelty claim.

## Theory Fit

- Domain bottleneck: in a CTDG, node state is a cross-event recursion. A per-window conversion error is not independent across events: it enters the next state, and the aggregation set `A_k` itself changes. Existing conversion analyses bound error along **layers** of a static network, not along **events** of an evolving graph.
- Method mechanism: derive `ε_k ≤ ρ ε_{k−1} + L_A ‖A_k − A_{k−1}‖ ‖s_{k−1}‖ + c/T + η_k`; carry the residual membrane potential forward for touched nodes, and recompute the static base and threshold only when the relative neighbor-set change exceeds `gamma`. This removes the `η_k` term for carry-over nodes and binds the recomputation cost to topology-change events.
- Expected advantage: lower end-of-window teacher disagreement at fixed `T`, with fewer recomputations than per-event full recalibration.
- Required adaptation: reimplement the differential coder independently; define a conversion-friendly teacher (ReLU/clip only, no attention softmax, no batch-norm at conversion time); freeze neighbor-set snapshots for reproducible `‖ΔA‖`.
- Failure mode: if the topology-change term is empirically negligible (gate ablation indistinguishable from global carry-over), the mechanism claim is falsified and the fallback diagnostic story applies.

## Feasibility

- Hardware fit: ≤100k-parameter teacher, ≤15 MB streams, MPS or CPU fallback; no CUDA dependency.
- Runtime estimate: ≤20 min/seed, ≤120 runs, ≤12 h total — **planning ceilings, not measured**. P2 prototype must confirm one seed end-to-end.
- Implementation complexity: moderate. Components are a small CTDG teacher, a differential/graded IF coder, an event-loop state machine, a topology-change tracker, and four ablation switches. SpikingJelly is optional; the coder can be plain PyTorch.
- Baseline availability: CRPI/SNNC-AP mechanisms are described in public papers and are cheap to reimplement; DCGS/QFCS/FTBC coders exist in the user's archive; EdgeBank/Base3 and DyGLib code exist locally. The strongest prediction-style baselines are literature-context only, with the reason recorded.
- Ablation availability: six planned ablations, each tied to one term of the bound or one design choice; see `theoretical-feasibility-audit.md` and `guidance.md`.
