# Lecture rebuild log

Working notes for the 2026 lecture refresh: what was rebuilt, what was
published, and what to pick up next. Not part of the website (Quarto only
renders `.qmd` files listed in `_quarto.yml`).

## How the site is published

- The live site is served from the **`gh-pages`** branch, which `quarto publish
  gh-pages` writes. It has been built with **Quarto 1.10.19**.
- `main` keeps the sources plus a committed `_site/`, but **`_site/` on `main` is
  stale** (parts were built with Quarto 1.5.56) and is not what is live.
- The live site has been published from a local copy that is **ahead of `main`**
  (see "Not yet in the repo" below). A full `quarto publish` from this repo
  would overwrite those local-only changes.
- Until the repo is caught up, publish a single deck the way Weeks 8 and 10
  were published: render the deck, then on a checkout of `gh-pages`
  1. copy in the new `CCGL9065_Wn.html` (decks use `embed-resources`, so the
     one file is enough),
  2. edit only that week's card in `index.html` and its row in
     `slidev_conversion.html`,
  3. replace that deck's entries in `search.json` with the fresh ones,
  4. commit and push to `gh-pages`.
- Rendering in a cloud session: Quarto is not preinstalled. Download
  `quarto-1.10.19-linux-amd64.tar.gz` from the quarto-cli GitHub releases
  (`pip install quarto-cli` stalls). Rendering also touches `.gitignore` and
  copies stray files into `_site/data` and `_site/site_libs`: revert/delete
  those before committing.

## The rebuild recipe (Weeks 7, 8, 10)

Each rebuilt week is `CCGL9065_Wn.qmd`, a Reveal.js deck at 1920×1200, built
on the Week 8 style block (`CCGL9065_W8.qmd`, copied with the `w8-` class
prefix renamed, e.g. `w10-`):

- coloured part dividers (`# Part n · Title {background-color="…"}` plus a
  `.wn-sub` line), dark hero-image slides with `.wn-hero-cap` / `.wn-hero-credit`
- number tiles, chains (`.wn-chain`), loops (`.wn-loop`), cards, bar charts
- evidence labels on claims: Settled / Emerging / Debated / New evidence
- a source line (`.wn-src`) under every factual slide; corrections to old
  figures go in speaker notes
- the debate block: two sides, core tension, "Why this motion?", motion,
  random group assignment, the **colour-by-minute countdown**, talking points
- takeaway, "The Semester So Far" map, "Two Threads That Run to Week 11",
  the week's Persuasion Playbook strategy, next-week preview, sources
- homepage card (`index.qmd`) and archive row (`slidev_conversion.qmd`) point
  at the Quarto deck; the Slidev conversion is kept as the earlier version

## 2026-11-16–17 — Week 11 rebuilt in Quarto

**Branch `codex/week11-refresh`**, based on the latest teaching branch
`claude/youthful-lovelace-xje7nt` at `7c24d77` (not stale `main`).

- Rebuilt `CCGL9065_W11.qmd` and `_site/CCGL9065_W11.html`: **59 slides**,
  including the title and reference slides. Week 10's Quarto design language
  carries through the coloured dividers, image slides, cards and causal loop.
- Refocused after course-lead review: **second homes, retaining responsibility
  for Earth and the concern about deserting it** now drive the lecture.
  Earthrise leads directly to Musk's dated, sourced survival argument; the
  Mars/MOXIE/independent-backup sequence tests that promise. “Insurance” and
  “abandonment” are interpretations to examine, not assumed consequences or
  attributed motives. “A backup for whom?” distinguishes continuity of
  civilisation from protection of people living here.
- Compressed satellite and atmospheric material into supporting evidence.
  Hong Kong warning access, DART and the debris feedback loop show why
  exploration and responsibilities on Earth cannot be treated as opposites.
  The public-funding debate and Earthrise return complete the story.
