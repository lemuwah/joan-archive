from pathlib import Path
import json
import tempfile

import event_spine
from law_guard import guard_promotion


def main():
    original_event_file = event_spine.EVENT_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        test_event_file = Path(temp_dir) / "research_events.jsonl"
        test_event_file.write_text("", encoding="utf-8")

        try:
            # Route all test writes to the temporary ledger.
            event_spine.EVENT_FILE = test_event_file
            before = test_event_file.read_text(
                encoding="utf-8"
            ).splitlines()

            event = guard_promotion(
                agent="SYSTEM_TEST",
                status="CONFIRMED",
                evidence_state="AI_WORKING_COPY",
                target="TEST-LAW-VIOLATION",
            )

            if event is None:
                raise SystemExit("FAIL: no audit event returned")

            if event["event_class"] != "LAW_VIOLATION":
                raise SystemExit("FAIL: incorrect event class")

            after = test_event_file.read_text(
                encoding="utf-8"
            ).splitlines()

            if len(after) != len(before) + 1:
                raise SystemExit("FAIL: expected exactly one event")

            recorded = json.loads(after[-1])

            if recorded["event_id"] != event["event_id"]:
                raise SystemExit("FAIL: returned and recorded events differ")

            print("PASS: certainty promotion blocked")
            print("PASS: LAW_VIOLATION event written to temporary ledger")
            print("PASS: recorded event matches returned event")
            print("LAW-VIOLATION AUDIT TEST: PASS")

        finally:
            event_spine.EVENT_FILE = original_event_file


if __name__ == "__main__":
    main()
