#!/usr/bin/env python3
"""
Adversarial regression test for the orchestrator no-veto invariant.

This test protects the rule that model/hypothesis status must not
silently suppress a historically relevant research lead.

The test deliberately creates:

    Model A = OPEN
    Model B = ELIMINATED (legacy/model-profile status)

Both models have relevant historical leads.

The test verifies that both leads reach the orchestrator's
search-target generation path.

This is a structural test. It does not decide which hypothesis
is historically correct.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "multi_agent_daily"))
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

import orchestrate


MODEL_A = "MODEL-A-OPEN"
MODEL_B = "MODEL-B-ELIMINATED"

PERSON = "Joan Unknown Greene"


def make_lead(model_id, status):
    return {
        "person_name": PERSON,
        "lens": "identity_disambiguation",
        "query": f'"{PERSON}" test query for {model_id}',
        "result": {
            "source": "internet_archive",
            "record_id": f"TEST-{model_id}",
            "title": f"Historical lead for {model_id}",
            "url": f"https://example.org/{model_id}",
            "description": (
                f"Historical source lead associated with "
                f"{model_id}; model status={status}"
            ),
        },
        "model_id": model_id,
        "model_status": status,
    }


def main():
    leads = [
        make_lead(MODEL_A, "OPEN"),
        make_lead(MODEL_B, "ELIMINATED"),
    ]

    laws = [
        "No Narrative Smoothing",
        "La Mance Law / Follow the Rivers",
        "No Premature Elimination",
        "No Algorithmic Contamination",
        "No Jurisdictional Assumption",
        "No Centering",
        "No Trust Without Evidence",
    ]

    captured_targets = []

    def capture_target(**kwargs):
        target = {
            "target_id": (
                f"TEST-{len(captured_targets) + 1}"
            ),
            **kwargs,
            "status": "READY_SHADOW",
        }
        captured_targets.append(target)
        return target

    original_add_target = orchestrate.add_target
    orchestrate.add_target = capture_target

    try:
        result = orchestrate.generate_search_targets(
            leads=leads,
            origin_event="TEST-ORIGIN-EVENT",
            laws=laws,
        )

        generated = result.get("generated", [])

        if not generated:
            raise SystemExit(
                "FAIL: orchestrator generated no search targets"
            )

        generated_text = json.dumps(
            generated,
            ensure_ascii=False,
        )

        # OPEN model must survive.
        if MODEL_A not in generated_text:
            raise SystemExit(
                "FAIL: OPEN model lead did not reach "
                "search-target generation"
            )

        print(
            "PASS: OPEN model lead reached "
            "search-target generation"
        )

        # Critical invariant:
        # ELIMINATED model status must NOT act as a veto.
        if MODEL_B not in generated_text:
            raise SystemExit(
                "FAIL: ELIMINATED model lead was silently "
                "filtered before search-target generation"
            )

        print(
            "PASS: ELIMINATED model lead also reached "
            "search-target generation"
        )

        # Verify that the competing lead remains identifiable
        # in the generated target rather than being converted
        # into an anonymous/generic target.
        b_targets = [
            target
            for target in generated
            if MODEL_B in json.dumps(
                target,
                ensure_ascii=False,
            )
        ]

        if not b_targets:
            raise SystemExit(
                "FAIL: competing model identity was not "
                "preserved in generated target"
            )

        print(
            "PASS: competing model identity preserved "
            "in generated target"
        )

        # Verify that both remain ordinary research targets.
        for target in generated:
            if target.get("status") != "READY_SHADOW":
                raise SystemExit(
                    "FAIL: generated target did not remain "
                    f"READY_SHADOW: {target}"
                )

        print(
            "PASS: all generated targets remain READY_SHADOW"
        )

        print()
        print(
            "ORCHESTRATOR NO-HYPOTHESIS-VETO "
            "REGRESSION TEST: PASS"
        )

    finally:
        orchestrate.add_target = original_add_target


if __name__ == "__main__":
    main()
