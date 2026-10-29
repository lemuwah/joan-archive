"""Regression coverage for search-target event/write recovery."""

import json
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTROL_DIR = ROOT / "tools" / "research_control"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

import search_targets


def read_events(event_file: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in event_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ] if event_file.exists() else []


def test_retry_after_target_write_failure_does_not_duplicate_event(
    tmp_path, monkeypatch
):
    target_file = tmp_path / "SEARCH_TARGETS.yml"
    event_file = tmp_path / "events.jsonl"

    original_write_text = Path.write_text
    failed_once = {"value": False}

    def fail_target_write_once(path, data, *args, **kwargs):
        if path == target_file and not failed_once["value"]:
            failed_once["value"] = True
            raise OSError("synthetic target YAML write failure")
        return original_write_text(path, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_target_write_once)

    arguments = {
        "question": "Inspect synthetic catalog record recovery",
        "reason": "Synthetic test only; no historical evidence.",
        "source_identifier": "test_catalog:record-001",
        "target_file": target_file,
        "event_file": event_file,
    }

    with pytest.raises(OSError, match="synthetic target YAML write failure"):
        search_targets.add_target(**arguments)

    first_events = read_events(event_file)

    assert len(first_events) == 1
    assert first_events[0]["event_id"].startswith("EVT-")
    assert first_events[0]["action"] == "NEW_SEARCH_TARGET"
    assert not target_file.exists()

    # Permit the target write to succeed on retry.
    monkeypatch.setattr(Path, "write_text", original_write_text)
    search_targets.add_target(**arguments)

    final_events = read_events(event_file)
    final_targets = (
        yaml.safe_load(target_file.read_text(encoding="utf-8")) or {}
    ).get("targets", [])

    assert len(final_targets) == 1
    assert len(final_events) == 1, (
        "Retry duplicated the event after the first event append succeeded "
        "but the target YAML write failed."
    )
    assert final_events[0]["event_id"] == first_events[0]["event_id"]
    assert final_targets[0]["target_id"] == first_events[0]["target"]


