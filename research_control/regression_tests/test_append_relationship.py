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


def run_append(
    record: dict,
    ledger: Path,
    *extra_args: str,
) -> subprocess.CompletedProcess:
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
                "--ledger-path",
                str(ledger),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
    finally:
        Path(input_path).unlink(missing_ok=True)


def main() -> None:
    # Every mutating CLI test uses an isolated temporary ledger.
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "relationships.jsonl"

        # 1. A structurally valid relationship must pass dry-run validation.
        result = run_append(VALID_RELATIONSHIP, ledger, "--dry-run")
        assert result.returncode == 0, result.stderr
        assert "DRY-RUN OK: REL-999999" in result.stdout
        assert not ledger.exists(), "dry-run unexpectedly created a ledger"

        # 2. An invalid relationship ID must be rejected.
        bad_id = dict(VALID_RELATIONSHIP)
        bad_id["relationship_id"] = "REL-BAD"

        result = run_append(bad_id, ledger, "--dry-run")
        assert result.returncode != 0
        assert "invalid ID" in result.stderr

        # 3. An invented relationship type must be rejected.
        bad_relation = dict(VALID_RELATIONSHIP)
        bad_relation["relation"] = "AI_THINKS_THIS_IS_TRUE"

        result = run_append(bad_relation, ledger, "--dry-run")
        assert result.returncode != 0
        assert "invalid enum value" in result.stderr

        # 4. Missing referenced claim/evidence records must not block append.
        result = run_append(VALID_RELATIONSHIP, ledger)
        assert result.returncode == 0, result.stderr
        assert ledger.exists()
        assert "APPENDED REL-999999" in result.stdout

        # 5. The same relationship ID must not append twice.
        before = ledger.read_bytes()
        result = run_append(VALID_RELATIONSHIP, ledger)
        assert result.returncode != 0
        assert "duplicate relationship_id REL-999999" in result.stderr
        assert ledger.read_bytes() == before, (
            "duplicate rejection modified existing ledger bytes"
        )

        # 6. The synthetic ledger must contain exactly one record.
        lines = ledger.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1

        stored = json.loads(lines[0])
        assert stored["relationship_id"] == "REL-999999"
        assert stored["evidence_id"] == "EVID-000001"
        assert stored["claim_id"] == "CLAIM-000001"

    print("RELATIONSHIP APPEND REGRESSION TESTS PASSED")
    print("Valid relationship accepted in temporary ledger.")
    print("Invalid relationship ID rejected.")
    print("Invalid relationship type rejected.")
    print("Missing referenced claim/evidence did not block append.")
    print("Duplicate relationship ID rejected without changing history.")
    print("Production relationship ledger was not used.")


if __name__ == "__main__":
    main()
