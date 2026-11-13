# Research Guidance File

## Title / Topic

- Working title: Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs
- Short name: TCAR
- Target field: spiking neural networks, graph representation learning, continuous-time dynamic graphs (CTDG), ANN-to-SNN conversion
- Target journal tier: CAS Tier 2 / JCR Q1 in Computer Science, Artificial Intelligence; established subscription/hybrid non-OA journal
- Candidate venue: **Neurocomputing** (Elsevier, founded 1989; verified 2026-11-13 as CAS computer-science Tier 2, JCR AI Q1, non-OA by default). Official guide-for-authors limits will be re-checked at P20 before `submission-constraints.md` is frozen.
- Technique/method: training-free ANN/GNN-to-SNN conversion with graded differential event coding, label-free percentile calibration, cross-event residual membrane-potential carry-over, and topology-change-gated base/threshold recomputation
- Selected application scenario: low-latency conversion fidelity on public timestamped interaction streams (Wikipedia primary; MOOC and Enron replication; Reddit and LastFM optional robustness)
- Intended reader: researchers working on ANN-to-SNN conversion, spiking graph learning, or temporal graph inference who care about where conversion error comes from and what it costs to suppress it
- Central scientific question: how does ANN-to-SNN conversion error accumulate along a CTDG event stream when the neighbor-aggregation operator itself changes, and can an event-triggered mechanism suppress that accumulation at a cost bounded by topology-change events rather than by total events?

## Core Idea

Train one lightweight, conversion-friendly CTDG ANN teacher (ReLU/clip nonlinearities only, no softmax in the converted path, batch normalization folded before calibration, at most 100,000 parameters). Convert it to an SNN by replacing each ReLU layer with a soft-reset integrate-and-fire unit using graded/differential events and a label-free percentile calibration over training activations, with `T` micro-steps per event (T in {1,2,4,8}). Then address the fact that a converted state is not reset between events: for nodes touched by an event, carry the residual membrane potential into the next window; and recompute that node's static base, threshold, and shared residual prefix only when its relative neighbor-set change `delta_v(k)` exceeds `gamma`. Static periods reuse the cached base. The converted model is evaluated against the frozen teacher on the same event stream, so the claim is about conversion fidelity rather than leaderboard ranking.

### Mechanism-Level Rationale

- Domain bottleneck: conversion error theory was built for one static forward pass. In a CTDG the same node state that carries the error is the input to the next event, and the set of neighbors being aggregated changes. The user's own `ZtL-sysu/gnn2snn` archive caches a static base `Wh0+b` and a shared residual prefix per forward pass; that cache is exactly what an evolving topology invalidates.
- Why the chosen technique fits: the single-layer conversion identity `E^l_i = sum_j w_ij E^{l-1}_j + (V_i(T) - V_i(0))/T` decomposes error into propagated upstream error and an un-emitted residual. Lifting it to the event axis gives `epsilon_k <= rho*epsilon_{k-1} + L_A*||A_k - A_{k-1}||*||s_{k-1}|| + c/T + eta_k`, where the topology-change term is new and the residual term is directly controllable.
- What must be changed or adapted: define a reproducible `A_k` per event; freeze neighbor snapshots and query identities; restrict carry-over to touched nodes; gate base recomputation on `delta_v(k)`; reimplement the differential coder independently because the source archive grants no blanket license; use a small M1-friendly teacher instead of the archive's RTX-3060-scale SuperPixel teacher.
- Why this is more than applying method X to dataset Y: it introduces a term absent from the source theory, ties an event-bound cost model to that term, and makes both falsifiable by topology stratification, a frozen-topology control, and a matched-budget comparison against a CRPI-style global carry-over control.

## Paper Story

