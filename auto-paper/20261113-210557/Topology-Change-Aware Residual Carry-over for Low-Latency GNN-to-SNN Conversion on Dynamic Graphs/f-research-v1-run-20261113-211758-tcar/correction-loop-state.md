# Autonomous Correction Loop State

Created at the first failed review/experiment gate (P3 baseline-first). Governing references: `f-research-v1/references/research-recovery.md`, `SKILL.md` "Autonomous Correction Loop". Every failed run, negative result and superseded plan is preserved as evidence; nothing is erased.

## Loop classification

| Cycle | Trigger | Earliest affected stage | Class | Blocker | Next owner | Pass condition |
|---|---|---|---|---|---|---|
| C1 | P3 gate R1: ANN teacher validation MRR 0.33–0.43 vs EdgeBank 0.936 / Base3 0.909 | P2 (teacher design) | `baseline` + `mechanism` | teacher state encoder cannot retain exact historical edges; strong temporal locality in the validation window | P2/P3 | teacher beats B1/B2 on validation, with per-seed values |
| C2 | P3 gate R2: B0 0.24 / 0.38 / 0.54 vs B1 0.936 / 0.466 / 0.667 | P2 | `evidence` | sampled-softmax training objective mismatched full-catalog evaluation ranking; memory feature under-trained | P2/P3 | same |
| C3 | P3 gate R3: B0 0.07 / 0.35 / 0.41 | P2 | `implementation` | full-softmax training unstable (loss rose 5.94→6.07 on Wikipedia); evaluation bank started empty although training used full history → feature distribution mismatch | P2/P3 | same |
| C4 | P3 gate R4 | P2 | `implementation` | causal training-history bank inherited at evaluation; learning rate stabilised; re-running | P2/P3 | same |

## Strategy changes (never a target change)

- `expected_strong`, `minimum`, `failure`, metric definitions, datasets, splits, and the six ablations are **unchanged** across C1–C4.
- Only the teacher architecture/training objective and the causal memory initialization changed. These are method-variant repairs inside the same method family (ANN→SNN conversion on CTDG), tier, and resource envelope.
- No result was fabricated; no failed evidence was deleted; no strong target was lowered.

## Stop-and-return discipline

If C4 still fails, the authorized next step is **not** to proceed to P4. It is either (i) a further mechanism repair inside the same family with a logged cycle, or (ii) a versioned replacement guidance contract that reopens P0 and reaccepts every gate in order, retaining its own baseline-calibrated `expected_strong`. A versioned contract that merely rewrites the teacher gate into a weaker condition without new evidence is prohibited.

## Current status

C4 re-running; see `results/p3_baselines/validation_mrr.json` for the authoritative numbers of every cycle (each run overwrites that file, so the per-cycle logs are preserved in `audits/P3-gate-history.md`).
