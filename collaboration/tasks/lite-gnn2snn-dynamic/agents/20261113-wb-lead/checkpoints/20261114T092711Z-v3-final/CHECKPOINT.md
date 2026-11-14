# Checkpoint: contract-v3 final delivery

- Task / agent: `lite-gnn2snn-dynamic` / `20261113-wb-lead`
- Status: `completed` (scientific pipeline delivered; user acceptance and submission still pending)
- Protocol: `collaboration/PROTOCOL.md` v1
- Contract: `guidance-v3.md` + `ccfa-startup-packet-v3/` (strict validation PASS); v1/v2 preserved as evidence

## What changed

The user's 2026-11-14 directive required a **genuine GNN** using the user's own `gnn2snn` conversion algorithm on dynamic graphs, a top-venue-grade experiment matrix, a manuscript of at least 21 pages, and a substantially expanded bibliography. Contract v3 reopened P0 with a recorded back-edge and added success criteria E6-E8; v1/v2 artifacts were preserved unchanged.

Implemented: a real row-normalised adjacency `A_k` built from interaction history with per-event `||Delta A_k||` logging; an L-layer residual GCN teacher; an **independent reimplementation** of the DCGS `MTH_diff` signed eight-level differential coder (`e_t=t(a_t-a_{t-1})` with telescoping decode, zero-latch, bias-once), 512-bin q=0.999 label-free histogram calibration, affine static-base caching and per-snapshot re-anchoring; and TCAR gating. No third-party source file was copied (`RIGHTS.md` grants no blanket licence).

## Real measurements

- 25 test runs = 5 public streams x 5 seeds x 11 methods/controls/ablations, plus T/architecture/calibration/robustness/aggregator sweeps.
- M0 agreement: wikipedia 0.9998, mooc 1.0000, enron 1.0000, reddit 1.0000, lastfm 1.0000.
- Mean `epsilon_k` reduction over C2: wikipedia 7.1%, mooc 1.4%, enron 14.3%, reddit 2.1%, lastfm 0.2%.
- Paired bootstrap and Benjamini-Hochberg: `{'wikipedia': True, 'mooc': True, 'enron': True, 'reddit': True, 'lastfm': False}` / `False`.
- Contract v3 verdicts: E6 real `A_k` = `True`, E7 matrix = `True`, E8 = 30 pages and 43 verified references.
- Original all-five-stream strong-result lock: `False` (NOT satisfied: LastFM null result, BH q=0.40). Evidence-bounded narrowed claim (C16): `True`. Full per-criterion table in `results/statistics/final-analysis-v3.json`.

## Corrections preserved

C1-C9 (v2) remain in the v2 run root. v3 added V3-1/V3-2 (smoke defects), C10 (DCGS ladder `floor`->`ceil`), C11 (per-stream validation `gamma` in a 5-20% cost band), C12 (real static-base caching/re-anchoring; removal of the harmful residual decay), C13 (comparator-class clarification), C14 (trigger on measured `||Delta A_k||` with conservative threshold EMA), C15 (finer validation `tau` grid for bimodal streams) and C16 (evidence-bounded claim narrowing after the LastFM null result, with a mandatory disclosure and a manuscript/audit consistency repair). No numeric binding target was lowered; the original `d_replication: false` verdict is preserved verbatim and all failed campaigns remain in the evidence package.

## Checks

`pipeline_state.py --complete` PASS (26 stages, contract_version v3, two reopen back-edges); `validate_guidance.py --strict --packet` PASS; clean-extraction recompile text identical to the delivered PDF; no undefined citations; no unresolved PENDING tokens; all deliverables inside the run root; `deliverables/manifest.json` lists 30-page PDF, TeX, 43-entry bibliography, 12 tables, 7 figures, raw results and audits.

## Unresolved, not fabricated

Corresponding email, funding and CRediT roles; GPT-generated Figure 1 (credit cost not authorised, local vector fallback recorded in `audits/P8-figure-fallback.md`); AutoResearchClaw CLI execution (LLM credentials not supplied, local equivalent recorded); full Scopus/IEEE novelty sweep; user acceptance and the submission decision.

## Decision

All 26 pipeline stages are executed and the deliverables are complete (E1-E3, E5-E8 PASS; E4 is a conditional PASS under the C16 narrowed claim). The original all-five-stream `expected_strong` condition remains unsatisfied and is disclosed rather than hidden. Stop gate (1) achievement is triggered with that condition attached. The manuscript is a complete first draft, not an acceptance or a submission; obtaining significance on the fifth stream would require new pre-registered evidence (for example additional seeds or a longer evaluation window), not operating-point tuning.
