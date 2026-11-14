# Spiking GNN / GNN→SNN 转换 2024–2026 调研 — 子代理报告 A

> 来源：并行调研子代理（SpikingGNN+conversion 方向），2026-11-14。**含两个关键修正**：CRPI/MPEF 身份澄清；Lite-SDGN 查无此文。

## 0. 两个关键修正

- **CRPI = Cross-Step Residual Potential Initialization**（ICML 2026，arXiv:2601.21778，Zijie Xu 等，北大余肇飞组；代码 github.com/xuzijie32/ANN2SNN-CRPI）：任务是 **RL 连续控制**的 ANN→SNN 转换（非 GNN 论文）。核心：SNN 动作近似误差在相邻决策步间时间相关，累积成状态分布漂移（error amplification）；把上一步残余膜电位 Δv 按系数 α 带入下一步初始电位，免训练。证据：MuJoCo 4 任务 + DMC 6 视觉任务；APR 82.6%→95.4%（T=16）；能耗 ANN 566.8μJ vs SNN 16.4μJ（T=32）；开销 <1%；5 seeds×10 episodes；α 扫描 + 误差余弦相似度诊断图。
- **MPEF = Membrane Potential Error-Feedback**（ICML 2026，PMLR v306:29284–29297，Haoran Fang 等，吉林大学；OpenReview nsd26wlIGP；代码 github.com/JustVelkhana/SpikingDiT）：任务是 **DiT 扩散模型**转换。核心：Multi-Threshhold 神经元（多电平发放）+ MPEF（跨去噪步时间相关性回收残余膜电位）。证据：ImageNet 256² DiT-XL/2 50 步，naive FID 198 → +MPEF 7.01 → 全配 6.52；T=4 时 FID 5.59 优于 FP ANN 的 5.75；MACs 118.7G→0.91G。
- **Lite-SDGN 不存在**：arXiv API 全库 0 命中、Web 0 命中。疑似历史审计笔误；最近真实名词是 SDGN（arXiv:2504.01278，2025，点过程用）。**处置：v4 related work 如需提及须替换为真实论文；v3 稿件未引用此名，不受影响。**

## 1. 重点论文清单

| # | 论文 | Venue/Year | 链接 |
|---|---|---|---|
| 1 | CRPI | ICML 2026 | arxiv.org/abs/2601.21778 |
| 2 | MPEF | ICML 2026 | proceedings.mlr.press/v306/fang26n.html |
| 3 | RMPA: Residual Membrane Potential Alignment | arXiv 2026.8 | arxiv.org/abs/2608.13952 |
| 4 | SpikeNet | AAAI 2023 | arxiv.org/abs/2208.10364 |
| 5 | Dy-SIGN | AAAI 2024 | arxiv.org/abs/2401.05373 |
| 6 | DRSGNN | AAAI 2024 | ojs.aaai.org/index.php/AAAI/article/view/29640 |
| 7 | SiGNN | Pattern Recognition 158:111026, 2025 | arxiv.org/abs/2404.07941 |
| 8 | Delay-DSGN | ICML 2025 (v267) | proceedings.mlr.press/v267/wang25dm.html |
| 9 | ChronoSpike | LoG 2026 | arxiv.org/abs/2602.01124（ρ<1 收缩 + BIBO 稳定性定理，83–88% 稀疏） |
| 10 | SpikingHAN | AAAI 2026 | arxiv.org/abs/2601.02401 |
| 11 | GT-SNT | AAAI 2026 | arxiv.org/abs/2504.11840 |
| 12 | SGNNBench（基准） | arXiv 2025.9 | arxiv.org/abs/2509.21342（能量公式 E_snn=Σ E_ac·FP·T·R_l，AC 0.9pJ vs MAC 4.5pJ） |
| 13 | Spiking GNN on Riemannian Manifolds | NeurIPS 2024 | arxiv.org/abs/2410.17941 |

