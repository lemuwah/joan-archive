#!/usr/bin/env python3

from tools.evidence_pipeline.intake_bridge import (
    AI_DISCLAIMER,
    build_ai_evidence_event,
)


def source():
    return {
        "title": "RI State Archives Land Records No. 1",
        "locator": "folios 259–260",
        "access_method": "DIGITAL_IMAGE",
        "repository": "RI State Archives",
        "collection": "Land Records",
        "page_or_image": "259–260",
    }


def test_ai_evidence_is_allowed_without_human_verification():
    event = build_ai_evidence_event(
        evidence_id="EVID-000901",
        source=source(),
        source_status="PRIMARY_READ",
        literal_observation="AI reports that the instrument names Joane Greene as wife.",
        actor="research-agent",
        platform="AI",
        access_method="DIGITAL_IMAGE",
        finding_id="FINDING-fe55dd3e755e",
    )

    assert event["provenance"]["actor_type"] == "AI"
    assert "FINDING-fe55dd3e755e" in event["provenance"]["session"]
    assert AI_DISCLAIMER in event["provenance"]["session"]


def test_claims_are_not_inherited_from_finding():
    event = build_ai_evidence_event(
        evidence_id="EVID-000902",
        source=source(),
        source_status="PRIMARY_READ",
        literal_observation="Joane Greene is named in the instrument.",
        actor="research-agent",
        platform="AI",
        access_method="DIGITAL_IMAGE",
        finding_id="FINDING-fe55dd3e755e",
    )

    assert event["claim_refs"] == []


def test_interpretation_remains_separate():
    event = build_ai_evidence_event(
        evidence_id="EVID-000903",
        source=source(),
        source_status="PRIMARY_READ",
        literal_observation="The words 'Joane Greene his wife' are reported.",
        actor="research-agent",
        platform="AI",
        access_method="DIGITAL_IMAGE",
        interpretation="This may identify Joan as John's wife at the time of the instrument.",
    )

    assert event["literal_observation"].startswith("The words")
    assert event["interpretation"].startswith("This may identify")


def test_ai_cannot_create_human_verified_evidence():
    try:
        build_ai_evidence_event(
            evidence_id="EVID-000904",
            source=source(),
            source_status="PRIMARY_VERIFIED",
            literal_observation="Joane Greene is named.",
            actor="research-agent",
            platform="AI",
            access_method="DIGITAL_IMAGE",
        )
    except ValueError as exc:
        assert "PRIMARY_VERIFIED" in str(exc)
    else:
        raise AssertionError(
            "AI-first bridge incorrectly allowed PRIMARY_VERIFIED evidence"
        )


def test_ai_work_is_not_claimed_as_human_verification():
    event = build_ai_evidence_event(
        evidence_id="EVID-000905",
        source=source(),
        source_status="PRIMARY_READ",
        literal_observation="No Joan signature or mark is visible in the reviewed image.",
        actor="research-agent",
        platform="AI",
        access_method="DIGITAL_IMAGE",
    )

    assert event["provenance"]["actor_type"] == "AI"
    assert "verification" not in event
    assert "human" not in event["provenance"]["actor"].lower()


if __name__ == "__main__":
    test_ai_evidence_is_allowed_without_human_verification()
    test_claims_are_not_inherited_from_finding()
    test_interpretation_remains_separate()
    test_ai_cannot_create_human_verified_evidence()
    test_ai_work_is_not_claimed_as_human_verification()
    print("AI-FIRST EVIDENCE INTAKE BRIDGE TESTS: PASS")
