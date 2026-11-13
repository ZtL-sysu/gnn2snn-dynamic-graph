# 对 `ZtL-sysu/gnn2snn` 静态图归档的只读调研

调研日期 2026-11-13；本地只读克隆 `_refs/gnn2snn`（`.gitignore` 排除，不上传）；远端 https://github.com/ZtL-sysu/gnn2snn 。仅 1 个浅提交 `f19a2f2`，是 2026-11-13 用户要求暂停后整理的精选公开归档，**不是可投稿成果**。

代号：`TK = _refs/gnn2snn/research/visual-graphs/takeover_20261112`。

## 问题与技术路线

主线是**视觉静态图上的 ANN→SNN 训练免费转换**：冻结已训练 GNN 教师，用固定的 DCGS 差分源单元 `MTH_diff`（外部 `h-z-h-cell/ANN-to-SNN-DCGS` commit `5e0e4c7…`）把 ReLU 激活编码成事件流，在低时步 T 内复现教师 logits。事件是**带符号八档分级事件**，不是二进制 IF 脉冲。关键限定：这是项目对源单元的图适配（手写 ReLU 分支放置 + 全训练集直方图校准），不是原 converter 的原样复现；GatedGCN 路径每 tick 仍重算稠密门/归一化/归约。

核心机制：

| 名称 | 机制 | 出处 |
|---|---|---|
| 误差恒等式 | 固定非负 A、线性读出 R：`B̂−B = RA((Ĥ−H)W₂)`；线性性推论，不证明保真/成本 | `docs/METHODS.md` |
| DCGS 差分编码 | `e_t = t(a_t−a_{t−1})`，解码 `Σ e_s/s` | `TK/dcgs_fixed_residual_gcn_event_forward_v1.py` |
| differential hybrid | 状态依赖门每 tick 重算，node/MLP 电流走差分编码，oracle-free | `TK/gated_differential_hybrid_v1.py` |
| frozen gate | 先跑 ANN 前向记录 edge gates 再冻结 replay；teacher-oracle 混合，非独立 SNN | `TK/gated_frozen_gate_prototype.py` |
| affine-base / shared-consumer | `h_l=h₀+q_l`、`e_l=e₀+r_l`，`Wh₀+b` 静态基只算一次，残差前缀编码一次供同层 A/B/D/E 共享；skip 保留原始 q/r。三模式 generic / first_analog / centered | `TK/gated_affine_base_v1.py`、`research/visual-graphs/DERIVATION_PACKAGE_v2.md` |
| centered residual 证明 | 等宽恒等残差下 q_l≥0；float64 合成检查最大膜差 8.41e−12 | `TK/centered-residual-proof-review-v1.md` |
| normalized-gate 界 | `\|m(z',b')−m(z,b)\| ≤ max\|b'−b\| + R(b')·tanh(η/2)` | `TK/stable-normalized-gate-bound-v1.md` |

## 数据 / 架构 / 指标

PyG `GNNBenchmarkDataset` 官方 SuperPixel **MNIST 55k/5k/10k**、**CIFAR10 45k/5k/10k**；SLIC 超像素，节点 = 均值颜色 + 2D 坐标（5 维），有向 top-k 相似邻域 + 标量 edge_attr。教师：固定 GCN 4 层 width-146（101,365 参数）、GatedGCN 4 层 width-70。无学生训练；转换前向即"学生"，冻结教师 + 全训练 label-free 512-bin 直方图 q=0.999 阈值。种子 = 教师 41/42/43。T ∈ {1,2,4,8}。主指标 top-1、教师类别一致率、logit MSE、分级事件数、分项操作数；N=3 均值±样本 SD（描述性，非 CI）。**测试集历史已暴露，非盲测。**

## 真实量化结果（实测）

完整 10k test、三种子（`README.md`、`TK/fixed-gcn-test-three-seed-summary-v1.md`、`TK/gated-three-teacher-seed-summary-v1.md`、`results/teacher_fidelity_plot_data.json`）：

| 设定 | ANN 教师 | T1 | T2 | T4 | T8 |
|---|---|---|---|---|---|
| MNIST 固定 GCN | 91.02±0.27 | 71.43±2.80 | 90.16±0.49 | **91.05±0.26** | **91.02±0.26** |
| CIFAR10 固定 GCN | 54.94±0.07 | 46.81±1.22 | 54.06±0.24 | **54.92±0.08** | **54.97±0.05** |
| CIFAR10 GatedGCN | 68.77±0.41 | — | — | **68.75±0.33** | **68.76±0.39** |

