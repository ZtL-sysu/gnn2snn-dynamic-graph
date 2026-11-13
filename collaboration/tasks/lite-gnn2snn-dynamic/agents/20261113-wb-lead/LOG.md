# LOG: lite-gnn2snn-dynamic / 20261113-wb-lead

仅追加。时间带时区；结果区分实测与推断；失败只记简明摘要与必要反例。

- 2026-11-13T20:34+0800 | 目标启动，加载 4 个技能规范（research-github-sync / f-guidance-builder-v1 / f-research-v1 / relentless-goal-executor） | 确认流水线为严格依序 gate，不可跳关；`f-research-v1` 要求所有产物在 guidance 目录内的 run root | 规范文件
- 2026-11-13T20:35+0800 | 硬件与 GitHub 环境探测 | 实测：Apple M1 / 8 核 / 16 GB / 8 核 GPU / 316–339 GB 可用磁盘；conda Python 3.14.6；torch 2.13.0 + MPS；`pdflatex/xelatex/latexmk` 齐全；`gh` 登录 `ZtL-sysu` | 本检查点 `docs/hardware-profile.md`
- 2026-11-13T20:36+0800 | 克隆并深读 `ZtL-sysu/gnn2snn` | 实测：静态超像素图 ANN→SNN 转换，三种子 T4/T8 教师一致率 99.5%+；2026-11-13 暂停，无稿件级成果；动态图为空白且理论前提冲突 | `docs/prior-repo-survey.md`
- 2026-11-13T20:40+0800 | 依赖盘点 | 发现 `ccf-*` 与 AutoResearchClaw CLI 不在 WorkBuddy 注册路径；`f-research-v1/bundled-skills/` 9 个写作/编译子技能在 | `dependency-resolution.md`
- 2026-11-13T20:42+0800 | 用户决策锁定 | 新建公开仓库 `gnn2snn-dynamic-graph`；目标期刊 Neurocomputing；依赖处理选「先安装」；确认档位授权档 | `goal-ledger.md` 第 1/7 节
- 2026-11-13T20:45+0800 | 用户追加指令改道 | 「没有的技能你可以去本地的 codex 目录下找来用，不用再装了」→ 依赖策略由「安装」改为「只读复用 `~/.codex/skills/`」；败因归类：条件不备已由用户指令解决 | `goal-ledger.md` 第 6 节 R1
- 2026-11-13T20:47+0800 | 依赖解析 | 实测 `~/.codex/skills/` 含 17 个 `ccf-*` + f 系列；AutoResearchClaw CLI 全盘未发现，按 `dependency-map.md` 降级为 vendored 规范等价执行；未执行任何安装 | `dependency-resolution.md`
- 2026-11-13T20:48+0800 | 创建公开仓库 | `gh repo create ZtL-sysu/gnn2snn-dynamic-graph --public` 成功，`gh repo view` 确认 `visibility: PUBLIC` | 远端 https://github.com/ZtL-sysu/gnn2snn-dynamic-graph
- 2026-11-13T20:49+0800 | 运行硬件探针 | 实测输出：`cpu_count 8`, `memory_bytes 17179869184`, `torch.mps_available true`, `cuda_available false`, `recommended_device mps`, `disk_free 339078103040`；探针的 `--output` 参数不被支持（只打印 JSON），已把打印结果落盘为 `docs/hardware-profile.md`，**未伪造文件输出** | `docs/hardware-profile.md`
- 2026-11-13T20:52+0800 | 历史动态图流水线调研 | 实测核实：4 个 Zenodo 事件流（CC BY 4.0）与 DyGLib 代码本机存在；TGN 单 seed 28,800 s 超时、强基线零 test 指标；动态图 SNN 架构与 spike-proxy 稀疏执行已被历史审计封死；GNN→SNN 转换主机制在历史项目中无重复 | `docs/prior-pipeline-survey.md`
- 2026-11-13T20:58+0800 | 落盘协议、账本、任务与检查点 | 建立 `collaboration/` v1、`goal-ledger.md` v1.0、TASK、HANDOFF、本 LOG 与首个 CHECKPOINT；准备按 FORMAT.md 生成 manifest 并推送 | 首个检查点
- 2026-11-13T21:00+0800 | 推送首个检查点 | `checkpoint_manifest.py create/verify` 均通过（12 artifacts）；`git push` 成功；`git ls-remote` 显示 agent 分支 `96afc0194d504c16b0eff38194f8e4e8e2d8a0e7` = 本地 HEAD，`main` = `75aee0ef…`。**E1 PASS** | 远端 https://github.com/ZtL-sysu/gnn2snn-dynamic-graph
- 2026-11-13T21:02+0800 | 真实文献检索 G0/G4 | 实测确认转换误差递推公式、CRPI(ICML 2026 arXiv:2601.21778) 与 MPEF(ICML 2026) 是最强威胁；TAMI(NeurIPS 2025)、HyperEvent、TGB leaderboard 为近期强基线；Neurocomputing 1989 创刊/Elsevier/中科院计算机 2 区/非 OA | `literature-baseline-matrix.md`、`prior-art-opportunity-map.md`
- 2026-11-13T21:05+0800 | G1 数据访问实测 | Zenodo API HTTP 200 / CC BY 4.0 / 15 个直链；enron.zip HEAD HTTP 200 + attachment；4 个本地冻结 npz 全部 `numpy.load` 成功并读出数组形状与 1024/4096 查询 ID | `dataset-access-log.md`
- 2026-11-13T21:05+0800 | 发现本地 AutoResearchClaw 源码 | 历史 run 的 `dependencies/AutoResearchClaw/` 含 `pyproject.toml` 与 `researchclaw/` 包；`PYTHONPATH` 下 `import researchclaw` 成功，`pipeline/stages.py` 含 stages 16–23 契约。完整 CLI 需 LLM 凭据（用户未提供），仍按本地等价执行记录 | `dependency-resolution.md`、账本 A8
- 2026-11-13T21:07+0800 | 选题重定义 | 因 CRPI 已占「跨步残差结转」，把主机制改为「事件轴误差递推 + `‖ΔA_k‖` 拓扑变化项 + 事件门控重校准」，并把 CRPI 提升为 `must-rerun` 对照；S1/S2/S3 场景在 G4/G3/G7 判死 | `scenario-decision-log.md`、`idea-cards.md`
- 2026-11-13T21:12+0800 | guidance 全套产物落盘 | guidance.md、8 个旁证、CCFA startup packet 7 个 md、`feasibility-contract.json`（3 claims 哈希绑定 7 文件）、`guidance-pipeline-state.md`、`generated-research-directions.md` 完成 | run 目录
- 2026-11-13T21:14+0800 | 两个校验器通过 | `validate_guidance.py --strict --packet` → `Guidance structure is valid.` EXIT=0；`pipeline_state.py --complete` 与 `--before G0` → `PASS: ordered, current evidence` EXIT=0。**E2 PASS** | `validation-report.md`
- 2026-11-13T21:15+0800 | 账本更新与第二个检查点 | `goal-ledger.md` v1.1：E1/E2 PASS、M1/M2 PASS、R2 换道至 S2、A8 升级为源码级可用；HANDOFF/LOG/依赖解析同步；准备生成 manifest 并推送 | 本检查点
