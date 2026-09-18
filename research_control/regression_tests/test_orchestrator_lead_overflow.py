#!/usr/bin/env python3
"""
Adversarial regression test for lead-overflow preservation.

Resource limits may batch or delay research, but they must not silently
erase eligible research leads.

This test creates 250 distinct leads.

It checks whether leads beyond the current 100-target processing boundary
remain represented somewhere in the generated research state.

EXPECTED INITIAL RESULT:
    FAIL

That failure is intentional. It establishes whether the current
orchestrator has an overflow/preservation mechanism.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "multi_agent_daily"))
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

import orchestrate


TOTAL_LEADS = 250
CAP = 100


def make_lead(index):
    return {
        "person_name": f"Test Person {index}",
        "lens": (
            "narragansett_indigenous_context"
            if index == 250
            else "test_lens"
        ),
        "query": f"historical test query {index}",
        "result": {
            "record_id": f"TEST-RECORD-{index}",
            "title": f"Historical lead {index}",
            "url": f"https://example.org/record/{index}",
        },
        "model_id": (
            "MODEL-CRITICAL-OVERFLOW"
            if index == 250
            else f"MODEL-{index}"
        ),
        "model_status": "OPEN",
    }


def main():
    leads = [make_lead(index) for index in range(1, TOTAL_LEADS + 1)]

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
            origin_event="TEST-OVERFLOW-EVENT",
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
        print(f"EXPECTED TOTAL LEADS PRESERVED: {TOTAL_LEADS}")

        # First establish whether all leads became targets.
        if len(generated) == TOTAL_LEADS:
            print(
                "PASS: all leads became explicit search targets"
            )
            print()
            print(
                "ORCHESTRATOR LEAD OVERFLOW "
                "REGRESSION TEST: PASS"
            )
            return

        print(
            f"INFO: only {len(generated)} of {TOTAL_LEADS} "
            "leads became targets"
        )

        # If not all leads became targets, the overflow lead must at
        # least remain explicitly represented in the returned state.
        if "MODEL-CRITICAL-OVERFLOW" not in generated_text:
            raise SystemExit(
                "FAIL: overflow lead was neither converted to a target "
                "nor preserved in generated research state"
            )

        print(
            "PASS: overflow lead remains explicitly represented "
            "despite not being processed in the current target batch"
        )

        print()
        print(
            "ORCHESTRATOR LEAD OVERFLOW "
            "REGRESSION TEST: PASS"
        )

    finally:
        orchestrate.add_target = original_add_target


if __name__ == "__main__":
    main()
