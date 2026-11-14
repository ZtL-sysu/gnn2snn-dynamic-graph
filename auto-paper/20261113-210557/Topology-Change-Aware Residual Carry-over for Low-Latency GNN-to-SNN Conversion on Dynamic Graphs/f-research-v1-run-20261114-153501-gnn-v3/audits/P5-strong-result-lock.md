# P5 Strong-Result Lock (contract v3)

Authoritative evidence: `results/aggregated.json` (25 runs), `results/statistics/final-analysis-v3.json`, `results/p4_auxiliary/sweeps_v3.json`, `results/bound-check/*_trace.json`.

Binding v2 targets retained verbatim and re-verified on the v3 GNN/DCGS implementation:

| Criterion | Verdict |
|---|---|
| (a) T=4 agreement >= 98.5% on every stream | {'wikipedia': True, 'mooc': True, 'enron': True, 'reddit': True, 'lastfm': True} |
| (a) MRR retention >= 99% | {'wikipedia': True, 'mooc': True, 'enron': True, 'reddit': True, 'lastfm': True} |
| (b) `$epsilon_k$` strictly lowest vs the six conversion controls C0-C4 and D1 (A1 is a 100%-cost diagnostic upper bound, reported separately) | {'wikipedia': True, 'mooc': True, 'enron': True, 'reddit': True, 'lastfm': True} |
| (b) paired bootstrap 95% CI excludes 0 on every stream | {'wikipedia': True, 'mooc': True, 'enron': True, 'reddit': True, 'lastfm': False} |
| (b) Benjamini--Hochberg q < 0.05 | False |
| (c) recalibration <= 20% of events | {'wikipedia': True, 'mooc': True, 'enron': True, 'reddit': True, 'lastfm': True} |
| (d) replication across streams (ORIGINAL all-five-stream binding condition) | False |
| (d') evidence-bounded claim after C16 narrowing (4/5 streams, no numeric target lowered) | True |

New v3 criteria: **E6** real measured `$A_k$` (mean `||Delta A_k||` logged per event, `True`); **E7** top-venue matrix rows all `done` (`True`); **E8** >=21 pages and >=43 verified references (see `final-metadata-counts.json` and `reference-dedup-audit.md`).

Every required experiment is `done` in `experiment-traceability.md`. Negative diagnostics (stream-dependent effect size, non-monotone relative dose-response, agreement saturation, non-blind identifiers) are preserved and disclosed.

**The original all-five-stream binding condition is NOT satisfied.** `False`: the LastFM paired bootstrap interval covers zero and its Benjamini--Hochberg q-value is 0.40. This verdict is recorded unmodified in `results/statistics/final-analysis-v3.json` and is not rewritten. Tuning the operating point until that interval excludes zero would be p-hacking and was explicitly rejected (cycle C16).

**Accepted claim: evidence-bounded narrowing (C16).** `True`: significant state-error reduction is asserted on the four streams with a dispersed operator-change distribution; LastFM is reported as a direction-consistent but non-significant boundary case with a mandatory disclosure in the abstract, Results and Discussion. No numeric `minimum`, `expected_strong` or `failure` value is lowered; a new negative-result disclosure obligation is added. A1 is a 100%-cost diagnostic upper bound, not a conversion comparator. A5 barely changes state error on four streams, which is itself disclosed as a negative finding.

Verdict: **PARTIAL on the original binding condition; PASS on the delivered, narrowed claim**. This is a complete first draft, not an acceptance or a submission.
