# 目标死磕状态账本

> 唯一进度载体。历史记录不得改写，修正只追加。账本版本 v1.0。最后更新：2026-11-13T20:58:54+0800。

## 1 目标档案

| 项 | 内容 |
|----|------|
| 目标陈述 | 按用户科研流水线标准严格走完 `research-github-sync` → `f-guidance-builder-v1` → `f-research-v1`，产出一篇面向 Neurocomputing 的完整可投稿成稿（TeX + 编译 PDF + 可回溯证据包）；方向为轻量级 GNN→SNN 转换 + 动态图 |
| 背景与动机 | 用户原话：「从我的 github 上找到 gnn2snn 的研究…针对本机的算力，我们做轻量级的 gnn2snn 的模型做动态图为大方向…验证可行性后写协议，然后按照 f-research-v1 进行实验和写作…得到一篇完美的成稿，目标为老牌的闭源中科院二区或三区的期刊」 |
| 边界 | 不实际投稿；不合并 main/force push；不做神经形态能耗实测；不做 spike-proxy 稀疏执行主贡献；不用私有/受限数据；不上传 >50 MiB 单文件；不使用未在授权清单内的远程算力 |
| 时间尺度 | 会话内死磕 + 账本落盘跨会话恢复（用户未开启心跳、未设期限） |
| 资源约束 | Apple M1 / 8 核 / 16 GB RAM / 8 核 GPU(MPS) / 339 GB 可用磁盘；无 CUDA；本机 conda `/Users/xhf/miniconda3/bin/python` |
| 判定者 | 用户验收 + 系统可核验产物（脚本校验、git 远端 SHA、PDF 编译、原始指标日志） |
| 确认档位 | **授权档**（用户 2026-11-13 明确选择；切换记录见第 7 节） |
| 运行模式 | 会话内死磕；账本与 GitHub 检查点支持续跑 |

## 2 手段弹药库

| 条目 | 路目 | 能力描述 | 可用状态 | 调用路径 | 风险等级 | 白名单 |
|------|------|---------|---------|---------|---------|--------|
| A1 | 内置能力 | 本地文件读写、Bash、conda Python 执行 | 可用 | Read/Write/Edit/Bash + `/Users/xhf/miniconda3/bin/python` | 低 | PASS |
| A2 | 内置能力 | 文献/网络检索 | 可用 | WebSearch / WebFetch | 低 | PASS |
| A3 | 可组合编排 | 并行只读调研子代理 | 可用 | Agent(Explore/general-purpose) | 低 | PASS |
| A4 | 内置能力 | GitHub 仓库/分支/检查点操作 | 可用 | `gh` CLI（账号 ZtL-sysu，已登录）+ git | 中 | PASS |
| A5 | 可检索能力 | 17 个 `ccf-*` 技能包（CCFA 全流程职责规范） | 可用（只读复用，不安装） | `/Users/xhf/.codex/skills/ccf-*/SKILL.md` | 低 | PASS |
| A6 | 可组合编排 | 写作/配图/编译/引用 9 个 vendored 子技能 | 可用 | `~/.workbuddy/skills/f-research-v1/bundled-skills/` | 低 | PASS |
| A7 | 内置能力 | LaTeX 编译与 PDF 验收 | 可用 | `/Library/TeX/texbin/{pdflatex,xelatex,latexmk}` | 低 | PASS |
| A8 | 可检索能力 | AutoResearchClaw CLI（stages 16–23） | **不可用（降级）** | 本机无 CLI / 无安装包；改用 `bundled-skills/0-autoresearch-skill/SKILL.md` 规范 + 本地等价执行，产物格式对齐 stage 契约 | 低 | PASS（降级如实记录） |
| A9 | 外部资源 | Zenodo 公开动态图事件流 + 本机已存 DyGLib/Base3/TPNet baseline 代码 | 可达（待 G1 实测下载核验） | `10.5281/zenodo.7213796`；`/Users/xhf/full-paper/dynamic graph/d2/.../dependencies/` | 低 | PASS |
| A10 | 内置能力 | torch 2.13.0 + MPS 训练/推理 | 可用 | conda python，`device=mps` | 低 | PASS |
| A11 | 可组合编排 | 定时心跳自动化 | 可用但**默认关闭** | `automation_update`（用户未开启，不主动创建） | 中 | PASS |
| A12 | 外部资源 | 远程 exp-4090 GPU 池 | **剔除**：用户未授权远程执行，历史记录显示节点 offline、`eligible_nodes=0` | — | — | 剔除（超出授权算力范围） |
| A13 | 外部资源 | `gnn2snn` 历史稿件 / 权重 | **剔除**：历史稿明确标注不可投稿；权重 >40 MiB 不上传 | 仅本地只读引用 | — | 剔除（不作为成稿/上传依据） |

