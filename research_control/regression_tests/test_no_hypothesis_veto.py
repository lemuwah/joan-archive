#!/usr/bin/env python3
"""
Regression test for the no-hypothesis-veto invariant.

This test protects a core research-control rule:

    A Best Hypothesis must not silently eliminate, suppress,
    or make unsearchable a competing hypothesis.

A hypothesis that is not promotable as Best Hypothesis may
still be a valid research target.

This test deliberately exercises the real orchestrator
search-target generation path rather than calling add_target()
directly.

This is a structural test. It does not decide which historical
hypothesis is true.
"""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Make the existing research-control modules importable
# without changing production package structure.
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

# Make the multi-agent orchestrator importable.
sys.path.insert(0, str(ROOT / "tools" / "multi_agent_daily"))

import agent_chain
import best_hypothesis_gate
import event_spine
import orchestrate
import search_targets


LAWS = sorted(agent_chain.SEVEN_LAWS)

HYPOTHESIS_A = "HYPOTHESIS-A-CURRENT-BEST"
HYPOTHESIS_B = "HYPOTHESIS-B-COMPETING-ALTERNATIVE"


def event(event_id, agent, target, parent=""):
    return {
        "event_id": event_id,
        "timestamp": "2026-01-01T00:00:00+00:00",
        "event_class": "RESEARCH",
        "agent": agent,
        "action": "TEST_AGENT_WORK",
        "target": target,
        "laws": LAWS,
        "status": "TESTED",
        "parent_event": parent,
    }


def write_events(events):
    temp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
    )

    for item in events:
        temp.write(json.dumps(item) + "\n")

    temp.close()
    return Path(temp.name)


def lead(person_name, lens, record_id, title, query):
    """Build a lead in the exact shape consumed by the orchestrator."""
    return {
        "person_name": person_name,
        "lens": lens,
        "query": query,
        "status": "FOUND",
        "result": {
            "record_id": record_id,
            "title": title,
        },
    }


