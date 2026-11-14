# 顶会差距分析（L5）与 v4 契约增量草案（L6）

> 状态：**草案 v0.2**——基于报告 B（CTDG）与 D（实验方法论）；报告 A（SpikingGNN/转换）与 C（转换理论）返回后定稿。
> 规则：每个增量要么变成 v4 契约的新 binding 实验行，要么变成稿件要求；不得削弱任何 v3 binding 目标。

## 三列表（L5）

### 致命缺口（fatal，不补会被拒）
| # | 缺口 | 证据来源 | v4 处置 |
|---|------|---------|---------|
| F1 | 核心边界案例（LastFM q=0.40）只收窄未解决；5 seeds 对 <1% 效应功效不足 | D（Du 2025）；v3 C16 | 预注册加 seeds 至 10（41–50），决策规则先锁后验（见契约增量 C-1） |
| F2 | 无闭式定理，只有递推不等式；自称"claim to be tested, not a theorem" | 待报告 C 确认家族标准 | 闭式窗口界定理 + 假设集 + tightness/violation 验证实验（C-2） |
| F3 | 效率叙事不透明的：无 op-count 能量公式、 firing rate 未分层、延迟口径未声明 | D（Yan 2024、Horowitz 2014、Spiking CenterNet 惯例） | 能量公式全式 + 分层 firing rate + 口径声明（C-3） |

### 可信度缺口（credibility，缺了显稚嫩）
| # | 缺口 | 来源 | v4 处置 |
|---|------|------|---------|
| C4 | 无 effect size / probability of improvement；主表无 per-seed 散布 | D（rliable 范式） | 统计升级包：paired Cohen's d、PoI、per-seed 图（C-4） |
| C5 | 鲁棒性单点无 sweep；无时间漂移维度 | D、B（TTGBench/AUT 趋势） | 三扰动强度 sweep + 时间切片漂移曲线（C-5） |
| C6 | fidelity 指标无下游效度传递实验（"so what"） | B | ε_k→MRR 损失 dose-response 分层（C-6） |
| C7 | 无 transductive/inductive 分层 | B（TGB 双设置惯例） | unseen-node 分层 agreement（C-7，诚实 scope：分层报告非重训） |
| C8 | CRAFT/TGB-Seq 式反叙事未回应（memory 是否必要） | B | intro/讨论主动引用并回应（稿件要求 M-1） |

### 优势（保持并显性化）
| # | 已有优势 | 处置 |
|---|---------|------|
| A1 | 配对 bootstrap + BH 统计框架**超过**动态图社区标准（社区仅 mean±std） | 稿件显性声明 |
| A2 | 真算子 A_k + 逐事件 ‖ΔA_k‖ 实测（E6） | 保持 |
| A3 | 负结果披露纪律（A5、LastFM、非单调） | 保持；v4 披露新增负结果（若有） |
| A4 | 5 流 + 冻结协议 + 逐 seed 可回溯 | 保持并扩至 10 seeds |

## 契约增量草案（L6，待 A+C 定稿）

- **C-1 十种子预注册扩展**：seeds 41–50，5 流 × 11 方法 = 50 主运行（v3 的 25 次保留，新 25 次追加，合计 50）。**先锁决策规则**：10-seed 配对 BCa CI + sign-flip 置换 + BH；若 LastFM 在 10 seeds 下 CI 排除 0 且 q<0.05 → 恢复五流 claim；否则维持四流收窄并更新披露。不允许为凑显著改操作点（C16 延续）。
- **C-2 理论升级**：把式（bound)/(unfolded)升级为正式定理环境（命名假设 A1–A9 已有），新增门控触发代价的期望界（触发率 × 单触发代价），以及 tightness 实验：实测 ε_k vs 界（常数从标定数据估计），报 tightness ratio 与 violation rate。
- **C-3 效率透明化包**：E = E_MAC·#MAC + E_AC·#AC·s_r·T（45 nm 系数 0.9/4.6 pJ，Horowitz 2014）；firing rate 三级分层（global / per-layer / per-time-window）；延迟口径声明（M1 CPU、计时方法、含编码开销）；Pareto 加命名操作点。
- **C-4 统计升级包**：每流 paired Cohen's d 与 probability of improvement；主表 per-seed 散点图；CI 类型全表注明。
- **C-5 鲁棒性升级**：edge dropout / timestamp perturbation / activation noise 各 5 级 sweep 曲线；时间切片（10 片）漂移评估：agreement 与 ε_k 随评估窗口位置的变化 + AUT 式汇总。
- **C-6 下游效度**：测试查询按 ε_k 分层 → 各层 MRR 损失 dose-response；证明 fidelity 指标有预测效度（对 B1/B2 上下文）。
- **C-7 inductive 分层**：按源/目标节点在训练前缀中是否出现过分层报 agreement（transductive vs inductive 查询）。
- **M-1 叙事升级**：回应 CRAFT/TGB-Seq 反叙事；定位表（直接训练脉冲 GNN / 静态图转换 / 动态图 ANN / 本工作）×（算子变化感知 / 无重训练 / 逐事件界 / 事件驱动成本）。

## 可行性速算（M1 本机）

- 50 主运行：冒烟标定 1 流 1 seed（window=2000）≈147 s；v3 全量 25 运行 + sweeps ≈90 min → v4 主矩阵 ≈3 h，sweeps/分析 ≈1.5 h，总预算 ≤5 h，PASS。
- 全部新分析均为已训练教师上的再评估/分层，无重训练（除 5 个新 seed 教师，训练 16 s/个）。
