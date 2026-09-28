from law_guard import check_promotion


def main():
    tests = [
        ("AI_FOUND", "AI_WORKING_COPY", True),
        ("UNTESTED", "AI_WORKING_COPY", True),
        ("PROOF", "AI_WORKING_COPY", False),
        ("PROOF", "HUMAN_VERIFIED_PRIMARY", True),
    ]

    for status, evidence_state, expected in tests:
        actual = check_promotion(status, evidence_state)

        if actual != expected:
            raise SystemExit(
                f"FAIL: {status}/{evidence_state} "
                f"expected {expected}, got {actual}"
            )

        print(
            f"PASS: {status}/{evidence_state} "
            f"-> {'ALLOWED' if actual else 'REJECTED'}"
        )

    print("SEVEN-LAW PROMOTION TEST COMPLETE")


if __name__ == "__main__":
    main()
