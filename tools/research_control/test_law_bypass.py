from law_guard import check_promotion


def main():
    bypass_labels = [
        "CONFIRMED",
        "VERIFIED",
        "ESTABLISHED",
        "CERTAIN",
        "IDENTIFIED",
    ]

    failures = []

    for label in bypass_labels:
        allowed = check_promotion(label, "AI_WORKING_COPY")

        if allowed:
            print(f"LOOPHOLE FOUND: {label} was allowed")
            failures.append(label)
        else:
            print(f"BLOCKED: {label}")

    if failures:
        print(
            f"RESULT: {len(failures)} certainty-label loopholes detected"
        )
        return 1

    print("RESULT: no certainty-label loopholes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
