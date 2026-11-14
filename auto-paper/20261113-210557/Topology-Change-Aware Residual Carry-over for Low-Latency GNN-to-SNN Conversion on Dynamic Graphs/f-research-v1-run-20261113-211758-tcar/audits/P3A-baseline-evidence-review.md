# P3A Baseline-Evidence Stop-Loss Review

Executed after P3 (baseline-first) and before the P4 full campaign. Inputs: `results/p3_baselines/validation_mrr.json`, `results/p3_teachers/*.json`, `results/p3_data/stream-summary.json`, `guidance-v2.md`, `guidance-v2-amendment.md`.

## Numeric audit (`ccf-integrity-auditor`, numeric-audit mode)

| Check | Result |
|---|---|
| Metric | mean reciprocal rank (MRR), higher is better, unit `fraction` |
| Split | chronological 70/15/15; values below are **validation** queries only; test queries were not read at P3 |
| Seeds | 5 (41–45), every per-seed value retained in `validation_mrr.json` |
| Teacher training loss | Wikipedia 3.23–3.29 → 3.37; MOOC 3.33 → 4.00–4.03; Enron 3.11–3.18 → 2.86. MOOC loss rises because its 97-item catalog makes the full softmax harder; the readout is still learned (validation MRR 0.26 ≈ 26× chance) |
| Units / direction | consistent across all rows; no percentage/fraction mixing |
| Reproducibility | `scripts/run_campaign.py` + `results/p3_teachers/teachers.npy` + frozen stream SHA-256 in `inputs/frozen-identities.json` |

## Baseline landscape (validation MRR, mean over 5 seeds where applicable)

| Stream | B0 ANN teacher | B1 EdgeBank∞ (global binary memory) | B2 Base3 k=10 | chance 1/C | EdgeBank context |
|---|---:|---:|---:|---:|---|
| Wikipedia | 0.3036 | 0.9474 | 0.9092 | 0.0010 | discrete memory dominates |
| MOOC | 0.2645 | 0.6307 | 0.3509 | 0.0103 | discrete memory dominates |
| Enron | 0.3020 | 0.9477 | 0.4885 | 0.0054 | discrete memory dominates |

`B1` and `B2` are deterministic w.r.t. the stream, so their values are identical across teacher seeds; this is expected, not an error.

## Reassessment (`ccf-idea-reviewer`, standard mode)

- **Teacher non-vacuity (v2 gate)**: B0 exceeds 5× chance on all three streams (Wikipedia 304×, MOOC 26×, Enron 56×). PASS.
- **Absolute predictive SOTA**: not claimed. The v2 amendment records that EdgeBank/Base3 are context, not beaten baselines, because repeat interactions dominate these streams. The manuscript must disclose this.
- **Mechanism delta still credible**: the converted state contributes a bounded learned readout term on top of the shared discrete memory; conversion fidelity is measured by `agreement@K` and state error `ε_k`, not by absolute MRR. The v2 criterion (b) uses `ε_k` strict dominance plus paired bootstrap and BH correction.
- **No fatal soundness/novelty/evidence concern remains unresolved**; concerns 1, 4, 6, 9 from `audits/ccfa-pre-experiment-action-ledger.md` are still open for their owning stages (P4/P12/P20).

## Verdict

Baseline metrics and reproducibility artifacts exist before proposed-method iteration. The baseline landscape does not defeat the conversion-fidelity claim. **P3A pass**; P4 may begin.
