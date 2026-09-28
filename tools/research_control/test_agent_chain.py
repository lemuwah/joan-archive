from pathlib import Path
import json
import tempfile

import agent_chain


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


def test_with_events(label, events, candidate, expected):
    original = agent_chain.EVENT_FILE

    try:
        agent_chain.EVENT_FILE = write_events(events)

        allowed, reason = agent_chain.verify_agent_chain(
            candidate
        )

        if allowed != expected:
            raise SystemExit(
                f"FAIL: {label}: expected {expected}, "
                f"got {allowed} — {reason}"
            )

        result = "ALLOWED" if allowed else "BLOCKED"
        print(f"PASS: {label} -> {result}")
        print(f"      {reason}")

    finally:
        agent_chain.EVENT_FILE = original


LAWS = sorted(agent_chain.SEVEN_LAWS)


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


def main():
    candidate = "CANDIDATE-CHAIN-TEST"

    # Attack 1: labels are missing actual events.
    test_with_events(
        "no agent events",
        [],
        candidate,
        False,
    )

    # Attack 2: all four agents exist, but are not linked.
    test_with_events(
        "unlinked four-agent labels",
        [
            event("E1", "EXPLORER", candidate),
            event("E2", "ARCHIVIST", candidate),
            event("E3", "HOSTILE_REVIEW", candidate),
            event("E4", "SYNTHESIZER", candidate),
        ],
        candidate,
        False,
    )

    # Attack 3: broken parent link.
    test_with_events(
        "broken parent chain",
        [
            event("E1", "EXPLORER", candidate),
            event("E2", "ARCHIVIST", candidate, "WRONG"),
            event("E3", "HOSTILE_REVIEW", candidate, "E2"),
            event("E4", "SYNTHESIZER", candidate, "E3"),
        ],
        candidate,
        False,
    )

    # Attack 4: one agent missing a Law.
    broken_laws = LAWS[:-1]

    events = [
        event("E1", "EXPLORER", candidate),
        event("E2", "ARCHIVIST", candidate, "E1"),
        event("E3", "HOSTILE_REVIEW", candidate, "E2"),
        event("E4", "SYNTHESIZER", candidate, "E3"),
    ]

    events[2]["laws"] = broken_laws

    test_with_events(
        "missing Law in Hostile Review",
        events,
        candidate,
        False,
    )

    # Legitimate complete chain.
    test_with_events(
        "complete four-agent chain",
        [
            event("E1", "EXPLORER", candidate),
            event("E2", "ARCHIVIST", candidate, "E1"),
            event("E3", "HOSTILE_REVIEW", candidate, "E2"),
            event("E4", "SYNTHESIZER", candidate, "E3"),
        ],
        candidate,
        True,
    )

    print("FOUR-AGENT EVIDENCE CHAIN TEST: PASS")


if __name__ == "__main__":
    main()
