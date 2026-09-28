from pathlib import Path
import json
import tempfile

import agent_chain
import best_hypothesis_gate


LAWS = sorted(agent_chain.SEVEN_LAWS)
CANDIDATE = "INTEGRATED-GATE-TEST"


def make_event(event_id, agent, target, parent=""):
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


def run_with_events(label, events, expected_status):
    temp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
    )

    for event in events:
        temp.write(json.dumps(event) + "\n")

    temp.close()

    original_chain_file = agent_chain.EVENT_FILE
    original_gate_file = best_hypothesis_gate.verify_agent_chain

    try:
        agent_chain.EVENT_FILE = Path(temp.name)

        result = best_hypothesis_gate.check_best_hypothesis(
            CANDIDATE
        )

        allowed = result[0]

        if allowed != expected_status:
            raise SystemExit(
                f"FAIL: {label}: expected "
                f"{expected_status}, got {allowed} — {result[1]}"
            )

        state = "ALLOWED" if allowed else "BLOCKED"
        print(f"PASS: {label} -> {state}")
        print(f"      {result[1]}")

    finally:
        agent_chain.EVENT_FILE = original_chain_file


def main():
    # 1. No chain.
    run_with_events(
        "no evidence",
        [],
        False,
    )

    # 2. Four agent names, but no chain.
    run_with_events(
        "unlinked agents",
        [
            make_event("E1", "EXPLORER", CANDIDATE),
            make_event("E2", "ARCHIVIST", CANDIDATE),
            make_event("E3", "HOSTILE_REVIEW", CANDIDATE),
            make_event("E4", "SYNTHESIZER", CANDIDATE),
        ],
        False,
    )

    # 3. Proper chain, but Hostile Review missing a Law.
    events = [
        make_event("E1", "EXPLORER", CANDIDATE),
        make_event("E2", "ARCHIVIST", CANDIDATE, "E1"),
        make_event("E3", "HOSTILE_REVIEW", CANDIDATE, "E2"),
        make_event("E4", "SYNTHESIZER", CANDIDATE, "E3"),
    ]

    events[2]["laws"] = LAWS[:-1]

    run_with_events(
        "missing Law",
        events,
        False,
    )

    # 4. Proper chain.
    run_with_events(
        "complete evidence chain",
        [
            make_event("E1", "EXPLORER", CANDIDATE),
            make_event("E2", "ARCHIVIST", CANDIDATE, "E1"),
            make_event("E3", "HOSTILE_REVIEW", CANDIDATE, "E2"),
            make_event("E4", "SYNTHESIZER", CANDIDATE, "E3"),
        ],
        True,
    )

    print("INTEGRATED BEST-HYPOTHESIS GATE TEST: PASS")


if __name__ == "__main__":
    main()
