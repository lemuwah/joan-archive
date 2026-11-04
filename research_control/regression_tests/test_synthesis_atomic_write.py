#!/usr/bin/env python3
"""Synthesis must preserve an existing ledger if publication fails."""

import importlib.util
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "tools/synthesis_workflow/synthesize_legacy_pages.py"
)

spec = importlib.util.spec_from_file_location("synthesis_atomic_write_test", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load synthesis script: {SCRIPT}")

synthesis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synthesis)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="synthesis-atomic-write-") as temp:
        path = Path(temp) / "ledger.jsonl"
        original = b'{"proposal_id":"OLD-001","human_disposition":"KEEP"}\n'
        path.write_bytes(original)

        records = {
            "NEW-001": {
                "proposal_id": "NEW-001",
                "human_disposition": None,
            }
        }

        with patch.object(
            os,
            "replace",
            side_effect=OSError("simulated publication failure"),
        ):
            try:
                synthesis.write_jsonl(path, records)
            except OSError:
                pass
            else:
                raise AssertionError("Expected publication failure")

        if path.read_bytes() != original:
            raise AssertionError(
                "Existing ledger changed after simulated publication failure"
            )

        leftovers = list(path.parent.glob(".ledger.jsonl.*.tmp"))
        if leftovers:
            raise AssertionError(f"Temporary files were left behind: {leftovers}")

    print("SYNTHESIS ATOMIC WRITE: PASS")


if __name__ == "__main__":
    main()
