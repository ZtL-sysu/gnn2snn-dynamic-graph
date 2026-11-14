# 新引用核验日志（v4 候选）

> 核验时间 2026-11-14；方法：直接抓取 arXiv/abs 页面核对标题/作者/venue 声称。P12/P14 正式引用前需再过一遍仓库引用核验流程（DOI/arXiv 双查 + 去重）。

| 声称 | 核验结果 | 结论 |
|------|---------|------|
| Yan et al., TCAD, SNN 能效重审 | arXiv:2409.08290；标题 "Reconsidering the Energy Efficiency of Spiking Neural Networks Inference from Analytical Perspectives"；作者 Zhanglu Yan 等；comment "accepted by TCAD"；容量匹配与 T=5 时 firing rate <5.7% 规则确认 | **PASS** |
| CRAFT | arXiv:2505.19408；标题 "Future Link Prediction Without Memory or Aggregation"；作者 Lu Yi 等；preprint 无 venue | **PASS（引用时标 preprint）** |
| GraphSSM, NeurIPS 2024 | arXiv:2406.00943；标题 "State Space Models on Temporal Graphs: A First-Principles Study"；作者 Jintang Li 等；accepted NeurIPS 2024 | **PASS** |
| TGB-Seq, ICLR 2025 | arXiv:2502.02975；标题 "TGB-Seq Benchmark: Challenging Temporal GNNs with Complex Sequential Dynamics"；作者 Lu Yi 等；ICLR 2025 | **PASS** |

| Horowitz, ISSCC 2014 | IEEE Xplore 6757323 "Computing's Energy Problem (and what we can do about it)"，Mark Horowitz；45 nm FP32 add 0.9 pJ、MAC ≈4.6 pJ（乘法 3.7 + 加法 0.9）确认，SNN op-count 惯例系数源头 | **PASS** |
| 待核验（A/C 报告返回后追加）：Spiking CenterNet NeurIPS 2024、GRSNN ICML 2024、ChronoSpike、CRPI/MPEF ICML 2026、Du 2025 paired bootstrap、Agarwal rliable NeurIPS 2021（已有 v3 引用基础的可复用）。
