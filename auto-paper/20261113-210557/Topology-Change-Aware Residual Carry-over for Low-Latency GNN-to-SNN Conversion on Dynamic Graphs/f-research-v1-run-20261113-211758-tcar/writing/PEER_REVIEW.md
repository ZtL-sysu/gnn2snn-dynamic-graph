# P9 PEER_REVIEW (local equivalent execution, scientific + full-manuscript review)

Two independent reviewer reports plus an AC/meta-review, written against `paper/main.tex` and the accepted evidence dossier. Reviewer text is kept out of drafting inputs.

## Reviewer 1 (conversion theory)

- **Strength**: the event-axis recursion with an explicit `‖ΔA_k‖` term is a genuine extension of the layer-wise identity; the six ablations isolate individual terms.
- **Concern R1.1 (major)**: Equation (2) is presented as a derivation but `L_A`, `c` and `η_k` are never measured. A reviewer cannot tell whether the inequality holds or is merely plausible. **Required**: state explicitly that it is a claim to be tested and add a direct check of its terms, or narrow to a conditional statement.
- **Concern R1.2 (major)**: the strongest competitor CRPI is adapted, but the manuscript must say exactly how C4 differs (per-node residual, single global threshold, no gate) and why the comparison is fair.
- **Concern R1.3 (minor)**: `ρ = 0.70` is chosen by construction rather than estimated; note as a limitation.

## Reviewer 2 (dynamic graph evaluation)

- **Strength**: three public streams, five seeds, frozen splits, paired bootstrap with BH correction, and honest cost accounting.
- **Concern R2.1 (major)**: absolute predictive accuracy is dominated by EdgeBank (0.947 vs teacher 0.304). Without a prominent statement that predictive SOTA is not claimed, readers will read Table 2 as a leaderboard result. **Required**: state the context-only status in the Abstract/Introduction and discuss it.
- **Concern R2.2 (major)**: the relative error reduction is 3.7% on Enron and negative in two topology bins. This is a negative result about the mechanism and must be reported, not averaged away.
- **Concern R2.3 (major)**: argmax agreement saturates above 0.975 and the M0–C4 agreement CI contains zero on two streams; using agreement as the headline evidence would overstate the result. **Required**: identify `ε_k` as the discriminating metric and report the saturation.
- **Concern R2.4 (minor)**: test query identifiers are non-blind; disclose. No neuromorphic energy claim should appear.

## AC / meta-review

The contribution is a bounded mechanistic result, not a new predictive state of the art. All four major concerns are addressable by clarification and disclosure rather than new experiments: the manuscript already contains the relevant evidence. Acceptance is conditional on (i) explicit context-only framing of absolute MRR, (ii) the saturation and negative dose-response being stated in the Abstract and Discussion, (iii) a statement that the bound is tested rather than assumed, and (iv) a precise C4 description. No unresolved soundness, integrity or reproducibility concern remains after these edits.
