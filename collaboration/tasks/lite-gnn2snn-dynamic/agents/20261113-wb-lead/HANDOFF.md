# HANDOFF — lite-gnn2snn-dynamic / 20261113-wb-lead

- Updated: 2026-11-14 (contract v3 final, C16 consistency pass)
- Branch: `agent/lite-gnn2snn-dynamic/20261113-wb-lead`
- Work status: `completed` — scientific pipeline delivered; **user acceptance and submission still pending**
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见首个检查点 `manifest.json`）
- Effective contract: `guidance-v3.md` + `ccfa-startup-packet-v3/`；v1/v2 保持原样作为证据
- Latest checkpoint: `checkpoints/20261114T092521Z-v3-final/`（**以此为准**）
- Superseded: `checkpoints/20261114T092323Z-v3-final/` 的 manifest 生成于一次被 `git diff --cached --check` 中止的推送尝试，hash 清单与最终交付树不一致；按协议检查点不可回写，故保留为历史记录并新建最终检查点，不再以其 hash 清单为准。
- Sync: `main` = `75aee0ef95f57f6c8a12285e596aac3b3998c9ba`（本 agent 分支不合并 main）；历史检查点 `96afc01…`(init)、`3fca914…`(guidance)、`a727681…`(P0–P2)、`1f4a548…`(v2 final)、`12319c0…`(v3 首次推送，含被废弃检查点)

## Current state (v3)

- **停止门①为「附条件触发」**：交付物与 26 阶段流水线完成，但**原始全五流 `expected_strong` 判据未通过**（`d_replication=false`，LastFM BH q=0.40）。按 C16 收窄 claim 至四条流并强制披露负结果；未下调任何数值目标，原始判据保留不改。账本 `goal-ledger.md` v1.5，E4 记为「附条件 PASS」。
- `f-research-v1-run-20261114-153501-gnn-v3/pipeline-state.json`：26 阶段依序 passed，含第二次 `reopen P0` back-edge；`pipeline_state.py --complete` EXIT=0。`validate_guidance.py --strict --packet` PASS。
- **成稿**：`auto-paper/20261113-210557/<TCAR 标题>/f-research-v1-run-20261114-153501-gnn-v3/paper/main.tex` 与 `paper/main.pdf`（**30 页**）。六节结构、43 条 Crossref/arXiv 核验引用、12 表 7 图、GenAI 声明、摘要 249 词（≤250）、7 关键词、4 highlights（≤85 字符）。干净目录重编译文本 SHA 与交付 PDF 完全一致，undefined citations = 0，PENDING = 0。

## Established evidence (v3)

- **真 GNN**：`build_graph_state` 逐事件构造行归一化 `A_k(u,c)=1/sqrt(d_k(u)d_k(c))` 并记录 `‖ΔA_k‖`；L 层 residual GCN 教师 + 学习读出。这是对用户最初「用我们的 gnn2snn 转换算法，只不过用在动态图上」指令的落实，v2 的「图味序列模型」硬伤已修复。
- **转换族**：从归档数学描述**独立重实现** DCGS `MTH_diff` 带符号八档差分编码（伸缩解码、zero-latch、bias-once）、512-bin q=0.999 label-free 双遍直方图校准、阈值迭代、affine static base 缓存与 TCAR 重锚；`RIGHTS.md` 无通用许可，未复制任何上游源码。
- **实验**：5 条公开流 × 5 seeds = 25 次真实测试，11 个方法/对照/消融；T 曲线、graded events / firing rate / SynOps、clipping/quantisation/residual 误差分解、深度与聚合器消融、校准与鲁棒性、直接训练脉冲对照、bound 剂量反应、延迟–保真 Pareto、配对 bootstrap + BH 校正。
- **主数值**：M0 agreement 0.9998 / 1.0000 / 1.0000 / 1.0000 / 1.0000；相对 C2 的 per-event 误差降幅 7.1% / 1.4% / 14.3% / 2.1% / 0.17%；触发率 0.165 / 0.072 / 0.103 / 0.127 / 0.096（≤20% 硬上限）。M0 在五流上对六个转换对照 `ε_k` **严格最低**；配对区间在四条流上排除 0，LastFM 不排除（q=0.40）。
- **诚实负结果已写进稿件**：LastFM 非显著边界案例（摘要/结果/讨论/结论均披露）、A5 去聚合消融在四条流上几乎无效应、离散记忆主导绝对 MRR、agreement 饱和、相对降幅非单调、测试 ID 非盲、无神经形态能耗实测、训练前缀覆盖上限 80,000 事件、教师消息权重固定。
- **修正循环留痕**：v2 C1–C9 在 v2 run root；v3 V3-1/V3-2 与 C10–C16 在 v3 的 `correction-ledger.md` / `correction-loop-state.md` / `../guidance-v3-amendment.md`。C16 额外修复了稿件/审计仍描述 C12 前残差衰减、C14 前门控定义、以及统计表把全局最小 BH q 打印到每一行等一致性缺陷。所有失败运行保留为负证据。
- **期刊合规**：Elsevier *Neurocomputing* 官方硬性限制已核实并满足，见 `audits/submission-constraints.md`；≥21 页与 ≥40 引用为用户要求，非官方页数上限。

## v2 historical (superseded, retained as evidence)

`f-research-v1-run-20261113-211758-tcar/`：14 页 PDF、18 条引用、3 流 × 5 seeds、`d_three_streams=true`、E1–E5 PASS。用户 2026-11-14 指出该稿**方法里没有 GNN**、实验单薄、篇幅与引用不足，因此重开 P0 建立 v3；v2 稿件**不可投稿**，其证据包仅作前情/负结果上下文。

## Remaining

- 用户验收与决定是否投稿；对应邮箱、基金、CRediT 角色未提供，记为 unresolved，未编造。
- 若用户要求恢复「全五流显著」的原始判据，需要**新的预注册证据**（例如增加 seeds、延长评估窗口或新增流），不能靠调操作点凑 p 值；C16 已明确拒绝 p-hacking。
- Figure 1 为本地矢量示意图（图像生成需额外积分，未在授权清单内）；如用户授权可重做并重编译。
- AutoResearchClaw CLI 未运行（需用户未提供的 LLM 凭据），写作阶段按本地源码契约等价执行并如实标注。
- 新颖性置信度中等，未做 Scopus/IEEE 全库查重；正式投稿前建议补做。
- 本仓库未合并 `main`、未发布 Release、未投稿。

## Live jobs

无。所有后台作业已结束，无远程任务、无后台进程。

## Resume

1. 读 `goal-ledger.md`、`collaboration/PROJECT.md`、本文件，再看 v3 run root 的 `pipeline-state.md`、`audits/P5-strong-result-lock.md`、`audits/final-audit-note.md`、`deliverables/manifest.json`。
2. 若需修改稿件：编辑 v3 `paper/main.tex` → 在 `paper/` 下 `pdflatex` → `bibtex` → `pdflatex` ×2 → 重跑 `_probe/finalize_v3.sh`（9 步）→ 再发**新**检查点，旧检查点不回写。
3. 停止条件：停止门①附条件触发；用户叫停为最高优先级。
4. 续接者另建自己的 `agent/<task_id>/<agent_id>` 分支与 HANDOFF，不覆盖已有检查点。
