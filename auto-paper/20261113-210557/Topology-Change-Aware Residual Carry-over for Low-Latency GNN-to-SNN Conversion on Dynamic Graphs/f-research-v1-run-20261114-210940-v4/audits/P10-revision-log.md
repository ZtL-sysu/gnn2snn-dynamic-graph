# P10 — Revision log (reviewer comments → resolutions)

Date: 2026-11-15. Applies to `paper/main.tex` + `paper/tables_v4.tex` (commit `7e8b3b1`).
Every comment from `audits/P9-peer-review.md` is resolved or explicitly justified below.

| # | Reviewer | Comment | Resolution |
|---|---|---|---|
| 1 | R1 major | C2 ≡ C1 bitwise; "CRPI-style carry-over control" description wrong | Root-caused to engine (`dcgs_encode` ignores `carry`; v3 byte-identical). Disclosed as defect D1 in: abstract; §2.3 positioning paragraph; positioning table row; §3.4 TCAR paragraph; §3.6 cost-model paragraph; §3.7 (T3 discussion); §4.2 control definition; §4.6 decomposition paragraph; §4.8 V-5 reclassification; tab:varms caption; fig:dose caption; NEW ninth limitation; design-lesson paragraph. Engine left byte-identical (pre-registration integrity; evidence hashes unchanged). |
| 2 | R1 minor | "six conversion controls" | → "seven conversion controls" (C0–C4, C5-MT, D1) in §4.3. |
| 3 | R1 minor | stale "above 0.97" agreement captions | fig:main caption → "≥ 0.995 for every variant" (measured min 0.9952, lastfm A2). Discussion sentence kept (">0.97 on several streams" is true). |
| 4 | R1 minor | T-curve "10–19% below C2" | Recomputed per-T from `results/theory/theory_arms.json`: 4.1/8.7/15.3/18.4/18.5% → text now "$4$--$19\%$"; absolute endpoints verified against data (9.40e-3, 5.05e-3, 9.01e-3, 4.27e-3). |
| 5 | R2 major | V-5 / C-8 α-dose arms measure an unread knob | §4.8: V-5 reclassified as "numerically zero slope … disclosed null control"; tab:varms + fig:dose captions annotated; ninth limitation explains the zero is by construction. |
| 6 | R2 major | B1/B2 EdgeBank/Base3 dangling promise in §4.2 | Removed; §4.2 now states memory baselines are outside the 12-method matrix, discussed only in Discussion limitation 1 (which has the teacher-MRR context number). |
| 7 | R2 minor | "deliberately left untouched" prefix chain misleading | §3.4 and §3.6 now attribute the flush/decay harm to the earlier pilot engine and state the inertness explicitly. |
| 8 | R2 minor | positioning table carrier column | Now "gated base re-anchoring + local threshold (carried prefix inert: D1)". |
| 9 | both | (positive instruction) keep negative findings | Unchanged: non-replication, MOOC direction-negative, V-4 failure, flat downstream, energy overhead 2.748% > 2% bar all retained and stated at exact resolution. |

No scope language was shortened away; all revisions are description-honesty fixes, not
evidence changes. No numbers were altered except the T-curve percentage range, which was
recomputed from the locked data.
