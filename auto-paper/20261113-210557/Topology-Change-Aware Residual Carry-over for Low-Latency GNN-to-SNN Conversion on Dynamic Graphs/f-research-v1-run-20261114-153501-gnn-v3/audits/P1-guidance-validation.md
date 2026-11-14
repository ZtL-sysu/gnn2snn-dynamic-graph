# P1 Guidance Validation (contract v3)

`../guidance-v3.md` validated with `validate_guidance.py --strict --packet ../ccfa-startup-packet-v3` → `Guidance structure is valid.` (EXIT=0). v2 and v1 also still validate, and their hash-bound packets are preserved.

Contract extraction: topic = DCGS-converted dynamic-graph GNN; venue = Neurocomputing; main claim = topology-change-aware static-base re-anchoring suppresses event-axis conversion error; datasets = 5 Zenodo streams; baselines = 6 adapted conversion methods + CRPI-style control + directly trained spiking GNN; primary metric = `agreement@K`; secondary = `epsilon_k`, measured `||Delta A_k||`, graded events, firing rate, SynOps, error decomposition, latency; strong target = v2 verbatim; length >= 21 pages; >= 40 verified refs.

Startup decision in packet v3 = `proceed` (v3 re-acceptance). Planned claims remain distinct from observed findings; `observed_finding = unresolved_until_evidence`. **P1 pass.**
