# Hardware Profile

## Local Experiment Machine

- Role: run experiments, training, evaluation, preprocessing, writing, and artifact preparation by default
- OS: macOS Darwin 24.6.0, arm64
- CPU: Apple M1, 8 logical cores (`sysctl -n hw.ncpu` = 8)
- RAM: 17,179,869,184 bytes (16 GiB), unified memory
- GPU: Apple M1 integrated GPU, 8 cores, Metal 3
- GPU memory: shared with system RAM; no discrete VRAM
- Disk free: 339,078,103,040 bytes at probe time
- CUDA: `torch.cuda.is_available() = false`, device count 0
- Apple MPS available: `true`; `recommended_device: mps`
- Conda/Python: `/Users/xhf/miniconda3/bin/python`, Python 3.14.6, torch 2.13.0
- Selected Conda environment: **not yet created**. P2 will create a project-specific environment; until then `base` is used for read-only probes. No global conda config is modified by the guidance phase.
- Key probes: `scripts/hardware_probe.py` from `f-guidance-builder-v1` was executed on 2026-11-13; raw output is transcribed in `docs/hardware-profile.md` at repository root. LaTeX toolchain `/Library/TeX/texbin/{pdflatex,xelatex,latexmk}` is installed.

## Optional Remote Compute

- Enabled only when: explicitly requested in the guidance or authorized after local feasibility fails. **Not enabled in this project.**
- Role: none. The user authorized local compute only. Historical exp-4090 attempts recorded `eligible_nodes=0` and `NO_ELIGIBLE_WORKER`; no endpoint, alias, or credential is recorded here.
- Artifact synchronization plan: not applicable; every claimed artifact will be produced under the local run root.

## Experiment Budget

- Maximum runtime per run: 20 minutes wall clock on CPU/MPS for any single seed of the main matrix; 30 minutes for the one-off baseline reproduction attempt.
- Maximum total runtime: 12 hours wall clock across the whole campaign (P3–P5).
- Maximum number of runs: 120 seed-level runs total, including failed and diagnostic runs; all are logged.
- Maximum dataset size: 15 MB per frozen event stream; Wikipedia 157,474 events (1,253,310 B npz), MOOC 411,749 events (2,821,369 B), Enron 808,719 B zip. Reddit and LastFM are optional robustness extensions and are capped at the same per-run budget.
- Maximum model size: 100,000 trainable parameters for the ANN teacher; the converted SNN reuses the same weights with no additional training.

## Measured vs Estimated

- **Measured**: all OS/CPU/RAM/GPU/torch/MPS/disk values above; Zenodo HTTP 200 direct-file access; local `.npz` shapes and dtypes loaded successfully.
- **Estimated (not yet measured)**: per-run 20 minutes, 120 runs, 12 hours. These are budget ceilings for planning, not observed runtimes. P2 prototype must verify one seed end-to-end before the budget is treated as feasible; if it fails, G5 is reopened with a scaled-down plan rather than silently exceeding the ceiling.
