# CCFA Startup Decision

**Decision: `proceed`**

Date: 2026-11-13. The only `proceed` outcome may enter `f-guidance-builder-v1` G0. This decision is based on the seven sibling artifacts in this packet and on the verified evidence they index; it is not based on any experimental result, because none exists.

## Checklist against the blocking rules

| Blocking condition | Status | Evidence |
|---|---|---|
| Unaddressed fatal risk | **clear** | Eight fatal risks F1–F8 in `idea-red-team-review.md` each have a named repair, an owning stage, and a score-change condition. The highest risk (CRPI overlap) is handled by promoting CRPI-style global carry-over to a `must-rerun` control and pre-registering three discriminating experiments. |
| Missing mechanism | **clear** | Card C3 states the algorithmic mechanism and the bound `ε_k ≤ ρ ε_{k−1} + L_A ‖ΔA_k‖ ‖s_{k−1}‖ + c/T + η_k`, with seven assumptions and six falsifying ablations in `theoretical-feasibility-audit.md`. |
| Unavailable baseline | **clear** | Four baseline classes with two directly rerunnable conversion controls (CRPI-style, SNNC-AP-light, DCGS coder, QCFS/FTBC, hard-reset IF, EdgeBank, Base3). Recent CTDG predictors are explicitly separated as literature-context with the local compute reason recorded. |
| Infeasible evidence plan | **clear** | `claim-evidence-matrix.md` and `strong-result-feasibility-contract.md` give an executable baseline-first queue, a 30-minute prototype milestone, ≤120 runs / ≤12 h / 5 seeds / ≤24 search trials, frozen test identities, and explicit stop-and-return conditions. |
| No directly public dataset | **clear** | Zenodo `10.5281/zenodo.7213796` returned HTTP 200 with CC BY 4.0 and direct file URLs on 2026-11-13; four local frozen `.npz` streams loaded successfully. See `dataset-access-log.md` one level up. |
| Unsupported binding claim | **clear** | `expected_strong` is calibrated against measured three-seed static-graph prior ranges from the user's own archive plus an effect-size criterion on paired within-run comparisons. No desired headline gain is used. |
| Novelty claimed without search | **clear with caution** | `prior-art-opportunity-map.md` records five closest-work clusters with links and explicitly labels novelty confidence as **moderate** pending a structured DOI/arXiv sweep at P12/P14. No unsearched novelty claim was converted into a positive score. |

## Mandatory conditions carried into G0–G8 and P0–P5

1. G4 must retain the CRPI differentiation statement verbatim in substance; a structured duplicate sweep at P12/P14 may downgrade novelty but must not be skipped.
2. G6 retains the explicit downgrade of TGN/GraphMixer/DyGFormer to literature-context. Promotion to `adaptation-attempt` is allowed only if the P2 prototype demonstrates ≤30 min/seed, and must be recorded as a contract update.
3. P2 must run the 30-minute single-seed prototype and freeze stream/test hashes before any tuning; P3 must establish B0/B1/B2/C0 before any proposed-method claim.
4. P3 must gate the ANN teacher against EdgeBank/Base3 on validation.
5. P4 must instrument `ε_k`, `‖ΔA_k‖`, `δ_v(k)` per event and verify the bound is not violated.
6. No energy or neuromorphic-hardware claim may enter the manuscript.
7. Any missed binding target enters `f-research-v1`'s authorized correction loop with a versioned replacement contract; targets are not lowered after results are seen.

## Why not the other outcomes

- `revise`: not chosen because the repairs are already concrete, owned, and pre-registered; nothing material is left unspecified at the idea stage.
- `pivot-with-rescue-route`: not chosen because each fatal risk has a repair inside the same method family and tier; no method-family or tier change is needed.
- `needs-evidence`: not chosen because the missing evidence (pilot runtime, measured `ρ`, clipping rate, duplicate sweep) is assigned to specific downstream gates with stop-and-return conditions; obtaining it before G0 would require experiments that the guidance-builder phase is not allowed to run.

## Limits of this decision

`proceed` here means the **plan** is admissible. It does not assert that the mechanism works, that novelty holds, that the journal will accept the paper, or that any target has been met. The independent red-team readiness score remains 6.2/10 with medium confidence, and P1B/P3A/P5A stop-loss reviews must re-examine these conclusions against real evidence.
