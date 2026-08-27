# RPG workshop production notes

This directory contains the two-session workshop **Teaching Through Designed Friction: AI, Critique, and Pedagogical Reasoning for PhD Students**. At HKU, RPg means research postgraduate; the primary audience is incoming RPg/PhD students who are about to begin teaching.

## Schedule requiring official confirmation

The working handoff specifies:

- Day 1: Thursday 27 August 2026, 3:00–4:00 pm
- Day 2: Friday 28 August 2026, 2:00–4:00 pm

These details have not been independently verified against an official organizer notice. Confirm the dates, times, room, delivery mode, and time zone before circulation. The official notice must supersede this README and the landing page if they differ.

## File map

| File | Purpose | Output |
|---|---|---|
| `day1.qmd` | Incident analysis and Oracle encounter deck | `day1.html` |
| `day2.qmd` | Trace analysis, friction design, and micro-test deck | `day2.html` |
| `workshop.css` | Shared 1600×900 RevealJS layout system and Day 2 visual base | embedded in each deck |
| `day1-quarto.css` | Day 1 white, Quarto-first visual reset | embedded after `workshop.css` in Day 1 |
| `index.qmd` | Participant-facing landing page and route map | `index.html` |
| `workbook.qmd` | Printable/HTML participant artifact chain | `workbook.html` |
| `facilitator.qmd` | Setup, scripts, run sheets, adaptations, and contingencies | `facilitator.html` |
| `sample-case.qmd` | Fictional hybrid-studio research proposal | `sample-case.html` |
| `assets/supplied-hybrid-studio-case.pdf` | Upload-ready, fictional fallback case | static PDF |
| `sample-transcript.qmd` | Synthetic, coded Oracle trace using the same case | `sample-transcript.html` |
| `site.css` | Shared styling and print rules for normal HTML pages | linked by companion pages |
| `README.md` | Build, validation, and limitation notes | source only |

## Artifact continuity

All participant-facing materials should preserve one chain:

1. a bounded, privacy-safe AI incident;
2. a continuous Oracle or peer-Oracle episode following one machine-selected issue;
3. coding for confirmed / reframed / challenged / misread / meaningful moments;
4. a short Day 2 partner reading with owner correction/veto and one careful content-free note;
5. an owner-approved New-area card mapping what the prepared questions missed—or evidence-based “nothing new here”;
6. a content-free room map;
7. a distinction between meaningful, failed, and misdirected friction;
8. an expert-to-novice transfer problem;
9. a teaching-pressure sequence with target thinking, shortcut, prompt, evidence, access route, and clear end point; and
10. a revision justified by micro-test evidence.

The supplied fallback episode is consistent across the companion materials: a fictional education/design proposal claiming that hybrid studios improve first-year students' confidence in design critique. Its pre/post survey design cannot isolate the format from time, practice, or familiarity. The defensible reframe is reported change within the cohort, a descriptive role for participation counts, and an explicit attribution limit. The synthetic trace begins with an Oracle opening, follows the same issue through researcher responses, includes a correctable misread, and ends with a question-free closure.

## Socratic Oracle deployment contract

