#!/usr/bin/env python3
"""Duplicate synthesis record IDs must fail closed without overwriting."""

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/synthesis_workflow/synthesize_legacy_pages.py"

spec = importlib.util.spec_from_file_location("legacy_synthesis_duplicate_test", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load synthesis script: {SCRIPT}")

synthesis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synthesis)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="joan-duplicate-id-test-") as temp:
        path = Path(temp) / "duplicate.jsonl"
        records = [
            {"proposal_id": "SYNTH-TEST-001", "human_disposition": None},
            {
                "proposal_id": "SYNTH-TEST-001",
                "human_disposition": "CONFLICTING_SECOND_RECORD",
            },
        ]
        path.write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8",
        )

        try:
            synthesis.load_jsonl(path)
        except ValueError as error:
            expected = f"{path}:2: duplicate record ID 'SYNTH-TEST-001'"
            if str(error) != expected:
                raise AssertionError(
                    f"Unexpected duplicate-ID error: {error}"
                ) from error
        else:
            raise AssertionError("Duplicate ID was silently accepted")

    print("SYNTHESIS DUPLICATE-ID GUARD: PASS")


if __name__ == "__main__":
    main()
