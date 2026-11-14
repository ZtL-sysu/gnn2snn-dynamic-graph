# P5A Pre-Draft Scientific Review (`ccf-paper-reviewer`, scientific mode)

Reviewed the clean pre-draft evidence dossier: `audits/P5-strong-result-lock.md`, `results/statistics/final-analysis.json`, `results/p4_runs/*.json`, `results/p4_auxiliary/sweeps.json`, `experiment-traceability.md`, `guidance-v2.md`, `guidance-v2-amendment.md`. Reviewer wording is kept external to drafting inputs.

| Dimension | Verdict |
|---|---|
| Novelty | Adequate with positioning. ANN→SNN conversion on CTDG with a topology-change term is distinct from directly trained spiking dynamic-graph models \cite{li2023spikenet,yin2024dysign} and from cross-step conversion in control/generation \cite{xu2026crpi,fang2026mpef}. Confidence moderate, pending a full database sweep. |
| Soundness | The bound is stated as a tested claim with explicit assumptions; the mechanism is isolated by six ablations; C4 is a faithful CRPI-style control. |
| Evidence | 15 test runs, 5 seeds, 3 streams, 11 methods, frozen splits, per-seed values, paired bootstrap, BH correction, raw traces. All binding targets met. |
| Reproducibility | Code, configs, frozen hashes, per-query rows and figures sources are in the run root; public Zenodo data. |
| Claim scope | Correctly bounded: conversion fidelity, not predictive SOTA; no energy claim; non-blind IDs disclosed. |

## Concerns and required actions

1. The relative dose-response is negative (non-monotone, with negative Enron bins). **Action**: mandatory disclosure in Abstract, Results and Discussion; do not present as mechanism support. Satisfied in `main.tex`.
2. Agreement saturates and does not discriminate on two streams. **Action**: name `ε_k` as the discriminating metric and report the paired CIs containing zero. Satisfied.
3. Absolute MRR is dominated by discrete memory. **Action**: context-only framing in all places where MRR appears. Satisfied.
4. The v2 amendments must remain visible and pre-registered, not quietly folded into the narrative. **Action**: keep `guidance-v2-amendment.md`, `correction-ledger.md` and the back-edge in `pipeline-state.json`. Satisfied.

No fatal soundness, novelty, evidence, or reproducibility concern remains unresolved. **P5A pass**; P6 may begin.
