# Submission constraints (target journal: Neurocomputing, per guidance-v4)

Date: 2026-11-15. Source: guidance-v4 Constraints section (retained verbatim from v1:
"Neurocomputing official limits"). This file records the strictest applicable limits
currently known to this pipeline and the measured compliance. **No submission is
performed by this pipeline** (`不实际投稿`); this is the readiness record.

| Constraint | Limit | Measured | Status |
|---|---|---|---|
| Abstract length | ≤ 250 words | 248 words (stripped-LaTeX count) | PASS |
| Keywords | 1–7 | 7 (`\begin{keyword}` block) | PASS |
| Highlights | 3–5, ≤ 85 chars each | 5 highlights, 79–85 chars (`paper/highlights.txt`) | PASS |
| GenAI declaration | required, before references | §"Declaration of generative AI…" at line ~517, before `\bibliography` ~line 529 | PASS |
| Data/code availability statement | required | §"Data and code availability" present | PASS |
| Page limit | none official; user requirement ≥ 21 pp | 40 pages | PASS |
| Figures/tables | no official quota | 13 figs + 12 tables, all cited/captioned | PASS |
| Anonymity | Neurocomputing single-anonymous is standard; no author info asserted in this pipeline's build | no `\author` block filled — author metadata left to the human author | RECORDED |
| Cover letter / submission fields | journal-form specific | unresolved — to be completed by the human author at real submission | UNRESOLVED |

## Items that must not be relaxed

- The hard limits above cannot be waived by preference; the only currently
  UNRESOLVED items are the cover letter, author/affiliation/corresponding-author
  metadata, and any Elsevier-submission-system fields. These are human-author actions
  at submission time, recorded here per the P20 gate ("if no target requirements exist,
  record as unresolved" — target exists, so the unresolved set is the form-level
  metadata only).
