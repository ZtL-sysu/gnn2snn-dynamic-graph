# P10 PAPER_REVISION — concern-to-action ledger

Each concern maps to an affected proposition, an evidence status, an action, a target location and a factual check. No valid condition was weakened and no negative/null finding was removed.

| Concern | Proposition affected | Evidence status | Action | Target location in `main.tex` | Factual check |
|---|---|---|---|---|---|
| R1.1 | Eq. (2) is a derivation, not a theorem | `results/bound-check/*_trace.json` logs `ε_k`, `δ`, activations; the absolute-error dose-response is reported | REWRITE + NARROW: add "Equation (2) is a claim to be tested, not an established result" and report the direct check in §4.3 | end of §3.2; §4.3 dose-response paragraph | the sentence now matches the mixed outcome (growth on MOOC/Enron, not Wikipedia) |
| R1.2 | C4 is the strongest discriminator | `scripts/run_campaign.py` C4 branch | KEEP + clarify: "C4 CRPI-style per-node residual carry-over with a single global threshold and no gate" | §3.3, §4.1 | implementation uses `resid_node[C4][u]`, `theta_global`, no gate |
| R1.3 | `ρ = 0.70` is fixed | `ALPHA = 0.30` | KEEP + disclose in §5 as a limitation | §5 limitation six | no claim that `ρ` was estimated |
| R2.1 | Table 2 could be read as a leaderboard | validation MRR in `p3_baselines/validation_mrr.json` | REWRITE: explicit "scientific claim is conversion fidelity, not predictive accuracy" in §1 and Abstract; "reported as context" in §5 | §1 final paragraph; Abstract; §5 first limitation | teacher 0.304 / EdgeBank 0.947 values match the JSON |
| R2.2 | mechanism effect is small/negative in some bins | `final-analysis.json` diagnostics | KEEP + expand: report 68.7/20.9/3.7% and the negative Enron bins explicitly in Abstract, §4.3 and §5 | §4.2, §4.3, §5 third limitation | all numbers taken verbatim from `final-analysis.json` |
| R2.3 | agreement saturates | paired bootstrap CIs | KEEP + emphasise: `ε_k` named the discriminating metric, saturation stated with the two CIs containing zero | §4.2 | CIs match the analysis output |
| R2.4 | non-blind IDs; no energy claim | `inputs/frozen-identities.json`; hardware profile | KEEP + disclose: non-blind statement in §4.1/§5; cost metrics framed as positive evidence boundaries in §3.3/§5 | §4.1, §5 | no energy figure appears anywhere |

## Post-revision check

Facts, equations, numbers, citations and terminology were preserved. Scope conditions became more explicit, not weaker. The whole-paper narrative was re-read after the edits; Results and Discussion retain distinct roles (measurement vs interpretation).
