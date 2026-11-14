# P5A Pre-Draft Scientific Review (ccf-paper-reviewer, scientific mode)

Reviewed the clean evidence dossier: the v3 bound check with a real measured `A_k`, the five-stream main matrix, eleven controls/ablations, T/spike/error-decomposition/architecture/calibration/robustness sweeps, paired bootstrap with BH correction, and the rights-clean independent reimplementation of DCGS.

- **Novelty**: adequate with positioning. A converted GNN on an evolving graph, with an explicit cross-snapshot increment `R(A_k-A_{k-1})H W`, is distinct from directly trained spiking dynamic-graph models (SpikeNet, Dy-SIGN, continuous spiking GNNs) and from cross-step conversion in control/generation (CRPI, MPEF). Confidence moderate pending a full database sweep.
- **Soundness**: `A_k` is now genuinely constructed and `||Delta A_k||` logged; A5 removes aggregation as a falsifying ablation; the DCGS coder is independently reimplemented from published mathematics.
- **Evidence**: 25 test runs, five streams, five seeds, all top-venue experiment categories, per-seed values, traces and figures.
- **Reproducibility**: public Zenodo data, frozen hashes, code in run root, no copied third-party source.
- **Claim scope**: conversion fidelity, not predictive SOTA; no energy claim; non-blind IDs disclosed.

Concerns requiring disclosure (all satisfied in `main.tex`): discrete-memory dominance of absolute MRR, agreement saturation, stream-dependent effect sizes, non-monotone relative dose-response, and the visibility of the two versioned contract amendments. No unresolved fatal soundness, novelty, evidence or reproducibility concern. **P5A pass.**
