# Research Guidance File

> **Contract version v4** (2026-11-14, user directive: deepen the research by learning from the last two years of top-venue work). This file supersedes `guidance-v3.md` for experiment depth, theory content, efficiency transparency and manuscript requirements. All binding `minimum`, `expected_strong` and `failure` targets from v1/v2/v3 are retained verbatim, including the C16 narrowed claim and its recorded `d_replication: false` verdict. v1, v2, v3 and their hash-bound packets are preserved as evidence. Rationale and the full top-venue study are at `guidance-v4-amendment.md` and `docs/top-venue-study/` (reports 00–04, `gap-analysis.md` v1.0, `citation-verification-log.md`).

## Title / Topic

Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs, contract v4: a top-venue-depth revision adding a ten-seed pre-registered replication, a three-theorem theory package with violation-rate validation, a full efficiency and statistics transparency package, and an MPEF-style multi-threshold conversion control.

Target field: spiking neural networks meet continuous-time dynamic graphs. Target journal tier: Q2-or-better journal, locked to Neurocomputing (Elsevier, CAS Q2). Contribution claim: a mechanism-level account of how ANN-to-SNN conversion error accumulates along a CTDG event stream when the normalised aggregation operator changes, with a gated re-anchoring mechanism (TCAR), a formal error bound with an explicit topology term, and a pre-registered ten-seed evidence package.

## Core Idea

### Mechanism-Level Rationale

The v3 mechanism is unchanged and remains the core: at event k a normalised bipartite adjacency A_k(u,c)=1/sqrt(d_k(u)d_k(c)) is built from the interaction history, an L-layer residual GCN teacher propagates over the sampled neighbour set, and the teacher is converted by an independent reimplementation of the user's `gnn2snn` DCGS family: signed eight-level differential coding with telescoping decode, zero-latch, bias-once injection, 512-bin q=0.999 label-free two-pass histogram calibration, threshold iteration, and affine static-base caching. Because A_k changes, the cached affine base acquires a cross-snapshot increment R(A_k-A_{k-1})H_{k-1}W; TCAR gates base re-anchoring and conservative threshold recalibration on delta_v(k) > gamma or measured ||Delta A_k|| > tau, leaving the residual prefix intact.

The v4 deepening adds four mechanism-level upgrades, each traced to a named reviewer objection in the top-venue study.

- **T1 (local error identity)**: the DCGS differential coder admits a per-event error identity in which the discarded term eta_k is written explicitly as a function of the differential spike sequence; under the bounded-range ladder the identity shows eta_k is bounded and, at calibration coverage, near-orthogonal to the transmitted signal (verified exactly on a single-site toy, experiment V-6).
- **T2 (network bound with topology term)**: applying a spectral-norm recursion over the L residual GCN layers (template: ISC, CVPR 2025) gives a per-event logits-error bound in which the product L_A times ||Delta A_k|| times ||s_{k-1}|| appears as an independent topology term; the residual form W-tilde = I + A-hat_k W makes the spectral condition explicit. No 2024–26 top-venue conversion bound contains a graph-operator-change term.
- **T3 (steady-state bound and the carry-over trade)**: solving the event-axis recursion under rho < 1 gives epsilon_oo <= (L_A E[||Delta A||] E[||s||] + c/T + eta-bar)/(1-rho); residual carry-over lowers epsilon_0 at a rho cost, which turns the v3 design choice into a theorem-level trade with a falsifiable signature (experiment V-4).
- **C5-MT (multi-threshold control)**: an MPEF-style multi-threshold IF neuron (n = 4 levels) with inter-event membrane error feedback, adapted to graph layers on the same calibrated teacher, closes the strongest same-family mechanism gap identified by the study.

### Application Scenario and Feasibility

Selected application scenario: low-latency conversion fidelity on public timestamped interaction streams (Wikipedia primary; MOOC, Enron, Reddit, LastFM replication), unchanged from v3. Central scientific question: how does ANN-to-SNN conversion error accumulate along a CTDG event stream when the normalised neighbour-aggregation operator A_k genuinely changes, and can the static-base re-anchoring that this change forces be gated so that conversion fidelity is preserved at a cost bounded by topology-change events?

The single-layer conversion identity E^l_i = sum_j w_ij E^{l-1}_j + (V_i(T) - V_i(0))/T decomposes error into propagated upstream error and an un-emitted residual; for a GNN layer the per-snapshot identity B-hat - B = R A_k ((H-hat - H) W) holds, and caching A_{k-1} produces exactly the increment R(A_k - A_{k-1})H_{k-1}W, yielding epsilon_k <= rho epsilon_{k-1} + L_A ||Delta A_k|| times ||s_{k-1}|| + c/T + eta_k. The DCGS differential coder controls c/T and eta_k; the gate controls the topology term.