@pytest.mark.parametrize("replacement_event_id", [None, "INVALID-EVENT-ID"])
def test_matching_event_with_invalid_or_missing_id_is_not_reused(
    tmp_path, monkeypatch, replacement_event_id
):
    target_file = tmp_path / "SEARCH_TARGETS.yml"
    event_file = tmp_path / "events.jsonl"
    arguments = {
        "question": "Inspect synthetic catalog record invalid event ID",
        "reason": "Synthetic test only; no historical evidence.",
        "source_identifier": "test_catalog:record-invalid-event-id",
        "target_file": target_file,
        "event_file": event_file,
    }

    original_write_text = Path.write_text
    failed_once = {"value": False}

    def fail_target_write_once(path, data, *args, **kwargs):
        if path == target_file and not failed_once["value"]:
            failed_once["value"] = True
            raise OSError("synthetic target YAML write failure")
        return original_write_text(path, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_target_write_once)
    with pytest.raises(OSError, match="synthetic target YAML write failure"):
        search_targets.add_target(**arguments)

    invalid_event = read_events(event_file)[0]
    if replacement_event_id is None:
        invalid_event.pop("event_id")
    else:
        invalid_event["event_id"] = replacement_event_id

    monkeypatch.setattr(Path, "write_text", original_write_text)
    original_write_text(
        event_file,
        json.dumps(invalid_event, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    assert not target_file.exists()

    target = search_targets.add_target(**arguments)

    events = read_events(event_file)
    targets = (yaml.safe_load(target_file.read_text(encoding="utf-8")) or {}).get(
        "targets", []
    )
    assert len(events) == 2
    assert events[0] == invalid_event
    assert re.fullmatch(r"EVT-[0-9a-f]{12}", events[1]["event_id"])
    assert events[1]["target"] == target["target_id"]
    assert [row["target_id"] for row in targets] == [target["target_id"]]


def test_repeated_successful_target_call_does_not_duplicate_event(tmp_path):
    target_file = tmp_path / "SEARCH_TARGETS.yml"
    event_file = tmp_path / "events.jsonl"
    arguments = {
        "question": "Inspect synthetic catalog record repeated call",
        "reason": "Synthetic test only; no historical evidence.",
        "source_identifier": "test_catalog:record-repeat",
        "target_file": target_file,
        "event_file": event_file,
    }

    first_target = search_targets.add_target(**arguments)
    target_bytes_after_first = target_file.read_bytes()
    event_bytes_after_first = event_file.read_bytes()

    second_target = search_targets.add_target(**arguments)

    assert second_target["target_id"] == first_target["target_id"]
    assert target_file.read_bytes() == target_bytes_after_first
    assert event_file.read_bytes() == event_bytes_after_first
    assert len(read_events(event_file)) == 1
    assert len(
        (yaml.safe_load(target_file.read_text(encoding="utf-8")) or {}).get(
            "targets", []
        )
    ) == 1


def test_distinct_targets_receive_distinct_creation_events(tmp_path):
    target_file = tmp_path / "SEARCH_TARGETS.yml"
    event_file = tmp_path / "events.jsonl"

    first_target = search_targets.add_target(
        question="Inspect synthetic catalog record one",
        reason="Synthetic test only; no historical evidence.",
        source_identifier="test_catalog:record-one",
        target_file=target_file,
        event_file=event_file,
    )
    second_target = search_targets.add_target(
        question="Inspect synthetic catalog record two",
        reason="Synthetic test only; no historical evidence.",
        source_identifier="test_catalog:record-two",
        target_file=target_file,
        event_file=event_file,
    )

    events = read_events(event_file)
    targets = (yaml.safe_load(target_file.read_text(encoding="utf-8")) or {}).get(
        "targets", []
    )
    assert first_target["target_id"] != second_target["target_id"]
    assert len(targets) == 2
    assert {event["target"] for event in events} == {
        first_target["target_id"],
        second_target["target_id"],
    }
    assert len({event["event_id"] for event in events}) == 2


def test_malformed_event_file_blocks_target_creation(tmp_path):
    target_file = tmp_path / "SEARCH_TARGETS.yml"
    event_file = tmp_path / "events.jsonl"
    malformed_event = "{not-json}\n"
    event_file.write_text(malformed_event, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid event JSON"):
        search_targets.add_target(
            question="Inspect synthetic catalog record with bad history",
            reason="Synthetic test only; no historical evidence.",
            source_identifier="test_catalog:record-bad-events",
            target_file=target_file,
            event_file=event_file,
        )

    assert event_file.read_text(encoding="utf-8") == malformed_event
    assert not target_file.exists()


def test_truncated_final_event_line_blocks_target_without_changing_history(
    tmp_path,
):
    target_file = tmp_path / "SEARCH_TARGETS.yml"
    event_file = tmp_path / "events.jsonl"
    prior_event = {
        "event_id": "EVT-000000000001",
        "timestamp": "2026-10-28T00:00:00+00:00",
        "event_class": "RESEARCH",
        "agent": "SYNTHETIC_TEST",
        "action": "PRIOR_EVENT",
        "target": "ST-PRIOR",
        "laws": [],
        "search_scope": {},
        "source": "",
        "evidence": "Synthetic fixture only.",
        "result": "Prior event preserved.",
        "status": "RECORDED",
        "contradiction": "",
        "next_action": "",
        "parent_event": "",
        "research_effect": "",
    }
    ledger_bytes = (
        json.dumps(prior_event, ensure_ascii=False, sort_keys=True).encode("utf-8")
        + b'\n{"event_id":"EVT-truncated'
    )
    event_file.write_bytes(ledger_bytes)

    with pytest.raises(ValueError, match=r"Invalid event JSON .*line 2"):
        search_targets.add_target(
            question="Inspect synthetic catalog record after interrupted append",
            reason="Synthetic test only; no historical evidence.",
            source_identifier="test_catalog:record-truncated-event",
            target_file=target_file,
            event_file=event_file,
        )

    assert event_file.read_bytes() == ledger_bytes
    assert not target_file.exists()
