# P2 Environment and Prototype Check (contract v3)

Measured: Apple M1, 8 cores, 16 GiB, MPS available, CUDA unavailable, Python 3.14.6, torch 2.13.0, ~339 GB free. `build_graph_state` produced `A_k` of shape (157474, 8) for Wikipedia with mean `||A_k-A_{k-1}|| = 0.3712`, confirming E6's operator is real and logged (not a proxy).

Prototype gate: a 30-minute single-seed end-to-end smoke must complete (graph construction, teacher calibration, DCGS conversion, evaluation, JSON artifacts) before the full matrix is released. The first smoke exposed and fixed two defects: (i) a missing output directory, (ii) an unbounded state recurrence that inflated the calibrated thresholds to ~1e20; the recurrence was corrected to use the last converted layer activation. Both the failure and the repair are preserved in the run log.

**P2 pass** once the corrected smoke completes with finite thresholds.
