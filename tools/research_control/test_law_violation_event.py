from pathlib import Path
import json

from law_guard import guard_promotion


ROOT = Path(__file__).resolve().parents[2]
EVENT_FILE = ROOT / "research_queue" / "research_events.jsonl"


def main():
    before = EVENT_FILE.read_text(encoding="utf-8").splitlines()

    event = guard_promotion(
        agent="SYSTEM_TEST",
        status="CONFIRMED",
        evidence_state="AI_WORKING_COPY",
        target="TEST-LAW-VIOLATION",
    )

    if event is None:
        raise SystemExit(
            "FAIL: blocked promotion did not return an audit event"
        )

    if event["event_class"] != "LAW_VIOLATION":
        raise SystemExit(
            "FAIL: blocked promotion was not classified "
            "as LAW_VIOLATION"
        )

    after = EVENT_FILE.read_text(encoding="utf-8").splitlines()

    if len(after) != len(before) + 1:
        raise SystemExit(
            "FAIL: exactly one audit event was not appended"
        )

    recorded = json.loads(after[-1])

    if recorded["event_id"] != event["event_id"]:
        raise SystemExit(
            "FAIL: returned event does not match recorded event"
        )

    print("PASS: certainty promotion blocked")
    print("PASS: LAW_VIOLATION event created")
    print("PASS: event written to Event Spine")
    print("PASS: recorded event matches returned event")
    print("LAW-VIOLATION AUDIT TEST: PASS")


if __name__ == "__main__":
    main()