- Musk's quotation is from his 2017 authored paper, based on his 2016 talk.
  Current SpaceX lunar/Mars goals are identified as development goals; NASA's
  MOXIE result is explicitly separate. The optional official talk is linked.
- Added three recent anecdotes after the next course-lead review: Musk's
  February 2026 lunar-city priority announcement; the CHAPEA crew's October
  2026 completion and November account of everyday supplies/ground support;
  Starbase's May 2025 incorporation vote and its mayor's dual public/SpaceX
  roles. Each has an explicit second-home question and primary sources.
  Replaced two repeated abstract-framework slides, adding one reference slide
  for a net increase of two slides. CHAPEA is visibly a Houston simulation;
  the governance extension is hypothetical; the county vote record retains
  its “unofficial results” qualifier. NASA's authentic crew photos are linked.
- Reworked the isolated Moon-pivot anecdote into a short chronological
  backtrack: 2016–17 Mars ambition → January 2025 “Moon is a distraction”
  statement → February 2026 Moon-city priority. The 2021 NASA lunar-lander
  selection remains visible context: a changed public priority is not a
  claim that the Moon first entered the programme in 2026. The January quote
  is sourced to contemporaneous Ars Technica reporting and the original post.
- Followed this with “Easier to reach—for what?” (folding in the old
  visit/settle/backup framework), then a conditional resource-management chain.
  NASA/JPL and USGS support the distinction between material being present,
  practical access and dependable supply. Depletion prompts choices among
  extraction, recovery, demand and imports; it is not attributed as Musk's
  explanation, a forecast that Earth is nearly empty, or a lunar-mining cost
  claim. MOXIE now follows as the worked example of resource conversion.
- New motion: *“This house would redirect new public funding for permanent
  human settlements on the Moon or Mars to climate adaptation on Earth for
  the next ten years.”* Visible definitions cover future commitments,
  permanent residence, adaptation, excluded activities and mixed-use projects.
- Preserved six stakeholder roles, five-minute presentation limit and the
  50-minute activity. Roles can take either side. Assignment results persist
  for the browser session; the Week 10 colour-by-minute timer is retained.
- Updated evidence: ESA's February 2026 model population (page updated
  13 November 2026), MOXIE's 122 g total, carefully bounded DART results,
  rocket-soot modelling and observed re-entry metals. Removed unsupported
  spending comparisons, universal overview-effect claims and automatic
  self-persuasion claims. Source links and limitations are on slides/in notes.
- Updated `index.qmd`, `slidev_conversion.qmd`, their generated HTML pointers
  and Week 11 search entries. The earlier Slidev version is retained.
- Rendered with Quarto 1.10.19. Google Fonts were unreachable in this session;
  the rendered deck reuses the fully embedded simple-theme stylesheet from
  `_site/CCGL9065_W10.html`. It has no external script or stylesheet dependency.
  A normal connected re-render should embed these fonts directly.
- Added one final-portfolio deadline slide: presenters in the last class on
  Wednesday 25 November submit by Tuesday 24 November, 11:59 PM; students
  not presenting submit by Sunday 29 November, 11:59 PM. All dates are 2026
  and all deadlines use Hong Kong time (UTC+8).
- Validation: 59 slides; all four images embedded with alt text; no duplicate
  IDs or broken local links; all 20 inline scripts parse; Reveal menu loads;
  role uniqueness/session restore/reset and all timer bands/pause/resume/reset/
  deadline expiry pass. Browser visual inspection was unavailable: browser
  host failed and Safari UI access returned `cgWindowNotFound`.

**Published on 17 November 2026.** Quarto and the updated `index.qmd` pointer
were confirmed before publication. Terminal GitHub DNS was unavailable, so
the GitHub connector uploaded an identical source-tree snapshot to remote
`codex/week11-refresh` at `22b5d10` (same tree as local `c866b66`; the local
incremental history is retained separately).

