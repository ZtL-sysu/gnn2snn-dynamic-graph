# P18 Figure and Table Audit

| Artifact | Scientific question | Evidence source | Caption accuracy | Placement | Legibility | Verdict |
|---|---|---|---|---|---|---|
| Fig. 1 framework | What components are converted and which are shared? | verified method components only; `audits/P8-figure-fallback.md` | lists only components in §3 | §4.2, first discussion of the pipeline | vector PDF, 300 dpi PNG | PASS |
| Fig. 2 methods | Which conversion variant is closest to the teacher? | `results/p4_runs/*.json`, 5 seeds, Wikipedia | states agreement and `ε_k`, dashed line = 98.5% target (explicitly a target) | §4.2 adjacent to Table 1 | vector | PASS |
| Fig. 3 streams | Does the effect replicate and what does it cost? | three-stream `ε_k` and trigger rates | measured quantities only | generated and retained; cross-stream values are also in Table 2 | vector | PASS |
| Fig. 4 dose | Does the topology term behave as the bound predicts? | `results/bound-check/*_trace.json`, fixed pre-registered bins | non-monotone result shown, not smoothed | §4.3 immediately after the dose-response text | vector | PASS |
| Table 1 | Full control/ablation comparison on Wikipedia | `final-analysis.json` | mean/SD over 5 seeds; Ret/Trig units stated | §4.2 | compact, fits single column | PASS |
| Table 2 | Three-stream replication | `final-analysis.json` + `validation_mrr.json` | Teacher/EdgeBank/Base3 column explicitly labelled validation context | §4.2 | compact | PASS |

Omitted artifacts: no `fig3_streams` panel is cited in the main text because its information is carried by Table 2; this omission is recorded for traceability. No figure is assigned to a subsection merely to satisfy a quota. No visual implies a hardware energy comparison. Every plotted value traces to a raw row in `results/` (see `paper/figures/figure-sources.json`). **P18 pass.**
