# 依赖解析记录（2026-11-13）

用户指令：「没有的技能你可以去本地的 codex 目录下找来用，不用再装了」。因此**未执行任何安装**（无 pip install、无 git clone 外部依赖、无全局配置修改），改为只读复用本机现成技能包，按各自 `SKILL.md` 的职责规范执行。

## 探测结果

| 依赖 | 需求来源 | 本机实际位置 | 状态 |
|---|---|---|---|
| `ccf-pipeline-orchestrator` | CCFA startup / 修正循环 | `/Users/xhf/.codex/skills/ccf-pipeline-orchestrator/SKILL.md` | 可用（只读复用） |
| `ccf-idea-optimizer` | CCFA startup / 修正循环 | `/Users/xhf/.codex/skills/ccf-idea-optimizer/` | 可用 |
| `ccf-literature-searcher` | CCFA startup / G0 / G4 | `/Users/xhf/.codex/skills/ccf-literature-searcher/` | 可用 |
| `ccf-idea-reviewer` | CCFA red-team / P1B / P3A | `/Users/xhf/.codex/skills/ccf-idea-reviewer/` | 可用 |
| `ccf-experiment-designer` | claim-evidence / 强结果契约 / P1A | `/Users/xhf/.codex/skills/ccf-experiment-designer/` | 可用 |
| `ccf-integrity-auditor` | P1B / P3A / P5A / P9 | `/Users/xhf/.codex/skills/ccf-integrity-auditor/` | 可用 |
| `ccf-paper-reviewer` | P5A / P9 | `/Users/xhf/.codex/skills/ccf-paper-reviewer/` | 可用 |
| `ccf-common`（共享治理） | 上述技能的 routing / 输出标准 / 隐私证据策略 | `/Users/xhf/.codex/skills/ccf-common/references/` | 可用 |
| 其余 ccf-* 共 17 个 | 按需 | `/Users/xhf/.codex/skills/` | 可用（同目录另有 `.claude/skills/`、`.cc-switch/skills/` 副本） |
| `f-guidance-builder-v1` / `f-research-v1` / `f-submit-v1` | 主流水线 | `/Users/xhf/.workbuddy/skills/`（本机已加载）；`/Users/xhf/.codex/skills/` 亦有副本 | 可用 |
| `research-github-sync` | 检查点 | `/Users/xhf/.workbuddy/skills/research-github-sync/` | 可用 |
| `relentless-goal-executor` | 死磕守护 | `/Users/xhf/.workbuddy/skills/relentless-goal-executor/` | 可用 |

## 写作与产出链路（vendored，原生可用）

`~/.workbuddy/skills/f-research-v1/bundled-skills/`：`0-autoresearch-skill`、`autoresearch` 规范、`citation-audit`、`humanizer`、`ml-paper-writing`、`nature-citation`、`nature-figure`、`paper-compile`、`paper-polish-workflow`、`paper-refine`。

工具链：LaTeX `/Library/TeX/texbin/{pdflatex,xelatex,latexmk}` 齐全；`/Users/xhf/miniconda3/bin/python` 3.14.6 + torch 2.13.0 + MPS；`gh` CLI 已登录 `ZtL-sysu`。

## 降级项（如实记录，不伪造调用）

| 项 | 事实 | 处理 |
|---|---|---|
| AutoResearchClaw CLI 端到端运行（stages 16–23） | **源码可用，完整 CLI 运行不可用**：源码在历史 run 的 `dependencies/AutoResearchClaw/`（含 `pyproject.toml`、`researchclaw/` 包、`config.researchclaw.example.yaml`、`pipeline/stages.py` 中的 16–23 契约）；`PYTHONPATH=<该目录>` 下 `import researchclaw` 实测成功。但 `pyproject.toml` 的 CLI 依赖 OpenAI 兼容 LLM 端点与 API key，用户未提供凭据，且用户要求「不再安装」 | 依 `f-research-v1/references/dependency-map.md`，用本地源码的 stage 契约 + `bundled-skills/0-autoresearch-skill/SKILL.md` 规范做**本地等价执行**：按 stage 契约产出 PAPER_OUTLINE / PAPER_DRAFT / PEER_REVIEW / PAPER_REVISION / QUALITY_GATE / EXPORT_PUBLISH / CITATION_VERIFY 对应 artifacts，并在 run root 记录「未运行 ARC CLI，按源码契约等价执行」及原因。不等价于宣称运行了 AutoResearchClaw；不编造 API 凭据 |
| `ccf-*` 未在 WorkBuddy 的 Skill 注册路径 | WorkBuddy 的 `available_skills` 只列 `/Users/xhf/.workbuddy/skills/` | 直接读取 `/Users/xhf/.codex/skills/ccf-*/SKILL.md` 与 `references/`，由本会话/子代理按规范执行；在产物中注明「按该技能规范执行」而非「通过 Skill 工具加载」 |

## 约束

- 不修改 `~/.codex/skills/` 下任何文件（只读）。
- 不把本地绝对路径、凭证或私有材料写进公开仓库产物。
- `f-research-v1` 的 `references/writing-adapter.md` 要求验证「外部 ARC 上下文隔离」真实状态；CLI 缺失时按等价执行如实标注，不假定已隔离。
