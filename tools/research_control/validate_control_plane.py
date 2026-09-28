from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
EVENT_FILE = ROOT / "research_queue" / "research_events.jsonl"

ALLOWED_EVENT_CLASSES = {
    "RESEARCH",
    "SYSTEM_TEST",
    "LAW_VIOLATION",
}


def load_events():
    if not EVENT_FILE.exists():
        return []

    events = []

    for line_number, line in enumerate(
        EVENT_FILE.read_text(encoding="utf-8").splitlines(),
        1,
    ):
        if not line.strip():
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"INVALID EVENT JSON at line {line_number}: {exc}"
            )

        required = [
            "event_id",
            "timestamp",
            "event_class",
            "agent",
            "action",
            "status",
        ]

        missing = [
            field
            for field in required
            if field not in event
        ]

        if missing:
            raise SystemExit(
                f"EVENT {line_number} missing: {missing}"
            )

        if event["event_class"] not in ALLOWED_EVENT_CLASSES:
            raise SystemExit(
                f"EVENT {line_number} has invalid event_class: "
                f"{event['event_class']}"
            )

        events.append(event)

    return events


def main():
    events = load_events()

    if not events:
        print("CONTROL PLANE: no events yet")
        return 0

    ids = {event["event_id"] for event in events}

    for event in events:
        parent = event.get("parent_event", "")

        if parent and parent not in ids:
            raise SystemExit(
                f"INTEGRITY FAILURE: {event['event_id']} "
                f"references missing parent {parent}"
            )

    print(f"CONTROL PLANE: {len(events)} events validated")
    print("EVENT CLASS: OK")
    print("PARENT LINKS: OK")
    print("EVENT SCHEMA: OK")
    print("RESULT: PASS")

    return 0


if __name__ == "__main__":
    sys.exit(main())
