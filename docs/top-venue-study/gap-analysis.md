# 顶会差距分析（L5）与 v4 契约增量（L6）— v1.0 定稿

> 定稿 2026-11-14：综合报告 A（SpikingGNN/转换）、B（CTDG）、C（转换理论）、D（实验方法论）。
> 规则：每个增量要么变成 v4 契约的新 binding 实验行，要么变成稿件要求；**不得削弱任何 v3 binding 目标**；v3 的 25 次运行保留，新实验追加。

## 致命缺口（fatal，不补会被拒）

| # | 缺口 | 证据来源 | v4 处置 |
|---|------|---------|---------|
| F1 | 核心边界案例（LastFM q=0.40）只收窄未解决；5 seeds 对 <1% 效应功效不足 | D（Du 2025）、v3 C16 | **C-1 十种子预注册扩展**：seeds 41–50；决策规则先锁后验（下详） |
| F2 | 理论只有递推不等式，自称"claim to be tested, not a theorem"；无 tightness 验证 | C（家族标准：定理三段式；且"实测 vs 界"曲线无人做=差异化点） | **C-2 定理包 T1–T3 + 验证实验 V-1..V-6**（violation rate 为签名实验） |
| F3 | 效率叙事不透明：无理论能耗公式、发放率未分层、TCAR 自身开销未声明 | D、A（SGNNBench 公式模板；CRPI <1% 声明惯例） | **C-3 能耗透明化包**（公式/分层/开销/Pareto 命名操作点） |
| F4 | 同族 ICML 2026 机制未对接：**MPEF 多阈值神经元无任何对照**；CRPI 已被 C2 覆盖但缺 α-权衡分析 | A（审稿人恰是这两组人的风险） | **C-5 新对照 C5-MT**（MPEF 式 MT 神经元 + 误差反馈适配图层，进主网格）+ **C-8 α-权衡实验** |

## 可信度缺口（credibility，缺了显稚嫩）

| # | 缺口 | 来源 | v4 处置 |
|---|------|------|---------|
| C4 | 无 effect size / probability of improvement；主表无 per-seed 散布 | D（rliable 范式） | **C-4 统计升级包**：paired Cohen's d、PoI、per-seed 图、CI 类型注明 |
| C6 | fidelity 指标无下游效度（"so what"） | B | **C-6 下游效度**：ε_k 分层 → MRR 损失 dose-response |
| C7 | 无 transductive/inductive 分层 | B（TGB 双设置惯例） | **C-7 unseen-node 分层 agreement**（诚实 scope：分层报告非重训） |
| C9 | 鲁棒性单点无 sweep；无时间漂移维度 | D、B | **C-9 鲁棒性升级**：三扰动 5 级 sweep + 时间切片漂移曲线（10 片）+ AUT 式汇总 |
| C10 | 无逐组件消融阶梯图；无稀疏度×拓扑变化分层 | A（MPEF 阶梯图惯例）、v3 自承缺口 | **稿件要求 M-2**：消融阶梯图（ε_k 每加一组件降一级）；**C-10 稀疏度分层表** |
| C11 | CRAFT/TGB-Seq 反叙事（memory 是否必要）未回应 | B | **稿件要求 M-1**：intro/discussion 主动引用回应 + 定位表 |

## 明确拒绝的增量（超出信封，记录理由）

| # | 建议 | 拒绝理由 |
|----|------|---------|
| R1 | 新增大规模数据集（DBLP/Tmall/Patent 2.7M 节点）与 Micro/Macro-F1@训练比例协议 | 违反本机 M1/16GB 信封与已锁定轻量流范围；v3 已声明 fidelity 非 leaderboard 定位。以 C-6 下游效度 + 诚实 scope 声明替代 |
| R2 | TGB leaderboard 背书 | 需官方 eval 管道与榜单提交，超出会话授权范围；以协议对齐（chronological split、负样本分层）替代 |

## v4 契约增量（L6 定稿）

### C-1 十种子预注册扩展（对 F1）
seeds 41–50，5 流 × 11 方法 + 新对照 C5-MT = 12 方法列 → 60 主运行（v3 的 25 次保留，新 35 次含 5 个新 seed 的教师训练）。**先锁决策规则（写入契约，先于任何 10-seed 结果检查）**：
- 主判据：10-seed 配对 BCa bootstrap（4,000 次）+ sign-flip 置换检验 + BH 跨流校正；α=0.05。
- 若 LastFM 判据通过（CI 排除 0 且 q<0.05）→ 恢复五流显著 claim；否则维持四流收窄并更新披露文本。
- 禁止为凑显著改操作点/改评估窗（C16 延续）。

