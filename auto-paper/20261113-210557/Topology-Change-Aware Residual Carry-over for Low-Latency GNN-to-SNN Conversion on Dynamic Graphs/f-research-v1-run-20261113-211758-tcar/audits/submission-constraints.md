# Submission Constraints (P20, primary source)

Source: Elsevier, *Neurocomputing* Guide for Authors, https://www.sciencedirect.com/journal/neurocomputing/publish/guide-for-authors , accessed 2026-11-14. The page was retrieved successfully; a direct `curl` returned a Cloudflare challenge page, so the primary-source text below is the retrieved page content, not the challenge page. Journal facts (Elsevier, founded 1989, ISSN 0925-2312, CAS computer-science Tier 2, subscription/hybrid) were cross-checked against public journal-information pages on 2026-11-13.

## Hard numeric limits (quoted from the guide)

| Field | Limit | Status for this manuscript |
|---|---|---|
| Abstract | "does not exceed 250 words" | must be counted on the exact plain text |
| Keywords | "1 to 7 keywords" | use 5–6 |
| Highlights | "3 to 5 bullet points, each a maximum of 85 characters, including spaces" | use 4, counted with spaces |
| Vitae | "maximum 100 words" per author | optional submission element, recorded as unresolved until author metadata is confirmed |
| Page limit | **none stated** in the guide | no invented page target |
| References | no numeric quota; "Every reference included must correspond to a real, existing source"; include DOIs where available; numbered `[1]` in order of appearance | `reference-dedup-audit.md` + P12/P14 verification |

## Mandatory structure and declarations

- Article type: **Type 1 Regular article**. The guide states the journal "does NOT accept submissions on pure dynamical systems, pure control engineering, pure fuzzy logics, pure image processing or pure combination of existing algorithms, which are not directly relevant to neural networks or learning systems." Our contribution is a mechanism-level ANN→SNN conversion method with a bound, so it is directly relevant to neural networks and learning systems; it is not a pure combination of existing algorithms.
- "Divide your manuscript into clearly defined and numbered sections. Number subsections 1.1 (then 1.1.1, ...), then 1.2, etc." The `f-research-v1` six-section contract is compatible.
- "Do not include the article abstract within section numbering."
- **Declaration of generative AI use is required**: "Authors must declare the use of generative AI tools in the manuscript preparation process upon submission"; the statement "should be placed in a new section before the reference list", with the exact section title *Declaration of generative AI and AI-assisted technologies in the manuscript preparation process* and the example statement form. This manuscript was prepared with AI assistance, so the declaration is included as a section immediately before the references.
- **Declaration of competing interests**: the declarations tool must always be completed; "I have nothing to declare." if none. This is an external submission element, not inserted into the manuscript by default.
- **Research data — Option C** applies: deposit research data in a relevant repository, provide a link during submission, or state why sharing is impossible. Our public Zenodo source (`10.5281/zenodo.7213796`, CC BY 4.0) and the public code/protocol repository satisfy the spirit of this requirement; the exact repository link for derived artifacts is recorded in `manuscript-metadata.md`.
- Acknowledgements "should be placed in a separate section that appears directly before the reference list".
- LaTeX: the guide encourages the Elsevier LaTeX template and requires "all relevant editable source files upon submission". `elsarticle.cls` is installed locally (`kpsewhich elsarticle.cls` resolved).

## Unresolved / not invented

- Corresponding-author email, funding, and CRediT roles were not supplied by the user; they are recorded as unresolved in `manuscript-metadata.md` and are not fabricated.
- No word-count limit for the body and no reference-count quota exist in the guide; none is invented here.
- The official Article Transfer Service / license options are submission-time choices, not recorded as manuscript constraints.
