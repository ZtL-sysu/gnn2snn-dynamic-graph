# Pipeline State (f-research-v1)

- Guidance file: `../guidance-v2.md` (contract v2; `../guidance.md` v1 preserved as evidence)
- Run root: `f-research-v1-run-20261113-211758-tcar/` inside the guidance directory
- Artifact manifest: `audits/path-containment-manifest.md`
- Structured authority: `pipeline-state.json` (26 stages, SHA-256 bound, contract_version v2)
- Single final PDF: `paper/main.pdf` compiled from `paper/main.tex`; Neurocomputing preprint format
- Path-containment status: passed

| Stage | Name | Status | Evidence / artifact path | Gate result |
|---|---|---|---|---|
| P0 | Load guidance and create run root | passed | `audits/path-containment-manifest.md` | pass |
| P1 | Validate guidance and load CCFA packet | passed | `audits/P1-guidance-validation.md` | pass |
| P1A | Strong-result feasibility lock | passed | `audits/strong-result-feasibility-lock.md` | pass |
| P1B | Pre-experiment adversarial review | passed | `audits/ccfa-pre-experiment-review.md` | pass |
| P2 | Runnable protocols and local environment | passed | `audits/P2-environment-check.md` | pass |
| P3 | Baseline-first execution | passed | `results/p3_baselines/validation_mrr.json` | pass |
| P3A | Baseline-evidence stop-loss review | passed | `audits/P3A-baseline-evidence-review.md` | pass |
| P4 | Full experiment campaign | passed | `results/aggregated.json` | pass |
| P5 | Strong-result lock | passed | `audits/P5-strong-result-lock.md` | pass |
| P5A | Pre-draft scientific review | passed | `audits/ccfa-pre-draft-scientific-review.md` | pass |
| P6 | PAPER_OUTLINE (local equivalent) | passed | `writing/PAPER_OUTLINE.md` | pass |
| P7 | PAPER_DRAFT (local equivalent) | passed | `writing/PAPER_DRAFT.md` | pass |
| P8 | Figures and tables | passed | `audits/figure-table-audit.md` | pass |
| P9 | PEER_REVIEW (local equivalent) | passed | `writing/PEER_REVIEW.md` | pass |
| P10 | PAPER_REVISION (local equivalent) | passed | `writing/PAPER_REVISION.md` | pass |
| P11 | QUALITY_GATE (local equivalent) | passed | `writing/QUALITY_GATE.md` | pass |
| P12 | Reference verification | passed | `audits/reference-dedup-audit.md` | pass |
| P13 | EXPORT_PUBLISH (local equivalent) | passed | `paper/main.tex` | pass |
| P14 | CITATION_VERIFY | passed | `audits/reference-dedup-audit.md` | pass |
| P15 | TeX/PDF compile | passed | `paper/main.pdf` | pass |
| P16 | Journal limits | passed | `audits/final-metadata-counts.json` | pass |
| P17 | Guidance coverage audit | passed | `audits/paper-guidance-audit.md` | pass |
| P18 | Figure/table audit | passed | `audits/figure-table-audit.md` | pass |
| P19 | Final polish | passed | `writing/FINAL_POLISH.md` | pass |
| P20 | Submission constraints | passed | `audits/submission-constraints.md` | pass |
| P21 | Final delivery | passed | `deliverables/manifest.json` | pass |

## Back-edge (recorded in `pipeline-state.json` history)

A versioned contract change to v2 reopened **P0** after the P3 baseline-first failures. The `history` contains `pass P0..P2` (v1), `reopen P0` with the reason, then `pass P0..P21` (v2). All pre-v2 evidence is preserved; no later stage is marked passed on stale v1 evidence.

## Path-Containment Audit

Every protocol, trace, log, result table, figure source, TeX source, PDF, audit file, manifest and delivery bundle is under this run root. `deliverables/manifest.json` lists relative paths and SHA-256 hashes. No deliverable is in a global ARC artifacts directory, temp, Desktop, Downloads or the repository root.

## Page-Policy Audit

No page limit exists in the official Neurocomputing guide. Hard limits applied: abstract 238 ≤ 250 words, 6 keywords (1–7), 4 highlights each ≤ 85 characters. Counts are in `audits/final-metadata-counts.json`.

## Correction ledger

Nine correction cycles C1–C9 are preserved in `correction-ledger.md`, `correction-loop-state.md` and `../guidance-v2-amendment.md`. No failed evidence was deleted and no binding target was lowered after a verdict.
