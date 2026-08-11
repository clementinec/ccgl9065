#!/usr/bin/env python3
"""Convert the existing CCGL9065 Quarto/Reveal decks into parallel Slidev decks.

The QMD sources are read-only inputs. Generated Markdown is written beside this
script and local media is copied into slides/conversion-assets for shared use.
"""

from __future__ import annotations

import html
import json
import platform
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CONVERSION_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CONVERSION_DIR.parents[1]
ASSET_OUTPUT = PROJECT_ROOT / "slides" / "conversion-assets"


@dataclass(frozen=True)
class Deck:
    slug: str
    source: str
    week: str
    short_title: str


DECKS = (
    Deck("week2", "CCGL9065_W2.qmd", "02", "Food futures"),
    Deck("week3", "CCGL9065_W3.qmd", "03", "Consumption & fashion"),
    Deck("week4", "CCGL9065_W4.qmd", "04", "Energy & transport"),
    Deck("week5", "CCGL9065_W5.qmd", "05", "Cities & buildings"),
    Deck("week6", "CCGL9065_W6.qmd", "06", "Economics & incentives"),
    Deck("week7", "CCGL9065_W7.qmd", "07", "Truth & manufactured doubt"),
    Deck("week8", "CCGL9065_W8.qmd", "08", "Oceans & infrastructure"),
    Deck("week9", "W9.qmd", "09", "Climate displacement"),
    Deck("week10", "W10.qmd", "10", "Systems & cascade effects"),
    Deck("week11", "CCGL9065_W11.qmd", "11", "Space & planetary futures"),
)


def pandoc_binary() -> str:
    available = shutil.which("pandoc")
    if available:
        return available

    architecture = "aarch64" if platform.machine() in {"arm64", "aarch64"} else "x86_64"
    bundled = Path("/Applications/quarto/bin/tools") / architecture / "pandoc"
    if bundled.exists():
        return str(bundled)
    raise FileNotFoundError("Pandoc was not found.")


def split_frontmatter(source: str) -> tuple[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", source, flags=re.DOTALL)
    if not match:
        return "", source
    return match.group(1), source[match.end() :]


def metadata_value(frontmatter: str, key: str, fallback: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return fallback
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value


def split_slide_stream(markdown: str, pandoc_output: bool = False) -> list[str]:
    """Split on Reveal slide headings and explicit horizontal rules."""
    slides: list[str] = []
    current: list[str] = []
    rule = re.compile(r"^-{5,}\s*$" if pandoc_output else r"^---\s*$")
    slide_heading = re.compile(r"^#{1,2}(?:\s|$)")

    def emit() -> None:
        content = "\n".join(current).strip()
        if content:
            slides.append(content)
        current.clear()

    for line in markdown.splitlines():
        if rule.match(line):
            emit()
            continue
        if slide_heading.match(line) and any(part.strip() for part in current):
            emit()
        current.append(line)
    emit()
    return slides


def source_slides(body: str) -> list[str]:
    return split_slide_stream(body)


def pandoc_slides(originals: list[str]) -> list[str]:
    markers = [
        f"<!-- CCGL_SLIDE_BREAK_{index} -->"
        for index in range(1, len(originals))
    ]
    joined_parts: list[str] = []
    for index, slide in enumerate(originals):
        if index:
            joined_parts.append(markers[index - 1])
        joined_parts.append(slide)
    joined = "\n\n".join(joined_parts)

    result = subprocess.run(
        [
            pandoc_binary(),
            "--from=markdown",
            "--to=gfm",
            "--wrap=none",
        ],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
        input=joined,
    )
    converted = re.split(
        r"<!-- CCGL_SLIDE_BREAK_\d+ -->",
        result.stdout,
    )
    return [slide.strip() for slide in converted]


def clean_title(markdown: str) -> str:
    title = re.sub(r"\{.*?\}\s*$", "", markdown).strip()
    title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
    title = re.sub(r"<[^>]+>", " ", title)
    # Pandoc escapes literal heading punctuation in GFM (for example ``\|``
    # and ``\#4``). Unescape it before normalising emphasis so section titles
    # retain meaningful text such as "Strategy #4".
    title = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|])", r"\1", title)
    title = re.sub(r"[*_`]", "", title)
    return html.unescape(re.sub(r"\s+", " ", title)).strip()


def first_source_heading(source_slide: str) -> tuple[int, str]:
    match = re.search(r"(?m)^(#{1,6})[ \t]*(.*?)[ \t]*$", source_slide)
    if not match:
        return 0, ""
    return len(match.group(1)), clean_title(match.group(2))


