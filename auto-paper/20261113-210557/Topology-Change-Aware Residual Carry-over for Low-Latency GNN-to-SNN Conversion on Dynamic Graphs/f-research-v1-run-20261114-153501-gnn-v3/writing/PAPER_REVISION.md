# P10 PAPER_REVISION (contract v3)

| Concern | Action | Location | Factual check |
|---|---|---|---|
| no real GNN in v2 | rebuild with `A_k`, L-layer residual GCN, A5 ablation | §3.1--3.2, §4.7 | `build_graph_state` logs `||Delta A_k||` |
| DCGS rights | independent reimplementation from published mathematics; cite ICML 2025 DCGS | §2.2, §3.3, Data availability | no copied source file |
| thin experiment matrix | add T/spike/error-decomp/arch/calib/robustness/bound/Pareto | §4.4--4.10 | all rows `done` |
| 14 pages / 18 refs | expand to >=21 pages with substantive content; 43 verified references | whole manuscript | `final-metadata-counts.json` |
| absolute MRR context | explicit context-only framing | Abstract, §1, §4.3, §5 | values from `validation_mrr_v3.json` |
| saturated agreement | name `epsilon_k` as discriminating metric | §4.3, §5 | bootstrap CI table |
| contract amendments visible | preserve v1/v2/v3 and publish amendments | repository | `guidance-v3-amendment.md` |

Facts, equations, numbers, citation keys and terminology preserved; scope conditions made more explicit, not weaker. Whole-paper narrative re-read after edits; Results and Discussion retain distinct roles.
