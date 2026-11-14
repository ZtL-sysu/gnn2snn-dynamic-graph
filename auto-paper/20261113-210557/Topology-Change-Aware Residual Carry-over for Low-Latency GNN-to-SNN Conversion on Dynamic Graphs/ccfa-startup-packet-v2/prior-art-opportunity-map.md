# Prior-Art Opportunity Map (standard mode)

Owner: `ccf-literature-searcher` spec at `/Users/xhf/.codex/skills/ccf-literature-searcher/SKILL.md`. Search date 2026-11-13. Public-safe queries only; no private draft text was used in a query. **Searched evidence and inference are separated below.** Source-quality policy: prefer official proceedings, publisher pages, arXiv, and public benchmark leaderboards; exclude policy-excluded venues; record source links and access dates. Several entries are recorded from search-result text and the local predecessor corpus and still require DOI-level verification at P12/P14.

## Closest-work clusters

### Cluster A — ANN→SNN conversion error theory (supports our assumptions)

| Work | Year / source | What it establishes | Link |
|---|---|---|---|
| BayesianSpikeFusion | 2024, Frontiers in Neuroscience 18:1420119 | layer recursion `E^l_i = Σ_j w_ij E^{l−1}_j + (V_i(T)−V_i(0))/T`; `O(1/T)` residual floor; layer-wise normalization origin | https://doi.org/10.3389/fnins.2024.1420119 |
| SNNC-AP / Parameter Calibration | 2022, arXiv:2205.10121 | flooring/clipping error split, second-order propagation, light calibration with ~1024 unlabeled samples | https://arxiv.org/abs/2205.10121 |
| CASC | 2024, Information Sciences, ScienceDirect S0020025524007369 | upper/lower bounds for accurate conversion; consistent activation mapping | https://www.sciencedirect.com/science/article/pii/S0020025524007369 |
| Membrane-potential modulation / TF-reset | 2023, Engineering Applications of AI, S0952197623005067 | conversion error formula for deep nets and reset-related error sources | https://www.sciencedirect.com/science/article/pii/S0952197623005067 |

**Inference**: these give the per-window `c/T` term and justify calibration, but all assume a fixed network and a fixed input operator. None models an event-recursive state with a changing aggregation set.

### Cluster B — cross-step error accumulation (strongest novelty threat)

| Work | Year / source | What it establishes | Link |
|---|---|---|---|
| CRPI, *Error Amplification Limits ANN-to-SNN Conversion in Continuous Control* | 2026, ICML 2026 (PMLR 306), arXiv:2601.21778v2 | conversion errors are temporally correlated across decision steps → state distribution shift; gradient-free Cross-Step Residual Potential Initialization recovers ANN performance | https://arxiv.org/abs/2601.21778 ; code https://github.com/xuzijie32/ANN2SNN-CRPI |
| Spiking DiTs MPEF | 2026, ICML 2026 | membrane-potential error feedback across denoising steps; multi-threshold neurons | https://www.icml.cc/virtual/2026/poster/61672 |

**Inference**: the general "carry residual across steps" idea is **not novel**. Both works have a fixed network; neither has a graph, a neighbor set, or an `A_k`. Our differentiation must be the topology-change term, the event-triggered recalibration, and the three discriminating experiments — not residual carry-over itself.

### Cluster C — spiking dynamic graphs (domain occupants)

| Work | Year / source | Method family | Link / id |
|---|---|---|---|
| SpikeNet | 2023, AAAI, DOI `10.1609/aaai.v37i7.26034` | directly trained spiking dynamic graph model | AAAI proceedings (id recorded from local predecessor audit) |
| Dy-SIGN | 2024, AAAI, DOI `10.1609/aaai.v38i15.29587` | spiking dynamic graph | AAAI proceedings (id recorded from local predecessor audit) |
| Lite-SDGN, SGNNBench, AMPLE | 2023–2025, per local predecessor audit | spiking dynamic graph / efficiency diagnosis | local predecessor corpus |

**Inference**: these occupy "build a spiking dynamic-graph model". Our work **converts an existing ANN teacher**; no architecture competition is claimed. A predecessor audit (`realsparse-v2-top-tier-close-v1.md`, 2.54/5 CLOSE) already rejected the sparse-execution angle on this hardware.

### Cluster D — CTDG link-prediction baselines and benchmarks