def unique_slug(title: str, used: set[str]) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def local_asset_url(path_text: str) -> str:
    cleaned = path_text.split("#", 1)[0].split("?", 1)[0]
    if not cleaned or cleaned.startswith(("/", "http://", "https://", "data:")):
        return path_text

    source_path = (PROJECT_ROOT / cleaned).resolve()
    try:
        relative = source_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return path_text

    if not source_path.is_file():
        print(f"warning: local asset not found: {cleaned}", file=sys.stderr)
        return path_text

    destination = ASSET_OUTPUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination)
    # The built deck lives at slides/conversion/weekN/. Keeping the media URL
    # relative to that output avoids Slidev's image preloader combining a
    # root-relative URL with the deck base and issuing a duplicate 404 request.
    return f"../../conversion-assets/{relative.as_posix()}"


def rewrite_assets(markdown: str) -> str:
    def replace_html_src(match: re.Match[str]) -> str:
        rewritten = local_asset_url(match.group(2))
        if rewritten.startswith("../../conversion-assets/"):
            prefix = re.sub(r"\bsrc=[\"']$", "", match.group(1))
            return f'{prefix}:src="\'{rewritten}\'"'
        return f"{match.group(1)}{rewritten}{match.group(3)}"

    markdown = re.sub(
        r'(<(?:img|video|source)\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])',
        replace_html_src,
        markdown,
        flags=re.IGNORECASE,
    )

    def replace_markdown_image(match: re.Match[str]) -> str:
        return f"{match.group(1)}{local_asset_url(match.group(2))}{match.group(3)}"

    return re.sub(r"(!\[[^\]]*\]\()([^) \t]+)(\))", replace_markdown_image, markdown)


def extract_background(source_slide: str) -> tuple[str | None, str | None]:
    image_match = re.search(
        r"background-image\s*=\s*(['\"])(.*?)\1",
        source_slide,
        flags=re.IGNORECASE,
    )
    color_match = re.search(
        r"background-color\s*=\s*(['\"])(.*?)\1",
        source_slide,
        flags=re.IGNORECASE,
    )
    size_match = re.search(
        r"background-size\s*=\s*(['\"])(.*?)\1",
        source_slide,
        flags=re.IGNORECASE,
    )

    if image_match:
        return local_asset_url(image_match.group(2)), (
            size_match.group(2) if size_match else "cover"
        )
    if color_match:
        return color_match.group(2), None
    return None, None


def convert_notes(markdown: str) -> str:
    pattern = re.compile(
        r'<div class="notes">\s*(.*?)\s*</div>',
        flags=re.DOTALL | re.IGNORECASE,
    )
    return pattern.sub(lambda match: f"<!--\n{match.group(1).strip()}\n-->", markdown)


def add_incremental_lists(markdown: str) -> str:
    """Wrap Markdown list blocks in Slidev's incremental reveal component."""
    lines = markdown.splitlines()
    output: list[str] = []
    list_item = re.compile(r"^ {0,3}(?:[-+*]|\d+[.)])\s+")
    index = 0
    in_comment = False
    in_fence = False

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("<!--"):
            in_comment = True
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence

        if not in_comment and not in_fence and list_item.match(line):
            block: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if list_item.match(candidate) or (
                    candidate.strip()
                    and len(candidate) - len(candidate.lstrip()) >= 2
                ):
                    block.append(candidate)
                    index += 1
                    continue

                if not candidate.strip():
                    lookahead = index + 1
                    while lookahead < len(lines) and not lines[lookahead].strip():
                        lookahead += 1
                    if lookahead < len(lines):
                        following = lines[lookahead]
                        if list_item.match(following) or (
                            len(following) - len(following.lstrip()) >= 2
                        ):
                            block.extend(lines[index:lookahead])
                            index = lookahead
                            continue
                break

            output.extend(["<v-clicks>", "", *block, "", "</v-clicks>"])
            continue

        output.append(line)
        if in_comment and "-->" in stripped:
            in_comment = False
        index += 1

    return "\n".join(output)


def extract_js_strings(source_slide: str, property_name: str) -> list[str]:
    match = re.search(
        rf"{re.escape(property_name)}\s*:\s*\[(.*?)\]",
        source_slide,
        flags=re.DOTALL,
    )
    if not match:
        return []
    values = []
    for single, double in re.findall(
        r"'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\"",
        match.group(1),
    ):
        value = single or double
        value = value.replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
        values.append(value)
    return values


