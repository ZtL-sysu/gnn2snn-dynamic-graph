# Final Audit Note (P21)

## Delivered

`paper/main.tex`, `paper/main.pdf` (14 pages, compiled from the exact delivered TeX), `paper/references.bib`, `paper/highlights.txt`, four vector figures with PNG mirrors, `results/` (15 raw test runs, per-query rows, per-event bound traces, aggregated statistics, auxiliary sweeps, frozen identities), `audits/` (all gate, numeric, integrity, citation, metadata and figure audits, `metrics.csv`), `writing/` (stage 16–20 equivalents), `correction-loop-state.md`, `correction-ledger.md`, `guidance-v2-amendment.md`, `experiment-traceability.md`, `pipeline-state.md`, `pipeline-state.json`, and `deliverables/manifest.json`.

## Consistency checks

- Source ↔ PDF: `main.pdf` was recompiled after the final abstract edit; no stale duplicate TeX or PDF exists in the run root.
- Bibliography ↔ citations: BibTeX ran with `unsrt`, no undefined citations; two benign warnings about simultaneous volume/number fields on two AAAI entries were reviewed and left as metadata, not errors.
- Metadata: abstract 238 words (≤250), 6 keywords (1–7), 4 highlights each ≤85 characters; numbered sections exactly 1–6; required GenAI declaration placed immediately before the reference list.
- Numbers: every value in the manuscript traces to `results/statistics/final-analysis.json` or `results/p4_runs/*.json`; no target value is presented as a measurement.
- Negative results: agreement saturation, small MOOC/Enron effect sizes, non-monotone dose-response, negative Enron bins, non-blind identifiers, and the rejected full-flush pilot are all disclosed.
- Failures preserved: C1–C9 correction cycles, five P3 gate failures, the IF-coder defect and its repair remain in the run root.
- Path containment: every deliverable is inside the run root inside the guidance directory; `deliverables/manifest.json` proves it.

## Known unresolved items (not fabricated)

- Corresponding-author email, funding and CRediT roles were not supplied; recorded as unresolved in `audits/manuscript-metadata.md`.
- Figure 1 uses a recorded local fallback rather than GPT image generation (credit cost not authorised); see `audits/P8-figure-fallback.md`.
- AutoResearchClaw CLI was not run; writing stages were executed locally from its source contracts; see `dependency-resolution.md`.
- Novelty confidence remains moderate pending a full Scopus/IEEE sweep; no novelty claim is overstated in the manuscript.
- The user has not reviewed or submitted the manuscript. This delivery is a complete first draft, not an acceptance or a submission.
