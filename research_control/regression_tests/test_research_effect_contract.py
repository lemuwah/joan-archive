#!/usr/bin/env python3
"""
Adversarial regression tests for the Research Effect contract.

This suite tests research-process classification only.

It must never allow a research effect to become:
- an identity assignment,
- a confidence score,
- a hypothesis ranking,
- a proof status,
- an absence-of-existence conclusion, or
- a silent claim promotion.

Core principle:

    RESEARCH ACTION
          |
          v
    RESEARCH EFFECT
          |
          v
    NEXT TEST / REVIEW

Research Effect is not historical truth.
"""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "research_control" / "RESEARCH_EFFECT_CONTRACT.md"


ALLOWED_EFFECTS = {
    "NEW_DOCUMENTARY_EVIDENCE",
    "NEGATIVE_SEARCH_RESULT",
    "CORROBORATION",
    "CONTRADICTION",
    "IDENTITY_SHAPING_INFERENCE",
    "LEAD_ONLY",
    "NO_MATERIAL_CHANGE",
}

FORBIDDEN_FIELDS = {
    "identity",
    "identity_status",
    "identity_confidence",
    "confidence",
    "hypothesis_rank",
    "best_hypothesis",
    "proof_status",
    "claim_status",
    "historical_certainty",
    "eliminated_hypothesis",
    "person_identity",
}


def assert_contract_exists():
    assert CONTRACT.is_file(), "Research Effect contract is missing"


def test_effect_vocabulary_is_closed():
    expected = {
        "NEW_DOCUMENTARY_EVIDENCE",
        "NEGATIVE_SEARCH_RESULT",
        "CORROBORATION",
        "CONTRADICTION",
        "IDENTITY_SHAPING_INFERENCE",
        "LEAD_ONLY",
        "NO_MATERIAL_CHANGE",
    }

    assert ALLOWED_EFFECTS == expected


def test_unknown_effect_is_not_allowed():
    assert "PERSON_IDENTIFIED" not in ALLOWED_EFFECTS
    assert "HYPOTHESIS_CONFIRMED" not in ALLOWED_EFFECTS
    assert "ABSENCE_PROVEN" not in ALLOWED_EFFECTS


def test_research_effect_has_no_identity_semantics():
    sample = {
        "effect": "IDENTITY_SHAPING_INFERENCE",
        "literal_basis": (
            "A later genealogy uses the name Enfield Greene while "
            "La Mance earlier speculates that John of Quidnessett "
            "probably lived at Enfield."
        ),
        "interpretation": (
            "This may reveal a place-name generation mechanism "
            "requiring an earlier-source search."
        ),
        "next_test": (
            "Locate the earliest independent appearance of "
            "Enfield Greene."
        ),
    }

    assert not (set(sample) & FORBIDDEN_FIELDS)


def test_negative_search_is_not_absence():
    effect = "NEGATIVE_SEARCH_RESULT"

    assert effect in ALLOWED_EFFECTS
    assert "ABSENCE_PROVEN" not in ALLOWED_EFFECTS
    assert "PERSON_DID_NOT_EXIST" not in ALLOWED_EFFECTS


def test_corroboration_requires_independence_conceptually():
    non_independent_sources = {
        "AI_AGREEMENT",
        "DUPLICATE_CATALOG",
        "DUPLICATE_TRANSCRIPTION",
        "COPIED_GENEALOGY",
        "SAME_SOURCE_CITATION",
    }

    assert "AI_AGREEMENT" not in ALLOWED_EFFECTS
    assert "DUPLICATE_CATALOG" not in ALLOWED_EFFECTS

    # The controlled effect describes a research consequence; it does not
    # encode "agents agree" as corroboration.
    assert "CORROBORATION" in ALLOWED_EFFECTS


def test_enfield_ghost_name_remains_research_effect_only():
    effect = "IDENTITY_SHAPING_INFERENCE"

    literal_basis = (
        "La Mance presents Enfield as a probable residence of "
        "John of Quidnessett; a later genealogy contains "
        "the name Enfield Greene."
    )

    forbidden_conclusions = {
        "Enfield Greene was fabricated",
        "Enfield Greene was fictional",
        "Enfield Greene was not a real person",
        "Enfield Greene was John Greene's child",
        "Enfield Greene was not John Greene's child",
    }

    assert effect in ALLOWED_EFFECTS
    assert literal_basis
    assert not any(
        conclusion in literal_basis
        for conclusion in forbidden_conclusions
    )


def test_no_material_change_is_valid():
    assert "NO_MATERIAL_CHANGE" in ALLOWED_EFFECTS


def test_identity_shaping_does_not_promote_identity():
    assert "IDENTITY_SHAPING_INFERENCE" in ALLOWED_EFFECTS
    assert "PERSON_IDENTIFIED" not in ALLOWED_EFFECTS
    assert "IDENTITY_CONFIRMED" not in ALLOWED_EFFECTS


def test_effects_are_not_claim_statuses():
    claim_statuses = {
        "UNTESTED",
        "OPEN",
        "SEARCHING",
        "PARTIAL",
        "EVIDENCE_LOCATED",
        "VERIFIED",
        "REJECTED",
    }

    assert ALLOWED_EFFECTS.isdisjoint(claim_statuses)


def test_effects_are_not_search_result_states():
    search_result_states = {
        "NO_RESULT_LOCATED",
        "RESULT_LOCATED",
        "PARTIAL_RESULT",
        "CONFLICTING_RESULTS",
        "SOURCE_INACCESSIBLE",
        "SEARCH_ERROR",
    }

    assert ALLOWED_EFFECTS.isdisjoint(search_result_states)


def test_contract_preserves_core_boundary():
    text = CONTRACT.read_text(encoding="utf-8")

    required_phrases = [
        "does not establish historical truth",
        "does not identify Joan Greene",
        "does not rank hypotheses",
        "does not assign confidence",
        "does not promote a claim",
        "NEGATIVE_SEARCH_RESULT",
        "CORROBORATION",
        "IDENTITY_SHAPING_INFERENCE",
        "NO_MATERIAL_CHANGE",
        "Enfield",
        "place-name",
        "generation mechanism",
    ]

    for phrase in required_phrases:
        assert phrase in text, f"Contract lost required boundary: {phrase}"


if __name__ == "__main__":
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]

    for test in tests:
        test()

    print("RESEARCH EFFECT CONTRACT: PASS")
