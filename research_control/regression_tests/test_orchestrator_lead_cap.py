#!/usr/bin/env python3
"""
Adversarial regression test for the orchestrator lead-cap problem.

The orchestrator currently processes:

    leads[:100]

This test places a historically relevant competing lead at position 101.

EXPECTED INITIAL RESULT:
    FAIL

That failure is intentional. It demonstrates that a relevant lead can
be silently excluded from search-target generation solely because 100
other leads appeared first.

The test must NOT modify production code.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "multi_agent_daily"))
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

import orchestrate


CRITICAL_LEAD = "MODEL-B-AFTER-CAP"


def make_lead(index, model_id):
    return {
        "person_name": f"Test Person {index}",
        "lens": "test_lens",
        "query": f"test query {index}",
        "result": {
            "record_id": f"TEST-RECORD-{index}",
            "title": f"Historical lead {index}",
            "url": f"https://example.org/record/{index}",
        },
        "model_id": model_id,
        "model_status": "OPEN",
    }


def main():
    leads = []

    # 100 ordinary leads occupy positions 1–100.
    for index in range(1, 101):
        leads.append(make_lead(index, f"FILLER-{index}"))

    # Critical competing lead is position 101.
    critical = make_lead(101, CRITICAL_LEAD)
    critical["person_name"] = "Joan Unknown Greene"
    critical["lens"] = "narragansett_indigenous_context"
    critical["query"] = (
        '"Joan Unknown Greene" Narragansett '
        'Quidnessett alternative identity test'
    )
    leads.append(critical)

    captured_targets = []

    def capture_target(**kwargs):
        target = {
            "target_id": f"TEST-{len(captured_targets) + 1}",
            **kwargs,
            "status": "READY_SHADOW",
        }
        captured_targets.append(target)
        return target

    original_add_target = orchestrate.add_target
    orchestrate.add_target = capture_target

    try:
        generated = orchestrate.generate_search_targets(
            leads=leads,
            origin_event="TEST-CAP-EVENT",
            laws=[
                "No Narrative Smoothing",
                "Follow the Rivers",
                "No Premature Elimination",
                "No Algorithmic Contamination",
                "No Jurisdictional Assumption",
                "No Centering",
                "No Trust Without Evidence",
            ],
        )

        generated_text = json.dumps(
            generated,
            ensure_ascii=False,
        )

        print(f"INPUT LEADS: {len(leads)}")
        print(f"GENERATED TARGETS: {len(generated)}")

        if CRITICAL_LEAD not in generated_text:
            raise SystemExit(
                "FAIL: relevant lead at position 101 was excluded "
                "from search-target generation"
            )

        print(
            "PASS: lead beyond position 100 reached "
            "search-target generation"
        )

        print()
        print(
            "ORCHESTRATOR LEAD-CAP REGRESSION TEST: PASS"
        )

    finally:
        orchestrate.add_target = original_add_target


if __name__ == "__main__":
    main()
