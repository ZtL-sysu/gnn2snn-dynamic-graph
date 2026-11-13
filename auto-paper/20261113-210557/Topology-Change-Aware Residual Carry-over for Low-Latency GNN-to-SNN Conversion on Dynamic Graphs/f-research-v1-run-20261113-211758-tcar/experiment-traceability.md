# Experiment Traceability

Updated before and after each batch. Statuses: `pending`, `done`, `infeasible-with-evidence`, `failed-preserved`. A row is `done` only when its config hash, seed, command, hardware profile, raw metrics and completion marker exist in `results/`.

| Guidance requirement | Row ID | Required artifact | Minimum success check | Strong success check | Planned figure/table | Must appear in paper? | Status |
|---|---|---|---|---|---|---|---|
| Datasets / frozen splits | D0 | `inputs/frozen-identities.json` | SHA-256 of four streams and query arrays | all three used streams verified and hash-matched | dataset/split table | yes | done (P2) |
| Environment / prototype | P2-SMOKE | `results/p2-prototype/*` | one seed end-to-end <=30 min | code path + instrumentation + operator probe | none (not a result) | no | done (P2, labelled smoke) |
| ANN teacher oracle | B0 | `results/p3_b0/*` | trained teacher with validation MRR | beats B1/B2 on validation | baseline table | yes | pending |
| Simple baseline | B1 | `results/p3_b1/*` | EdgeBank measured | per-seed values with units | baseline table | yes | pending |
| Simple baseline | B2 | `results/p3_b2/*` | Base3 k=10 measured | per-seed values with units | baseline table | yes | pending |
| Matched internal control | C0 | `results/p3_c0/*` | hard-reset IF on the same teacher | 5 seeds | baseline table | yes | pending |
| Calibration control | C1 | `results/p4_c1/*` | SNNC-AP-light reproduced | 5 seeds | baseline table | yes | pending |
| Coder-family control | C2 | `results/p4_c2/*` | DCGS graded differential coder | 5 seeds | baseline table | yes | pending |
| Low-latency conversion control | C3 | `results/p4_c3/*` | QCFS/FTBC clipped conversion | 5 seeds | baseline table | yes | pending |
| Strongest discriminator | C4 | `results/p4_c4/*` | CRPI-style global carry-over | 5 seeds, matched recomputation budget | baseline table | yes | pending |
| Main method | M0 | `results/p4_m0/*` | TCAR full | strong target met | agreement curve | yes | pending |
| Ablations 1-6 | A1-A6 | `results/p4_ablations/*` | all six rows done | each isolates its named term, BH corrected | ablation table | yes | pending |
| Directly trained control | D1 | `results/p4_d1/*` | matched-size spiking encoder | 5 seeds | baseline table | yes | pending |
| T sweep | S1 | `results/p4_s1/*` | T in {1,2,4,8} | latency/fidelity frontier | T-sweep plot | yes | pending |
| gamma sweep | S2 | `results/p4_s2/*` | <=6 gamma values | cost/accuracy Pareto | Pareto plot | yes | pending |
| Three-stream replication | R1-R3 | `results/p4_r*/*` | primary + one replication | three streams, consistent direction | replication table | yes | pending |
| Window-length robustness | K1-K3 | `results/p4_k*/*` | K in {1k, 5k, 10k} | monotone trend | agreement curve | yes | pending |
| Bound instrumentation | BOUND | `results/bound-check/*` | per-event `epsilon_k`, `||ΔA||`, `delta_v(k)` | no bound violation, monotone dose-response | dose-response panel | yes | pending |
| Statistical checks | STAT | `results/statistics/*` | 5 seeds, paired bootstrap | BH-corrected CIs exclude 0 | uncertainty bands | yes | pending |
| Cost accounting | COST | `results/cost/*` | recalibration rate measured | <=20% with no accuracy loss | cost table and Pareto | yes | pending |

No row above is `done` from the P2 smoke run. The smoke row is explicitly labelled `coverage: smoke/2000-events` and is excluded from the manuscript and from the formal `metrics.csv`.
