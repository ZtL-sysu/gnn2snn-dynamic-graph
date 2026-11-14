# Pipeline State (f-research-v1, contract v3)

- Guidance file: `../guidance-v3.md` (v1/v2 preserved)
- Run root: `f-research-v1-run-20261114-153501-gnn-v3/` inside the guidance directory
- Structured authority: `pipeline-state.json` (26 stages, SHA-256 bound, contract_version v3)
- Back-edge: user directive 2026-11-14 reopened P0 with a new method family and E6--E8.

| Stage | Name | Status | Evidence | Gate |
|---|---|---|---|---|
| P0 | Load guidance and create run root | passed | `audits/path-containment-manifest.md` | pass |
| P1 | Validate guidance and load CCFA packet | passed | `audits/P1-guidance-validation.md` | pass |
| P1A | Strong-result feasibility lock | passed | `audits/strong-result-feasibility-lock.md` | pass |
| P1B | Pre-experiment adversarial review | passed | `audits/ccfa-pre-experiment-review.md` | pass |
| P2 | Runnable protocols and local environment | passed | `audits/P2-environment-check.md` | pass |
| P3 | Baseline-first execution | passed | `results/p3_baselines/validation_mrr_v3.json` | pass |
| P3A | Baseline-evidence stop-loss review | passed | `audits/P3A-baseline-evidence-review.md` | pass |
| P4 | Full experiment campaign | passed | `results/aggregated.json` | pass |
| P5 | Strong-result lock | passed | `audits/P5-strong-result-lock.md` | pass |
| P5A | Pre-draft scientific review | passed | `audits/ccfa-pre-draft-scientific-review.md` | pass |
| P6 | PAPER_OUTLINE | passed | `writing/PAPER_OUTLINE.md` | pass |
| P7 | PAPER_DRAFT | passed | `writing/PAPER_DRAFT.md` | pass |
| P8 | Figures and tables | passed | `audits/figure-table-audit.md` | pass |
| P9 | PEER_REVIEW | passed | `writing/PEER_REVIEW.md` | pass |
| P10 | PAPER_REVISION | passed | `writing/PAPER_REVISION.md` | pass |
| P11 | QUALITY_GATE | passed | `writing/QUALITY_GATE.md` | pass |
| P12 | Reference verification | passed | `audits/reference-dedup-audit.md` | pass |
| P13 | EXPORT_PUBLISH | passed | `paper/main.tex` | pass |
| P14 | CITATION_VERIFY | passed | `audits/reference-dedup-audit.md` | pass |
| P15 | TeX/PDF compile | passed | `paper/main.pdf` | pass |
| P16 | Journal limits and author length | passed | `audits/final-metadata-counts.json` | pass |
| P17 | Guidance coverage audit | passed | `audits/paper-guidance-audit.md` | pass |
| P18 | Figure/table audit | passed | `audits/figure-table-audit.md` | pass |
| P19 | Final polish | passed | `writing/FINAL_POLISH.md` | pass |
| P20 | Submission constraints | passed | `audits/submission-constraints.md` | pass |
| P21 | Final delivery | passed | `deliverables/manifest.json` | pass |

## Correction ledger

v2 cycles C1--C9 are in the v2 run root; v3 cycles V3-1/V3-2 are in `correction-ledger.md`. No failed run was deleted and no numeric binding target was lowered after a verdict. Cycles C10-C16 are in `correction-ledger.md`; C16 narrows the CLAIM SCOPE (not any numeric target) after a genuine LastFM null result and adds a mandatory disclosure obligation. The original all-five-stream verdict `d_replication: false` is preserved.

## Accepted claim scope

All 26 stages are passed as executed; the delivered scientific claim is the C16 evidence-bounded one: significant state-error reduction on four streams, LastFM disclosed as a direction-consistent but non-significant boundary case. See `audits/P5-strong-result-lock.md`.

## Author length requirement

>=21 pages and >=40 verified references; see `audits/final-metadata-counts.json`.
