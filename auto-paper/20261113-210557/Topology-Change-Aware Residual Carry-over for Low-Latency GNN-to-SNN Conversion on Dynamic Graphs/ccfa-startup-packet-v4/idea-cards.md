# Idea Cards — contract v4

Restated at mechanism level from the v3 cards (unchanged core) plus the v4 deepening cards from the top-venue study. v3 cards remain authoritative for the retained claims; these cards cover the new binding increments.

## Card V4-1 (ten-seed pre-registered extension)

- **Bottleneck**: the v3 strong-result lock on all-five-stream significance failed on LastFM (paired bootstrap interval covers zero, BH q = 0.40) with 5 seeds; for sub-1% effects 5 seeds is at the power floor (Du 2025 paired-bootstrap protocol).
- **Mechanism**: more paired seeds reduce the standard error of the paired difference `ε_C2 − ε_M0`; the paired design removes stream-level variance shared across seeds.
- **Assumptions**: identical frozen pipeline and query IDs; new seeds only change teacher random init / message weights / readout init; effect direction stable across seeds.
- **Falsification**: the locked decision rule (below) fails on LastFM even at 10 seeds → the C16 narrowed claim stands, disclosure updated, no further seed escalation.
- **Contribution type**: evidence-depth upgrade restoring or confirming the replication claim.
- **Feasibility risks**: none identified; 25 additional runs measured affordable (~3 h total main matrix).

## Card V4-2 (theory package T1–T3 + validation experiments)

- **Bottleneck**: v3 ships a recursion with one proposition and self-describes as "a claim to be tested, not an unconditional theorem"; the 2024–26 conversion-theory standard is explicit assumptions + classified results (identity / minimization / recursive bound) + theory-term-mapped ablations; measured-vs-bound tightness curves are an unoccupied differentiator.
- **Mechanism**: (T1) the DCGS differential coder admits a per-event error identity with `η_k` explicit; (T2) spectral-norm recursion over the L residual GCN layers isolates `L_A‖ΔA_k‖‖s_{k−1}‖` as an independent topology term absent from every 2024–26 top-venue bound; (T3) solving the event-axis recursion under ρ < 1 gives a steady-state bound and turns the carry-over choice into a theorem-level trade (lower ε₀ at a ρ cost).
- **Assumptions**: enumerated in the contract (A1–A9 retained plus bounded pre-activations, row-normalised `A_k`, frozen event order).
- **Falsification**: V-1 violation rate above the pre-registered ceiling; V-3 topology-term slope not positive; V-4 scaling with 1/(1−ρ) absent.
- **Contribution type**: theory depth (the topology term + ρ condition are whitespace vs the surveyed literature).
- **Feasibility risks**: constants `L_A, c, η̄` estimated from validation data — estimation protocol must be pre-registered to avoid test-set fitting.

## Card V4-3 (efficiency and statistics transparency)

- **Bottleneck**: v3 reports SynOps totals and local latency without the full op-count energy formula, without firing-rate stratification, without the method's own overhead percentage, and without effect sizes — all four are 2024–26 reviewer checklist items for SNN papers.
- **Mechanism**: none new (measurement/attribution upgrade); energy accounting follows the SGNNBench convention `E = Σ_l (E_MAC·#MAC_l + E_AC·#AC_l·T·R_l)` with Horowitz 2014 45 nm constants and the Yan 2024 capacity-matching caveat.
- **Assumptions**: op counts derive from the documented per-event complexity; firing rates measured per layer per window from the same traces.
- **Falsification**: not mechanism-falsifying; binding thresholds: TCAR overhead ≤ 2% of converted-model per-event ops (calibrated on v3 measured trigger rates), energy table reproduced from raw op counts.
- **Contribution type**: evidence quality upgrade.
- **Feasibility risks**: low; pure instrumentation of existing traces.

## Card V4-4 (MPEF-style multi-threshold control C5-MT)

- **Bottleneck**: v3's six conversion controls do not include the multi-threshold neuron family introduced by MPEF (ICML 2026); reviewers from that community can question whether the TCAR advantage survives the strongest same-family mechanism.
- **Mechanism**: multi-threshold IF neurons emit multi-level spikes against n thresholds and feed inter-event membrane error forward; adapted to graph layers on top of the same calibrated teacher.
- **Assumptions**: same calibration pipeline; thresholds derived from the same label-free histogram with n = 4 levels (bounded adaptation cost).
- **Falsification**: if C5-MT attains strictly lower `ε_k` than M0 at comparable event cost, the strict-dominance claim must be narrowed to "among single-threshold differential-coding controls" — a pre-authorized claim-scope correction.
- **Contribution type**: baseline completeness.
- **Feasibility risks**: moderate (new decode path); fallback recorded — if the faithful adaptation exceeds the implementation budget, C5-MT is demoted to literature-positioned with the failed-attempt evidence preserved.
