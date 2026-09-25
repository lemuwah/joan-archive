#!/usr/bin/env python3

"""
Regression tests for the Found Artifact contract.

Found Artifacts preserve discovery only.

They must not become:
    - Claims
    - Evidence
    - Identity conclusions
    - Promotion decisions
    - Rankings
    - Historical statuses

These tests do not write to production ledgers.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_FILE = ROOT / "research_control" / "schemas" / "found_artifact.schema.json"


ARTIFACT = {
    "artifact_id": "ARTIFACT-TEST001",
    "found_at": "2026-09-24T23:30:00+00:00",
    "search_ref": {
        "search_id": "SEARCH-123456",
        "target_id": "TARGET-EXAMPLE",
        "execution_event_id": "EXEC-EXAMPLE",
    },
    "source": {
        "name": "example_archive",
        "access_method": "DATABASE",
    },
    "locator": {
        "url": "",
        "collection": "Example Collection",
        "volume": "Volume I",
        "page": "42",
        "record_identifier": "",
    },
    "discovery": {
        "matched_terms": ["Joan Greene"],
        "title": "Example record",
        "description": "A result containing the name Joan Greene.",
        "raw_reference": "",
    },
    "person_slots": [
        {
            "name": "Joan Greene",
            "role": "NAME_APPEARANCE_ONLY",
        }
    ],
    "provenance": {
        "actor_type": "SYSTEM",
        "actor": "SEARCH_EXECUTOR",
        "platform": "joan-archive",
        "recorded_at": "2026-09-24T23:30:00+00:00",
    },
}


FORBIDDEN_FIELDS = {
    "claim",
    "claim_id",
    "claim_ref",
    "claim_status",
    "evidence",
    "evidence_id",
    "evidence_ref",
    "evidence_status",
    "evidentiary_value",
    "supports_claim",
    "contradicts_claim",
    "identity",
    "identity_status",
    "same_person",
    "person_match",
    "identity_confidence",
    "promotion",
    "promotion_status",
    "promoted",
    "promotion_ref",
    "historical_status",
    "verified",
    "proven",
    "disproven",
    "rejected",
    "confirmed",
    "score",
    "rank",
    "priority",
    "best_hypothesis",
    "confidence",
    "next_test",
    "interpretation",
    "assessment",
    "meaning",
}


def test_schema_exists():
    assert SCHEMA_FILE.exists()
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    assert schema["title"] == "Found Artifact"
    assert schema["additionalProperties"] is False


def test_artifact_has_only_contract_fields():
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    allowed = set(schema["properties"])
    actual = set(ARTIFACT)

    assert actual <= allowed
    assert not actual - allowed


def test_required_fields_are_present():
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    required = set(schema["required"])

    assert required <= set(ARTIFACT)


def test_no_forbidden_fields_are_in_schema():
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    allowed = set(schema["properties"])

    overlap = allowed & FORBIDDEN_FIELDS

    assert not overlap, (
        "Found Artifact schema contains forbidden semantic fields: "
        + repr(sorted(overlap))
    )


def test_no_forbidden_fields_are_in_artifact():
    present = set(ARTIFACT) & FORBIDDEN_FIELDS

    assert not present, (
        "Found Artifact contains forbidden semantic fields: "
        + repr(sorted(present))
    )


def test_name_appearance_does_not_assert_identity():
    person = ARTIFACT["person_slots"][0]

    assert person["name"] == "Joan Greene"
    assert person["role"] == "NAME_APPEARANCE_ONLY"

    assert "identity_status" not in ARTIFACT
    assert "same_person" not in ARTIFACT


def test_search_reference_is_preserved():
    assert ARTIFACT["search_ref"]["search_id"] == "SEARCH-123456"
    assert ARTIFACT["search_ref"]["target_id"] == "TARGET-EXAMPLE"
    assert ARTIFACT["search_ref"]["execution_event_id"] == "EXEC-EXAMPLE"


def test_multiple_artifacts_can_share_search_arrival():
    second = copy.deepcopy(ARTIFACT)
    second["artifact_id"] = "ARTIFACT-TEST002"

    assert second["search_ref"]["search_id"] == ARTIFACT["search_ref"]["search_id"]
    assert second["artifact_id"] != ARTIFACT["artifact_id"]


def test_irrelevance_does_not_require_rewriting_discovery():
    artifact = copy.deepcopy(ARTIFACT)

    artifact["discovery"]["description"] = (
        "A name match later determined to concern an unrelated person."
    )

    assert artifact["artifact_id"] == ARTIFACT["artifact_id"]
    assert "identity_status" not in artifact
    assert "historical_status" not in artifact


def test_json_round_trip():
    encoded = json.dumps(ARTIFACT, sort_keys=True)
    decoded = json.loads(encoded)

    assert decoded == ARTIFACT


if __name__ == "__main__":
    tests = [
        test_schema_exists,
        test_artifact_has_only_contract_fields,
        test_required_fields_are_present,
        test_no_forbidden_fields_are_in_schema,
        test_no_forbidden_fields_are_in_artifact,
        test_name_appearance_does_not_assert_identity,
        test_search_reference_is_preserved,
        test_multiple_artifacts_can_share_search_arrival,
        test_irrelevance_does_not_require_rewriting_discovery,
        test_json_round_trip,
    ]

    for test in tests:
        test()
        print(f"[PASS] {test.__name__}")

    print("\n[PASS] ALL FOUND ARTIFACT CONTRACT TESTS")
    print("[PASS] Schema + regression test created")
    print("[PASS] No production ledger was modified")
