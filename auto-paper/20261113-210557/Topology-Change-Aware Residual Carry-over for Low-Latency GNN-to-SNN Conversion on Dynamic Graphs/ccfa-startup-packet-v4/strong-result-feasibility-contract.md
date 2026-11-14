# Strong-Result Feasibility Contract — contract v4

Machine-checkable index: `feasibility-contract.json` (schema_version 1, decision `proceed`). This Markdown is the substantive contract; the JSON binds claims to it and hash-binds the seven startup artifacts.

## Claim CL1 (C4v): ten-seed pre-registered replication

- Claim: the paired difference `ε_C2 − ε_M0` is positive with a paired 95% BCa confidence interval excluding zero after BH correction on **all five streams** at 10 seeds; if and only if this holds, the v3 all-five-stream significance claim is restored; otherwise the C16 four-stream narrowing stands with updated disclosure.
- Mechanism: gated re-anchoring suppresses the topology term of the event-axis error recursion.
- Assumptions: frozen pipeline/query IDs; seeds change only random inits; paired design.
- Falsifying ablation: A2 (remove carry-over) closes the gap to C2 — isolates the carried-residual component of the effect.
- Dataset/split: five Zenodo streams; chronological 70/15/15; frozen identities (SHA-256 at P2 of the v4 run).
- Metrics: mean per-event ε_k (lower better) primary; agreement@K secondary.
- minimum: 10-seed paired point estimate positive on ≥ 4 streams (the v3 direction replicates).
- expected_strong: locked rule satisfied on all five streams (`d_replication_10seed: true`).
- failure: point estimate ≤ 0 on any stream at 10 seeds, or the decision-rule machinery itself cannot be executed as written.
- Baselines: simple B0 teacher; strong C2 (CRPI-style); matched A1 (oracle cost).
- Implementation path: v4 engine extends `gnn_campaign.py`; 5 additional teacher trains (16 s each measured).
- Prototype check: one new seed (46) end-to-end smoke in the v4 run root before the full grid.
- Calibration evidence: v3 measured per-seed means + variances (results/aggregated.json) justify 10-seed power (sub-1% effects need 8–10 paired seeds per Du 2025).
- Test isolation: the locked rule is evaluated once on test queries; no operating-point tuning after inspection.
- Stop-and-return: if the v4 engine cannot reproduce v3's 5-seed numbers for seeds 41–45 within numerical tolerance, return to P2 before any 10-seed claim.

## Claim CL2 (C5v): theory package T1–T3 with signature validation

- Claim: T1 (per-event coder error identity), T2 (spectral-norm network bound with an explicit topology term `L_A‖ΔA_k‖‖s_{k−1}‖`), T3 (steady-state bound with ρ < 1 sufficient condition and the carry-over trade) are stated with enumerated assumptions and supported by V-1…V-6; V-1 violation rate ≤ 5% with constants estimated on validation only.
- Mechanism: see idea card V4-2.
- Assumptions: A1–A9 (v3) plus bounded pre-activations, row-normalised `A_k`, frozen event order, sub-Gaussian `η_k` for T3's concentration (T3 stated without concentration if T4 is dropped).
- Falsifying ablation: V-3 synthetic edge insert/delete sweep — the topology-term slope must be positive and match `L_A‖s‖` within an order of magnitude.
- Dataset/split: same streams; validation window for constant estimation; test window for the single reported violation rate.
- Metrics: violation rate (lower), tightness ratio distribution (reported), topology slope (positive).
- minimum: theorems stated with assumptions; V-1 computed and reported regardless of level.
- expected_strong: violation rate ≤ 5%, positive topology slope with CI excluding 0, V-4 ε_∞ direction consistent with 1/(1−ρ).
- failure: violation rate > 20% (bound useless as stated) → theorem assumptions revised and re-registered, or theory demoted to conjecture with the evidence package intact.
- Baselines: structural template ISC (CVPR 2025); no numerical baseline needed.
- Implementation path: analysis scripts over existing per-event traces (`results/bound-check/*` extended in v4).
- Prototype check: V-6 single-site identity check (T1 exactness) runs before the paper draft.
- Calibration evidence: constants from validation histograms (`L_A` from measured norms, `c` from T-sweep intercept, `η̄` from coder residual trace).
- Test isolation: one locked evaluation of the violation rate on the test window.
- Stop-and-return: if V-6 falsifies T1's identity, T1 is removed and the theory package reopens at the mechanism stage.