What must be changed or adapted for v4: extend the seed grid to 10 (41–50) with the decision rule frozen before inspection; instrument per-layer and per-window firing rates, op counts and latency with declared measurement protocol; implement the C5-MT decode path; add synthetic edge perturbation arms (V-3) and residual-branch scaling arms (V-4); add downstream-validity, inductive-stratification, drift-slice and sparsity-stratification analyses over the same traces. All adaptations stay inside the v3 method family and the recorded resource envelope.

## Paper Story

- Opening problem: a trained ANN encoder can be converted into an SNN without retraining, but the error guarantees assume a fixed graph and a single inference window; real interaction streams are event-recursive and their neighbour sets change. v4 sharpens the opening with the survey's debunking pattern: the strongest recent conversion theory presumes a stationary operator, while the strongest dynamic-graph results presume continuous ANN execution, so the intersection is unstudied.
- Gap: conversion error theory (2024–26) covers feedforward, attention and closed-loop control settings but not an unbounded event stream with a changing aggregation operator; dynamic-graph SNNs are directly trained architectures, not converted ones; and the evaluation conventions of both communities (op-count energy formulas, effect sizes, pre-registered statistics) have not been jointly applied to conversion fidelity.
- Insight: the operator change contributes an additive topology term to the event-axis error recursion, and the residual membrane potential is a free information carrier across events; gating the expensive correction on the measured topology change and carrying the residual prefix elsewhere suppresses the two dominant error sources at bounded cost.
- Planned claim (not an observed finding): topology-change-gated residual carry-over reduces end-of-window teacher disagreement at small T while binding recomputation cost to topology-change events on public CTDG streams, now with a formal bound, a violation-rate validation, a ten-seed pre-registered replication, and a full transparency package.
- Boundary of the claim: one lightweight teacher family, five public interaction streams, op-count energy proxies with cited constants (not hardware measurement), conversion fidelity rather than predictive leaderboard ranking.

Why a skeptical top-venue reviewer cares, per the study: the topology term plus rho condition are whitespace in the surveyed 2024–26 literature; the violation-rate experiment is an unoccupied differentiator; the ten-seed pre-registered resolution of a disclosed null result is methodologically distinctive; and the transparency package (energy formula, stratified firing rates, effect sizes) matches the SNN community's current checklist.

## Paper Outline

1. Introduction: debunking-flavoured opening (stationary-operator conversion theory meets continuous-execution dynamic graphs; neither side covers the intersection); the event-axis error question; contributions (genuine dynamic-graph GNN; independent DCGS reimplementation; TCAR; three-theorem bound with topology term; ten-seed pre-registered evidence; MPEF-style control; transparency package); explicit response to the CRAFT/TGB-Seq anti-memory narrative and a positioning table (direct-trained spiking GNN / static-graph conversion / dynamic-graph ANN / this work) over (operator-change-aware, no retraining, per-event bound, event-driven cost).
2. Related Work: rate-based conversion; low-latency conversion and error decomposition; cross-step error amplification (CRPI) and membrane-potential error feedback (MPEF); differential coding theory (DCGS); spectral-norm conversion bounds (ISC); spiking and dynamic graph networks (SpikeNet, Dy-SIGN, DRSGNN, SiGNN, Delay-DSGN, ChronoSpike); dynamic-graph learning and evaluation (TGN lineage, TGB/TGB-Seq, negative-sampling protocol); SNN energy methodology (op-count conventions, capacity-matching caveat).
3. Method: dynamic graph construction and A_k; residual GNN teacher; DCGS signed multi-level differential coding; label-free calibration; affine static base and cross-snapshot increment; TCAR gate; theorems T1–T3 with enumerated assumptions and proof sketches; complexity and the op-count energy formula with cited constants.
4. Experiments and Results: protocol; baselines and the new C5-MT control; main comparison with per-seed scatter and effect sizes; timestep curve; spike activity with three-level firing-rate stratification, energy table, TCAR overhead; error decomposition; ablations with the component-ladder figure; robustness sweeps and time-sliced drift; bound verification with violation rate, topology dose-response and rho scaling; carry-over alpha trade-off; downstream-validity and inductive stratification; sparsity stratification; five-stream ten-seed replication with the locked decision rule and the LastFM verdict; latency-fidelity Pareto with named operating points.
5. Discussion: bounded claim restated; negative results (A5 stream dependence, non-monotone relative reduction, the recorded LastFM verdict at the pre-registered power); what the theory does and does not assume; deployment-facing reading of the energy proxies; threats to validity.
6. Conclusion: mechanism, evidence and boundary; extensions (learned message weights, estimated state Lipschitz constant, event-driven backend).

