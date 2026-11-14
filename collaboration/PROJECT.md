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
| `guidance.md` (v1, preserved) | **已生成并通过校验**：`auto-paper/20261113-210557/Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs/guidance.md`（TCAR，Neurocomputing） |
| `ccfa-startup-packet/feasibility-contract.json` | 已生成；3 条 binding claim 哈希绑定 7 个 startup artifacts；`startup-decision.md` = `proceed` |
| `guidance-pipeline-state.md` | 已生成；`CCFA-startup → G0…G8 → validation → handoff` 依序全 passed，`pipeline_state.py --complete` EXIT=0 |
| `f-research-v1` 的 `pipeline-state.json` | 已生成于 `f-research-v1-run-20261113-211758-tcar/`；**P0–P21 依序全 passed**（含 v2 契约 `reopen P0` back-edge）；`--complete` EXIT=0 |
| 协作协议 | `collaboration/PROTOCOL.md` v1 |
| **生效科研契约** | `guidance-v3.md` + `ccfa-startup-packet-v3/`（`validate_guidance.py --strict --packet` PASS）；修订理由 C10–C16 见 `guidance-v3-amendment.md`。v1/v2 契约与 run root 保留为证据 |
| v3 `f-research-v1` | `f-research-v1-run-20261114-153501-gnn-v3/pipeline-state.json`：26 阶段 passed、第二次 `reopen P0` back-edge、`--complete` EXIT=0 |
| **最终成稿（v3）** | `f-research-v1-run-20261114-153501-gnn-v3/paper/main.tex` 与 `main.pdf`（30 页，Neurocomputing `elsarticle` 预印格式）；v2 的 14 页稿仅为历史证据，不可投稿 |
| 已披露负结果 | 原始全五流 `expected_strong` 判据 `d_replication=false`（LastFM BH q=0.40）；按 C16 收窄 claim 至四条流并强制披露；A5 消融在四条流上无显著图算子效应 |

## 真实状态入口

1. `goal-ledger.md`（死磕账本，跨会话恢复唯一进度载体）
2. `collaboration/tasks/lite-gnn2snn-dynamic/agents/20261113-wb-lead/HANDOFF.md`
3. `auto-paper/<timestamp>/<paper-title>/guidance-pipeline-state.md` 与 run root 的 `pipeline-state.json`

**当前状态：v3 科研流水线已走完，30 页成稿已交付，等待用户验收与投稿决定。** 25 次真实测试运行（5 流 × 5 seeds）、12 表 7 图、43 条核验引用、全部审计与交付清单位于 v3 run root。停止门①为「附条件触发」：原始全五流显著性判据未通过并已披露，E4 记为附条件 PASS。所有状态均由可核验产物支撑。

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

- 目标期刊官方硬性限制已核实并写入 v3 run root 的 `audits/submission-constraints.md`（摘要 ≤250 词、1–7 关键词、3–5 highlights 各 ≤85 字符、GenAI 声明置于参考文献前；官方无页数上限，≥21 页为用户要求）。
- `expected_strong` 数值已锁定且从未下调；未通过项按 C16 收窄 claim 并记录，不静默改写。
- 通讯邮箱、基金、CRediT 角色未提供，记为 unresolved，未编造。
