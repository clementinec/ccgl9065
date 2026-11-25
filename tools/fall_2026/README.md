# Fall 2026 exhibition handoff

Run the commands below from the repository root on `main`. The gallery reads [the public manifest](../../data/students_2026_fall_public.json). [The Fall page](../../exhibition_2026_fall.qmd) supplies the four visible totals. [The shared gallery script](../../assets/2026/gallery.js) renders the tiles, players and essay dialog for both semesters.

The 25 November 2026 release covered the original LMS exports, `Additions`, `Additions2`, and the public Notion pages available at the time. It had 44 portfolios, 41 collages, 36 essays and 36 videos (source `67e3828`, Pages `602776e`). Read [portfolios.csv](portfolios.csv) for current coverage. Blank cells are pending. P21’s previous collage submission was a text outline. P43 had a collage and video and was awaiting an essay.

## Match the student once

On the course machine the private workbook is `~/Downloads/courseid_138992_student_work_W11_graded_2026-11-20.xlsx`. The ignored `.exhibition-imports/fall-2026-roster-map.csv` maps the actual Excel row in **Weekly Notion** (header is row 1) to a stable gallery ID such as `p04`. LMS filenames carry a numeric submission ID and the student’s name. Match the name to the workbook, then use that workbook row to look up the gallery ID. The submission number, roster position, and public portfolio number are distinct.

A fresh clone needs the private workbook and crosswalk from the course maintainer. Until those are available, a new agent can run the ledger comparison and inspect anonymous coverage. Resolve ambiguous matches against the private roster before assigning an ID. Give a genuinely new contributor the next number above the highest gallery ID and add the row to the private crosswalk. Keep the workbook, crosswalk, raw exports, Notion scan output and student-identifying filenames outside Git and the public site.

## Rescan Notion

1. Start with **W11 Link audit** in the workbook. Join its **Workbook row** to **Weekly Notion** and use **Selected/retained URL**. If that is empty or unusable, check **Notion Site URL (Porfolio Link)** on the matched roster row, then **Student Work** by email. Some rows have only a Moodle note or no URL.
2. Open the public homepages and their portfolio subpages, including entries in inline Notion databases. Skip titles containing “Weekly” or “Week 1” through “Week 11”. Inspect the homepage itself for submissions as well. Record unreadable links and missing URLs separately from accessible pages with no new work.
3. Look for the visual creation, the video and the reflective essay independently. Check embedded media, shared links, pasted iframe or image markup, and prose below essay headings. Compare each to the matched gallery record. A YouTube watch link and an embed with the same video ID represent the same film. Compare poster artwork visually and essay text by paragraphs, allowing for PDF line wrapping.
4. For a repeatable batch pull on the course machine, the local grading toolkit provides `~/Downloads/CCGL9065-Grading-Toolkit/notion_public.py`. Its `PublicNotion.load` and `extract` methods cache responses on disk. Use a fresh private cache for each poll and follow the same page-title exclusions. The browser procedure above also works without the toolkit. Report new or revised **components** separately from newly discovered pages. Notion-only work goes in the manifest and coverage ledger. An LMS receipt requires an actual exported file.

## Ingest a cumulative LMS folder

The three assignment numbers identify the components even when the export suffix changes. For example, check the delivered `Additions2` folder with these commands. Substitute the actual directories for the next export.

```sh
batch="$HOME/Downloads/Additions2"
python3 tools/fall_2026/ledger.py pending collage "$batch/190477081-3"
python3 tools/fall_2026/ledger.py pending essay   "$batch/190477082-3"
python3 tools/fall_2026/ledger.py pending video   "$batch/190477083-3"
```

[reviewed_files.csv](reviewed_files.csv) holds cumulative receipts keyed by component, numeric submission ID and file content hash. Keep original filenames when checking or recording. Inspect each pending file, including links inside PDFs, DOCX, RTF, text and screenshots. A new receipt can be a re-export of artwork already displayed, a revision of an existing essay, or a genuinely missing piece. Keep the existing public asset for equivalent work. Carry forward previous submissions that are absent from a later export.

