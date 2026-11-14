# Guidance Contract Amendment v3 → v4

Issued 2026-11-14 after the user's directive to deepen the research by learning from the last two years of top-venue work in this family: how those papers tell their story, how they design experiments, and how they execute them; then to upgrade the `f-guidance-builder-v1` skill with the distilled process and run a deeper experiment-and-writing cycle under `f-research-v1`.

## Trigger and diagnosis

The v3 manuscript (30 pages, 43 verified references, 25 real runs) is complete and honest, but the user judged its depth possibly insufficient against current top-venue standards. The four-agent top-venue study (`docs/top-venue-study/`) confirmed concrete depth gaps, each traced to a named reviewer objection:

| Gap | Survey evidence | v4 increment |
|---|---|---|
| LastFM null result unresolved; 5 seeds at the power floor for sub-1% effects | Du 2025 paired protocol; rliable norms | C-1 ten-seed pre-registered extension with a locked decision rule |
| Theory is a recursion, not a theorem set; no tightness validation | 2024–26 conversion-theory standard (explicit assumptions, classified results); ISC has no measured-vs-bound curve | C-2 theorems T1–T3 + V-1 violation-rate signature + V-3/V-4 dose-responses |
| Efficiency narrative lacks the op-count formula, stratified firing rates, overhead percentage | SGNNBench convention; Spiking CenterNet stratification; CRPI overhead declaration | C-3 transparency package |
| No effect sizes or per-seed scatter; statistics above community norm but incomplete by 2026 standards | rliable (Agarwal 2021) | C-4 statistics package |
| MPEF-style multi-threshold mechanism has no control | ICML 2026 same-family work | C-5 new control C5-MT |
| Fidelity metric lacks downstream validity; no inductive stratification | TGB-era protocol expectations | C-6, C-7 |
| Robustness single-point; no temporal drift dimension | methodology survey (AUT-style drift) | C-9 |
| No carry-over trade-off analysis | CRPI Figure 4 convention | C-8 |
| CRAFT/TGB-Seq anti-memory narrative unaddressed | CTDG survey | M-1 positioning + response |
| No component-ladder figure | MPEF ablation-ladder convention | M-2 |

## What v4 changes

Experiment contract: ten seeds (41–50) across five streams and twelve method columns (60 main runs); six theory-validation experiments V-1…V-6; the C5-MT control; the transparency and stratification analysis batches; robustness upgraded to five-level sweeps with a ten-slice drift evaluation; success criteria E9–E12 added (E9 locked replication verdict; E10 theory signatures; E11 transparency thresholds; E12 C5-MT grid). Manuscript contract: positioning table and CRAFT/TGB-Seq response (M-1); component-ladder figure (M-2); energy formula with cited constants; effect-size columns; per-seed scatter; theorems with enumerated assumptions. Skill contract: `f-guidance-builder-v1` gained `references/top-venue-learning-mode.md` (L1–L6), wired into Overview, CCFA-startup, G0, G8 and the output contract.

## What does NOT change

Every binding `minimum`, `expected_strong` and `failure` condition from v1/v2/v3 is retained verbatim, including agreement at least 98.5 percent and retention at least 99.0 percent on the primary stream, strict dominance over the six conversion controls (now seven with C5-MT), the 20 percent trigger ceiling, the C16 narrowed claim with its recorded `d_replication: false`, and E1–E8. No number is altered, no failed run deleted, no target lowered. The v3 run root, its 25 runs, its audits and hashes remain byte-preserved evidence; v3 files are not edited by the v4 cycle. The dataset set, the local-only compute rule, the no-hardware-energy boundary and the six-section outline are unchanged.

## The locked C-1 decision rule (frozen here, before any 10-seed inspection)

Estimator: per-seed mean epsilon_k per method per stream, seeds 41–50, paired within seed. Test: paired BCa bootstrap with 4,000 resamples on the per-seed paired differences epsilon_C2 minus epsilon_M0, plus a sign-flip permutation test; multiplicity control by Benjamini–Hochberg across the five streams at q less than 0.05. Verdict mapping, evaluated once on the test window: if LastFM's paired 95 percent BCa interval excludes zero and its BH q is below 0.05, `d_replication_10seed` is true and the all-five-stream significant-reduction claim is restored; otherwise `d_replication_10seed` is false, the C16 four-stream narrowing stands, and the disclosure text is updated with the doubled-power result. No operating point, threshold, evaluation window, or stream subset may be altered after the first inspection of 10-seed test results. Selecting a more favourable configuration after seeing the verdict is p-hacking and is prohibited exactly as in C16.

## Re-acceptance

`validate_guidance.py guidance-v4.md --strict --packet ccfa-startup-packet-v4` must pass and is recorded in `validation-report.md`. `f-research-v1` records a third `reopen P0` back-edge with `contract_version: v4`, opens a new run root inside this guidance directory, and re-accepts P0 through P2 before P3. Reuse rule: v3 results are cited as prior evidence only where the applicability note states why the row is unchanged (same pipeline, same frozen identities, same teacher family); new binding claims rest on v4 runs.

## Rights note

Retained from v3: the DCGS coder, histogram calibration and affine base are independently reimplemented from published mathematics; `RIGHTS.md` grants no blanket licence; no third-party source file is copied. The C5-MT control is an original adaptation of the published MPEF mechanism, not a copy of its code.
