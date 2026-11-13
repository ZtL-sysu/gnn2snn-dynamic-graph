# Dataset Access Log

Access date: 2026-11-13. All checks performed from the local machine with `curl` and the project Conda Python. License and file sizes come from the Zenodo REST record, not from secondary summaries.

## Directly public source (verified)

| Dataset | Direct access URL | License/terms | Size | Labels/targets | Access friction | Decision |
|---|---|---|---|---|---|---|
| Wikipedia | https://zenodo.org/api/records/7213796/files/wikipedia.zip/content | CC BY 4.0 (record `10.5281/zenodo.7213796`) | 50,208,031 B zip | timestamped `(src, dst, t)` interaction events; link-prediction candidates | none; HTTP 200 with `content-disposition: attachment` | direct-public |
| MOOC | https://zenodo.org/api/records/7213796/files/mooc.zip/content | CC BY 4.0 | 7,597,555 B zip | same schema | none | direct-public |
| Enron | https://zenodo.org/api/records/7213796/files/enron.zip/content | CC BY 4.0 | 808,719 B zip | same schema | none; HEAD verified HTTP 200 | direct-public |
| Reddit (optional) | https://zenodo.org/api/records/7213796/files/reddit.zip/content | CC BY 4.0 | 326,784,735 B zip | same schema | none; large download | direct-public, optional |
| LastFM (optional) | https://zenodo.org/api/records/7213796/files/lastfm.zip/content | CC BY 4.0 | 23,831,149 B zip | same schema | none | direct-public, optional |
| Record metadata / readme | https://zenodo.org/api/records/7213796 | CC BY 4.0 | 8,983 B JSON | file inventory, DOI, license | none | direct-public |

The upstream record is *"Dataset for Towards Better Evaluation for Dynamic Link Prediction"*, DOI `10.5281/zenodo.7213796`, license `cc-by-4.0`. Fifteen files are listed. No email approval, institutional login, NDA, payment, IRB, or "available on request" step was encountered. A plain HTTP HEAD/GET on a file URL returns 200 with an attachment disposition.

## Local frozen streams (verified readable)

A previous local project froze four event streams as `.npz`. These are **local copies**, not an additional dataset source; the canonical public source remains Zenodo. All four were opened with `numpy.load` on 2026-11-13 and their arrays inspected:

| File | Events | Key arrays | Sizes |
|---|---:|---|---|
| `wikipedia-events.npz` | 157,474 | `src, dst, timestamp, original_row, edge_id` + `source_labels(8227), destination_labels(1000), catalog(1000), validation_query(1024), test_query(4096)` and weights/bins | 1,253,310 B |
| `mooc-events.npz` | 411,749 | same schema; `source_labels(7047), destination_labels(97), catalog(97)` | 2,821,369 B |
| `reddit-events.npz` | 672,447 | same schema; `source_labels(10000), destination_labels(984), catalog(984)` | 7,266,991 B |
| `lastfm-events.npz` | 1,293,103 | same schema; `source_labels(980), destination_labels(1000), catalog(1000)` | 10,938,846 B |

Each file contains pre-frozen `validation_query` (1,024) and `test_query` (4,096) identifiers with weights and bins. **The test identifiers are already present locally and were used in a previous project**, so this is not a blind held-out set; the guidance states this as a limitation. Val/test identity must be hash-frozen before any tuning at P2.

## Split protocol (inherited, to be re-frozen)

Chronological 70/15/15 split by event time, inherited from the local predecessor protocol (`evaluation-protocol.md` in the historical RiskSet-DyG run). Training events are used for teacher training and label-free activation calibration only; validation queries select `T`, the topology-change threshold `gamma`, and calibration percentile; test queries are evaluated once at P5 after the contract is frozen. Any change to these identities requires a versioned contract update.

## Rejected datasets and why

| Candidate | Reason for rejection |
|---|---|
| TGB 2.0 (largest variants, up to 53 M edges) | Exceeds the 16 GiB unified-memory and 12 h wall-clock envelope; a previous local audit already excluded it on a 12 GB GPU budget. |
| Datasets requiring author contact / institutional approval / private buckets | G1 hard block: not directly public. |
| SuperPixel MNIST / CIFAR10 from the user's `gnn2snn` archive | Static graphs; teacher training required an RTX 3060 12 GB and 55k graphs, infeasible on this machine, and the task has no topology evolution. Kept only as a source of conversion code and prior accuracy ranges. |
| MaleCNS / fly connectome (1.05 GB Feather), neuPrint | Access friction and prior `IncompleteRead` / token failures on this machine; not directly public for this workflow. |

## Licensing note

The user's `ZtL-sysu/gnn2snn` archive states in `RIGHTS.md` that no blanket license is granted. Code reused from it is treated as a **local read-only reference**; the manuscript will describe the algorithmic idea and cite the public repository, while the new implementation is written independently in this project's run root. The Zenodo data license is CC BY 4.0 and permits research reuse with attribution.