### C-2 定理包（对 F2）
- **T1（局部恒等式）**：DCGS 差分编码器 vs ReLU 的逐事件误差恒等式，η_k 显式化为差分 spike 序列函数，证有界性（结构对标 DCGS Thm4.4/4.5 + ECL 三分解）。假设显式枚举。
- **T2（全网络界）**：第 k 事件 logits 误差的谱范数递归界（对标 ISC Thm1）；残差 GCN 的 W̃=(I+Â_kW) 使谱条件显式化；**拓扑项 L_A‖ΔA_k‖‖s_{k-1}‖ 独立成项**（现有顶会界无图结构变化项 = novelty）。
- **T3（稳态界）**：显式解递推；ρ<1 充分条件；稳态界 ε_∞ ≤ (L_A·E‖ΔA‖‖s‖ + c/T + η̄)/(1−ρ)；carry-over 降 ε₀ 付 ρ 代价的定理级权衡。
- **V-1 violation-rate 实验（签名）**：逐事件实测 ε_k vs 定理 RHS（常数从验证数据估计），报 tightness ratio 分布与 violation rate——**2024–26 顶会几乎无人做的低成本差异化**。
- V-2 T dose-response（验 c/T）；V-3 合成边插删比例 p 扫描（验拓扑项线性，斜率对标 L_A‖s‖）；V-4 残差分支缩放改 ρ（验 ε_∞∝1/(1−ρ) 及发散边界）；V-5 carry-over vs reset 对照（CRPI α 样式）；V-6 单点 toy 验 T1 恒等式精确成立。

### C-3 能耗透明化包（对 F3）
- 理论能耗公式（SGNNBench 惯例）：E = Σ_l (E_MAC·#MAC_l + E_AC·#AC_l·T·R_l)，E_AC=0.9 pJ / E_MAC=4.6 pJ（Horowitz 2014, 45nm FP32）；注明代理局限（忽略数据搬运，引 Yan 2024 TCAD 容量匹配论证）。
- 发放率三级分层：global / per-layer / per-time-window（Spiking CenterNet 惯例）。
- TCAR 自身开销百分比声明（对标 CRPI <1%）；延迟口径声明（M1 CPU、计时方法、含编码开销）。
- Pareto 前沿加命名操作点（Fastest/Balanced/Accurate）。

### C-4 统计升级包
每流 paired Cohen's d（ε_C2−ε_M0）、probability of improvement（rliable 式）、主表 per-seed 散点图、全表 CI 类型注明。

### C-5 新对照 C5-MT（对 F4）
MPEF 式多阈值神经元 + 跨事件误差反馈适配图层（多电平发放，n 级阈值），复用校准管道；进主网格（5 流 × 10 seeds）。预期角色：technique-family 对照。若忠实实现超出预算，降级为文献定位并留证据（不得静默删除）。

### C-6 下游效度
测试查询按 ε_k 分 5 层 → 各层 MRR 损失 dose-response（对 B1/B2 上下文）；证明 fidelity 指标有预测效度。

### C-7 inductive 分层
按源/目标节点在训练前缀中是否出现分层 agreement（transductive vs inductive 查询），5 流全报。

### C-8 α-权衡实验（对 F4/CRPI 对接）
携带系数 α ∈ {0, 0.25, 0.5, 0.75, 1.0} 扫描（wikipedia 主 seed + 验证窗），报 ε_k 与误差自相关系数曲线 → decorrelation-vs-overcorrection 权衡图（CRPI Fig 4 样式）。

### C-9 鲁棒性升级
edge dropout / timestamp perturbation / activation noise 各 5 级强度 sweep（替换 v3 单点）；时间切片漂移：评估窗 10 等片的 agreement/ε_k 曲线 + AUT 式汇总。

### C-10 稀疏度分层
graded events / firing rate 按 ‖ΔA_k‖ 分 5 层报（稀疏性×拓扑变化分层）。

### M-1 / M-2 稿件要求
M-1：intro/discussion 主动引用并回应 CRAFT（arXiv:2505.19408）与 TGB-Seq（ICLR 2025）反叙事；加定位表（直接训练脉冲 GNN / 静态图转换 / 动态图 ANN / 本工作）×（算子变化感知 / 无重训练 / 逐事件界 / 事件驱动成本）。
M-2：逐组件消融阶梯图（MPEF 样式）。

## 新增引用需求（进 P12 核验清单）
CRPI（已引 xu2026crpi，复核）、MPEF（已引 fang2026mpef，复核）、ECL ICML 2025、ISC CVPR 2025、RMP-SNNv2、When-SNN-meets-ANN TMLR 2025、SGNNBench、ChronoSpike、Delay-DSGN、SiGNN、DRSGNN、SpikingHAN、GT-SNT、RMPA、TGB、TGB 2.0、TGB-Seq、Suter 2022、CRAFT、GraphSSM、DyCIL、Yan 2024 TCAD、Horowitz 2014、Agarwal 2021 rliable、Du 2025。已预核验 5 条（见 citation-verification-log.md）。

## 可行性核算（M1 本机实测）
- 冒烟标定：1 流 1 seed（window=2000）全流水线 147 s；教师训练 16 s/个。
- C-1：60 主运行 ≈3 h；C-5 新列评估含在运行内（+约 9%）；C-2 验证实验 V-1..V-6 均为已训练教师上的再评估/合成扰动 ≈1 h；C-3/C-4/C-6/C-7/C-10 为分析脚本 ≈30 min；C-8/C-9 sweeps ≈40 min。
- **总预算 ≤5.5 h**，分两个批次执行（主矩阵批 + 分析批），M1 信封 PASS。
