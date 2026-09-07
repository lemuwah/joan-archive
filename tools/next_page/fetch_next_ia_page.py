#!/usr/bin/env python3
"""
fetch_next_ia_page.py — chase the next page image in an Internet Archive volume.

Track A of the two-track "next image in the chain" tooling (see tools/next_page/README.md).
Covers public-domain printed volumes already hosted on archive.org — the majority of this
archive's primary sources (Bartlett's Colonial Records, Arnold's Records of the Colony,
Potter's Early History, RIHS Collections, etc. — see sources.yml).

Does NOT cover FamilySearch manuscript/microfilm images (the 008204949-* deed book scans).
See tools/next_page/familysearch_manual_track.md for why, and what to do instead.

What it does, per volume in sources.yml with a non-null last_known_seq:
  1. Fetch the IIIF Presentation manifest for the identifier.
  2. Look up leaf index (last_known_seq + 1).
  3. If that leaf exists, download the full-resolution image via its IIIF Image API URL
     into images/_pending_review/ (never directly into images/ — a human or a follow-up
     AI transcription pass promotes it after review, same as the existing workflow for
     uploaded manuscript images).
  4. If that leaf does NOT exist, treat it as "no more pages" — log it as such rather than
     erroring. Per the archive owner's own framing: if an image can't be found, it's either
     not digitized/accessible, or it doesn't exist. Either way, that's a result worth logging,
     not a failure to hide.
  5. Append one line to research_queue/next_page_fetch_log.md either way, so this behaves
     like every other search in the archive: logged whether it found something or not
     (Law 7 / NEGATIVE_LOG conventions).

Does NOT commit anything to git and does NOT touch sources.yml's last_known_seq automatically —
that update is left to the human/PR-reviewer step (see the GitHub Action), so a bad fetch can't
silently ratchet the registry forward.

Usage:
    python fetch_next_ia_page.py                  # process every volume with a non-null last_known_seq
    python fetch_next_ia_page.py --id earlyhistoryofna00pott   # process one volume only
"""

import argparse
import datetime
import pathlib
import sys

import requests
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCES_FILE = REPO_ROOT / "tools" / "next_page" / "sources.yml"
PENDING_DIR = REPO_ROOT / "images" / "_pending_review"
LOG_FILE = REPO_ROOT / "research_queue" / "next_page_fetch_log.md"

IIIF_MANIFEST_URL = "https://iiif.archive.org/iiif/{id}/manifest.json"


def load_sources():
    with open(SOURCES_FILE) as f:
        data = yaml.safe_load(f)
    return data["volumes"]


def get_manifest_canvases(identifier: str):
    """Return the ordered list of IIIF canvases for a volume. Raises on network/format errors."""
    resp = requests.get(IIIF_MANIFEST_URL.format(id=identifier), timeout=30)
    resp.raise_for_status()
    manifest = resp.json()
    # IIIF Presentation API v2 shape (what archive.org has historically served).
    if "sequences" in manifest:
        return manifest["sequences"][0]["canvases"]
    # v3 shape, in case IA has migrated by the time this runs.
    if "items" in manifest:
        return manifest["items"]
    raise ValueError(f"Unrecognized IIIF manifest shape for {identifier} — check by hand.")


def canvas_image_url(canvas: dict) -> str:
    """Extract a full-resolution image URL from a v2-or-v3-shaped IIIF canvas."""
    try:
        # v2
        return canvas["images"][0]["resource"]["@id"]
    except (KeyError, IndexError):
        pass
    try:
        # v3
        body = canvas["items"][0]["items"][0]["body"]
        return body["id"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Could not find an image URL in canvas: {canvas.get('label')}") from e


def log_result(line: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    is_new = not LOG_FILE.exists()
    with open(LOG_FILE, "a") as f:
        if is_new:
            f.write(
                "# Next-Page Fetch Log\n\n"
                "Automated log from `tools/next_page/fetch_next_ia_page.py`. "
                "One line per attempt, found or not — do not delete lines for failed attempts, "
                "a logged negative is still evidence (see methodology/editorial_standards.md, Law 7).\n\n"
                "| Date | Volume ID | Leaf attempted | Result |\n"
                "|---|---|---|---|\n"
            )
        f.write(line + "\n")


def process_volume(vol: dict) -> None:
    identifier = vol["id"]
    label = vol.get("label", identifier)
    last_seq = vol.get("last_known_seq")
    date = datetime.date.today().isoformat()

    if last_seq is None:
        print(f"[skip] {identifier}: last_known_seq is null in sources.yml — fill it in first.")
        return

    next_seq = last_seq + 1
    print(f"[check] {identifier} ({label}): looking for leaf {next_seq}")

    try:
        canvases = get_manifest_canvases(identifier)
    except Exception as e:
        print(f"[error] {identifier}: could not load manifest — {e}")
        log_result(f"| {date} | {identifier} | {next_seq} | ERROR fetching manifest: {e} |")
        return

    if next_seq >= len(canvases):
        print(f"[end] {identifier}: no leaf {next_seq} — volume has {len(canvases)} leaves. "
              f"Either the end of the volume, or not digitized further.")
        log_result(
            f"| {date} | {identifier} | {next_seq} | NOT FOUND — volume only has "
            f"{len(canvases)} leaves (0-indexed). Likely end of digitized volume. |"
        )
        return

    canvas = canvases[next_seq]
    try:
        image_url = canvas_image_url(canvas)
    except Exception as e:
        print(f"[error] {identifier}: {e}")
        log_result(f"| {date} | {identifier} | {next_seq} | ERROR reading canvas: {e} |")
        return

    # Request full resolution via the IIIF Image API.
    if not image_url.endswith("/full/full/0/default.jpg"):
        image_url = image_url.rstrip("/") + "/full/full/0/default.jpg"

    try:
        img_resp = requests.get(image_url, timeout=60)
        img_resp.raise_for_status()
    except Exception as e:
        print(f"[error] {identifier}: image download failed — {e}")
        log_result(f"| {date} | {identifier} | {next_seq} | ERROR downloading image: {e} |")
        return

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PENDING_DIR / f"{identifier}_leaf{next_seq:04d}.jpg"
    out_path.write_bytes(img_resp.content)
    print(f"[saved] {out_path.relative_to(REPO_ROOT)}")
    log_result(
        f"| {date} | {identifier} | {next_seq} | FOUND — saved to "
        f"`images/_pending_review/{out_path.name}`. Needs human/AI review before promotion "
        f"to images/ with a descriptive name and a Search Log entry. |"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Process only this volume identifier.")
    args = parser.parse_args()

    volumes = load_sources()
    if args.id:
        volumes = [v for v in volumes if v["id"] == args.id]
        if not volumes:
            print(f"'{args.id}' not found in sources.yml — add it there first.")
            sys.exit(1)

    for vol in volumes:
        process_volume(vol)


if __name__ == "__main__":
    main()
