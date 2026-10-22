#!/usr/bin/env python3
"""Verify a result artifact exists before the executor records its event."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "research_control"))
sys.path.insert(0, str(ROOT / "research_control" / "tools"))

import execute_search_targets as executor


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        targets_file = tmp_path / "targets.yml"
        result_dir = tmp_path / "results"

        targets_file.write_text(
            """
targets:
  - target_id: ST-PUBLICATION-FAILURE
    question: Synthetic publication-order test
    reason: Verify artifact exists before event recording.
    target_type: DOCUMENT
    person_slots:
      - Synthetic Person
    jurisdictions:
      - Rhode Island
    record_families:
      - land
    date_range:
      start: 1600
      end: 1800
    name_variants:
      - Synthetic Person
    laws:
      - No Trust Without Evidence
    status: READY
""",
            encoding="utf-8",
        )

        synthetic_result = {
            "target_id": "ST-PUBLICATION-FAILURE",
            "query": '"Synthetic Person" "Rhode Island"',
            "execution_status": "EXECUTED",
            "result_status": "FOUND",
            "source_results": {
                "internet_archive": {
                    "results": [{"record_id": "SYNTH-001"}],
                    "error": None,
                },
                "library_of_congress": {
                    "results": [],
                    "error": None,
                },
            },
            "results": [{"record_id": "SYNTH-001"}],
            "errors": [],
        }

        original_target_file = executor.TARGET_FILE
        original_result_dir = executor.RESULT_DIR
        original_execute_target = executor.execute_target
        original_record_event = executor.record_event
        original_argv = sys.argv

        observed_artifact: Path | None = None

        def fake_execute_target(**kwargs):
            return dict(synthetic_result)

        def failing_record_event(**kwargs):
            nonlocal observed_artifact

            observed_artifact = Path(kwargs["evidence"])
            assert observed_artifact.is_file(), (
                "Event recorder was called before its artifact existed"
            )

            published = json.loads(
                observed_artifact.read_text(encoding="utf-8")
            )
            assert published["run_id"], "Initial artifact lacks run ID"
            assert "event_id" not in published, (
                "Event ID should not exist before event recording"
            )

            raise RuntimeError("SYNTHETIC_EVENT_WRITE_FAILURE")

        try:
            executor.TARGET_FILE = targets_file
            executor.RESULT_DIR = result_dir
            executor.execute_target = fake_execute_target
            executor.record_event = failing_record_event
            sys.argv = [
                "execute_search_targets.py",
                "--target",
                "ST-PUBLICATION-FAILURE",
                "--delay",
                "0",
            ]

            try:
                executor.main()
            except RuntimeError as exc:
                assert str(exc) == "SYNTHETIC_EVENT_WRITE_FAILURE", (
                    f"Unexpected failure: {exc}"
                )
            else:
                raise AssertionError(
                    "Expected synthetic event-recording failure"
                )

            assert observed_artifact is not None
            assert observed_artifact.is_file(), (
                "Published artifact disappeared after event failure"
            )

            files = list(result_dir.glob("ST-PUBLICATION-FAILURE.*.json"))
            assert files == [observed_artifact], (
                f"Expected one published result artifact; found {files}"
            )

            print(
                "PASS: artifact exists before event recorder is called"
            )
            print(
                "PASS: event-recording failure leaves the artifact available"
            )
            print(
                "PASS: artifact contains a run ID but no fabricated event ID"
            )
            print(
                "PASS: synthetic failure test uses a temporary result directory"
            )
            print("SEARCH EXECUTOR PUBLICATION FAILURE: PASS")

        finally:
            executor.TARGET_FILE = original_target_file
            executor.RESULT_DIR = original_result_dir
            executor.execute_target = original_execute_target
            executor.record_event = original_record_event
            sys.argv = original_argv


if __name__ == "__main__":
    main()
