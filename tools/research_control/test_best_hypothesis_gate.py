import json
import tempfile
from pathlib import Path

import agent_chain
import best_hypothesis_gate


LAWS = sorted(agent_chain.SEVEN_LAWS)


def write_events(events):
    temp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
    )

    for event in events:
        temp.write(
            json.dumps(
                event,
                ensure_ascii=False,
            )
            + "\n"
        )

    temp.close()
    return Path(temp.name)


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


def with_events(events, function):
    original = agent_chain.EVENT_FILE

    try:
        agent_chain.EVENT_FILE = write_events(events)
        return function()

    finally:
        agent_chain.EVENT_FILE = original


def expect_blocked(label, events, candidate):
    allowed, reason = with_events(
        events,
        lambda: best_hypothesis_gate.check_best_hypothesis(
            candidate
        ),
    )

    if allowed:
        raise SystemExit(
            f"FAIL: {label} was incorrectly allowed"
        )

    print(f"PASS: {label} blocked — {reason}")


def main():
    candidate = "CANDIDATE-BEST-HYPOTHESIS-TEST"

    # Attack 1: no actual Event Spine evidence.
    expect_blocked(
        "no Event Spine evidence",
        [],
        candidate,
    )

    # Attack 2: only one agent actually recorded.
    expect_blocked(
        "single-agent chain",
        [
            event("E1", "EXPLORER", candidate),
        ],
        candidate,
    )

    # Attack 3: all four agents exist, but are not linked.
    expect_blocked(
        "unlinked four-agent chain",
        [
            event("E1", "EXPLORER", candidate),
            event("E2", "ARCHIVIST", candidate),
            event("E3", "HOSTILE_REVIEW", candidate),
            event("E4", "SYNTHESIZER", candidate),
        ],
        candidate,
    )

    # Attack 4: all four agents are present, but Hostile Review
    # is missing one of the Seven Laws.
    broken_laws = LAWS[:-1]

    events = [
        event("E1", "EXPLORER", candidate),
        event("E2", "ARCHIVIST", candidate, "E1"),
        event("E3", "HOSTILE_REVIEW", candidate, "E2"),
        event("E4", "SYNTHESIZER", candidate, "E3"),
    ]

    events[2]["laws"] = broken_laws

    expect_blocked(
        "missing Law in Hostile Review",
        events,
        candidate,
    )

    # Legitimate complete chain.
    complete_chain = [
        event("E1", "EXPLORER", candidate),
        event("E2", "ARCHIVIST", candidate, "E1"),
        event("E3", "HOSTILE_REVIEW", candidate, "E2"),
        event("E4", "SYNTHESIZER", candidate, "E3"),
    ]

    allowed, reason = with_events(
        complete_chain,
        lambda: best_hypothesis_gate.check_best_hypothesis(
            candidate
        ),
    )

    if not allowed:
        raise SystemExit(
            f"FAIL: complete chain was blocked — {reason}"
        )

    print("PASS: complete four-agent Seven-Law chain allowed")
    print(f"      {reason}")

    # Promotion must use the same real chain.
    promotion_event = with_events(
        complete_chain,
        lambda: best_hypothesis_gate.promote_best_hypothesis(
            candidate
        ),
    )

    if promotion_event is None:
        raise SystemExit(
            "FAIL: valid Best Hypothesis was not recorded"
        )

    if promotion_event["status"] != "BEST_HYPOTHESIS":
        raise SystemExit(
            "FAIL: valid candidate did not receive "
            "BEST_HYPOTHESIS status"
        )

    if promotion_event["event_class"] != "RESEARCH":
        raise SystemExit(
            "FAIL: valid Best Hypothesis was not "
            "classified as RESEARCH"
        )

    if promotion_event["result"] != (
        "BEST HYPOTHESIS PROMOTION ALLOWED"
    ):
        raise SystemExit(
            "FAIL: unexpected promotion result"
        )

    if promotion_event["status"] == "PROOF":
        raise SystemExit(
            "FAIL: Best Hypothesis was conflated with Proof"
        )

    expected_next_action = (
        "Continue adversarial testing; "
        "Best Hypothesis is not Proof."
    )

    if promotion_event["next_action"] != expected_next_action:
        raise SystemExit(
            "FAIL: Best Hypothesis was not explicitly "
            "kept distinct from Proof"
        )

    print("PASS: four-agent review required")
    print("PASS: Seven-Law coverage required")
    print("PASS: unlinked chains blocked")
    print("PASS: complete chain allowed")
    print("PASS: valid candidate becomes BEST_HYPOTHESIS")
    print("PASS: BEST_HYPOTHESIS remains distinct from Proof")
    print("BEST HYPOTHESIS GATE TEST: PASS")


if __name__ == "__main__":
    main()