- Opening problem: a trained ANN encoder can be converted into an SNN without retraining, but the error guarantees assume a fixed graph and a single inference window. Real interaction streams are event-recursive and their neighbor sets change.
- Why existing work is insufficient: conversion analyses (SNNC-AP 2022, CASC 2024, BayesianSpikeFusion 2024) bound error along layers of a fixed network; CRPI (ICML 2026) and Spiking DiTs MPEF (ICML 2026) show cross-step error amplification and residual carry-over but have no graph and no changing aggregation operator; SpikeNet (AAAI 2023) and Dy-SIGN (AAAI 2024) are directly trained spiking dynamic-graph models, not conversions.
- Core insight: cross-event conversion error has a component proportional to the change in the aggregation operator, so suppressing it should be triggered by topology change rather than by every event.
- What evidence should convince the reader: a measured error bound that is not violated, a monotone dose-response between cumulative `||delta A||` and end-of-window disagreement, a shrinking advantage under frozen topology, and a win over global carry-over at equal or lower recomputation count with paired bootstrap confidence intervals excluding zero.
- Planned claim (not an observed finding): topology-change-gated residual carry-over reduces end-of-window teacher disagreement at small T while binding recomputation cost to topology-change events on public CTDG streams.
- Finding to assess after experiments: unresolved until evidence exists. `observed_finding` is updated only at P5A/P6 from accepted P5 artifacts; guidance expectations are never reported as findings.
- Main claim: conversion error on CTDG streams accumulates along the event axis with a topology-change term, and gating residual carry-over plus base recalibration on that term improves low-latency fidelity at bounded recomputation cost.
- Boundary of the claim: one lightweight teacher family, three public interaction streams, graded-event and recomputation counts plus local PyTorch latency as cost proxies, no neuromorphic hardware energy measurement, absolute MRR reported as context only.
- Skeptical-reviewer hook: "Is this just CRPI on a graph?" The three discriminating experiments above are the answer.
- Strongest competing paper: CRPI, arXiv:2601.21778, ICML 2026. It is implemented as a direct control rather than cited away.
- Expected contribution type: mechanism plus an empirically checked bound plus an event-bound cost trade-off, with a measurement/diagnostic fallback if the mechanism is falsified.

## Paper Outline

1. Introduction: motivate event-recursive conversion error, state the gap in static conversion theory and cross-step methods, list the three contributions (bound, mechanism, cost), and delimit the claim.
2. Related Work: ANN-to-SNN conversion and error analysis; cross-step residual and error-feedback methods; spiking and dynamic graph models; CTDG benchmarks and evaluation protocols.
3. Method: define the CTDG teacher, the conversion and calibration procedure, derive the event-axis recursion and the topology-change term, define `delta_v(k)` and the TCAR trigger, and state the cost model and all assumptions.
4. Experiments and Results: datasets and frozen splits, baseline-first setup, main fidelity and retention results at T in {1,2,4,8}, the three discriminating experiments, six ablations, T/gamma sweeps, three-stream replication, statistical checks, and efficiency measurements.
5. Discussion: interpret the bound against measured `epsilon_k` and `||delta A||`, state what the results do and do not establish, cover the non-blind test identifiers, the literature-context status of strong CTDG predictors, moderate novelty confidence, and the absence of neuromorphic energy measurement.
6. Conclusion: restate the mechanism and the evidence-backed scope, name one concrete next step for event-driven deployment, and stop. No research content follows this section.

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| Wikipedia | https://zenodo.org/api/records/7213796/files/wikipedia.zip/content | CC BY 4.0, DOI 10.5281/zenodo.7213796 | primary stream | 157,474 events; 1,253,310 B frozen npz | timestamped interaction events, frozen candidate catalog, 1024 validation / 4096 test queries | chronological 70/15/15, IDs hash-frozen at P2 | direct-public, HTTP 200 verified 2026-11-13 |
| MOOC | https://zenodo.org/api/records/7213796/files/mooc.zip/content | CC BY 4.0 | replication | 411,749 events; 2,821,369 B frozen npz | same schema, 97-node catalog | same | direct-public |
| Enron | https://zenodo.org/api/records/7213796/files/enron.zip/content | CC BY 4.0 | replication / exact enumeration | 808,719 B zip | same schema | same | direct-public, HEAD HTTP 200 verified |
| Reddit (optional) | https://zenodo.org/api/records/7213796/files/reddit.zip/content | CC BY 4.0 | optional robustness | 672,447 events; 7,266,991 B frozen npz | same schema | same | direct-public, budget-capped |
| LastFM (optional) | https://zenodo.org/api/records/7213796/files/lastfm.zip/content | CC BY 4.0 | optional robustness | 1,293,103 events; 10,938,846 B frozen npz | same schema | same | direct-public, budget-capped |

Source/access details, rejected datasets, and the licensing note are in `dataset-access-log.md`. Test identifiers were used in a predecessor local project; this is disclosed and absolute MRR is treated as context, not as the main claim.

### Baselines

