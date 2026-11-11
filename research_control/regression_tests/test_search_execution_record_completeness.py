#!/usr/bin/env python3
"""Regression tests for read-only search publication completeness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "research_control"
CONTROL_TOOLS = ROOT / "research_control" / "tools"

sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(CONTROL_TOOLS))

import audit_search_execution_records as auditor
import record_found_artifacts as artifacts
import record_search_arrivals as arrivals


EXPECTED_SOURCES = [
    "internet_archive",
    "library_of_congress",
]


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n"
                for record in records),
        encoding="utf-8",
    )


def synthetic_publication(tmp_path: Path) -> dict:
    """Build one internally consistent, entirely synthetic execution."""

    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"
    arrival_path = tmp_path / "search_events.jsonl"
    artifact_path = tmp_path / "found_artifacts.jsonl"

    target = {
        "target_id": "ST-PUBLICATION-WIRING-TEST",
        "question": "Synthetic publication test",
        "jurisdictions": ["Synthetic jurisdiction"],
        "record_families": ["land"],
        "date_range": {"start": 1600, "end": 1800},
        "name_variants": ["Synthetic name"],
    }

    result = {
        "target_id": target["target_id"],
        "run_id": "synthetic-run-001",
        "event_id": "EVT-SYNTHETIC-001",
        "question": target["question"],
        "query": '"Synthetic name" "land" "Synthetic jurisdiction"',
        "result_status": "FOUND",
        "source_results": {
            "internet_archive": {
                "results": [
                    {
                        "title": "Synthetic IA result A",
                        "url": "https://example.invalid/ia-a",
                        "people": [{"name": "Example Person"}],
                    },
                    {
                        "title": "Synthetic IA result B",
                        "url": "https://example.invalid/ia-b",
                    },
                ],
                "error": None,
            },
            "library_of_congress": {
                "results": [
                    {
                        "title": "Synthetic LOC result",
                        "url": "https://example.invalid/loc-a",
                    },
                ],
                "error": None,
            },
        },
    }

    event = {
        "event_id": result["event_id"],
        "action": "SEARCH_TARGET_EXECUTED",
        "target": target["target_id"],
        "search_scope": {
            "run_id": result["run_id"],
            "sources": list(EXPECTED_SOURCES),
        },
        "evidence": str(result_path),
    }

    arrival_records = []
    artifact_records = []

    for source_name, source_record in result["source_results"].items():
        arrival = arrivals.build_arrival(
            target=target,
            execution=result,
            source_name=source_name,
            source_results=source_record["results"],
            source_error=source_record["error"],
            artifact_ref=str(result_path),
            execution_event_id=event["event_id"],
        )
        arrival_records.append(arrival)

        artifact_records.extend(
            artifacts.build_found_artifacts(
                arrival=arrival,
                source_results=source_record["results"],
            )
        )

    write_json(result_path, result)
    write_jsonl(event_path, [event])
    write_jsonl(arrival_path, arrival_records)
    write_jsonl(artifact_path, artifact_records)

    return {
        "result_path": result_path,
        "event_path": event_path,
        "arrival_path": arrival_path,
        "artifact_path": artifact_path,
        "result": result,
        "event": event,
        "arrivals": arrival_records,
        "artifacts": artifact_records,
    }


def audit(publication: dict) -> dict:
    return auditor.audit_execution_publications(
        result_path=publication["result_path"],
        event_file=publication["event_path"],
        arrival_file=publication["arrival_path"],
        artifact_file=publication["artifact_path"],
    )


def test_complete_two_source_publication_has_no_findings(tmp_path):
    publication = synthetic_publication(tmp_path)

    report = audit(publication)

    assert report["findings"] == [], report


def test_missing_source_arrival_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)
    remaining = [
        record for record in publication["arrivals"]
        if record["source"]["name"] != "library_of_congress"
    ]
    write_jsonl(publication["arrival_path"], remaining)

    report = audit(publication)

    assert any(
        finding["code"] == "MISSING_SOURCE_ARRIVAL"
        and finding.get("source") == "library_of_congress"
        for finding in report["findings"]
    ), report


def test_missing_found_artifact_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)
    remaining = publication["artifacts"][:-1]
    write_jsonl(publication["artifact_path"], remaining)

    report = audit(publication)

    assert any(
        finding["code"] == "MISSING_FOUND_ARTIFACT"
        for finding in report["findings"]
    ), report


def test_arrival_with_wrong_execution_event_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)
    changed = [dict(record) for record in publication["arrivals"]]
    changed[0] = json.loads(json.dumps(changed[0]))
    changed[0]["provenance"]["execution_event_id"] = "EVT-WRONG"
    write_jsonl(publication["arrival_path"], changed)

    report = audit(publication)

    assert any(
        finding["code"] == "ARRIVAL_EVENT_MISMATCH"
        for finding in report["findings"]
    ), report


def test_audit_does_not_change_any_input_bytes(tmp_path):
    publication = synthetic_publication(tmp_path)
    paths = [
        publication["result_path"],
        publication["event_path"],
        publication["arrival_path"],
        publication["artifact_path"],
    ]
    before = {path: path.read_bytes() for path in paths}

    audit(publication)

    after = {path: path.read_bytes() for path in paths}
    assert after == before


def test_duplicate_source_arrival_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)
    duplicated = publication["arrivals"] + [publication["arrivals"][0]]
    write_jsonl(publication["arrival_path"], duplicated)

    report = audit(publication)

    assert any(
        finding["code"] == "DUPLICATE_SOURCE_ARRIVAL"
        for finding in report["findings"]
    ), report


def test_duplicate_found_artifact_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)
    duplicated = publication["artifacts"] + [publication["artifacts"][0]]
    write_jsonl(publication["artifact_path"], duplicated)

    report = audit(publication)

    assert any(
        finding["code"] == "DUPLICATE_FOUND_ARTIFACT"
        for finding in report["findings"]
    ), report


def test_missing_expected_source_result_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)
    result = publication["result"]
    result["source_results"].pop("library_of_congress")
    write_json(publication["result_path"], result)

    report = audit(publication)

    assert any(
        finding["code"] == "MISSING_SOURCE_RESULT"
        and finding.get("source") == "library_of_congress"
        for finding in report["findings"]
    ), report


def test_malformed_arrival_line_is_reported_and_valid_lines_are_checked(
    tmp_path,
):
    publication = synthetic_publication(tmp_path)
    original = publication["arrival_path"].read_text(encoding="utf-8")
    publication["arrival_path"].write_text(
        '{"broken": \n' + original,
        encoding="utf-8",
    )

    report = audit(publication)

    assert any(
        finding["code"] == "MALFORMED_ARRIVAL_LINE"
        and finding.get("line") == 1
        for finding in report["findings"]
    ), report

    assert not any(
        finding["code"] == "MISSING_SOURCE_ARRIVAL"
        for finding in report["findings"]
    ), report


def test_arrival_cannot_report_no_results_when_source_returned_records(
    tmp_path,
):
    publication = synthetic_publication(tmp_path)
    changed = json.loads(json.dumps(publication["arrivals"]))

    ia_arrival = next(
        record for record in changed
        if record["source"]["name"] == "internet_archive"
    )
    ia_arrival["result"]["outcome"] = "NO_RESULT_LOCATED"
    ia_arrival["visibility"] = "NEGATIVE"
    write_jsonl(publication["arrival_path"], changed)

    report = audit(publication)

    assert any(
        finding["code"] == "SOURCE_OUTCOME_MISMATCH"
        and finding.get("source") == "internet_archive"
        for finding in report["findings"]
    ), report


def test_arrival_cannot_report_results_when_source_returned_an_error(
    tmp_path,
):
    publication = synthetic_publication(tmp_path)
    result = json.loads(json.dumps(publication["result"]))
    result["source_results"]["internet_archive"]["error"] = (
        "Synthetic source failure"
    )
    write_json(publication["result_path"], result)

    report = audit(publication)

    assert any(
        finding["code"] == "SOURCE_OUTCOME_MISMATCH"
        and finding.get("source") == "internet_archive"
        for finding in report["findings"]
    ), report


def test_found_artifact_is_reported_for_source_with_error(tmp_path):
    publication = synthetic_publication(tmp_path)
    result = json.loads(json.dumps(publication["result"]))
    result["source_results"]["internet_archive"]["error"] = (
        "Synthetic source failure"
    )
    write_json(publication["result_path"], result)

    changed = json.loads(json.dumps(publication["arrivals"]))
    ia_arrival = next(
        record for record in changed
        if record["source"]["name"] == "internet_archive"
    )
    ia_arrival["result"]["outcome"] = "SEARCH_ERROR"
    ia_arrival["visibility"] = "ERROR"
    write_jsonl(publication["arrival_path"], changed)

    report = audit(publication)

    assert any(
        finding["code"] == "ARTIFACT_FOR_ERROR_SOURCE"
        and finding.get("source") == "internet_archive"
        for finding in report["findings"]
    ), report


def test_prior_run_arrival_for_same_target_is_ignored(tmp_path):
    publication = synthetic_publication(tmp_path)

    prior_arrival = arrivals.build_arrival(
        target={
            "target_id": publication["result"]["target_id"],
            "question": publication["result"]["question"],
            "jurisdictions": ["Synthetic jurisdiction"],
            "record_families": ["land"],
            "date_range": {"start": 1600, "end": 1800},
            "name_variants": ["Synthetic name"],
        },
        execution=publication["result"],
        source_name="internet_archive",
        source_results=[],
        source_error=None,
        artifact_ref=str(publication["result_path"]),
        execution_event_id="EVT-SYNTHETIC-PRIOR-RUN",
    )

    write_jsonl(
        publication["arrival_path"],
        publication["arrivals"] + [prior_arrival],
    )

    report = audit(publication)

    assert report["findings"] == [], report


def test_ambiguous_execution_events_block_downstream_attribution(tmp_path):
    publication = synthetic_publication(tmp_path)

    duplicate_event = json.loads(json.dumps(publication["event"]))
    duplicate_event["event_id"] = "EVT-SYNTHETIC-DUPLICATE"

    write_jsonl(
        publication["event_path"],
        [publication["event"], duplicate_event],
    )

    report = audit(publication)

    assert any(
        finding["code"] == "MULTIPLE_EXECUTION_EVENTS"
        for finding in report["findings"]
    ), report

    assert any(
        finding["code"] == "DOWNSTREAM_AUDIT_SKIPPED_AMBIGUOUS_EVENT"
        for finding in report["findings"]
    ), report

    downstream_codes = {
        "MISSING_SOURCE_ARRIVAL",
        "DUPLICATE_SOURCE_ARRIVAL",
        "ARRIVAL_EVENT_MISMATCH",
        "ARRIVAL_ID_MISMATCH",
        "ARRIVAL_RESULT_PATH_MISMATCH",
        "SOURCE_OUTCOME_MISMATCH",
        "MISSING_FOUND_ARTIFACT",
        "DUPLICATE_FOUND_ARTIFACT",
        "ARTIFACT_FOR_ERROR_SOURCE",
        "FOUND_ARTIFACT_LINKAGE_MISMATCH",
    }

    assert not any(
        finding["code"] in downstream_codes
        for finding in report["findings"]
    ), report


def test_duplicate_expected_source_declarations_block_downstream_attribution(
    tmp_path,
):
    publication = synthetic_publication(tmp_path)

    publication["event"]["search_scope"]["sources"].append(
        "internet_archive"
    )

    write_jsonl(
        publication["event_path"],
        [publication["event"]],
    )

    report = audit(publication)

    assert any(
        finding["code"] == "DUPLICATE_EXPECTED_SOURCE"
        for finding in report["findings"]
    ), report

    assert any(
        finding["code"]
        == "DOWNSTREAM_AUDIT_SKIPPED_DUPLICATE_SOURCE_DECLARATION"
        for finding in report["findings"]
    ), report


def test_unexpected_artifact_for_current_execution_is_reported(tmp_path):
    publication = synthetic_publication(tmp_path)

    orphan = json.loads(json.dumps(publication["artifacts"][0]))
    orphan["artifact_id"] = "ARTIFACT-SYNTHETIC-ORPHAN"
    orphan["search_ref"]["search_id"] = "SEARCH-SYNTHETIC-UNEXPECTED"

    write_jsonl(
        publication["artifact_path"],
        [*publication["artifacts"], orphan],
    )

    report = audit(publication)

    assert any(
        finding["code"] == "UNEXPECTED_FOUND_ARTIFACT"
        and finding.get("artifact_id") == "ARTIFACT-SYNTHETIC-ORPHAN"
        for finding in report["findings"]
    ), report


def test_artifact_from_different_execution_event_is_not_reported_as_orphan(tmp_path):
    publication = synthetic_publication(tmp_path)

    older_artifact = json.loads(json.dumps(publication["artifacts"][0]))
    older_artifact["artifact_id"] = "ARTIFACT-SYNTHETIC-OLDER"
    older_artifact["search_ref"]["search_id"] = "SEARCH-SYNTHETIC-OLDER"
    older_artifact["search_ref"]["execution_event_id"] = "EVT-SYNTHETIC-OLDER"

    write_jsonl(
        publication["artifact_path"],
        [*publication["artifacts"], older_artifact],
    )

    report = audit(publication)

    assert not any(
        finding["code"] == "UNEXPECTED_FOUND_ARTIFACT"
        and finding.get("artifact_id") == "ARTIFACT-SYNTHETIC-OLDER"
        for finding in report["findings"]
    ), report


def test_non_string_expected_source_blocks_downstream_attribution(tmp_path):
    publication = synthetic_publication(tmp_path)

    publication["event"]["search_scope"]["sources"].append(
        {"unexpected": "object"}
    )

    write_jsonl(
        publication["event_path"],
        [publication["event"]],
    )

    report = audit(publication)

    assert any(
        finding["code"] == "INVALID_EXPECTED_SOURCE"
        for finding in report["findings"]
    ), report

    assert any(
        finding["code"]
        == "DOWNSTREAM_AUDIT_SKIPPED_INVALID_SOURCE_DECLARATION"
        for finding in report["findings"]
    ), report


def test_non_string_found_artifact_id_is_reported_without_crashing_or_writes(
    tmp_path,
):
    publication = synthetic_publication(tmp_path)

    malformed = json.loads(
        json.dumps(publication["artifacts"])
    )
    malformed[0]["artifact_id"] = {"unexpected": "object"}

    write_jsonl(publication["artifact_path"], malformed)

    paths = [
        publication["result_path"],
        publication["event_path"],
        publication["arrival_path"],
        publication["artifact_path"],
    ]
    before = {
        path: path.read_bytes()
        for path in paths
    }

    report = audit(publication)

    assert any(
        finding["code"] == "INVALID_FOUND_ARTIFACT_ID"
        for finding in report["findings"]
    ), report

    assert any(
        finding["code"] == "MISSING_FOUND_ARTIFACT"
        for finding in report["findings"]
    ), report

    assert {
        path: path.read_bytes()
        for path in paths
    } == before


def test_non_string_found_artifact_search_id_is_reported_without_crashing_or_writes(
    tmp_path,
):
    publication = synthetic_publication(tmp_path)

    malformed = json.loads(
        json.dumps(publication["artifacts"])
    )
    malformed[0]["search_ref"]["search_id"] = {
        "unexpected": "object"
    }

    write_jsonl(publication["artifact_path"], malformed)

    paths = [
        publication["result_path"],
        publication["event_path"],
        publication["arrival_path"],
        publication["artifact_path"],
    ]
    before = {
        path: path.read_bytes()
        for path in paths
    }

    report = audit(publication)

    assert any(
        finding["code"] == "INVALID_FOUND_ARTIFACT_SEARCH_ID"
        for finding in report["findings"]
    ), report

    assert {
        path: path.read_bytes()
        for path in paths
    } == before


@pytest.mark.parametrize(
    ("ledger_key", "error_code", "forbidden_codes"),
    [
        (
            "event_path",
            "INVALID_EVENT_ENCODING",
            {"MISSING_EXECUTION_EVENT"},
        ),
        (
            "arrival_path",
            "INVALID_ARRIVAL_ENCODING",
            {"MISSING_SOURCE_ARRIVAL", "MISSING_FOUND_ARTIFACT"},
        ),
        (
            "artifact_path",
            "INVALID_FOUND_ARTIFACT_ENCODING",
            {"MISSING_SOURCE_ARRIVAL", "MISSING_FOUND_ARTIFACT"},
        ),
    ],
)
def test_invalid_ledger_encoding_stops_downstream_attribution(
    tmp_path, ledger_key, error_code, forbidden_codes
):
    publication = synthetic_publication(tmp_path)
    publication[ledger_key].write_bytes(b"\xff\n")

    report = audit(publication)
    codes = {finding["code"] for finding in report["findings"]}

    assert error_code in codes, report
    assert "DOWNSTREAM_AUDIT_SKIPPED_UNREADABLE_LEDGER" in codes, report
    assert not (codes & forbidden_codes), report


@pytest.mark.parametrize(
    ("ledger_key", "error_code", "forbidden_codes"),
    [
        (
            "event_path",
            "EVENT_READ_ERROR",
            {"MISSING_EXECUTION_EVENT"},
        ),
        (
            "arrival_path",
            "ARRIVAL_READ_ERROR",
            {"MISSING_SOURCE_ARRIVAL", "MISSING_FOUND_ARTIFACT"},
        ),
        (
            "artifact_path",
            "FOUND_ARTIFACT_READ_ERROR",
            {"MISSING_SOURCE_ARRIVAL", "MISSING_FOUND_ARTIFACT"},
        ),
    ],
)
def test_ledger_read_error_stops_downstream_attribution(
    tmp_path, monkeypatch, ledger_key, error_code, forbidden_codes
):
    publication = synthetic_publication(tmp_path)
    unreadable_path = publication[ledger_key]
    original_read_text = Path.read_text

    def read_text_with_selected_failure(path, *args, **kwargs):
        if path == unreadable_path:
            raise PermissionError("synthetic permission failure")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text_with_selected_failure)

    report = audit(publication)
    codes = {finding["code"] for finding in report["findings"]}

    assert error_code in codes, report
    assert "DOWNSTREAM_AUDIT_SKIPPED_UNREADABLE_LEDGER" in codes, report
    assert not (codes & forbidden_codes), report
