#!/usr/bin/env python3
"""
Regression test for automatic search-result breadcrumb routing.

Desired chain:

    SEARCH_TARGET_EXECUTED
            ↓
      search result
            ↓
      breadcrumb lead
            ↓
      child search target

The router must preserve ancestry, source identity, and research-only
status. It must not turn search output into proof.
"""

import json
import tempfile
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

import event_spine
import search_targets

# This import is intentionally the new production seam.
# It should fail until the router is implemented.
from route_search_results import route_search_result


LAWS = [
    "No Narrative Smoothing",
    "La Mance Law / Follow the Rivers",
    "No Premature Elimination",
    "No Algorithmic Contamination",
    "No Jurisdictional Assumption",
    "No Centering",
    "No Trust Without Evidence",
]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        event_file = tmp / "events.jsonl"
        target_file = tmp / "targets.yml"

        target_file.write_text(
            "targets: []\n",
            encoding="utf-8",
        )

        # ------------------------------------------------------------
        # A. Simulate the execution event.
        # ------------------------------------------------------------
        execution_event = event_spine.record_event(
            agent="SEARCH_EXECUTOR",
            action="SEARCH_TARGET_EXECUTED",
            target="ST-TARGET-A",
            laws=LAWS,
            search_scope={
                "query": '"Joan Unknown Greene" "synthetic breadcrumb"',
                "sources": ["internet_archive"],
            },
            evidence="synthetic-result.json",
            result="FOUND",
            status="EXECUTED",
            contradiction="Synthetic regression test only.",
            next_action="Route captured search leads.",
            parent_event="EVT-PARENT-A",
            event_class="RESEARCH",
            event_file=event_file,
        )

        execution_id = execution_event["event_id"]

        # ------------------------------------------------------------
        # B. Simulate the result artifact written by the executor.
        # ------------------------------------------------------------
        result = {
            "target_id": "ST-TARGET-A",
            "question": "Find records related to Joan Unknown Greene.",
            "target_status": "READY",
            "execution_status": "EXECUTED",
            "query": '"Joan Unknown Greene" "synthetic breadcrumb"',
            "results": [
                {
                    "source": "internet_archive",
                    "record_id": "BREADCRUMB-001",
                    "title": "Synthetic newly discovered record",
                    "creator": "Synthetic Creator",
                    "date": "1682",
                    "url": "https://example.invalid/BREADCRUMB-001",
                    "description": "Synthetic breadcrumb.",
                }
            ],
            "errors": [],
            "result_status": "FOUND",
            "event_id": execution_id,
            "note": (
                "Search output is a source lead only. It does not establish "
                "historical proof, identity, or certainty."
            ),
        }

        # ------------------------------------------------------------
        # C. The source target that generated the result.
        #
        # In production this metadata already exists in SEARCH_TARGETS.yml.
        # ------------------------------------------------------------
        source_target = {
            "target_id": "ST-TARGET-A",
            "question": "Find records related to Joan Unknown Greene.",
            "reason": "Synthetic regression target.",
            "origin_event": "EVT-PARENT-A",
            "target_type": "DOCUMENT",
            "person_slots": ["Joan Unknown Greene"],
            "jurisdictions": ["Rhode Island"],
            "record_families": ["land"],
            "date_range": {},
            "name_variants": ["Joan Unknown Greene"],
            "laws": LAWS,
            "disproof_record": "Synthetic only.",
            "status": "READY",
        }

        # ------------------------------------------------------------
        # D. THIS is the behavior currently missing.
        #
        # route_search_result() must:
        #   1. recognize the result as a research lead,
        #   2. create a child target,
        #   3. use the execution event as ancestry,
        #   4. preserve the source identifier,
        #   5. leave the child READY_SHADOW.
        # ------------------------------------------------------------
        routed = route_search_result(
            result=result,
            source_target=source_target,
            target_file=target_file,
            event_file=event_file,
        )

        generated = routed["generated"]

        if len(generated) != 1:
            raise AssertionError(
                f"Expected one child target; got {len(generated)}"
            )

        child = generated[0]

        # ------------------------------------------------------------
        # E. Ancestry must point to the execution event.
        # ------------------------------------------------------------
        assert child["origin_event"] == execution_id, (
            "Child target lost execution ancestry: "
            f"{child['origin_event']!r} != {execution_id!r}"
        )

        print("PASS: child target inherits execution event ancestry")

        # ------------------------------------------------------------
        # F. Source identity must survive.
        # ------------------------------------------------------------
        assert (
            child["source_identifier"]
            == "https://example.invalid/BREADCRUMB-001"
        )

        print("PASS: breadcrumb source identifier is preserved")

        # ------------------------------------------------------------
        # G. Child remains human-gated.
        # ------------------------------------------------------------
        assert child["status"] == "READY_SHADOW"

        print("PASS: breadcrumb child target remains READY_SHADOW")

        # ------------------------------------------------------------
        # H. Search result remains research lead, not proof.
        # ------------------------------------------------------------
        result_text = json.dumps(result, ensure_ascii=False)

        assert "PROOF" not in result_text
        assert "source lead only" in result["note"]

        print("PASS: search result remains source-lead-only")

        # ------------------------------------------------------------
        # I. NO_RESULTS must produce no child target.
        # ------------------------------------------------------------
        no_result = {
            **result,
            "results": [],
            "result_status": "NO_RESULTS",
            "event_id": execution_id + "-NORESULT",
        }

        no_result_routed = route_search_result(
            result=no_result,
            source_target=source_target,
            target_file=target_file,
            event_file=event_file,
        )

        assert no_result_routed["generated"] == []

        print("PASS: NO_RESULTS produces no fabricated child target")

        print("SEARCH-RESULT BREADCRUMB ROUTING REGRESSION TEST: PASS")


if __name__ == "__main__":
    main()
