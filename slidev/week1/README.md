# CCGL9065 Week 1 — Slidev prototype

This is the source for the redesigned Week 1 lecture, **Will AI Take Your Job—or Just Make Everyone’s Work Look the Same?**

## Run locally

```sh
npm install
npm run dev
```

## Build for the Quarto site

```sh
npm run build
```

The static deck is written to `../../slides/week1/`. The Quarto project copies that folder into `_site/slides/week1/` through the `resources` setting in `_quarto.yml`. The production build uses hash-based routing so direct slide links continue to work when the deck is hosted in this subdirectory.

## Teaching notes

- The deck is intentionally an argument rather than a technology survey.
- The *Nightborne* extract is embedded from the official Barley Studios upload and starts at 06:43. Play roughly 60–70 seconds, then replay it using the close-reading prompts.
- Claims carry short linked sources on their slides; the final two slides provide full references.
- “AI slop” is introduced as a working course definition, not a settled technical category.
