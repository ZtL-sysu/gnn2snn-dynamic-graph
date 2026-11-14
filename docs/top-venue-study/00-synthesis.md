# 顶会学习模式：通用流程（00-synthesis）

> 蒸馏自 2026-11-14 四路顶会调研（01–04 报告），流程本身已写入技能 `~/.codex/skills/f-guidance-builder-v1/references/top-venue-learning-mode.md`（L1–L6），本文是其在本项目的应用记录与通用化表述。

## 一句话定义

**顶会学习模式** = 在动笔/动实验之前，先把目标家族最近 24 个月的顶会论文当作"评审标准原文"来拆解，把拆解结果转成自己项目的预注册契约增量，而不是写完再对标。

## 通用流程（L1–L6）

```
L1 定位对标簇      → 同族(技术×任务) + 邻族(竞争技术×同任务) + 迁移族(同技术×邻任务)
                     8–12 张论文卡：标题/venue/年/链接/代码/一句话故事；链接不实即弃
L2 拆叙事骨架      → 每卡五拍：problem → gap(哪个假设失效+怎么证的) → insight → mechanism → evidence chain
                     提炼跨论文招式：aha 放哪、最强前作在哪 preempt、是否"打假开场"
L3 拆实验矩阵      → 家族必备表图清单；baseline 分层；机制消融(one-factor+crippled 对照)；
                     效率记账惯例(公式+系数出处+tradeoff 曲线+命名操作点)；鲁棒性三轴 sweep；统计规范
L4 拆执行细节      → split 冻结、seed 政策、负采样/查询协议、计时口径、方差报告类型、代码发布形态
L5 三列表差距分析  → fatal(不补被拒) / credibility(缺了显稚嫩) / advantage(已超社区标准，显性化)
                     按 (审稿风险 × 本地可行性) 排序；明确拒绝项也要记录理由
L6 预注册契约增量  → 每个增量 = 新 binding 实验行（含 falsifying ablation + stop-and-return）
                     或稿件要求；决策规则先于证据锁定；只加深、不交换
```

## 本轮调研的跨家族模式（可复用结论）

1. **"打假开场"是 2024–26 主流叙事**：TGB-Seq（重复边注水）、Suter（负采样虚高）、CRAFT（memory 不必要）——先证伪再立论比"补白式" intro 高一个档次。
2. **误差过程化**：转换家族把"精度差"重定义为有结构的误差过程（时间相关性/分布漂移/截断偏置），残余膜电位 = 被丢弃的免费信息载体。证据用误差本身的统计量（余弦相似度、消融阶梯、violation rate）。
3. **定理三段式**：统一符号 + 假设显式枚举 + 结论分类（零期望/最小化命题/递归界）；proof sketch 主文、证明附录；理论项与消融行一一对应。
4. **"实测 vs 界" tightness 曲线几乎无人画**（ISC 明确没有）——低成本差异化点。
5. **效率记账透明化**：完整 op-count 公式 + 系数工艺节点出处 + 发放率分层 + 本方法开销百分比。
6. **统计加分项**：社区普遍仅 mean±std（5 seeds），配对 bootstrap+BH+effect size 即超标准；小效应（<1%）需 8–10 seeds 才有功效。
7. **协议代际意识**：动态图社区从 DyGLib 代际走向 TGB/TGB-Seq 代际；老数据要主动声明协议对齐与定位理由。

## 本项目应用映射（→ v4 契约）

| 模式 | 本项目落点 |
|------|-----------|
| 打假开场 | M-1：回应 CRAFT/TGB-Seq 反叙事 + 定位表 |
| 误差过程化 | C-8 α-权衡图（decorrelation-vs-overcorrection）+ C-10 稀疏度分层 |
| 定理三段式 | C-2：T1 恒等式 / T2 谱范数界（拓扑项独立成项）/ T3 稳态界 + ρ 条件 |
| tightness 差异化 | V-1 violation-rate 实验（签名） |
| 效率透明化 | C-3：SGNNBench 公式 + Horowitz 45nm + TCAR 开销 % + 命名操作点 |
| 统计加分 | C-1 十种子 + C-4 effect size/PoI/per-seed 图 |
| 协议代际 | C-6 下游效度 + C-7 inductive 分层 + 负样本分层声明 |

## 技能升级记录

`~/.codex/skills/f-guidance-builder-v1`：
- 新增 `references/top-venue-learning-mode.md`（L1–L6 完整流程 + artifact contract）。
- `SKILL.md` 五处接线：Overview（模式启用条件）、CCFA-startup（L6 增量并入 claim-evidence 矩阵）、G0（L1/L2/L3 成为文献图硬证据）、G8（L5 fatal 清单逐条处置）、输出契约（top-venue-study/ 产物集）。
- 不改动既有 gate 判定标准，只加证据要求；不放宽任何 binding 目标。
