# P21 Clean-Extraction Compile Check

The delivered `paper/main.tex`, `references.bib` and all four figure PDFs were copied to a clean temporary directory and compiled there with `pdflatex` → `bibtex` → `pdflatex` ×2.

{
  "accepted_pdf": "paper/main.pdf",
  "rebuilt_pdf": "clean-extraction main.pdf",
  "accepted_pages": 14,
  "rebuilt_pages": 14,
  "normalized_text_identical": true,
  "accepted_text_sha256": "19c23a09bd5641c94eabad94367c2621c42a38e6e149911b429fa3e56ff243f1",
  "rebuilt_text_sha256": "19c23a09bd5641c94eabad94367c2621c42a38e6e149911b429fa3e56ff243f1",
  "accepted_pdf_sha256": "34c2ff2b3a42c84d9b25420d68aa90de6181323b15623fee629dace9d34a8ba3",
  "rebuilt_pdf_sha256": "90688ba363e5d58f1300766b54223a814f1c6e57af9f477a92ffa17db43936f0",
  "verdict": "PASS"
}

The comparison uses extracted plain text (PyMuPDF) and page count; PDF byte hashes are recorded for information because TeX embeds compilation metadata.
