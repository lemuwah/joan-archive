#!/usr/bin/env python3
"""
Route structured search-result records into the existing search-target
generation path.

This module is deliberately narrow:

    executed result -> structured breadcrumb lead -> child target

It does not:
- establish historical proof,
- infer identity,
- promote hypotheses,
- interpret free-form AI prose,
- bypass READY_SHADOW,
- fabricate leads from NO_RESULTS.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT / "tools" / "multi_agent_daily"))

import orchestrate


def route_search_result(
    *,
    result: dict,
    source_target: dict,
    target_file: str | Path,
    event_file: str | Path,
) -> dict:
    """
    Route structured records from one executed search result into the
    existing orchestrator target-generation path.

    The execution event ID becomes the child's origin_event so the
    resulting target can be traced directly to the search execution
    that produced the breadcrumb.
    """

    if result.get("result_status") != "FOUND":
        return {
            "generated": [],
            "deferred": [],
            "reason": "Only FOUND search results may produce breadcrumb leads.",
        }

    execution_event_id = result.get("event_id", "").strip()

    if not execution_event_id:
        raise ValueError(
            "SEARCH_RESULT_ROUTING_REQUIRES_EXECUTION_EVENT_ID"
        )

    records = result.get("results", [])

    if not isinstance(records, list):
        raise ValueError(
            "SEARCH_RESULT_ROUTING_REQUIRES_STRUCTURED_RESULTS_LIST"
        )

    leads: list[dict] = []

    person_slots = source_target.get("person_slots") or []
    record_families = source_target.get("record_families") or []
    name_variants = source_target.get("name_variants") or []

    person = person_slots[0] if person_slots else ""
    lens = record_families[0] if record_families else "search_result_breadcrumb"

    for record in records:
        if not isinstance(record, dict):
            continue

        source_identifier = (
            record.get("url")
            or record.get("record_id")
            or ""
        )

        # A structured result without a source identifier cannot provide
        # a durable breadcrumb, so it is preserved out of the target path
        # rather than silently converted into an anonymous target.
        if not source_identifier:
            continue

        title = (
            record.get("title")
            or record.get("record_id")
            or "untitled source"
        )

        leads.append(
            {
                "person_name": person,
                "lens": lens,
                "query": result.get("query", ""),
                "status": result.get("result_status", ""),
                "result": record,
                "breadcrumb_event": execution_event_id,
                "source_target_id": source_target.get("target_id", ""),
                "name_variants": name_variants,
            }
        )

    if not leads:
        return {
            "generated": [],
            "deferred": [],
            "reason": "No structured result records contained durable source identifiers.",
        }

    laws = source_target.get("laws") or []

    return orchestrate.generate_search_targets(
        leads=leads,
        origin_event=execution_event_id,
        laws=laws,
        target_file=target_file,
        event_file=event_file,
    )


if __name__ == "__main__":
    raise SystemExit(
        "This module is a library component; use route_search_result()."
    )
