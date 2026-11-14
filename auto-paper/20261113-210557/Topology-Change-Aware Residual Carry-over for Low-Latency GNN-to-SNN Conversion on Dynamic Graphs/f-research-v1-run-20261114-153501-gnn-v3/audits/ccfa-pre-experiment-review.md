# CCFA Pre-Experiment Adversarial Review (P1B, standard mode)

Inputs: `../guidance-v3.md`, `../guidance-v3-amendment.md`, the v3 literature map, `../ccfa-startup-packet-v3/*`, `audits/P1-guidance-validation.md`.

| Dimension | Level | Basis |
|---|---|---|
| Readiness | 6.8/10 | real GNN operator + DCGS conversion family now matches the title; top-venue matrix pre-registered; novelty confidence moderate |
| Development potential | 8.0/10 | the cross-snapshot increment has a concrete derivation from the user's own archive; five streams + full ablation family |
| Confidence | medium | DOI/arXiv verification in progress; no Scopus sweep; M1-only compute |

Fatal risks and repairs: (R1) DCGS coder is third-party with no blanket license → independent reimplementation from published mathematics, upstream ICML 2025 cited, no source file copied. (R2) `A_k` must be measurable, not a proxy → `build_graph_state` logs `||A_k-A_{k-1}||` per event (E6). (R3) discrete edge memory dominates absolute MRR → context-only framing retained from v2. (R4) argmax agreement saturates → `epsilon_k` strict dominance + bootstrap/BH retained. (R5) contract changed twice in a result-driven way → v1/v2/v3 all preserved, amendments public, v3 reopens P0 with a recorded back-edge. (R6) 21 pages must be substantive → derivations, complete matrices and extended analysis inside the six sections, no padding appendix.

No unresolved fatal soundness, novelty, feasibility or claim-support risk. **P1B pass.**