- `gh-pages` commit `8f2ef36` changes exactly four files: the standalone
  `CCGL9065_W11.html`, Week 11 homepage card in `index.html`, archive row in
  `slidev_conversion.html`, and Week 11 records in `search.json`. All other
  published pages/assets, including the live-only Week 9, retain their hashes.
- GitHub Pages build, report and deployment jobs succeeded:
  https://github.com/clementinec/ccgl9065/actions/runs/44032824415 .
- Deck: https://clementinec.github.io/ccgl9065/CCGL9065_W11.html .
  Deadline slide: `#/final-portfolio-two-submission-deadlines`.
- Published blob hashes match the checked local files. A fresh hosted-page
  visual check remains unavailable: terminal DNS and browser/web access to
  the Pages host failed in this session. Deployment success is confirmed
  through GitHub Actions; this does not claim a live browser inspection.

## 2026-11-09 — Week 10 rebuilt and published

**Branch `claude/youthful-lovelace-xje7nt`**

- `afd9122` Rebuild Week 10 cascade lecture in Quarto
  - new `CCGL9065_W10.qmd` (+ `_site/CCGL9065_W10.html`), 64 slides
  - structure: three shapes of cascade (chain, loop, cliff); Part 2 is
    *Clarkson's Farm* Season 1 as the worked cascade (the £144 year: wet
    autumn 2019 → wettest February on record → record sunny/dry spring 2020 →
    national wheat harvest down ~40% → £144); ice–albedo and permafrost;
    tipping points; fixes that cascade (Aral Sea, Carson, geoengineering)
  - the £144 opens the lecture and returns at the end, demonstrating
    Strategy #9, the Cliffhanger Return
  - new motion: *"This house believes that governments should pay farmers to
    protect soil, water and climate rather than to maximise food production —
    even if it means growing less food at home."* (replaces geoengineering)
  - corrected figures: Arctic warming ≈ 4× global; methane ≈ 80× (20 yr) /
    ≈ 30× (100 yr); permafrost release as a gradual leak; tipping thresholds
    from Armstrong McKay et al. (2022); coral reefs likely past their tipping
    point (2025); Yellowstone "wolves moved rivers" labelled Debated
- `ab3c4f0` Align Week 10 recap with live Week 9 and sync homepage links
  - Week 10 recap rewritten to match the revised, live Week 9
  - `index.qmd`: Week 9 → `W9.html`, Week 10 → `CCGL9065_W10.html`, archive
    band wording as on the live site
  - `slidev_conversion.qmd`: replaced with the live archive page content
    (Weeks 7–10 current in Quarto)

**Branch `gh-pages` (live)**

- `0158736` Publish rebuilt Week 10 cascade lecture — added
  `CCGL9065_W10.html`; Week 10 card in `index.html`; Week 10 row in
  `slidev_conversion.html`; Week 10 entries in `search.json`

**Checked with the course lead:** the Lamborghini tractor being too big for
the farm, and the wet-then-drought farming year, both match the show. The
"90%+ of Hong Kong's food is imported" figure is kept as is.

**Old files kept:** `W10.qmd` (original Quarto deck) and
`slidev/conversion/week10.md` (Slidev conversion) are unchanged.

## Not yet in the repo (live only)

- **Revised Week 9.** The live `W9.html` (Part 1 "Who Counts as a Climate
  Refugee?" … Part 9 stakeholder debate, Tai Po evidence exercise) has no
  committed source; `W9.qmd` in the repo is the older deck. Commit the local
  source, or rebuild `W9.qmd` from the live page.
- **Theme/style changes.** Live pages use a different compiled Bootstrap
  stylesheet than a build from this repo, so local style changes are also
  uncommitted.
- **`main` is behind.** All of the above work is on
  `claude/youthful-lovelace-xje7nt`; merge it into `main`.

## Next up

- Week 11 is rebuilt in `CCGL9065_W11.qmd`; the earlier Slidev deck remains
  available in the archive. The Quarto deck is now published.
- Weeks 2–6 still open their Slidev conversions from the homepage.
