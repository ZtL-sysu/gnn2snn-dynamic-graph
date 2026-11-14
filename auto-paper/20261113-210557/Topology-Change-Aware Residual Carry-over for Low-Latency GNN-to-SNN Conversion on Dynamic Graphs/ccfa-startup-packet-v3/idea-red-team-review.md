# Independent Idea Red-Team Review (standard mode)

Owner: `ccf-idea-reviewer` spec at `/Users/xhf/.codex/skills/ccf-idea-reviewer/SKILL.md`. This review is intentionally separate from the idea cards and was written **after** the opportunity map existed. It reviews the problem and mechanism only, not prose or structure. No reviewer sentiment, acceptance probability, or prior art is invented.

## Verdict summary

| Dimension | Score / level | Basis |
|---|---|---|
| **Current readiness** | **6.2 / 10** | A real, named mechanism with a derivable bound and three discriminating experiments; but the closest 2026 work (CRPI) shares the core cross-step idea, the strongest prediction baselines cannot be rerun locally, and novelty has not had a structured database sweep. |
| **Development potential** | **7.5 / 10** | If the topology term is measurable, the work yields a bound + a cost-bound mechanism + a diagnostic protocol that transfers to other event-stream models. |
| **Confidence in the assessment** | **medium** | Public web search plus local predecessor corpus; no Scopus/IEEE sweep, no pilot run yet, and the ANN teacher has not been trained on this machine. |
| **Decision** | **proceed with mandatory repair conditions** | No *unaddressed* fatal risk remains: each fatal risk below has a concrete, pre-registered repair and an experiment that would expose failure. Missing mechanism, unavailable baseline, and infeasible evidence plan are all resolved on paper with executable paths. |

A low readiness score is not by itself a rejection. This review does **not** convert an unsearched novelty claim into a positive score: novelty is explicitly scored below and held at moderate confidence.

## Fatal risks and required repairs

| # | Fatal risk | Why a strict reviewer deducts | Repair condition (must be satisfied before P2 / P4) | Score-change condition |
|---|---|---|---|---|
| F1 | CRPI (ICML 2026) already carries residual potential across steps; "graph version" reads as incremental | The central mechanism is not new in kind | Implement CRPI-style global carry-over as a `must-rerun` control; add topology-change dose-response, static-graph control, and matched-budget comparison. If TCAR does not beat global carry-over on all three, the method claim is withdrawn and the diagnostic fallback applies | +1.5 if all three discriminating experiments are pre-registered and pass P3A; −2.0 if any is dropped from the plan |
| F2 | No direct rerun of recent strong CTDG predictors (TGN/GraphMixer/DyGFormer) | A reviewer can say the teacher and the absolute-MRR context are weak | Main claim is conversion fidelity on a matched teacher; conversion-family baselines are direct reruns. Absolute MRR is explicitly context. If P2 prototype shows GraphMixer ≤30 min/seed on a Wikipedia subset, promote it to `adaptation-attempt` | +0.5 if promoted; −0.5 if the limitation is not disclosed in the manuscript |
| F3 | Novelty not verified by structured database search | "No one has done X" is unsupportable from web results alone | P12/P14 DOI/arXiv/title/venue duplicate sweep with `reference-dedup-audit.md`; moderate confidence stated openly | +0.8 if the sweep finds no direct overlap; −2.5 and reopen G4 if a directly overlapping paper exists |
| F4 | Teacher quality may be near chance, making fidelity vacuous | Retention of a bad teacher is meaningless | Gate at P3: teacher must beat EdgeBank/Base3 on validation before P4 proceeds | −1.5 if the gate is skipped |
| F5 | Bound (1) may be theoretically plausible but empirically false or unmeasurable | A theory paper with no measured `ε_k`, `‖ΔA_k‖` is unfalsifiable | Instrument per-event `ε_k`, `‖ΔA_k‖`, `δ_v(k)` from the prototype; verify the inequality within numerical tolerance at P4 | −2.0 if instrumentation is absent |
| F6 | Test queries were used in a predecessor local project | Not a blind evaluation; absolute numbers can be optimised | Freeze IDs and hashes at P2, disclose in Discussion, keep main claim on paired within-run comparisons | −1.0 if undisclosed |
| F7 | M1/16 GiB/12 h budget may not support 5 seeds × 3 streams × all ablations | An incomplete matrix cannot carry the claim | 30-minute single-seed prototype at P2; if it fails, reopen G5 with evidence-preserving scaling (fewer optional streams, still ≥2 seeds and all six ablations on the primary stream) | −1.5 if budget is silently exceeded; +0.5 if prototype completes |
| F8 | "Energy" or "5×" claims are not supportable without neuromorphic hardware | Prior user archive already withdrew such a claim | Removed from scope; report graded-event counts, recomputation counts, parameters, and local PyTorch latency only | −1.0 if any energy claim appears |

## Score-change conditions (explicit)

- Readiness rises to ≥7.5 only when F1's three discriminating experiments are pre-registered, F4's teacher gate passes at P3, F5's instrumentation lands at P4, and F7's prototype completes at P2.
- Readiness falls below 5.0 (block) if F3 finds a directly overlapping paper, if F4's teacher gate fails with no repair, or if F5's bound is empirically violated with no replacement mechanism.
- Confidence rises from medium to high only after P5A's independent scientific review of the real evidence dossier. **No score in this file is based on experimental results, because none exist yet.**

## What the reviewer would want to see that is not yet present

1. A measured `ρ` (state-update Lipschitz constant) on the actual teacher, not an assumed value.
2. A concrete definition of `A_k` for the chosen aggregation, with a Jacobian fallback if the operator is not linear.
3. Evidence that the recalibration trigger rate is genuinely below the event count on real streams (the ≤20% cost target).
4. A failure-mode write-up preserving negative and null results.

All four are listed as explicit P2/P4 actions in `strong-result-feasibility-contract.md` and `evaluation-protocol.md`.
