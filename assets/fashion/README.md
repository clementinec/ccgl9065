# Week 3 visual teaching materials

The editable source is `CCGL9065_W3.qmd`. The course homepage opens its generated
Slidev version at `slides/conversion/week3/`. The shared CSS is scoped to the
`fashion-*` classes and is also used by the Notion guide.

## Figures

All six SVGs are original teaching diagrams. They work without external image
requests and include accessible titles and descriptions.

- `denim-lifecycle.svg`: simplified garment stages.
- `denim-hotspots.svg`: published rounded water and climate shares from
  [Levi Strauss & Co., The Life Cycle of a Jean (2015), pp. 21–22](https://www.levistrauss.com/wp-content/uploads/2015/03/Full-LCA-Results-Deck-FINAL.pdf).
  Other stages are grouped; this is a historical 501 case, not a current industry
  average. The two bars each total 100% of their own impact indicator.
- `denim-routes.svg`: repair/reuse, upcycling, textile-to-textile recycling and
  downcycling. These routes do not establish an environmental ranking.
- `denim-upcycling.svg`: illustrative jeans-to-bag reconstruction. See
  [Redress’s definitions](https://redress.com.hk/educational-resource/upcycling-reconstruction/).
- `denim-downcycling.svg`: simplified denim-to-insulation route based on
  [Blue Jeans Go Green](https://bluejeansgogreen.org/faq/). The programme also calls
  this upcycling; the lecture explicitly discusses the differing perspectives
  on material quality and final product value.
- `system-boundaries.svg`: simplified comparison of included processes; a next
  product needs explicit assumptions about processing and shared impacts.

The per-wear arithmetic on the slides is hypothetical and labelled as such.

## Lecture flow and presentation recipe

The overview connects Notion logistics,
the open-loop callback and cross-sector comparisons, contrast, the garment's
life and reuse/upcycling/downcycling options, LCA and system boundaries, the
fashion-retailer responsibility debate, and the closing Barnum segment.
The suggested presentation recipe follows the random vocational assignment and
precedes the timer: role, daily work and stakes, then a supported position on
the motion, a counterargument and a clear ask.

The denim-to-insulation video now leads directly into LCA and system boundaries;
the route-selection exercise and the following “Better” recap have been removed.

## Title spacing

The shared Slidev cover and section styles explicitly override the default
theme's fixed 80px line height. Cover titles use 1.12 line height; section titles
use 1.15. The cover subtitle also has more separation and 1.25 line height.
This preserves the existing type sizes, weights and body-slide styling. Week 3
has been rebuilt; other converted weeks pick up these shared rules on rebuild.

## SHEIN case replacement

The former “Voices From the Battlefield” section is now a four-slide SHEIN case:
a demand-feedback diagram, a dated scale/scrutiny timeline,
the distinction between recycled content and a recyclable garment, and a short
Temu/PDD comparison. Allow roughly four minutes for the case.
“Two Stories, One Industry” now revisits this case through two policy pitches,
immediately followed by the exact debate motion, moved from ahead of the case.
The seven-slide “Would You Rather?” / dilemma / ethics detour and repeated
spectacle formula and speeches have been removed. The route is now case → two
positions → motion → credibility and role-play preparation. The credibility
slide distinguishes a regulatory finding, a company account and a student's
argument. The opening logistics, presentation recipe and Barnum segment remain.

These are editable HTML/CSS diagrams, not screenshots or reproductions of shop
interfaces. The timeline is “rise and reality check”, not an unverified claim
that SHEIN has collapsed. The 2026 investigation is labelled as an opening event,
not a final finding. Corporate accounts are attributed; the sample pitches are
explicitly illustrative, with no invented worker testimony.

Sources checked on 15 September 2026:

- [SHEIN on initial batches and restocking (2025)](https://www.sheingroup.com/newsroom/shein-ramps-up-denim-production-using-cool-transfer-denim-printing-by-90-in-2024).
- [H&M's business proposition](https://hmgroup.com/about-us/business-idea/).
- [EC platform designation, 26 April 2024](https://digital-strategy.ec.europa.eu/en/news/commission-designates-shein-very-large-online-platform-under-digital-services-act).
- [AGCM green-claims decision summary, 4 August 2025](https://en.agcm.it/en/media/press-releases/2025/8/PS12709).
- [EC investigation opening, 17 February 2026](https://digital-strategy.ec.europa.eu/en/news/commission-launches-investigation-shein-under-digital-services-act).
- [SHEIN's brand/marketplace description](https://www.sheingroup.com/our-group).
- [PDD 2025 annual report, pp. 3, 70–72](https://investor.pddholdings.com/static-files/92dafbdc-3125-4f2c-a28f-3d61203efbaf).

This flow edit is not a full audit of older statistics and quotations. The LCA
takeaway is that boundaries must be justified alongside the functional unit,
impact measures, data and trade-offs—not that choosing a boundary can make
anything sustainable.

## Logistics stage colours

The opening slides use blue (`fashion-before`) for preparation, including
tutorial; amber (`fashion-during`) for role-based refinement and both live
reflection types; and teal (`fashion-after`) for the final takeaway and cleanup.
The spectacle row blends blue into amber to show that the pitch already exists
before the role assignment. Written labels accompany the colours, and neutral
callouts indicate instructions that apply across the whole weekly entry.

## Videos and teaching cues

Links and embed metadata checked on 15 September 2026. Playback needs an internet
connection. Every slide has a direct viewing link and a figure-based fallback.

| Video | Classroom excerpt | Viewing task |
|---|---|---|
| [TED-Ed / Angel Chang: The life cycle of a t-shirt](https://www.youtube.com/watch?v=BiSYoeqb_VY) | 0:00–2:00 | Track the changes from plant to garment. |
| [Redress / Orsola de Castro: Up-cycling Design Tutorial](https://www.youtube.com/watch?v=b7n8AVUE_dg) | 0:00–2:00 | Notice a decision shaped by the available fabric. |
| [Discover Cotton: The Blue Jeans Go Green Denim Recycling Process](https://www.youtube.com/watch?v=LaAcguFBtzM) | Full 1:33 | Identify where fabric becomes fibre; name missing evidence. |

The older Redress clip `U_f_MNIUC54` is private; use the linked Orsola de Castro
tutorial. Process videos illustrate a route, not a measured net environmental
saving. Presenter notes supply discussion prompts and contextual qualifications.

## Updating this week

From the repository root:

```sh
python3 slidev/conversion/convert_quarto.py week3
```

From `slidev/conversion/`:

```sh
node build-all.mjs week3
```

Render `notion_guide.qmd` and `CCGL9065_W3.qmd --to revealjs` with Quarto after the
Slidev build so the website copies the latest deck. These commands do not publish
the website.
