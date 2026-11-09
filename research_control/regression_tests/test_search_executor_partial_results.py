#!/usr/bin/env python3
"""Regression tests for honest multi-source search completion reporting."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "research_control"))
sys.path.insert(0, str(ROOT / "research_control" / "tools"))

import execute_search_targets as executor
import event_spine
import record_search_arrivals
import record_found_artifacts


TARGET = {
    "target_id": "ST-PARTIAL-TEST",
    "question": "Synthetic multi-source search test",
    "person_slots": ["Synthetic Person"],
    "jurisdictions": ["Rhode Island"],
    "record_families": ["land"],
    "date_range": {"start": 1600, "end": 1800},
    "name_variants": ["Synthetic Person"],
    "laws": [],
    "status": "READY",
}


def run_case(ia_results, ia_error, loc_results, loc_error):
    """Run the real source aggregation with deterministic fake sources."""

    def fake_ia(session, query, rows):
        if ia_error:
            raise RuntimeError(ia_error)
        return ia_results

    def fake_loc(session, query, rows):
        if loc_error:
            raise RuntimeError(loc_error)
        return loc_results

    original_ia = executor.ia_search
    original_loc = executor.loc_search
    original_sleep = executor.time.sleep

    try:
        executor.ia_search = fake_ia
        executor.loc_search = fake_loc
        executor.time.sleep = lambda _: None

        return executor.execute_target(
            target=TARGET,
            rows=10,
            delay=0,
            dry_run=False,
        )
    finally:
        executor.ia_search = original_ia
        executor.loc_search = original_loc
        executor.time.sleep = original_sleep


def test_aggregate_result_status_matrix():
    hit = [{"source": "synthetic", "record_id": "REC-1"}]

    cases = [
        ("both sources find results", hit, None, hit, None, "FOUND"),
        ("one source finds, other empty", hit, None, [], None, "FOUND"),
        ("one source finds, other errors", hit, None, [], "LOC unavailable", "PARTIAL"),
        ("one source empty, other errors", [], None, [], "LOC unavailable", "PARTIAL"),
        ("both sources error", [], "IA unavailable", [], "LOC unavailable", "ERROR"),
        ("both sources empty", [], None, [], None, "NO_RESULTS"),
        ("IA empty, LOC finds", [], None, hit, None, "FOUND"),
    ]

    for label, ia, ia_err, loc, loc_err, expected in cases:
        result = run_case(ia, ia_err, loc, loc_err)

        assert result["result_status"] == expected, (
            f"{label}: expected {expected}, got {result['result_status']}"
        )

        assert result["execution_status"] == "EXECUTED"

        # Every source's results and errors remain separately inspectable.
        assert result["source_results"]["internet_archive"]["results"] == ia
        assert result["source_results"]["library_of_congress"]["results"] == loc

        if ia_err:
            assert result["source_results"]["internet_archive"]["error"]
        if loc_err:
            assert result["source_results"]["library_of_congress"]["error"]

    print("PASS: multi-source result-status matrix")


def test_partial_execution_preserves_successful_source_results():
    hit = [{"source": "internet_archive", "record_id": "REC-IA-1"}]

    result = run_case(hit, None, [], "LOC temporarily unavailable")

    assert result["result_status"] == "PARTIAL"
    assert result["source_results"]["internet_archive"]["results"] == hit
    assert result["results"] == hit
    assert result["errors"] == [{
        "source": "library_of_congress",
        "error": "LOC temporarily unavailable",
    }]

    print("PASS: partial execution preserves successful discoveries")


def test_partial_execution_leaves_target_ready_and_records_source_arrivals():
    hit = [{"source": "internet_archive", "record_id": "REC-IA-2"}]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        targets_file = tmp / "targets.yml"
        result_dir = tmp / "results"
        event_file = tmp / "research_events.jsonl"
        search_ledger = tmp / "search_events.jsonl"
        artifact_ledger = tmp / "found_artifacts.jsonl"

        production_event_ledger = event_spine.EVENT_FILE
        production_event_bytes = (
            production_event_ledger.read_bytes()
            if production_event_ledger.exists()
            else None
        )
        production_search_ledger = record_search_arrivals.SEARCH_LEDGER
        production_search_bytes = (
            production_search_ledger.read_bytes()
            if production_search_ledger.exists()
            else None
        )
        production_artifact_ledger = record_found_artifacts.ARTIFACT_LEDGER
        production_artifact_bytes = (
            production_artifact_ledger.read_bytes()
            if production_artifact_ledger.exists()
            else None
        )

        targets_file.write_text(
            yaml.safe_dump({"targets": [TARGET]}, sort_keys=False),
            encoding="utf-8",
        )

        def fake_ia(session, query, rows):
            return hit

        def fake_loc(session, query, rows):
            raise RuntimeError("LOC temporarily unavailable")

        def fake_record_event(**kwargs):
            event = {
                "event_id": "EVT-PARTIAL-TEST",
                "timestamp": "2026-11-05T00:00:00+00:00",
                **kwargs,
            }
            with event_file.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event) + "\n")
            return event

        original_ia = executor.ia_search
        original_loc = executor.loc_search
        original_sleep = executor.time.sleep
        original_target_file = executor.TARGET_FILE
        original_result_dir = executor.RESULT_DIR
        original_record_event = executor.record_event
        original_arrival_ledger = record_search_arrivals.SEARCH_LEDGER
        original_artifact_ledger = executor.ARTIFACT_LEDGER
        original_argv = sys.argv

        try:
            executor.ia_search = fake_ia
            executor.loc_search = fake_loc
            executor.time.sleep = lambda _: None
            executor.TARGET_FILE = targets_file
            executor.RESULT_DIR = result_dir
            executor.record_event = fake_record_event
            record_search_arrivals.SEARCH_LEDGER = search_ledger
            executor.ARTIFACT_LEDGER = artifact_ledger
            sys.argv = [
                "execute_search_targets.py",
                "--target",
                TARGET["target_id"],
                "--targets-file",
                str(targets_file),
                "--delay",
                "0",
            ]

            executor.main()
        finally:
            executor.ia_search = original_ia
            executor.loc_search = original_loc
            executor.time.sleep = original_sleep
            executor.TARGET_FILE = original_target_file
            executor.RESULT_DIR = original_result_dir
            executor.record_event = original_record_event
            record_search_arrivals.SEARCH_LEDGER = original_arrival_ledger
            executor.ARTIFACT_LEDGER = original_artifact_ledger
            sys.argv = original_argv

        saved_target = yaml.safe_load(
            targets_file.read_text(encoding="utf-8")
        )["targets"][0]

        assert saved_target["status"] == "READY"

        result_files = list(result_dir.glob("ST-PARTIAL-TEST.*.json"))
        assert len(result_files) == 1

        result = json.loads(result_files[0].read_text(encoding="utf-8"))
        assert result["result_status"] == "PARTIAL"
        assert result["execution_status"] == "EXECUTED"
        assert result["event_id"] == "EVT-PARTIAL-TEST"
        assert result["source_results"]["internet_archive"]["results"] == hit

        events = [
            json.loads(line)
            for line in event_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert len(events) == 1
        assert events[0]["result"] == "PARTIAL"
        assert events[0]["status"] == "EXECUTED"

        arrivals = [
            json.loads(line)
            for line in search_ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        by_source = {row["source"]["name"]: row for row in arrivals}

        assert by_source["internet_archive"]["result"]["outcome"] == "RESULT_LOCATED"
        assert by_source["library_of_congress"]["result"]["outcome"] == "SEARCH_ERROR"

        assert by_source["internet_archive"]["visibility"] == "POSITIVE"
        assert by_source["library_of_congress"]["visibility"] == "ERROR"

        print("PASS: partial execution remains retryable and preserves source outcomes")

        artifacts = [
            json.loads(line)
            for line in artifact_ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert len(artifacts) == 1
        assert artifacts[0]["locator"]["record_identifier"] == "REC-IA-2"

        current_production_bytes = (
            production_artifact_ledger.read_bytes()
            if production_artifact_ledger.exists()
            else None
        )
        assert current_production_bytes == production_artifact_bytes, (
            "Production Found Artifact ledger changed during isolated test"
        )

        print("PASS: Found Artifact persisted only to temporary ledger")
        print("PASS: production Found Artifact ledger remained byte-for-byte unchanged")

        current_event_bytes = (
            production_event_ledger.read_bytes()
            if production_event_ledger.exists()
            else None
        )
        assert current_event_bytes == production_event_bytes, (
            "Production event spine changed during isolated test"
        )
        print("PASS: production event spine remained byte-for-byte unchanged")

        current_search_bytes = (
            production_search_ledger.read_bytes()
            if production_search_ledger.exists()
            else None
        )
        assert current_search_bytes == production_search_bytes, (
            "Production search-arrival ledger changed during isolated test"
        )
        print("PASS: production search-arrival ledger remained byte-for-byte unchanged")


if __name__ == "__main__":
    test_aggregate_result_status_matrix()
    test_partial_execution_preserves_successful_source_results()
    test_partial_execution_leaves_target_ready_and_records_source_arrivals()
    print("SEARCH EXECUTOR PARTIAL RESULTS: PASS")
