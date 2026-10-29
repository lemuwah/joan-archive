#!/usr/bin/env python3
"""Regression test: synthesis reruns preserve existing proposal dispositions."""

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/synthesis_workflow/synthesize_legacy_pages.py"

spec = importlib.util.spec_from_file_location("legacy_synthesis", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load synthesis script: {SCRIPT}")

synthesis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synthesis)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="joan-synthesis-test-") as temp:
        temp_root = Path(temp)
        people = temp_root / "people"
        people.mkdir()
        page = people / "sample.md"
        page.write_text("# Synthetic test page\n", encoding="utf-8")

        synthesis.ROOT = temp_root
        synthesis.PEOPLE_DIR = people
        synthesis.OBSERVATIONS = (
            temp_root / "data/research/legacy_observations.jsonl"
        )
        synthesis.PROPOSALS = (
            temp_root / "data/research/synthesis_proposals.jsonl"
        )

        _, generated = synthesis.page_record(page)
        proposal_id = generated["proposal_id"]

        prior_disposition = {
            **generated,
            "human_disposition": "TEST_PRIOR_DISPOSITION_PRESERVE",
        }
        synthesis.PROPOSALS.parent.mkdir(parents=True, exist_ok=True)
        synthesis.PROPOSALS.write_text(
            json.dumps(prior_disposition, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        result = synthesis.build(check=False)
        if result != 0:
            raise AssertionError(f"Synthesis build returned {result}")

        records = [
            json.loads(line)
            for line in synthesis.PROPOSALS.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]
        matches = [r for r in records if r.get("proposal_id") == proposal_id]

        if len(matches) != 1:
            raise AssertionError(
                f"Expected exactly one proposal {proposal_id}; "
                f"found {len(matches)}"
            )

        actual = matches[0].get("human_disposition")
        if actual != "TEST_PRIOR_DISPOSITION_PRESERVE":
            raise AssertionError(
                "Existing proposal disposition was overwritten: "
                f"{actual!r}"
            )

    print("SYNTHESIS HISTORY PRESERVATION: PASS")


if __name__ == "__main__":
    main()
