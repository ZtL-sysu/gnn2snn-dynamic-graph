# P8 Figure-1 Fallback Record

`f-research-v1` requires Figure 1 (the overall framework/architecture figure) to be generated directly with the GPT image-generation capability rather than through `nature-figure`. The image-generation tool is available but consumes approximately 5–10 additional credits per call. The user's authorization list covers repository creation, local writes, Conda environments, experiments and checkpoint pushes; it does **not** include spending credits, and the user was not asked mid-run for a new authorization.

Recorded fallback: Figure 1 is a local vector schematic produced by `scripts/make_figures.py` (matplotlib) from the verified method components, saved as `paper/figures/fig1_framework.pdf` and `.png`. It shows only components described in §3 (event stream, ANN/SNN message paths, topology-change tracker, gate, shared memory/readout, metrics) and no invented module. Data-visualisation figures 2–4 are also produced locally rather than through `nature-figure`, which was unavailable as an installed skill; the vendored copy exists but no executable CLI was used.

This is a **recorded fallback, not a claim that the GPT-image path was executed**. If the user authorises the credit cost, Figure 1 can be regenerated with the image-generation model after the full paper is understood, following `f-research-v1/references/framework-figure-style.md`, and the PDF must then be recompiled and re-audited.

No generated image is presented as experimental evidence.
