# Checkpoint: 20261113T125854Z-init

- Task / agent: `lite-gnn2snn-dynamic` / `20261113-wb-lead`
- Status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见 [manifest.json](manifest.json)）
- Manifest: [manifest.json](manifest.json)

## Changes and actual commands

本检查点只发布**基础设施与已核实事实**，不含任何实验结果或科学结论。

实际执行的命令（均在 `/Users/xhf/code/phd-project/phd-gnn2snn-dynamic-graph`）：

```bash
uname -a; uname -m; sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize; system_profiler SPDisplaysDataType
gh auth status; gh repo list --limit 200 --json name,description,visibility,updatedAt
gh repo clone ZtL-sysu/gnn2snn _refs/gnn2snn -- --depth=1
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/hardware_probe.py
gh repo create ZtL-sysu/gnn2snn-dynamic-graph --public --description "..."
gh repo view ZtL-sysu/gnn2snn-dynamic-graph --json name,visibility,url,defaultBranchRef
```

随后写入：`README.md`、`.gitignore`、`collaboration/PROTOCOL.md`、`collaboration/PROJECT.md`、
`collaboration/tasks/lite-gnn2snn-dynamic/TASK.md`、
`collaboration/tasks/lite-gnn2snn-dynamic/agents/20261113-wb-lead/{HANDOFF.md,LOG.md}`、
`goal-ledger.md`、`dependency-resolution.md`、
`docs/{hardware-profile.md,prior-repo-survey.md,prior-pipeline-survey.md}`。

`collaboration/` 骨架的首个 `main` 提交由本 lead 代整合者完成（仓库初始化的一部分）；此后所有工作产物只提交到 `agent/lite-gnn2snn-dynamic/20261113-wb-lead` 分支，不自行合并 `main`。

## Checks and results

| 检查 | 结果 | 证据 |
|---|---|---|
| 本机算力 | 实测 Apple M1 / 8 核 / 16 GB / MPS / 339 GB 可用磁盘，`cuda_available: false` | `docs/hardware-profile.md` |
| GitHub 认证与仓库创建 | `gh auth status` 已登录 `ZtL-sysu`；`gh repo view` 返回 `visibility: PUBLIC` | 远端 https://github.com/ZtL-sysu/gnn2snn-dynamic-graph |
| 技能依赖 | `~/.codex/skills/` 含 17 个 `ccf-*`；AutoResearchClaw CLI 全盘未发现 | `dependency-resolution.md` |
| 历史材料 | 两份只读调研产出，结论均指向具体历史文件路径 | `docs/prior-repo-survey.md`、`docs/prior-pipeline-survey.md` |
| manifest 生成与校验 | `checkpoint_manifest.py create` 后 `verify` | 本目录 `manifest.json` |

**本检查点无 `metrics.csv`**：尚无任何真实测量指标，按 FORMAT.md 不造空结果表。

## Claims supported / still unproven

**已支持（事实层）**：仓库已创建且为 PUBLIC；本机无 CUDA、MPS 可用；`gnn2snn` 归档只覆盖静态图且已暂停；历史动态图流水线有四个 Zenodo 事件流与 DyGLib 代码可复用；TGN 单 seed 曾 28,800 s 超时、强基线零 test 指标；历史审计封死了动态图 SNN 架构与 spike-proxy 稀疏执行两条路线。

**未支持 / 待验证**：任何关于新方法有效性、转换等价性、误差界、精度/脉冲/延迟 Pareto 的结论；`GNN→SNN 转换 × 动态图` 的新颖性（须由 G0/G4 真实文献检索判定，当前只是基于本机历史项目的**局部**观察，不等于文献无重复）；Zenodo 数据集在本机的实际可下载性（G1 待实测）；目标期刊现行官方硬性限制（P20 待核实）；任何 `expected_strong` 数值（尚未锁定）。

**明确不作为证据**：历史归档中的 5× 能量主张、`0.650→0.295` 计划值、`paper/historical-draft/` 历史稿、`affine` 一致率（非 ground-truth 准确率）。

## Decision and next action

继续 S1。下一步：按 `f-guidance-builder-v1` 在 `auto-paper/<yyyyMMdd-HHmmss>/<paper-title>/` 初始化
`guidance-pipeline-state.md` 与 `pipeline-state.json`，先完成 `CCFA-startup`（startup-stage-plan / idea-cards /
prior-art-opportunity-map / idea-red-team-review / claim-evidence-matrix / strong-result-feasibility-contract /
startup-decision / feasibility-contract.json），再依序 G0→G8。

G0/G4 必须做真实文献检索；G1 必须实测数据集下载；G3 必须给出可证伪的机制与消融；G5/G6 必须正视 M1 算力与历史强基线超时教训；G7 的 `expected_strong` 必须 baseline-calibrated，不得编造。

停止条件：`goal-ledger.md` 第 8 节任一停止门触发，或 E1–E5 全 PASS 后由整合者验收。无运行中的长作业。
