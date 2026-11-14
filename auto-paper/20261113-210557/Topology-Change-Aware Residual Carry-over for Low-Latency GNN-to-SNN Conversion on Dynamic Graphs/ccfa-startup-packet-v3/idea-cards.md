# Idea Cards (standard mode, mechanism level)

Owner: `ccf-idea-optimizer` spec at `/Users/xhf/.codex/skills/ccf-idea-optimizer/SKILL.md`. Novelty is marked as uncertainty until searched; the searched verdict is in `prior-art-opportunity-map.md`. No results, baselines, or reviewer reactions are invented here.

## Card C1 — "Static-base reuse under event streams" (diagnostic only)

- **Bottleneck**: the user's `gnn2snn` archive caches a static base `Wh₀+b` and a shared residual prefix per forward pass. That cache assumes `graph`, `W`, and the incoming edge set are constant within a conversion trajectory. A CTDG violates all three.
- **Mechanism**: quantify the discrepancy when the cached base is reused across events; derive a term proportional to the change in the aggregation operator `‖ΔA_k‖`.
- **Assumptions**: fixed event order; reproducible neighbor snapshots; linear/normalized aggregation.
- **Falsification condition**: the discrepancy does not grow with cumulative `‖ΔA_k‖` (no dose-response).
- **Contribution type**: negative/diagnostic empirical result + theory.
- **Feasibility risks**: moderate. Requires instrumentation of `A_k`, but no new architecture.
- **Why it is not enough alone**: a diagnostic paper without a mechanism that repairs the discrepancy will be judged thin for Neurocomputing. **Not selected as the main claim**; retained as a required ablation and as the honest fallback story.

## Card C2 — "Global cross-step residual carry-over on graphs" (control only)

- **Bottleneck**: hard reset discards residual membrane potential at every event window, so quantization error is not corrected downstream.
- **Mechanism**: carry residual potential across event windows for all nodes (CRPI-style).
- **Assumptions**: same as C1 plus a bounded state-update Lipschitz constant.
- **Falsification condition**: no reduction in end-of-window disagreement versus hard reset.
- **Contribution type**: adaptation.
- **Feasibility risks**: low; gradient-free and cheap.
- **Novelty status**: **already covered** by CRPI (ICML 2026, arXiv:2601.21778) and, in a different domain, by Spiking DiTs MPEF (ICML 2026). Using this as the main claim would be incremental.
- **Role**: `must-rerun` adapted control — the single most important discriminator for C3.

## Card C3 — SELECTED: topology-change-aware residual carry-over (TCAR)

- **Bottleneck**: in a CTDG, conversion error recurs along the **event axis**, and the aggregation operator itself changes. Existing conversion error theory bounds error along **layers** of a fixed network; cross-step residual methods (CRPI/MPEF) handle temporally correlated error but have no graph and no changing neighbor set. Neither explains or targets the topology-change contribution.
- **Causal/algorithmic mechanism**:
  1. Derive `ε_k ≤ ρ ε_{k−1} + L_A ‖ΔA_k‖ ‖s_{k−1}‖ + c/T + η_k`, where `ε_k` is the converted-vs-ANN state error, `ΔA_k` the change in the neighbor-aggregation operator, `c/T` the rate-coding floor, and `η_k` the discarded residual potential.
  2. Carry the residual membrane potential forward for nodes touched by an event (removes `η_k` there).
  3. Recompute the static base, recalibrate the threshold, and flush the shared residual prefix **only** when the node's relative neighbor-set change `δ_v(k)` exceeds `gamma` (targets `‖ΔA_k‖` where it is large).
  4. Consequence: recomputation cost scales with topology-change events, not with total events.
- **Assumptions**: see the seven assumptions A1–A7 in `theoretical-feasibility-audit.md`; the most fragile are `ρ < 1` (A1), a well-defined normalized `A_k` (A2), and conversion-friendly teacher nonlinearities (A3).
- **Falsification condition**: any of the following kills the main claim — (i) the topology-change-gate ablation is indistinguishable from global carry-over at matched recomputation budget; (ii) there is no monotone dose-response between `‖ΔA_k‖` and disagreement; (iii) freezing the topology does not shrink the TCAR advantage; (iv) bound (1) is empirically violated.
- **Contribution type**: mechanism + bound + event-bound cost trade-off, with a diagnostic fallback.
- **Known feasibility risks**:
  - CRPI overlap (highest). Mitigated by the three discriminating experiments and by implementing CRPI-style carry-over as a direct control.
  - Teacher quality: a near-chance teacher makes fidelity numbers vacuous. Mitigated by requiring the teacher to beat EdgeBank/Base3 on validation before P4.
  - Non-blind test IDs. Disclosed; main claim rests on paired within-run comparisons.
  - Strong prediction baselines are not locally rerunnable within 12 h. Explicitly downgraded to literature-context, with the reason in the baseline matrix.
  - Novelty confidence moderate, pending a structured DOI/arXiv duplicate sweep at P12/P14.
- **Why this is more than "apply method X to dataset Y"**: it introduces a term that does not exist in the source theory, ties a cost model to that term, and makes both falsifiable through topology stratification and a static-graph control.

## Card C4 — "Directly trained spiking CTDG encoder" (rejected)

- **Bottleneck**: converted SNNs inherit an ANN ceiling.
- **Mechanism**: surrogate-gradient training of a small spiking dynamic-graph encoder.
- **Falsification condition**: it does not match the converted model at equal parameter count.
- **Contribution type**: architecture.
- **Feasibility risks**: training cost on M1; and the domain is already occupied by SpikeNet / Dy-SIGN.
- **Decision**: rejected as main claim at G4; retained as the `D1` parallel control in the experiment plan.

## Idea-stage risk register

| Risk | Severity | Repair condition before G0 |
|---|---|---|
| CRPI makes C3 look incremental | high | three discriminating experiments written into the claim-evidence matrix; CRPI promoted to `must-rerun` control |
| No runnable strong baseline on M1 | high | conversion-family baselines (cheap) carry the main comparison; prediction SOTA explicitly separated |
| Novelty unsearched | high | structured literature search recorded in the opportunity map; confidence stated as moderate |
| Test IDs not blind | medium | disclosed; absolute-MRR claims downgraded |
| Energy claim unsupported | medium | removed from scope entirely; cost metrics are event counts and local latency |