| Work | Year / source | Role | Link |
|---|---|---|---|
| DyGLib / *Towards Better Dynamic Graph Learning* | 2023, KDD-linked | unified library, 9 models, 13 datasets | local `dependencies/DyGLib/`; public benchmark code |
| TGB leaderboard, link property prediction | 2023–2025 | published MRR reference rows (e.g. GraphMixer `tgbl-review` test MRR 0.521±0.015) | https://tgb.complexdatalab.com/docs/leader_linkprop/ |
| TAMI | 2025, NeurIPS 2025 | recent authoritative CTDG method, MIT code | https://github.com/Alleinx/TAMI_temporal_graph |
| HyperEvent | 2025, arXiv:2507.11836v2 | strong simple baseline with relative structural encoding; Table III MRR rows | https://arxiv.org/abs/2507.11836 |
| Dynamic GNN survey (Zheng, Yi, Wei) | 2024/2025, Frontiers of Computer Science, DOI `10.1007/s11704-024-3853-2` | discrete vs continuous-time dynamic graph taxonomy | https://news.scienet.cn/htmlpaper/2025/6/20256510324292133928.shtm (secondary report; primary DOI to verify) |

**Inference**: the absolute-MRR landscape is mature and crowded; a converted-model paper should not claim predictive SOTA here. The opportunity is a **conversion-fidelity** evaluation on the same public streams.

### Cluster E — the user's own prior work (local, not external prior art)

- `ZtL-sysu/gnn2snn` (2026, paused): static SuperPixel GNN→SNN conversion; measured T=4 teacher agreement 99.28–99.98% (three seeds), DCGS `MTH_diff` coder, affine static base, label-free histogram calibration. Static graph only.
- Local `RiskSet-DyG` predecessor (2026, unpublished): Zenodo streams, DyGLib baselines, chronological 70/15/15 protocol; core `−log q` law falsified, all ten idea branches closed before download.

## Public datasets and opportunity

| Dataset | Direct access | License | Why it fits |
|---|---|---|---|
| Wikipedia / MOOC / Enron (+ optional Reddit, LastFM) | `https://zenodo.org/api/records/7213796/files/<name>.zip/content`, HTTP 200 verified 2026-11-13 | CC BY 4.0 | small (≤15 MB frozen npz), timestamped events with changing neighbor sets, pre-frozen val/test queries, mature MRR/AP protocol |

## Current strong baselines, metrics, code status

- **Direct rerun/adaptation (main comparison)**: CRPI-style global carry-over, SNNC-AP-light calibration, DCGS differential coder, QCFS/FTBC, rate-coded IF hard reset, EdgeBank, Base3. All are lightweight; the last two have local predecessor validation numbers (0.54429530077 and 0.46552137188 MRR) that are **historical measurements from a different project**, not this project's results.
- **Literature context (not rerun)**: TGN, GraphMixer, DyGFormer, CAWN, TAMI, HyperEvent, TPNet, SpikeNet, Dy-SIGN. Reason: local TGN seed took 28,800 s and timed out; 12 h ceiling.
- **Metrics**: primary `agreement@K` (teacher→SNN argmax agreement at end of a 10k-event window); secondary MRR/AP retention, logit MSE, graded-event count, recalibration rate, `ε_k`, `‖ΔA_k‖`, wall-clock ms/event; 5 seeds with paired bootstrap CI and BH correction.
- **Code/checkpoint availability**: DyGLib, Base3, TPNet, AutoResearchClaw source exist in the local predecessor's `dependencies/`; CRPI's official code link is public but not yet cloned; DCGS/QFCS/FTBC-style coders exist in the user's archive (no blanket license → reimplement).

## Differentiation routes (ranked)

1. **Bound + topology term + event-triggered mechanism** (selected). Distinct from Cluster A (no event axis), B (no graph) and C (not conversion).
2. Diagnostic-only measurement of error vs cumulative `‖ΔA_k‖` (honest fallback if the gate fails).
3. Cross-domain replication (three streams + static-graph control) to make the bound credible rather than a single-dataset curve.

Rejected routes: new spiking architecture, sparse-execution/energy Pareto, sampler-robust link prediction — all occupied or falsified locally (see `scenario-decision-log.md`).

## Search limitations (explicit)

- Searches were public web queries plus the local predecessor corpus, not a systematic Scopus/IEEE/Web of Science sweep.
- Several DOIs, venue names and author lists come from secondary pages or local audits and are **not citation-verified**.
- Novelty confidence is therefore **moderate**. P12/P14 must run a structured duplicate scan by DOI, arXiv id, normalized title, and venue version, and record the result in `reference-dedup-audit.md`. If a directly overlapping paper is found, the novelty claim must be narrowed or the direction reopened at G4.
