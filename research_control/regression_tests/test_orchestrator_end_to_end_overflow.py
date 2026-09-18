#!/usr/bin/env python3
"""End-to-end regression test for lead preservation and ledger isolation."""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.multi_agent_daily import orchestrate


TEST_DATE = "2099-01-01"


def make_sweep_record(index: int) -> dict:
    """Create one synthetic sweep record using the production input shape."""
    critical = index == 250

    return {
        "person_name": (
            "Joan Unknown Greene"
            if critical
            else f"Test Person {index:04d}"
        ),
        "lens": (
            "narragansett_indigenous_context"
            if critical
            else "test_lens"
        ),
        "query": (
            '"Joan Unknown Greene" Narragansett'
            if critical
            else f'"Test Person {index:04d}" test'
        ),
        "results": [
            {
                "title": (
                    "CRITICAL HISTORICAL LEAD — Joan Unknown Greene"
                    if critical
                    else f"Historical lead {index:04d}"
                ),
                "record_id": f"TEST-RECORD-{index:04d}",
                "url": f"https://example.invalid/test/{index:04d}",
            }
        ],
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        sweep_path = tmp / "sweep.jsonl"
        output_root = tmp / "agent_runs"
        role_output = tmp / "role_output"
        target_file = tmp / "SEARCH_TARGETS.yml"
        event_file = tmp / "research_events.jsonl"

        records = [make_sweep_record(i) for i in range(1, 251)]

        sweep_path.write_text(
            "\n".join(json.dumps(record) for record in records) + "\n",
            encoding="utf-8",
        )

        target_file.write_text("targets: []\n", encoding="utf-8")
        event_file.write_text("", encoding="utf-8")

        canonical_target_file = (
            Path(__file__).resolve().parents[2]
            / "research_queue"
            / "SEARCH_TARGETS.yml"
        )
        canonical_event_file = (
            Path(__file__).resolve().parents[2]
            / "research_queue"
            / "research_events.jsonl"
        )

        canonical_target_before = canonical_target_file.read_bytes()
        canonical_event_before = canonical_event_file.read_bytes()

        result = orchestrate.run(
            date=TEST_DATE,
            sweep_path=sweep_path,
            output_root=output_root,
            role_output=role_output,
            target_file=target_file,
            event_file=event_file,
        )

        run_dir = Path(result)
        summary_path = run_dir / "run_summary.json"
        deferred_path = run_dir / "deferred_leads.json"

        if not summary_path.exists():
            raise SystemExit("FAIL: run_summary.json was not created")

        if not deferred_path.exists():
            raise SystemExit("FAIL: deferred_leads.json was not created")

        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        deferred = json.loads(deferred_path.read_text(encoding="utf-8"))

        generated_count = summary.get("search_targets_generated")
        deferred_count = summary.get("leads_deferred")

        print(f"INPUT RECORDS: {len(records)}")
        print(f"OUTPUT DIRECTORY: {run_dir}")
        print(f"SEARCH TARGETS GENERATED: {generated_count}")
        print(f"LEADS DEFERRED: {deferred_count}")

        if generated_count != 100:
            raise SystemExit(
                f"FAIL: expected 100 generated targets, got {generated_count}"
            )

        if deferred_count != 150:
            raise SystemExit(
                f"FAIL: expected 150 deferred leads, got {deferred_count}"
            )

        print("PASS: processing budget remains bounded at 100 targets")

        if len(deferred) != 150:
            raise SystemExit(
                f"FAIL: expected 150 deferred leads, got {len(deferred)}"
            )

        print("PASS: exactly 150 overflow leads were recorded as deferred")

        deferred_ids = {
            lead.get("result", {}).get("record_id")
            for lead in deferred
        }

        expected_ids = {
            f"TEST-RECORD-{index:04d}"
            for index in range(101, 251)
        }

        if deferred_ids != expected_ids:
            missing = sorted(expected_ids - deferred_ids)
            extra = sorted(deferred_ids - expected_ids)
            raise SystemExit(
                f"FAIL: deferred lead set mismatch; missing={missing[:5]} "
                f"extra={extra[:5]}"
            )

        print("PASS: deferred_leads.json preserves every overflow lead")

        critical = next(
            (
                lead
                for lead in deferred
                if lead.get("result", {}).get("record_id")
                == "TEST-RECORD-0250"
            ),
            None,
        )

        if critical is None:
            raise SystemExit(
                "FAIL: critical overflow lead is absent from deferred_leads.json"
            )

        print("PASS: critical overflow lead is preserved in deferred_leads.json")

        if critical.get("preservation_status") != "DEFERRED":
            raise SystemExit(
                "FAIL: critical lead lacks explicit DEFERRED preservation status"
            )

        if not critical.get("preservation_origin_event"):
            raise SystemExit(
                "FAIL: critical deferred lead lacks preservation provenance"
            )

        print(
            "PASS: deferred lead retains explicit preservation status "
            "and origin-event provenance"
        )

        forbidden_statuses = {
            "NO_RESULTS",
            "REJECTED",
            "DISCOUNTED",
            "SUSPENDED",
        }

        if critical.get("status") in forbidden_statuses:
            raise SystemExit(
                "FAIL: deferred lead was represented as a terminal/negative result"
            )

        print("PASS: deferred lead is not represented as a negative or terminal result")

        temp_targets = target_file.read_text(encoding="utf-8")
        temp_events = event_file.read_text(encoding="utf-8")

        import yaml

        target_data = yaml.safe_load(temp_targets) or {}
        temp_target_records = target_data.get("targets", [])

        if len(temp_target_records) != 100:
            raise SystemExit(
                "FAIL: isolated test SEARCH_TARGETS.yml contains "
                f"{len(temp_target_records)} targets; expected 100"
            )

        if not any(
            "example.invalid/test/" in target.get("source_identifier", "")
            for target in temp_target_records
        ):
            raise SystemExit(
                "FAIL: isolated test SEARCH_TARGETS.yml did not receive "
                "the generated synthetic source leads"
            )

        if "NEW_SEARCH_TARGET" not in temp_events:
            raise SystemExit(
                "FAIL: isolated test research_events.jsonl did not receive "
                "search-target events"
            )

        print(
            "PASS: synthetic target and event writes stayed inside "
            "temporary test ledgers"
        )

        canonical_target_after = canonical_target_file.read_bytes()
        canonical_event_after = canonical_event_file.read_bytes()

        if canonical_target_after != canonical_target_before:
            raise SystemExit(
                "FAIL: canonical SEARCH_TARGETS.yml was modified by regression test"
            )

        if canonical_event_after != canonical_event_before:
            raise SystemExit(
                "FAIL: canonical research_events.jsonl was modified by regression test"
            )

        print("PASS: canonical SEARCH_TARGETS.yml remained unchanged")
        print("PASS: canonical research_events.jsonl remained unchanged")

        print()
        print(
            "ORCHESTRATOR END-TO-END LEAD PRESERVATION + "
            "LEDGER ISOLATION REGRESSION TEST: PASS"
        )


if __name__ == "__main__":
    main()
