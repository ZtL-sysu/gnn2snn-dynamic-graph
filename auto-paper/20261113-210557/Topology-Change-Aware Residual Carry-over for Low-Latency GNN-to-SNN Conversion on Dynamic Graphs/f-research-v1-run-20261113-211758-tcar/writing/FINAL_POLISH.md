# P19 Final Polish (local equivalent execution)

Style defects were diagnosed before editing; correct technical passages were not paraphrased merely to differ.

| Diagnosed defect | Location | Action | Recheck |
|---|---|---|---|
| "We also report negative findings:" followed by a long enumeration weakened the journal register and pushed the abstract over the 250-word limit | Abstract, final sentence | replaced with "Negative findings are also reported: discrete memory dominates absolute accuracy, agreement saturates for all variants, effect sizes vary, and the relative reduction is not monotone." | abstract 238 words, all four negative findings retained |
| Rhetorical framing ("Why would a skeptical reviewer care") from the internal story audit | not present in `main.tex` | no action; verified absence | PASS |
| Conversational verdicts and "the paper therefore centers" | not present | no action; verified absence | PASS |
| Direct negations that could be reframed as positive evidence boundaries | §3.3, §5 | kept "No neuromorphic energy measurement is claimed" and "no label leaks" (correctness), and used positive framing for cost metrics ("we report graded-event counts, recalibration counts, parameter counts and local latency") | PASS |
| Repetitive disclaimers across Discussion | §5 | each limitation has a distinct, named scope condition; no duplicated sentence | PASS |

Facts, equations, numbers, citation keys, terminology and the formal register were preserved. The final whole-paper check (`writing/QUALITY_GATE.md`) passes. No humanizer-style paraphrase was applied to correct technical prose.
