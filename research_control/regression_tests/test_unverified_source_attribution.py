#!/usr/bin/env python3
"""A search context must not be mistaken for source-to-person attribution."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR_DIR = ROOT / "tools" / "multi_agent_daily"

if str(ORCHESTRATOR_DIR) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATOR_DIR))

import orchestrate


def main() -> None:
    lead = {
        "person_name": "Joan Greene",
        "lens": "narragansett_indigenous_context",
        "query": '"Joan Greene" Narragansett kinship',
        "result": {
            "title": "The arena of life: the dynamics of ecology",
            "url": "https://example.org/unrelated-catalog-record",
            "record_id": "CATALOG-TEST-001",
        },
    }

    captured = []
    original_add_target = orchestrate.add_target

    def capture_target(*args, **kwargs):
        target = {
            "question": kwargs.get("question", ""),
            "reason": kwargs.get("reason", ""),
            "person_slots": kwargs.get("person_slots", []),
            "name_variants": kwargs.get("name_variants", []),
            "record_families": kwargs.get("record_families", []),
            "source_identifier": kwargs.get("source_identifier", ""),
            "status": "READY_SHADOW",
        }
        captured.append(target)
        return target

    try:
        orchestrate.add_target = capture_target
        result = orchestrate.generate_search_targets(
            leads=[lead],
            origin_event="EVT-TEST-UNVERIFIED-ATTRIBUTION",
            laws=["No Algorithmic Contamination", "No Trust Without Evidence"],
        )
    finally:
        orchestrate.add_target = original_add_target

    assert len(captured) == 1, "The discovered source lead must be preserved"
    target = captured[0]

    # Keep the record traceable, but do not assign it to Joan automatically.
    assert target["source_identifier"] == lead["result"]["url"]
    assert target["person_slots"] == [], (
        "Unverified catalog results must not inherit the searched person"
    )
    assert target["name_variants"] == [], (
        "A searched person's name must not become a source identity claim"
    )
    assert target["record_families"] == [], (
        "The originating lens must not automatically become the source's record family"
    )

    # Preserve the origin of discovery as context, explicitly not attribution.
    assert "Joan Greene" in target["reason"]
    assert lead["query"] in target["reason"]
    assert lead["lens"] in target["reason"]
    assert "unverified" in target["reason"].lower()

    # The follow-up should investigate the catalog record itself.
    assert "for Joan Greene" not in target["question"]
    assert target["status"] == "READY_SHADOW"
    assert result["generated"], "Generated targets should remain visible to callers"

    print("PASS: source lead preserved with URL and original search context")
    print("PASS: searched person is not automatically assigned to the source")
    print("PASS: originating lens is not automatically assigned as record family")
    print("PASS: target remains READY_SHADOW")


if __name__ == "__main__":
    main()
