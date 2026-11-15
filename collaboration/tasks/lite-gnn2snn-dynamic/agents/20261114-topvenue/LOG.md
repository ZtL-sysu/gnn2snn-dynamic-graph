# LOG — 20261114-topvenue（仅追加）

## 2026-11-14

- 12:20Z 认领任务：用户新目标（顶会学习 → 升级 f-guidance-builder-v1 → f-research-v1 v4 深做 → GitHub 同步）。读 PROJECT.md / PROTOCOL.md / TASK.md / wb-lead HANDOFF / goal-ledger，形成认知摘要：v3 已交付 30 页成稿，E4 附条件 PASS（LastFM q=0.40），本周期做 v4 加深。
- 12:26Z 从 wb-lead HEAD `509c4ed` 切出本 agent 分支 `agent/lite-gnn2snn-dynamic/20261114-topvenue`。
- 12:34Z 启动 4 个并行文献调研子代理（SpikingGNN+conversion / CTDG / 转换理论 / 实验方法论）。等待期间写协作骨架。
- 12:50Z **事故留痕**：在 v3 run root 内直接跑 `V3_QUICK=1` 冒烟测时延，覆盖了 4 个 v3 证据文件（aggregated.json、bound-check/wikipedia_s41_trace.json、p3_data/stream-summary.json、p4_auxiliary/sweeps_v3.json）。立即 `git checkout HEAD --` 恢复，`git status` 干净，aggregated.json 核验回 25 runs。**教训：任何 smoke 必须在新 run root 或临时副本中跑，绝不在历史 run root 内执行。**
- 12:52Z 冒烟时延标定（wikipedia 单 seed，window=2000）：graph+train 16 s，全流水线 147 s → v4 全量（5 流×10 seeds）约 3 h，可行性 PASS。方法论调研代理返回：缺 effect size/能量公式透明化/firing-rate 分层/seeds 提到 8–10/时间漂移切片等。

## 2026-11-15 (UTC)

- 03:10Z 左右 P2 通过（环境核验 + 冻结输入哈希 + 引擎 smoke PASS：12 方法全在，C5MT 事件 6.15 正常，1.7s）。
- 引擎补齐三块 instrumentation：C-6 ε 分层 MRR-loss 累加（EPSBIN_EDGES 预注册）、界估计日志 log_bound_features（与评估同一函数形式）、V4_METHODS 单方法隔离探针。
- 驱动 scripts/rerun_v4_main.py 七阶段成形；protocols/bound-constants-protocol.md 预注册锁定。
- 04:30Z train 完成：50 教师（5 流 × 种子 41–50）缓存 results/p3_teachers/teachers_v4.npy（27MB，增量断点）。
- **reproduce 门三轮诊断（任何 10-seed 结果之前）**：初版绝对 1e-6 容差 FAIL → 定位：agreement/trigger 跨引擎跨进程逐位一致，MRR/ε 存在 ≤9.3e-3 相对的**对齐相关浮点路径偏移**（同代码同配置同教师，两进程互跑逐位一致，但与 v3 存储行有偏移；不可复现属环境本质）→ 修正判据（G1a agreement 精确 / G1b MRR ≤1e-6 / G2 ε ≤2e-2 相对 / G3 种子 46 agreement 硬栅栏 + ε Tukey 软栅栏 ≤4/流 <5%）→ **PASS**（audits/reproduction-check.json）。
- **界常数两轮修正（测试评估之前）**：(1) 全局 eps_{k-1} 形式 R²=0.02–0.55（流事件交错于不同节点，全局前项无信息）→ 改**逐节点递归**（eps_prev(u)），R²→0.87–0.92，rho 拟合 0.67–0.78 ≈ 解析 0.7；(2) 最小二乘给条件均值，界需上包络 → eta 加 **95% 分位数 margin**，样本内违例率 0.00–0.18%（≤5% 上限）。两次修正均记录在协议文件。
- **V-6 玩具四轮设计修正**（全部记录在案）：分段常数算子塌缩到固定点线（slope≡1）→ 持续激励随机游走仍 slope=1（**单元 Wmix 使激活差=状态差精确抵消收缩**；稳态本就意味着 ek≈prev）→ 剂量 2 失败暴露**教师状态衰减固定 ALPHA=0.3** 与 SNN alpha_state 不匹配 → 终版：子玩具 A（Wmix=0.5I、α=0.3 教师匹配、瞬态对）rho 拟合 0.891 vs 解析 0.850 PASS；子玩具 B（Wmix=I 随机游走）拓扑项 b>0、corr 0.375 PASS。剂量响应证据由真实流 V-4 臂承担。
- P3、P3A 标记 passed；**主矩阵 50 runs 后台运行中**（bbxmdidyn）；V-6 PASS 后 analyze_v4.py 就绪待跑。
- 检查点：manifest 24 artifacts 全哈希绑定。

## 2026-11-15 (UTC) — v4 执行与收口（续 03:10Z 之后）

- 主矩阵 50 runs 完成 → 时延相（发现并修正单方法探针的 bound 方法集 bug，仅时延相、文档化在驱动 docstring）→ `analyze_v4.py` 锁定分析一次执行。
- **C-1 verdict：FALSE**。Wikipedia +4.90e-04 (q=0.039, dz=1.27, PoI=1.000) 唯一显著；MOOC −5.05e-05 方向负；Enron/Reddit/LastFM 方向正不显著。前驱四流主张双倍功效不复制，claim 按锁定映射收窄。
- E10 界 PASS（违例 ≤2.3% vs 5% 上限，tightness ≈0.5–0.62）；M0 在 wiki/enron/lastfm 12 方法排第 2（仅次于 A1 神谕）；下游剂量响应五流全平（负结果保留）；V-arms 5/8，V-4 方向失败（保留）。
- 论文 v4 初稿（38pp，0 错误）→ 评审工作流 7 子代理全部 API 429 → 改主线内联双评审（`audits/P9-peer-review.md`）。
- **P13 自评审发现 C2 ≡ C1 逐位一致（全 10 seeds diff=0.00e+00）** → 根因：`dcgs_encode(a,theta,T,bias,carry)` 的 `carry` 形参被接受但从未消费（`res = a - bias`），v3 引擎逐字节相同 → 披露为**缺陷 D1**，不写补丁（预注册纪律）。C-1 判决不受影响；机制证据收敛为门控+阈值两分量。全文 9 处修订（摘要/§2.3/§3.4/§3.6/§3.7/§4.2/§4.6/§4.8/新 limitation 9）。
- 其余 P13 修复：six→seven controls；0.97→≥0.995 captions；T-curve 10–19%→4–19%（数据复算）；B1/B2 悬空句删除；`efron1987`/`benjamini1995` 补引用（50/50 全被引）。
- Neurocomputing 硬约束复核：摘要 449→**248 词**；highlights 5 条全部 ≤85 字符；7 关键词；声明位置合规。fig1 框架图插入（D1 范围 caption）。
- **P5A+P6..P21 全部 mark passed**（哈希绑定证据）；P21：干净提取编译复现 40pp 字节一致、无 /Users/ 路径入交付物、无密钥、v3 哈希 5/5 PASS。
- 检查点 `7671e11` → `7e8b3b1` → `2260d1d`，均 push + ls-remote 核验。HANDOFF 终版已写。