def replace_interactive_slide(source_slide: str, markdown: str) -> str:
    lowered = markdown.lower()
    if "w11slider" in lowered or (
        "visualise your split" in lowered and 'type="range"' in lowered
    ):
        return "# Visualise Your Split\n\n<BudgetSplit />"

    if "groupassignment" in lowered and "start the assignment" in lowered:
        roles = extract_js_strings(source_slide, "vocations")
        role_value = html.escape("|".join(roles), quote=True)
        return (
            "# Group Assignment Time!\n\n"
            f'<GroupAssignment roles="{role_value}" />'
        )

    if "presentation countdown" in lowered and (
        "timerinterval" in lowered or "start timer" in lowered
    ):
        seconds_match = re.search(
            r"(?:countdownDuration|timeLeft)\s*=\s*(\d+)",
            source_slide,
        )
        seconds = int(seconds_match.group(1)) if seconds_match else 300
        return f'# Presentation Countdown\n\n<CountdownTimer :seconds="{seconds}" />'

    return markdown


def replace_quarto_video(source_slide: str, markdown: str) -> str:
    match = re.search(r"\{\{<\s*video\s+([^\s>]+)", source_slide)
    if not match:
        return markdown

    url = match.group(1)
    vimeo = re.match(r"https?://vimeo\.com/(\d+)", url)
    if vimeo:
        url = f"https://player.vimeo.com/video/{vimeo.group(1)}"

    iframe = (
        '<div class="converted-video">'
        f'<iframe src="{html.escape(url, quote=True)}" '
        'title="Embedded lecture video" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
        'gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
        "</div>"
    )
    shortcode = re.compile(r"(?m)^\{\{.*?\bvideo\s+.*?\}\}[ \t]*$")
    if shortcode.search(markdown):
        return shortcode.sub(iframe, markdown)

    heading = re.search(r"(?m)^#{1,2}[ \t].*$", markdown)
    if heading:
        return markdown[: heading.end()] + "\n\n" + iframe + markdown[heading.end() :]
    return iframe + "\n\n" + markdown


def normalize_first_heading(markdown: str) -> str:
    match = re.search(r"(?m)^(#{1,2})[ \t]*(.*?)[ \t]*$", markdown)
    if not match:
        return markdown.strip()

    heading_source = match.group(2)
    title = clean_title(heading_source)
    heading_link = re.fullmatch(
        r"\[([^\]]+)\]\(([^)]+)\)(?:\s+\{.*\})?",
        heading_source.strip(),
    )
    if title and heading_link:
        replacement = f"# [{title}]({heading_link.group(2)})"
    else:
        replacement = f"# {title}" if title else ""
    return (
        markdown[: match.start()]
        + replacement
        + markdown[match.end() :]
    ).strip()


def content_density(markdown: str) -> tuple[int, int]:
    visible = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"[*_`#|:\-\[\]()]", " ", visible)
    words = len(re.findall(r"\b[\w’'-]+\b", visible))
    lines = sum(1 for line in markdown.splitlines() if line.strip())
    return words, lines


def slide_zoom(markdown: str) -> float | None:
    words, lines = content_density(markdown)
    table_rows = sum(
        1 for line in markdown.splitlines() if line.lstrip().startswith("|")
    )
    inline_em_sizes = [
        float(size)
        for size in re.findall(r"font-size:\s*([0-9.]+)em", markdown)
    ]
    largest_inline_em = max(inline_em_sizes, default=1.0)
    title_match = re.search(r"(?m)^#\s+(.+?)\s*$", markdown)
    is_appendix = bool(
        title_match and title_match.group(1).strip().lower().startswith("appendix")
    )

    if words > 320 or lines > 58:
        return 0.68
    if words > 250 or lines > 46:
        return 0.76
    if words > 190 or lines > 36:
        return 0.84
    # Line counts alone understate the height of appendices, long tables, and
    # source slides that deliberately enlarge their prose. These compact
    # rules preserve the content while restoring the breathing room Reveal's
    # vertically centred layout previously supplied.
    if is_appendix and (words > 115 or lines > 25):
        return 0.84
    if words > 135 or lines > 27:
        return 0.92
    if is_appendix and lines >= 20:
        return 0.92
    if table_rows >= 12:
        return 0.92
    if largest_inline_em >= 1.3 and words > 105:
        return 0.92
    return None


