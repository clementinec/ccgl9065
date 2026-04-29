# Essay extraction notes

- Scope: processed `data/2026/essay_pass` only.
- Manifest: `data/2026/essay_pass/manifest.txt` was treated as a manifest and excluded from the CSV. It reports 36 requested files, 36 successes, and 0 failures.
- Filename parsing: all 36 non-manifest files matched the Moodle pattern `submission id - student name - student number_original filename.ext`.
- Output paths: all paths in `essay_extract.csv` are relative to the repository root.
- Existing PDFs: 34 submissions are already PDF files, with `essay_pdf_path` set to the source PDF path and `conversion_needed=false`.
- Conversion needed: 2 submissions are DOCX files and were not converted. Their `essay_pdf_path` is blank and `conversion_needed=true`:
  - `225592` Hua Zong: `data/2026/essay_pass/2946489991 - Hua Zong - 225592_Hua_Zong_essay_4021069_2111720163.docx`
  - `351352` Shijun Feng: `data/2026/essay_pass/2946665379 - Shijun Feng - 351352_Shijun_Feng_Shijun_Feng_Essay_4021069_296110792.docx`
- Anomalies: no filename parse failures, no manifest download failures, and no unsupported extensions beyond the two DOCX files requiring later PDF conversion.
