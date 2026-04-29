#!/usr/bin/env python3
"""
Build pipeline for the CCGL9065 2026 Exhibition.

Reads:    data/2026/portfolio_master_2026.csv (canonical join, made by upstream agent)
Emits:    data/students_2026_public.json   (anonymous, numbered, no names/emails)
          data/students_2026_curator.json  (full info — names, emails, real paths)
          data/2026/thumbs/pXX.jpg         (square-ish 1200px-wide collage thumbs)
          data/2026/anon/pXX/{collage,essay}.<ext>  (anonymized media copies)

Idempotent — re-run when the master CSV changes.

Numbering: portfolio numbers (p01 .. p38) are assigned by sorted email so
they stay stable across rebuilds, even if the master CSV row order shifts.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
MASTER = REPO / "data/2026/portfolio_master_2026.csv"
PUBLIC_JSON = REPO / "data/students_2026_public.json"
CURATOR_JSON = REPO / "data/students_2026_curator.json"
THUMBS = REPO / "data/2026/thumbs"
ANON = REPO / "data/2026/anon"
VIDEOS = REPO / "data/2026/videos"

THUMB_WIDTH = 1200
THUMB_QUALITY = 82

# Per-student overrides: when a student's collage PDF has the actual collage on
# a page other than page 1, set email → 1-based page number here.
# Optionally pair with COLLAGE_CROP_TOP_FRAC to trim a header band from the top.
COLLAGE_PAGE_OVERRIDES: dict[str, int] = {
    "u3659408@connect.hku.hk": 6,  # Hong Kiu Jamie Lee — collage is on the last page
}

# Fraction of the rendered page height to crop off the TOP after page extraction.
# Used when the page contains a small text header above the actual collage image.
COLLAGE_CROP_TOP_FRAC: dict[str, float] = {
    "u3659408@connect.hku.hk": 0.13,  # remove "Video Essay / Link: ... / Collage" header
}


def classify_collage(row: dict) -> str:
    p = row["collage_best_link_or_path"] or ""
    if not p:
        return "none"
    if p.startswith("https://i.ibb.co"):
        return "ibb_direct"
    if p.startswith("https://ibb.co"):
        return "ibb_page"
    if "canva.com" in p:
        return "canva"
    if "drive.google.com" in p:
        return "drive"
    if p.lower().endswith(".pdf"):
        return "local_pdf"
    if p.lower().endswith((".png", ".jpg", ".jpeg")):
        return "local_image"
    return "other"


def classify_video(row: dict) -> str:
    p = row["video_best_link_or_path"] or ""
    if not p:
        return "none"
    if "youtube.com/embed" in p:
        return "youtube"
    if p.lower().endswith((".mp4", ".mov", ".m4v", ".webm")):
        return "local"
    return "other"


def fetch_canva_thumbnail_url(view_url: str) -> str | None:
    """Pull the document-export S3 signed URL out of a Canva /view page."""
    # Strip ?embed and ensure /view (not /view?embed)
    page_url = view_url.split("?")[0].rstrip("/")
    if not page_url.endswith("/view"):
        page_url = page_url + "/view"
    try:
        req = urllib.request.Request(
            page_url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read(2_000_000).decode("utf-8", errors="replace")
        m = re.search(r'https?://[^"]*document-export\.canva\.com[^"]*0001\.png[^"]*', html)
        return m.group(0) if m else None
    except Exception as e:
        print(f"  ! Canva fetch failed: {e}", file=sys.stderr)
        return None


def drive_thumbnail_url(share_url: str, width: int = 1600) -> str | None:
    """Convert a /file/d/<id>/view URL into the public thumbnail endpoint."""
    m = re.search(r"/file/d/([^/]+)", share_url)
    if not m:
        return None
    return f"https://drive.google.com/thumbnail?id={m.group(1)}&sz=w{width}"


def fetch_og_image(page_url: str) -> str | None:
    """Resolve an ibb.co page link to its og:image URL. Best effort, returns None on any failure."""
    try:
        req = urllib.request.Request(
            page_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ccgl9065-builder)"},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read(200_000).decode("utf-8", errors="replace")
        m = re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
            html,
            re.IGNORECASE,
        )
        return m.group(1) if m else None
    except Exception as e:
        print(f"  ! OG fetch failed for {page_url}: {e}", file=sys.stderr)
        return None


def download_to_anon(image_url: str, out_path: Path) -> bool:
    """Download a remote image and resize to thumbnail width via sips."""
    if out_path.exists():
        return True
    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path = out_path.with_suffix(".raw")
    try:
        req = urllib.request.Request(
            image_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ccgl9065-builder)"},
        )
        with urllib.request.urlopen(req, timeout=20) as r, raw_path.open("wb") as f:
            shutil.copyfileobj(r, f)
        if raw_path.stat().st_size < 1024:
            raw_path.unlink(missing_ok=True)
            return False
        # sips will overwrite raw_path in place if --out is the same; use a new file.
        if not resize_image(raw_path, out_path):
            # If sips fails, fall back to renaming the raw bytes (still anonymized URL).
            raw_path.rename(out_path)
        else:
            raw_path.unlink(missing_ok=True)
        return out_path.exists()
    except Exception as e:
        print(f"  ! download failed for {image_url}: {e}", file=sys.stderr)
        raw_path.unlink(missing_ok=True)
        return False


_URL_RE = re.compile(r"https?\S*|www\.\S*|\S*\.(?:com|so|be|org|net|edu|gov|hk|co)\S*", re.IGNORECASE)

_NOISE_RE = re.compile(
    r"\b(?:ccgl\s*\d{0,5}|ccgl9?0?59?|"  # course codes (incl. typo CCGL9059)
    r"final|portfolio|reflection|reflective|"
    r"essay|paper|video|collage|poster|image\s*link|submission|embed(?:ded)?|"
    r"link|links|copy|revised|file|pdf|png|jpe?g|youtube|youtu|"
    r"notion|canva|drive|google|on|of|in|the|a|an|"  # platform names + common stopwords
    r"3036\d{6}|u3\d{6}|"                # HKU UIDs
    r"\d{7,12}"                           # other long numeric ids
    r")\b",
    re.IGNORECASE,
)

_GIBBERISH_RE = re.compile(
    r"(?:[A-Za-z]{2,}\d|\d[A-Za-z]{2,}|[A-Za-z]{15,})"  # mixed alnum or super-long word → likely a video id
)


def name_tokens(row: dict) -> list[str]:
    """Every token of every name plus full forms — for greedy stripping."""
    bag = set()
    for field in ("student_name", "first_name", "last_name"):
        v = (row.get(field) or "").strip()
        if v:
            bag.add(v)
            for t in re.split(r"[\s_\-]+", v):
                if len(t) >= 2:
                    bag.add(t)
    for field in ("student_number", "turnitin_user_id"):
        v = (row.get(field) or "").strip()
        if v:
            bag.add(v)
    return sorted(bag, key=len, reverse=True)  # longest first so we don't half-match


def clean_title(raw: str, tokens: list[str]) -> str:
    if not raw:
        return ""
    # Step 1: kill obvious URL fragments before separators get normalized.
    t = _URL_RE.sub(" ", raw)
    # Step 2: normalize separators so word boundaries actually work.
    t = re.sub(r"[_\-]+", " ", t)
    # Step 3: strip name tokens as substrings (handles cases like "MatthewSitu").
    for tok in tokens:
        if len(tok) >= 3:
            t = re.sub(re.escape(tok), " ", t, flags=re.IGNORECASE)
    # Step 4: strip noise words.
    t = _NOISE_RE.sub(" ", t)
    # Step 5: drop standalone numeric groups and gibberish runs.
    words = [w for w in t.split()
             if not w.isdigit()
             and not _GIBBERISH_RE.fullmatch(w)
             and len(w) >= 2]
    t = " ".join(words)
    t = re.sub(r"[^\w\s,.&'?!:’–—]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s{2,}", " ", t).strip(" -_:,.")
    return t


def pick_anon_title(row: dict, pid: str) -> str:
    tokens = name_tokens(row)
    candidates: list[str] = []
    for raw in (row["essay_title"], row["collage_title"], row["video_title"]):
        c = clean_title((raw or "").strip(), tokens)
        if not c or len(c) < 8:
            continue
        if len(c.split()) < 2:
            continue
        if re.fullmatch(r"[\W\d\s]+", c):
            continue
        # Reject if more than 30% of chars are digits (e.g., "3036059899 Ccgl")
        digit_ratio = sum(ch.isdigit() for ch in c) / max(len(c), 1)
        if digit_ratio > 0.20:
            continue
        candidates.append(c)
    fallback = f"Portfolio {pid.upper()}"
    if not candidates:
        return fallback
    # Pick the candidate with the most meaningful words (each ≥3 chars).
    def score(c: str) -> tuple[int, int]:
        meaningful = [w for w in c.split() if len(w) >= 3 and not w.isdigit()]
        return (len(meaningful), len(c))
    best = max(candidates, key=score)[:64].rstrip(" ,.-_:")
    if best.islower() or best.isupper():
        best = best.title()
    return best


def render_pdf_page(pdf: Path, out_jpg: Path, page: int = 1, width: int = THUMB_WIDTH) -> bool:
    """pdftoppm one specific page (1-based) → JPG. Returns True on success."""
    if out_jpg.exists():
        return True
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    stem = out_jpg.with_suffix("")
    cmd = [
        "pdftoppm", "-jpeg", "-jpegopt", f"quality={THUMB_QUALITY}",
        "-f", str(page), "-l", str(page),
        "-scale-to-x", str(width), "-scale-to-y", "-1",
        str(pdf), str(stem),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"  ! pdftoppm failed: {e.stderr.decode()[:200]}", file=sys.stderr)
        return False
    # pdftoppm names the output as stem-{page}.jpg (zero-padded for multi-digit page counts).
    for candidate in (
        stem.with_name(f"{stem.name}-{page}.jpg"),
        stem.with_name(f"{stem.name}-{page:02d}.jpg"),
        stem.with_suffix(".jpg"),
    ):
        if candidate.exists():
            if candidate != out_jpg:
                candidate.rename(out_jpg)
            return True
    return False


def render_pdf_first_page(pdf: Path, out_jpg: Path) -> bool:
    return render_pdf_page(pdf, out_jpg, page=1)


def crop_top_fraction(jpg: Path, frac: float) -> bool:
    """Crop the top `frac` of the image height (in place)."""
    if frac <= 0:
        return True
    try:
        from PIL import Image
    except ImportError:
        return False
    try:
        im = Image.open(jpg).convert("RGB")
        w, h = im.size
        top = int(h * frac)
        im.crop((0, top, w, h)).save(jpg, "JPEG", quality=THUMB_QUALITY)
        return True
    except Exception as e:
        print(f"  ! top-crop failed for {jpg}: {e}", file=sys.stderr)
        return False


def trim_whitespace(jpg: Path, threshold: int = 240) -> bool:
    """Crop near-white borders from a JPG in place. Returns True on success."""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return False
    try:
        im = Image.open(jpg).convert("RGB")
        # Build a mask of non-white pixels.
        bg = Image.new("RGB", im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg)
        # Threshold: anything brighter than (255-threshold) per channel counts as background.
        bbox = diff.point(lambda p: 255 if p > (255 - threshold) else 0).getbbox()
        if not bbox:
            return False
        # Add a small margin so we don't shave the actual content.
        margin = 8
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0 - margin); y0 = max(0, y0 - margin)
        x1 = min(im.size[0], x1 + margin); y1 = min(im.size[1], y1 + margin)
        im.crop((x0, y0, x1, y1)).save(jpg, "JPEG", quality=THUMB_QUALITY)
        return True
    except Exception as e:
        print(f"  ! trim failed for {jpg}: {e}", file=sys.stderr)
        return False


def resize_image(src: Path, out_jpg: Path) -> bool:
    """Resize via sips (macOS native, no PIL dep needed at runtime)."""
    if out_jpg.exists():
        return True
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["sips", "-Z", str(THUMB_WIDTH), "-s", "format", "jpeg",
           "-s", "formatOptions", str(THUMB_QUALITY),
           str(src), "--out", str(out_jpg)]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return out_jpg.exists()
    except subprocess.CalledProcessError as e:
        print(f"  ! sips failed: {e.stderr.decode()[:200]}", file=sys.stderr)
        return False


def copy_to_anon(src: Path, dst: Path) -> None:
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def encode_video(src: Path, dst_mp4: Path) -> bool:
    """ffmpeg re-encode to web-friendly 720p H.264. Skips if dst exists."""
    if dst_mp4.exists():
        return True
    dst_mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-vf", "scale='min(1280,iw)':-2",
        "-c:v", "libx264", "-preset", "medium", "-crf", "24",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(dst_mp4),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ! ffmpeg failed for {src.name}: {e.stderr.decode()[:300]}", file=sys.stderr)
        return False


def main() -> int:
    if not MASTER.exists():
        print(f"Master CSV not found: {MASTER}", file=sys.stderr)
        return 1

    THUMBS.mkdir(parents=True, exist_ok=True)
    ANON.mkdir(parents=True, exist_ok=True)
    VIDEOS.mkdir(parents=True, exist_ok=True)

    with MASTER.open() as f:
        rows = list(csv.DictReader(f))

    # Stable numbering: sort by email
    rows.sort(key=lambda r: (r["email"].lower(), r["student_number"]))

    public_records: list[dict[str, Any]] = []
    curator_records: list[dict[str, Any]] = []

    for i, r in enumerate(rows, start=1):
        pid = f"p{i:02d}"
        coll_kind = classify_collage(r)
        vid_kind = classify_video(r)

        anon_dir = ANON / pid

        # ------ Collage ------
        thumb_url: str | None = None
        full_collage_url: str | None = None
        collage_meta: dict[str, Any] = {"kind": coll_kind}

        c_src = r["collage_best_link_or_path"]

        if coll_kind == "ibb_direct":
            # Download locally so the URL doesn't leak student names in the filename.
            anon_img = anon_dir / "collage.jpg"
            thumb_jpg = THUMBS / f"{pid}.jpg"
            if download_to_anon(c_src, anon_img):
                full_collage_url = f"data/2026/anon/{pid}/collage.jpg"
                # Reuse the anon copy as the thumb (already resized).
                if not thumb_jpg.exists():
                    shutil.copy2(anon_img, thumb_jpg)
                thumb_url = f"data/2026/thumbs/{pid}.jpg"
                collage_meta["mirrored_from_ibb"] = True
            else:
                # Fallback: hotlink (degraded anonymity, but better than no image).
                thumb_url = c_src
                full_collage_url = c_src
                collage_meta["mirror_failed"] = True
        elif coll_kind == "ibb_page":
            resolved = fetch_og_image(c_src)
            if resolved:
                anon_img = anon_dir / "collage.jpg"
                thumb_jpg = THUMBS / f"{pid}.jpg"
                if download_to_anon(resolved, anon_img):
                    full_collage_url = f"data/2026/anon/{pid}/collage.jpg"
                    if not thumb_jpg.exists():
                        shutil.copy2(anon_img, thumb_jpg)
                    thumb_url = f"data/2026/thumbs/{pid}.jpg"
                    collage_meta["mirrored_from_ibb_page"] = c_src
                else:
                    thumb_url = resolved
                    full_collage_url = resolved
                    collage_meta["resolved_from_page"] = c_src
            else:
                full_collage_url = c_src
                collage_meta["unresolved_page"] = True
        elif coll_kind == "local_pdf":
            src_pdf = REPO / c_src
            override_page = COLLAGE_PAGE_OVERRIDES.get(r["email"].lower().strip())
            if override_page:
                # The actual collage is on a non-first page → render it as a JPG and
                # promote the record to local_image so the modal shows the picture
                # directly instead of the cover-page PDF.
                anon_jpg = anon_dir / "collage.jpg"
                thumb_jpg = THUMBS / f"{pid}.jpg"
                # Render full-resolution to anon path, then copy + downscale to thumb.
                anon_jpg.unlink(missing_ok=True)
                if render_pdf_page(src_pdf, anon_jpg, page=override_page, width=2000):
                    crop_frac = COLLAGE_CROP_TOP_FRAC.get(r["email"].lower().strip(), 0.0)
                    if crop_frac:
                        crop_top_fraction(anon_jpg, crop_frac)
                    trim_whitespace(anon_jpg)
                    full_collage_url = f"data/2026/anon/{pid}/collage.jpg"
                    collage_meta["kind"] = "local_image"
                    collage_meta["pdf_page_override"] = override_page
                    coll_kind = "local_image"  # so renderer treats it as image
                    thumb_jpg.unlink(missing_ok=True)
                    if resize_image(anon_jpg, thumb_jpg):
                        thumb_url = f"data/2026/thumbs/{pid}.jpg"
                else:
                    # Fallback to default behaviour
                    anon_pdf = anon_dir / "collage.pdf"
                    copy_to_anon(src_pdf, anon_pdf)
                    if render_pdf_first_page(src_pdf, thumb_jpg):
                        thumb_url = f"data/2026/thumbs/{pid}.jpg"
                    full_collage_url = f"data/2026/anon/{pid}/collage.pdf"
            else:
                anon_pdf = anon_dir / "collage.pdf"
                copy_to_anon(src_pdf, anon_pdf)
                thumb_jpg = THUMBS / f"{pid}.jpg"
                if render_pdf_first_page(src_pdf, thumb_jpg):
                    thumb_url = f"data/2026/thumbs/{pid}.jpg"
                full_collage_url = f"data/2026/anon/{pid}/collage.pdf"
        elif coll_kind == "local_image":
            src_img = REPO / c_src
            ext = src_img.suffix.lower().lstrip(".")
            if ext == "jpeg":
                ext = "jpg"
            anon_img = anon_dir / f"collage.{ext}"
            copy_to_anon(src_img, anon_img)
            thumb_jpg = THUMBS / f"{pid}.jpg"
            if resize_image(src_img, thumb_jpg):
                thumb_url = f"data/2026/thumbs/{pid}.jpg"
            full_collage_url = f"data/2026/anon/{pid}/collage.{ext}"
        elif coll_kind == "canva":
            full_collage_url = c_src  # iframe src for the modal stays the embed URL
            preview_url = fetch_canva_thumbnail_url(c_src)
            if preview_url:
                anon_img = anon_dir / "collage.jpg"
                thumb_jpg = THUMBS / f"{pid}.jpg"
                if download_to_anon(preview_url, anon_img):
                    if not thumb_jpg.exists():
                        shutil.copy2(anon_img, thumb_jpg)
                    thumb_url = f"data/2026/thumbs/{pid}.jpg"
                    collage_meta["preview_from_canva"] = True
        elif coll_kind == "drive":
            full_collage_url = c_src
            preview_url = drive_thumbnail_url(c_src)
            if preview_url:
                anon_img = anon_dir / "collage.jpg"
                thumb_jpg = THUMBS / f"{pid}.jpg"
                if download_to_anon(preview_url, anon_img):
                    if not thumb_jpg.exists():
                        shutil.copy2(anon_img, thumb_jpg)
                    thumb_url = f"data/2026/thumbs/{pid}.jpg"
                    collage_meta["preview_from_drive"] = True
        # else: "none" → no collage

        # ------ Video ------
        v_src = r["video_best_link_or_path"]
        video_meta: dict[str, Any] = {"kind": vid_kind}
        full_video_url: str | None = None

        if vid_kind == "youtube":
            full_video_url = v_src
        elif vid_kind == "local":
            src_vid = REPO / v_src
            anon_mp4 = VIDEOS / f"{pid}.mp4"
            if encode_video(src_vid, anon_mp4):
                full_video_url = f"data/2026/videos/{pid}.mp4"
            else:
                # Fallback: copy as-is so something plays
                fallback = anon_dir / f"video{src_vid.suffix.lower()}"
                copy_to_anon(src_vid, fallback)
                full_video_url = f"data/2026/anon/{pid}/{fallback.name}"

        # ------ Essay ------
        essay_url: str | None = None
        essay_path = r["essay_pdf_path"]
        if essay_path:
            src_pdf = REPO / essay_path
            if src_pdf.exists():
                anon_essay = anon_dir / "essay.pdf"
                copy_to_anon(src_pdf, anon_essay)
                essay_url = f"data/2026/anon/{pid}/essay.pdf"

        # ------ Title selection (anonymous label) ------
        last = r["last_name"].strip()
        first = r["first_name"].strip()
        anon_title = pick_anon_title(r, pid)

        public_records.append({
            "id": pid,
            "title": anon_title,
            "thumb": thumb_url,
            "collage": {"url": full_collage_url, **collage_meta},
            "video": {"url": full_video_url, **video_meta},
            "essay": {"url": essay_url, "available": bool(essay_url)},
        })

        curator_records.append({
            "id": pid,
            "name": r["student_name"],
            "first_name": first,
            "last_name": last,
            "email": r["email"],
            "student_number": r["student_number"],
            "anon_title": anon_title,
            "essay_title": r["essay_title"],
            "collage_title": r["collage_title"],
            "video_title": r["video_title"],
            "thumb": thumb_url,
            "collage": {
                "url": full_collage_url,
                "kind": coll_kind,
                "source_path": r["collage_source_path"],
                "original_link": c_src,
            },
            "video": {
                "url": full_video_url,
                "kind": vid_kind,
                "source_path": r["video_source_path"],
                "original_link": v_src,
            },
            "essay": {
                "url": essay_url,
                "available": bool(essay_url),
                "source_path": r["essay_source_path"],
                "converted_from_docx": r["essay_converted_from_docx"] in ("true", "True", "1"),
            },
        })

    # Public JSON: shuffle order doesn't matter for cycling but we keep stable order.
    PUBLIC_JSON.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_JSON.write_text(json.dumps({
        "generated_at": "build_2026.py",
        "count": len(public_records),
        "portfolios": public_records,
    }, indent=2, ensure_ascii=False))

    CURATOR_JSON.write_text(json.dumps({
        "generated_at": "build_2026.py",
        "count": len(curator_records),
        "portfolios": curator_records,
    }, indent=2, ensure_ascii=False))

    print(f"\nWrote {PUBLIC_JSON.relative_to(REPO)} ({len(public_records)} entries)")
    print(f"Wrote {CURATOR_JSON.relative_to(REPO)} ({len(curator_records)} entries)")
    # Coverage summary
    coll_with_thumb = sum(1 for p in public_records if p["thumb"])
    has_video = sum(1 for p in public_records if p["video"]["url"])
    has_essay = sum(1 for p in public_records if p["essay"]["available"])
    print(f"Coverage: thumbs={coll_with_thumb}/{len(public_records)}  "
          f"videos={has_video}  essays={has_essay}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
