# HANDOFF — lite-gnn2snn-dynamic / 20261114-topvenue

- Updated: 2026-11-15 (cycle v4 收口 — 流水线 P0–P21 全部 PASSED)
- Branch: `agent/lite-gnn2snn-dynamic/20261114-topvenue`，HEAD `2260d1d`（已 push，ls-remote 核验）
- Work status: **complete**（待用户验收）
- Protocol: `collaboration/PROTOCOL.md` v1
- Effective contract: v4 = `guidance-v4.md` + `guidance-v4-amendment.md` + `ccfa-startup-packet-v4/`（v1/v2/v3 契约与证据保留不动；C-1 锁定决策规则原文绑定于 `scripts/bind_contract.py`）

## 本周期任务（用户 2026-11-14 指令）→ 完成状态

1. ✅ 顶会调研（2024–2026 GNN→SNN/脉冲图网络/动态图）：4 个子代理产物在 `docs/top-venue-study/`（reports 00–04、gap-analysis v1.0、citation-verification-log）。
2. ✅ 「顶会学习模式」蒸馏：L1–L6 流程写入技能 `~/.codex/skills/f-guidance-builder-v1/references/top-venue-learning-mode.md`，SKILL.md 接 5 处。
3. ✅ f-guidance-builder-v1 升级完成（仓库外技能目录，不入本仓库 git）。
4. ✅ v4 契约 + f-research-v1 新 run root（`f-research-v1-run-20261114-210940-v4/`）执行完毕：**P0–P21 全部 passed**（`pipeline-state.json` 哈希绑定证据；可读镜像 `pipeline-state.md`）。
5. ✅ research-github-sync：两次检查点已 push（`7671e11` P4-P5、`7e8b3b1` P13 修订、`2260d1d` 全链收口），均 ls-remote 核验。

## v4 交付物（run root `f-research-v1-run-20261114-210940-v4/`）

- **论文**：`paper/main.pdf` 40 页，0 LaTeX 错误；13 图 + 12 表全部真实数据生成（`scripts/make_figures_v4.py` / `fill_values_v4.py`，283 宏 0 PENDING）；50 条参考文献全部核验、全部被引。
- **实验**：50 主运行（5 流 × 10 seeds 41–50 × 12 方法）+ 时延相 + 理论臂 V-1..V-6 + C-6..C-10 全部批次；结果 `results/aggregated.json`（600 方法行）。
- **审计链**：`audits/P1…P21` 全套（含 P9 双评审报告、P10 修订日志、P12 去重、P14 引用核验、P17 guidance 覆盖、P18 图表插入、P19 文风扫描、P21 交付核验 + 清单 manifest）。
- **合规**：Neurocomputing 硬约束全过（摘要 248≤250 词、7 关键词、5 条 highlights ≤85 字符、GenAI 声明与数据/代码声明在文献前）；作者/投稿字段按设计留空（不实际投稿）。

## 周期最重要的科学结论（与 verdict of record）

1. **C-1 锁定判决 `d_replication_10seed = FALSE`**：双倍功效下前驱四流显著性主张不复制——仅 Wikipedia 显著（BH q=0.039，d_z=1.27，PoI=1.000），Enron/Reddit/LastFM 方向正但不显著，**MOOC 方向为负**。论文 claim 按锁定规则收窄，目标数值未做任何下调。
2. **披露的引擎缺陷 D1**：`dcgs_encode` 接受残差结转参数但从不消费（v3/v4 引擎逐字节相同）→ **C2 ≡ C1 逐位一致**，α 剂量臂（V-5）按构造为零。C-1 判决不受影响（比较的是编码即执行的方法，且 v3→v4 比较同构）；机制证据收敛为「拓扑门控基重锚 + 局部阈值再校准」两个活分量。已在摘要/§2.3/§3/§4/第九条 limitation 披露；引擎与证据保持逐字节不动（预注册纪律）。
3. 负结果全部保留：V-4 状态衰减臂方向失败、下游 ε→MRR 剂量响应五流全平、TCAR 开销 2.748% 高于 2% 条（如实披露）、MOOC 方向负。

## 验收后建议的下一步（不在本周期执行）

- **D1 修复 + 锁定协议重跑**（论文 limitation 9 已写明）：把 carry 真正接入差分编码器，新开 run root 按同一 C-1 规则原文重跑——这是唯一既有科学价值又不破坏预注册的路径。
- 作者信息/投稿字段由用户填写；建议投稿前由用户本人做一次 voice pass（P19 已留建议）。

## Resume（若周期重开）

1. 读本文件 + `goal-ledger.md` §10 + run root `pipeline-state.md`；
2. 一切产物在分支 `agent/lite-gnn2snn-dynamic/20261114-topvenue`（HEAD `2260d1d`）；
3. v3 run root 与其证据哈希清单 `audits/v3-evidence-hashes.json` 保持 byte-preserved（P21 复核 5/5 PASS）；
4. 不要 force push / 不要合 main / 不要在历史 run root 内跑 smoke（2026-11-14 12:50Z 事故教训）。

## Live jobs

无。4 个文献调研子代理（含最后的「脉冲图网络顶会论文」）均已返回并落盘。
