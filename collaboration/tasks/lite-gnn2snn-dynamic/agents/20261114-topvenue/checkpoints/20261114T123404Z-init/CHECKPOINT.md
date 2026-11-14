# Checkpoint: v4 cycle init (top-venue deepening)

- Task / agent: `lite-gnn2snn-dynamic` / `20261114-topvenue`
- Status: `in_progress`
- Protocol: `collaboration/PROTOCOL.md` v1（SHA-256 见 manifest.json）
- Base: wb-lead HEAD `509c4ed`（v3 final checkpoint 已核对远端一致）

## What changed

用户 2026-11-14 新指令开启 v4 周期：顶会学习（近 2 年 GNN→SNN/动态图）→ 蒸馏「顶会学习模式」→ 升级 `~/.codex/skills/f-guidance-builder-v1` → 按升级契约调 `f-research-v1` 加深实验与论文 → `research-github-sync` 同步。新 agent 分支 `agent/lite-gnn2snn-dynamic/20261114-topvenue` 建立；`goal-ledger.md` 追加 R6 行与第 10 节 v4 周期小节（历史不改写）。

## Jobs

4 个并行文献调研子代理运行中（SpikingGNN+conversion / CTDG / 转换理论 / 实验方法论）。产物将落盘 `docs/top-venue-study/`。

## Notes

- v3 交付物与判据原样保留；v4 走版本化契约 reopen-P0 路线。
- 本检查点无实验指标，故无 `metrics.csv`（协议：没有指标不造空表）。