一致率：固定 GCN T4/T8 约 99.28–99.98%；GatedGCN test T4 99.55±0.16%、T8 99.90±0.03%。早期 Planetoid 5 seeds（FTBC T8）：Cora/CiteSeer/PubMed ANN 0.8046/0.7016/0.7750 → 0.8016/0.6872/0.7728。affine 六 profile（45,000 训练图、单 seed41、label-free）：scale1 T4 教师一致率 generic 0.99316 / first_analog 0.99749 / centered 0.99751，centered logit MSE 4.51e−4 vs generic 2.79e−3 —— **一致率不是 ground-truth 准确率，无验证/测试外推**。负结果：稠密 hybrid MAC ≈ ANN 的 T 倍（T4/T8 = 4×/8×）；projected-branch 缓存屏 T1 比 0.2536 > 0.2 被拒；causal IF 对照 T8 仅 25.72%/10.38%。

**计划/目标，非实测**：公开 benchmark 参照（GCN MNIST 90.705、CIFAR10 55.710；MNIST GatedGCN 97.340）、5× 能量、E0–E6 工时，来自 `review-suggestions/grok-bot/cvpr-actionable-guide.md`。**不得引用为结果**。

## 暂停点与遗留问题

`TK/PAUSE_SNAPSHOT_20261113.md`（权威）：用户 2026-11-13 暂停；无 Python/Conda 进程；无科学 gate 或终稿评审完成；6 个 affine profile + 4 个 shared-θ 控制已完成；CIFAR corrected-secondary cells 与 seeds 1–4 未执行；`shared profile audit` 报告缺失（只有脚本 `audit_shared_affine_profiles_v1.py`）；numerical full-cost screen pending；不产生 ≥5× 能量、稳定方法优势、新颖性、CCFA≥7、submission_ready。`frozen-gate` 只有校准产物 `gcal_v1.json`，无 `gval_v1.json` 官方验证。引用真实性审计：42 条中 16 verified / 21 metadatawrong / 5 unresolved。外部评审 `cvpr-submission-review.md` 结论「不建议投 CVPR 2027」；历史稿 `paper/historical-draft/` 明确**不可投稿**。

## 可复用资产

- 代码（`TK/`）：`gated_teacher_model.py`、`full_teacher_gcn.py`、`gated_differential_hybrid_v1.py`、`gated_causal_hybrid.py`、`gated_affine_base_v1.py`、`dcgs_fixed_residual_gcn_event_forward_v1.py`、`activation_histogram.py`、`check_*.py` 回归族、`full_teacher_{calibrate,conversion,test}.py`。
- baseline：`TK/public_baselines/`（benchmarking-gnns 的 PyG 移植，MIT，commit `b6c4077…`）。
- 教师权重：`artifacts/verified-evidence.zip`（40,118,963 B，SHA256 `37e243ea…8210e`），9 个 `best.pt`，`tools/restore_evidence.py` 幂等展开。
- 环境 `environment-executed.yml`：原 conda `dyg-cold` / Python 3.13.13 / torch 2.11.0+cu128 / PyG 2.8.0 / RTX 3060 12 GB —— **本机不可复现**。
- 权利：`RIGHTS.md` 无 blanket license，复用前需单独澄清代码许可。

## 与动态图的关联度：低，是空白但有方法学资产可迁移

主线全部为**静态图**：`T` 是转换时步，不是时间演化维度；"dynamic" 仅指 GatedGCN 的状态依赖边门。真正的时序图线索只在文献/未来计划里（SpikeNet、Dy-SIGN、AEGNN、E6 系列），本仓库无可审阅主结果。

**理论前提直接冲突**：误差恒等式要求固定线性 A；affine-base 的静态基缓存、共享前缀、q/r 非负归纳都假定 `h₀/e₀`、`graph`、`W` 在一次轨迹内不变；normalized-gate 界假设同一 incoming edge set。图拓扑随时间变化时，base 必须按时间重算、skip 与共享消费者坐标原点需重推、门界需引入跨快照项——**仓库完全未处理**。

可直接复用的只有：`MTH_diff` 差分单元、全训练 label-free 直方图校准、冻结协议 + 逐文件 SHA 的证据纪律、归一化门扰动界、`check_*.py` 回归框架。方法主体需重新定义"时间轴"。