- Simple baseline: EdgeBank (time-window and unlimited) and Base3 k=10, both available in the local DyGLib/Base3 copies and measured in seconds per evaluation by a predecessor project.
- Matched internal baseline: the identical frozen ANN teacher converted with plain rate-coded IF neurons, hard reset, no calibration (C0); plus the unconverted ANN teacher as an oracle upper bound (B0).
- Domain-standard baseline to rerun/adapt: DCGS `MTH_diff` graded differential coder (C2) and QCFS/FTBC clipped conversion (C3), reimplemented locally from the user's archive procedures.
- Strong recent baseline to rerun/adapt: CRPI-style global cross-step residual carry-over (C4, adapted from arXiv:2601.21778) and SNNC-AP light parameter calibration (C1, arXiv:2205.10121). Both are gradient-free and fit the local budget. C4 is the single strongest discriminator.
- Strong recent baseline for literature context only: TGN, GraphMixer, DyGFormer, CAWN, TAMI (NeurIPS 2025), HyperEvent (arXiv:2507.11836), TPNet, SpikeNet (AAAI 2023), Dy-SIGN (AAAI 2024). A predecessor TGN/Wikipedia/seed7 run timed out at 28,800 s with no test metrics, so these are not claimed as direct reruns. If the P2 prototype shows GraphMixer completes within 30 min per seed on a Wikipedia subset, it is promoted to adaptation-attempt via a recorded contract update.
- Technique-family baseline: hard-reset IF, clipped ReLU conversion, differential coding, global carry-over, and a directly trained spiking encoder of matched size (D1) as a parallel control, not an oracle.
- Upper-bound or oracle-style comparison: the frozen ANN teacher itself (B0), used as the reference for all retention and agreement numbers.
- Strongest expected comparison: TCAR versus C4 (CRPI-style global carry-over) at equal or lower recomputation count, with paired bootstrap intervals.

### Proposed Method Variants

- Main method (M0): TCAR with residual carry-over on touched nodes and topology-change-gated base/threshold recomputation at threshold `gamma`.
- Variant A (A1): no topology gate, recompute at every event (upper-cost control).
- Variant B (A2): no residual carry-over, hard reset at every window.
- Variant C (A3): frozen static base with no recalibration at all.
- Variant D (A4): static-graph control with neighbor sets frozen for the same event sequence.
- Additional variants: A5 `||delta A||` quartile stratification, A6 `gamma` and T sweeps.
- Implementation notes: plain PyTorch is sufficient; no SpikingJelly dependency is required. The differential coder is reimplemented rather than copied because `ZtL-sysu/gnn2snn/RIGHTS.md` grants no blanket license. Batch normalization is folded before calibration; threshold and gauge must be consistent, following the archive's regression-check ideas. MPS is preferred where operators are supported, otherwise CPU fallback is recorded per operator.

### Metrics

- Primary metric: end-of-window teacher-to-SNN decision agreement `agreement@K` over the last segment of a 10,000-event window (higher is better), computed against the frozen ANN teacher's argmax over the candidate catalog.
- Secondary metrics: MRR and AP retention relative to the ANN teacher (higher is better), logit MSE and teacher-to-SNN KL (lower is better), per-event state error norm `epsilon_k`, per-event topology change `||A_k - A_{k-1}||`, relative neighbor-set change `delta_v(k)`, and bound-violation rate.
- Efficiency metrics: graded-event count per event, base/threshold recalibration count and trigger rate, parameter count, and local PyTorch wall-clock milliseconds per event reported separately for CPU and MPS. No hardware energy claim is made.
- Statistical test / confidence reporting: 5 seeds with every per-seed value retained; paired bootstrap 95% confidence intervals over queries for each main comparison; Benjamini-Hochberg correction across the ablation family; mean plus sample SD with explicit N; metric direction recorded for every row.

### Required Ablations

- Ablation 1 (A1): remove the topology-change gate and recompute every event, isolating the cost policy.
- Ablation 2 (A2): remove residual carry-over, isolating the `eta_k` term.
- Ablation 3 (A3): freeze the static base with no recalibration, isolating the `||delta A||` term.
- Ablation 4 (A4): freeze the topology entirely, isolating topology change from temporal depth.
- Ablation 5 (A5): stratify by `||delta A||` quartile, testing the dose-response predicted by the bound.
- Ablation 6 (A6): sweep T in {1,2,4,8} and `gamma` over at most six values, testing the latency/cost frontier.
- Robustness or subgroup analysis: window length K in {1k, 5k, 10k}; node-activity quartiles; three-stream replication; CRPI-style matched-budget control.
- Error analysis: record where and when the bound is violated, clipping-rate outliers, and failure cases of the calibration; preserve negative and null findings.

