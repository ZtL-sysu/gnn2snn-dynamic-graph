# Idea Red-Team Review — contract v4 increments

Independent red-team pass over the v4 increments (cards V4-1…V4-4 and increments C-1…C-10, M-1/M-2 from `docs/top-venue-study/gap-analysis.md`). Readiness score, development potential, confidence, fatal risks and score-change conditions are preserved separately from the v3 review; this is a revision review, not a replacement.

## Readiness

- Current readiness: **7.5/10** (v3 direction was 6.5 at startup; the delivered v3 evidence lifts the base, and the v4 increments are evidence-deepening rather than direction-changing).
- Development potential: **high** — the theory whitespace (streaming conversion with changing operator) and the violation-rate differentiator are genuinely unoccupied per the four-agent survey.
- Confidence: **moderate-high** on execution (all v4 rows are reruns/instrumentation on a pipeline that produced 25 real runs); **moderate** on novelty until the P12/P14 structured duplicate sweep.

## Fatal risks (each needs a repair or a blocking condition)

| # | Risk | Repair / blocking condition |
|---|---|---|
| F1 | Ten-seed extension still null on LastFM → story unchanged, effort "wasted" | Not fatal by construction: the locked decision rule makes either outcome a publishable, pre-registered result (restored five-stream claim or confirmed boundary case with doubled power). Blocking only if the rule itself is ambiguous — mitigated by writing the rule before any 10-seed inspection. |
| F2 | Theorem constants (`L_A, c, η̄`) fitted on test would be reviewer-fatal | Estimation protocol frozen to validation data only; test-set constants are computed once and reported; violation-rate ceiling pre-registered at 5%. |
| F3 | C5-MT implementation bloat breaks the 12 h envelope | Fallback pre-authorized: demote to literature-positioned with failed-attempt evidence (same G6 discipline as strong TGN baselines in v3). |
| F4 | New theory overclaims (e.g., ρ condition stated without proof) | Theorems limited to what the assumptions support; proofs or proof sketches in the manuscript; T1 verified exactly on a single-site toy (V-6) before the paper claims it. |
| F5 | "Depth" reads as padding (more pages, same science) | Every increment maps to a named reviewer objection from the survey (gap-analysis F1–F4 trace to survey findings); M-1/M-2 are reviewer-objection-driven, not decorative. |
| F6 | Energy formula constants (0.9/4.6 pJ) misread as measured energy | Manuscript states constants' source (Horowitz 2014, 45 nm) and the Yan 2024 capacity-matching caveat; no hardware energy claim (v3 boundary retained). |
| F7 | Survey-agent citations hallucinated | All new citations pass the P12/P14 verification pipeline; five load-bearing ones pre-verified 2026-11-14 (`citation-verification-log.md`); unverifiable items are dropped, not softened. |
| F8 | v3 evidence accidentally mutated by v4 tooling | v3 run root is byte-preserved; v4 uses a new run root; a hash-check script compares v3 deliverable hashes before v4 delivery (P21 gate). |

## Score-change conditions

- To 8.5+: C-1 executed with the locked rule and C5-MT implemented faithfully within budget.
- To ≤6: violation-rate ceiling exceeded with no assumption repair, or C5-MT defeats M0 and the dominance claim must narrow (claim-scope correction pre-authorized).
- Rejection triggers: any new binding target proposed after seeing v4 results; any v3 target weakened; use of test queries for the C-1 decision rule beyond the single locked evaluation.

## Verdict

Proceed to `claim-evidence-matrix.md` and `strong-result-feasibility-contract.md`. No increment is blocked; F1–F8 all have repairs or pre-authorized corrections.