## Claim CL3 (C6v + C7v): efficiency and statistics transparency

- Claim: full op-count energy table with cited constants; 3-level firing-rate stratification; TCAR overhead ≤ 2% of per-event converted ops; paired Cohen's d + probability of improvement + per-seed scatter on every headline comparison.
- Mechanism: attribution/measurement upgrade (no new mechanism).
- Assumptions: op counts follow the documented per-event complexity; constants from Horowitz 2014 (45 nm FP32) with the Yan 2024 caveat.
- Falsifying ablation: re-deriving any table cell from raw traces must reproduce the cell (scripted check).
- Dataset/split: same.
- Metrics: energy/event proxy (lower), overhead % (lower), |d| with CI (reported).
- minimum: table present, constants cited, d reported on main rows.
- expected_strong: overhead ≤ 2% (v3 trigger rates 3.8–9.8% × single-re-anchor cost support ≤ 2%; measured value reported), all headline rows carry d + PoI.
- failure: overhead > 5% at the selected operating point → the cost claim narrows and the ceiling breach is disclosed.
- Baselines: v3 SynOps row retained; SGNNBench formula as convention reference.
- Implementation path: analysis scripts over v4 traces; no retraining.
- Prototype check: one method's energy row recomputed by hand matches the script.
- Calibration evidence: v3 cost rows.
- Test isolation: not applicable (accounting).
- Stop-and-return: if op counts cannot be derived from the instrumented traces, the energy table is replaced by a complexity-analysis table and the limitation disclosed.

## Claim CL4 (C8v): MPEF-style multi-threshold control

- Claim: C5-MT (multi-threshold IF with inter-event error feedback, n = 4 levels) is implemented faithfully and evaluated on the full 10-seed grid; M0 retains strictly lowest mean ε_k among conversion controls; the margin over C5-MT is reported per stream.
- Mechanism: multi-level spikes raise per-step expressiveness; error feedback reuses residual potential across events (MPEF adapted to graph layers).
- Assumptions: same calibration pipeline; thresholds from the same label-free histogram.
- Falsifying ablation: n/a — C5-MT is itself the discriminating control; its victory would falsify strict dominance and trigger the pre-authorized scope narrowing.
- Dataset/split: same.
- Metrics: mean ε_k (lower), graded events/event (cost parity check ±25%).
- minimum: C5-MT runs on ≥ 1 stream × 3 seeds with per-seed artifacts (feasibility evidence) even under the demotion fallback.
- expected_strong: full grid; M0 strictly lowest with paired test vs C5-MT reported.
- failure: C5-MT strictly lower than M0 on ≥ 3 streams → dominance claim narrowed to single-threshold differential controls; narrowing disclosed.
- Baselines/controls: C2 strongest single-threshold differential control.
- Implementation path: new decode path in the v4 engine (contained; reuses calibration and evaluation harness).
- Prototype check: C5-MT smoke on Wikipedia seed 41 with finite thresholds before grid release.
- Calibration evidence: histogram thresholds exist from the v3 pipeline.
- Test isolation: single locked grid evaluation.
- Stop-and-return: if the faithful adaptation exceeds 90 minutes of implementation or fails its smoke twice, execute the pre-authorized demotion (literature-positioned + failed-attempt evidence).

## Budget envelope (v4 total)

10 seeds; ≤ 6 additional runtime hours beyond v3's consumed budget; ≤ 24 search trials retained; ≤ 16 GiB; ≤ 100k parameters; 60 main runs + ~20 analysis runs. Exhaustion rule: analysis increments (C-3, C-4, C-6, C-7, C-9, C-10) are droppable in reverse priority order C-10 → C-9 → C-7 → C-6 after recording the drop; C-1, C-2, C-5, C-8 are not droppable.
