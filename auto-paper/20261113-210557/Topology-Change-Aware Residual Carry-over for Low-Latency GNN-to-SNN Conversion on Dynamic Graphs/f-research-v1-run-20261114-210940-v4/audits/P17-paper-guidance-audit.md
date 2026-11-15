# P17 — Paper vs guidance-v4 coverage audit

Date: 2026-11-15. Guidance: `guidance-v4.md` (+ `guidance-v4-amendment.md`). Paper: `paper/main.tex` (40 pp).

## Traceability checklist (guidance table, row by row)

| Guidance requirement | Status | Where |
|---|---|---|
| Directly public datasets (5 streams, hashed, licensed) | COVERED | §4.1; frozen SHA-256 at P2 (`audits/` + dataset-access-log.md); Zenodo 10.5281/zenodo.7213796, CC BY 4.0. |
| Ten-seed replication + locked rule executed once | COVERED | §4.1 quotes the rule verbatim; §4.4 records `d_replication_10seed`=FALSE; per-seed scatter fig:stats/fig:main. 50 main runs (5 streams × 10 seeds × 12 methods per run) + latency phase; the guidance's "60 runs" counts B0 as a separate context row — B0 is computed inside every run as the teacher row. |
| Theory package T1–T3 + V-1..V-6 | COVERED | §3.8 theorems with assumptions A1–A6; §4.8 arms; V-1 subsumed into §4.9 (locked single-pass estimation). |
| Efficiency transparency | COVERED | §3.10 + §4.13 op-count energy with cited constants (horowitz2014, zhang2025sgnnbench); firing-rate strata fig:strata; overhead 2.748% disclosed against the 2% bar (not lowered). |
| Statistical completeness (d_z, PoI on headline rows) | COVERED | §4.4 + tab:stats; fig:stats forest plot; macros \DzWikipedia, \PoIWikipedia. |
| New control C5-MT on full grid | COVERED | §3.9 + main matrix column; §4.3 margin reported; no demotion triggered. |
| Carry-over trade (α curve) | COVERED-WITH-DISCLOSURE | §4.8 + limitation 9: the α curve is computed but null by construction — the executed coder does not consume the carried prefix (defect D1). Knee "identified either way": no knee exists because the dose is inert; reported as such rather than invented. |
| Downstream + inductive validity | COVERED (negative result) | §4.11 flat dose-response reported; §4.12 strata; C-7 gap ≈ 0. |
| Robustness and drift | COVERED | §4.10 five-level sweeps + ten-slice drift. |
| Citation integrity | COVERED | `audits/P12-reference-dedup-audit.md`, `audits/P14-citation-verify.md`. |
| Guidance coverage | THIS FILE | — |

## Must-run batches

- Batch 1 (main matrix): DONE — 50 runs + seed-46 smoke precondition + v3-reproduction tolerance check (passed at P3A).
- Batch 2 (theory validation): DONE — V-1..V-6 in `results/theory/theory_arms.json`; V-6 toy PASS.
- Batch 3 (transparency/stratification): DONE — energy derivation, C-6..C-10, robustness, drift.
- Runtime envelope: within the 12 h budget (main matrix ≈ 3 h; total ≈ 6 h class).

## Binding constraint compliance (Neurocomputing, retained verbatim from v1)

- Abstract ≤ 250 words: **248** (rewritten 2026-11-15; previously 449 — non-compliant, now fixed).
- Keywords 1–7: **7**.
- Highlights 3–5, ≤ 85 chars: **5 highlights, 79–85 chars each** (rewritten; previously up to 270 chars).
- GenAI declaration before references: §Declaration … line 517, bibliography at line ~529. PASS.
- Data/code statement: §Data and code availability. PASS.
- No official page limit; user ≥ 21-page requirement: **40 pages**. PASS.
- No hardware energy claim: energy is op-count convention only, stated twice. PASS.
- Negative-result disclosures mandatory: non-replication, MOOC direction-negative, V-4 failure, flat downstream, overhead>2%, D1 inert carry — all in abstract + Discussion. PASS.

## Outcome deviations from `expected_strong` (reported, not lowered)

1. Strict dominance on each stream — not met on MOOC (C1/C2 lower); reported in §4.3.
2. C-1 verdict FALSE (Wikipedia only).
3. V-4 consistency with 1/(1−ρ) — direction failed.
4. Downstream positive dose-response — flat on all five streams.
5. TCAR overhead ≤ 2% — measured 2.748%.

Per the claim-adjustment rule these outcomes stand at exact resolution; no target was edited after inspection (the locked C-1 text is byte-identical to the contract).

## B1/B2 treatment

Guidance-v4's Baselines section lists B1/B2 as retained; the must-run matrix lists only "B0 context row, C0–C5-MT, D1, M0, A1, A2, A3, A5". B1/B2 are therefore **not matrix rows**; their role (exact edge memory as a strong competitor) is covered by the teacher-MRR context in Discussion limitation 1 and by the saturation analysis in limitation 2. The earlier dangling sentence promising B1/B2 numbers was removed in the P10 revision. Recorded here so the coverage decision is explicit rather than silent.
