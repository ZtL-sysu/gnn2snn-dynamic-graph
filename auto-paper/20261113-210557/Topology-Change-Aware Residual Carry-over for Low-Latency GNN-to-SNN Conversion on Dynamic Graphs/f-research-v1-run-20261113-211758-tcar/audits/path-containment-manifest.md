# Path-Containment Manifest (P0)

- Guidance file: `../guidance.md` in the parent folder `auto-paper/20261113-210557/Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs/`
- Run root: `f-research-v1-run-20261113-211758-tcar/` inside that guidance folder. Verified with `realpath` at P0: the run root is a descendant of the guidance directory.
- Subdirectories created: `audits/ results/ scripts/ paper/ protocols/ inputs/ figures/ writing/ deliverables/`.
- Structured ledger: `pipeline-state.json` initialized with the canonical 26 stages `P0, P1, P1A, P1B, P2, P3, P3A, P4, P5, P5A, P6 … P21` using `f-research-v1/scripts/pipeline_state.py --init`.
- Readable view: `pipeline-state.md`.

## Containment rules

1. Every protocol, trace, log, result table, figure source, TeX source, PDF, audit file, manifest, and delivery bundle created by this run must be under this run root.
2. The public dataset remains at its canonical Zenodo URL; a local frozen copy is supplied at run time via the `CTDG_FROZEN_STREAM` environment variable. Raw `.npz` files are excluded from the public repository by `.gitignore`; `inputs/frozen-identities.json` records their SHA-256 instead.
3. AutoResearchClaw is not installed as a CLI here. Its stage contracts are read from the local source tree, but no external artifacts directory is used and no deliverable is written outside this run root.
4. The user's `gnn2snn` archive and the local predecessor `dependencies/` are read-only references. No file from them is copied into the deliverable as if it were this project's code.
5. No credential, private dialogue, or machine-specific identity path is written into published artifacts. The prototype script takes its data path from an environment variable rather than embedding a home-directory path.

## P0 gate

Guidance file exists and is readable; run root is inside `guidance_dir`; `pipeline-state.md` and this manifest exist in the run root. **P0 pass.**
