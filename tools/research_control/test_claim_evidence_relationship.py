#!/usr/bin/env python3
"""Design tests for the claim–evidence relationship schema.

These tests validate structure only. They do not determine historical truth.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT / "research_control/tools"))

from append_event import validate


SCHEMA_PATH = (
    ROOT / "research_control/schemas/claim_evidence_relationship.schema.json"
)


def load_relationship_schema() -> dict:
    import json

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


VALID_RELATIONSHIP = {
    "relationship_id": "REL-000001",
    "evidence_id": "EVID-000001",
    "claim_id": "CLAIM-000001",
    "relation": "DIRECTLY_SUPPORTS",
    "scope": (
        "The deed explicitly names Joan/Joane Greene as the wife of John Greene."
    ),
    "provenance": {
        "actor_type": "AI",
        "actor": "research-agent",
        "platform": "joan-archive",
        "recorded_at": "2026-09-15T00:00:00Z",
    },
}


def check(record, should_pass: bool, label: str):
    errors = validate(record, load_relationship_schema())
    passed = not errors

    assert passed == should_pass, (
        f"{label}: expected "
        f"{'PASS' if should_pass else 'BLOCK'}, got "
        f"{'PASS' if passed else 'BLOCK'}\n"
        + "\n".join(errors)
    )


def main():
    check(
        VALID_RELATIONSHIP,
        True,
        "valid DIRECTLY_SUPPORTS relationship",
    )

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    bad["relationship_id"] = "REL-BAD"
    check(bad, False, "invalid relationship ID")

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    bad["evidence_id"] = "FINDING-fe55dd3e755e"
    check(bad, False, "finding ID used as evidence ID")

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    bad["claim_id"] = "CLAIM-BAD"
    check(bad, False, "invalid claim ID")

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    bad["relation"] = "AI_THINKS_THIS_IS_TRUE"
    check(bad, False, "invented relationship type")

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    bad["scope"] = ""
    check(bad, False, "empty relationship scope")

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    del bad["provenance"]
    check(bad, False, "missing provenance")

    context = copy.deepcopy(VALID_RELATIONSHIP)
    context["relation"] = "CONTEXT_ONLY"
    context["scope"] = (
        "The source provides historical context relevant to the investigation "
        "but does not itself establish the claim."
    )
    check(context, True, "CONTEXT_ONLY relationship")

    non_support = copy.deepcopy(VALID_RELATIONSHIP)
    non_support["relation"] = "DOES_NOT_ESTABLISH"
    non_support["scope"] = (
        "The wife-name observation does not establish Joan's geographic or "
        "cultural origin."
    )
    check(non_support, True, "DOES_NOT_ESTABLISH relationship")

    contradiction = copy.deepcopy(VALID_RELATIONSHIP)
    contradiction["relation"] = "CONTRADICTS"
    contradiction["scope"] = (
        "The observation conflicts with the proposition stated in the claim."
    )
    check(contradiction, True, "CONTRADICTS relationship")

    bad = copy.deepcopy(VALID_RELATIONSHIP)
    bad["historical_truth"] = True
    check(bad, False, "unknown field")

    ai_record = copy.deepcopy(VALID_RELATIONSHIP)
    ai_record["provenance"]["actor_type"] = "AI"
    check(
        ai_record,
        True,
        "AI-created relationship remains structurally valid",
    )

    print("CLAIM-EVIDENCE RELATIONSHIP DESIGN TEST: PASS")
    print("Structural validation works through the existing generic validator.")
    print("Relationships remain separate from Event Spine ledgers.")
    print("No historical truth was inferred by the validator.")
    print("No production ledger was modified.")


if __name__ == "__main__":
    main()
