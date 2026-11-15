# P14 — Citation verification

Date: 2026-11-15. Object: `paper/main.tex` × `paper/references.bib`.

## Mechanical checks (automated)

- `\cite{...}` keys used in text: 48 distinct (pre-fix 48; after fix 50 — see Actions).
- Keys cited but absent from the bib: **0** (programmatic cross-check).
- Bib entries never cited: **2 found and fixed** — `efron1987` and `benjamini1995` were in
  the bibliography (they ground the BCa bootstrap and the BH procedure the locked rule
  uses) but had no `\cite`. Both now cited at the verbatim locked-rule quote in §4.1,
  their first and primary use. Re-run of the cross-check after the fix: cited 50/50,
  missing 0, uncited 0.
- LaTeX log: 0 undefined citations (`main.blg`/`main.log` clean on the post-fix build).

## Authenticity

- 7 v4-added/re-verified entries checked against primary records 2026-11-15:
  `chen2026rmpa` (RMPA — title and author list corrected; the pre-v4 draft had carried
  over CRPI metadata under the wrong key `xu2026rmpa`, which was caught and fixed during
  the citation audit), `zhang2025sgnnbench` (title/authors corrected),
  `horowitz2014` (45\,nm energy convention numbers used in §3.10 match the paper's
  Table: AC 0.9\,pJ, MAC 4.6\,pJ), `benjamini1995`, `efron1987`, `cohen1988`,
  `agarwal2021`.
- 43 carried entries were verified during the v3 cycle; no authenticity regressions
  detected in re-inspection of the v3 audit trail.

## Relevance and placement

- Every cited work is referenced in a contextually correct sentence (spot-checked all
  7 corrected entries sentence-by-sentence; the 43 carried entries were placement-checked
  in the v3 cycle and their usage is unchanged in v4).
- Duplicate-paper status: consistent with `audits/P12-reference-dedup-audit.md` (no
  unresolved conflicts).

## Result

PASS — no unresolved placeholders, no missing/uncited/duplicate entries after the fix.
