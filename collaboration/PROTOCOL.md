# Collaboration Protocol v1

本仓库按 `research-github-sync` 统一格式 v1 协作。协议只约束**记录与同步**，不替代科研目标、实验范围、验收指标或 `f-guidance-builder-v1` / `f-research-v1` 的科学流程。

## 仓库与分支

- 仓库：`ZtL-sysu/gnn2snn-dynamic-graph`（PUBLIC）。
- 默认分支：`main`，只放协作协议骨架与项目级索引。
- 每个工作者使用唯一 `agent_id` 和 `agent/<task_id>/<agent_id>` 分支；`task_id` / `agent_id` 用小写字母、数字、短横线。
- 本任务：`task_id = lite-gnn2snn-dynamic`，`agent_id = 20261113-wb-lead`，分支 `agent/lite-gnn2snn-dynamic/20261113-wb-lead`。
- 推送前先 `git fetch` 主线与相关 agent 分支；不在共享脏工作区 checkout / reset / stash。
- **合入 `main` 是验收结果**，仅由 `collaboration/PROJECT.md` 指定的整合者在验收后执行；agent 分支不得自行 merge、force push、删除远程分支或发布 Release。

## 单一写入者

| 文件 | 唯一写入者 |
|---|---|
| `collaboration/PROTOCOL.md`, `collaboration/PROJECT.md` | 整合者（用户 / 指定的 lead） |
| `collaboration/tasks/<task>/TASK.md` | task owner |
| `.../agents/<agent_id>/HANDOFF.md` | 该 agent |
| `.../agents/<agent_id>/LOG.md` | 该 agent（仅追加） |
| `.../agents/<agent_id>/checkpoints/<UTC-id>/` | 该 agent，发布后不回写；更正须发新检查点并引用旧记录 |
| 分配到的代码 / 结果路径 | TASK.md 中列明的 agent |

## 检查点规则

1. 在首次认领、重要结论形成、长实验启动/结束、失败/阻塞、交接前发布检查点；持续工作时每 15–30 分钟整理一次有意义的变化。
2. 每个检查点含 `CHECKPOINT.md` 与 `manifest.json`（由 `scripts/checkpoint_manifest.py` 生成 SHA-256 清单）；**有真实测量时**才建 `metrics.csv`（固定列见 FORMAT.md）。没有指标不造空表，未完成不写成成功。
3. 实验数字用 `metrics.csv` 固定列，一行一个真实指标，`status` ∈ `measured / failed / partial / historical`，目标值不混入实测表；均值与 SD 用独立 metric 名并保留每 seed 原值与 N。
4. 只 stage 本轮明确产物，**禁止 `git add .` / `git add -A`**；提交前检查 `git diff --cached --check` 与文件清单，去除凭证、私人对话、本机身份路径、缓存与重复大包。公开仓库上传范围必须过内容检查；单文件 > 50 MiB 默认不上传，记录相对路径/哈希/大小与后续存储安排。
5. commit 后 push 自己的分支，并用 `git ls-remote` 核对远程分支 SHA 与本地 HEAD 一致；只有远端确认才能写"已上传"，否则写"未同步"并给恢复命令。

## 状态语义

- `CHECKPOINT.md` 的 `in_progress / completed / blocked / failed` 是**工作状态**，`completed` 不自动代表科学主张成立。
- 旧日志不能证明进程仍活着或已停止；长作业必须记录 provider、真实 job_id、最近核实时间与恢复命令。
- 协议、split、baseline、选点、科学阈值发生实质改变时，按项目规则版本化并登记影响；旧结果保留，不得改哈希或改阈值把失败变成通过。

## 冲突与离线

- push 被拒：保留本地提交，fetch 后查清分支/owner，只在自己的干净分支处理明确冲突；不 force push、不覆盖远程、不无限重试。
- 网络失败最多一次即时重试；仍失败则记录未同步的本地 commit SHA 与恢复命令，继续本地授权工作，交接/结束再试一次。