## 3 成功标准证据清单（锁定，修改须走目标迭代并经用户确认）

| 编号 | 标准（可观测事实） | 判定者 | 反例排除（什么不算达成） | 当前状态 |
|------|-------------------|--------|------------------------|---------|
| E1 | 公开仓库 `ZtL-sysu/gnn2snn-dynamic-graph` 存在 `collaboration/` 骨架与本任务 agent 分支检查点（含 `manifest.json`），`git ls-remote` 远程 SHA 与本地 HEAD 一致 | 系统 + 用户 | 只有本地 commit / 只有空仓库 / 远程 SHA 不一致 | 待验证 |
| E2 | `guidance.md` 通过 `validate_guidance.py --strict --packet`；`guidance-pipeline-state.md` 证明 `CCFA-startup → G0…G8 → validation → handoff` 依序全 `passed`；8 个必需旁证文件与 `ccfa-startup-packet/` 齐全 | 系统 + 用户 | 跳关、倒填状态、把未核查的新颖性写成已核查 | 待验证 |
| E3 | `pipeline-state.json` 证明 P0…P21 依序全 `passed`；run root 内 `paper.tex` 与编译成功的 `paper.pdf` 存在，且 clean-extraction 重编译 PDF 与验收版一致；交付清单在 run root 内 | 系统 + 用户 | 只写稿未跑实验 / 编译失败 / 源码与 PDF 不同版 | 待验证 |
| E4 | guidance 承诺的每个实验 `done`，主 claim 达到**预先锁定**的 `expected_strong`；baseline 先于方法结论；逐 seed 原始日志 + `metrics.csv` + 复现命令可回溯 | 系统 + 用户 | 数字只出现在论文正文 / 事后下调目标 / 把计划值写成实测 | 待验证 |
| E5 | 稿件为 `1 Introduction / 2 Related Work / 3 Method / 4 Experiments and Results / 5 Discussion / 6 Conclusion` 六节；引用真实且 `reference-dedup-audit.md` 通过；目标期刊硬性限制有官方来源记录；`paper-guidance-audit.md` 无未覆盖项 | 系统 + 用户 | 占位引用 / 自编期刊限制 / 承诺实验未出现在稿中 | 待验证 |

> 「完美成稿」为不可观测表述，已按 RGE1 转为 E2–E5 的可观测代理指标并经用户确认锁定。

## 4 里程碑链

| 里程碑 | 绑定证据 | 预期完成依据 | 状态 |
|--------|---------|-------------|------|
| M1 | E1 | 仓库 + 协议 + 账本 + 依赖解析 + 首个检查点远端确认 | 进行中 |
| M2 | E2 | guidance.md 与各审计文件、CCFA packet、strict 校验通过 | 未开始 |
| M3 | E4 | 全部实验原始证据 + 达到 expected_strong + baseline 先行 | 未开始 |
| M4 | E3, E5 | P0–P21 状态全 passed + TeX/PDF + 各类审计 | 未开始 |
| M5 | E1–E5 | 用户验收、检查点归档、停止报告 | 未开始 |

