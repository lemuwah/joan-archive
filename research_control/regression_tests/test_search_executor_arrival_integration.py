#!/usr/bin/env python3
"""
Regression test for executor -> per-source search-arrival integration.

Production path under test:

    execute_search_targets.main()
            |
            +--> execute_target()
            |
            +--> SEARCH_TARGET_EXECUTED
            |
            +--> Internet Archive arrival
            |
            +--> Library of Congress arrival

This test uses synthetic source functions and temporary ledgers.
It never writes to production research_events.jsonl or search_events.jsonl.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "research_control"))
sys.path.insert(0, str(ROOT / "research_control" / "tools"))

import execute_search_targets as executor
import record_search_arrivals


LAWS = [
    "No Narrative Smoothing",
    "La Mance Law / Follow the Rivers",
    "No Premature Elimination",
    "No Algorithmic Contamination",
    "No Jurisdictional Assumption",
    "No Centering",
    "No Trust Without Evidence",
]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        targets_file = tmp / "SEARCH_TARGETS.yml"
        result_dir = tmp / "search_results"
        event_file = tmp / "research_events.jsonl"
        search_ledger = tmp / "search_events.jsonl"

        targets_file.write_text(
            """
targets:
  - target_id: ST-EXEC-ARRIVAL
    question: Find records related to Joan Unknown Greene.
    reason: Synthetic executor-arrival regression.
    origin_event: EVT-SYNTHETIC-PARENT
    target_type: DOCUMENT
    person_slots:
      - Joan Unknown Greene
    jurisdictions:
      - Rhode Island
    record_families:
      - land
    date_range:
      start: 1600
      end: 1800
    name_variants:
      - Joan Unknown Greene
      - Joan Greene
    laws:
      - No Narrative Smoothing
      - La Mance Law / Follow the Rivers
      - No Premature Elimination
      - No Algorithmic Contamination
      - No Jurisdictional Assumption
      - No Centering
      - No Trust Without Evidence
    disproof_record: Synthetic regression only.
    status: READY
""",
            encoding="utf-8",
        )

        # Synthetic source behavior:
        # IA returns a result; LOC returns no result.
        def fake_ia(session, query, rows):
            return [
                {
                    "source": "internet_archive",
                    "record_id": "SYNTH-IA-001",
                    "title": "Synthetic IA result",
                }
            ]

        def fake_loc(session, query, rows):
            return []

        def fake_record_event(**kwargs):
            event = {
                "event_id": "EVT-EXEC-ARRIVAL-001",
                "timestamp": "2026-09-19T14:00:00+00:00",
                **kwargs,
            }

            event_file.parent.mkdir(parents=True, exist_ok=True)
            with event_file.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event) + "\n")

            return event

        original_ia = executor.ia_search
        original_loc = executor.loc_search
        original_target_file = executor.TARGET_FILE
        original_result_dir = executor.RESULT_DIR
        original_record_event = executor.record_event
        original_arrival_ledger = record_search_arrivals.SEARCH_LEDGER

        try:
            executor.ia_search = fake_ia
            executor.loc_search = fake_loc
            executor.TARGET_FILE = targets_file
            executor.RESULT_DIR = result_dir
            executor.record_event = fake_record_event
            record_search_arrivals.SEARCH_LEDGER = search_ledger

            sys.argv = [
                "execute_search_targets.py",
                "--target",
                "ST-EXEC-ARRIVAL",
                "--delay",
                "0",
            ]

            executor.main()

        finally:
            executor.ia_search = original_ia
            executor.loc_search = original_loc
            executor.TARGET_FILE = original_target_file
            executor.RESULT_DIR = original_result_dir
            executor.record_event = original_record_event
            record_search_arrivals.SEARCH_LEDGER = original_arrival_ledger

        # ------------------------------------------------------------
        # A. Executor produced its normal result artifact.
        # ------------------------------------------------------------
        result_path = result_dir / "ST-EXEC-ARRIVAL.json"
        assert result_path.exists(), "Executor result artifact was not written"

        result = json.loads(result_path.read_text(encoding="utf-8"))

        assert result["result_status"] == "FOUND"
        assert set(result["source_results"]) == {
            "internet_archive",
            "library_of_congress",
        }

        print("PASS: executor completed synthetic target execution")

        # ------------------------------------------------------------
        # B. Execution event exists and is attached to artifact.
        # ------------------------------------------------------------
        assert result["event_id"] == "EVT-EXEC-ARRIVAL-001"

        events = read_jsonl(event_file)
        assert len(events) == 1
        assert events[0]["action"] == "SEARCH_TARGET_EXECUTED"

        print("PASS: SEARCH_TARGET_EXECUTED event is attached")

        # ------------------------------------------------------------
        # C. Both source arrivals were actually recorded.
        # ------------------------------------------------------------
        arrivals = read_jsonl(search_ledger)

        assert len(arrivals) == 2, (
            f"Expected 2 source arrivals; got {len(arrivals)}"
        )

        by_source = {record["source"]["name"]: record for record in arrivals}

        assert set(by_source) == {
            "internet_archive",
            "library_of_congress",
        }

        print("PASS: executor recorded one arrival per source")

        # ------------------------------------------------------------
        # D. Source outcomes remain independent.
        # ------------------------------------------------------------
        assert (
            by_source["internet_archive"]["result"]["outcome"]
            == "RESULT_LOCATED"
        )
        assert by_source["internet_archive"]["visibility"] == "POSITIVE"

        assert (
            by_source["library_of_congress"]["result"]["outcome"]
            == "NO_RESULT_LOCATED"
        )
        assert by_source["library_of_congress"]["visibility"] == "NEGATIVE"

        print("PASS: source outcomes remain independently classified")

        # ------------------------------------------------------------
        # E. Arrival provenance points back to the executor.
        # ------------------------------------------------------------
        for arrival in arrivals:
            assert arrival["provenance"]["actor_type"] == "SYSTEM"
            assert arrival["provenance"]["actor"] == "SEARCH_EXECUTOR"
            assert arrival["provenance"]["session"] == "ST-EXEC-ARRIVAL"
            assert arrival["result"]["artifact_ref"].endswith(
                "ST-EXEC-ARRIVAL.json"
            )

        print("PASS: arrivals preserve executor provenance")

        # ------------------------------------------------------------
        # F. Arrivals remain research activity, never proof.
        # ------------------------------------------------------------
        import re

        arrival_text = json.dumps(arrivals, ensure_ascii=False)

        assert "PROOF" not in arrival_text
        assert re.search(r"\bproven\b", arrival_text.lower()) is None
        assert "historical proof" in arrival_text

        print("PASS: arrivals remain research-only")

        # ------------------------------------------------------------
        # G. No production search ledger was touched.
        # ------------------------------------------------------------
        production_ledger = ROOT / "research_control" / "search_events.jsonl"

        assert not production_ledger.exists() or (
            production_ledger.read_text(encoding="utf-8").strip() == ""
        )

        print("PASS: production search ledger remains untouched")

        print("SEARCH EXECUTOR ARRIVAL INTEGRATION: PASS")


if __name__ == "__main__":
    main()
