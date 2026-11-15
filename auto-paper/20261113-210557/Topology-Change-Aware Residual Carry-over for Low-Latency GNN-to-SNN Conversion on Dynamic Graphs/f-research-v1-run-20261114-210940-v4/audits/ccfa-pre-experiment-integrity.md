# P1B Pre-Experiment Integrity Check (contract v4)

Date: 2026-11-14. Mode: `ccf-integrity-auditor` claim-audit over **planned** claims only.

| Planned claim | Marked as | Support status | Required action |
|---|---|---|---|
| C1v fidelity at T=4 (v3 retained) | planned evidence | mechanism + 25 completed v3 runs as prior evidence; v4 adds 35 runs | evaluate under v4 matrix; do not cite v3 numbers as v4 results |
| C2v strict dominance (v3 retained, comparator class now C0–C5-MT, D1) | planned evidence | v3 strict dominance vs 6 controls; C5-MT is new and unevaluated | paired tests must include C5-MT before any dominance sentence |
| C3v cost bound (v3 retained + overhead ≤ 2%) | planned evidence | v3 trigger rates measured; overhead percentage not yet computed | compute from v4 traces; report measured value even if above ceiling |
| C4v ten-seed replication verdict | planned evidence | decision rule locked; zero 10-seed results inspected at lock time | execute rule exactly once; record `d_replication_10seed` verbatim |
| C5v theory package | planned/planned-to-be-proven | T1–T3 stated in contract; no validation results exist | V-6 before drafting; violation rate from single locked evaluation |
| C6v–C11v transparency/statistics/validity/strata | planned evidence | instrumentation specified; no results | compute from traces; every cell traceable |

No planned evidence was promoted to reported evidence anywhere in this run root. The `d_replication: false` v3 verdict remains recorded verbatim in the v3 analysis file and is not rewritten. Verdict: no integrity violations at P1B.
