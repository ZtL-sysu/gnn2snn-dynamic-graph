# P9 PEER_REVIEW (contract v3)

Reviewer 1 (conversion theory): the telescoping lemma and the cross-snapshot increment are now derived; concern R1.1 asks whether `L_A`, `c` and `eta_k` are measured. Resolution: the manuscript states the bound is a claim to be tested, reports the measured `||Delta A_k||` dose-response and an empirical lag-1 `rho` estimate, and explicitly declines a strict inequality check for uninstrumented constants. R1.2 asks for a precise C2 description: C2 is DCGS with per-event residual carry-over and a single global threshold (CRPI-style), stated in Section 4.2.

Reviewer 2 (graph evaluation): R2.1 asks whether the method is a real GNN. Resolution: `A_k` is a row-normalised adjacency built from the interaction history and ablation A5 removes it. R2.2 asks about spike cost: graded events, firing rate and SynOps are now reported. R2.3 asks about absolute MRR: context-only framing, with the EdgeBank/Base3 values disclosed. R2.4 asks about robustness and non-blind IDs: both are now covered.

AC/meta-review: the two earlier soundness gaps (no graph operator; result-driven contract revisions) are resolved by a genuine GNN and by preserved v1/v2/v3 contracts with public amendments. Acceptance conditional on the disclosures, all present.
