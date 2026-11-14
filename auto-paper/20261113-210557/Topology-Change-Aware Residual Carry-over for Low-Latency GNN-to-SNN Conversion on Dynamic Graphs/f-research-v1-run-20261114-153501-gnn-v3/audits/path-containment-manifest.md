# Path-Containment Manifest (P0, contract v3)

- Guidance file: `../guidance-v3.md`; v1 (`../guidance.md`) and v2 (`../guidance-v2.md`) preserved as evidence.
- Run root: this directory, inside the guidance directory. Verified by `realpath`.
- All protocols, traces, logs, result tables, figure sources, TeX, PDF, audits, manifests and delivery bundles live here. No deliverable is written to a global ARC artifacts directory, temp, Desktop, Downloads, or the repository root.
- Public data: Zenodo `10.5281/zenodo.7213796` (CC BY 4.0); local frozen copies are supplied at run time by `CTDG_STREAM_DIR` / `CTDG_ENRON_ZIP` and are referenced by SHA-256, not redistributed.
- The v2 run root is retained as historical evidence; no v2 result is reused as a v3 claim.

**P0 gate:** guidance exists, run root is inside the guidance directory, `pipeline-state.md` and this manifest exist, 26-stage `pipeline-state.json` initialized. PASS.
