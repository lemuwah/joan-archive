#!/usr/bin/env python3
"""
Regression test for the Search Arrival -> Found Artifact bridge.

Contract:

    FOUND search arrival
        |
        +--> one Found Artifact per returned source result
        |
        +--> preserve search provenance
        |
        +--> preserve source metadata
        |
        +--> names remain NAME_APPEARANCE_ONLY
        |
        +--> no identity/evidence/claim/promotion semantics

    NO_RESULTS -> zero artifacts
    ERROR      -> zero artifacts

This test is intentionally written before the production bridge.
It should FAIL until the bridge implementation exists.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT / "research_control" / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "research_control"))

from append_event import load_schema, validate
from record_search_arrivals import build_arrival
from record_found_artifacts import build_found_artifacts, append_unique


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


def target():
    return {
        "target_id": "ST-BRIDGE-TEST",
        "question": "Find records related to Joan Unknown Greene.",
        "record_families": ["land"],
        "jurisdictions": ["Rhode Island"],
        "date_range": {"start": 1600, "end": 1800},
        "name_variants": [
            "Joan Unknown Greene",
            "Joan Greene",
        ],
    }


def execution(event_id="EVT-BRIDGE-TEST", status="FOUND"):
    return {
        "event_id": event_id,
        "executed_at": "2026-09-24T23:30:00+00:00",
        "query": '"Joan Greene" land',
        "result_status": status,
    }


def found_results():
    return [
        {
            "source": "internet_archive",
            "record_id": "IA-001",
            "title": "Synthetic record one",
            "url": "https://example.invalid/item/IA-001",
            "collection": "Synthetic Collection",
            "description": "Returned by the search source.",
            "matched_terms": ["Joan Greene"],
            "people": [
                {
                    "name": "Joan Greene",
                    "role": "NAME_APPEARANCE_ONLY",
                }
            ],
        },
        {
            "source": "internet_archive",
            "record_id": "IA-002",
            "title": "Synthetic record two",
            "url": "https://example.invalid/item/IA-002",
            "collection": "Synthetic Collection",
            "volume": "Volume II",
            "page": "42",
            "description": "Another returned source result.",
            "matched_terms": ["Greene"],
            "people": [
                {
                    "name": "John Greene",
                    "role": "NAME_APPEARANCE_ONLY",
                }
            ],
        },
    ]


def build_found_arrival():
    return build_arrival(
        target=target(),
        execution=execution(),
        source_name="internet_archive",
        source_results=found_results(),
        source_error=None,
        artifact_ref="research_queue/search_results/ST-BRIDGE-TEST.json",
        execution_event_id="EVT-BRIDGE-TEST",
    )


def assert_schema_valid(artifact):
    schema = load_schema("artifact")
    errors = validate(artifact, schema)
    assert errors == [], f"Found Artifact failed schema validation: {errors}"


def assert_no_forbidden_fields(value):
    encoded = json.dumps(value, ensure_ascii=False).lower()

    for field in FORBIDDEN_FIELDS:
        assert field not in value
        assert f'"{field}"' not in encoded


def main():
    arrival = build_found_arrival()

    # ------------------------------------------------------------
    # A. FOUND arrival produces one artifact per source result.
    # ------------------------------------------------------------
    artifacts = build_found_artifacts(
        arrival=arrival,
        source_results=found_results(),
    )

    assert len(artifacts) == 2
    print("PASS: one Found Artifact is created per returned source result")

    # ------------------------------------------------------------
    # B. Search provenance is preserved.
    # ------------------------------------------------------------
    for artifact in artifacts:
        assert artifact["search_ref"]["search_id"] == arrival["search_id"]
        assert (
            artifact["search_ref"]["target_id"]
            == target()["target_id"]
        )
        assert (
            artifact["search_ref"]["execution_event_id"]
            == "EVT-BRIDGE-TEST"
        )

    print("PASS: search provenance is preserved")

    # ------------------------------------------------------------
    # C. Source provenance is preserved.
    # ------------------------------------------------------------
    for artifact in artifacts:
        assert artifact["source"]["name"] == "internet_archive"
        assert artifact["source"]["access_method"] == "DATABASE"

    print("PASS: source provenance is preserved")

    # ------------------------------------------------------------
    # D. Source result identity/locator data is preserved
    #    without inventing historical meaning.
    # ------------------------------------------------------------
    first = artifacts[0]
    second = artifacts[1]

    assert first["locator"]["record_identifier"] == "IA-001"
    assert first["locator"]["url"] == (
        "https://example.invalid/item/IA-001"
    )
    assert first["discovery"]["title"] == "Synthetic record one"
    assert first["discovery"]["matched_terms"] == ["Joan Greene"]

    assert second["locator"]["record_identifier"] == "IA-002"
    assert second["locator"]["volume"] == "Volume II"
    assert second["locator"]["page"] == "42"

    print("PASS: available source metadata is preserved")

    # ------------------------------------------------------------
    # E. Person firewall.
    # ------------------------------------------------------------
    for artifact in artifacts:
        for person in artifact["person_slots"]:
            assert person["role"] == "NAME_APPEARANCE_ONLY"
            assert "identity_status" not in person
            assert "same_person" not in person

    print("PASS: person names remain NAME_APPEARANCE_ONLY")

    # ------------------------------------------------------------
    # F. No forbidden semantic fields.
    # ------------------------------------------------------------
    for artifact in artifacts:
        assert_no_forbidden_fields(artifact)
        assert_schema_valid(artifact)

    print("PASS: artifacts remain discovery-only")

    # ------------------------------------------------------------
    # G. NO_RESULTS produces zero artifacts.
    # ------------------------------------------------------------
    negative_arrival = build_arrival(
        target=target(),
        execution=execution(
            event_id="EVT-BRIDGE-NORESULTS",
            status="NO_RESULTS",
        ),
        source_name="internet_archive",
        source_results=[],
        source_error=None,
        artifact_ref="research_queue/search_results/ST-BRIDGE-TEST.json",
        execution_event_id="EVT-BRIDGE-NORESULTS",
    )

    negative_artifacts = build_found_artifacts(
        arrival=negative_arrival,
        source_results=[],
    )

    assert negative_artifacts == []

    print("PASS: NO_RESULTS produces zero Found Artifacts")

    # ------------------------------------------------------------
    # H. ERROR produces zero artifacts.
    # ------------------------------------------------------------
    error_arrival = build_arrival(
        target=target(),
        execution=execution(
            event_id="EVT-BRIDGE-ERROR",
            status="ERROR",
        ),
        source_name="internet_archive",
        source_results=[],
        source_error={"error": "Synthetic source failure"},
        artifact_ref="research_queue/search_results/ST-BRIDGE-TEST.json",
        execution_event_id="EVT-BRIDGE-ERROR",
    )

    error_artifacts = build_found_artifacts(
        arrival=error_arrival,
        source_results=[],
    )

    assert error_artifacts == []

    print("PASS: ERROR produces zero Found Artifacts")

    # ------------------------------------------------------------
    # I. Multiple artifacts may share one search arrival.
    # ------------------------------------------------------------
    assert (
        artifacts[0]["search_ref"]["search_id"]
        == artifacts[1]["search_ref"]["search_id"]
    )
    assert artifacts[0]["artifact_id"] != artifacts[1]["artifact_id"]

    print("PASS: multiple artifacts may share one search arrival")

    # ------------------------------------------------------------
    # J. Append duplicate protection.
    # ------------------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "found_artifacts.jsonl"

        assert append_unique(artifacts[0], ledger=ledger) is True
        assert append_unique(artifacts[0], ledger=ledger) is False

        records = [
            json.loads(line)
            for line in ledger.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        assert len(records) == 1

    print("PASS: duplicate artifact_id is not appended")

    print("\n[PASS] SEARCH ARRIVAL -> FOUND ARTIFACT BRIDGE CONTRACT")


if __name__ == "__main__":
    main()
