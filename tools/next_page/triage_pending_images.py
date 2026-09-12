#!/usr/bin/env python3
"""
triage_pending_images.py — cheap first-pass relevance check on images/_pending_review/*.

Not a substitute for a human decision, and not a citation — this only decides what order
a human should look at pending images in, and drafts a starting-point transcription they
can correct. Every output it produces is tagged AI-SOURCED per
methodology/editorial_standards.md and theory/three_laws.md Law 7 — never PROOF on its own.

Requires an ANTHROPIC_API_KEY (repo secret in CI; env var locally). Uses vision-capable
Claude to describe each pending image and flag whether it plausibly mentions any of the
archive's core search terms. Writes one .md sidecar per image, same folder, for the human
reviewer — it does not touch /people/ or any published page.

Usage:
    export ANTHROPIC_API_KEY=...
    python triage_pending_images.py
"""

import base64
import json
import pathlib

import requests

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PENDING_DIR = REPO_ROOT / "images" / "_pending_review"

SEARCH_TERMS = [
    "Greene", "Green", "Joan", "Joane", "Quidnessett", "Quidnesset",
    "Fones", "Anashuecot", "Absolom", "Tibbetts", "Tibbits", "Warwick",
    "Occupasuetuxet", "Narragansett", "Kingstown", "Potowomut",
]

PROMPT = (
    "You are looking at a scanned page from a 17th/18th-century Rhode Island colonial "
    "records or genealogy volume. Transcribe as much legible text as you reasonably can — "
    "this is a rough working read, not a paleographic verification, so mark unclear words "
    "with [?]. Then, separately, list which of these terms (or close phonetic/spelling "
    "variants) appear to be present: " + ", ".join(SEARCH_TERMS) + ". "
    "Respond as JSON only: {\"rough_transcription\": \"...\", \"terms_found\": [...], "
    "\"confidence_note\": \"one short sentence on how legible/reliable this read is\"}."
)


def triage_one(image_path: pathlib.Path) -> dict:
    image_b64 = base64.b64encode(image_path.read_bytes()).decode()
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": __import__("os").environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1500,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                    {"type": "text", "text": PROMPT},
                ],
            }],
        },
        timeout=90,
    )
    resp.raise_for_status()
    text = "".join(b["text"] for b in resp.json()["content"] if b["type"] == "text")
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(text)


def main():
    images = sorted(PENDING_DIR.glob("*.jpg")) + sorted(PENDING_DIR.glob("*.JPG"))
    if not images:
        print("Nothing in images/_pending_review/ to triage.")
        return

    for img in images:
        sidecar = img.with_suffix(".triage.md")
        if sidecar.exists():
            continue  # already triaged
        print(f"[triage] {img.name}")
        try:
            result = triage_one(img)
        except Exception as e:
            print(f"  error: {e}")
            continue

        found = result.get("terms_found", [])
        flag = "LIKELY RELEVANT" if found else "NO OBVIOUS MATCH — still needs a human look, this is a weak filter"
        sidecar.write_text(
            f"# Triage — {img.name}\n\n"
            f"⚠️ AI-SOURCED — AI TRANSCRIPTION per Law 7. Working read only, not a "
            f"paleographic verification. Verify against the original before citing.\n\n"
            f"**Flag:** {flag}\n"
            f"**Terms matched:** {', '.join(found) if found else 'none'}\n"
            f"**Confidence note:** {result.get('confidence_note', '')}\n\n"
            f"## Rough transcription\n\n{result.get('rough_transcription', '')}\n"
        )
        print(f"  -> {sidecar.name} ({flag})")


if __name__ == "__main__":
    main()
