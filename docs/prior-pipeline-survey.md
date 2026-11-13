# 本机历史「动态图 / GNN-SNN」流水线只读调研

调研日期 2026-11-13。目的：为新项目（轻量级 GNN→SNN 转换 + 动态图 → Neurocomputing）避免选题重复、复用数据/baseline、规避已知陷阱。所有内容为只读核实，未修改任何历史文件。

代号：

- `D1 = /Users/xhf/full-paper/dynamic graph/d2/auto-paper/20260816-194553/`
- `D2 = /Users/xhf/Downloads/phd/4090/fly-gnn-snn-vision/papers/`
- `D3 = /Users/xhf/Downloads/phd/auto-paper/20260831-154027/EvoSpikeCare - Energy-Aware Personalized Graph Spiking Intelligence for Smart Healthy Ageing/`

## 项目总览与最终状态

| 项目 | 题目 / 科学问题 | 目标 | 最终状态 |
|---|---|---|---|
| A1 `D1/…Robust Dynamic Link Forecasting/` | RiskSet-DyG：负采样策略 `q` 混淆动态链接预测结论，能否学出采样器不变的事件选择分数（logits 减 `log q`，多策略 worst-policy 风险） | KDD/WWW 主会 | **未走完 P21**：P0–P2 passed、P3 running、P19–P21 pending；`experiment-traceability.md` 记「Original RiskSet invariance was rejected and remains superseded」；无任何 `.tex` 主稿 |
| A2 `D1/…Robust Dynamic Graphs/` | 同上早期命名 | — | 空壳目录树，零文件 |
| C `D2/paper-01/` | Wiring as an Inductive Bias（果蝇连接组稀疏图网络） | CVPR 2027 | P0–P21 全 pending；`audits/P2-blocker-no-eligible-worker.md` 全阻塞；guidance 被判 G4 FAIL / G7 FAIL → superseded |
| D `D2/paper-null-ladder/` | 结构敏感零模型阶梯暴露连接组对照协议盲点 | CVPR 2027 | **v1 是唯一走完 P21 且有成稿**：`paper/main.tex`(40,982 B) + `main.pdf`(9 页)，26 阶段全 passed；独立评审最高 7.5/5，governing 5.2/4.6 NOT_QUALIFIED，目标 >8.0 未达。v2 重启后全 pending |
| E `D3/` | EvoSpikeCare：传感器图 + 脉冲 + 个性化联邦的精度-校准-能效 Pareto | Q2+ 期刊 | **仅 guidance 阶段**：CCFA-startup→G8→validation→handoff 全 passed，但明确 proposal-stage，无实验、无成稿；后改名为 AnchorCare |

## 可直接复用的动态图数据（G1 关键）

Zenodo `10.5281/zenodo.7213796`，CC BY 4.0，**公开可直接下载**，时序 70/15/15：

| 数据集 | 事件数 / 大小 | 备注 |
|---|---|---|
| Wikipedia | 157,474 / 2.9 MB | 已落盘 CSV |
| MOOC | 411,749 / 7.1 MB | 策略/冷启动压力 |
| Reddit | 672,447 / 13 MB | 大重复流 |
| LastFM | 23.8 MB 归档 | 未下载；本地 4.35 年跨度与原 JODIE「一个月」描述冲突 |
| Enron / UCI | 0.81 / 0.68 MB | 可选，exact 枚举 |

本机已有冻结流：`D1/.../f-research-v1-run-20260911-151852-riskset/inputs/frozen-streams-v1/{wikipedia,mooc,reddit,lastfm}-events.npz` 与 `inputs/frozen-features-v1/*.npy`。TGB 2.0 因 12 GB 显存预算排除。

指标：worst-policy MRR（主）、mean MRR / AP / AUC / Hits@10、new-pair / repeat-pair 分项、鲁棒性 `PSC=(best−worst)/best`、估计偏差与 rank Spearman、train time / ms-per-event / RSS / VRAM；5 seeds + 配对 bootstrap 95% CI。

