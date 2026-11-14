# Startup Stage Plan — contract v4 (top-venue deepening)

Issued 2026-11-14 by agent `20261114-topvenue` under the user's directive to deepen the project using the top-venue learning mode (see `docs/top-venue-study/` and the skill reference `f-guidance-builder-v1/references/top-venue-learning-mode.md`).

## Stage sequence

1. **Top-venue study L1–L6 (done, 2026-11-14)**: four parallel survey agents (spiking-GNN/conversion, CTDG, conversion theory, experiment methodology) produced `docs/top-venue-study/00-synthesis.md` … `04-experiment-methodology.md`; gap analysis v1.0 at `docs/top-venue-study/gap-analysis.md`; five load-bearing citations pre-verified (`citation-verification-log.md`).
2. **CCFA startup deliberation (this packet)**: opportunity map refresh, idea cards restated at mechanism level, red-team review of the v4 increments, claim-evidence matrix v4, strong-result feasibility contract v4.
3. **G0–G8 re-acceptance** for the v4 revision: gates re-evaluated against v4 evidence; v3 gate evidence reused where unchanged (dataset access, hardware, theory fit); new evidence where the increment demands it (G0 literature map extended, G8 story re-audit).
4. **Validation**: `validate_guidance.py guidance-v4.md --strict --packet ccfa-startup-packet-v4` must exit 0; recorded in `validation-report.md`.
5. **Handoff**: `f-research-v1` records a third `reopen P0` back-edge (`contract_version: v4`), opens a new run root, re-accepts P0–P2 before P3; unaffected v3 evidence reused with explicit applicability notes.

## Decision required at this phase

Whether the v4 increments C-1…C-10 and manuscript requirements M-1/M-2 (`gap-analysis.md`) form a feasible, mechanism-consistent deepening within the recorded resource envelope (M1/16 GiB/12 h; no remote compute; no new datasets). Verdict recorded in `startup-decision.md`.

## Roles

- `ccf-pipeline-orchestrator`: stage plan and gate ownership (this file).
- `ccf-idea-optimizer`: mechanism cards (idea-cards.md).
- `ccf-literature-searcher`: opportunity map refresh (prior-art-opportunity-map.md).
- `ccf-idea-reviewer`: red-team review of increments (idea-red-team-review.md).
- `ccf-experiment-designer`: claim-evidence matrix and feasibility contract (claim-evidence-matrix.md, strong-result-feasibility-contract.md; machine-readable `feasibility-contract.json`).

## Hard constraints carried from v1–v3

Public data only; local execution only; no neuromorphic energy measurement; no `spike-proxy → real sparse execution` main claim; no re-use of the non-submittable `Ztn2snn` historical manuscript; no lowering of any binding v1–v3 target; v3 evidence preserved byte-for-byte.