## Experiment Plan

### Datasets

Unchanged from v3, all directly public. Source/access: Zenodo record 10.5281/zenodo.7213796, CC BY 4.0, direct file URLs, HTTP 200 verified 2026-11-13. Direct access URL for the primary stream: https://zenodo.org/api/records/7213796/files/wikipedia.zip/content. Five streams: Wikipedia (157,474 events; primary), MOOC (411,749), Enron (125,235, derived from ml_enron.csv in the same record), Reddit (672,447), LastFM (1,293,103; replication and the pre-registered boundary case). Frozen SHA-256 identities recorded at P2 of the v4 run. The study's large-graph suggestion (DBLP/Tmall/Patent) is rejected in gap-analysis R1 for the recorded hardware envelope; downstream-validity experiment substitutes for leaderboard breadth.

### Baselines

Retained from v3: B0 ANN teacher oracle; B1 EdgeBank; B2 Base3; C0 hard-reset IF; C1 DCGS without carry-over; C2 CRPI-style global carry-over (strongest discriminating control); C3 QCFS-style clipped uniform quantisation; C4 offset-spike calibration; D1 directly trained spiking quantiser surrogate; A1 re-anchor-every-event oracle; A2 no carry-over; A3 gate without threshold recalibration; A5 no aggregation. New in v4: C5-MT MPEF-style multi-threshold neuron with inter-event error feedback (n = 4 levels, same calibration pipeline), with the pre-authorized demotion fallback recorded in the feasibility contract.

### Proposed Method Variants

M0 TCAR full (v3, unchanged). New analysis variants: M0 with carry-over coefficient alpha in {0, 0.25, 0.5, 0.75, 1.0} (C-8); residual branch scaling to vary rho (V-4); synthetic edge insertion/deletion at five ratios for the topology-slope arm (V-3).

### Metrics

Primary metric: mean per-event teacher-to-SNN state error epsilon_k (lower is better) with the strict-dominance condition over conversion controls; agreement@K retained as the deployment-facing secondary metric (saturation disclosed). Secondary metrics: MRR retention, logit MSE, measured ||Delta A_k||, graded events per event, firing rate (global, per-layer, per-time-window), SynOps proxy and the full op-count energy proxy with cited constants, clipping/quantisation/residual decomposition, recalibration trigger rate, TCAR overhead percentage, parameter count, local wall-clock latency with declared protocol. New statistical metrics: paired Cohen's d with CI, probability of improvement, violation rate and tightness ratio, topology-term slope with CI, time-sliced drift summary.

### Required Ablations

Retained: A1 cost-policy isolation; A2 eta_k isolation; A3 topology-term isolation; A5 operator falsification; depth L in {1,2,3}; aggregation mean/max/gated; calibration percentile; T in {1,2,4,8,16}. New: C5-MT as the family-completeness control; alpha sweep as the carry-over trade; residual scaling as the rho-condition signature; negative-type and unseen-node stratifications as protocol stratifications rather than ablations.

### Complete must-run experiment list

Batch 1 (main matrix): 5 streams x 10 seeds (41–50) x 12 methods (B0 context row, C0–C5-MT, D1, M0, A1, A2, A3, A5 evaluation arms as applicable) = 60 runs, with the seed-46 smoke and v3-reproduction tolerance check as a binding precondition. Batch 2 (theory validation): V-1 violation rate and tightness on all 5 streams; V-2 T dose-response; V-3 synthetic edge-ratio sweep (5 arms); V-4 residual scaling (5 arms); V-5 carry-over versus reset contrast; V-6 single-site identity toy. Batch 3 (transparency and stratification): energy table derivation; three-level firing-rate stratification; TCAR overhead; Cohen's d and probability of improvement on all headline rows; C-6 downstream-validity strata; C-7 inductive strata; C-8 alpha trade-off curve; C-9 five-level robustness sweeps and ten-slice drift; C-10 sparsity-by-topology strata. Every row writes config hash, seed, command, hardware profile, raw JSON and JSONL, and an explicit completion or failure marker before the next batch starts.

### Runtime / Hardware Budget