## Baseline 代码与本机跑通情况

`D1/.../f-research-v1-run-20260911-151852-riskset/dependencies/` 含 `DyGLib/`、`Base3/`、`TPNet/`、`burstguard-baselines-v1/loretta/DyGLib/`、`T-spear-shield/`、`AutoResearchClaw/`。24 方法列入 `literature-baseline-matrix.md`（EdgeBank、recent-popularity、TGN、GraphMixer、DyGFormer、FreeDyG、CAWN、NAT、Base3 等）。

**实测跑通的只有简单基线**：q049 EdgeBank/Wikipedia validation-only full-catalog MRR 0.54429530077（0.6658 s）、q057 Base3_k10 0.46552137188。`q001` TGN/Wikipedia/seed7 为 `incomplete_timeout`（23 epochs，best validation MRR 0.6772067，**28,800 s**，test 未计算）。GraphMixer / DyGFormer / FreeDyG / CAWN 全为 `planned`。累计 3 configurations / 3 staged-model runs / 14,068 optimizer updates / **8.0838255 accelerator hours**，**零 test 指标**。

> 教训：G6 不能只列 literature-context 强基线；必须选在 M1/MPS 上真能跑完的 baseline 组合，否则 P3 会重演死循环。

## 计划值 / 负结果（勿误用）

- A1 契约里的「MOOC AP 0.650→0.295，55% 崩塌」「≥3/4 数据集 effect≥0.5」**来自缺可执行归档的受控模拟器**，`audits/p1-stoploss-review-v1.md` 明确禁止借该数字放行，不得引用。
- D v1 实测：主矩阵 real 0.8152 vs 各 null 0.4795–0.5133，Δ 0.30–0.34，BH q=0.0002；但 rung 间仅差 0.0244、单调性反转 → 阶梯无法定位效应。真实 MaleCNS top-4 稀疏 real 0.6423，度保持 null 0.6162（CI 含 0），`hypothesis_supported=false`。R63 独立链 LESION_GAP 0.0013 CI [−0.0043,0.0070]，`positive_result = False`。

## 已知陷阱（按阶段）

1. **P1 数学可证伪性**：`candidate-law-oracle-v1.json` 证明排除正例时 `−log q` 后验不成立（K=1 最大误差 100/527）；`policy-optimum-oracle-v1.json` 证明两组合法策略最优排序无法由共同分数推出。评分 85/100 → 42/100 (2.10/5)，裁决 `pivot-with-rescue-route`。新颖性被 Conditional NCE(2018)、*Correcting the LogQ Correction*(RecSys 2025) 等覆盖。
2. **P3 无限创意筛选死循环**：TimeWarp-DyG、AssetContinuity-Flow、JointForecast-DyG、ResidualCopula-DyG、QueryPurity-DyG、SparseCal-DyG、ReleaseConstraint-DyG 等全部 "closed before data / before download"，`post-c78-eligible-space-exhaustion-v1.md` 宣告候选空间耗尽。→ 本项目必须**先冻结协议与强结果契约再开实验**。
3. **能耗故事被硬件否决**：`ten-dynamic-graph-ideas-report.md` Idea 7 明示「3060 非神经形态硬件，不能讲能耗」；`realsparse-v2-top-tier-close-v1.md` 严格评审 **2.54/5 CLOSE**，理由「SpikeNet / Dy-SIGN 占据 dynamic-graph SNN，SGNNBench / AMPLE 占稀疏效率诊断」；M1 无 CUDA kernel 路线。
4. **算力/数据访问**：exp-4090 两节点 offline、`eligible_nodes=0`、task 15259/15264 `NO_ELIGIBLE_WORKER` 后 cancel；neuPrint 需 token 被拒；flyvis license 未验证；1.05 GB Feather 整目录 pull `IncompleteRead` 失败。
5. **完整性/审稿**：R39 审计查出 3 条 `PROJECT-RECORD` 假题录（编造标题），已修正；CVPR 2027 强制 LLM Usage Statement；R47 抓出呈现选择性（主动丢弃两列 null）；R49 锁定的精确字节版稿件磁盘已不存在且无 git 历史可恢复；JCR/WoS 不可得，10 篇 SCI comparator 表如实标 `blocked`。
6. **选题天花板**：`R63-direction-pool.md`「三轮独立评审 7.5 → 6.9 → 6.3，天花板不在执行质量而在选题」。

