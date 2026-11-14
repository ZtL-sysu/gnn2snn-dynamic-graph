- Updated: 2026-11-14T09:09:14+0800
- Branch: `agent/lite-gnn2snn-dynamic/20261113-wb-lead`
- Work status: `completed` (scientific pipeline delivered; user acceptance and submission still pending)
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见首个检查点 `manifest.json`）
- Latest checkpoint: `checkpoints/20261114T010914Z-final/`
- Sync: `main` = `75aee0ef95f57f6c8a12285e596aac3b3998c9ba`；历史检查点 `96afc01…`(init)、`3fca914…`(guidance)、`a727681…`(P0–P2)。最终检查点待本轮推送后补 SHA。

## Established

- **E1–E5 全 PASS；停止门①（达成）已触发。** 账本 `goal-ledger.md` v1.3。
- `f-research-v1` 的 `pipeline-state.json` 证明 P0–P21 依序全 `passed`（含 `reopen P0` 的 v2 契约 back-edge），`pipeline_state.py --complete` EXIT=0。
- **成稿**：`auto-paper/20261113-210557/<TCAR 标题>/f-research-v1-run-20261113-211758-tcar/paper/main.tex` 与 `paper/main.pdf`（14 页）。六节结构、18 条经核验引用、4 张图、2 张表、GenAI 声明、摘要 238 词（≤250）。干净目录重编译文本与验收版完全一致。
- **实验**：3 条公开流 × 5 seeds = 15 次测试，11 个方法/消融，T/γ/窗口扫描，配对 bootstrap + BH 校正。主结果：M0 agreement 0.9990/0.9949/0.9969，MRR 保持 ≥0.9988，`ε_k` 在所有流严格最低，触发率 0.197/0.129/0.049。`d_three_streams=true`。
- **诚实负结果已写进稿件**：离散记忆主导绝对 MRR（EdgeBank 0.947 vs 教师 0.304）、agreement 饱和、MOOC/Enron 效应量仅 20.9%/3.7%、相对降幅非单调、测试 ID 非盲、无神经形态能耗实测。
- **9 次修正循环 C1–C9 全部留痕**：`correction-loop-state.md`、`correction-ledger.md`、`guidance-v2-amendment.md`。v1 契约与校验记录保留未改；v2 通过 strict 校验。
- 目标期刊 Neurocomputing：官方硬性限制已核实并满足（摘要/关键词/highlights/引用/GenAI 声明）。

## Remaining

- 用户验收与决定是否投稿；对应邮箱、基金、CRediT 角色未提供，记为 unresolved，未编造。
- Figure 1 使用本地矢量示意图（图像生成需额外积分，未在授权清单内）；如用户授权可重做并重编译。
- AutoResearchClaw CLI 未运行（需用户未提供的 LLM 凭据），写作阶段按本地源码契约等价执行并如实标注。
- 新颖性置信度中等，未做 Scopus/IEEE 全库查重；正式投稿前建议补做。
- 本仓库未合并 `main`、未发布 Release、未投稿。

## Live jobs

无。所有后台作业已结束，无远程任务、无后台进程。

## Resume

1. 读 `goal-ledger.md`、`collaboration/PROJECT.md`、本文件，再看 run root 的 `pipeline-state.md`、`audits/final-audit-note.md`、`deliverables/manifest.json`。
2. 若需修改稿件：编辑 `paper/main.tex` → 在 `paper/` 下 `pdflatex` → `bibtex` → `pdflatex` ×2 → 重新跑 `_probe/finalize_artifacts.py`、`_probe/build_final_state.py` 与 `pipeline_state.py --complete`，再发新检查点（旧检查点不回写）。
3. 停止条件：停止门①已触发；用户叫停为最高优先级。
4. 续接者另建自己的 `agent/<task_id>/<agent_id>` 分支与 HANDOFF，不覆盖已有检查点。
