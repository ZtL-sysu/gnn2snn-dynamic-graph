# Reference Verification and Duplicate Audit (P12/P14)

Verification date: 2026-11-14. Sources: Crossref REST API (`api.crossref.org/works/<doi>`, HTTP 200 with title/author/year/venue), arXiv abstract pages (`arxiv.org/abs/<id>`, HTTP 200 with `citation_title`/`citation_author`/`citation_date`), and the ICML 2026 virtual poster page. Every entry in `paper/references.bib` was checked; no entry was added to satisfy a count. The journal's official guide states "Every reference included must correspond to a real, existing source" and sets no numeric quota.

## Verified entries

| Key | Identifier | Verification | Result |
|---|---|---|---|
| `maass1997` | 10.1016/S0893-6080(97)00011-7 | Crossref 200 | Neural Networks 10(9), 1659–1671, 1997 |
| `rueckauer2017` | 10.3389/fnins.2017.00682 | Crossref 200 | Frontiers in Neuroscience 11:682, 2017 |
| `diehl2015` | 10.1109/IJCNN.2015.7280696 | Crossref 200 | IJCNN 2015, pp. 1–8 |
| `li2022snncap` | arXiv:2205.10121 | arXiv abs 200 | "Converting Artificial Neural Networks to Spiking Neural Networks via Parameter Calibration", 2022 |
| `habara2024` | 10.3389/fnins.2024.1420119 | Crossref 200 | Frontiers in Neuroscience 18:1420119, 2024 |
| `xu2026crpi` | arXiv:2601.21778 | arXiv abs 200 | "Error Amplification Limits ANN-to-SNN Conversion in Continuous Control", 2026 |
| `li2023spikenet` | 10.1609/aaai.v37i7.26034 | Crossref 200 | AAAI 37(7):8588–8596, 2023, real title "Scaling Up Dynamic Graph Representation Learning via Spiking Neural Networks" |
| `yin2024dysign` | 10.1609/aaai.v38i15.29587 | Crossref 200 | AAAI 38(15):16495–16503, 2024, real title "Dynamic Spiking Graph Neural Networks" |
| `fang2023spikingjelly` | 10.1126/sciadv.adi1480 | Crossref 200 | Science Advances 9(40):eadi1480, 2023 |
| `zheng2025survey` | 10.1007/s11704-024-3853-2 | Crossref 200 | Frontiers of Computer Science 19(6):196323 |
| `xia2026neuro` | 10.1016/j.neucom.2026.132604 | Crossref 200 | Neurocomputing 670:132604, 2026 |
| `rossi2020tgn` | arXiv:2006.10637 | arXiv abs 200 | "Temporal Graph Networks for Deep Learning on Dynamic Graphs", 2020 |
| `yu2023dyglib` | arXiv:2303.13047 | arXiv abs 200 | "Towards Better Dynamic Graph Learning: New Architecture and Unified Library", 2023 |
| `poursafaei2022` | 10.52202/068431-2386 | Crossref 200 | NeurIPS D&B 2022, pp. 32928–32941 |
| `gao2025hyperevent` | arXiv:2507.11836 | arXiv abs 200 | "HyperEvent: A Strong Baseline for Dynamic Link Prediction via Relative Structural Encoding", 2025 |
| `poursafaei2022dataset` | 10.5281/zenodo.7213796 | Zenodo API 200, CC BY 4.0 | dataset record, 15 files |
| `li2024casc` | ScienceDirect PII S0020025524007369 | publisher page reachable via search result; Crossref DOI not verified | recorded with URL, no DOI claimed |
| `fang2026mpef` | ICML 2026 poster 61672 | ICML virtual page reachable | recorded with URL, no DOI claimed |

## Duplicate and version scan (DOI / arXiv id / normalized title / venue version)

| Potential duplicate | Resolution |
|---|---|
| `xu2026crpi` (arXiv:2601.21778) vs its ICML 2026 PMLR 306 version | **One work, one entry.** The arXiv record is used because its metadata and PDF were verified; the `note` field records the ICML version so no second bibliography entry is created. |
| `poursafaei2022` (NeurIPS D&B paper) vs `poursafaei2022dataset` (Zenodo record) | **Different artifact types**: the paper and the dataset it released. Both are cited because the dataset is the direct source of the experimental streams and the paper defines the evaluation protocol. Marked `[dataset]` in the title. |
| `li2022snncap` (arXiv:2205.10121) vs a possible ICML 2022 published version | Not resolved to a DOI. Only the arXiv record is cited; no duplicate entry created. |
| `rossi2020tgn` (arXiv:2006.10637) vs an ICLR 2020 workshop version | Only the arXiv record is cited; no duplicate entry. |
| `gao2025hyperevent` v1 vs v2 | Only one arXiv id `2507.11836` is cited; no version-specific duplicate. |
| `li2024casc` SSRN preprint 10.2139/ssrn.4545036 vs the Information Sciences article | The SSRN record was a preprint of the same work and is **not** cited; only the publisher URL entry is used. |
| `zheng2025survey` DOI 10.1007/s11704-024-3853-2 (2024 online, 2025 volume) | One entry; year follows the published volume (2025) and the DOI encodes the online-first year. |

## Rejected candidate identifiers (do not cite)

- `10.1016/j.ins.2024.120489` — Crossref 200 but the title is "The strategy of consensus and consistency improving considering bounde...", unrelated to CASC. Rejected to avoid a wrong citation.
- arXiv:2203.04344 and arXiv:2302.08090 — both resolve to unrelated papers (astrophysics and hardware security). Rejected.

## Integrity statement

No placeholder, no fabricated author list, no invented venue, no "in press" claim, and no citation added for recency padding. All 18 entries support a specific statement in the manuscript. Reference numbering is in order of first appearance via the `unsrt` BibTeX style, which matches the journal's numbered `[1]` requirement.
