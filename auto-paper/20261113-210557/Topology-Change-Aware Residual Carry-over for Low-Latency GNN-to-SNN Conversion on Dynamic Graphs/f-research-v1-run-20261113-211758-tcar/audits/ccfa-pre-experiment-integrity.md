# CCFA Pre-Experiment Integrity Audit (P1B, claim-audit mode)

Executed per the `ccf-integrity-auditor` specification read read-only from `/Users/xhf/.codex/skills/ccf-integrity-auditor/SKILL.md`. Scope: claim-support and result-to-claim consistency **for planned claims only**. No numeric audit of results is possible yet because there are no results.

## Claim ledger — every claim is PLANNED EVIDENCE, never REPORTED EVIDENCE

| Claim | Status | Planned support | Overstatement risk | Required action before it may become a reported claim |
|---|---|---|---|---|
| C-1 conversion error accumulates with a topology-change term | `planned` | bound (1), A3/A5/A4, per-event instrumentation | high if presented as an established theorem | measure `rho`, define `A_k`, verify the inequality at P4 |
| C-2 TCAR improves `agreement@K` at small T | `planned` | C0-C4 controls, A1/A2, 5 seeds, paired bootstrap | high if smoke numbers are cited | real trained teacher at P3; full P4 matrix; P5 lock |
| C-3 recomputation cost is event-bound | `planned` | A1 vs M0, S2 gamma sweep | medium | real trigger-rate accounting at P4 |
| C-4 advantage is topology-driven | `planned` | A4 frozen-topology control | medium | frozen-topology run at P4 |
| S-1 teacher is a meaningful target | `planned` | teacher vs B1/B2 on validation | high if skipped | P3 gate |
| S-2 three-stream replication | `planned` | R1-R3 | medium | P4 |
| S-3 absolute MRR is context only | `planned framing` | published literature rows clearly labelled | medium | P12/P14 verification |

## Numeric and unit consistency (pre-data)

- Metric directions are declared in `evaluation-protocol.md`: `agreement@K` higher, MRR/AP retention higher, logit MSE/KL lower, recalibration rate lower, bound-violation rate lower.
- Units are declared: fractions for agreement/retention/rates, norm units for `epsilon_k`, counts for graded events and recalibrations, milliseconds for local latency. Percentages and fractions must not be mixed in `metrics.csv`.
- The P2 smoke numbers are explicitly labelled `coverage: smoke/2000-events` and carry a note that they are NOT scientific results. They are excluded from the manuscript and from the formal `metrics.csv` at collaboration checkpoints.
- Prior-range numbers quoted in the guidance (99.28–99.98%, 99.55±0.16%) are attributed to the user's static-graph archive and marked as **prior ranges from a different project**, not this project's measurements.

## Prohibited patterns checked

No placeholder citation, no fabricated DOI, no invented baseline result, no target value presented as a measurement, no planned claim phrased as a finding. `observed_finding` remains `unresolved_until_evidence` in `audits/P1-guidance-validation.md`.

## P1B integrity verdict

Every claim is marked as planned evidence; no unsupported item was repaired by invention. **Claim-audit pass.** A real `numeric-audit` is scheduled for P3A after baselines exist, and a `full` audit for P5A/P9 after results exist.
