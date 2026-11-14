# Prior-art Opportunity Map — contract v4 refresh

Refresh of the v3 opportunity map after the 2026-11-14 top-venue study (`docs/top-venue-study/01–04`). Links verified by survey agents; P12/P14 re-verifies before citation. **Finding of record: `Lite-SDGN` (named in the historical audit as occupying the dynamic-graph SNN architecture space) has no arXiv or web presence and is treated as a phantom name; the real neighbours are SpikeNet, Dy-SIGN, DRSGNN, SiGNN, Delay-DSGN, ChronoSpike, SpikingHAN, GT-SNT.**

## Same family (ANN→SNN conversion, error structure)

| Cluster | Works | Status vs v4 |
|---|---|---|
| Residual/carry-over across steps | CRPI (ICML 2026, arXiv:2601.21778); RMPA (arXiv:2608.13952) | C2 already adapts CRPI to graph layers; v4 adds the α trade-off experiment (C-8) that CRPI's Figure 4 made standard. RMPA cited, not rerun (initial-potential scheduling, orthogonal mechanism) |
| Multi-threshold + error feedback | MPEF (ICML 2026, PMLR v306) | **v4 control C5-MT closes this gap** |
| Quantization-aware / calibration | QCFS, SNNC-AP, CASC, offset-spike, ECL (ICML 2025), FTBC (ECCV 2024), RMP-SNNv2, When-SNN-meets-ANN (TMLR 2025) | C3/C4 cover the QCFS/offset family; ECL/FTBC/RMP-SNNv2 added to related work for the dose-response convention |
| Bounds via spectral norms | ISC (CVPR 2025, arXiv:2409.03368) | template for T2; T2 adds the topology term ISC lacks |
| Differential coding theory | DCGS (ICML 2025, arXiv:2503.00301) | template for T1 (Thm 4.4/4.5 style) |
| Streaming/stateful conversion | Error Amplification = CRPI paper; Temporal Misalignment (ICML 2025, PMLR v267 bojkovic25a) | **whitespace confirmed: no 2024–26 top-venue theory for conversion with an unbounded state stream and changing operator — v4 T2/T3 occupy it** |

## Adjacent techniques (competing routes on dynamic graphs)

| Cluster | Works | v4 response |
|---|---|---|
| Direct-trained spiking GNNs | SpikeNet (AAAI 2023); Dy-SIGN (AAAI 2024); DRSGNN (AAAI 2024); SiGNN (PR 2025); Delay-DSGN (ICML 2025); ChronoSpike (LoG 2026, ρ<1 stability); SpikingHAN (AAAI 2026); GT-SNT (AAAI 2026) | positioned as complementary (direct training vs conversion); D1 control + positioning table M-1; SGNNBench (arXiv:2509.21342) supplies the energy-accounting template |
| Dynamic-graph ANN teachers | TGN, TGAT, GraphMixer, DyGFormer/TGB, GraphSSM (NeurIPS 2024), TIDFormer, CRAFT (arXiv:2505.19408) | teacher family fixed by contract; CRAFT/TGB-Seq anti-memory narrative answered in M-1; GraphSSM cited for the state-space view of temporal memory |
| Benchmarks/protocols | TGB (NeurIPS 2023 D&B); TGB 2.0 (2024); TGB-Seq (ICLR 2025); Suter et al. (NeurIPS 2022 D&B) | protocol aligned where applicable (chronological split, negative-type stratification in C-6/C-7); leaderboard submission out of scope (recorded in gap-analysis R2) |

## Public datasets

Unchanged from v3: five Zenodo streams (DOI 10.5281/zenodo.7213796, CC BY 4.0, HTTP 200 verified 2026-11-13, frozen SHA-256 identities). The top-venue study's dataset-breadth suggestion (DBLP/Tmall/Patent) is **rejected** in gap-analysis R1 (hardware envelope + fidelity-not-leaderboard scope); downstream-validity experiment C-6 answers the "so what" question instead.

## Differentiation routes (v4)

1. Topology-term theory (T2) + steady-state ρ condition (T3) — whitespace.
2. Measured-vs-bound tightness with violation rate (V-1) — unoccupied at 2024–26 top venues.
3. Full transparency package (energy formula, stratified firing rates, overhead %, effect sizes) — exceeds community statistics (mean±std, no corrections).
4. Ten-seed pre-registered resolution of a disclosed null result — methodologically distinctive.