### Complete must-run experiment list

B0 ANN teacher oracle; B1 EdgeBank; B2 Base3; C0 hard-reset IF; C1 SNNC-AP-light; C2 DCGS coder; C3 QCFS/FTBC; C4 CRPI-style global carry-over; M0 TCAR full; A1-A6 six ablations; D1 directly trained spiking control; S1 T sweep; S2 gamma sweep; R1-R3 three-stream replication; K1-K3 window-length robustness; bound-check instrumentation on every event. Every row writes config hash, seed, command, hardware profile, raw metrics JSON and JSONL, and an explicit completion or failure marker before the next batch starts.

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Apple M1, 8 cores, 16 GiB unified memory, MPS available, no CUDA, 339 GB free; project-specific Conda environment created at P2 using `/Users/xhf/miniconda3/bin/python`; no global Conda configuration is changed.
- Optional remote fallback, only if authorized: none. Remote compute is not authorized and is not used.
- GPU/CPU: MPS preferred for supported operators, CPU fallback recorded per operator.
- RAM: 16 GiB ceiling; disk: 339 GB free; maximum dataset size 15 MB per frozen stream.
- Max runtime per run: 20 minutes wall clock for one seed; 30 minutes for the one-off P2 prototype.
- Max total runs: 120 seed-level runs including failures; maximum total wall clock 12 hours; maximum model size 100,000 parameters.
- Frozen train/validation/test identifiers and validation-only selection policy: SHA-256 of every npz and of the 1024 validation / 4096 test query arrays written to `inputs/frozen-identities.json` at P2. Validation queries alone select T, gamma, calibration percentile, and early stopping. Test queries are read once at P5 after the contract is frozen.
- Full search/trial ledger and held-out test isolation: at most 24 (T, gamma) combinations, every trial logged with config hash and outcome; a query used for selection is never described as unseen.
- CCFA packet path and feasibility-contract.json: `ccfa-startup-packet/` in this folder; its `feasibility-contract.json` hash-binds the seven startup artifacts.
- Resource budget exhaustion and next-candidate decision rule: if the ceiling is reached, reduce optional streams (Reddit/LastFM, then Enron) but keep the six ablations and 5 seeds on the primary stream; if that still fails, return to G5 with a versioned scaled plan.
- Scaling fallback: smaller hidden width, fewer optional streams, frozen teacher with fewer epochs, and fewer but stronger ablations. Scaling must not remove the mechanism-isolating experiments.
- Stopping criteria: all required rows done, strong-result lock satisfied, budget not exceeded. Stop and return to guidance design if the P2 prototype fails, measured `rho` is unbounded with no repair, clipping rate on validation exceeds 1 percent with no percentile repair, the ANN teacher fails to beat B1/B2 on validation, CRPI-style control cannot be implemented, or bound (1) is empirically violated.

## Expected Results

- Minimum acceptable result: at T=4 on Wikipedia, `agreement@K` at least 95.0 percent and MRR retention at least 95.0 percent, with the ANN teacher beating EdgeBank and Base3 on validation; all five seeds retained.
- Strong result: (a) T=4 `agreement@K` at least 98.5 percent and MRR retention at least 99.0 percent on the primary stream; (b) over a 10,000-event window TCAR agreement decay at most 0.5 percentage points while C4 global carry-over decays at least 2.0 percentage points, with paired bootstrap 95 percent confidence intervals excluding zero; (c) recalibration triggered on at most 20 percent of events with no accuracy loss versus A1 at matched accuracy; (d) the direction of (a)-(c) replicated on MOOC and Enron. These targets are calibrated against measured three-seed static-graph prior ranges from the user's own archive (T=4 teacher agreement 99.28-99.98 percent, GatedGCN T4 99.55 plus or minus 0.16 percent) plus a non-inferiority allowance for the harder dynamic setting.
- Failure signal: T=8 `agreement@K` below 95 percent; TCAR indistinguishable from C4 at matched recomputation budget with the confidence interval containing zero; no monotone dose-response between cumulative `||delta A||` and disagreement; bound (1) empirically violated; or the ANN teacher failing the B1/B2 gate. A converted SNN that merely runs, or a small absolute-MRR gain on one stream, is a failure signal rather than a strong result.
- What to do if minimum is not reached: debug data alignment, gauge/threshold consistency, calibration percentile, and state-update implementation; strengthen the baselines; tune within the 24-combination budget; add ablations; then rerun. Do not write the paper until P5 passes.
- Claim adjustment rule if expectations fail: enter `f-research-v1`'s authorized correction loop with a versioned replacement contract recorded in the run root, reopening the earliest affected stage. The pre-declared lower-tier story is a measurement/diagnostic paper on conversion-error accumulation versus event-window length and cumulative topology change. Targets are never lowered after results are seen, and no result is fabricated.

