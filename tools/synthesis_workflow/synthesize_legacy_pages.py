#!/usr/bin/env python3
"""Snapshot legacy people pages and create review-only synthesis proposals.

This tool preserves page history by content hash. It never edits source pages,
promotes claims, or writes to public-facing files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "people"
OBSERVATIONS = ROOT / "data/research/legacy_observations.jsonl"
PROPOSALS = ROOT / "data/research/synthesis_proposals.jsonl"
STATUS_TAGS = ("PROOF", "PLAUSIBLE", "DISCREDITED", "SUSPENDED", "UNVERIFIED", "UNKNOWN")


def load_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    records = {}
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {error.msg}") from error
        key = record.get("observation_id") or record.get("proposal_id")
        if not key:
            raise ValueError(f"{path}:{line_number}: missing record ID")
        records[key] = record
    return records


def write_jsonl(path: Path, records: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(json.dumps(records[item], ensure_ascii=True, sort_keys=True) + "\n" for item in sorted(records))
    path.write_text(content)


def page_record(path: Path) -> tuple[dict, dict]:
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_text()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    observation_id = f"OBS-PEOPLE-{hashlib.sha256(f'{relative}:{digest}'.encode()).hexdigest()[:12]}"
    headings = re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    linked_paths = sorted(set(re.findall(r"\(([^()\s]+\.md)(?:#[^)]+)?\)", text)))
    status_tags = sorted({tag for tag in STATUS_TAGS if re.search(rf"\b{tag}\b", text, re.IGNORECASE)})
    title = next((heading.lstrip("# ").strip() for heading in text.splitlines() if heading.startswith("#")), path.stem)
    observation = {
        "observation_id": observation_id,
        "observation_type": "LEGACY_PAGE_SNAPSHOT",
        "source_path": relative,
        "title": title,
        "content_sha256": digest,
        "byte_count": len(text.encode("utf-8")),
        "headings": headings,
        "linked_paths": linked_paths,
        "status_tags": status_tags,
        "legacy_preserved": True,
    }
    proposal_id = f"SYNTH-PEOPLE-{hashlib.sha256(observation_id.encode()).hexdigest()[:12]}"
    proposal = {
        "proposal_id": proposal_id,
        "status": "PENDING_HUMAN_REVIEW",
        "proposal_type": "LEGACY_PAGE_RECONCILIATION",
        "observation_ids": [observation_id],
        "source_path": relative,
        "subject": title,
        "proposed_action": "RETAIN_AS_LEGACY_NOTE",
        "summary": "Keep the page as historical project context; review its statements against source-linked claims before any public promotion.",
        "indicators": {
            "heading_count": len(headings),
            "linked_markdown_count": len(linked_paths),
            "status_tags": status_tags,
        },
        "promotion_allowed": False,
        "human_disposition": None,
    }
    return observation, proposal


def build(check: bool) -> int:
    observations = load_jsonl(OBSERVATIONS)
    proposals = load_jsonl(PROPOSALS)
    current_observation_ids = set()
    current_proposal_ids = set()
    pages = sorted(PEOPLE_DIR.glob("*.md"))
    for page in pages:
        observation, proposal = page_record(page)
        observations[observation["observation_id"]] = observation
        proposals[proposal["proposal_id"]] = proposal
        current_observation_ids.add(observation["observation_id"])
        current_proposal_ids.add(proposal["proposal_id"])

    before_observations = OBSERVATIONS.read_text() if OBSERVATIONS.exists() else ""
    before_proposals = PROPOSALS.read_text() if PROPOSALS.exists() else ""
    new_observations = "".join(json.dumps(observations[item], ensure_ascii=True, sort_keys=True) + "\n" for item in sorted(observations))
    new_proposals = "".join(json.dumps(proposals[item], ensure_ascii=True, sort_keys=True) + "\n" for item in sorted(proposals))
    if check:
        stale = []
        if before_observations != new_observations:
            stale.append(str(OBSERVATIONS.relative_to(ROOT)))
        if before_proposals != new_proposals:
            stale.append(str(PROPOSALS.relative_to(ROOT)))
        if stale:
            print("Generated outputs are stale; run the synthesis tool:", *stale, sep="\n- ", file=sys.stderr)
            return 1
    else:
        write_jsonl(OBSERVATIONS, observations)
        write_jsonl(PROPOSALS, proposals)
    print(f"People pages scanned: {len(pages)}")
    print(f"Current snapshots: {len(current_observation_ids)}; historical snapshots retained: {len(observations)}")
    print(f"Current proposals: {len(current_proposal_ids)}; historical proposals retained: {len(proposals)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check generated files without writing them")
    return build(parser.parse_args().check)


if __name__ == "__main__":
    raise SystemExit(main())