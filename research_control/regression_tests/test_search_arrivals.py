#!/usr/bin/env python3
"""
Regression tests for per-source search arrival recording.

Contract:

    SEARCH_TARGET_EXECUTED
            |
            +--> Internet Archive arrival
            |
            +--> Library of Congress arrival

Each source gets an independent arrival record.

FOUND      -> RESULT_LOCATED / POSITIVE
NO_RESULTS -> NO_RESULT_LOCATED / NEGATIVE
ERROR      -> SEARCH_ERROR / ERROR

Search arrivals record research activity only. They never establish proof.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research_control" / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

from append_event import load_schema, validate
from record_search_arrivals import append_unique, build_arrival


def target():
    return {
        "target_id": "ST-ARRIVAL-TEST",
        "question": "Find records related to Joan Unknown Greene.",
        "record_families": ["land"],
        "jurisdictions": ["Rhode Island"],
        "date_range": {"start": 1600, "end": 1800},
        "name_variants": ["Joan Unknown Greene", "Joan Greene"],
    }


def execution(event_id="EVT-ARRIVAL-TEST", status="FOUND"):
    return {
        "event_id": event_id,
        "executed_at": "2026-09-19T14:00:00+00:00",
        "query": '"Joan Unknown Greene" "land"',
        "result_status": status,
    }


def assert_schema_valid(record):
    schema = load_schema("search")
    errors = validate(record, schema)
    assert errors == [], f"Arrival failed search-event schema validation: {errors}"


def read_records(path):
    if not path.exists():
        return []

    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "search_events.jsonl"

        # ------------------------------------------------------------
        # A. FOUND source result.
        # ------------------------------------------------------------
        found = build_arrival(
            target=target(),
            execution=execution(status="FOUND"),
            source_name="internet_archive",
            source_results=[
                {
                    "source": "internet_archive",
                    "record_id": "IA-001",
                    "title": "Synthetic result",
                }
            ],
            source_error=None,
            artifact_ref="research_queue/search_results/ST-ARRIVAL-TEST.json",
            execution_event_id="EVT-ARRIVAL-TEST",
        )

        assert found["result"]["outcome"] == "RESULT_LOCATED"
        assert found["visibility"] == "POSITIVE"
        assert found["source"]["name"] == "internet_archive"
        assert found["provenance"]["execution_event_id"] == "EVT-ARRIVAL-TEST"
        assert_schema_valid(found)
        assert append_unique(found, ledger=ledger) is True

        print("PASS: FOUND -> RESULT_LOCATED / POSITIVE")

        # ------------------------------------------------------------
        # B. NO_RESULTS source result.
        # ------------------------------------------------------------
        negative = build_arrival(
            target=target(),
            execution=execution(
                event_id="EVT-ARRIVAL-NEGATIVE",
                status="NO_RESULTS",
            ),
            source_name="library_of_congress",
            source_results=[],
            source_error=None,
            artifact_ref="research_queue/search_results/ST-ARRIVAL-TEST.json",
            execution_event_id="EVT-ARRIVAL-NEGATIVE",
        )

        assert negative["result"]["outcome"] == "NO_RESULT_LOCATED"
        assert negative["visibility"] == "NEGATIVE"
        assert negative["source"]["name"] == "library_of_congress"
        assert_schema_valid(negative)
        assert append_unique(negative, ledger=ledger) is True

        print("PASS: NO_RESULTS -> NO_RESULT_LOCATED / NEGATIVE")

        # ------------------------------------------------------------
        # C. Source error.
        # ------------------------------------------------------------
        error = build_arrival(
            target=target(),
            execution=execution(
                event_id="EVT-ARRIVAL-ERROR",
                status="ERROR",
            ),
            source_name="internet_archive",
            source_results=[],
            source_error={"error": "Synthetic source failure"},
            artifact_ref="research_queue/search_results/ST-ARRIVAL-TEST.json",
            execution_event_id="EVT-ARRIVAL-ERROR",
        )

        assert error["result"]["outcome"] == "SEARCH_ERROR"
        assert error["visibility"] == "ERROR"
        assert "Synthetic source failure" in error["result"]["description"]
        assert_schema_valid(error)
        assert append_unique(error, ledger=ledger) is True

        print("PASS: SOURCE ERROR -> SEARCH_ERROR / ERROR")

        # ------------------------------------------------------------
        # D. Duplicate protection.
        # ------------------------------------------------------------
        assert append_unique(found, ledger=ledger) is False
        print("PASS: duplicate search_id is not appended")

        # ------------------------------------------------------------
        # E. One arrival remains one source.
        # ------------------------------------------------------------
        records = read_records(ledger)

        assert len(records) == 3

        sources = [record["source"]["name"] for record in records]

        assert sources.count("internet_archive") == 2
        assert sources.count("library_of_congress") == 1

        print("PASS: arrivals remain independently source-scoped")

        # ------------------------------------------------------------
        # F. Research-only boundary.
        # ------------------------------------------------------------
        for record in records:
            text = json.dumps(record, ensure_ascii=False)

            assert "PROOF" not in text
            assert record["provenance"]["actor"] == "SEARCH_EXECUTOR"
            assert "historical proof" in record["next_test"]

        print("PASS: arrivals remain research-only and non-promotional")

        print("SEARCH ARRIVAL REGRESSION TEST: PASS")


if __name__ == "__main__":
    main()