## Figure/Table Decision Rules

Select the final visual set only after evidence stabilizes at P5/P5A; no fixed artifact count and no per-subsection quota applies.

- Required first figure type: one overall framework/architecture figure generated directly with the GPT image-generation capability after the full paper is understood, following `f-research-v1/references/framework-figure-style.md`; it shows only verified components (event stream, ANN teacher, converted SNN state, topology-change tracker, gated recalibration) and allowed labels. It is not routed through Nature skills.
- Required experiment visualizations if supported by data: an `agreement@K` versus event-window-length curve with confidence bands; a disagreement-versus-cumulative-`||delta A||` dose-response panel; a T-sweep latency/fidelity frontier; a recomputation-rate versus accuracy Pareto plot; and a topology-quartile stratification panel. Each is produced only if the underlying rows exist in `results/`.
- Required result tables if supported by data: one baseline/conversion-control comparison table with per-seed values and confidence intervals; one six-ablation table; one three-stream replication table; one cost table with graded events, recalibration count, parameters, and local latency. Every cell must trace to a raw `metrics.json` or `metrics.csv` row.
- Placement rule: each visual answers a scientific question, is cited and interpreted near its first discussion, and does not drift far from that text. Captions state measured quantities and units only.
- No visual may contain a target value presented as a measurement, and no figure may imply a hardware energy comparison.

## Traceability Checklist

| Guidance requirement | Required artifact | Minimum success check | Strong success check | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|
| Directly public datasets | `dataset-access-log.md`, frozen identities JSON | HTTP 200 and license recorded for all used streams | all three replication streams verified and hashed | dataset/split table | yes |
| Baseline-first execution | `results/p3_*` raw rows | B0/B1/B2/C0 exist before M0 | all four plus C1-C4 with per-seed values | baseline comparison table | yes |
| Main fidelity claim | `results/p4_*` raw rows | minimum target met on primary stream | strong target met with bootstrap CI excluding zero | agreement curve and baseline table | yes |
| Bound and topology term | `results/bound-check/*` | `epsilon_k`, `||delta A||`, `delta_v(k)` logged per event | bound not violated and monotone dose-response | dose-response panel, quartile panel | yes |
| Mechanism isolation | `results/ablations/*` | all six ablation rows done | each ablation isolates its named term with BH correction | six-ablation table | yes |
| Cost claim | `results/cost/*` | recalibration rate measured at most 50 percent | at most 20 percent with no accuracy loss versus A1 | cost Pareto plot and cost table | yes |
| Replication | `results/R1-R3/*` | primary plus one replication stream | three streams with consistent direction | replication table | yes |
| Statistical checks | `results/statistics/*` | 5 seeds retained, CI computed | BH-corrected CIs exclude zero on all main comparisons | uncertainty bands | yes |
| Citation integrity | `reference-dedup-audit.md` | all cited DOIs/arXiv ids checked | no duplicates, no metadata errors, moderate novelty resolved | none | no (audit artifact) |
| Guidance coverage | `paper-guidance-audit.md` | every promised experiment and section covered | no unresolved item | none | no (audit artifact) |

## Citation Scope

