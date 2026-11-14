# P17 Paper-Guidance Coverage Audit

Audited `paper/main.tex` against `guidance-v2.md` (which supersedes v1 only for the two amended clauses; both files preserved).

| Guidance promise | Covered in manuscript | Verdict |
|---|---|---|
| Six canonical numbered sections | §1–§6 exactly | PASS |
| Problem, gap, insight, evidence chain | §1 → §3 → §4 → §5 | PASS |
| Event-axis bound with topology term and unfolded form | Eq. (2), Eq. (3), §3.2 | PASS |
| Seven assumptions A1–A7 | §3.4 | PASS |
| Three public datasets + direct URLs/licence | §4.1, \cite{poursafaei2022dataset}, data-availability section | PASS |
| Chronological 70/15/15, frozen query IDs, validation-only selection | §4.1, §5 non-blind disclosure | PASS |
| B0/B1/B2, C0–C4, D1, M0 | §4.1 and Table 1 | PASS |
| Six falsifying ablations (A1–A6) | A1–A4 in Table 1; A5 stratification in §4.3/Fig. 4; A6 T and γ sweeps in §4.3 | PASS |
| Three-stream replication R1–R3 | Table 2 | PASS |
| Window-length robustness K1–K3 | §4.3 (178/869/1731 queries) | PASS |
| T sweep {1,2,4,8} and γ sweep | §4.3 | PASS |
| Primary metric `agreement@K`, secondary metrics, `ε_k`, cost | §4.1–§4.3, Tables 1–2 | PASS |
| 5 seeds, paired bootstrap 95% CI, BH correction | §4.1–§4.2, `ε` CIs and q values | PASS |
| `minimum` / `expected_strong` / `failure` | reported as measured outcomes in §4 and bounded in §5; targets not presented as findings | PASS |
| Expected contribution type and claim boundary | §1, §5 | PASS |
| `planned_claim` ≠ `observed_finding` | §3.2 says Eq. (2) is a claim to be tested | PASS |
| Citation scope, must-cite works, dedup | `references.bib`, `reference-dedup-audit.md` | PASS |
| Honest limitations / threat-to-validity plan | §5 seven named limitations | PASS |
| No energy claim; positive evidence boundaries | §3.3, §5 | PASS |
| Non-blind test disclosure | §4.1, §5 | PASS |
| Negative results preserved | §4.3, §5, Abstract | PASS |
| Figure/table decision rules | Figs. 1–4, Tables 1–2; each answers a scientific question | PASS |

No promised experiment, section, claim, figure, table or analysis is uncovered. Contract-v2 amendments are transparently recorded in `guidance-v2-amendment.md` rather than silently absorbed. **P17 pass.**