Local machine and environment: Apple M1, 8 cores, 16 GiB, MPS available, no CUDA; `/Users/xhf/miniconda3/bin/python`; no remote compute. Measured v3 timing (90 minutes for 25 runs plus sweeps) and the 2026-11-14 smoke (147 s for one stream-seed at window 2000; 16 s per teacher train) bound the v4 campaign: main matrix at most 3.5 h; theory validation 1.5 h; transparency and stratification 0.5 h; C5-MT implementation and smoke 1.0 h; total additional runtime at most 6.5 h within the 12 h envelope. RAM ceiling 16 GiB; maximum stream size 15 MB; maximum model 100,000 parameters; total runs at most 240 including failures. Search budget: at most 24 (T, gamma) combinations, ledger retained; the v4 increments add no new test-set search. Frozen train/validation/test identities and validation-only selection are carried verbatim from v3.

Stopping criteria: all required rows done, strong-result locks satisfied, budget not exceeded. Stop-and-return conditions retained from v3 (prototype failure, unbounded rho with no repair, validation clipping above 1 percent, teacher non-vacuity failure, C2 infeasibility, bound empirically violated) plus v4 additions: seed-46 smoke outside tolerance returns to P2; V-6 falsifying T1 reopens the theory mechanism; C5-MT exceeding its implementation budget triggers the recorded demotion.

## Expected Results

- Minimum acceptable result: the v3 minimum is retained verbatim (T=4 agreement at least 95.0 percent and MRR retention at least 95.0 percent on Wikipedia with a non-vacuous teacher), now required on all ten seeds; plus the v4 floor that every transparency artifact (energy table, stratified firing rates, effect sizes, per-seed scatter) exists with every cell traceable to raw rows.
- Strong result: (a) v3 strong retained verbatim (agreement at least 98.5 percent, retention at least 99.0 percent, strict dominance of M0 over every conversion control on each stream); (b) the locked C-1 decision rule on ten seeds, recorded as `d_replication_10seed` true or false with the rule executed exactly once; (c) V-1 violation rate at most 5 percent with constants estimated on validation only, positive topology slope with CI excluding zero, and V-4 scaling consistent with 1/(1-rho); (d) TCAR overhead at most 2 percent and every headline row carrying Cohen's d and probability of improvement; (e) C5-MT on the full grid with M0 strictly lowest among conversion controls and the per-stream margin reported; (f) the direction of (a)–(e) replicated across MOOC, Enron, Reddit with the LastFM verdict recorded by the locked rule rather than renegotiated.
- Failure signal: retained verbatim from v3 (T=8 agreement below 95 percent; TCAR indistinguishable from C4 at matched budget with CI covering zero; no dose-response; bound empirically violated; teacher failing the B1/B2 gate), plus v4 signals: violation rate above 20 percent; C5-MT strictly lower than M0 on at least three streams; overhead above 5 percent; the C-1 machinery not executable as written. A converted SNN that merely runs remains a failure signal.
- What to do if minimum is not reached: debug data alignment, calibration, and the new instrumentation first; strengthen baselines; tune within the 24-combination budget; then rerun. Do not write the paper until P5 passes. V-6 failure removes T1 and reopens the theory mechanism rather than weakening the statement.
- Claim adjustment rule: unchanged from v3 — versioned replacement contract inside the authorized correction loop, reopening the earliest affected stage; targets are never lowered after results are seen; the pre-declared diagnostic fallback story is retained.

## Figure/Table Decision Rules

Select the final visual set only after evidence stabilizes at P5/P5A; no fixed artifact count and no per-subsection quota applies. Required first figure type: the overall framework figure (v3 fallback: local vector schematic, upgraded only if the user authorises image-generation credits) showing event stream, ANN teacher, converted SNN state, topology-change tracker and gated recalibration.

Visuals required if supported by data, beyond v3's set: a component-ladder figure of per-event epsilon_k as each TCAR component is added (MPEF-style); the alpha trade-off curve with the decorrelation-versus-overcorrelation knee; measured epsilon_k versus bound RHS with the violation-rate annotation; three-level firing-rate stratification panels; robustness degradation curves over five perturbation levels; the ten-slice drift curve; downstream-validity dose-response; per-seed scatter on headline rows. Required tables beyond v3's set: the op-count energy table with cited constants; the Cohen's d and probability-of-improvement columns in the main and replication tables; the C5-MT column in the main comparison; the stratification tables (inductive, sparsity-by-topology, negative type). Every cell must trace to a raw metrics row; no visual may present a target as a measurement or imply a hardware energy comparison.

## Traceability Checklist

