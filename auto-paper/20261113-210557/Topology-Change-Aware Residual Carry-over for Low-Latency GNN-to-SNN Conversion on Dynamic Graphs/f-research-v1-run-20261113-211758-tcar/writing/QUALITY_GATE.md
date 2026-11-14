# P11 QUALITY_GATE (local equivalent execution)

| Check | Result | Evidence |
|---|---|---|
| Exactly six numbered main sections with the canonical names | PASS | `audits/final-metadata-counts.json`; `main.tex` |
| No alternative top-level structure, no appendix, no checklist added after conclusion | PASS | `main.tex` |
| Claim/evidence alignment | PASS | every number in Tables 1–2 and in prose traces to `results/p4_runs/*` or `results/statistics/final-analysis.json` |
| Result strength | PASS | `audits/P5-strong-result-lock.md`, `d_three_streams = true` |
| Figure/table placement | PASS | Figs. 1–2 and Tables 1–2 are cited and interpreted in §4; Fig. 4 in §4.3 |
| Paragraph reverse outline | PASS | `writing/PAPER_DRAFT.md`; no two adjacent paragraphs share a job |
| Whole-paper continuity | PASS | Introduction gap → Method mechanism → Results evidence → Discussion limits → Conclusion bounded restatement |
| Distinct Results/Discussion roles | PASS | Results reports measurements; Discussion interprets and bounds |
| Negative and null findings preserved | PASS | saturation, small effect sizes, non-monotone dose-response, negative Enron bins, non-blind IDs |
| No process narration in manuscript | PASS | no stage names, tool logs, delivery notes or citation-process text in `main.tex` |
| Abstract ≤ 250 words; 1–7 keywords; 3–5 highlights ≤ 85 chars | PASS | `audits/final-metadata-counts.json` (238 words, 6 keywords, 4 highlights) |
| Bibliography verified and deduplicated | PASS | `audits/reference-dedup-audit.md` |
| Compiled PDF matches current TeX | PASS | recompiled after the final abstract edit; 14 pages |

No unresolved major issue. P11 pass.
