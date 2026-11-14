# P3A Baseline-Evidence Stop-Loss Review (contract v3)

Baseline-first results are in `results/p3_baselines/validation_mrr_v3.json`. EdgeBank$_\infty$ attains 0.947 / 0.631 / 0.948 / 0.898 / 0.911 validation MRR on Wikipedia / MOOC / Enron / Reddit / LastFM; Base3 k=10 attains 0.826 / 0.256 / 0.476 / 0.756 / 0.291. A random continuous-state teacher attains 0.001--0.057, i.e. far above chance only on small catalogs. The real GNN teacher is non-vacuous (held-out MRR reported in Table 1 and in `results/aggregated.json`).

Numeric audit: metric is MRR (fraction, higher better), chronological 70/15/15 validation queries, deterministic baselines, five seeds for all teacher conditions, units consistent, no fraction/percent mixing. The discrete-memory dominance is a **diagnosis, not a defeat**: the v3 claim is conversion fidelity for a fixed teacher, and the ablation A5 (no aggregation) now directly tests whether the graph operator is the mechanism's source.

Verdict: baseline metrics and reproducibility artifacts exist before proposed-method iteration; the baseline landscape does not defeat the conversion-fidelity claim. **P3A pass**.
