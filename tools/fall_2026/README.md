# Fall 2026 exhibition ledger

Use this ledger when the LMS exports the whole class again. The two CSVs contain anonymous portfolio IDs and fit in about 16 KB together. The local workbook-to-gallery crosswalk lives in the ignored `.exhibition-imports/fall-2026-roster-map.csv`.

- `portfolios.csv` has one row per gallery ID. An empty component is pending. Collages and local videos are identified by the SHA-256 of the public file, essays by the SHA-256 of the reader text, and hosted videos by their public embed URL. The gallery manifest supplies this snapshot, including submissions originally found on Notion.
- `reviewed_files.csv` accumulates one receipt per reviewed export submission version and component. Its hash combines the numeric LMS submission ID with the file content hash. A changed file or a different student's submission therefore comes up for review, even if filenames or content overlap. The two excluded weekly-work submissions have receipts. Notion-only work has no LMS receipt until its export is reviewed.

From the repository root, check a new export locally. The output lists original filenames, so keep it private.

```sh
python3 tools/fall_2026/ledger.py pending collage /path/to/collage-export
python3 tools/fall_2026/ledger.py pending essay /path/to/essay-export
python3 tools/fall_2026/ledger.py pending video /path/to/video-export
```

Match the pending files using the private roster crosswalk. After updating and verifying the gallery, record each decision and refresh the snapshot. A new submission hash signals a file to inspect, which may still point to artwork already on display.

```sh
python3 tools/fall_2026/ledger.py record essay "/path/to/123 - student - essay.pdf" imported --portfolio p40
python3 tools/fall_2026/ledger.py record collage "/path/to/456 - student - weekly.pdf" excluded
python3 tools/fall_2026/ledger.py sync
```

Commit the CSV updates alongside the gallery change. Old receipts stay in the ledger when a file is revised. The snapshot reflects the current gallery and Git tracks its history. Run a fresh Notion scan when checking changes made directly to a public portfolio.
