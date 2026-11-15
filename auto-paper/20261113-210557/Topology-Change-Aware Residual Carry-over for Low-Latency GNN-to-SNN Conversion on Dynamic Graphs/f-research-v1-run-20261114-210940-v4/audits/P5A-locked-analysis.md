# P5A — Locked statistical analysis (post-matrix)

Date: 2026-11-15. Run root: `f-research-v1-run-20261114-210940-v4`.

## What this stage is

P5A executes the analysis phase on the completed 50-run main matrix + latency phase,
under the v4 locked contract (C-1 decision rule frozen 2026-11-14 before any 10-seed
result inspection; amendment sha256 `cd6926f6…` bound in `scripts/bind_contract.py`).

## Inputs executed

- `results/aggregated.json` — 50 runs (5 streams × 10 seeds 41–50 × 12 methods), latency phase re-runs merged.
- `results/latency/latency_probe.json` — per-method per-event wall time (M0 = 0.257 ms/event).
- `results/theory/theory_arms.json`, `results/theory/bound_constants.json` — validation arms + locked bound constants.
- `scripts/analyze_v4.py` — single analysis program (integrity self-checks inside).

## Locked-rule verdict (C-1, executed exactly once)

Decision rule (verbatim, frozen): per-seed mean ε_k per method per stream, seeds 41–50,
paired within seed; paired BCa bootstrap 4,000 resamples on per-seed paired differences
ε_C2 − ε_M0, plus sign-flip permutation; Benjamini–Hochberg across the five streams at q < 0.05.

Verdict `d_replication_10seed = FALSE`:

| stream | mean paired diff | BH q | Cohen d_z | direction |
|---|---|---|---|---|
| wikipedia | +4.90e-04 | 0.0391 | +1.27 | positive, significant (only one) |
| mooc | −5.05e-05 | 0.4453 | −0.25 | negative |
| enron | +3.96e-04 | 0.2376 | — | positive, ns |
| reddit | +9.59e-05 | 0.2376 | — | positive, ns |
| lastfm | +5.57e-05 | 0.4453 | — | positive, ns |

The predecessor 4-stream claim does not replicate at doubled power; the paper claim is
narrowed to exactly this resolution.

## E10 bound verification (locked constants, test traces, single pass)

Per-node bound rhs_k(u) = ρ̂·ε_prev(u) + L̂_A·topo_k + ĉ/T + η̂ with topo_k = ‖ΔA_k‖·‖s_k(u)‖
(C1/C2 always; M0 zeroed off-trigger). Violation rates ≤ 2.3% on every stream/method against
the 5% ceiling (PASS); tightness ≈ 0.62 (C1) / 0.50 (C2/M0).

## Additional analyses produced here

- Method rankings: M0 lowest ε among the 7 conversion controls on wiki/enron/reddit/lastfm; 2/12 overall on wiki/enron/lastfm behind only oracle A1; 7/12 on mooc (reported, not explained away).
- Downstream ε-stratified MRR dose-response: FLAT on all five streams (negative finding, kept).
- Robustness (5 levels × noise/dt/drop), 10-slice drift, energy op-count, strata gaps ≈ 0.
- V-arms: 5/8 directionally correct; V-4 state-decay FAILS its predicted direction (reported).

## Post-hoc defect found at this stage (disclosed, not patched)

`dcgs_encode` accepts the carried-residual argument but never consumes it (byte-identical
in the v3 and v4 engines). Consequently C2 ≡ C1 bitwise on every seed/stream, and the
α-carry dose arm (V-5) is a null control. Locked-rule impact: none — C-1 compares the
methods as coded; both engines share the identical coder so the v3→v4 comparison is
apples-to-apples. Disclosed as defect D1 in the manuscript (abstract, §2.3, §3, §4,
limitations) — see `audits/P10-revision-log.md`.

## Evidence

- `results/final-analysis-v4.json` (all statistics above; hash-bound)
- `results/aggregated.json`, `results/latency/latency_probe.json`
- `scripts/analyze_v4.py` (rerunnable; integrity block passes)
- Manuscript sections 4.1–4.13 state exactly these numbers.
