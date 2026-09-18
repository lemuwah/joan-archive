#!/usr/bin/env python3
"""Regression tests for the zero-trust relationship append boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "research_control/tools/append_event.py"
LEDGER = ROOT / "research_control/relationships.jsonl"


VALID_RELATIONSHIP = {
    "relationship_id": "REL-999999",
    "evidence_id": "EVID-000001",
    "claim_id": "CLAIM-000001",
    "relation": "DIRECTLY_SUPPORTS",
    "scope": "Synthetic regression fixture only.",
    "provenance": {
        "actor_type": "AI",
        "actor": "regression-test",
        "platform": "joan-archive",
        "recorded_at": "2026-09-16T00:00:00Z",
    },
}


def run_append(record: dict, *extra_args: str) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".json",
        delete=False,
    ) as handle:
        json.dump(record, handle)
        input_path = handle.name

    try:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "relationship",
                input_path,
                *extra_args,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
    finally:
        Path(input_path).unlink(missing_ok=True)


def main() -> None:
    # The test must not inherit a pre-existing production relationship ledger.
    if LEDGER.exists():
        raise AssertionError(
            f"test requires no pre-existing ledger: {LEDGER}"
        )

    # 1. A structurally valid relationship must pass dry-run validation.
    result = run_append(VALID_RELATIONSHIP, "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "DRY-RUN OK: REL-999999" in result.stdout

    # 2. An invalid relationship ID must be rejected.
    bad_id = dict(VALID_RELATIONSHIP)
    bad_id["relationship_id"] = "REL-BAD"

    result = run_append(bad_id, "--dry-run")
    assert result.returncode != 0
    assert "invalid ID" in result.stderr

    # 3. An invented relationship type must be rejected.
    bad_relation = dict(VALID_RELATIONSHIP)
    bad_relation["relation"] = "AI_THINKS_THIS_IS_TRUE"

    result = run_append(bad_relation, "--dry-run")
    assert result.returncode != 0
    assert "invalid enum value" in result.stderr

    # 4. The append boundary must NOT require referenced claim/evidence
    #    records to exist. Cross-record validation belongs to Provenance Gate.
    result = run_append(VALID_RELATIONSHIP)
    assert result.returncode == 0, result.stderr
    assert LEDGER.exists()
    assert "APPENDED REL-999999" in result.stdout

    # 5. The same relationship ID must not append twice.
    result = run_append(VALID_RELATIONSHIP)
    assert result.returncode != 0
    assert "duplicate relationship_id REL-999999" in result.stderr

    # 6. The test-created ledger must contain exactly one record.
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    stored = json.loads(lines[0])
    assert stored["relationship_id"] == "REL-999999"
    assert stored["evidence_id"] == "EVID-000001"
    assert stored["claim_id"] == "CLAIM-000001"

    # Cleanup: this regression test must never leave synthetic research data.
    LEDGER.unlink()

    print("RELATIONSHIP APPEND REGRESSION TESTS PASSED")
    print("Valid relationship accepted.")
    print("Invalid relationship ID rejected.")
    print("Invalid relationship type rejected.")
    print("Missing referenced claim/evidence did not block append.")
    print("Duplicate relationship ID rejected.")
    print("Synthetic relationship ledger cleaned up.")


if __name__ == "__main__":
    main()
