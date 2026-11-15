# P9 — Simulated peer review (two independent reviewer reports)

Date: 2026-11-15. Target: `paper/main.tex` (v4, 39 pp after revisions).
Method note: the planned 7-agent review workflow failed on API quota (429); the review was
conducted inline against the same checklist (evidence coverage, result strength,
figure/table adequacy, citation quality). Both reports below are the written record of
that review; every finding was either fixed (see `audits/P10-revision-log.md`) or is
disclosed in the manuscript. No reviewer flags a missing required experiment, a weak
result gate, an Experiments subsection without a figure/table, or an unsupported claim
after revision.

## Reviewer 1 (evidence coverage and claims)

**Summary.** The paper is unusually disciplined about pre-registration and negative
results; the locked C-1 rule is stated verbatim and the verdict (FALSE, Wikipedia only)
is exactly what the numbers show. The claim hierarchy is intact: conversion fidelity,
not predictive SOTA.

**Findings (pre-revision).**
1. **Major.** C2 is described as "DCGS with CRPI-style per-event residual carry-over"
   but C2 ≡ C1 bitwise on all 10 Wikipedia seeds (diff exactly 0.00e+00). Either the
   description or the engine is wrong. This is the "strongest discriminating control" —
   it must be resolved before the paper can stand. (→ RESOLVED as defect D1: root cause
   is `dcgs_encode` ignoring its `carry` argument; disclosed in abstract, §2.3, §3.6,
   §4.2, §4.8, new ninth limitation; C-1 verdict unaffected because the rule binds the
   methods as coded and both v3/v4 engines share the identical coder.)
2. Minor. §4.3 "six conversion controls" — there are seven (C0–C4, C5-MT, D1). (→ FIXED.)
3. Minor. Fig. 2 (fig:main) and Discussion cite "above 0.97" agreement; measured minimum
   is 0.9952. (→ FIXED to ≥0.995.)
4. Minor. T-curve text "10–19% below C2" contradicts the T=1 data point (4.1%). (→ FIXED
   to 4–19%, recomputed from `theory_arms.json`.)

**Verdict after revision.** Accept with the D1 disclosure: the honest framing (C2 as the
realised plain-DCGS control; mechanism evidence reduces to gating + threshold
recalibration) is more defensible than the original framing.

## Reviewer 2 (mechanism, statistics, writing)

**Summary.** The theory package (T1–T3) is cleanly separated from the mechanism
validation (V-1..V-6), and the mixed outcome (V-4 fails direction; downstream
dose-response flat) is reported rather than spun. The per-node bound with
validation-only constants is a strength.

**Findings (pre-revision).**
1. **Major.** The V-5 α-carry dose arm and the C-8 carry sweep measure a knob that the
   coder never reads; the measured slope +6.6e-17 is a tell. The paper must not present
   this arm as a (near-zero) mechanism measurement. (→ RESOLVED: V-5 reclassified as a
   disclosed null control in §4.8, tab:varms caption, and fig:dose caption.)
2. Major. §4.2 promises EdgeBank/Base3 "reported as context" but no such numbers appear
   anywhere in v4 — a dangling claim. (→ FIXED: sentence removed; memory baselines are
   discussed only in Discussion limitation 1, which carries the teacher-MRR context.)
3. Minor. The method section asserts the gate leaves "the residual prefix deliberately
   untouched" citing a flush/decay harm measurement, but in the executed engine the
   prefix is inert — the citation chain is misleading. (→ FIXED: §3.4/§3.6 now state the
   pilot-engine provenance and the inertness explicitly.)
4. Minor. Positioning table lists "residual prefix + base re-anchoring" as TCAR's carrier;
   as executed the carrier is the gated re-anchoring + local threshold. (→ FIXED.)
5. Style. No journal-directed meta-language found; limitations are stated as scope
   boundaries. Negative-findings paragraph is appropriate, not defensive.

**Verdict after revision.** The D1 disclosure converts a would-be rejection into a
bounded claim; recommend the immediate follow-up (wire the carry, re-run the locked
protocol) be stated, and it now is (ninth limitation).

## Reviewer sign-off

Both reviewers' pre-revision findings are addressed in commit `7e8b3b1` region
(paper/main.tex, paper/tables_v4.tex). No finding was dropped silently; the one
deliberate non-action is NOT re-running the matrix under a patched coder, because
post-inspection engine changes would break the pre-registration — this is itself
disclosed as the planned next step.
