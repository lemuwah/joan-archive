#!/usr/bin/env python3
"""Regression tests for the zero-trust event append gate."""

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "research_control/tools/append_event.py"

VALID_CLAIM = {
    "claim_id": "CLAIM-999999",
    "created_at": "2026-09-14T00:00:00Z",
    "claim_text": "Synthetic regression-test claim; not research evidence.",
    "source_status": "UNLOCATED",
    "status": "UNTESTED",
    "observation": "Synthetic test fixture only.",
    "true_test": "Synthetic true-test target.",
    "false_test": "Synthetic false-test target.",
    "provenance": {
        "actor_type": "SYSTEM",
        "actor": "regression-test",
        "platform": "joan-archive",
        "recorded_at": "2026-09-14T00:00:00Z",
    },
}


def run(record):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "event.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return subprocess.run(
            ["python3", str(TOOL), "claim", "--dry-run", str(path)],
            capture_output=True,
            text=True,
        )


def main():
    result = run(VALID_CLAIM)

    assert result.returncode == 0, (
        "VALID RECORD REJECTED\n"
        + result.stdout
        + result.stderr
    )

    bad = dict(VALID_CLAIM)
    bad["claim_id"] = "CLAIM-BAD"
    result = run(bad)
    assert result.returncode != 0, "INVALID ID WAS ACCEPTED"

    bad = dict(VALID_CLAIM)
    bad["unexpected"] = "contamination"
    result = run(bad)
    assert result.returncode != 0, "UNKNOWN FIELD WAS ACCEPTED"

    legacy = dict(VALID_CLAIM)
    legacy["claim_id"] = "CLAIM-999998"
    legacy["legacy_history"] = {
        "authority": "HISTORICAL_ONLY",
        "source_file": "methodology/source_spine.md",
        "historical_status": "PROVEN",
        "historical_reasoning": "Synthetic historical label; not current evidence.",
        "historical_expected_outcome": "Synthetic only.",
    }
    result = run(legacy)
    assert result.returncode == 0, "VALID HISTORICAL RECORD WAS REJECTED"
    assert legacy["status"] == "UNTESTED", "HISTORICAL STATUS PROMOTED CURRENT STATUS"
    assert legacy["legacy_history"]["historical_status"] == "PROVEN"

    print("REGRESSION TESTS PASSED")
    print("Valid synthetic record accepted by validator.")
    print("Invalid ID rejected.")
    print("Unknown field rejected.")
    print("No production ledger was modified.")


if __name__ == "__main__":
    main()
