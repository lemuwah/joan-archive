#!/usr/bin/env python3
"""Convert one executed search result into structured per-source search arrivals.

This records research activity only. It does not create evidence or claims.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from append_event import append_record

ROOT = Path(__file__).resolve().parents[2]
SEARCH_LEDGER = ROOT / "research_control" / "search_events.jsonl"


def search_id(
    target_id: str,
    source_name: str,
    execution_event_id: str,
) -> str:
    """Create a schema-compatible ID unique to one execution/source arrival."""
    raw = f"{target_id}|{source_name}|{execution_event_id}"
    number = int(
        hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12],
        16,
    ) % 1_000_000
    return f"SEARCH-{number:06d}"


def source_access_method(source_name: str) -> str:
    return {
        "internet_archive": "DATABASE",
        "library_of_congress": "DATABASE",
    }.get(source_name, "OTHER")


def outcome_for(result_status: str, source_results: list, source_error: dict | None) -> tuple[str, str]:
    if source_error:
        return "SEARCH_ERROR", "ERROR"

    if source_results:
        return "RESULT_LOCATED", "POSITIVE"

    return "NO_RESULT_LOCATED", "NEGATIVE"


def build_arrival(
    *,
    target: dict,
    execution: dict,
    source_name: str,
    source_results: list,
    source_error: dict | None,
    artifact_ref: str,
    execution_event_id: str,
) -> dict:
    outcome, visibility = outcome_for(
        execution.get("result_status", ""),
        source_results,
        source_error,
    )

    timestamp = execution.get("executed_at") or dt.datetime.now(
        dt.timezone.utc
    ).isoformat()

    return {
        "search_id": search_id(
            target["target_id"],
            source_name,
            execution_event_id,
        ),
        "timestamp": timestamp,
        "question": target.get("question", ""),
        "scope": {
            "repository": source_name,
            "record_type": ", ".join(
                str(value) for value in target.get("record_families", [])
            ),
            "jurisdiction": ", ".join(
                str(value) for value in target.get("jurisdictions", [])
            ),
            "date_range": str(target.get("date_range", "")),
        },
        "query": {
            "terms": [execution.get("query", "")],
            "variants": [
                str(value)
                for value in target.get("name_variants", [])
            ],
        },
        "source": {
            "name": source_name,
            "access_method": source_access_method(source_name),
        },
        "result": {
            "outcome": outcome,
            "description": (
                f"{len(source_results)} result(s) located."
                if source_results
                else (
                    f"Search error: {source_error.get('error', '')}"
                    if source_error
                    else "No result located in this defined search."
                )
            ),
            "artifact_ref": artifact_ref,
        },
        "visibility": visibility,
        "provenance": {
            "actor_type": "SYSTEM",
            "actor": "SEARCH_EXECUTOR",
            "platform": "joan-archive",
            "session": target["target_id"],
            "recorded_at": timestamp,
        },
        "blind_spots": [],
        "next_test": (
            "Review source lead; do not treat search output as historical proof."
        ),
    }


def append_unique(
    record: dict,
    ledger: Path | None = None,
) -> bool:
    """Validate and append one search event through the authoritative writer."""
    target_ledger = ledger if ledger is not None else SEARCH_LEDGER

    try:
        append_record("search", record, ledger=target_ledger)
    except ValueError as exc:
        if str(exc).startswith("REFUSING TO APPEND: duplicate search_id"):
            return False
        raise

    return True