def main():
    complete_a = [
        event("A1", "EXPLORER", HYPOTHESIS_A),
        event("A2", "ARCHIVIST", HYPOTHESIS_A, "A1"),
        event("A3", "HOSTILE_REVIEW", HYPOTHESIS_A, "A2"),
        event("A4", "SYNTHESIZER", HYPOTHESIS_A, "A3"),
    ]

    # B deliberately has an incomplete chain.
    # It therefore cannot become Best Hypothesis,
    # but that must not make it unsearchable.
    incomplete_b = [
        event("B1", "EXPLORER", HYPOTHESIS_B),
    ]

    all_events = complete_a + incomplete_b
    event_file = write_events(all_events)

    original_agent_event_file = agent_chain.EVENT_FILE
    original_spine_event_file = event_spine.EVENT_FILE
    original_orchestrate_add_target = orchestrate.add_target

    temp_targets = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
        suffix=".yml",
    )
    temp_targets.write("targets: []\n")
    temp_targets.close()

    try:
        agent_chain.EVENT_FILE = event_file
        event_spine.EVENT_FILE = event_file
        search_targets.TARGET_FILE = Path(temp_targets.name)

        # Keep the orchestrator's imported add_target function pointed
        # at the same production implementation while allowing the
        # actual generate_search_targets() path to be exercised.
        orchestrate.add_target = search_targets.add_target

        # ------------------------------------------------------------
        # 1. A is independently promotable as Best Hypothesis.
        # ------------------------------------------------------------
        allowed_a, reason_a = (
            best_hypothesis_gate.check_best_hypothesis(
                HYPOTHESIS_A
            )
        )

        if not allowed_a:
            raise SystemExit(
                "FAIL: current Best Hypothesis candidate A "
                f"was unexpectedly blocked — {reason_a}"
            )

        promotion = (
            best_hypothesis_gate.promote_best_hypothesis(
                HYPOTHESIS_A
            )
        )

        if promotion.get("status") != "BEST_HYPOTHESIS":
            raise SystemExit(
                "FAIL: candidate A did not receive "
                "BEST_HYPOTHESIS status"
            )

        print("PASS: candidate A can become BEST_HYPOTHESIS")

        # ------------------------------------------------------------
        # 2. B is deliberately not promotable.
        # ------------------------------------------------------------
        allowed_b, reason_b = (
            best_hypothesis_gate.check_best_hypothesis(
                HYPOTHESIS_B
            )
        )

        if allowed_b:
            raise SystemExit(
                "FAIL: incomplete competing hypothesis B "
                "was incorrectly promotable"
            )

        print(
            "PASS: competing candidate B remains non-promotable "
            f"without being promoted — {reason_b}"
        )

        # ------------------------------------------------------------
        # 3. Build actual orchestrator-style discovery leads.
        #
        # Both A and B enter discovery. B is not granted any
        # evidentiary status merely because it is preserved.
        # ------------------------------------------------------------
        lead_a = lead(
            person_name="Joan Unknown Greene",
            lens="identity_disambiguation",
            record_id="TEST-HYPOTHESIS-A",
            title=HYPOTHESIS_A,
            query="test competing hypothesis A",
        )

        lead_b = lead(
            person_name="Joan Unknown Greene",
            lens="identity_disambiguation",
            record_id="TEST-HYPOTHESIS-B",
            title=HYPOTHESIS_B,
            query="test competing hypothesis B",
        )

        discoveries = [lead_a, lead_b]

        # Preserve the exact discovery identity before processing.
        original_b_identity = (
            discoveries[1]["person_name"],
            discoveries[1]["lens"],
            discoveries[1]["result"]["record_id"],
            discoveries[1]["result"]["title"],
            discoveries[1]["query"],
        )

        # ------------------------------------------------------------
        # 4. Exercise the REAL orchestrator target-generation path.
        #
        # This is the critical architectural test:
        # Best Hypothesis promotion happens separately, then BOTH
        # discoveries are sent through generate_search_targets().
        # ------------------------------------------------------------
        target_result = orchestrate.generate_search_targets(
            leads=discoveries,
            origin_event=promotion["event_id"],
            laws=LAWS,
            target_file=Path(temp_targets.name),
            event_file=event_file,
        )

        generated = target_result["generated"]
        deferred = target_result["deferred"]

        if len(generated) != 2:
            raise SystemExit(
                "FAIL: both competing discoveries did not reach "
                "the real search-target generation path — "
                f"generated={len(generated)}"
            )

        if deferred:
            raise SystemExit(
                "FAIL: competing discoveries were unexpectedly "
                f"deferred — deferred={len(deferred)}"
            )

        print(
            "PASS: both Best-Hypothesis and competing discoveries "
            "reach the real search-target generation path"
        )

        # ------------------------------------------------------------
        # 5. Verify B remains an ordinary research target.
        # ------------------------------------------------------------
        generated_by_id = {
            target.get("source_identifier"): target
            for target in generated
        }

        target_b = generated_by_id.get("TEST-HYPOTHESIS-B")

        if target_b is None:
            raise SystemExit(
                "FAIL: competing hypothesis B disappeared from "
                "search-target generation"
            )

        if target_b.get("status") != "READY_SHADOW":
            raise SystemExit(
                "FAIL: competing hypothesis B was not preserved "
                "as READY_SHADOW — "
                f"status={target_b.get('status')!r}"
            )

        target_b_text = json.dumps(
            target_b,
            ensure_ascii=False,
        )

        if HYPOTHESIS_B not in target_b_text:
            raise SystemExit(
                "FAIL: competing hypothesis B identity was "
                "not preserved in the generated research target"
            )

        print(
            "PASS: competing hypothesis B remains "
            "research-eligible after A becomes Best Hypothesis"
        )

        # ------------------------------------------------------------
        # 6. Verify A's promotion did not mutate B's discovery identity.
        # ------------------------------------------------------------
        current_b_identity = (
            lead_b["person_name"],
            lead_b["lens"],
            lead_b["result"]["record_id"],
            lead_b["result"]["title"],
            lead_b["query"],
        )

        if current_b_identity != original_b_identity:
            raise SystemExit(
                "FAIL: Best Hypothesis promotion or target "
                "generation mutated competing hypothesis B"
            )

        print(
            "PASS: Best Hypothesis promotion does not mutate "
            "the competing discovery"
        )

        # ------------------------------------------------------------
        # 7. Verify B was not silently assigned a terminal status.
        # ------------------------------------------------------------
        forbidden_statuses = {
            "REJECTED",
            "DISCOUNTED",
            "SUSPENDED",
            "DISMISSED",
            "ELIMINATED",
            "KILLED",
            "NO_RESULTS",
            "NEGATIVE",
            "EXECUTED",
        }

        if target_b.get("status") in forbidden_statuses:
            raise SystemExit(
                "FAIL: competing hypothesis B was silently converted "
                f"to a terminal/negative status — {target_b.get('status')}"
            )

        print(
            "PASS: Best Hypothesis promotion does not automatically "
            "reject, eliminate, or negatively classify competing research"
        )

        print(
            "NO-HYPOTHESIS-VETO REGRESSION TEST: PASS"
        )

    finally:
        agent_chain.EVENT_FILE = original_agent_event_file
        event_spine.EVENT_FILE = original_spine_event_file
        orchestrate.add_target = original_orchestrate_add_target


if __name__ == "__main__":
    main()
