# ANN→SNN 转换理论 2024–2026 调研 — 子代理报告 C

> 来源：并行调研子代理（转换理论方向），2026-11-14。口径：NeurIPS/ICML/ICLR 2024–2026 为主，辐射 CVPR/ECCV/AAAI/TMLR。澄清：QCFS(ICLR 2023)、SNNC-AP(ICML 2021) 早于窗口但是理论基线故纳入；"QK-L" 与 "bias once" 精确短语在窗口内顶会不存在。

## 一、重点论文

### 量化感知 / 残差误差 / 校准（feedforward 主线）
- **[QCFS]** ICLR 2023 — https://arxiv.org/abs/2303.04347 —— 期望转换误差为零；低 T 时残差膜电位项是主项。
- **[RMP-SNNv2]** IEEE Trans. 2025 / arXiv 2024 — https://arxiv.org/abs/2404.17456 —— 残差误差建模为加性零均值高斯噪声，证任意 T、L、δ 期望误差为零；合成噪声 δ 剂量反应验证。
- **[When SNN meets ANN]** TMLR 2025 — https://openreview.net/forum?id=GTzP2GC7NR —— 三类误差分解；reset 移到末时刻消 deviation 项；u(T) 分布直方图检验假设。
- **[ECL]** ICML 2025 — https://proceedings.mlr.press/v267/liu25bl.html —— 命题 v*(0)=θ/2 最小化期望平方误差；教科书级 dose-response（双阈值消融 T=2 +19.31% vs T=8 +1.29%）。
- **[FTBC]** ECCV 2024 — https://arxiv.org/abs/2403.18388 —— 逐时间步通道偏置校准使每步期望误差→0。
- **[ISC]** CVPR 2025 — https://arxiv.org/abs/2409.03368 —— **最标准的"界"**：Thm1 谱范数递归界 e^L ≤ Σ_l (Π_{k>l}‖w^k‖₂)·‖S(ẑ^l)−A(ẑ^l)‖₂；由界导出阈值平衡算法。**明确不画"实测 vs 界"曲线**。
- **[QAC]** ICLR 2025 投稿 — https://openreview.net/pdf?id=D4sQzdMvcG —— 量化位宽↔时间步等价。

### 时序 / 循环 / 动态算子
- **[SpikedAttention]** NeurIPS 2024 — proceedings.neurips.cc（WOSS spike-shift 替换 softmax；无有限 T 非渐近界）
- **[SpikeZIP-TF]** ICML 2024 — https://proceedings.mlr.press/v235/you24b.html（附录 Lemmas 证 ST-BIF≡量化器、SESA≡量化自注意力）
- **[QCRC]** ICANN 2024 — https://arxiv.org/abs/2408.09403（RBIF 神经元循环网络无损转换；**顶会级循环转换理论基本空白**）
- **[Error Amplification（=CRPI 论文）]** arXiv 2026 — https://arxiv.org/abs/2601.21778 —— 闭环误差沿决策步正相关放大（ε̃_{k+1}=ε_{k+1}−αε_k），提出 CRPI；α 剂量反应验证。**与"状态沿事件流递归"的 TCAR 最同构**。
- 空白结论：**streaming/online（状态无限延续）转换 2024–26 顶会无系统理论**；最接近的是 Temporal Misalignment（ICML 2025，https://proceedings.mlr.press/v267/bojkovic25a.html）。

### 差分 / 多值编码理论
- **[DCGS]** ICML 2025 — https://arxiv.org/abs/2503.00301 —— Thm4.2/4.3 非线性层与双输入乘法→差分 graded unit 等价；Thm4.4 速率编码→差分编码构造；Thm4.5 线性层≡去 bias+下级膜电位初始化；Thm4.10 阈值迭代全局收敛（高斯预激活假设）。

## 二、模式提炼

**A. 标准结构**
1. **定理三段式**：统一符号；**假设显式枚举**（ReLU、软重置 IF、直接编码 e⁰=0、有界膜电位、高斯预激活、平衡态）；结论三类——零期望/恒等式、最小化命题、递归界。
2. **proof sketch 位置**：主文 3–4 页 Error Analysis 小节，Lemma→Theorem 编号，完整证明在 appendix，配 1 张误差分解示意图。
3. **理论→算法→实验闭环**：定理落成组件，消融逐项对应"消掉的误差项"，Discussion 回扣。

**B. "界+验证"组合拳（按频率排序）**
1. accuracy/error-vs-T dose-response；2. 组件消融对照理论项；3. 参数扫描验趋势/斜率；4. 分布诊断（u(T) 直方图、余弦相关表）；5. 合成/受控实验；6. **实测 vs 界 tightness 曲线——几乎没人做，审稿人也少要求，是低成本差异化点**。

## 三、对 TCAR 的差距分析：补 3–4 定理 + 6 实验

**定理 1（局部恒等式）**：差分编码器 vs ReLU 的逐事件误差恒等式，η_k 显式化并证有界/零均值（对标 DCGS Thm4.4/4.5 + ECL 三分解）。
**定理 2（空间递归→全网络界）**：套 ISC 谱范数递归给出事件 k logits 误差界；残差 GCN 的 W̃=(I+ÂW) 使谱范数条件显式化；**把 L_A‖ΔA_k‖‖s‖ 立为独立拓扑误差项 = 核心 novelty**（现有界只有权重谱范数，无图结构变化项）。
**定理 3（时间递归→稳态界）**：解显式递推，ρ<1 充分条件（‖I+Â_kW‖₂≤ρ 或对角优势）与稳态界 ε_∞ ≤ (L_A·E‖ΔA‖‖s‖ + c/T + η̄)/(1−ρ)。对标 Error Amplification：carry-over 降 ε₀ 但付 ρ 代价的**定理级权衡**。
**定理 4（加分）**：事件到达平稳假设下 ε_∞ 高概率界（Azuma/Hoeffding）。

**验证实验**：①逐事件实测 ε_k vs 定理 RHS + **violation rate**（差异化点，直击"只有不等式"的软肋）；② T dose-response 验 c/T；③ 合成边插入/删除比例 p 扫描验拓扑项线性（斜率匹配 L_A‖s‖）；④ 缩放残差分支改 ρ，验 ε_∞∝1/(1−ρ) 与 ρ≥1 发散（定理 3 签名预测）；⑤ carry-over vs reset ε_k 对照（CRPI α 剂量反应样式）；⑥ 单点 toy 验证定理 1 恒等式精确成立。

**定位**：结构对标 ISC（界→算法→消融）+ ECL（分解+剂量反应）+ ErrorAmp（递归状态误差放大）；定理 2 拓扑项 + 定理 3 ρ 条件 = 相对 2024–26 全部顶会论文的空白；实验①单点即可形成差异化。
