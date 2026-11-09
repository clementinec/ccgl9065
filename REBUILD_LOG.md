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

- Week 11 (Space & planetary futures) is still the Slidev conversion. To
  rebuild: start from `CCGL9065_W11.qmd` and the recipe above; the Week 10
  "Two Threads" slide sets up Week 11 (the Kessler cascade of space debris,
  and Strategy #10: no framing is neutral).
- Weeks 2–6 still open their Slidev conversions from the homepage.