- Topic clusters: ANN-to-SNN conversion theory and calibration; cross-step error amplification and residual membrane potential; spiking and dynamic graph neural networks; continuous-time dynamic link prediction benchmarks and evaluation; temporal-graph survey and taxonomy; neuromorphic coding and graded/differential event coding.
- Must-cite works (identity to be verified at P12/P14): Maass 1997 (Networks of Spiking Neurons, Neural Networks 10(9)); Rueckauer et al. 2017 (Frontiers in Neuroscience 11:682); Diehl et al. 2015 weight normalization; SNNC-AP arXiv:2205.10121; CASC Information Sciences 2024 (S0020025524007369); BayesianSpikeFusion Frontiers 2024; CRPI arXiv:2601.21778 (ICML 2026); Spiking DiTs MPEF ICML 2026; SpikeNet AAAI 2023 DOI 10.1609/aaai.v37i7.26034; Dy-SIGN AAAI 2024 DOI 10.1609/aaai.v38i15.29587; DyGLib / Towards Better Evaluation for Dynamic Link Prediction (Zenodo 10.5281/zenodo.7213796); TGN ICLR 2020; GraphMixer 2023; DyGFormer 2023; TAMI NeurIPS 2025; HyperEvent arXiv:2507.11836; dynamic GNN survey DOI 10.1007/s11704-024-3853-2; SpikingJelly Science Advances 2023.
- Venue/domain boundaries: favour official proceedings, publisher pages, arXiv, TGB leaderboard, and primary dataset records. Secondary blog/aggregator pages are used only for discovery and are replaced by primary records before the bibliography is frozen. No invented venue, DOI, author list, or acceptance status.
- Citation recency expectations: the conversion-error and cross-step clusters must include 2024-2026 work; the CTDG baseline cluster must include 2023-2025 work; foundational items are retained where they establish definitions. No fixed bibliography count is imposed and no recency quota is filled with padding.
- Known duplicate/preprint risks: CRPI arXiv:2601.21778 has an ICML 2026 PMLR version; SNNC-AP arXiv:2205.10121 may have a published version; HyperEvent arXiv:2507.11836 has at least a v2; several CTDG methods have both DyGLib implementations and TGB leaderboard entries. P14 resolves these by DOI, arXiv id, normalized title, and venue version in `reference-dedup-audit.md`.
- The user's `ZtL-sysu/gnn2snn` archive is cited as a public code/prior-range reference only; it grants no blanket license, and the manuscript does not claim its historical draft as a publication.

## Constraints and Preferences

- Preferred writing language: English, formal journal register. No workflow logs, delivery notes, artifact checklists, citation-process narration, or "how we worked" text in the manuscript body.
- Preferred template or venue style: Neurocomputing (Elsevier) article structure with exactly the six numbered main sections listed in Paper Outline; no alternative top-level structure, no appendices, no reproducibility checklists added to the paper, and no research content after the conclusion.
- Page policy: no invented length target. With no explicit author requirement, assess completeness and proportion against the evidence; the official guide-for-authors limits are recorded at P20 in `submission-constraints.md` and applied as the strictest currently authoritative constraint. Public secondary pages suggest 10+ pages and 25+ references, but these are treated as unverified until the official page is checked.
- User-specific constraints: local Conda execution with `/Users/xhf/miniconda3/bin/python`; local compute only; distinguish measured from inferred at every step; never write tool/process mechanics into the paper; scientific revisions must name a precise location and replacement text; no energy or 5x claims; no fabricated datasets, citations, or results.
- Local artifact policy: every protocol, trace, log, result table, figure source, TeX source, PDF, audit file, manifest, and delivery bundle lives in a single `f-research-v1-run-*` run root inside this guidance file's directory. Nothing used for a claim is left outside it.
- Protected scope: the six-section structure, all verified numbers and equations, citation keys, terminology, and formal register. Stage ledgers, lock verdicts, reviewer dialogue, debug chronology, and production notes stay outside drafting context.
- Data/code/declaration statements are conditional submission elements, routed according to the official journal instructions rather than inserted by default. Final source, compiled PDF, bibliography, figures, and source archive must all represent the same accepted revision.

## External audit references

- `ccfa-startup-packet/` in this folder: `startup-stage-plan.md`, `idea-cards.md`, `prior-art-opportunity-map.md`, `idea-red-team-review.md`, `claim-evidence-matrix.md`, `strong-result-feasibility-contract.md`, `startup-decision.md`, `feasibility-contract.json`.
- `hardware-profile.md`, `dataset-access-log.md`, `scenario-decision-log.md`, `literature-baseline-matrix.md`, `novelty-feasibility-report.md`, `theoretical-feasibility-audit.md`, `story-strength-audit.md`, `evaluation-protocol.md` in this folder.
- `guidance-pipeline-state.md` and `pipeline-state.json` in this folder; `goal-ledger.md` and `collaboration/` at repository root.
- Historical material indexed in `collaboration/PROJECT.md` and `docs/prior-*.md`; those files are evidence of prior work, not results of this project.
