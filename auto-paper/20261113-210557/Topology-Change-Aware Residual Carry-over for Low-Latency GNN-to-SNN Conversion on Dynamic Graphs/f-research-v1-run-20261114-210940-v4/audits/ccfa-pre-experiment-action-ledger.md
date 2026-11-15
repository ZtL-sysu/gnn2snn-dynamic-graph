# P1B Concern-to-Action Ledger (contract v4)

| # | Concern (source) | Action | Owner stage | Status |
|---|---|---|---|---|
| A1 | Survey citations may be hallucinated (red-team F7) | Route all new citations through P12/P14 verification; drop unverifiable items; keep `citation-verification-log.md` current | P12/P14 | open |
| A2 | v3 evidence could be mutated by v4 tooling (F8) | Hash-check script compares v3 deliverable hashes before v4 P21; v3 root is read-only for v4 | P21 | open |
| A3 | C5-MT implementation may exceed budget (F3) | Time-box 90 min; smoke gate; pre-authorized demotion with failed-attempt evidence | P3–P4 | open |
| A4 | Theory constants could be test-fitted (F2) | Estimation protocol restricted to validation window; recorded in analysis script header | P4 | open |
| A5 | C-1 rule must not be edited after inspection (contract) | Decision-rule text frozen in amendment; diff-check in analysis script asserts rule text hash | P4/P5 | open |
| A6 | Downstream validity is stratification, not fresh task (review deduction) | Report as scope boundary; do not overstate as predictive validity | P6–P7 | open |
| A7 | Energy constants misread as measurement (F6) | Manuscript text mandated in guidance constraints; audit at P18 | P18 | open |
| A8 | Seed-46 reproduction precondition (CL1 stop-return) | Run v3-config row for seed 46 in v4 engine and compare against v3 distributional ranges before grid release | P2/P3 | open |
