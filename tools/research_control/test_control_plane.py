import json
import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATOR = Path(__file__).with_name("validate_control_plane.py")


def run_validator(events):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        events_file = root / "research_queue" / "research_events.jsonl"
        events_file.parent.mkdir(parents=True)

        events_file.write_text(
            "\n".join(json.dumps(event) for event in events) + "\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=Path(__file__).resolve().parents[2],
            capture_output=True,
            text=True,
        )

        return result


def main():
    valid = {
        "event_id": "EVT-TEST-001",
        "timestamp": "2026-09-15T00:00:00+00:00",
        "agent": "SYSTEM_TEST",
        "action": "TEST",
        "status": "COMPLETED",
        "parent_event": "",
    }

    child = {
        **valid,
        "event_id": "EVT-TEST-002",
        "parent_event": "EVT-TEST-001",
    }

    result = run_validator([valid, child])

    if result.returncode != 0:
        raise SystemExit("FAIL: valid event chain was rejected")

    print("PASS: valid event chain accepted")
    print("CONTROL-PLANE SELF-TEST COMPLETE")


if __name__ == "__main__":
    main()
