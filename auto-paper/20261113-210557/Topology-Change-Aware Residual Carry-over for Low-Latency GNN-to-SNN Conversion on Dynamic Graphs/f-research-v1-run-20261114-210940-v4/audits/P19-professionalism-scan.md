# P19 — Professionalism scan

Date: 2026-11-15. Scope: `paper/main.tex` (post-P13). Method: targeted scan for the
prohibited pattern classes (templated transitions, rhetorical self-questioning,
rule-of-three padding, journal-facing meta-language, repeated negative parallelism,
conversational comparison, production/debugging narration); each flagged defect was
fixed individually — no blanket paraphrase, no number/citation/equation altered.

## Flagged defects and fixes

1. **Templated transition, §4.5** — "This is the standard latency–fidelity trade-off of
   conversion methods …, observed here up to a saturated agreement ceiling." Fine on
   re-read (substantive, with citations); NO CHANGE.
2. **Repeated negative parallelism, limitation 9 draft** — the first revision of the D1
   limitation stacked three "not" clauses; rewritten to positive scope statements
   ("reduces cleanly to topology-gated base re-anchoring plus local-threshold
   recalibration — the two components that are live").
3. **Production narration risk, §3.4/§3.6** — "recorded in the public correction ledger"
   (process-flavoured) → reframed as a measurement provenance statement ("in the pilot
   engine of the correction ledger, a full flush or a partial decay discarded…"),
   keeping the scientific content (what was measured) and dropping the file-pointer tone.
4. **Conversational comparison** — none found ("better for the wrong reason"-class
   phrases absent; checked via grep for "wrong reason|it is worth asking|notice that
   importantly|we argue that" — no hits in body text).
5. **Defensive limitations** — limitations are stated as measurement conditions and
   applicability boundaries (energy convention, saturation mechanism, coverage cap);
   the ninth limitation states the repair path (wire the carry, re-run the locked
   protocol) as future evidence, not as an apology.
6. **Abstract length** — was 449 words (style+compliance defect); rewritten to 248 words
   (see P17). The rewrite preserved every quantitative anchor (T=4, ten seeds, twelve
   methods, q=0.039, d_z=1.27, 5% ceiling).

## Preserve list (explicitly NOT touched)

- All equations, numbers, macros, citation keys, figure references.
- Technical terms: DCGS, TCAR, graded events, per-node event-axis recursion, etc.
- The verbatim locked-rule quote in §4.1 (contract text; untouchable).
- Academic-humanizer pass deferred to the human author: the prose is formal and
  exact; a final voice pass by the author is recommended before any real submission
  (this pipeline does not submit).

Result: PASS — no flagged AI-like, conversational, defensive, or meta-process prose
remains; every change above has an identified defect.