- **Collage.** Open the artwork to check it is a visual submission. Use a stable direct image or supported embed URL where supplied. Store a small JPEG mosaic thumbnail under `data/2026_fall/thumbs/pXX.jpg`. For an uploaded image or poster PDF, create the public image under `data/2026_fall/anon/pXX/`. P36 shows a hosted collage and P42 an uploaded poster. Keep an outline or weekly worksheet pending.
- **Essay.** Extract the full prose and references, preserve paragraphs, and strip student bylines, IDs and submission headers. Populate `essay.available`, `essay.url` and `essay.text`. Write the same text as escaped HTML in `data/2026_fall/anon/pXX/essay.html`. The **Read full essay** dialog uses the manifest text. P13 is a worked example.
- **Video.** Use a YouTube embed URL (`kind: youtube`), a publicly viewable Google Drive preview (`kind: drive`), or an anonymous, browser-playable MP4 (`kind: local`). P42, P44 and P41 respectively demonstrate these cases. For a direct upload, check picture, sound and identifying metadata.
- **Partial entries.** Set missing component URLs to `null`, with `kind: none` for media or `available: false` for essays. Set the manifest count to the number of portfolios and update the four Fall page totals from the populated components.

After verifying the match and content, record each reviewed LMS file and refresh coverage. Use `imported` for a confirmed copy of a component already represented in the gallery as well as for newly added work. Use `excluded` for reviewed non-exhibition content. Leave uncertain items pending for follow-up.

```sh
python3 tools/fall_2026/ledger.py record essay "/path/to/123 - student - essay.pdf" imported --portfolio p40
python3 tools/fall_2026/ledger.py record collage "/path/to/456 - student - weekly.pdf" excluded
python3 tools/fall_2026/ledger.py sync
```

Rerun the three `pending` commands. A fully reviewed batch returns zero in each. Compare the ledger diff to the intended IDs and components.

## Render, verify and release

```sh
quarto render exhibition_2026_fall.qmd
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:8000/exhibition_2026_fall.html`. Check the totals and click every changed tile. Inspect the full collage, play each added video, and open and close each changed essay, including its final paragraph and references. Check visible work, metadata and filenames for student identifiers. If shared gallery or navigation code changed, also open the Spring page and check the Exhibition menu on desktop and mobile.

Stage the intended source files, both ledger updates when changed, and their rendered counterparts in `_site/` by explicit path. Review `git diff --cached --stat` and `git diff --cached --check` before committing and pushing `main`. A Quarto build can leave unrelated changes throughout `_site/`.

For a publication request, release the committed output to `gh-pages`. The example below assumes one scoped source commit at `HEAD`. For a release spanning several commits, set `before` to the source commit from the previous release. Run each step after the preceding one succeeds.

```sh
release=$(git rev-parse HEAD)
before=$(git rev-parse "$release^")
git -C _site diff --name-status --relative "$before" "$release" -- .
git fetch origin gh-pages
release_dir=$(mktemp -d)
git worktree add --detach "$release_dir/site" origin/gh-pages
git -C _site diff --binary --relative "$before" "$release" -- . > "$release_dir/gallery.patch"
git -C "$release_dir/site" apply --check "$release_dir/gallery.patch"
git -C "$release_dir/site" apply --index "$release_dir/gallery.patch"
git -C "$release_dir/site" diff --cached --stat
git -C "$release_dir/site" commit -m "Publish Fall exhibition submissions"
git -C "$release_dir/site" push origin HEAD:gh-pages
```

The patch paths start at the public site root. Review the file list and reconcile any overlap with a newer Pages release before pushing. After GitHub Pages finishes deploying, compare the live manifest and changed assets to the rendered files. Repeat the tile, essay and playback checks on the public URL. Report the new counts, any unresolved components, and the source and Pages commit IDs. [Live Fall exhibition](https://caadfutures2025.hku.hk/ccgl9065/exhibition_2026_fall.html)