| Guidance requirement | Required artifact | Minimum success check | Strong success check | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|
| Directly public datasets | dataset-access-log.md, frozen identities JSON | HTTP 200 and license recorded for all streams | all five streams verified and hashed | dataset/split table | yes |
| Ten-seed replication | results v4 main matrix | 60 runs with per-seed rows | locked decision rule executed once, verdict recorded | replication table with per-seed scatter | yes |
| Theory package | results/theory/* plus Method theorems | T1–T3 stated with assumptions; V-1 computed | violation rate at most 5 percent, V-3 slope CI excludes zero | bound-versus-measured figure | yes |
| Efficiency transparency | results/energy/* | energy table with cited constants | overhead at most 2 percent, three-level firing-rate stratification | energy table, stratification panels | yes |
| Statistical completeness | results/statistics/* | Cohen's d on main rows | d with CI plus probability of improvement on every headline row | main table columns | yes |
| New control C5-MT | results v4 main matrix | smoke plus 1 stream x 3 seeds minimum | full grid with per-stream margin | main comparison column | yes |
| Carry-over trade | results/theory/alpha/* | alpha curve computed | knee identified and reported either way | alpha trade-off figure | yes |
| Downstream and inductive validity | results/strata/* | epsilon-stratified MRR loss computed | positive dose-response trend; strata reported | validity figure and table | yes |
| Robustness and drift | results/robust_v4/* | five-level sweeps computed | degradation curves and drift summary | sweep and drift figures | yes |
| Citation integrity | reference-dedup-audit.md | all cited DOIs/arXiv ids checked | no duplicates, new survey citations verified | none | no (audit artifact) |
| Guidance coverage | paper-guidance-audit.md | every promised experiment and section covered | no unresolved item | none | no (audit artifact) |

## Citation Scope

Topic clusters (v3 retained): ANN-to-SNN conversion theory and calibration; cross-step error amplification and residual membrane potential; spiking and dynamic graph networks; continuous-time dynamic link prediction benchmarks and evaluation; temporal-graph survey and taxonomy; neuromorphic coding and graded/differential event coding. New clusters from the study: conversion-theory standards (ISC spectral-norm bounds, ECL decomposition and dose-response, RMP-SNNv2, When-SNN-meets-ANN, FTBC); the MPEF/CRPI/RMPA same-family mechanisms; direct-trained spiking GNN families (DRSGNN, SiGNN, Delay-DSGN, ChronoSpike, SpikingHAN, GT-SNT) and the SGNNBench benchmark; dynamic-graph evaluation protocol (TGB, TGB 2.0, TGB-Seq, Suter negative-sampling study, CRAFT); SNN energy methodology (Horowitz 2014 constants, Yan 2024 capacity matching); evaluation statistics (Agarwal rliable, Du 2025 paired protocol).

Must-cite works (identity verified at P12/P14; five pre-verified 2026-11-14 in citation-verification-log.md): all v3 must-cite works retained; plus ECL (ICML 2025), ISC (CVPR 2025), RMP-SNNv2, When-SNN-meets-ANN (TMLR 2025), FTBC (ECCV 2024), SGNNBench, ChronoSpike, Delay-DSGN, SiGNN, DRSGNN, SpikingHAN, GT-SNT, TGB, TGB 2.0, TGB-Seq, Suter et al. 2022, CRAFT, GraphSSM, Horowitz 2014, Yan 2024, Agarwal 2021, Du 2025, RMPA. Bibliography expectation: at least 48 verified entries (v3 delivered 43; E8's binding floor of at least 40 is retained and not raised).

## Constraints and Preferences

Retained verbatim: six numbered sections; Neurocomputing official limits (abstract at most 250 words, 1–7 keywords, 3–5 highlights of at most 85 characters, GenAI declaration before references; no official page limit, the at-least-21-pages requirement is the user's and is retained); GenAI declaration; data/code statement; no hardware energy claim; negative-result disclosures mandatory. New in v4: the C-1 decision rule text is part of this contract and may not be edited after the first 10-seed test inspection; theorem constants are estimated on validation data only; the C5-MT demotion path is pre-authorized and must leave failed-attempt evidence.

## External audit references

- `guidance-v4-amendment.md` (trigger, changes, non-changes, re-acceptance)
- `ccfa-startup-packet-v4/` (seven startup artifacts plus feasibility-contract.json hash-binding them)
- `docs/top-venue-study/` (00-synthesis, 01–04 survey reports, gap-analysis v1.0, citation-verification-log)
- `ccfa-startup-packet-v3/` and `guidance-v3.md` (superseded contract, preserved)
- v3 run root `f-research-v1-run-20261114-153501-gnn-v3/` (evidence reused under applicability notes)
