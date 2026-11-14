# CTDG 动态图学习 2024–2026 调研 — 子代理报告 B

> 来源：并行调研子代理（动态图方向），2026-11-14。链接经子代理检索；正式引用前需按仓库引用核验流程复核（尤其 venue/year 声称）。

## 一、重要论文清单

### 基准与评测协议
1. **TGB** — NeurIPS 2023 D&B — https://arxiv.org/abs/2307.01026 —— 统一评测协议；filtered MRR + 每正样本 20 个固定难负样本；5 seeds mean±std；transductive/inductive 双设置；leaderboard 背书。
2. **TGB 2.0** — NeurIPS 2024 D&B — https://arxiv.org/abs/2406.09639 —— 时序知识图谱/异构图 8 大数据集；time-aware filtered MRR；基线 OOM/超时本身作为 scalability 结果。
3. **TGB-Seq** — ICLR 2025 — https://arxiv.org/abs/2502.02975 —— 重复边注水问题；去重边 8 数据集；每测试事件 100 负样本。
4. **Suter et al.** — NeurIPS 2022 D&B — https://proceedings.neurips.cc/paper_files/paper/2022/file/d49042a5d49818711c401d34172f9900-Paper-Datasets_and_Benchmarks_Track.pdf —— 负采样争议源头：RNS 虚高；historical/inductive 难负样本；EdgeBank；TEA/TET 分解。
5. **Le Yu et al.** — arXiv 2023 — https://arxiv.org/abs/2307.12510 —— DyGLib 管道复现 11 方法反超原报数 → 榜单数字是"管道+调参"产物。
6. **ENS** — Scientific Reports 2024 — https://pubmed.ncbi.nlm.nih.gov/38387201/ ；**ATNSF** — IJCAI 2026 — https://www.ijcai.org/proceedings/2026/0302.pdf —— 负样本难度调度。

### 方法论文（叙事样本）
7. **DyGLib/DyGFormer** — NeurIPS 2023 — https://arxiv.org/abs/2303.13047 —— 13 数据集、chronological 70/15/15、5 runs mean±std、AP(RNS 1:1)；transductive/inductive × 3 负采样；效率表与精度表并列。
8. **GraphSSM** — NeurIPS 2024 — https://arxiv.org/abs/2406.00943 —— "TGN memory module 本质是粗糙 SSM"，第一性原理叙事。
9. **TIDFormer** — KDD 2025 — https://arxiv.org/abs/2506.00431 —— 更简单更快双杀。
10. **DyGMamba** — KDD 2025 TGL WS — https://arxiv.org/abs/2408.04713 —— SSM 长程依赖。
11. **CRAFT** — 2025 preprint — https://arxiv.org/abs/2505.19408 —— 反叙事：node ID embedding + cross-attention 即可，去掉 memory 和聚合反而更强。
12. **DyCIL** — AAAI 2026 — https://arxiv.org/abs/2603.01626 —— OOD/因果不变性叙事。

### 效率/可扩展性
13. **Orca** — SIGMOD 2023/TOCS 2025 — https://dl.acm.org/doi/10.1145/3588737（缓存 embedding ~100× 加速，效率即主结果）
14. **PipeTGL** — VLDB 2025；**TGM** — https://arxiv.org/abs/2510.07586；**FAST** — ICPP 2026 — https://arxiv.org/abs/2607.05095

### SNN × 动态图（直接相关）
15. **SpikeNet** — AAAI 2023 — https://arxiv.org/abs/2208.10364；**Dy-SIGN** — AAAI 2024 — https://arxiv.org/abs/2401.05373；**GRSNN**（~20× 能耗主张）— ICML 2024 — https://proceedings.mlr.press/v235/xiao24f.html；**ChronoSpike** — 2026 preprint — https://arxiv.org/abs/2602.01124

## 二、模式提炼

**A. 2024–2026 叙事模式**
1. **"打假"开场成主流**：先证伪再立论（TGB-Seq 重复边、Suter RNS、CRAFT 反 memory）。
2. **把 memory module 理论化**（GraphSSM/DyGMamba 的 SSM/ODE 一阶近似）。
3. **论证"动态性是难点"的标准姿势**：novel/unseen edge 性能落差、去 memory 消融、序列 case study。
4. **效率升为一等公民**：speedup 与精度并列主表。
5. **新轴：OOD/因果/多任务**（2026）。

**B. 实验协议模板**
- ≥5–7 跨域流是底线；背书型 = DyGLib 全 13 + TGB 子集或挂 leaderboard。
- Split：DyGLib 模板 70/15/15；TGB 官方 split；**transductive + inductive 双设置近乎必需**。
- Seeds：社区底线 5 seeds mean±std；几乎无人做假设检验（本项目 bootstrap+BH 超社区标准，是加分项）。
- 负采样：趋势是"越难、越固定越好"（historical/inductive NS 或 TGB 固定 20–100 难负样本 + filtered MRR）。
- 效率：wall-clock、吞吐（events/s）、显存、可扩展性曲线。

## 三、对 TCAR 项目的差距分析（按审稿杀伤力排序）

1. **数据集代际**：5 条 JODIE 时代小流，无 TGB 代际背书 → 必被问"真实大流上是否成立"。
2. **指标脱离下游**：只有逐事件 fidelity，无 fidelity→AP/MRR 损失传递性实验（预测效度）。
3. **无 inductive/冷启动设置**：unseen node 上转换误差是否崩塌是天然研究问题。
4. **负采样协议缺席**：agreement 应在 random vs historical/inductive 负样本下分层。
5. **直接训练 SNN 基线**：D1 是量化代理；社区期望 SpikeNet/Dy-SIGN 级对照（本项目范围内以 D1+文献定位回应，注明边界）。
6. **效率叙事缺位**：吞吐/时延表是硬通货（v3 有 Pareto 与本地时延，可补 throughput 曲线）。
7. **叙事风险**：CRAFT/TGB-Seq 正瓦解"memory/时序状态是核心"共识——intro 必须主动引用并回应。

**一句话结论**：协议骨架合规且统计更严；缺 TGB 代际背书、下游效度、效率证据、直接训练对照——按 2025–26 标准补这四样才够格。
