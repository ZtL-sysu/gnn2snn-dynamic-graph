# CCFA Pre-Experiment Adversarial Review (P1B)

Executed per the `ccf-idea-reviewer` specification read read-only from `/Users/xhf/.codex/skills/ccf-idea-reviewer/SKILL.md` (standard mode). Inputs: `../ccfa-startup-packet/prior-art-opportunity-map.md`, `../ccfa-startup-packet/idea-cards.md`, `../ccfa-startup-packet/claim-evidence-matrix.md`, `../ccfa-startup-packet/strong-result-feasibility-contract.md`, and `audits/P1-guidance-validation.md`. This is a review of **planned** claims; no experiment has been run.

## Verdict

`proceed` for P2, with one additional binding condition added below. No `pivot-with-rescue-route`, no `needs-literature-search`, no unsupported binding claim, and no unbounded implementation risk remains unresolved.

| Dimension | Level | Basis |
|---|---|---|
| Current readiness | 6.4 / 10 | Same mechanism as the startup red-team (6.2/10), plus a completed P1A lock and a concrete prototype path. Still limited by CRPI overlap, moderate novelty confidence, and literature-context-only CTDG predictors. |
| Development potential | 7.5 / 10 | bound + mechanism + cost model, with a diagnostic fallback |
| Confidence | medium | public web search plus local predecessor corpus; no structured DOI sweep; no real teacher trained yet |

## Fatal-risk re-check against the now-frozen contract

| Risk | Status after P1A | Repair still required |
|---|---|---|
| CRPI overlap | mitigated on paper; **not yet empirically resolved** | C4 must be implemented at P4; the three discriminating experiments are mandatory, not optional |
| Strong CTDG predictors not rerun | disclosed, downgraded | P2 prototype decides whether GraphMixer is promotable; otherwise the downgrade stays in the manuscript |
| Novelty moderate | open | P12/P14 structured duplicate sweep |
| Teacher vacuity | gated | P3 teacher must beat B1/B2 on validation |
| Bound unmeasurable | instrumented | per-event `epsilon_k`, `||ΔA||`, `delta_v(k)` from the prototype onward |
| Non-blind test | disclosed | frozen IDs + paired within-run main claim |
| Budget | **new evidence** | P2 smoke completed in under one second on 2000 events; a full 157k-event window still needs a real timing check at P3 before the 12 h ceiling is accepted |
| Energy claim | removed | none may appear |

## Additional binding condition raised at P1B

The smoke prototype uses an **untrained random teacher** and a saturating residual state, so its absolute agreement (0.0755 / 0.33 in the repaired run) is not a fidelity measurement. P3 must (1) train a real lightweight teacher to a non-vacuous validation level before any conversion claim, (2) add state decay or normalization so the state norm does not saturate, and (3) re-check the clipping-rate assumption A4 on the trained teacher. If any of these fails, P3 returns to P2 rather than continuing to P4.

## Score-change conditions

- Readiness rises to >=7.5 only after P3A confirms a non-vacuous teacher and reproducible baselines, and P5A confirms the three discriminating experiments with real evidence.
- A `pivot-with-rescue-route` is triggered if C4 cannot be implemented, the bound is empirically violated, or the structured novelty sweep finds a directly overlapping paper.

## P1B gate

No fatal novelty, soundness, feasibility, or claim-support risk remains unresolved; every score deduction has a repair condition. **P1B pass.** P2 may begin.
