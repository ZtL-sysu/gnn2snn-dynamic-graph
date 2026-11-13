# Hardware Profile（本机实测）

探测时间：2026-11-13 20:49 +0800。探测脚本：`/Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/hardware_probe.py`，在 `/Users/xhf/miniconda3/bin/python` 下运行。脚本只向 stdout 打印 JSON（不接受 `--output`），以下为**原样实测输出**的转录，未做任何推断性补充。

```json
{
  "conda_environment": null,
  "cpu_count": 8,
  "machine": "arm64",
  "memory_bytes": 17179869184,
  "os": "Darwin",
  "os_release": "24.6.0",
  "privacy_note": "Serial numbers, UUIDs, usernames, hostnames, and network identifiers are intentionally omitted.",
  "python": "3.14.6",
  "python_executable": "/Users/xhf/miniconda3/bin/python",
  "torch": {
    "cuda_available": false,
    "cuda_device_count": 0,
    "installed": true,
    "mps_available": true,
    "recommended_device": "mps",
    "version": "2.13.0"
  },
  "working_directory_disk_free_bytes": 339078103040
}
```

## 补充实测（独立命令）

- `uname -m` = `arm64`；`sysctl -n machdep.cpu.brand_string` = `Apple M1`；`hw.ncpu` = 8；`hw.memsize` = 17179869184。
- `system_profiler SPDisplaysDataType`：Apple M1 GPU，8 核，Metal 3。
- LaTeX：`/Library/TeX/texbin/pdflatex`、`xelatex`、`latexmk` 均存在。
- conda 环境：`base`（`/Users/xhf/miniconda3`）、`ceg_snn_mi`、`wecom_draft_mcp`；**尚无本项目专用环境**，P2 需新建。
- `gh` CLI 已登录 `ZtL-sysu`，token scopes `gist, read:org, repo`。

## 对实验规模的硬约束（推断，非实测结论）

- 无 CUDA；MPS 可用但不支持全部 PyTorch 稀疏/散射算子，需在 P2 逐算子验证；不支持时记录 CPU fallback。
- 16 GB 统一内存下，不能承载 55k 张超像素图的 GCN 教师训练（原归档依赖 RTX 3060 12 GB）。本项目只做小事件流上的轻量教师/转换。
- 历史记录：TGN 在动态图上单 seed 曾耗时 28,800 s 超时。G6 的强基线必须选本机可实证跑完的组合，或按 guidance 明确降级并给出替代证据。
- 远程/云执行为 opt-in，用户未授权，默认不使用。
