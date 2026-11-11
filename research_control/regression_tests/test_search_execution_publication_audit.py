#!/usr/bin/env python3
"""Read-only audit test for an interrupted search-result publication."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

import audit_search_execution_publications as auditor


def test_result_without_matching_event_is_reported_without_writes(tmp_path):
    result_dir = tmp_path / "results"
    result_dir.mkdir()

    result_path = result_dir / "ST-AUDIT-TEST.synthetic-run.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-AUDIT-TEST",
        "question": "Synthetic publication audit test",
        "execution_status": "EXECUTED",
        "executed_at": "2026-11-06T12:00:00+00:00",
        "query": '"Synthetic Person" "Rhode Island"',
        "results": [
            {"record_id": "SYNTHETIC-RECORD-001"}
        ],
        "errors": [],
        "source_results": {
            "internet_archive": {
                "results": [
                    {"record_id": "SYNTHETIC-RECORD-001"}
                ],
                "error": None,
            },
            "library_of_congress": {
                "results": [],
                "error": "Synthetic connection failure",
            },
        },
        "result_status": "PARTIAL",
        "run_id": "synthetic-run-001",
        "note": (
            "Search output is a source lead only. "
            "It does not establish historical proof, identity, or certainty."
        ),
    }

    result_path.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    event_path.write_text("", encoding="utf-8")

    # Capture exact input bytes so this test can prove the auditor is read-only.
    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "RESULT_MISSING_EVENT"
        and finding["target_id"] == "ST-AUDIT-TEST"
        and finding["run_id"] == "synthetic-run-001"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_matching_execution_event_is_accepted_without_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-MATCH-TEST",
        "run_id": "matching-run-001",
        "event_id": "EVT-MATCH-TEST",
    }
    event = {
        "event_id": "EVT-MATCH-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-MATCH-TEST",
        "search_scope": {
            "run_id": "matching-run-001",
        },
        "evidence": str(result_path),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert report["findings"] == []
    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_event_published_before_result_event_id_is_reported(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-INTERRUPTED-TEST",
        "run_id": "interrupted-run-001",
    }
    event = {
        "event_id": "EVT-INTERRUPTED-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-INTERRUPTED-TEST",
        "search_scope": {
            "run_id": "interrupted-run-001",
        },
        "evidence": str(result_path),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "RESULT_MISSING_EVENT_ID"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_conflicting_result_event_id_is_reported_without_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-CONFLICT-TEST",
        "run_id": "conflict-run-001",
        "event_id": "EVT-WRONG",
    }
    event = {
        "event_id": "EVT-CORRECT",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-CONFLICT-TEST",
        "search_scope": {
            "run_id": "conflict-run-001",
        },
        "evidence": str(result_path),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "RESULT_EVENT_ID_MISMATCH"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_event_with_wrong_evidence_path_is_reported_without_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-PATH-TEST",
        "run_id": "path-run-001",
        "event_id": "EVT-PATH-TEST",
    }
    event = {
        "event_id": "EVT-PATH-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-PATH-TEST",
        "search_scope": {
            "run_id": "path-run-001",
        },
        "evidence": str(tmp_path / "different-result.json"),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "EVENT_EVIDENCE_PATH_MISMATCH"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_equivalent_absolute_and_relative_paths_are_accepted(tmp_path):
    import os

    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-RELATIVE-PATH-TEST",
        "run_id": "relative-path-run-001",
        "event_id": "EVT-RELATIVE-PATH-TEST",
    }
    event = {
        "event_id": "EVT-RELATIVE-PATH-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-RELATIVE-PATH-TEST",
        "search_scope": {
            "run_id": "relative-path-run-001",
        },
        "evidence": str(result_path.resolve()),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    relative_result_path = Path(
        os.path.relpath(result_path, Path.cwd())
    )

    report = auditor.audit_result_event(
        result_path=relative_result_path,
        event_file=event_path,
    )

    assert report["findings"] == [], report


def test_multiple_matching_execution_events_are_reported(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-DUPLICATE-EVENT-TEST",
        "run_id": "duplicate-event-run-001",
        "event_id": "EVT-DUPLICATE-A",
    }

    events = [
        {
            "event_id": "EVT-DUPLICATE-A",
            "action": "SEARCH_TARGET_EXECUTED",
            "target": "ST-DUPLICATE-EVENT-TEST",
            "search_scope": {"run_id": "duplicate-event-run-001"},
            "evidence": str(result_path),
        },
        {
            "event_id": "EVT-DUPLICATE-B",
            "action": "SEARCH_TARGET_EXECUTED",
            "target": "ST-DUPLICATE-EVENT-TEST",
            "search_scope": {"run_id": "duplicate-event-run-001"},
            "evidence": str(result_path),
        },
    ]

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        "".join(json.dumps(event) + "\n" for event in events),
        encoding="utf-8",
    )

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "MULTIPLE_MATCHING_EXECUTION_EVENTS"
        for finding in report["findings"]
    ), report

    assert any(
        finding["code"] == "DOWNSTREAM_AUDIT_SKIPPED_AMBIGUOUS_EVENT"
        for finding in report["findings"]
    ), report


def test_malformed_event_line_is_reported_while_valid_lines_are_checked(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-MALFORMED-EVENT-TEST",
        "run_id": "malformed-run-001",
        "event_id": "EVT-MALFORMED-TEST",
    }

    valid_event = {
        "event_id": "EVT-MALFORMED-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-MALFORMED-EVENT-TEST",
        "search_scope": {"run_id": "malformed-run-001"},
        "evidence": str(result_path),
    }

    malformed_line = '{"event_id": "BROKEN", "action": '
    event_path.write_text(
        malformed_line + "\n" + json.dumps(valid_event) + "\n",
        encoding="utf-8",
    )
    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )

    before_events = event_path.read_bytes()
    before_result = result_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "MALFORMED_EVENT_LINE"
        and finding["event_line"] == 1
        for finding in report["findings"]
    ), report

    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert event_path.read_bytes() == before_events
    assert result_path.read_bytes() == before_result


def test_non_object_event_line_is_reported_while_valid_lines_are_checked(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-INVALID-SHAPE-TEST",
        "run_id": "invalid-shape-run",
        "event_id": "EVT-INVALID-SHAPE-TEST",
    }

    valid_event = {
        "event_id": "EVT-INVALID-SHAPE-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-INVALID-SHAPE-TEST",
        "search_scope": {"run_id": "invalid-shape-run"},
        "evidence": str(result_path),
    }

    event_path.write_text(
        "[]\n" + json.dumps(valid_event) + "\n",
        encoding="utf-8",
    )
    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )

    before_events = event_path.read_bytes()
    before_result = result_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_EVENT_SHAPE"
        and finding["event_line"] == 1
        for finding in report["findings"]
    ), report

    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert event_path.read_bytes() == before_events
    assert result_path.read_bytes() == before_result


def test_invalid_search_scope_shape_is_reported_while_valid_events_are_checked(
    tmp_path,
):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-NESTED-SHAPE-TEST",
        "run_id": "nested-shape-run",
        "event_id": "EVT-NESTED-SHAPE-TEST",
    }

    invalid_event = {
        "event_id": "EVT-INVALID-NESTED",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-NESTED-SHAPE-TEST",
        "search_scope": [],
        "evidence": str(result_path),
    }

    valid_event = {
        "event_id": "EVT-NESTED-SHAPE-TEST",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-NESTED-SHAPE-TEST",
        "search_scope": {"run_id": "nested-shape-run"},
        "evidence": str(result_path),
    }

    event_path.write_text(
        json.dumps(invalid_event) + "\n"
        + json.dumps(valid_event) + "\n",
        encoding="utf-8",
    )
    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )

    before_events = event_path.read_bytes()
    before_result = result_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_EVENT_SEARCH_SCOPE"
        and finding["event_line"] == 1
        for finding in report["findings"]
    ), report

    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert event_path.read_bytes() == before_events
    assert result_path.read_bytes() == before_result


def test_non_object_result_is_reported_without_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result_path.write_text("[]\n", encoding="utf-8")
    event_path.write_text("", encoding="utf-8")

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_RESULT_SHAPE"
        for finding in report["findings"]
    ), report

    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert report["target_id"] is None
    assert report["run_id"] is None
    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_malformed_result_json_is_reported_without_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result_path.write_text("{broken\n", encoding="utf-8")
    event_path.write_text("", encoding="utf-8")

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "MALFORMED_RESULT_JSON"
        for finding in report["findings"]
    ), report

    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert report["target_id"] is None
    assert report["run_id"] is None
    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_non_string_event_id_is_reported_without_crashing_or_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-INVALID-EVENT-ID-TEST",
        "run_id": "invalid-event-id-run",
        "event_id": "EVT-EXPECTED",
    }
    event = {
        "event_id": ["NOT", "A", "STRING"],
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-INVALID-EVENT-ID-TEST",
        "search_scope": {"run_id": "invalid-event-id-run"},
        "evidence": str(result_path),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_EVENT_ID"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_non_string_result_event_id_is_reported_without_crashing_or_writes(
    tmp_path,
):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-INVALID-RESULT-EVENT-ID",
        "run_id": "invalid-result-event-id-run",
        "event_id": {"unexpected": "object"},
    }
    event = {
        "event_id": "EVT-EXPECTED",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-INVALID-RESULT-EVENT-ID",
        "search_scope": {"run_id": "invalid-result-event-id-run"},
        "evidence": str(result_path),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_RESULT_EVENT_ID"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_missing_event_id_is_reported_without_crashing_or_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-MISSING-EVENT-ID",
        "run_id": "missing-event-id-run",
        "event_id": "EVT-EXPECTED",
    }
    event = {
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-MISSING-EVENT-ID",
        "search_scope": {"run_id": "missing-event-id-run"},
        "evidence": str(result_path),
    }

    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )
    event_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_EVENT_ID"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_empty_event_id_is_reported_without_crashing_or_writes(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-EMPTY-EVENT-ID",
        "run_id": "empty-event-id-run",
        "event_id": "EVT-EXPECTED",
    }
    event = {
        "event_id": "   ",
        "action": "SEARCH_TARGET_EXECUTED",
        "target": "ST-EMPTY-EVENT-ID",
        "search_scope": {"run_id": "empty-event-id-run"},
        "evidence": str(result_path),
    }

    result_path.write_text(json.dumps(result) + "\n", encoding="utf-8")
    event_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "INVALID_EVENT_ID"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_result_with_invalid_utf8_returns_structured_finding(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result_path.write_bytes(b'{"target_id": "\xff"}')
    event_path.write_text("", encoding="utf-8")

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "RESULT_INVALID_ENCODING"
        for finding in report["findings"]
    ), report

    assert report["target_id"] is None
    assert report["run_id"] is None
    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_event_ledger_with_invalid_utf8_returns_structured_finding(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-INVALID-EVENT-LEDGER-ENCODING",
        "run_id": "invalid-event-ledger-encoding-run",
        "event_id": "EVT-EXPECTED",
    }
    result_path.write_text(json.dumps(result) + "\n", encoding="utf-8")
    event_path.write_bytes(b'{"event_id": "\xff"}\n')

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "EVENT_LEDGER_INVALID_ENCODING"
        for finding in report["findings"]
    ), report

    assert report["target_id"] == result["target_id"]
    assert report["run_id"] == result["run_id"]
    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_missing_result_file_returns_structured_read_error(tmp_path):
    result_path = tmp_path / "missing-result.json"
    event_path = tmp_path / "events.jsonl"
    event_path.write_text("", encoding="utf-8")

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "RESULT_READ_ERROR"
        for finding in report["findings"]
    ), report
    assert report["target_id"] is None
    assert report["run_id"] is None
    assert not result_path.exists()
    assert event_path.read_bytes() == b""


def test_event_ledger_oserror_returns_structured_read_error(
    tmp_path, monkeypatch
):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-EVENT-LEDGER-READ-ERROR",
        "run_id": "event-ledger-read-error-run",
        "event_id": "EVT-EXPECTED",
    }
    result_path.write_text(json.dumps(result) + "\n", encoding="utf-8")
    event_path.write_text("", encoding="utf-8")

    before_result = result_path.read_bytes()
    before_events = event_path.read_bytes()
    original_read_text = Path.read_text

    def fail_event_ledger_read(path, *args, **kwargs):
        if path == event_path:
            raise PermissionError("synthetic event-ledger read denial")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", fail_event_ledger_read)

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "EVENT_LEDGER_READ_ERROR"
        for finding in report["findings"]
    ), report
    assert report["target_id"] == result["target_id"]
    assert report["run_id"] == result["run_id"]
    assert not any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report

    assert result_path.read_bytes() == before_result
    assert event_path.read_bytes() == before_events


def test_missing_event_ledger_preserves_missing_event_finding(tmp_path):
    result_path = tmp_path / "result.json"
    event_path = tmp_path / "events.jsonl"

    result = {
        "target_id": "ST-MISSING-EVENT-LEDGER",
        "run_id": "missing-event-ledger-run",
        "event_id": "EVT-EXPECTED",
    }
    result_path.write_text(
        json.dumps(result) + "\n",
        encoding="utf-8",
    )

    report = auditor.audit_result_event(
        result_path=result_path,
        event_file=event_path,
    )

    assert any(
        finding["code"] == "RESULT_MISSING_EVENT"
        for finding in report["findings"]
    ), report
    assert not any(
        finding["code"] in {
            "EVENT_LEDGER_INVALID_ENCODING",
            "EVENT_LEDGER_READ_ERROR",
        }
        for finding in report["findings"]
    ), report
    assert not event_path.exists()
