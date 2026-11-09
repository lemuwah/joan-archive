import json
import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATOR = Path(__file__).with_name("validate_control_plane.py")
PRODUCTION_EVENTS = (
    Path(__file__).resolve().parents[2]
    / "research_queue"
    / "research_events.jsonl"
)


def run_validator(events):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        events_file = root / "research_queue" / "research_events.jsonl"
        events_file.parent.mkdir(parents=True)

        events_file.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--events",
                str(events_file),
            ],
            cwd=Path(__file__).resolve().parents[2],
            capture_output=True,
            text=True,
        )

        return result


def main():
    production_before = (
        PRODUCTION_EVENTS.read_bytes()
        if PRODUCTION_EVENTS.exists()
        else None
    )

    valid = {
        "event_id": "EVT-TEST-001",
        "timestamp": "2026-09-15T00:00:00+00:00",
        "event_class": "SYSTEM_TEST",
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

    assert result.returncode == 0, (
        "Valid synthetic event chain was rejected. "
        f"stdout={result.stdout!r}, stderr={result.stderr!r}"
    )
    assert "2 events validated" in result.stdout
    print("PASS: valid synthetic event chain accepted")

    broken_child = {
        **child,
        "event_id": "EVT-TEST-003",
        "parent_event": "EVT-MISSING-PARENT",
    }

    result = run_validator([valid, broken_child])

    assert result.returncode != 0, (
        "Synthetic chain with missing parent was incorrectly accepted"
    )
    assert "references missing parent EVT-MISSING-PARENT" in result.stderr
    print("PASS: missing-parent synthetic chain rejected")

    production_after = (
        PRODUCTION_EVENTS.read_bytes()
        if PRODUCTION_EVENTS.exists()
        else None
    )

    assert production_after == production_before, (
        "Production event ledger changed during control-plane test"
    )
    print("PASS: production event ledger remained byte-for-byte unchanged")
    print("CONTROL-PLANE SELF-TEST: PASS")


if __name__ == "__main__":
    main()
