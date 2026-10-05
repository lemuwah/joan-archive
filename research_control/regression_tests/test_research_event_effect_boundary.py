"""
Regression test for the boundary between Event Spine activity
and Research Effect classification.

This test defines the contract only.
It does not modify event_spine.py, ledgers, orchestrators, or production data.
"""

ALLOWED_EFFECTS = {
    "NEW_DOCUMENTARY_EVIDENCE",
    "NEGATIVE_SEARCH_RESULT",
    "CORROBORATION",
    "CONTRADICTION",
    "IDENTITY_SHAPING_INFERENCE",
    "LEAD_ONLY",
    "NO_MATERIAL_CHANGE",
}

FORBIDDEN_EFFECTS = {
    "BEST_HYPOTHESIS",
    "CONFIRMED",
    "PROVEN",
    "ELIMINATED",
    "IDENTIFIED_PERSON",
    "FABRICATED_PERSON",
    "FICTIONAL_PERSON",
    "REJECTED_PERSON",
}

FORBIDDEN_FIELDS = {
    "identity",
    "identity_confidence",
    "person_identity",
    "best_hypothesis",
    "hypothesis_ranking",
    "proof_status",
    "claim_status",
    "historical_status",
}

SEARCH_RESULT_STATES = {
    "NO_RESULT_LOCATED",
    "RESULT_LOCATED",
    "PARTIAL_RESULT",
    "CONFLICTING_RESULTS",
    "SOURCE_INACCESSIBLE",
    "SEARCH_ERROR",
}

EVENT_STATUSES = {
    "RECORDED",
    "COMPLETED",
    "BLOCKED",
    "BEST_HYPOTHESIS",
}


def test_all_controlled_effects_are_allowed():
    assert len(ALLOWED_EFFECTS) == 7

    for effect in ALLOWED_EFFECTS:
        assert isinstance(effect, str)
        assert effect == effect.upper()


def test_effects_are_not_event_statuses():
    assert ALLOWED_EFFECTS.isdisjoint(EVENT_STATUSES)


def test_effects_are_not_search_result_states():
    assert ALLOWED_EFFECTS.isdisjoint(SEARCH_RESULT_STATES)


def test_forbidden_historical_conclusions_are_not_effects():
    assert ALLOWED_EFFECTS.isdisjoint(FORBIDDEN_EFFECTS)


def test_effect_cannot_contain_identity_authority_fields():
    example_effect = {
        "effect": "IDENTITY_SHAPING_INFERENCE",
        "literal_basis": (
            "A later genealogical person-name appears to correspond "
            "to a place-name previously presented as speculative."
        ),
        "next_test": (
            "Locate the earliest independent appearance of the "
            "person-name and test its documentary basis."
        ),
    }

    assert set(example_effect).isdisjoint(FORBIDDEN_FIELDS)


def test_la_mance_enfield_is_identity_shaping_not_person_identification():
    effect = "IDENTITY_SHAPING_INFERENCE"

    literal_basis = (
        "La Mance described Enfield as a probable home location; "
        "a later genealogy uses Enfield as part of a person-name."
    )

    forbidden_conclusions = {
        "IDENTIFIED_PERSON",
        "FABRICATED_PERSON",
        "FICTIONAL_PERSON",
        "REJECTED_PERSON",
    }

    assert effect in ALLOWED_EFFECTS
    assert effect not in FORBIDDEN_EFFECTS
    assert literal_basis
    assert not (effect in forbidden_conclusions)


def test_no_material_change_is_a_valid_research_outcome():
    assert "NO_MATERIAL_CHANGE" in ALLOWED_EFFECTS


def test_effect_does_not_replace_event_activity():
    event = {
        "event_class": "RESEARCH",
        "action": "SOURCE_REVIEW",
        "result": "SOURCE_LOCATED",
        "status": "COMPLETED",
        "research_effect": "NEW_DOCUMENTARY_EVIDENCE",
    }

    assert event["event_class"] == "RESEARCH"
    assert event["action"] == "SOURCE_REVIEW"
    assert event["result"] == "SOURCE_LOCATED"
    assert event["status"] == "COMPLETED"
    assert event["research_effect"] in ALLOWED_EFFECTS


if __name__ == "__main__":
    tests = [
        test_all_controlled_effects_are_allowed,
        test_effects_are_not_event_statuses,
        test_effects_are_not_search_result_states,
        test_forbidden_historical_conclusions_are_not_effects,
        test_effect_cannot_contain_identity_authority_fields,
        test_la_mance_enfield_is_identity_shaping_not_person_identification,
        test_no_material_change_is_a_valid_research_outcome,
        test_effect_does_not_replace_event_activity,
    ]

    for test in tests:
        test()

    print("RESEARCH EVENT EFFECT BOUNDARY: PASS")
