# Project: lightweight GNN→SNN conversion for dynamic graphs

## 用户目标

按用户自建科研流水线（`research-github-sync` → `f-guidance-builder-v1` → `f-research-v1`，全程由 `relentless-goal-executor` 守护）严格走完，产出一篇可投稿的**完整成稿**（TeX + 编译 PDF），目标为**老牌、非纯 OA 的中科院二区/三区期刊**，已锁定 **Neurocomputing**（Elsevier）。方向：针对本机算力做**轻量级** GNN→SNN 模型，**动态图**为大方向。

## 范围

- 方法族：ANN/GNN→SNN **转换**（weight scaling / threshold balancing / 差分或分级事件编码 / 转换误差界），不是新设计一个动态图 SNN 架构。
- 数据：直接公开可下载的小型动态图事件流；禁用需审批、付费、私有或联系作者的数据。
- 算力：本机 Apple M1 / 8 核 / 16 GB / MPS，无 CUDA；远程计算为**显式 opt-in**，默认不用。
- 交付：`auto-paper/<timestamp>/<paper-title>/` 下的 guidance 全套产物，以及其内 `f-research-v1-run-*` run root 中的 P0–P21 证据、六节结构稿件、`paper.tex`、`paper.pdf`、引用去重审计与交付清单。

## 不在范围

- 不做神经形态硬件能耗实测或 5× 能量主张（本机非神经形态硬件，历史审计已否决）。
- 不把 `spike proxy → 真实稀疏执行` 当主贡献（历史 `RealSparse-DyG` 2.54/5 CLOSE）。
- 不复用 `ZtL-sysu/gnn2snn` 的历史稿件（该稿被明确标注不可投稿）。
- 不上传模型权重、私有对话、凭证、本机绝对路径到大文件；公开仓库内容须过检查。

## 当前科学协议 / 指导文件及版本

| 项 | 状态 |
|---|---|
| `guidance.md` | **未生成**（`f-guidance-builder-v1` 进行中）。生成后路径写入本表并附 SHA-256 |
| `ccfa-startup-packet/feasibility-contract.json` | 未生成 |
| `guidance-pipeline-state.md` | 未生成（canonical order: CCFA-startup → G0…G8 → validation → handoff） |
| `f-research-v1` 的 `pipeline-state.json` | 未生成（canonical order: P0 → P1 → P1A → P1B → P2 … P21） |
| 协作协议 | `collaboration/PROTOCOL.md` v1 |

## 真实状态入口

1. `goal-ledger.md`（死磕账本，跨会话恢复唯一进度载体）
2. `collaboration/tasks/lite-gnn2snn-dynamic/agents/20261113-wb-lead/HANDOFF.md`
3. `auto-paper/<timestamp>/<paper-title>/guidance-pipeline-state.md` 与 run root 的 `pipeline-state.json`

**当前无任何实验结论、无稿件。** 本文件中所有"未生成"状态不得被后来的 agent 静默改写为 completed，除非对应产物真实存在且可核验。

## 历史材料定位

| 材料 | 位置 | 用途 |
|---|---|---|
| `ZtL-sysu/gnn2snn` 静态图归档 | 本仓库 `_refs/gnn2snn/`（本地只读克隆，.gitignore 排除）；远端 https://github.com/ZtL-sysu/gnn2snn | 差分源单元 `MTH_diff`、label-free 直方图校准、冻结协议 + 逐文件 SHA 证据纪律、`check_*.py` 回归框架、门控教师/基线代码；调研见 `docs/prior-repo-survey.md` |
| 历史动态图流水线 `RiskSet-DyG` | `/Users/xhf/full-paper/dynamic graph/d2/auto-paper/20260816-194553/…Robust Dynamic Link Forecasting/` | Zenodo 四个事件流、DyGLib/Base3/TPNet baseline 代码、时序 70/15/15 协议；调研见 `docs/prior-pipeline-survey.md` |
| 历史成稿范本 `paper-null-ladder` v1 | `/Users/xhf/Downloads/phd/4090/fly-gnn-snn-vision/papers/paper-null-ladder/` | 唯一走完 P21 的 9 页 TeX/PDF 格式范本 |
| 技能包 | `/Users/xhf/.codex/skills/ccf-*`（17 个）、`/Users/xhf/.workbuddy/skills/f-research-v1/bundled-skills/` | 见 `dependency-resolution.md` |

历史产物保持原路径，用索引引用，不为统一格式搬移或改写证据。

## 整合者与合并权限

- 整合者：用户（方序鸿）；本轮执行 lead 为 `20261113-wb-lead`，**无合并权限**。
- 只有整合者在验收后可把 agent 分支合入 `main`。
- 用户已选择**授权档**：一次性授权创建本公开仓库、本地文件写入、新建 conda 环境、运行实验、按本协议推送检查点；清单外操作（对外发送、删分支、改历史、合并主线、实际投稿）仍逐项确认。

## 未知项

- 目标期刊的现行官方作者指南硬性限制：待 P20 从 Elsevier 官方页面核实后写入 `submission-constraints.md`；当前不虚构页数/字数限制。
- 最终选题与 `expected_strong` 数值：待 G0–G8 与 CCFA startup 的证据核查后锁定。
