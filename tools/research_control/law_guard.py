from event_spine import record_event


CERTAINTY_STATUSES = {
    "PROOF",
    "CONFIRMED",
    "VERIFIED",
    "ESTABLISHED",
    "CERTAIN",
    "IDENTIFIED",
}


def check_promotion(status, evidence_state):
    normalized_status = status.strip().upper()

    if (
        normalized_status in CERTAINTY_STATUSES
        and evidence_state != "HUMAN_VERIFIED_PRIMARY"
    ):
        return False

    return True


def guard_promotion(
    agent,
    status,
    evidence_state,
    target="",
    parent_event="",
):
    allowed = check_promotion(status, evidence_state)

    if not allowed:
        return record_event(
            agent=agent,
            action="PROMOTION_ATTEMPT",
            target=target,
            laws=[
                "No Trust Without Evidence",
                "No Algorithmic Contamination",
            ],
            evidence=evidence_state,
            result="CERTAINTY PROMOTION BLOCKED",
            status="BLOCKED",
            contradiction=(
                f"{status} cannot be promoted "
                f"from {evidence_state}"
            ),
            next_action=(
                "Continue investigation; "
                "do not promote to certainty."
            ),
            parent_event=parent_event,
            event_class="LAW_VIOLATION",
        )

    return None