The live [Socratic Oracle](https://socraticoracle.netlify.app) is a PDF-led workflow, not a prompt box:

1. Browser PDF.js extracts searchable text and builds page-aware chunks. PDF bytes are not sent to Netlify or written into browser storage; the full extracted corpus and session remain in the current tab's `sessionStorage`.
2. A balanced, bounded coverage packet is sent for a source-linked paper map. The service selects up to three pressure points and makes one active for the displayed opening challenge.
3. The Oracle challenge is text on screen. Voice mode means that the participant answers aloud. Browser-local Whisper creates an editable transcript; only the reviewed/submitted text, not raw audio, is sent for tutoring. Keyboard is an equal route. The deployed web client has no text-to-speech path.
4. Follow-up turns send bounded locally retrieved passages, recent dialogue, and signed Oracle state. The participant stays with one issue until the interface reports a stopping point or the participant stops.
5. A resolved/deferred point receives a short question-free recap, then the interface offers **Examine another issue** or **End session**. Operational closure is not an epistemic verdict.

The browser client accepts PDFs up to 10 MB and 100 pages and does not provide browser OCR for an image-only scan. The browser session expires after two hours. Treat those values as current implementation details and recheck them before delivery.

On 11 August 2026 the live `/health` response reported `browser_whisper` speech input and research sharing available with its default set to `true`. Workshop delivery therefore requires participants to uncheck **Share this session with the research team** before Start and to verify that the control remains off. This opt-out prevents the optional research-copy relay; it does not prevent the model-processing requests needed for the tutor exchange.

Ending a session downloads JSON locally. That export can include the full dialogue, document metadata, bounded paper context, a document manifest, and Oracle state/diagnostics. It does not contain the complete browser-local chunk corpus or raw audio. The workshop never exchanges or collects this JSON.

## Day 2 short-episode contract

Day 2 is an evidence exchange with the trace owner retaining authority—not peer review of the proposal:

1. owner privately reflects on meaningful, failed, and misdirected friction;
2. owner selects view, content-free description, supplied trace, or solo route;
3. partner follows what changed, uses the prepared questions with C/R/X/M/★ marks, then sets those labels aside;
4. owner corrects context and may veto any interpretation or further use;
5. owner and partner make one evidence-anchored New-area card as extending, connecting, or sitting outside the prepared questions—or record “nothing new here”;
6. owner and partner write one careful, content-free note and may preserve disagreement; and
7. the room receives only an approved abstract area, definition, relation to the prepared questions, observable sign, and limit or counterexample.

No screenshots, copies, links, forwarding, recording, retention of another person's material, or reporting of research detail are permitted. The source remains on the owner's device or paper. Supplied and solo routes are equal and can contribute to the room map. Passing and evidence-based “nothing new here” are valid.

## Participant reading source of truth

The landing page section [Required and recommended reading — before Day 1](index.qmd#required-and-recommended-reading-before-day-1) is the canonical participant list. Lee et al. and Kosmyna et al. are required; the methodological comment paired with Kosmyna is part of that required bundle. Becker et al./METR and Fernandes et al. are recommended; participants who read METR should use the 2026 study-design update alongside it. Murrell's **The Age of Average** is an optional convergence refresher.

The landing page also owns the between-session preparation: one owner-selected, already-redacted Oracle episode, with the synthetic supplied transcript as an equal route. Decks and email copy should link to this section instead of maintaining parallel bibliographies. Before circulation, check every external link, preserve an alternate-format route, and ensure the source descriptions still match the linked pages.

## Render configuration requirement

The workshop sits one level below the original `genai/` files. A full-project render must explicitly include the nested sources. Confirm that the root `_quarto.yml` render list includes a pattern such as:

```yaml
project:
  render:
    - "genai/rpg-workshop/*.qmd"
```

The older `genai/*.qmd` pattern does **not** match files in this subdirectory. Do not assume an explicit one-file render proves that the full website build includes the workshop.

## Build commands

From the repository root:

```bash
quarto render genai/rpg-workshop/day1.qmd
quarto render genai/rpg-workshop/day2.qmd
quarto render genai/rpg-workshop/index.qmd
quarto render genai/rpg-workshop/workbook.qmd
quarto render genai/rpg-workshop/facilitator.qmd
quarto render genai/rpg-workshop/sample-case.qmd
quarto render genai/rpg-workshop/sample-transcript.qmd
```

After nested render coverage is present in `_quarto.yml`, build the complete site with:

```bash
quarto render
```

For local review of an individual entry point:

```bash
quarto preview genai/rpg-workshop/index.qmd
```

The repository's project-level post-render hook uses Node to filter sitemap entries. The workshop itself has no Python or R execution cells. The current local baseline identified during authoring was Quarto 1.5.56 and Node 22.17.0; these are observations, not a locked toolchain.

## Validation commands

Check source presence:

```bash
for file in day1.qmd day2.qmd index.qmd workbook.qmd facilitator.qmd sample-case.qmd sample-transcript.qmd workshop.css day1-quarto.css site.css README.md assets/supplied-hybrid-studio-case.pdf; do
  test -f "genai/rpg-workshop/$file" || exit 1
done
```

Check expected build outputs after rendering:

```bash
for file in day1.html day2.html index.html workbook.html facilitator.html sample-case.html sample-transcript.html; do
  test -f "_site/genai/rpg-workshop/$file" || exit 1
done
```

Inspect local and external links in source:

```bash
rg -n '\]\([^)]*\)|href="[^"]+"' genai/rpg-workshop/*.qmd
```

Serve the whole output directory so relative site links are tested in their deployed shape:

```bash
python3 -m http.server 8000 --directory _site
```

Then review `http://localhost:8000/genai/rpg-workshop/`.

## Visual validation

Review both decks at a 1600×900 viewport and at the actual room's projector resolution. At minimum, check:

- no clipped content, especially workbenches, transcript sheets, the Day 2 timetable, worked examples, and teaching-pressure card;
- slide numbers and controls remain legible without obscuring content;
- white slides preserve contrast for muted text and restrained accent colors;
- C/R/X/M/★ meanings remain readable without color;
- all participant instructions can be followed from text alone;
- keyboard navigation, focus indication, 200% browser zoom, and reduced-motion preference;
- A4 print preview for workbook, facilitator guide, case, and transcript; and
- links among landing page, decks, workbook, facilitator guide, and samples.
- external required-reading and evidence links, their visible PDF/HTML labels, and the alternate-format route.

The Reveal decks use `embed-resources: true`, so their HTML files will be comparatively large but portable. External hyperlinks still require network access.

## Visual system

`workshop.css` supplies the shared layout geometry and component fallbacks:

- orange-red for active structure and questions;
- pale gray for working surfaces and secondary guidance;
- green for privacy and access safeguards; and
- blue and purple for evidence and interpretation where a distinction helps.

Day 1 loads `day1-quarto.css`, which resets the shared treatment to the built-in Reveal `simple` theme: white canvas, near-black text, restrained orange emphasis, pale warnings, and thin gray rules. Day 2 uses the same base plus `day2-quarto.css` for its timetable, pressure-placement map, plain sequence, and worked examples. Both decks are white, vertically centered, and use the shared geometry without saturated poster-like surfaces.

The system is intentionally flat and diagrammatic rather than card-driven: rules, axes, search fields, transcript annotation surfaces, tally boards, workbenches, and design canvases. Inline SVG is used where a diagram materially improves understanding. No external raster asset is required.

`site.css` governs the normal HTML companions and includes A4 print rules. It does not store workbook input; participants should print, annotate a local copy, or keep notes in an authorized local system.

## Privacy and fallback contract

- Never require use of personal research material.
- Do not enter confidential, identifiable, participant-related, collaborator-owned, proprietary, restricted, or sensitive unpublished material into a public AI service.
- Treat “file remains in browser” and “no remote model processing” as different claims.
- Uncheck optional research sharing before Start and verify that it remains off throughout the workshop; it was selected by default during authoring. Any research contribution requires a separate, authorized, informed process outside class participation.
- Do not collect transcripts, downloaded JSON, research files, or participant artifacts by default.
- For Day 2, circulate only an owner-selected, already-redacted bounded episode or a content-free description; prohibit screenshots, copying, forwarding, recording, and retention. The owner may correct or veto an interpretation.
- Preserve supplied-case, observation, non-text, solo, and offline peer-Oracle routes as equivalent ways to meet the learning outcomes and contribute to the content-free room map.
- Recheck the live Oracle's disclosure, availability, and sharing behavior immediately before delivery.

## Current limitations and confirmations

1. **Schedule:** dates and times are provisional until matched to an official organizer notice.
2. **Room and cohort:** no confirmed room, cohort size, device provision, Wi-Fi arrangement, or accommodation list is encoded here.
3. **Live service:** on 11 August 2026, the health endpoint reported the tutor available, browser-local Whisper voice input, and research collection available with its default set to `true`. The deployed interface displays Oracle questions as text; participants speak or type responses, review voice transcripts before Send, and receive sustained follow-ups on one active issue. The landing disclosure said an enabled research copy contains the transcript, session details, and bounded paper context; the client sends bounded coverage for the opening and retrieved passages plus recent conversation for follow-ups. The workshop therefore instructs participants to switch sharing off before Start. Provider retention and institutional authorisation remain unverified, and every point must be checked again on the delivery day.
4. **Build inclusion:** the root render list now covers the nested QMD sources, and a 46-input full-project render succeeded locally with Quarto 1.5.56.
5. **Deployment:** local generated HTML is built, linked, and visually inspected. Publishing and checking the deployed URLs remain separate steps.
6. **Print:** Chrome A4 previews were inspected for the workbook, facilitator guide, fictional case, and sample transcript. The actual delivery browser and printer still require a short check.
7. **No persistence:** workbook fields are writing surfaces, not a saved web form.
8. **No real evidence claim:** the supplied case and dialogue are fictional pedagogical artifacts, not research results or an evaluation of the Oracle.
9. **Versioning:** there is no package lock or CI build specifically for this workshop.
10. **Link visibility:** the parent GenAI landing page now links the workshop as a separate supplement to the existing three-class module.

## Production acceptance checklist

- [ ] Official schedule and room confirmed
- [x] Root project render includes nested QMD files
- [x] Full-site render succeeds (46 inputs; verified 12 August 2026)
- [x] All seven expected workshop HTML outputs exist
- [x] Landing and parent-module links resolve
- [x] Day 1 and Day 2 reviewed at 1600×900
- [x] No slide overflows in projector and PDF/print modes
- [x] Workbook and facilitator pages reviewed in A4 print preview
- [x] Fictional sample is identical in substance across all materials
- [x] Live disclosure and research-sharing control checked during authoring
- [x] Offline sample case and continuous trace available
- [ ] Live service, sharing default, and disclosure rechecked immediately before delivery
- [ ] Accessibility and cohort adaptations agreed with organizer
- [x] No confidential material appears in workshop examples or generated outputs
