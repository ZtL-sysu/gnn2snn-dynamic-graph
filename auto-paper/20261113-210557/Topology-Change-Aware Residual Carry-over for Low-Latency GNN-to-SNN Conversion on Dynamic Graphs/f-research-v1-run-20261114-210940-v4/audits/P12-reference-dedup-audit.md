# P12 — Reference dedup audit

Date: 2026-11-15. Bibliography: `paper/references.bib` — **50 entries, 50 unique keys**.

## Verification status

- 7 entries added or re-verified for v4 against Crossref/arXiv primary records
  (2026-11-15): `chen2026rmpa` (RMPA: Chen Zirui et al., "Reducing ANN-SNN Conversion
  Error via Residual Membrane Potential Alignment" — title/authors corrected after an
  earlier draft had copied CRPI metadata), `zhang2025sgnnbench` (SGNN-Bench: Zhang et
  al. — title/authors corrected), `horowitz2014` (45nm op-energy convention),
  `benjamini1995`, `efron1987`, `cohen1988`, `agarwal2021`.
- 43 entries carried from the v3 verified set (each was checked against primary
  sources during the v3 cycle; `NRefs=50` macro records the count).

## Recency

37/50 entries are 2022–2026 (74%); the 13 older entries are foundational and cited as
such (maass1997; cao2015spiking; diehl2015; akopyan2015; rueckauer2017; kipf2017gcn;
hamilton2017graphsage; davies2018; velickovic2018; horowitz2014; benjamini1995;
efron1987; cohen1988). Gate: ≥36 real, relevant, mostly-last-3-5-years — PASS.

## Duplicate-paper detection

Dimensions checked across all 50 entries:

1. **Key uniqueness** — 50/50 unique (trivially true in the file; listed for completeness).
2. **DOI / arXiv-id collision** — no two entries share a DOI or arXiv id. Pairs sharing
   a first author + year were inspected individually (below).
3. **Normalized-title similarity** — no near-identical titles.
4. **Authors/year near-duplicates** — one flagged pair, resolved:
   - `poursafaei2022` (TGB: the benchmark/paper) vs `poursafaei2022dataset` (TGB
     datasets paper) — **distinct works** by the same group in the same year; both cited
     in different contexts (benchmark protocol vs dataset availability). NOT duplicates.
5. **Venue vs preprint versions** — no entry appears in both preprint and published
   form (each work appears once).

## Unresolved duplicates

None.
