# 顶会实验方法论调研（2024–2026）— 子代理报告 D：效率与统计执行规范

> 来源：并行调研子代理（实验方法论方向），2026-11-14。所有链接经子代理检索核验；正式引用前按仓库引用核验流程复核。

## 关键参照（均附链接）

**能耗/效率测量**
- Yin et al., IEEE TCAS-I 2023 —— AC/MAC 能量比惯例出处（E_AC=0.9 pJ / E_MAC=4.6 pJ）；IEEE Xplore 链接待补。
- Horowitz, "Computing's Energy Problem", ISSCC 2014（0.9/4.6 pJ 系数源头）：https://ieeexplore.ieee.org/document/6757323
- Yan et al., "Reconsidering the Energy Efficiency of SNN Inference", IEEE TCAD：https://arxiv.org/abs/2409.08290 —— 解析式 E_SNN/E_ANN 模型；容量匹配规则（T 步 SNN vs ⌈log₂(T+1)⌉ 位 QNN）；T=5 时 firing rate 需 <5.7% 才省电。
- Meta-SpikeFormer / Spike-driven Transformer V2, ICLR 2024：https://arxiv.org/abs/2404.03663 —— spike-driven 能耗记账范式。
- Spiking CenterNet, NeurIPS 2024：https://openreview.net/pdf?id=NQUXBoGiDU —— syops-counter + firing rate 报告。
- Falcon, arXiv 2026：https://arxiv.org/abs/2609.35260 —— Fastest/Balanced/Accurate 三 operating points tradeoff 曲线。
- SpikeFit, 2025 Workshop：https://arxiv.org/abs/2510.15542 —— SynOps 代理 + 真实硬件部署双轨。
- ML.ENERGY Benchmark, NeurIPS 2025 D&B：https://proceedings.neurips.cc/paper_files/paper/2025/file/9dc510e3d7b0b3b2a58ffed7a3ad6b0f-Paper-Datasets_and_Benchmarks_Track.pdf

**统计严谨性**
- Agarwal et al., NeurIPS 2021：https://arxiv.org/abs/2108.13264 + https://agarwl.github.io/rliable/ —— 分层 bootstrap CI、IQM、probability of improvement，顶会评估统计事实标准。
- Du, "When +1% Is Not Enough", 2025：https://arxiv.org/abs/2511.19794 —— 配对多 seed + per-seed delta BCa CI + sign-flip 置换；3 seeds 下配对检验几乎检不出小提升。

**可复现性**
- NeurIPS Paper Checklist：https://neurips.cc/public/guides/PaperChecklist（16 项，缺 checklist desk reject）
- NeurIPS 2024 CFP：https://neurips.cc/Conferences/2024/CallForPapers
- MLRC 2026 成为 NeurIPS 官方 track：https://blog.neurips.cc/2026/05/04/mlrc-2026-reproducibility-as-an-official-track-at-neurips/
- Papers with Code 2025-10 下线：https://blog.tib.eu/2025/10/02/papers-with-code-went-offline-the-knowledge-doesnt-have-to/

**鲁棒性基准**
- Ada-DyGNN：https://arxiv.org/abs/2207.10839（邻居嵌入高斯噪声 σ² 扫描）
- TGB-Seq, ICLR 2025：https://github.com/TGB-Seq/TGB-Seq
- TTGBench：https://arxiv.org/abs/2609.08226（结构演化 + 语义漂移联合基准）

## A. 顶会实验执行 Checklist（蒸馏）

**1. 叙事证据（主表+CI）**
- 主表每个数字带区间估计（CI），注明 SD/SE/95% CI 类型与计算方法。
- 跨数据集汇总用 IQM 或 mean±CI 双报；per-seed 散点（boxplot/violin + jitter），不接受仅 mean±bar。
- 关键提升给 effect size（paired Cohen's d）与 probability of improvement，不只 p 值。

**2. 机制消融**
- one-factor-at-a-time，同 budget 重训；消融表与主结论一一映射。
- 关键超参给敏感性 heatmap/sweep 曲线；含正向对照（crippled variant 应显著变差）。

**3. 效率（SNN 专项）**
- 完整 op-count 能量公式 E = E_MAC·#MAC + E_AC·#AC·firing_rate·T，系数注明来源与工艺节点（45 nm: 0.9/4.6 pJ）。
- firing rate 分层报：global + per-layer + 按时间窗。
- latency-accuracy tradeoff 曲线 + operating points 标注；说明 SynOps 代理局限（忽略数据搬运）。

**4. 鲁棒性**
- 扰动强度 sweep + degradation 曲线（不接受单点）。
- 覆盖特征噪声 / 结构扰动 / 时间维度（timestamp 抖动、概念漂移）。
- 动态图补时间切片评估（AUT 式）暴露 drift；与非 SNN 基线同扰动对比。

**5. 统计**
- seeds ≥5；小提升（<1%）用配对设计 + BCa bootstrap CI + sign-flip 置换。
- 多方法比较多重比较校正（BH 优先）；配对检验优先；声明 seed 数与完整矩阵。

**6. 可复现性**
- checklist 16 项逐项；匿名 repo + 环境 + 复现脚本；LICENSE；结果登记公开榜单。

## B. 对 TCAR 项目的差距分析（原文）

已达标：配对 bootstrap + BH、Pareto 前沿、三类鲁棒性扰动、机制消融三件套、T 曲线与误差分解。

**缺口按优先级**：
1. **Effect size 与图表形态（必补，工作量小）**：补 paired Cohen's d / probability of improvement；主表 per-seed 散点/boxplot；核心对比提到 **8–10 seeds**（现 5 seeds 处于下限，<1% 提升功效不足）。
2. **能量公式透明化（必补）**：写全 E = E_MAC·#MAC + E_AC·#AC·s_r·T，系数出处（Horowitz 45 nm），引 Yan 2024 容量匹配论证比较公平性。
3. **Firing rate 分层（必补，SNN 审稿人必问）**：per-layer + 按时间窗两级表 + firing rate–accuracy 联合扫描曲线。
4. **延迟测量口径**：注明硬件、计时方法、是否含编码开销；operating points 标注。
5. **鲁棒性升级**：单点改强度 sweep 曲线；新增**时间漂移维度**（时间切片 AUT），这是动态图项目 2026 年的差异化证据。
6. **开源 checklist（投稿前）**：16 项过一遍、匿名 repo + 环境 + 复现脚本、LICENSE。

> 结论：补完 1–4 即达 2026 主会执行标准；5–6 是从"合格"到"有竞争力"的分水岭。
