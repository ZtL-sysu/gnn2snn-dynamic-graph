# Checkpoint: 20261113T131524Z-guidance

- Task / agent: `lite-gnn2snn-dynamic` / `20261113-wb-lead`
- Status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见 [manifest.json](manifest.json)）
- Manifest: [manifest.json](manifest.json)

## Changes and actual commands

本检查点发布 `f-guidance-builder-v1` 的完整产物与校验证据。**仍无任何实验结果或稿件。**

实际执行（工作目录为仓库根，`RUN` 为 `auto-paper/20261113-210557/Topology-Change-Aware Residual Carry-over for Low-Latency GNN-to-SNN Conversion on Dynamic Graphs/`）：

```bash
gh repo clone ZtL-sysu/gnn2snn _refs/gnn2snn -- --depth=1
curl -sS "https://zenodo.org/api/records/7213796"                 # HTTP 200, CC BY 4.0
curl -sS -I "https://zenodo.org/api/records/7213796/files/enron.zip/content"   # HTTP 200 attachment
/Users/xhf/miniconda3/bin/python -c "import numpy; numpy.load(...)"  # 四个冻结 npz 全部可读
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/hardware_probe.py
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py --init "$RUN/pipeline-state.json"
/Users/xhf/miniconda3/bin/python _probe/build_state.py "$RUN"
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/validate_guidance.py "$RUN/guidance.md" --strict --packet "$RUN/ccfa-startup-packet"
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py "$RUN/pipeline-state.json" --complete
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py "$RUN/pipeline-state.json" --before G0
```

真实文献检索（WebSearch，2026-11-13）覆盖：ANN→SNN 转换误差理论（SNNC-AP arXiv:2205.10121、CASC S0020025524007369、BayesianSpikeFusion 2024）、跨步误差放大（CRPI arXiv:2601.21778 ICML 2026、Spiking DiTs MPEF ICML 2026）、CTDG 基线（TAMI NeurIPS 2025、HyperEvent arXiv:2507.11836、TGB leaderboard、DyGLib）、Neurocomputing 期刊事实。

新增产物：`RUN/guidance.md`、`guidance-pipeline-state.md`、`pipeline-state.json`、`validation-report.md`、`hardware-profile.md`、`dataset-access-log.md`、`scenario-decision-log.md`、`literature-baseline-matrix.md`、`novelty-feasibility-report.md`、`theoretical-feasibility-audit.md`、`story-strength-audit.md`、`evaluation-protocol.md`；`RUN/ccfa-startup-packet/` 下 7 个 Markdown + `feasibility-contract.json`；`auto-paper/generated-research-directions.md` 追加一行。

## Checks and results

| 检查 | 实际输出 | 结论 |
|---|---|---|
| `validate_guidance.py --strict --packet` | `Guidance structure is valid.` (EXIT=0) | 必需章节、strict 厚度、六节 canonical outline、占位符、packet 七文件与三条 claim 的哈希绑定全通过 |
| `pipeline_state.py --complete` | `PASS: ordered, current evidence; scientific/visual gate judgment remains required.` (EXIT=0) | 12 阶段依序 passed，contract/inputs/evidence 哈希有效，history 顺序一致 |
| `pipeline_state.py --before G0` | 同上 PASS (EXIT=0) | G0 前置全部通过 |
| Zenodo 数据访问 | API HTTP 200；文件 HEAD HTTP 200 + attachment；CC BY 4.0 | G1 直接公开可下载成立 |
| 本地冻结流 | 4 个 `.npz` 均 `numpy.load` 成功，数组形状/查询 ID 已记录 | 数据可用 |

**本检查点仍无 `metrics.csv`**：guidance 阶段不产生任何实验测量，按 FORMAT.md 不造空表。

## Claims supported / still unproven

**已支持**：guidance 契约结构合格、阶段顺序完整且哈希可核验；Zenodo 四个事件流直接公开且本机可读；本机 M1/MPS 无 CUDA；CRPI（ICML 2026）确为最强新颖性威胁且已被写成 `must-rerun` 对照；Neurocomputing 为 1989 年创刊、Elsevier、中科院计算机 2 区、JCR AI Q1、默认非 OA；AutoResearchClaw 完整源码本机存在且 `researchclaw` 包可 import。

**未支持 / 待验证**：机制有效性（误差界、拓扑变化项、TCAR 增益）、任何 `expected_strong` 数值、教师训练可行性、P2 30 分钟原型、结构化 DOI/arXiv 查重（P12/P14）、目标期刊官方硬性限制（P20）、任何 TeX/PDF 成稿。新颖性置信度为**中等**，不是已确证。

**明确不作为证据**：历史归档的 5× 能量主张、`0.650→0.295` 计划值、`gnn2snn` 历史稿、affine 一致率（非 ground-truth 准确率）、TGN 单 seed 超时产生的 validation MRR。

## Decision and next action

继续 S1，进入 `f-research-v1` P0：在 `RUN/` 内创建 `f-research-v1-run-<YYYYMMDD-HHMMSS>-tcar/`，初始化其 `pipeline-state.json`（26 阶段）与 `pipeline-state.md`，把本 `guidance.md` 作为契约，依序执行 P1、P1A（强结果锁）、P1B（预实验对抗评审）、P2（环境与 30 分钟原型）。**P3 之前不得声称任何方法优越性。**

停止条件：`goal-ledger.md` 第 8 节任一停止门触发，或 E1–E5 全 PASS 后由整合者验收。当前无运行中的长作业、无远程任务、无后台进程。
