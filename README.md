# gnn2snn-dynamic-graph

轻量级 **GNN→SNN 转换 + 动态图** 研究的公开协作仓库。目标期刊：**Neurocomputing**（Elsevier，中科院二区，订阅/混合制）。

## 状态（2026-11-13）

`IN PROGRESS` — 基础设施与协议已建立；guidance 构建与实验流水线尚未完成。请以
`collaboration/PROJECT.md`、`goal-ledger.md` 和 `collaboration/tasks/lite-gnn2snn-dynamic/agents/20261113-wb-lead/HANDOFF.md`
为真实状态入口，不要以本文件推断科学结论。

## 目录

| 路径 | 用途 |
|---|---|
| `collaboration/PROTOCOL.md` | 协作、分支、检查点与合并规则 |
| `collaboration/PROJECT.md` | 用户目标、协议版本、事实来源、历史材料定位 |
| `collaboration/tasks/lite-gnn2snn-dynamic/` | 本任务范围、验收、agent 检查点 |
| `goal-ledger.md` | 死磕目标执行器状态账本（跨会话恢复的唯一进度载体） |
| `dependency-resolution.md` | 本机技能/工具依赖解析（含降级记录） |
| `docs/prior-repo-survey.md` | 对 `ZtL-sysu/gnn2snn` 静态图归档的只读调研 |
| `docs/prior-pipeline-survey.md` | 对本机历史动态图/GNN-SNN 流水线的只读调研 |
| `auto-paper/<timestamp>/<paper-title>/` | `f-guidance-builder-v1` 产物（guidance.md 等） |
| `auto-paper/<timestamp>/<paper-title>/f-research-v1-run-*/` | `f-research-v1` P0–P21 run root |

## 科学边界（已核实的约束）

- 已有 `gnn2snn` 归档只覆盖**静态**超像素图；其 affine-base 静态基缓存、`Wh₀+b` 一次计算、共享前缀、归一化门扰动界均假设图拓扑在一条转换轨迹内不变，不能直接搬到动态图。
- 本机 Apple M1 / 8 核 / 16 GB / MPS / 339 GB 可用磁盘；无 CUDA。原归档依赖 RTX 3060 12 GB 训练 55k 超像素图，本机不可复现，因此本项目只做**轻量**动态图事件流。
- 历史审计已封死两条路线：动态图 SNN 架构（SpikeNet / Dy-SIGN / Lite-SDGN 已占）、spike-proxy 稀疏执行/能耗故事（非神经形态硬件上不成立，2.54/5 CLOSE）。
- 未测量的东西不写成结果；`planned_claim` 与 `observed_finding` 严格分离。

## 复现环境

代码统一使用本机 Conda：`/Users/xhf/miniconda3/bin/python`（Python 3.14.6，torch 2.13.0，MPS 可用）。
