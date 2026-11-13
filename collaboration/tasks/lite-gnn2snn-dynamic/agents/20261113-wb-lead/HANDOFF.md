# Handoff: lite-gnn2snn-dynamic / 20261113-wb-lead

- Updated: 2026-11-13T21:21:55+0800
- Branch: `agent/lite-gnn2snn-dynamic/20261113-wb-lead`
- Work status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见首个检查点 `manifest.json`）
- Latest checkpoint: `checkpoints/20261113T132155Z-p0p2/`
- Sync: `main` = `75aee0ef95f57f6c8a12285e596aac3b3998c9ba`；已核对的检查点提交：`96afc01…`(init)、`3fca914…`(guidance)。p0p2 检查点待本轮推送后补 SHA。

## Established

- **E1 PASS**、**E2 PASS**：公开仓库 + 协议骨架 + 校验通过的 guidance 契约（strict 与 `--complete` 均 EXIT=0），见 `validation-report.md`。
- **f-research-v1 P0–P2 依序 passed**，结构化账本 `f-research-v1-run-20261113-211758-tcar/pipeline-state.json`：`--before P3` 返回 PASS；`--complete` 正确返回 `ERROR: delivery requires every stage passed`（P3–P21 pending），证明未宣称完成。
- P1A 三条 binding claim 全部 `pass`，`expected_strong` 未被下调；P1B 无未解决致命风险，所有 claim 标为 planned evidence。
- P2 真实运行：冻结标识 `inputs/frozen-identities.json`（四个流与 1024/4096 查询 ID 的 SHA-256）；MPS matmul/ReLU 可用、CUDA 不可用；原型 0.981 s（远低于 30 分钟里程碑）。**原型第 1 次因 IF 未展开 T 步而 FAIL，修复后重跑**，两次原始记录都保留在 `audits/P2-environment-check.md`。修复后 carry-over 优于 hard reset（epsilon 3.4068 vs 8.4969；agreement 0.33 vs 0.0755），说明仪器化有区分力，但随机未训练教师使绝对一致率无意义。
- 脚本数据路径已参数化为 `CTDG_FROZEN_STREAM` 环境变量，公开产物不写本机绝对路径。
- 依赖：`~/.codex/skills/` 17 个 `ccf-*` 只读复用；AutoResearchClaw 源码在历史 run 的 `dependencies/AutoResearchClaw/`（`import researchclaw` 成功，完整 CLI 需用户未提供的 LLM 凭据）。**全程未安装任何东西。**
- `goal-ledger.md`（E1/E2 PASS，E3–E5 待验证；授权档；四停止门均未触发）。

## Remaining

- **P3–P21 全部未开始**；无真实实验指标、无稿件、无 TeX/PDF。
- P3 绑定前置：训练非平凡轻量教师 + 状态衰减/归一化 + 重查 clipping rate；教师必须在 validation 胜过 B1/B2，否则退回 P2。
- 之后依次：P3A、P4 全矩阵与六消融、P5 强结果锁、P5A、P6–P21 写作/图表/引用/编译/交付。
- P12/P14 结构化 DOI/arXiv/标题查重；P20 官方作者指南硬性限制（当前 unknown）。
- E3/E4/E5 未 PASS，**目标尚未达成**。

## Live jobs

无。未启动任何长作业、无远程任务、无后台进程。

## Resume

1. 工作目录 `/Users/xhf/code/phd-project/phd-gnn2snn-dynamic-graph`（git 根），分支 `agent/lite-gnn2snn-dynamic/20261113-wb-lead`。
2. 依次读 `collaboration/PROTOCOL.md`、`PROJECT.md`、`TASK.md`、`goal-ledger.md`、本文件；再读 `auto-paper/20261113-210557/<TCAR 标题>/guidance.md`、`evaluation-protocol.md`、`ccfa-startup-packet/strong-result-feasibility-contract.md`，以及 `f-research-v1-run-20261113-211758-tcar/pipeline-state.md`、`audits/P2-environment-check.md`、`audits/ccfa-pre-experiment-action-ledger.md`、`experiment-traceability.md`。
3. 下一条命令：**P3 baseline-first**。在现有 run root 内实现并训练非平凡轻量 CTDG 教师（状态归一化），跑 B0/B1/B2/C0 并写入 `results/p3_*` 与 `experiment-traceability.md`；教师胜过 B1/B2 后才放行 C1–C4 与 M0。跑代码用 `/Users/xhf/miniconda3/bin/python`，数据路径用 `CTDG_FROZEN_STREAM`。
4. 停止条件：`goal-ledger.md` 第 8 节任一停止门触发；或 E1–E5 全 PASS 后由整合者验收。任何阶段未通过不得跳到写作或交付；`pipeline_state.py --complete` 必须返回 PASS 才能宣称 P21。
5. 续接者另建自己的 `agent/<task_id>/<agent_id>` 分支与 HANDOFF，保留本分支记录，不覆盖已有检查点。
