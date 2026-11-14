# P6 PAPER_OUTLINE (local equivalent execution)

AutoResearchClaw CLI is not run (its source contracts were read from the local tree; the CLI needs an LLM credential the user did not supply). This artifact follows the stage-16 contract using only accepted P5/P5A evidence. Manuscript: `paper/main.tex`.

Canonical six numbered sections, question/answer path and one-sentence purpose per subsection:

| Section | Question answered | Subsections and purpose |
|---|---|---|
| 1 Introduction | Why is conversion error on an event stream a different problem? | opening problem (fixed-graph assumption), gap in prior work, three contributions, scope delimitation |
| 2 Related Work | What is already established and where is the gap? | (2.1) ANN-to-SNN conversion; (2.2) cross-step conversion error; (2.3) spiking and dynamic graphs; (2.4) dynamic link prediction |
| 3 Method | What is the mechanism and why should it work? | (3.1) setup and conversion-friendly teacher; (3.2) event-axis error recursion and unfolded bound; (3.3) IF coding and TCAR with the gate and cost model; (3.4) assumptions and six falsifying ablations |
| 4 Experiments and Results | What was measured and what did it show? | (4.1) data/protocol/controls; (4.2) main results with Tables 1–2 and Figs. 1–2; (4.3) ablations, sweeps and the dose-response diagnostic (Fig. 4) |
| 5 Discussion | What do the results establish and what do they not? | discrete-memory dominance; agreement saturation; stream-dependent effect size and negative dose-response; non-blind IDs; no neuromorphic energy; single teacher family; moderate novelty confidence; rejected full-flush pilot |
| 6 Conclusion | What is the bounded takeaway? | restate the recursion, mechanism and evidence-backed scope; one concrete next step |

Core claim path: Introduction (gap) → Method (bound + mechanism) → Results (strict dominance in `ε_k` with CI/BH, fidelity and cost) → Discussion (limits and negative findings) → Conclusion (bounded restatement). Supporting claims S-1 (teacher non-vacuity) and S-2 (three-stream replication) appear once, in Results; S-3 (absolute MRR as context) appears once, in Discussion.

Terminology frozen: "event axis", "topology change", "residual carry-over", "state error `ε_k`", "teacher-to-SNN agreement". `planned_claim` from the guidance is never used as `observed_finding`; all findings come from `results/statistics/final-analysis.json`.
