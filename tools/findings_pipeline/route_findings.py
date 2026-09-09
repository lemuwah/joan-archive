#!/usr/bin/env python3
"""Route research findings through the ordered, review-only agent queue."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FINDINGS = ROOT / "research_findings"
PENDING_IMAGES = ROOT / "images" / "_pending_review"
QUEUE = ROOT / "research_queue" / "finding_runs"
STAGES = (
    ("01_archivist", "Archivist", "establish provenance, stable identifiers, page/image anchors, and checksum needs"),
    ("02_hostile_review", "Hostile Review", "attack identity collisions, circular citations, OCR error, and unsupported inference"),
    ("03_synthesizer", "Synthesizer", "propose bounded claims while preserving contradictions and status tags"),
    ("04_explorer", "Explorer", "expand sideways context and identify where evidence may be hiding in plain sight"),
)


def slug(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")


def image_refs(text: str) -> list[str]:
    refs = set(re.findall(r"(?:images/|images\\/)([^\s)`\"']+\.(?:jpg|jpeg|png|gif|webp))", text, re.IGNORECASE))
    return sorted(refs)


def finding_record(path: Path, run_date: str) -> dict:
    text = path.read_text()
    relative = path.relative_to(ROOT).as_posix()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    refs = image_refs(text)
    pending = [name for name in refs if (PENDING_IMAGES / name).exists()]
    not_pending = [name for name in refs if name not in pending and (ROOT / "images" / name).exists()]
    missing = [name for name in refs if not (PENDING_IMAGES / name).exists() and not (ROOT / "images" / name).exists()]
    return {
        "finding_id": f"FINDING-{hashlib.sha256(f'{relative}:{digest}'.encode()).hexdigest()[:12]}",
        "source_path": relative,
        "source_sha256": digest,
        "run_date": run_date,
        "status": "PENDING_HUMAN_REVIEW",
        "image_references": refs,
        "pending_review_images": pending,
        "images_not_pending": not_pending,
        "missing_image_references": missing,
    }


def stage_text(record: dict, stage: tuple[str, str, str], finding_text: str) -> str:
    directory, title, purpose = stage
    image_note = ", ".join(record["image_references"]) if record["image_references"] else "none detected"
    lines = [
        f"# {title} Queue Packet — {record['source_path']}",
        "",
        f"**Finding ID:** `{record['finding_id']}`",
        f"**Status:** `{record['status']}`",
        f"**Source SHA-256:** `{record['source_sha256']}`",
        f"**Stage purpose:** {purpose}.",
        "**Publication rule:** This is a review packet, not evidence and not an approval.",
        "",
        "## Required action",
        f"Process this finding as stage `{directory}`. Preserve the exact source path and hash.",
        "Do not edit the source finding or promote any claim to PROOF.",
        "",
        "## Image gate",
        f"Referenced images: {image_note}.",
        f"Images already staged in `images/_pending_review/`: {', '.join(record['pending_review_images']) or 'none'}.",
        f"Referenced images already elsewhere in `images/` and not pending: {', '.join(record['images_not_pending']) or 'none'}.",
        f"Referenced images not found in the archive: {', '.join(record['missing_image_references']) or 'none'}.",
        "Any newly supplied image belongs in `images/_pending_review/` until a human reviews and promotes it.",
        "",
        "## Finding text",
        "```markdown",
        finding_text.rstrip(),
        "```",
        "",
        "## Required output",
        "Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.",
    ]
    if title == "Explorer":
        lines.extend([
            "",
            "## Required sideways-context checklist",
            "- Map household people, witnesses, neighbors, in-laws, buyers, sellers, and officials.",
            "- Expand across land, probate, court, church, militia, servant, captivity, shipping, and Indigenous-centered records.",
            "- Test Rhode Island, Massachusetts, Connecticut, Plymouth, New York, Crown, port, and local town repositories.",
            "- Search spelling variants and relationship descriptions, not only the target person's name.",
            "- For each proposed edge, state the source anchor that would prove it and the record that would disprove it.",
        ])
    lines.append("")
    return "\n".join(lines)


def route(run_date: str, check: bool) -> int:
    findings = sorted(path for path in FINDINGS.glob("*.md") if path.name != "README.md")
    output = QUEUE / run_date
    expected: dict[str, str] = {}
    for finding in findings:
        record = finding_record(finding, run_date)
        packet_dir = output / slug(finding)
        expected[str(packet_dir.relative_to(ROOT) / "run_manifest.json")] = json.dumps(record, indent=2, sort_keys=True) + "\n"
        text = finding.read_text()
        for stage in STAGES:
            expected[str((packet_dir / f"{stage[0]}.md").relative_to(ROOT))] = stage_text(record, stage, text)

    if check:
        stale = []
        for relative, content in expected.items():
            path = ROOT / relative
            if not path.exists() or path.read_text() != content:
                stale.append(relative)
        if stale:
            print("Finding queue is stale; run route_findings.py.\n- " + "\n- ".join(stale))
            return 1
    else:
        for relative, content in expected.items():
            path = ROOT / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print(f"Findings routed: {len(findings)}")
    print(f"Ordered stages per finding: {len(STAGES)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return route(args.date, args.check)


if __name__ == "__main__":
    raise SystemExit(main())