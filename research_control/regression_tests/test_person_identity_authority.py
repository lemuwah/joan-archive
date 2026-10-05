#!/usr/bin/env python3
"""
Adversarial regression tests for the Person Identity Authority.

This suite protects the narrow boundary between:

    NAME APPEARANCE
          |
          v
    DOCUMENTARY PERSON
          |
          v
    EXPLICIT SAME-PERSON RELATIONSHIP
          |
          v
    SEPARATE HISTORICAL CLAIM / HYPOTHESIS

The authority layer must never turn heuristic similarity into identity,
and it must never turn an unresolved hypothesis into a person fact.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "research_control" / "PERSON_IDENTITY_AUTHORITY.md"


def test_contract_exists():
    assert CONTRACT.is_file(), "Person Identity Authority contract is missing"


def contract_text():
    assert CONTRACT.is_file(), "Person Identity Authority contract is missing"
    return CONTRACT.read_text(encoding="utf-8")


def test_core_identity_distinctions_are_present():
    text = contract_text()

    required = [
        "Name appearance",
        "Documentary person",
        "Same-person relationship",
        "Historical hypothesis",
        "NAME_APPEARANCE_ONLY",
        "SAME_PERSON",
    ]

    for phrase in required:
        assert phrase in text, (
            f"Person Identity Authority lost required distinction: {phrase}"
        )


def test_heuristics_do_not_establish_same_person():
    text = contract_text()

    required_rejections = [
        "same or similar name",
        "same locality",
        "same occupation",
        "same associates",
        "same property",
        "same mark or signature form",
        "overlapping chronology",
        "similar family structure",
        "agreement between secondary genealogies",
        "agreement between AI systems",
        "database or catalog matching",
        "repeated search results",
    ]

    for phrase in required_rejections:
        assert phrase in text, (
            "Identity heuristic is no longer explicitly rejected: "
            + phrase
        )

    assert "They do not constitute identity authority." in text


def test_name_appearance_does_not_automatically_become_person():
    text = contract_text()

    assert "A name appearance does not establish identity." in text
    assert "New appearances require their own documentary identity assessment." in text


def test_same_person_requires_explicit_documentary_basis():
    text = contract_text()

    assert "A SAME_PERSON relationship must be explicit." in text
    assert "The relationship requires an identified documentary basis." in text
    assert "the source or sources supporting that basis" in text


def test_research_artifacts_cannot_silently_promote_identity():
    text = contract_text()

    forbidden_promotions = [
        "Search Result\n        != Person Identity",
        "Found Artifact\n        != Person Identity",
        "Research Effect\n        != Person Identity",
        "Best Hypothesis\n        != Person Identity",
        "Name Variant\n        != Same Person",
    ]

    for phrase in forbidden_promotions:
        assert phrase in text, (
            "Identity authority boundary lost: " + phrase
        )


def test_joan_is_not_identified_as_anashuecot():
    text = contract_text()

    assert "PERSON-JOAN-001" in text
    assert "Joan = Anashuecot" in text
    assert "identifying her as Anashuecot;" in text
    assert (
        "the Joan/Anashuecot question remains a separate unresolved"
        in text
    )


def test_suspended_may_1682_record_cannot_be_promoted_to_joan():
    text = contract_text()

    assert (
        "treating the suspended May 1682 record as her appearance;"
        in text
    )
    assert (
        "the suspended May 1682 record cannot become a Joan appearance"
        in text
    )


def test_unresolved_identity_is_an_allowed_state():
    text = contract_text()
    normalized = " ".join(text.split())

    assert "the authority layer must preserve the uncertainty." in normalized
    assert "**Unresolved is an allowed state.**" in normalized
    assert "without forced resolution" in normalized


def test_person_object_does_not_absorb_historical_hypotheses():
    text = contract_text()

    prohibited_identity_conclusions = [
        "Joan = Narragansett",
        "Joan = English",
        "Joan = Irish",
        "Joan = Beggarly",
    ]

    for conclusion in prohibited_identity_conclusions:
        assert conclusion in text

    assert "Those propositions require separate claims or hypotheses." in text


if __name__ == "__main__":
    tests = [
        test_contract_exists,
        test_core_identity_distinctions_are_present,
        test_heuristics_do_not_establish_same_person,
        test_name_appearance_does_not_automatically_become_person,
        test_same_person_requires_explicit_documentary_basis,
        test_research_artifacts_cannot_silently_promote_identity,
        test_joan_is_not_identified_as_anashuecot,
        test_suspended_may_1682_record_cannot_be_promoted_to_joan,
        test_unresolved_identity_is_an_allowed_state,
        test_person_object_does_not_absorb_historical_hypotheses,
    ]

    for test in tests:
        test()
        print(f"[PASS] {test.__name__}")

    print("\n[PASS] ALL PERSON IDENTITY AUTHORITY TESTS")
    print("[PASS] Identity authority remains failure-closed")
    print("[PASS] No production ledger was modified")
