# CCFA Startup Stage Plan

Executive owner: `ccf-pipeline-orchestrator` (specification read from `/Users/xhf/.codex/skills/ccf-pipeline-orchestrator/SKILL.md`; not installed into WorkBuddy, used read-only). This file records the coordination contract only; it does not perform downstream search, review, or experiment design.

## Project goal and current stage

- Goal: a Neurocomputing-targeted manuscript on low-latency GNN→SNN conversion for continuous-time dynamic graphs, with a mechanism-level contribution and a complete local evidence package.
- Current stage: **pre-guidance startup**. No experiments, no results, no manuscript exist.
- Target venue/tier: Neurocomputing (Elsevier, founded 1989; CAS computer-science Tier 2; JCR AI Q1; subscription/hybrid, non-OA by default). Verified from public journal-information pages on 2026-11-13; the official guide-for-authors page will be re-checked at P20 before `submission-constraints.md` is finalized.
- Constraints: local Apple M1 / 16 GiB / MPS only; ≤12 h wall clock; directly public data only; no neuromorphic energy claims; no remote compute; user's static-graph archive is a code/prior-range reference, not a results source.

## Stage gates and artifact owners

| Stage | Owner skill (spec read from `~/.codex/skills/`) | Required artifact | Pass condition | Handoff |
|---|---|---|---|---|
| startup coordination | `ccf-pipeline-orchestrator` | `startup-stage-plan.md` | gates, owners, venue, constraints explicit | → idea optimizer |
| idea concretization | `ccf-idea-optimizer` (standard) | `idea-cards.md` | ≥2 mechanism-level cards with bottleneck, mechanism, assumptions, falsification, contribution type, risks | → literature searcher |
| opportunity map | `ccf-literature-searcher` (standard) | `prior-art-opportunity-map.md` | closest-work clusters, public datasets, strong baselines, metrics, code status, differentiation routes, source-quality policy | → idea reviewer |
| red-team review | `ccf-idea-reviewer` (standard) | `idea-red-team-review.md` | separate readiness / development potential / confidence / fatal risks / score-change conditions | → experiment designer |
| claim-evidence + strong-result contract | `ccf-experiment-designer` (design) | `claim-evidence-matrix.md`, `strong-result-feasibility-contract.md`, `feasibility-contract.json` | every binding claim has mechanism, falsifying ablation, baselines, metric-calibrated targets, code path, prototype, compute/seed/search budget, stop-and-return | → startup decision |
| startup decision | orchestrator | `startup-decision.md` | exactly one of proceed / revise / pivot-with-rescue-route / needs-evidence | → G0 of `f-guidance-builder-v1` |

Only `proceed` may enter G0. A low readiness score alone is not a rejection; an unaddressed fatal risk, missing mechanism, unavailable baseline, or infeasible evidence plan is a block.

## Decision required at this start phase

Decide whether the selected card (C3, topology-change-aware residual carry-over) has (a) a mechanism that is not merely a domain transplant, (b) a directly public dataset and a reproducible protocol, (c) at least one strong recent conversion baseline that can actually be rerun locally, and (d) a baseline-calibrated strong target with a runnable prototype path. If any is missing, the decision must be `needs-evidence` or `pivot-with-rescue-route`, not `proceed`.

## Project-state note

No `ccfa.yaml` project-state file exists for this new project. Per the orchestrator specification, the run continues with the supplied artifacts and records that project-state tracking is unavailable; the authoritative state for this build is instead `guidance-pipeline-state.md` + `pipeline-state.json` in the parent folder, and `goal-ledger.md` at repository root.

## Next owner after startup

`f-guidance-builder-v1` G0 (recent literature and baseline map), then G1–G8 in canonical order. No downstream stage may be marked passed on stale evidence.
