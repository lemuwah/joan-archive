from best_hypothesis_gate import (
    check_best_hypothesis,
    promote_best_hypothesis,
    FOUR_AGENTS,
    SEVEN_LAWS,
)


def expect_blocked(label, candidate, agents, laws):
    allowed, reason = check_best_hypothesis(
        candidate,
        agents,
        laws,
    )

    if allowed:
        raise SystemExit(
            f"FAIL: {label} was incorrectly allowed"
        )

    print(f"PASS: {label} blocked — {reason}")


def main():
    # Attack 1: only one agent
    expect_blocked(
        "single-agent promotion",
        "Candidate A",
        ["EXPLORER"],
        SEVEN_LAWS,
    )

    # Attack 2: all agents, but missing Laws
    expect_blocked(
        "missing-Law promotion",
        "Candidate B",
        FOUR_AGENTS,
        [],
    )

    # Attack 3: empty candidate
    expect_blocked(
        "empty candidate",
        "",
        FOUR_AGENTS,
        SEVEN_LAWS,
    )

    # Legitimate Best Hypothesis
    event = promote_best_hypothesis(
        "Candidate C",
        FOUR_AGENTS,
        SEVEN_LAWS,
    )

    if event is None:
        raise SystemExit(
            "FAIL: valid Best Hypothesis was not recorded"
        )

    if event["status"] != "BEST_HYPOTHESIS":
        raise SystemExit(
            "FAIL: valid candidate did not receive "
            "BEST_HYPOTHESIS status"
        )

    if event["event_class"] != "RESEARCH":
        raise SystemExit(
            "FAIL: valid Best Hypothesis was not "
            "classified as RESEARCH"
        )

    if event["result"] != "BEST HYPOTHESIS PROMOTION ALLOWED":
        raise SystemExit(
            "FAIL: unexpected promotion result"
        )

    if "Proof" in event["result"]:
        raise SystemExit(
            "FAIL: Best Hypothesis was conflated with Proof"
        )

    print("PASS: four-agent review required")
    print("PASS: Seven-Law coverage required")
    print("PASS: empty candidates blocked")
    print("PASS: valid candidate becomes BEST_HYPOTHESIS")
    print("PASS: BEST_HYPOTHESIS remains distinct from Proof")
    print("BEST HYPOTHESIS GATE TEST: PASS")


if __name__ == "__main__":
    main()
