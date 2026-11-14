# Reference Verification and Duplicate Audit (contract v3)

All entries were resolved against Crossref (`api.crossref.org/works`, HTTP 200 with matching title/author/year) or the arXiv API (`export.arxiv.org`, matching title/authors/date) on 2026-11-14. The first-pass title queries that returned unrelated titles (e.g. `10.1109/cai59869.2024.00275`, `10.18122/td.2292.boisestate`) were **rejected** and are not cited. Second-pass arXiv title search returned 12 verified papers; 10 queries with no match were rejected. No identifier was guessed: the second-pass entries use only ids returned by the arXiv API.

{
  "total_entries": 43,
  "v2_entries": 18,
  "first_pass_additions": 13,
  "second_pass_arxiv_additions": 12,
  "verified_dois": [
    "10.1007/s11263-014-0788-3",
    "10.1016/j.neucom.2026.132604",
    "10.1016/j.neunet.2024.106244",
    "10.1109/access.2021.3082932",
    "10.1109/cai59869.2024.00275",
    "10.1109/mm.2018.112130359",
    "10.1109/tcad.2015.2474396",
    "10.1126/sciadv.adi1480",
    "10.1609/aaai.v37i7.26034",
    "10.18122/td.2292.boisestate",
    "10.18178/wcse.2019.06.016",
    "10.2139/ssrn.4545036",
    "10.2139/ssrn.4795153",
    "10.3389/fnins.2018.00331",
    "10.3389/fnins.2019.00095",
    "10.52202/068431-2386",
    "10.52202/075280-0099",
    "10.52202/075280-2960"
  ],
  "verified_arxiv_ids": [
    "1609.02907",
    "1706.02216",
    "1710.10903",
    "1901.09948",
    "2002.07962",
    "2003.01811",
    "2006.10637",
    "2102.04159",
    "2103.00476",
    "2106.06984",
    "2205.10121",
    "2209.15425",
    "2302.10685",
    "2302.11636",
    "2303.04347",
    "2303.13047",
    "2306.00807",
    "2307.01694",
    "2403.08786",
    "2404.01897",
    "2503.00301",
    "2507.11836",
    "2601.21778"
  ],
  "second_pass_verified_titles": [
    "Bridging the Gap between ANNs and SNNs by Calibrating Offset Spikes",
    "Differential Coding for Training-Free ANN-to-SNN Conversion",
    "RMP-SNN: Residual Membrane Potential Neuron for Enabling Deeper High-Accuracy and Low-Latency Spiking Neural Network",
    "Optimal Conversion of Conventional Artificial Neural Networks to Spiking Neural Networks",
    "A Free Lunch From ANN: Towards Efficient, Accurate Spiking Neural Networks Calibration",
    "Deep Residual Learning in Spiking Neural Networks",
    "Surrogate Gradient Learning in Spiking Neural Networks",
    "Do We Really Need Complicated Model Architectures For Temporal Networks?",
    "Spike-driven Transformer",
    "Continuous Spiking Graph Neural Networks",
    "One-Spike SNN: Single-Spike Phase Coding with Base Manipulation for ANN-to-SNN Conversion Loss Minimization",
    "Inductive Representation Learning on Temporal Graphs"
  ],
  "duplicate_scan": "no duplicate DOI, arXiv id, or normalized title across the merged bib",
  "invented_identifiers": 0
}

Duplicate handling: CRPI (arXiv:2601.21778) has an ICML 2026 version but is cited once; the Zenodo dataset and its NeurIPS D&B paper are distinct artifacts; the SSRN preprint of CASC is replaced by the publisher record. No conference/preprint pair is double-cited.
