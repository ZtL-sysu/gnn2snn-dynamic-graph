# Claim–Evidence Matrix (design mode)

Owner: `ccf-experiment-designer` spec at `/Users/xhf/.codex/skills/ccf-experiment-designer/SKILL.md`. All cells are **planned evidence**, never reported results. Every main claim maps to a reviewer question, dataset/workload, baselines, metric, ablation, robustness test, and an execution priority. Result values are absent by design.

## Main claims

| ID | Claim (planned) | Reviewer question it answers | Dataset / workload | Primary metric | Simple baseline | Strongest feasible domain/method baseline | Matched internal control | Falsifying ablation | Robustness / efficiency | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| C-1 | Conversion error on a CTDG accumulates along the event axis and contains a term proportional to the change in the neighbor-aggregation operator `‖ΔA_k‖` | "Why is this not just static-graph conversion with more steps?" | Wikipedia primary; MOOC, Enron replication; 10k-event windows | correlation/slope of `ε_k` vs cumulative `‖ΔA_k‖`; bound (1) violation rate | rate-coded IF, hard reset (C0) | CRPI-style global carry-over (C4) | same ANN teacher, no conversion (B0) | A3 frozen static base; A4 static-graph control; A5 `‖ΔA‖` quartile stratification | vary window length K ∈ {1k, 5k, 10k}; 5 seeds; paired bootstrap | P4 highest |
| C-2 | Topology-change-gated residual carry-over (TCAR) reduces end-of-window teacher disagreement at small `T` versus hard-reset and global carry-over | "Is your gain just CRPI?" | same three streams | `agreement@K` (higher), MRR retention | C0 | C4 (global carry-over), C1 SNNC-AP-light, C2 DCGS coder, C3 QCFS/FTBC | C0 plus B0 oracle | A2 no-carry-over; A1 no-topology-gate; matched recomputation budget comparison | T ∈ {1,2,4,8}; 5 seeds; BH correction across ablations | P4 highest |
| C-3 | The event-triggered recomputation policy binds cost to topology-change events, not to total events | "Is the mechanism affordable, or just accurate because it recomputes everything?" | same three streams; full event loop instrumented | recalibration trigger rate (lower), graded events/event, ms/event on local PyTorch | A1 (recompute every event) as the upper-cost control | C4 (no recomputation) as the lower-cost control | B0 (ANN teacher inference, no events) | A1 vs M0 at matched accuracy; `gamma` sweep S2 | report parameter count, local CPU/MPS latency separately, no hardware energy claim | P4 high |
| C-4 | The advantage is driven by topology change rather than by generic temporal depth | "Would the same trick help on a static graph?" | static-graph control built from the same stream with frozen neighbor sets | interaction contrast: `(TCAR − C4)` on dynamic minus the same on frozen topology | C0 on frozen topology | C4 on frozen topology | B0 on frozen topology | A4 static-graph control | repeat with 3 different frozen-topology seeds | P4 high |

## Supporting / auxiliary claims (not repeated across the whole paper)

| ID | Claim | Evidence | Where it appears |
|---|---|---|---|
| S-1 | The ANN teacher is a meaningful conversion target | teacher beats EdgeBank/Base3 on validation; per-seed validation MRR | one paragraph in Experiments and Results |
| S-2 | Findings replicate across streams with different sizes and activity patterns | three-stream direction agreement with per-stream values | one compact table in Experiments and Results |
| S-3 | Absolute predictive accuracy is context, not the contribution | published reference rows from TGB leaderboard / HyperEvent Table III clearly labelled as literature values | one short paragraph in Discussion |

## Reviewer-question → experiment crosswalk

| Reviewer question | Required experiment ID(s) | Minimum success check | Strong success check |
|---|---|---|---|
| Is the topology term real? | C-1 rows; A3/A4/A5 | a measurable non-zero slope between `ε_k` and cumulative `‖ΔA_k‖` | monotone dose-response across quartiles, bound (1) not violated, replicated on 3 streams |
| Is TCAR better than CRPI-style carry-over? | C-2 rows; matched-budget comparison | TCAR ≥ C4 in `agreement@K` on the primary stream | TCAR > C4 with paired bootstrap 95% CI excluding 0 at equal or lower recomputation count |
| Is it low-latency? | S1 T-sweep | `agreement@K` at T=4 ≥ 95% | T=4 ≥ 98.5% with MRR retention ≥ 99% |
| Is it cheap? | C-3 rows; S2 gamma sweep | recalibration triggered on ≤50% of events | ≤20% of events, with no loss versus A1 at matched accuracy |
| Is the claim bounded? | A4 static control | TCAR advantage on frozen topology is smaller than on dynamic | advantage shrinks toward zero (CI includes 0) on frozen topology |
| Are results stable? | 5 seeds, paired bootstrap, BH | all per-seed values retained and reported | CI excludes 0 on all three main comparisons with BH correction |

## Execution queue (baseline-first)

1. P2: environment, MPS/CPU operator check, 30-minute single-seed prototype, freeze stream/test hashes.
2. P3: B0 teacher, B1 EdgeBank, B2 Base3, C0 hard-reset IF. **No proposed-method claim before these exist.**
3. P3A: numeric audit of baseline metrics (units, splits, seeds, metric direction) and idea-reviewer reassessment.
4. P4: C1–C4 conversion controls → M0 TCAR → A1–A6 ablations → S1/S2 sweeps → D1 directly trained control → R1–R3 replication.
5. P5: strong-result lock; every required row `done`; failed runs preserved.

## Traceability requirement

Every row writes to `experiment-traceability.md` before and after its batch, with config hash, seed, command, hardware profile, raw `metrics.json` / `raw_results.jsonl`, and an `END_OF_RUN_OK` or explicit failure marker. Tables and figures in the manuscript must be traceable to these raw rows; no number may appear only in prose.
