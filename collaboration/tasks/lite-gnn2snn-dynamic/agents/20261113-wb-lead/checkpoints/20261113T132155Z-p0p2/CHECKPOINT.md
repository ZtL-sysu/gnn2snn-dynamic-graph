# Checkpoint: 20261113T132155Z-p0p2

- Task / agent: `lite-gnn2snn-dynamic` / `20261113-wb-lead`
- Status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见 [manifest.json](manifest.json)）
- Manifest: [manifest.json](manifest.json)

## Changes and actual commands

发布 `f-research-v1` 的 P0–P2 阶段产物与**真实运行**的原型证据。所有产物在 guidance 目录内的 `f-research-v1-run-20261113-211758-tcar/` run root 中。

```bash
RR="<guidance-dir>/f-research-v1-run-20261113-211758-tcar"
mkdir -p "$RR"/{audits,results,scripts,paper,protocols,inputs,figures,writing,deliverables}
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-research-v1/scripts/pipeline_state.py --init "$RR/pipeline-state.json"
CTDG_FROZEN_STREAM=<local wikipedia-events.npz> /Users/xhf/miniconda3/bin/python "$RR/scripts/prototype_smoke.py"
/Users/xhf/miniconda3/bin/python _probe/build_research_state.py "$RR"
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-research-v1/scripts/pipeline_state.py "$RR/pipeline-state.json" --before P3
/Users/xhf/miniconda3/bin/python /Users/xhf/.workbuddy/skills/f-research-v1/scripts/pipeline_state.py "$RR/pipeline-state.json" --complete
```

`CTDG_FROZEN_STREAM` 由运行时环境变量提供，脚本内**不嵌入本机路径**。冻结标识 `inputs/frozen-identities.json` 用 SHA-256 记录四个流与 1024/4096 查询 ID 数组，原始 `.npz` 不上传。

## Checks and results

| 检查 | 实际输出 | 结论 |
|---|---|---|
| `pipeline_state.py --before P3` | `PASS: ordered, current evidence; scientific/visual gate judgment remains required.` (EXIT=0) | P0/P1/P1A/P1B/P2 依序 passed，哈希有效 |
| `pipeline_state.py --complete` | `ERROR: delivery requires every stage passed` (EXIT=1) | **预期失败**：P3–P21 仍 pending，明确证明未宣称完成 |
| 原型第 1 次运行 | agreement 0.003 / 0.038，mean_epsilon 13.99 / 10.78 | **FAIL**：IF 转换未真正展开 T 步且电流多除一个 T，SNN 几乎不发放脉冲 |
| 原型第 2 次运行（修复后） | agreement 0.0755 / 0.33，mean_epsilon 8.4969 / 3.4068，wall clock 0.981 s，clipping 0.001，mean_delta_v 0.3723 | 代码路径跑通；仪器化有区分力；carry-over 优于 hard reset（与 CRPI 定性一致） |
| MPS/CPU 算子探针 | torch 2.13.0，mps true，cuda false，mps matmul true，mps ReLU true | 加速器决策成立，CPU fallback 可用 |
| 冻结标识 | wikipedia 157,474 / mooc 411,749 / reddit 672,447 / lastfm 1,293,103 事件，各 val 1024 / test 4096，SHA-256 逐项记录 | G1 数据身份可复现，且明示非盲测 |

**本检查点仍无 `metrics.csv`**：唯一的数值来自 `coverage: smoke/2000-events` 的环境冒烟测试，明确标注为**非科学结果**，不进入正式实测表，也不得写进论文。

## Claims supported / still unproven

**已支持**：run root 路径包含关系成立；guidance 契约与 CCFA packet 通过 P1 复核；三条 binding claim 在 P1A 全部 `pass` 且目标未被下调；P1B 无未解决致命风险，所有 claim 标为 planned evidence；P2 的代码路径、算子、数据身份、逐事件仪器化、30 分钟原型里程碑均真实可核验（原型 0.981 s）。

**未支持 / 待验证**：任何机制有效性结论、`expected_strong` 的任何数值、真实教师训练、B0/B1/B2/C0 baseline、C1–C4 转换对照、六个消融、三流复制、统计检验、稿件、TeX/PDF、引用查重、期刊硬性限制。**E3/E4/E5 仍待验证，目标未达成。**

**原型修复的边界**：第 2 次运行的绝对一致率仍远低于 95% 门槛，因为教师是随机未训练、状态累加趋于饱和、候选打分近并列。P1B 已把「训练非平凡教师 + 状态归一化 + 重查校准覆盖率」设为 **P3 的绑定前置条件**；若失败必须退回 P2，不得带入 P4。

## Content review before upload

显式 stage，仅本轮产物；无 `git add .`；已复核无凭证、无 API key、无私人对话、无 >50 MiB 单文件（`raw_results.jsonl` 约 362 KB）。原型脚本的数据路径已参数化。早期两份调研文档含用户自有公开项目的本地路径代号，属项目索引而非隐私材料，保留不改（以免破坏已发布检查点的 manifest 哈希）；后续产物一律不写本机绝对路径。

## Decision and next action

继续 S2，下一步 **P3 baseline-first**：训练一个非平凡的轻量 CTDG 教师（含状态衰减/归一化，重查 clipping rate），先跑 B0/B1/B2/C0，验证教师胜过简单基线后，才允许进入 C1–C4 与 M0。全部原始日志与逐 seed 值写入 `results/p3_*`。

停止条件：`goal-ledger.md` 第 8 节任一停止门触发，或 E1–E5 全 PASS 后由整合者验收。当前无运行中的长作业、无远程任务、无后台进程。
