from law_guard import check_promotion


def expect(status, evidence_state, expected):
    actual = check_promotion(status, evidence_state)

    if actual != expected:
        raise SystemExit(
            f"REGRESSION FAILURE: {status}/{evidence_state} "
            f"expected {expected}, got {actual}"
        )


def main():
    certainty_statuses = [
        "PROOF",
        "CONFIRMED",
        "VERIFIED",
        "ESTABLISHED",
        "CERTAIN",
        "IDENTIFIED",
        " proof ",
        "Verified",
        "cOnFiRmEd",
    ]

    research_statuses = [
        "LEAD",
        "HYPOTHESIS",
        "UNTESTED",
        "CANDIDATE",
        "CONTRADICTED",
        "SUSPENDED",
    ]

    for status in certainty_statuses:
        expect(status, "AI_WORKING_COPY", False)

    for status in research_statuses:
        expect(status, "AI_WORKING_COPY", True)

    expect("PROOF", "HUMAN_VERIFIED_PRIMARY", True)

    print("REGRESSION TEST: CERTAINTY FIREWALL PASS")
    print("REGRESSION TEST: AI RESEARCH FREEDOM PASS")
    print("REGRESSION TEST: HUMAN PRIMARY PROMOTION PASS")
    print("ALL LAW-GUARD REGRESSION TESTS PASS")


if __name__ == "__main__":
    main()
