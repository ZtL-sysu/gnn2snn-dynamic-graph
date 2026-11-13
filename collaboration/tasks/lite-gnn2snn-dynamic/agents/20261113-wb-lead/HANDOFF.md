# Handoff: lite-gnn2snn-dynamic / 20261113-wb-lead

- Updated: 2026-11-13T21:15:24+0800
- Branch: `agent/lite-gnn2snn-dynamic/20261113-wb-lead`
- Work status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见首个检查点 `manifest.json`）
- Latest checkpoint: `checkpoints/20261113T131524Z-guidance/`
- Sync: `main` = `75aee0ef95f57f6c8a12285e596aac3b3998c9ba`；agent 分支首检查点 = `96afc0194d504c16b0eff38194f8e4e8e2d8a0e7`，`git ls-remote` 已核对远程与本地一致。guidance 检查点待本轮推送后补 SHA。

## Established

- **E1 PASS**：公开仓库 `ZtL-sysu/gnn2snn-dynamic-graph` 已建，`collaboration/` 协议、账本、两份只读调研与首个 SHA-256 检查点已上传，远程 SHA 与本地 HEAD 一致。
- **E2 PASS**：`f-guidance-builder-v1` 全套产物完成并通过校验。`validate_guidance.py --strict --packet` 输出 `Guidance structure is valid.`；`pipeline_state.py --complete` 与 `--before G0` 输出 `PASS: ordered, current evidence`。见 `auto-paper/20261113-210557/.../validation-report.md`。
- Guidance 契约：`auto-paper/20261113-210557/Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs/guidance.md`，题目 TCAR，目标 Neurocomputing，`ccfa-startup-packet/startup-decision.md` = `proceed`。
- 真实文献检索命中 CRPI（arXiv:2601.21778, ICML 2026）与 Spiking DiTs MPEF（ICML 2026）为最强新颖性威胁，据此把机制重定义为「事件轴转换误差递推 + 拓扑变化项 + 事件门控重校准」，并把 CRPI 提升为 `must-rerun` 对照。新颖性置信度为**中等**，待 P12/P14 结构化查重。
- G1 实测：Zenodo `10.5281/zenodo.7213796` API HTTP 200、CC BY 4.0、文件 HEAD HTTP 200 + attachment；四个本地冻结 `.npz`（Wikipedia/MOOC/Reddit/LastFM）均 `numpy.load` 成功，查询 ID 形状已记录。
- 依赖：`~/.codex/skills/` 17 个 `ccf-*` 只读复用；AutoResearchClaw 完整源码在历史 run 的 `dependencies/AutoResearchClaw/`，`import researchclaw` 实测成功（完整 CLI 需用户未提供的 LLM 凭据）。**全程未安装任何东西。**
- 目标锁定与证据清单：`goal-ledger.md` v1.1（E1/E2 PASS，E3–E5 待验证；授权档；四停止门均未触发）。

## Remaining

- `f-research-v1` P0–P21 **尚未开始**；**无任何实验、无任何指标、无任何稿件**。
- P2 的 30 分钟单 seed 原型是绑定条件，未完成前不得放行 P3。
- P3 baseline-first（B0/B1/B2/C0）必须早于任何方法优越性结论。
- P12/P14 结构化 DOI/arXiv/标题查重；P20 目标期刊官方作者指南硬性限制（当前 unknown，不虚构）。
- E3/E4/E5 未 PASS，因此**目标尚未达成**，本任务仍 `in_progress`。

## Live jobs

无。未启动任何长作业、无远程任务、无后台进程。

## Resume

1. 工作目录 `/Users/xhf/code/phd-project/phd-gnn2snn-dynamic-graph`（git 根），分支 `agent/lite-gnn2snn-dynamic/20261113-wb-lead`。
2. 依次读 `collaboration/PROTOCOL.md`、`collaboration/PROJECT.md`、`collaboration/tasks/lite-gnn2snn-dynamic/TASK.md`、`goal-ledger.md`、本文件，再读上述 `guidance.md` 与其 `validation-report.md`、`evaluation-protocol.md`、`strong-result-feasibility-contract.md`。
3. 下一条命令：在 guidance 所在目录内创建 `f-research-v1-run-<YYYYMMDD-HHMMSS>-tcar/`，用 `/Users/xhf/.workbuddy/skills/f-research-v1/scripts/pipeline_state.py --init` 初始化 26 阶段 `pipeline-state.json`，然后依序执行 P0 → P1 → P1A → P1B → P2。所有产物必须留在该 run root 内。用 `/Users/xhf/miniconda3/bin/python` 跑代码。
4. 停止条件：`goal-ledger.md` 第 8 节任一停止门触发；或 E1–E5 全 PASS 后由整合者验收。任何阶段未通过不得跳到写作或交付。
5. 续接者另建自己的 `agent/<task_id>/<agent_id>` 分支与 HANDOFF，保留本分支记录，不覆盖已有检查点。
