# Task: lite-gnn2snn-dynamic

- Owner: `20261113-wb-lead`（执行）；整合者/验收者：用户
- Input revision/branch: 新建仓库 `ZtL-sysu/gnn2snn-dynamic-graph`，初始 `main` 骨架；输入材料见 `collaboration/PROJECT.md` 历史材料定位
- Protocol: `collaboration/PROTOCOL.md` v1；协作格式 `research-github-sync/references/FORMAT.md` v1
- Goal: 依序跑完 `f-guidance-builder-v1`（CCFA-startup → G0…G8 → validation → handoff）产出合格 `guidance.md`，再由 `f-research-v1` 以该 guidance 为契约跑完 P0…P21，交付 Neurocomputing 目标成稿（TeX + 编译 PDF + 完整证据包）
- Acceptance（可判定，须逐条有证据）:
  1. 公开仓库存在 `collaboration/` 骨架与本任务 agent 分支检查点，`git ls-remote` 远程 SHA 与本地 HEAD 一致；
  2. `guidance.md` 通过 `validate_guidance.py --strict --packet <ccfa-startup-packet>`；`guidance-pipeline-state.md` 证明所有必需阶段**依序** `passed`，无跳过/倒填；
  3. `pipeline-state.json` 证明 P0…P21 依序 `passed`；run root 内有 `paper.tex` 与编译成功的 `paper.pdf`，且 clean-extraction 重编译结果一致；
  4. guidance 承诺的每个实验 `done`，主 claim 达到预先锁定的 `expected_strong`，baseline 先于方法结论，逐 seed 原始日志 / `metrics.csv` 可回溯；
  5. 稿件为规定的 1–6 节结构，引用真实且去重审计通过，目标期刊硬性限制有官方来源记录，且 `paper-guidance-audit.md` 无未覆盖项。
- Out of scope: 实际投稿、发邮件、合并 `main`、force push、删除远程分支、上传 >50 MiB 单文件、私有/受限数据、神经形态能耗实测、`spike proxy → 真实稀疏执行` 主贡献
- Dependencies: 本机 `~/.codex/skills/ccf-*` 技能包（只读复用）；`f-research-v1/bundled-skills/`；本机 Conda Python；Zenodo 公开事件流；`ZtL-sysu/gnn2snn` 归档代码
- Writers:
  - `20261113-wb-lead` → `collaboration/tasks/lite-gnn2snn-dynamic/agents/20261113-wb-lead/**`、`goal-ledger.md`、`dependency-resolution.md`、`docs/**`、`auto-paper/**`
  - 整合者 → `collaboration/PROTOCOL.md`、`collaboration/PROJECT.md`、本 `TASK.md`
  - 一个文件只有一个写入者；发现同一路径或同一实验被认领时先协调，不重复启动、不覆盖
- Execution: 本机 `conda` `/Users/xhf/miniconda3/bin/python`；Apple M1 / 8 核 / 16 GB / MPS / 339 GB 可用磁盘；默认不远程；split/seed 规则由 guidance 冻结并经 P1A 锁定；检查点每 15–30 分钟或关键结论时一次，显式 stage、SHA-256 清单、核对远程 SHA
- Change control: 目标、split、baseline、选点、`expected_strong` 或科学阈值的实质改变，须由 task owner 版本化并登记影响，旧结果保留；协议/任务变更由整合者更新，agent 分支上的自报结果不得直接覆盖全局结论
- Stop condition: `goal-ledger.md` 第 8 节四停止门任一触发；或证据清单 E1–E5 全 PASS 后由整合者验收停止