## 对本项目最重要的结论

**已被占用 / 明确判死（勿重复）**：动态图 SNN 架构（SpikeNet AAAI 2023 `10.1609/aaai.v37i7.26034`、Dy-SIGN AAAI 2024 `10.1609/aaai.v38i15.29587`、Lite-SDGN、SGNNBench、AMPLE）；动态图 + 稀疏/脉冲执行系统；动态图采样器鲁棒性、评测协议、冷启动、记忆重置、缓存预算、motif、conformal、跨策略适配（10 个 idea 全已筛查）；连接组 + SNN 视觉；图 SNN + HAR 能效/联邦。

**空白可做**：历史项目中**没有任何**以 `GNN→SNN 转换`（ANN-to-SNN weight scaling / threshold balancing / 逐层转换误差界）为主机制的项目；`Neurocomputing|GNN.to.SNN|ANN.to.SNN|转换` 在 `D2/papers/*.md` 全局无命中；历史目标全为 KDD/WWW/CVPR/Q2，无一目标 Neurocomputing。差异化路线：把**转换**而非新 SNN 架构作为贡献，例如 CTDG 时序记忆状态（TGN memory / node state）在 ANN→SNN 转换下的等价性与误差累积界，或「转换后 SNN 在动态图事件流上的精度/脉冲/延迟 Pareto，与原生动态图 SNN 在同一协议下对照」。

**必须规避**：先做数学可证伪性（转换误差界 + 支撑条件）再跑；不要陷入 P3 创意筛选；先用 TRAIN-only、0-optimizer、30 分钟 CPU/MPS falsifier；不引用 0.650→0.295；不在非神经形态硬件上讲能耗；不把未复跑的 baseline 当已复现。

## 可照抄的产物格式

- `guidance.md` 一级标题：`# Research Guidance File` + `## Title / Topic`、`## Core Idea`、`## Paper Story`、`## Paper Outline`、`## Experiment Plan`、`## Expected Results`、`## Figure/Table Decision Rules`、`## Traceability Checklist`、`## Citation Scope`、`## Constraints and Preferences`、`## External audit references`。
- `ccfa-startup-packet/` 8 文件：`startup-stage-plan.md`、`idea-cards.md`、`prior-art-opportunity-map.md`、`idea-red-team-review.md`、`claim-evidence-matrix.md`、`strong-result-feasibility-contract.md`、`startup-decision.md`、`feasibility-contract.json`。
- guidance 目录同级：`guidance-pipeline-state.md`、`guidance-contract.yaml`、`dataset-access-log.md`、`evaluation-protocol.md`、`literature-baseline-matrix.md`、`baseline-ablation-plan.md`、`hardware-profile.md`、`novelty-feasibility-report.md`、`theoretical-feasibility-audit.md`、`story-strength-audit.md`、`scenario-decision-log.md`。
- run root 子目录：`audits/ results/ scripts/ paper/ protocols/ inputs/ figures/ writing/ deliverables/`；`paper/` 内 `main.tex / main.bib / preamble.tex / tables*.tex / paper.pdf`。
- `pipeline-state.md` 表头：`| Stage | Name | Status | Evidence / artifact path | Gate result | Notes |`，状态仅 `pending / running / passed / blocked / superseded`。
