# Pipeline State (f-research-v1)

- Guidance file: `../guidance.md` (absolute path resolved at P0; the run root is inside the guidance directory)
- Run root: `auto-paper/20261113-210557/Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs/f-research-v1-run-20261113-211758-tcar/`
- Artifact manifest: `audits/path-containment-manifest.md`
- Structured authority: `pipeline-state.json` in this run root (26 stages, SHA-256 bound)
- Single final PDF page policy: Neurocomputing; no explicit author length requirement; official limits to be verified at P20
- Path-containment status: passed at P0
- Allowed statuses: `pending`, `running`, `passed`, `blocked`, `superseded`. `skipped` is never valid.

| Stage | Name | Status | Evidence / artifact path | Gate result | Notes |
|---|---|---|---|---|---|
| P0 | Load guidance and create run root | passed | `audits/path-containment-manifest.md`, `pipeline-state.json` | pass | Guidance resolved; run root inside guidance directory; 26-stage ledger initialized |
| P1 | Validate guidance and load CCFA packet | passed | `audits/P1-guidance-validation.md` | pass | Strict structure + packet validation re-run; startup decision `proceed` |
| P1A | Strong-result feasibility lock | passed | `audits/strong-result-feasibility-lock.md` | pass | All three binding claims `pass`; targets remain pre-registered and unmet |
| P1B | Pre-experiment adversarial review | passed | `audits/ccfa-pre-experiment-review.md`, `audits/ccfa-pre-experiment-integrity.md`, `audits/ccfa-pre-experiment-action-ledger.md` | pass | No unresolved fatal risk; every claim explicitly marked as planned evidence |
| P2 | Runnable protocols and local environment | passed | `protocols/P2-environment-and-prototype.md`, `audits/P2-environment-check.md`, `results/p2-prototype/` | pass | One seed smoke completed in <1 s; MPS operators verified; split IDs frozen; IF coder bug found and repaired |
| P3 | Baseline-first execution | pending | — | pending | B0/B1/B2/C0 must exist before any proposed-method claim |
| P3A | Baseline-evidence stop-loss review | pending | — | pending | — |
| P4 | Full experiment campaign | pending | — | pending | — |
| P5 | Strong-result lock | pending | — | pending | — |
| P5A | Pre-draft scientific review | pending | — | pending | — |
| P6 | PAPER_OUTLINE | pending | — | pending | Local equivalent execution; ARC CLI not run |
| P7 | PAPER_DRAFT | pending | — | pending | — |
| P8 | Figures and tables | pending | — | pending | — |
| P9 | PEER_REVIEW | pending | — | pending | — |
| P10 | PAPER_REVISION | pending | — | pending | — |
| P11 | QUALITY_GATE | pending | — | pending | — |
| P12 | Reference verification | pending | — | pending | — |
| P13 | EXPORT_PUBLISH | pending | — | pending | — |
| P14 | CITATION_VERIFY | pending | — | pending | — |
| P15 | TeX/PDF compile | pending | — | pending | — |
| P16 | Journal limits | pending | — | pending | — |
| P17 | Guidance coverage audit | pending | — | pending | — |
| P18 | Figure/table audit | pending | — | pending | — |
| P19 | Final polish | pending | — | pending | — |
| P20 | Submission constraints | pending | — | pending | — |
| P21 | Final delivery | pending | — | pending | — |

## Path-Containment Audit

| Artifact class | Expected location | Status | External source | Notes |
|---|---|---|---|---|
| Protocols, audits, scripts, results, inputs, paper, figures, writing, deliverables | inside this run root | passed | none | No deliverable is placed in `auto-paper/` root, temp, Desktop, Downloads, or a global ARC artifacts directory |
| Public dataset | Zenodo 10.5281/zenodo.7213796, local frozen copy supplied at run time | passed | external, CC BY 4.0 | `inputs/frozen-identities.json` records SHA-256 of the four streams and of validation/test query arrays; raw `.npz` is not uploaded |
| Reference code | user's `ZtL-sysu/gnn2snn` archive, local predecessor `dependencies/` | passed | external, no blanket license | Read-only reference; differential coder reimplemented, not copied |
| CCFA startup packet | `../ccfa-startup-packet/` (guidance directory) | passed | none | Loaded as evidence at P1/P1A |

## Page-Policy Audit

No page target is applied until the official Neurocomputing guide-for-authors is checked at P20. No default threshold is invented.

## Correction ledger

One prototype repair occurred inside P2 (IF coder T-step bug). It is recorded in `audits/P2-environment-check.md` and `LOG.md`; no stage was reopened because the defect was found and repaired before P2's gate was declared passed. No guidance contract change was needed.
