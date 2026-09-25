#!/usr/bin/env python3
"""
Convert a FOUND search arrival into neutral Found Artifacts.

This module records discovery and provenance only.

It does NOT create evidence, claims, identity assertions,
promotion, ranking, interpretation, or next-test instructions.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from append_event import append_record


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_LEDGER = ROOT / "research_control" / "found_artifacts.jsonl"


def artifact_id(
    search_id: str,
    record: dict,
    index: int,
) -> str:
    """
    Generate a deterministic artifact ID from the originating search
    and the returned source result.

    The index is included only to disambiguate otherwise identical
    returned results within one search arrival.
    """
    raw = json.dumps(
        {
            "search_id": search_id,
            "record": record,
            "index": index,
        },
        sort_keys=True,
        ensure_ascii=False,
    )

    number = int(
        hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12],
        16,
    ) % 1_000_000

    return f"ARTIFACT-{number:06d}"


def _timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _person_slots(record: dict) -> list[dict]:
    """
    Preserve discovered names only as NAME_APPEARANCE_ONLY.

    Do not infer identity or historical relationship.
    """
    slots = []

    for person in record.get("people", []):
        if not isinstance(person, dict):
            continue

        name = str(person.get("name", "")).strip()

        if not name:
            continue

        slots.append(
            {
                "name": name,
                "role": "NAME_APPEARANCE_ONLY",
            }
        )

    return slots


def build_found_artifacts(
    *,
    arrival: dict,
    source_results: list[dict],
    timestamp: str | None = None,
) -> list[dict]:
    """
    Build one neutral Found Artifact for each returned source result.

    Only a FOUND arrival may produce artifacts.
    NO_RESULTS and ERROR produce zero artifacts.
    """
    result = arrival.get("result", {})

    if result.get("outcome") != "RESULT_LOCATED":
        return []

    if not source_results:
        return []

    search_ref = {
        "search_id": arrival["search_id"],
        "target_id": arrival["provenance"]["session"],
        "execution_event_id": arrival["provenance"]["execution_event_id"],
    }

    source = arrival["source"]

    recorded_at = timestamp or _timestamp()
    artifacts = []

    for index, record in enumerate(source_results):
        locator = {}

        for field in (
            "url",
            "collection",
            "volume",
            "page",
            "record_id",
        ):
            value = record.get(field)

            if value is not None:
                key = (
                    "record_identifier"
                    if field == "record_id"
                    else field
                )
                locator[key] = str(value)

        discovery = {
            "matched_terms": [
                str(value)
                for value in record.get("matched_terms", [])
            ],
            "title": str(record.get("title", "")),
            "description": str(
                record.get(
                    "description",
                    "Returned by the search source.",
                )
            ),
        }

        raw_reference = record.get("raw_reference")
        if raw_reference is not None:
            discovery["raw_reference"] = str(raw_reference)

        artifact = {
            "artifact_id": artifact_id(
                arrival["search_id"],
                record,
                index,
            ),
            "found_at": recorded_at,
            "search_ref": search_ref,
            "source": {
                "name": source["name"],
                "access_method": source["access_method"],
            },
            "locator": locator,
            "discovery": discovery,
            "person_slots": _person_slots(record),
            "provenance": {
                "actor_type": "SYSTEM",
                "actor": "SEARCH_EXECUTOR",
                "platform": "joan-archive",
                "recorded_at": recorded_at,
            },
        }

        artifacts.append(artifact)

    return artifacts


def append_unique(
    record: dict,
    *,
    ledger: Path | None = None,
) -> bool:
    """
    Append one Found Artifact unless its artifact_id already exists.
    """
    target_ledger = ledger or ARTIFACT_LEDGER

    if target_ledger.exists():
        for line in target_ledger.read_text(
            encoding="utf-8"
        ).splitlines():
            if not line.strip():
                continue

            existing = json.loads(line)

            if existing.get("artifact_id") == record.get("artifact_id"):
                return False

    append_record(
        "artifact",
        record,
        ledger=target_ledger,
    )

    return True


if __name__ == "__main__":
    raise SystemExit(
        "This module is a library for the search-to-artifact bridge."
    )
