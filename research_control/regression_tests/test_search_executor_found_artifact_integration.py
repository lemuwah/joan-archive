#!/usr/bin/env python3
"""
READ-ONLY REGRESSION TEST

Proves the live search executor seam can distinguish source-specific
Found Artifact creation:

    source with results     -> Found Artifact(s)
    source with no results  -> zero Found Artifacts

This test does NOT modify production ledgers.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "research_control"
CONTROL_TOOLS = ROOT / "research_control" / "tools"

sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(CONTROL_TOOLS))

import execute_search_targets as executor
import record_found_artifacts as artifacts
import record_search_arrivals


def main() -> None:
    print("=" * 60)
    print("LIVE EXECUTOR -> FOUND ARTIFACT INTEGRATION TEST")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        target_file = tmp / "targets.yml"
        result_dir = tmp / "results"
        result_dir.mkdir()

        event_ledger = tmp / "events.jsonl"
        arrival_ledger = tmp / "search_events.jsonl"
        artifact_ledger = tmp / "found_artifacts.jsonl"

        # Capture production state before redirecting anything.
        production_artifact_ledger = artifacts.ARTIFACT_LEDGER
        production_artifact_bytes = (
            production_artifact_ledger.read_bytes()
            if production_artifact_ledger.exists()
            else None
        )

        original_targets_file = executor.TARGET_FILE
        original_result_dir = executor.RESULT_DIR
        original_artifact_ledger = executor.ARTIFACT_LEDGER
        original_arrival_ledger = record_search_arrivals.SEARCH_LEDGER
        original_ia = executor.ia_search
        original_loc = executor.loc_search
        original_record_event = executor.record_event
        original_argv = sys.argv

        target = {
            "target_id": "ST-EXEC-ARTIFACT",
            "question": "Joan Greene",
            "person_slots": ["Joan Greene"],
            "jurisdictions": ["Rhode Island"],
            "record_families": ["land"],
            "date_range": {
                "start": 1600,
                "end": 1800,
            },
            "name_variants": ["Joan Greene"],
            "rows": 5,
            "status": "READY",
        }

        target_file.write_text(
            "targets:\n"
            "  - target_id: ST-EXEC-ARTIFACT\n"
            "    question: Joan Greene\n"
            "    person_slots:\n"
            "      - Joan Greene\n"
            "    jurisdictions:\n"
            "      - Rhode Island\n"
            "    record_families:\n"
            "      - land\n"
            "    date_range:\n"
            "      start: 1600\n"
            "      end: 1800\n"
            "    name_variants:\n"
            "      - Joan Greene\n"
            "    rows: 5\n"
            "    status: READY\n",
            encoding="utf-8",
        )

        # Synthetic source behavior:
        # Internet Archive returns one result.
        # Library of Congress returns no results.
        def fake_ia(session, query, rows):
            return [
                {
                    "url": "https://example.org/record/123",
                    "collection": "Example Collection",
                    "volume": "Volume I",
                    "page": "123",
                    "record_id": "REC-123",
                    "matched_terms": ["Joan Greene"],
                    "title": "Example record",
                    "description": "Synthetic result containing Joan Greene.",
                    "raw_reference": "EXAMPLE-123",
                    "people": [
                        {
                            "name": "Joan Greene",
                        }
                    ],
                }
            ]

        def fake_loc(session, query, rows):
            return []

        # Keep the existing synthetic event identity deterministic.
        def fake_record_event(**kwargs):
            return {
                "event_id": "EVT-EXEC-ARTIFACT-001",
            }

        # Execute the real production orchestration with every patched
        # global protected by one restoration boundary.
        try:
            executor.TARGET_FILE = target_file
            executor.RESULT_DIR = result_dir
            executor.ARTIFACT_LEDGER = artifact_ledger
            record_search_arrivals.SEARCH_LEDGER = arrival_ledger

            executor.ia_search = fake_ia
            executor.loc_search = fake_loc
            executor.record_event = fake_record_event

            sys.argv = [
                "execute_search_targets.py",
                "--target",
                "ST-EXEC-ARTIFACT",
                "--targets-file",
                str(target_file),
                "--rows",
                "5",
                "--delay",
                "0",
            ]

            executor.main()
        finally:
            executor.TARGET_FILE = original_targets_file
            executor.RESULT_DIR = original_result_dir
            executor.ARTIFACT_LEDGER = original_artifact_ledger
            record_search_arrivals.SEARCH_LEDGER = original_arrival_ledger

            executor.ia_search = original_ia
            executor.loc_search = original_loc
            executor.record_event = original_record_event

            sys.argv = original_argv

        # The production ledger must remain byte-for-byte unchanged.
        current_production_bytes = (
            production_artifact_ledger.read_bytes()
            if production_artifact_ledger.exists()
            else None
        )
        assert current_production_bytes == production_artifact_bytes, (
            "Production Found Artifact ledger changed during isolated test"
        )
        print("PASS: production Found Artifact ledger remained byte-for-byte unchanged")

        result_files = list(result_dir.glob("ST-EXEC-ARTIFACT.*.json"))
        assert len(result_files) == 1, (
            f"Expected exactly one uniquely named result file, "
            f"found {len(result_files)}: {result_files}"
        )
        result = json.loads(
            result_files[0].read_text(encoding="utf-8")
        )

        print("\n=== EXECUTOR RESULT ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        assert result["result_status"] == "FOUND"
        print("\nPASS: overall execution is FOUND")

        assert result["source_results"]["internet_archive"]["results"]
        assert result["source_results"]["library_of_congress"]["results"] == []
        print("PASS: source-specific result sets are preserved")

        # Read the arrivals actually persisted by production main().
        arrivals = [
            json.loads(line)
            for line in arrival_ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        print("\n=== PERSISTED ARRIVAL STATES ===")
        for arrival in arrivals:
            print(
                arrival["source"]["name"],
                "->",
                arrival["result"]["outcome"],
            )

        ia_arrival = next(
            a for a in arrivals
            if a["source"]["name"] == "internet_archive"
        )
        loc_arrival = next(
            a for a in arrivals
            if a["source"]["name"] == "library_of_congress"
        )

        assert ia_arrival["result"]["outcome"] == "RESULT_LOCATED"
        assert loc_arrival["result"]["outcome"] == "NO_RESULT_LOCATED"
        print("PASS: production persisted source-specific arrival outcomes")

        # Read Found Artifacts actually persisted by production main().
        found_artifacts = [
            json.loads(line)
            for line in artifact_ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        ia_artifacts = [
            a for a in found_artifacts
            if a["source"]["name"] == "internet_archive"
        ]
        loc_artifacts = [
            a for a in found_artifacts
            if a["source"]["name"] == "library_of_congress"
        ]

        assert len(ia_artifacts) == 1
        print("PASS: production FOUND source persists one Found Artifact")

        assert len(loc_artifacts) == 0
        print("PASS: production NO_RESULTS source persists zero Found Artifacts")

        artifact = ia_artifacts[0]

        assert artifact["search_ref"]["search_id"] == ia_arrival["search_id"]
        assert artifact["search_ref"]["target_id"] == "ST-EXEC-ARTIFACT"
        assert artifact["search_ref"]["execution_event_id"] == (
            "EVT-EXEC-ARTIFACT-001"
        )
        print("PASS: persisted artifact preserves complete search provenance")

        assert artifact["source"]["name"] == "internet_archive"
        assert artifact["source"]["access_method"] == (
            ia_arrival["source"]["access_method"]
        )
        print("PASS: persisted artifact preserves source provenance")

        assert artifact["person_slots"] == [
            {
                "name": "Joan Greene",
                "role": "NAME_APPEARANCE_ONLY",
            }
        ]
        print("PASS: persisted person remains NAME_APPEARANCE_ONLY")

        forbidden = {
            "claim",
            "evidence",
            "identity",
            "promotion",
            "confidence",
            "rank",
            "score",
            "verified",
            "proven",
            "confirmed",
            "next_test",
            "interpretation",
            "assessment",
            "meaning",
        }

        assert not forbidden.intersection(artifact)
        print("PASS: persisted artifact remains discovery-only")

        print("\n" + "=" * 60)
        print("[PASS] LIVE EXECUTOR -> FOUND ARTIFACT INTEGRATION")
        print("=" * 60)


if __name__ == "__main__":
    main()
