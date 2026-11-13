# Story Strength Audit

## 1 Why a skeptical Neurocomputing reviewer would care

ANN→SNN conversion is attractive because it inherits a trained network without retraining, but its error theory was built for **one static forward pass**. Deploying a converted model on an event stream is a different problem: the same state that carries the conversion error is fed into the next event, and the set of neighbors being aggregated changes. A reviewer who works on either SNN conversion or dynamic graphs will recognise that neither literature currently explains what happens to conversion error along the event axis. The paper offers a bound with an explicit topology-change term, a mechanism that targets it, and an instrumentation protocol that makes the term measurable.

## 2 The strongest existing paper that could make this look incremental

**CRPI, *Error Amplification Limits ANN-to-SNN Conversion in Continuous Control*, ICML 2026 (arXiv:2601.21778)**. It already establishes that conversion errors are temporally correlated across decision steps, produce state distribution shift, and can be suppressed by carrying residual membrane potential across steps — gradient-free. If our method were "carry the residual over on a dynamic graph", the correct verdict would be incremental.

A second threat is **Spiking DiTs MPEF (ICML 2026)**, which recycles residual membrane potential across denoising steps. Together they establish cross-step residual feedback as a 2026 theme.

## 3 The exact experiment that distinguishes this work from CRPI

Three linked tests, all on the same teacher and stream:

1. **Topology-change dose-response**: stratify test windows by measured `‖ΔA_k‖` (equivalently by the relative neighbor-set change `δ_v(k)`) and plot end-of-window teacher→SNN disagreement. CRPI has no `A_k`, so it predicts no systematic dependence on topology change. Our bound predicts a monotone increase that TCAR flattens.
2. **Static-graph control**: freeze the neighbor sets (same events, no topology evolution) and rerun all conversion variants. Our mechanism predicts the TCAR advantage over global carry-over shrinks toward zero; CRPI-style global carry-over should be unaffected.
3. **Matched-budget comparison**: global carry-over (CRPI-style, recompute-free) vs TCAR (recompute only on `δ_v(k) > gamma`). If TCAR wins at equal or lower recomputation count with paired bootstrap CI excluding zero, the topology gate — not residual carry-over alone — is the cause.

If all three fail, the honest conclusion is that the topology term is negligible and the contribution is a diagnostic measurement, not a method.

## 4 What result threshold is needed for a strong paper, not a runnable demo

From `strong-result-feasibility-contract.md`: at `T=4`, end-of-window teacher decision agreement ≥98.5% with MRR retention ≥99% on the primary stream; the agreement decay over a 10k-event window ≤0.5 pp for TCAR while the strongest conversion control decays ≥2.0 pp, with 5-seed paired bootstrap 95% CI excluding zero; recalibration triggered on ≤20% of events; and the direction replicated on two additional public streams. Merely producing a converted SNN that runs, or a small MRR gain on one dataset, is explicitly a **failure signal**, not a strong result.

These thresholds are calibrated against measured prior ranges in the user's own static-graph archive (T=4 teacher agreement 99.28–99.98%, GatedGCN T4 99.55±0.16%, three seeds) with a non-inferiority allowance for the harder dynamic setting. They are pre-registered here; P5 may not lower them after seeing results.

## 5 Honest risks a reviewer will raise, and the manuscript's answer

| Risk | Answer to be given in the paper |
|---|---|
| "You did not beat TGN/DyGFormer/GraphMixer" | The contribution is conversion fidelity, not predictive SOTA. Absolute MRR is reported as context with published reference rows; the main comparison is against matched conversion controls on the same teacher. The local compute ceiling that prevents a full SOTA rerun is disclosed. |
| "CRPI already did residual carry-over" | The topology-change term, the event-triggered base recalibration, and the three discriminating experiments above are the differentiation; CRPI is implemented as a direct control, not cited away. |
| "The test set is not blind" | Frozen query IDs were used in a predecessor local project; disclosed in Discussion, with absolute-MRR claims deliberately downgraded and the main claim resting on paired within-run comparisons. |
| "You claim energy savings without neuromorphic hardware" | No energy claim is made. We report graded-event counts, recomputation counts, parameter count, and local PyTorch wall-clock latency as positive evidence boundaries. |
| "Novelty is asserted from a web search" | Novelty confidence is stated as moderate; P12/P14 runs a structured DOI/arXiv/title duplicate audit and re-verifies every citation before the bibliography is frozen. |
| "One dataset" | Three public streams (Wikipedia primary, MOOC, Enron) with the same frozen protocol; Reddit/LastFM optional robustness. |

## 6 If the result is only partially positive

The pre-declared lower-tier story is a **measurement and diagnostics** paper: quantify conversion-error accumulation as a function of event-window length and cumulative `‖ΔA_k‖` on public CTDG streams, validate or refute the bound, and report which conversion controls fail where. This retains a theoretical/empirical contribution without claiming method superiority. It requires a **versioned guidance-contract change** under `f-research-v1/references/research-recovery.md`, not a quiet rewrite of `expected_strong`. If even the bound is not supported, the direction is closed and the negative evidence is published in the run root as a checkpoint.

## 7 Agreement with the strong-result feasibility contract

Every experiment named here (dose-response, static control, matched-budget comparison, T/gamma sweeps, three-stream replication, seed/bootstrap protocol, cost accounting) appears in `claim-evidence-matrix.md` and `strong-result-feasibility-contract.md` with a mechanism, a falsifying ablation, a code path, a prototype milestone, and a compute/seed/search budget. This audit promises no experiment that is absent from the contract.