def slide_frontmatter(
    source_slide: str,
    markdown: str,
    section_index: int,
    used_routes: set[str],
) -> tuple[list[str], int]:
    heading_level, source_title = first_source_heading(source_slide)
    background, background_size = extract_background(source_slide)
    fields = ["layout: default", "class: converted-slide legacy-content"]

    if heading_level == 1 and source_title:
        palette = ("cobalt-slide", "orange-slide", "green-slide", "black-slide")
        section_class = palette[section_index % len(palette)]
        fields = [
            "layout: section",
            f"class: converted-slide section-slide {section_class}",
            "level: 1",
            f"title: {yaml_string(source_title)}",
            f"routeAlias: {unique_slug(source_title, used_routes)}",
            f"menuDetail: {yaml_string('Lecture section')}",
        ]
        section_index += 1
    else:
        zoom = slide_zoom(markdown)
        if zoom:
            fields.append(f"zoom: {zoom}")

    if re.search(
        r"(?m)^#{1,2}\s+.*\{[^}]*\.smaller(?:\s|})",
        source_slide,
    ):
        fields[1] += " smaller"

    if background:
        fields.append(f"background: {yaml_string(background)}")
        if background_size:
            fields.append(f"backgroundSize: {background_size}")
        fields[1] += " background-slide"
        if background.lower() in {
            "black",
            "#000000",
            "#0a0a2e",
            "#1a1a2e",
            "#2c3e50",
            "#0a3d62",
        }:
            fields[1] += " dark-background"

    return fields, section_index


def cover_block(
    deck: Deck,
    title: str,
    subtitle: str,
) -> str:
    display_title = subtitle if subtitle else deck.short_title
    return f"""<div class="course-code">CCGL9065 · WEEK {deck.week}</div>

# {display_title}

<div class="course-place">{title}</div>

<div class="course-premise">{deck.short_title}</div>

<div class="course-welcome">Slidev conversion · original content preserved</div>"""


def global_headmatter(deck: Deck, title: str, subtitle: str) -> list[str]:
    return [
        "theme: default",
        f"title: {yaml_string(f'CCGL9065 Week {deck.week} — {deck.short_title}')}",
        'titleTemplate: "%s · CCGL9065"',
        "author: Dr Hongshan Guo",
        "colorSchema: light",
        "transition: fade-out",
        "aspectRatio: 16/9",
        "canvasWidth: 1440",
        "drawings:",
        "  persist: false",
        "mdc: true",
        "layout: cover",
        "class: course-title-slide converted-cover",
        "routeAlias: opening",
        "level: 1",
        f"menuDetail: {yaml_string(deck.short_title)}",
        f"sourceDeck: {yaml_string(deck.source)}",
        f"sourceTitle: {yaml_string(title)}",
        f"sourceSubtitle: {yaml_string(subtitle)}",
    ]


def convert_deck(deck: Deck) -> None:
    source_path = PROJECT_ROOT / deck.source
    source_text = source_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(source_text)
    title = metadata_value(
        frontmatter,
        "title",
        "CCGL9065: Our Response to Climate Change: Hong Kong 2100",
    )
    subtitle = metadata_value(frontmatter, "subtitle", deck.short_title)
    incremental = bool(
        re.search(r"(?m)^\s*incremental:\s*true\s*$", frontmatter)
    )

    originals = source_slides(body)
    converted = pandoc_slides(originals)
    if len(originals) != len(converted):
        raise RuntimeError(
            f"{deck.source}: source/Pandoc slide count differs "
            f"({len(originals)} vs {len(converted)})"
        )

    output_parts = [
        "---\n"
        + "\n".join(global_headmatter(deck, title, subtitle))
        + "\n---\n\n"
        + cover_block(deck, title, subtitle)
    ]

    used_routes = {"opening"}
    section_index = 0
    emitted = 1

    for source_slide, pandoc_slide in zip(originals, converted):
        markdown = rewrite_assets(pandoc_slide.strip())
        markdown = convert_notes(markdown)
        markdown = replace_quarto_video(source_slide, markdown)
        markdown = replace_interactive_slide(source_slide, markdown)
        markdown = normalize_first_heading(markdown)
        if incremental:
            markdown = add_incremental_lists(markdown)

        if not markdown.strip():
            continue

        fields, section_index = slide_frontmatter(
            source_slide,
            markdown,
            section_index,
            used_routes,
        )
        output_parts.append(
            "---\n" + "\n".join(fields) + "\n---\n\n" + markdown.strip()
        )
        emitted += 1

    destination = CONVERSION_DIR / f"{deck.slug}.md"
    destination.write_text("\n\n".join(output_parts) + "\n", encoding="utf-8")
    print(f"{deck.slug}: {emitted} slides from {deck.source}")


def main() -> None:
    requested = set(sys.argv[1:])
    selected = [deck for deck in DECKS if not requested or deck.slug in requested]
    unknown = requested.difference(deck.slug for deck in DECKS)
    if unknown:
        raise SystemExit(f"Unknown deck(s): {', '.join(sorted(unknown))}")

    ASSET_OUTPUT.mkdir(parents=True, exist_ok=True)
    for deck in selected:
        convert_deck(deck)


if __name__ == "__main__":
    main()
