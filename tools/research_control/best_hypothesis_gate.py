from event_spine import record_event
from agent_chain import verify_agent_chain


SEVEN_LAWS = {
    "No Narrative Smoothing",
    "La Mance Law / Follow the Rivers",
    "No Premature Elimination",
    "No Algorithmic Contamination",
    "No Jurisdictional Assumption",
    "No Centering",
    "No Trust Without Evidence",
}

CERTAINTY_STATUSES = {
    "PROOF",
    "CONFIRMED",
    "VERIFIED",
    "ESTABLISHED",
    "CERTAIN",
    "IDENTIFIED",
}


def check_best_hypothesis(candidate):
    candidate = candidate.strip()

    if not candidate:
        return False, "Candidate is empty"

    allowed, reason = verify_agent_chain(candidate)

    if not allowed:
        return False, reason

    return True, (
        "Candidate completed a real four-agent "
        "Seven-Law evidence chain"
    )


def promote_best_hypothesis(
    candidate,
    parent_event="",
):
    allowed, reason = check_best_hypothesis(candidate)

    if not allowed:
        return record_event(
            agent="BEST_HYPOTHESIS_GATE",
            action="BEST_HYPOTHESIS_ATTEMPT",
            target=candidate,
            laws=sorted(SEVEN_LAWS),
            result="BEST HYPOTHESIS PROMOTION BLOCKED",
            status="BLOCKED",
            contradiction=reason,
            next_action=(
                "Complete a real four-agent "
                "Seven-Law evidence chain."
            ),
            parent_event=parent_event,
        )

    return record_event(
        agent="BEST_HYPOTHESIS_GATE",
        action="BEST_HYPOTHESIS_PROMOTED",
        target=candidate,
        laws=sorted(SEVEN_LAWS),
        result="BEST HYPOTHESIS PROMOTION ALLOWED",
        status="BEST_HYPOTHESIS",
        next_action=(
            "Continue adversarial testing; "
            "Best Hypothesis is not Proof."
        ),
        parent_event=parent_event,
    )
