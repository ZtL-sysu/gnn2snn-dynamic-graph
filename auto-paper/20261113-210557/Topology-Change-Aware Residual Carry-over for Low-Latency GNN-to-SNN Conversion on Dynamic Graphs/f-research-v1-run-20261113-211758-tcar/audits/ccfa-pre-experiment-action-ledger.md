# Concern-to-Action Ledger (P1B)

| # | Concern | Raised by | Action | Owner stage | Pass condition | Status |
|---|---|---|---|---|---|---|
| 1 | CRPI (ICML 2026) makes residual carry-over non-novel | idea red-team F1 | Implement C4 global carry-over as direct control; run three discriminating experiments | P4 | all three rows done with paired bootstrap CI | open |
| 2 | Smoke agreement is far below the 95% minimum | P1B review + P2 evidence | Train a real teacher, add state decay/normalization, re-check calibration coverage | P3 (return to P2 if it fails) | teacher beats B1/B2 on validation; no state saturation | open |
| 3 | Strong CTDG predictors are literature-context only | red-team F2 | P2 prototype decides GraphMixer promotability; otherwise keep the disclosed downgrade | P2/P3 | either a <=30 min/seed adaptation or an explicit recorded downgrade | partially resolved at P2 |
| 4 | Novelty confidence moderate | red-team F3 | Structured DOI/arXiv/title/venue duplicate sweep | P12/P14 | `reference-dedup-audit.md` with no unresolved overlap | open |
| 5 | Test IDs non-blind | red-team F6 | Freeze IDs at P2; disclose in Discussion; keep main claim on paired comparisons | P2/P20 | `frozen-identities.json` exists; disclosure present in manuscript | resolved at P2 (disclosure still owed at P20) |
| 6 | Bound may be unmeasurable | red-team F5 | Instrument `epsilon_k`, `||ΔA||`, `delta_v(k)` per event from the prototype | P2/P4 | `raw_results.jsonl` contains all three per event | resolved at P2 (full-window check owed at P4) |
| 7 | Energy claim unsupported | red-team F8 | Remove from scope; report graded events, recomputation count, parameters, local latency | P4/P19 | no energy claim in manuscript | open (scope removed) |
| 8 | IF conversion code path defective | P2 smoke evidence verification | Repair the T-step integration and decoding scale, rerun | P2 | code path produces non-zero decoded activations and carry-over beats hard reset | **resolved at P2** |
| 9 | `rho` and clipping assumptions unverified | red-team F5 / A1,A4 | Measure `rho` on the trained teacher; re-check clipping rate | P3/P4 | `rho < 1` or bounded-horizon repair; clipping <=1% | open |
| 10 | Official venue limits unknown | P1 contract | Check Elsevier guide-for-authors | P20 | `submission-constraints.md` with primary-source links | open |

No concern above is resolved by inventing evidence. Items marked `open` are blocking for the stage that owns them, not for P2.
