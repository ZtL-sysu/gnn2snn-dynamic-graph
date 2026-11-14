# HANDOFF — lite-gnn2snn-dynamic / 20261114-topvenue

- Updated: 2026-11-14 (cycle v4 启动，顶会学习阶段)
- Branch: `agent/lite-gnn2snn-dynamic/20261114-topvenue`（基于 `20261113-wb-lead` HEAD `509c4ed` 切出；v3 交付物在本分支历史中完整保留）
- Work status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1
- Effective contract: v3 = `guidance-v3.md` + `ccfa-startup-packet-v3/`（本周期结束后将版本化出 v4 契约，v3 保留为证据不动）

## 本周期任务（用户 2026-11-14 指令）

1. 调研最近 2 年（2024–2026）顶会在「GNN→SNN 转换 / 脉冲图网络 / 动态图」方向的论文，学习其叙事、实验设计、实验执行；
2. 蒸馏出通用「顶会学习模式」流程；
3. 用该流程升级 `~/.codex/skills/f-guidance-builder-v1`（SKILL.md 外的新 reference，技能目录在仓库外，不入本仓库 git）；
4. 按升级后流程产出 v4 版 guidance 契约，调用 `f-research-v1` 开展更深实验与论文写作（新 run root）；
5. 用 `research-github-sync` 把研究资料同步到本公开仓库（分支 + 检查点 + push）。

## 已知的 v3 弱点（v4 加深靶点，待顶会调研确认优先级）

- LastFM 流原始显著性判据 FAIL（BH q=0.40），C16 收窄 claim 至四流——v4 预注册新证据（加 seeds 等）正面解决；
- 理论只有逐事件递推不等式，无闭式定理与 tightness 验证；
- 叙事深度可能不及顶会同类（机制故事 vs 工程报告）；
- 统计/效率报告可能缺 effect size、分层 firing rate、op-count 能量公式等当代标准件。

## Resume

1. 读 `goal-ledger.md`（v4 小节）、`../20261113-wb-lead/HANDOFF.md`、本文件；
2. 顶会调研产物在 `docs/top-venue-study/`（02 CTDG、04 方法论已返回并落盘；01 SpikingGNN、03 转换理论两个子代理仍在运行）；差距分析草案 `docs/top-venue-study/gap-analysis.md`（v0.2，待 A/C 定稿）；
3. 技能升级已完成：`~/.codex/skills/f-guidance-builder-v1` 新增 `references/top-venue-learning-mode.md`（L1–L6 流程），SKILL.md 已接 5 处（Overview/CCFA startup/G0/G8/输出契约+References）；
4. 引用预核验：Yan 2024 TCAD、CRAFT、GraphSSM、TGB-Seq、Horowitz 2014 已核 PASS，见 `docs/top-venue-study/citation-verification-log.md`；
5. v4 可行性已实测：冒烟 1 流 1 seed 147 s → 50 主运行 ≈3 h，总预算 ≤5 h（教训：smoke 不得在历史 run root 内跑，12:50Z 事故已恢复并留痕）。

## Live jobs

2 个文献调研子代理在后台运行（SpikingGNN+conversion、转换理论）。完成后通知回本会话。
