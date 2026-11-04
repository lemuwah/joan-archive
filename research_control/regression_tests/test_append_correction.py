#!/usr/bin/env python3
"""Regression tests for the append-only correction event ledger."""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research_control.tools import append_event  # noqa: E402


TIMESTAMP = "2026-10-19T12:00:00Z"


def correction(correction_id="CORR-000001"):
    """Return a synthetic correction record, never a historical claim."""
    return {
        "correction_id": correction_id,
        "timestamp": TIMESTAMP,
        "correction_type": "METHODOLOGY_CORRECTION",
        "target_refs": ["SYNTHETIC-TEST-ONLY"],
        "reason": "Synthetic regression test; not a historical conclusion.",
        "disposition": "UNRESOLVED",
        "uncertainty": "Synthetic test record only.",
        "provenance": {
            "actor_type": "SYSTEM",
            "actor": "regression-test",
            "platform": "joan-archive",
            "recorded_at": TIMESTAMP,
        },
    }


def expect_rejected(record, ledger, label):
    before = ledger.read_bytes() if ledger.exists() else None

    try:
        append_event.append_record("correction", record, ledger=ledger)
    except ValueError:
        pass
    else:
        raise AssertionError(f"{label}: invalid correction was accepted")

    after = ledger.read_bytes() if ledger.exists() else None
    assert after == before, f"{label}: rejected append changed the ledger"


def test_valid_correction_appends_only_to_temporary_ledger():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "corrections.jsonl"
        record = correction()

        append_event.append_record("correction", record, ledger=ledger)

        lines = ledger.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0]) == record


def test_invalid_id_is_rejected_without_writing():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "corrections.jsonl"
        record = correction("CORR-BAD")

        expect_rejected(record, ledger, "invalid ID")


def test_unknown_field_is_rejected_without_writing():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "corrections.jsonl"
        record = correction()
        record["identity_conclusion"] = "Synthetic forbidden field"

        expect_rejected(record, ledger, "unknown field")


def test_unresolved_correction_needs_no_replacement_wording():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "corrections.jsonl"
        record = correction()
        assert "corrected_wording" not in record

        append_event.append_record("correction", record, ledger=ledger)

        saved = json.loads(ledger.read_text(encoding="utf-8"))
        assert saved["disposition"] == "UNRESOLVED"
        assert "corrected_wording" not in saved


def test_duplicate_id_is_rejected_without_changing_history():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "corrections.jsonl"
        record = correction()

        append_event.append_record("correction", record, ledger=ledger)
        before = ledger.read_bytes()

        expect_rejected(record, ledger, "duplicate ID")
        assert ledger.read_bytes() == before


def test_appending_preserves_existing_history_byte_for_byte():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "corrections.jsonl"

        first = correction("CORR-000001")
        first_line = (
            json.dumps(first, ensure_ascii=False, sort_keys=True) + "\n"
        ).encode("utf-8")
        ledger.write_bytes(first_line)

        second = correction("CORR-000002")
        append_event.append_record("correction", second, ledger=ledger)

        final_bytes = ledger.read_bytes()
        assert final_bytes.startswith(first_line), (
            "Existing ledger bytes were modified"
        )

        lines = final_bytes.decode("utf-8").splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0]) == first
        assert json.loads(lines[1]) == second


def main():
    tests = [
        test_valid_correction_appends_only_to_temporary_ledger,
        test_invalid_id_is_rejected_without_writing,
        test_unknown_field_is_rejected_without_writing,
        test_unresolved_correction_needs_no_replacement_wording,
        test_duplicate_id_is_rejected_without_changing_history,
        test_appending_preserves_existing_history_byte_for_byte,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("PASS: all correction-ledger regression tests")
    print("PASS: production correction ledger was not used")


if __name__ == "__main__":
    main()
