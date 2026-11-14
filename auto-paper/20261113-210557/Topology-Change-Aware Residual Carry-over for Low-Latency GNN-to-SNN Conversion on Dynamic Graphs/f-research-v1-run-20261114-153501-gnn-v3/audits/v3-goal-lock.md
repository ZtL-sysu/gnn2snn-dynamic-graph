# Contract v3 Goal Lock (relentless-goal executor)

User directive 2026-11-14 15:16 (explicit target iteration, recorded in `goal-ledger.md`): add the real GNN using the user's own `gnn2snn` conversion algorithm on dynamic graphs; run a top-venue-grade experiment matrix; produce a manuscript of at least 21 pages with a substantially expanded bibliography; follow `f-research-v1` and the relentless-goal executor strictly.

| ID | Observable success criterion | Judge | Not achieved if | Status |
|---|---|---|---|---|
| E1-E5 | retained verbatim from v2 (repository/protocol, validated guidance, P0-P21 ledger + TeX/PDF + clean recompile, all experiments done with strong result met, six-section manuscript with verified refs) | system + user | any v2 criterion fails | re-verifying on v3 artifacts |
| **E6** | a genuine normalised graph operator `A_k` is constructed from interaction history in code, and `||A_k - A_{k-1}||` is logged per event in `results/bound-check/*`; `delta_v(k)` is only a cheap trigger, never a substitute | system + code review | `A_k` never built or only a proxy is logged | pending |
| **E7** | the experiment matrix covers the top-venue SNN paradigm: T-curve, spike/firing-rate/SynOps, error decomposition, architecture and calibration ablations, robustness, six adapted conversion baselines, directly trained spiking control, bound verification, five-stream replication, paired bootstrap + BH, latency-Pareto | system + `experiment-traceability.md` | any promised row not `done` | pending |
| **E8** | compiled PDF >= 21 pages and >= 40 verified bibliography entries | system + `final-metadata-counts.json` + `reference-dedup-audit.md` | fewer pages or fewer verified refs | pending |

Stop gates: (1) achievement when E1-E8 all PASS; (2) user stop is highest priority; (3) exhausted means; (4) no deadline set. Authorization tier: **authorized** (repository writes, local writes, Conda execution, checkpoint pushes); extra-credit image generation and ARC CLI with credentials are outside the list and are recorded as fallbacks.