**期刊侧结论**：TNNLS / Neural Networks / TPAMI 2024–2026 均未检索到 spiking-GNN / GNN→SNN 论文；家族主战场在 AAAI/ICML/LoG；期刊出口为 Pattern Recognition（SiGNN）、KBS 2026（HASNN）。NeurIPS 2025/ICLR 2026 无主会 spiking-GNN 论文。

## 2. 叙事与实验矩阵（精选）

- **CRPI 借鉴**：①误差相关性诊断图作为机制直接证据（ε_k 自相关/与拓扑变化量相关性）；②「方法开销 <1%」明确声明。
- **MPEF 借鉴**：①逐组件消融阶梯图（198→18.5→7.0→6.5）极具说服力，可平移到 per-event ε_k；②「T=4 反超 ANN」级低延迟卖点。
- **SpikeNet 借鉴**：训练比例协议（Micro/Macro-F1 @ 40/60/80%）+ 最大规模数据集做可扩展性。
- **ChronoSpike 借鉴**：理论 + 可解释性发现（收缩因子 ρ<1、异质时间感受野）是顶会加分项。
- **SGNNBench 借鉴**：能量公式与「effectiveness–efficiency–design-space」三视角评测结构可当模板。
- **Delay-DSGN 借鉴**：给超参一个可行域定理比纯经验调参高一个档次。

## 3. 模式提炼

**A. 叙事模式**：三步套路——①把「精度差」重新定义为**有结构的误差过程**（时间相关性/分布漂移/截断偏置），使误差可诊断可分解；②指出**残余膜电位是被丢弃的免费信息载体**，机制=回收利用，物理图像统一且免训练；③用**误差本身的统计量**（余弦相似度、消融阶梯、逐步分解）作证据，以「极小 T 持平/反超 ANN + 能耗 1–2 个数量级」收束。

**B. 实验矩阵模板（必备表图）**
1. 主表：fidelity × T 网格 × 编码变体 × 全部方法。
2. 效率表：参数量、显存、延迟、**理论能耗公式**（E_ac/E_mac × FLOPs × T × 发放率）、发放率、**本方法开销百分比**。
3. 诊断图：逐组件消融阶梯；误差 vs 驱动变量相关曲线 + 权衡拐点。
4. 鲁棒性：跨 T、seeds、神经元模型；动态图补跨训练比例。
5. 理论小节：至少一个带条件的定量命题。
6. 统计：5 seeds + 配对检验（本项目 bootstrap+BH 已达标）。

## 4. 对 TCAR 的差距分析（最缺 5 项，按优先级）

1. **任务级主指标与数据集广度**（Micro/Macro-F1 @ 训练比例 + 大规模图）：**超出本机信封与 fidelity 定位 → v4 处置：不采纳为新数据集，以 C-6 下游效度实验 + 诚实 scope 声明回应**（违反本地算力约束与已锁定的轻量流范围）。
2. **完整能耗证据链**：按 SGNNBench 公式报理论能耗（E_ac/E_mac × FLOPs × T × R_l）、逐层发放率、TCAR 自身开销（对标 CRPI <1% 声明）、能耗–保真度 Pareto。→ v4 C-3 采纳。
3. **理论规格**：递推不等式升级为显式命题（ε_k 上界对 ‖ΔA_k‖ 与门控增益的显式依赖 / 稳定性条件，借 ChronoSpike ρ<1、Delay-DSGN 核约束写法）。→ v4 C-2 采纳（定理 T1–T3）。
4. **与同族 ICML 2026 机制对接**：CRPI（跨步携带，已被 C2 覆盖）、MPEF（MT 神经元，**未被任何 v3 对照覆盖**）、RMPA（电位对齐，未覆盖）。→ v4 新增对照 C5-MT（MPEF 式多阈值神经元适配图层，主网格评估）；RMPA 以引用定位回应。
5. **门控敏感性与稀疏度分层**：α 扫描 + decorrelation-vs-overcorrection 权衡图（CRPI Fig 4 样式）；脉冲稀疏度随拓扑变化分层。→ v4 C-5/C-8 采纳。
