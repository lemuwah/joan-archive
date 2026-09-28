#!/usr/bin/env python3
"""
Regression test for autonomous research lead preservation.

Invariant:
A bounded processing budget may limit how many discovered leads are
processed into search targets, but it must NOT erase discovered leads
from the resulting research state.

Expected contract:

    generate_search_targets(...)
        -> {
            "generated": [...],
            "deferred": [...]
        }

Generated leads become search targets.
Deferred leads remain preserved research leads and have not been searched.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR_DIR = ROOT / "tools" / "multi_agent_daily"

if str(ORCHESTRATOR_DIR) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATOR_DIR))

import orchestrate


def make_lead(index: int) -> dict:
    return {
        "person_name": f"Test Person {index}",
        "lens": "test_lens",
        "query": f"historical test query {index}",
        "url": f"https://example.org/lead-{index}",
        "record_id": f"TEST-RECORD-{index:04d}",
        "title": f"Historical lead {index}",
        "result_status": "FOUND",
        "model_status": "OPEN",
    }


def main() -> None:
    leads = [make_lead(index) for index in range(1, 251)]

    critical_lead = leads[-1]
    captured_targets = []

    original_add_target = orchestrate.add_target

    def capture_target(*args, **kwargs):
        target = {
            "question": kwargs.get("question", args[0] if args else ""),
            "reason": kwargs.get("reason", args[1] if len(args) > 1 else ""),
            "target_type": kwargs.get("target_type", "DOCUMENT"),
            "person_slots": kwargs.get("person_slots", []),
            "jurisdictions": kwargs.get("jurisdictions", []),
            "record_families": kwargs.get("record_families", []),
            "date_range": kwargs.get("date_range", {}),
            "name_variants": kwargs.get("name_variants", []),
            "source_identifier": kwargs.get("source_identifier", ""),
            "status": "READY_SHADOW",
        }

        captured_targets.append(target)
        return target

    try:
        orchestrate.add_target = capture_target

        result = orchestrate.generate_search_targets(
            leads=leads,
            origin_event="EVT-TEST-PRESERVATION",
            laws=["Seven Laws"],
        )

    finally:
        orchestrate.add_target = original_add_target

    print(f"INPUT LEADS: {len(leads)}")
    print(f"GENERATED TARGETS OBSERVED: {len(captured_targets)}")
    print(f"CRITICAL LEAD: {critical_lead['record_id']}")

    # The production function must expose both sides of the bounded
    # processing decision.
    if not isinstance(result, dict):
        print("FAIL: generate_search_targets did not return a structured result")
        raise SystemExit(1)

    if "generated" not in result:
        print("FAIL: structured result missing 'generated'")
        raise SystemExit(1)

    if "deferred" not in result:
        print("FAIL: structured result missing 'deferred'")
        raise SystemExit(1)

    generated = result["generated"]
    deferred = result["deferred"]

    print(f"GENERATED TARGETS RETURNED: {len(generated)}")
    print(f"DEFERRED LEADS RETURNED: {len(deferred)}")

    if len(generated) != 100:
        print(
            "FAIL: bounded processing budget changed; "
            f"expected 100 generated targets, got {len(generated)}"
        )
        raise SystemExit(1)

    print("PASS: processing budget remains bounded at 100 targets")

    generated_source_ids = {
        target.get("source_identifier")
        for target in generated
        if isinstance(target, dict)
    }

    deferred_record_ids = {
        lead.get("record_id")
        for lead in deferred
        if isinstance(lead, dict)
    }

    expected_deferred_ids = {
        lead["record_id"] for lead in leads[100:]
    }

    if critical_lead["url"] in generated_source_ids:
        print("PASS: critical lead was processed into a target")
    elif critical_lead["record_id"] in deferred_record_ids:
        print("PASS: critical overflow lead preserved as deferred")
    else:
        print(
            "FAIL: critical overflow lead was neither processed "
            "nor preserved"
        )
        raise SystemExit(1)

    missing = expected_deferred_ids - deferred_record_ids

    if missing:
        sample = sorted(missing)[:5]
        print(
            "FAIL: overflow leads disappeared from research state; "
            f"missing={len(missing)}, sample={sample}"
        )
        raise SystemExit(1)

    print("PASS: all overflow leads preserved")

    # Preservation must not masquerade as a search result or rejection.
    forbidden_statuses = {
        "REJECTED",
        "DISMISSED",
        "ELIMINATED",
        "KILLED",
        "NO_RESULTS",
        "NEGATIVE",
        "EXECUTED",
    }

    for lead in deferred:
        if not isinstance(lead, dict):
            print("FAIL: deferred entry is not a structured lead")
            raise SystemExit(1)

        status = str(lead.get("status", "")).upper()

        if status in forbidden_statuses:
            print(
                "FAIL: deferred lead incorrectly carries terminal/"
                f"negative status: {status}"
            )
            raise SystemExit(1)

    print("PASS: deferred leads are not represented as negative results")

    print()
    print("ORCHESTRATOR LEAD PRESERVATION REGRESSION TEST: PASS")


if __name__ == "__main__":
    main()
