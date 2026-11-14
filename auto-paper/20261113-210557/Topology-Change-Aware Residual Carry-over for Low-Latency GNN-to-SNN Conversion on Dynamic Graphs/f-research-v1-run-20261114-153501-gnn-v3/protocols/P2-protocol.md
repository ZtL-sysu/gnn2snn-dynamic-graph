# P2 Environment and Protocol (contract v3)

- Python `/Users/xhf/miniconda3/bin/python` (3.14.6), numpy 2.x, torch 2.13.0 with MPS available, no CUDA. Probe recorded in `audits/P2-environment-check.md`.
- Environment variables: `CTDG_STREAM_DIR` (four frozen `.npz` streams), `CTDG_ENRON_ZIP` (Zenodo `enron.zip`), `V3_QUICK`, `V3_WINDOW`.
- `scripts/gnn_campaign.py` phases: `train` (graph state + histogram calibration + readout), `main` (5 streams x 5 seeds x 11 methods), `aux` (T/arch/calibration/robustness/aggregator/bound sweeps), `all`.
- Real GNN operator: `build_graph_state` constructs a row-normalised `1/sqrt(d_u d_c)` 8-slot local adjacency `A_k` per event from the interaction history and logs `||A_k-A_{k-1}||`.
- Conversion: `dcgs_encode` implements `e_t = t(a_t-a_{t-1})` with an 8-level signed ladder, telescoping decode, zero-latch and bias-once; `calibrate` implements the 512-bin q=0.999 two-pass label-free histogram; `evaluate` performs layer-wise ReLU→DCGS replacement and TCAR-gated static-base re-anchoring.
- No remote compute, no installation, no credential.