## 5 当前策略卡

| 项 | 内容 |
|----|------|
| 当前策略 | S1「先封锁基础设施与证据纪律，再以机制级空白（GNN→SNN 转换 × 动态图时序状态）做证据优先的 guidance」 |
| 核心假设 | 动态图上真正未被占领的不是"新 SNN 架构"而是"ANN→SNN 转换在时序记忆/状态更新下的等价性与误差累积"；且小事件流 + 轻量教师可在 M1/MPS 上完成可信实验 |
| 动作清单 | ①建仓库/协议/账本并推首个检查点 ②真实文献检索 G0/G4（含 SpikeNet/Dy-SIGN/Lite-SDGN 与 ANN→SNN 转换近作）③G1 实测 Zenodo 下载 ④G3/G5/G6/G7 机制与算力可行性 ⑤CCFA startup packet ⑥G8 故事强度 ⑦guidance.md + strict 校验 ⑧上传检查点 ⑨启动 f-research-v1 P0–P2 |
| 敏感标记 | 创建公开仓库、首次 push、新建 conda env、实际投稿（后者不在授权内） |
| 连败计数 | 0 |

## 6 执行轮与换道日志

| 轮次 | 策略 | 动作与结果 | 证据核验 | 败因归类 | 换道决策 |
|------|------|-----------|---------|---------|---------|
| R1 | S1 基础设施 | 已核实本机算力、GitHub 账号、`gnn2snn` 归档全貌与历史动态图流水线；依赖由「安装」改道为「复用 `~/.codex/skills/` 现成包」（用户 2026-11-13 20:45 指令）；公开仓库已创建；协议/账本/依赖解析已落盘 | E1 待验证（检查点尚未 push），E2–E5 待验证 | 条件不备（ccf-* 未装在 WorkBuddy skills 路径）→ 用户指令换道解决 | 继续 S1，完成首个检查点推送 |

> 失败日志只追加不改写。卡死检测：同策略连败 3 次强制换道。

## 7 守护记录

| 项 | 内容 |
|----|------|
| 白名单校验 | A12 远程 GPU、A13 历史稿/大权重已剔除（见第 2 节）；其余均在法律法规与平台规则内 |
| 确认档位切换 | 2026-11-13：默认严格档 → **授权档**，用户通过选项明确确认 |
| 敏感操作确认 | 2026-11-13 用户一次性授权：创建公开仓库、本地文件写入、新建 conda 环境、运行实验、按协议推送检查点。清单外（对外发送、删分支、改历史、合并 main、实际投稿）仍逐项确认 |
| 合规存疑处理 | AutoResearchClaw CLI 缺失：不伪造调用记录，按 `dependency-map.md` 使用 vendored 规范做等价执行并在 run root 记录降级原因 |
| 依赖解析 | 见 `dependency-resolution.md`；用户明确「没有的技能你可以去本地的 codex 目录下找来用，不用再装了」 |

## 8 停止门状态

| 门 | 状态 | 触发依据 |
|----|------|---------|
| ①达成 | 未触发 | E1–E5 均未 PASS |
| ②用户叫停 | 未触发 | 无 |
| ③穷尽 | 未触发 | 策略库 S1 首轮，弹药库未穷尽 |
| ④期限 | 未触发 | 用户未设预设期限（会话内 + 账本续跑） |

## 9 迭代与复盘

| 项 | 内容 |
|----|------|
| 账本版本 | v1.0 |
| 目标迭代记录 | 无（标准锁定后未修改） |
| 复盘沉淀 | ①历史 P3「无限创意筛选死循环」是最大已知陷阱：必须先冻结协议与强结果契约再开实验；②本机强基线 TGN 单 seed 曾耗时 8 h 超时，G6 必须选择可在 M1 上实证的 baseline 组合，不能只写 literature-context；③非神经形态硬件上不做能耗主张 |
| 归档状态 | 进行中 |
