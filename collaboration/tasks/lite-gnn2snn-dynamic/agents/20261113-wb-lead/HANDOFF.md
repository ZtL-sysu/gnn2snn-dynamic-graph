# Handoff: lite-gnn2snn-dynamic / 20261113-wb-lead

- Updated: 2026-11-13T20:58:54+0800
- Branch: `agent/lite-gnn2snn-dynamic/20261113-wb-lead`
- Work status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见首个检查点 `manifest.json`）
- Latest checkpoint: `checkpoints/20261113T125854Z-init/`
- Sync: 待首次 push 后填写（远程分支 + 已核验 commit SHA）

## Established

- 核实本机算力：Apple M1 / 8 核 / 16 GB / MPS / 339 GB 可用磁盘；`hardware_probe.py` 输出见 `docs/hardware-profile.md`（`recommended_device: mps`，`cuda_available: false`）。
- 核实 GitHub 账号 `ZtL-sysu` 已登录；新建 PUBLIC 仓库 `ZtL-sysu/gnn2snn-dynamic-graph`。
- 完成两份只读调研：`docs/prior-repo-survey.md`（`ZtL-sysu/gnn2snn` 静态图归档）、`docs/prior-pipeline-survey.md`（本机历史动态图/GNN-SNN 流水线）。二者结论均为**已核实事实**，不是科学成果。
- 依赖解析完成：`dependency-resolution.md`。17 个 `ccf-*` 从 `~/.codex/skills/` 只读复用，未安装；AutoResearchClaw CLI 缺失，按 vendored `0-autoresearch-skill` 规范做本地等价执行并如实标注。
- 目标锁定与证据清单：`goal-ledger.md`（E1–E5，授权档，四停止门均未触发）。
- 已知方向判断：**GNN→SNN 转换作为动态图主机制在历史项目中是空白**；动态图 SNN 架构与 spike-proxy 稀疏执行两条路线已被历史审计封死；四个 Zenodo 事件流与 DyGLib 代码本机可复用；强基线 TGN 历史单 seed 8 h 超时。

## Remaining

- `f-guidance-builder-v1` 全部阶段（CCFA-startup、G0–G8、validation、handoff）未开始；`guidance.md` 不存在。
- G0/G4 需要真实文献检索（SpikeNet、Dy-SIGN、Lite-SDGN、ANN→SNN 转换近作、Neurocomputing 近 3–5 年），尚未做。
- G1 需要实测 Zenodo 数据集下载，尚未做。
- `f-research-v1` P0–P21 全部未开始；**无任何实验、无任何稿件、无任何指标**。
- 目标期刊官方作者指南硬性限制待 P20 核实，当前为 unknown，不虚构。

## Live jobs

无。本轮未启动任何长作业、无远程任务、无后台进程；`PAUSE_SNAPSHOT` 类状态不适用于本仓库。

## Resume

1. 工作目录：`/Users/xhf/code/phd-project/phd-gnn2snn-dynamic-graph`（git 根）。
2. 读 `collaboration/PROTOCOL.md`、`collaboration/PROJECT.md`、`collaboration/tasks/lite-gnn2snn-dynamic/TASK.md`、`goal-ledger.md` 与本文件；再读 `docs/prior-repo-survey.md` 与 `docs/prior-pipeline-survey.md`。
3. 下一条命令：按 `f-guidance-builder-v1` 在 `auto-paper/<yyyyMMdd-HHmmss>/<paper-title>/` 建 `guidance-pipeline-state.md` 与 `pipeline-state.json`，先跑 `CCFA-startup`，依序 G0→G8。脚本：`/Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py`（用 `/Users/xhf/miniconda3/bin/python`）。
4. 停止条件：`goal-ledger.md` 第 8 节任一停止门触发；或 E1–E5 全 PASS 后由整合者验收。
5. 续接者另建自己的 `agent/<task_id>/<agent_id>` 分支与 HANDOFF，保留本分支记录，不覆盖本检查点。
