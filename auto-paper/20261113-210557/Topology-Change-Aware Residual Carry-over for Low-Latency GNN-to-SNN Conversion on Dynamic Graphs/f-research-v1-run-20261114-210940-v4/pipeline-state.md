# Pipeline State (contract v4) — readable view of pipeline-state.json

Canonical authority: `pipeline-state.json`. Contract version: v4. This file is its readable mirror; the validator checks the JSON.

| Stage | Status | Evidence |
|---|---|---|
| P0 | passed | audits/path-containment-manifest.md, pipeline-state.md |
| P1 | passed | audits/P1-guidance-validation.md |
| P1A | passed | audits/strong-result-feasibility-lock.md |
| P1B | passed | audits/ccfa-pre-experiment-review.md, audits/ccfa-pre-experiment-integrity.md, audits/ccfa-pre-experiment-action-ledger.md |
| P2 | passed | audits/P2-environment-check.md, protocols/P2-protocol.md, results/smoke/smoke_result.json, inputs/frozen-identities.json |
| P3 | passed | results/p3_teachers/teachers_v4.npy, audits/reproduction-check.json, results/smoke/smoke_result.json |
| P3A | passed | results/theory/bound_constants.json, results/theory/theory_arms.json, results/theory/v6_toy.json, protocols/bound-constants-protocol.md |
| P4 | passed | results/aggregated.json, results/latency/latency_probe.json, results/final-analysis-v4.json, results_main.log |
| P5 | passed | results/final-analysis-v4.json, audits/reproduction-check.json, audits/v3-evidence-hashes.json, results/theory/bound_constants.json |
| P5A | passed | audits/P5A-locked-analysis.md, results/final-analysis-v4.json |
| P6 | passed | paper/main.tex |
| P7 | passed | paper/main.tex |
| P8 | passed | audits/P18-figure-table-insertion-audit.md, paper/figures/fig1_framework.pdf |
| P9 | passed | audits/P9-peer-review.md |
| P10 | passed | audits/P10-revision-log.md |
| P11 | passed | audits/P11-quality-gate.md |
| P12 | passed | audits/P12-reference-dedup-audit.md, paper/references.bib |
| P13 | passed | paper/main.tex, paper/main.pdf |
| P14 | passed | audits/P14-citation-verify.md, paper/references.bib |
| P15 | passed | paper/main.pdf |
| P16 | passed | paper/main.pdf |
| P17 | passed | audits/P17-paper-guidance-audit.md |
| P18 | passed | audits/P18-figure-table-insertion-audit.md |
| P19 | passed | audits/P19-professionalism-scan.md |
| P20 | passed | paper/submission-constraints.md, paper/manuscript-metadata.md |
| P21 | passed | audits/P21-delivery-verification.md, audits/P21-delivery-manifest.json |

## P20 unresolved items (recorded per gate)

Author/affiliation/corresponding-author metadata, funding, cover letter, and
Elsevier-submission-system fields are UNRESOLVED by design — the pipeline fills no
author identities and performs no submission (human-author actions at submission time).
All other Neurocomputing constraints PASS: abstract 248 ≤ 250 words; 7 keywords;
5 highlights ≤ 85 chars; GenAI declaration and data/code statement before references;
40 pages (user floor 21).

## Final status

ALL STAGES P0–P21 PASSED (2026-11-15). Verdict of record: `d_replication_10seed = FALSE`
(Wikipedia-only significance, q=0.039; MOOC direction-negative; predecessor four-stream
claim does not replicate at doubled power). Disclosed defect D1: residual carry-over
inert in the executed DCGS coder (C2 ≡ C1 bitwise; v3 engine byte-identical). Engine and
evidence left byte-identical post-verdict; D1 repair + locked-protocol re-run is the
recorded next step.
