#!/usr/bin/env python3
"""Regression test for fair allocation of bounded research leads."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR_DIR = ROOT / "tools" / "multi_agent_daily"

if str(ORCHESTRATOR_DIR) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATOR_DIR))

import orchestrate


def make_lead(person: str, index: int) -> dict:
    return {
        "person_name": person,
        "lens": "test_lens",
        "query": f'"{person}" historical record {index}',
        "url": f"https://example.org/{person.replace(' ', '-')}/{index}",
        "record_id": f"{person.replace(' ', '-').upper()}-{index:04d}",
        "title": f"{person} lead {index}",
        "result_status": "FOUND",
        "model_status": "OPEN",
    }


def main() -> None:
    # Reproduce the fairness failure mode:
    # one person has enough leads to consume the entire positional budget.
    leads = (
        [make_lead("Dominant Person", index) for index in range(1, 121)]
        + [make_lead("Second Person", index) for index in range(1, 4)]
        + [make_lead("Third Person", index) for index in range(1, 4)]
    )

    selected, deferred = orchestrate.allocate_fair_leads(
        leads=leads,
        budget=100,
    )

    selected_counts = Counter(lead["person_name"] for lead in selected)
    deferred_counts = Counter(lead["person_name"] for lead in deferred)

    print(f"INPUT LEADS: {len(leads)}")
    print(f"SELECTED: {len(selected)}")
    print(f"DEFERRED: {len(deferred)}")
    print(f"SELECTED BY PERSON: {dict(selected_counts)}")
    print(f"DEFERRED BY PERSON: {dict(deferred_counts)}")

    if len(selected) != 100:
        raise SystemExit(
            f"FAIL: expected exactly 100 selected leads, got {len(selected)}"
        )

    if len(deferred) != 26:
        raise SystemExit(
            f"FAIL: expected exactly 26 deferred leads, got {len(deferred)}"
        )

    # The first round must give one lead to each person.
    first_three = [lead["person_name"] for lead in selected[:3]]
    expected_first_three = [
        "Dominant Person",
        "Second Person",
        "Third Person",
    ]

    if first_three != expected_first_three:
        raise SystemExit(
            "FAIL: allocation did not begin with deterministic round-robin order; "
            f"got {first_three!r}"
        )

    print("PASS: allocation begins with one lead per person")

    # Neither minority person may be starved merely because another person
    # has a much larger lead population.
    for person in ("Second Person", "Third Person"):
        if selected_counts[person] != 3:
            raise SystemExit(
                f"FAIL: {person} did not receive all available leads; "
                f"selected={selected_counts[person]}"
            )

    print("PASS: lower-volume people are not starved by the global cap")

    if selected_counts["Dominant Person"] != 94:
        raise SystemExit(
            "FAIL: dominant person's allocation is unexpected; "
            f"got {selected_counts['Dominant Person']}, expected 94"
        )

    print("PASS: remaining budget is consumed by the still-active person")

    # Exact preservation: every input lead appears exactly once in either side.
    input_ids = {id(lead) for lead in leads}
    selected_ids = {id(lead) for lead in selected}
    deferred_ids = {id(lead) for lead in deferred}

    if selected_ids & deferred_ids:
        raise SystemExit("FAIL: a lead appears in both selected and deferred")

    if selected_ids | deferred_ids != input_ids:
        raise SystemExit("FAIL: selected + deferred do not exhaustively partition input")

    if len(selected_ids) != len(selected):
        raise SystemExit("FAIL: duplicate selected lead detected")

    if len(deferred_ids) != len(deferred):
        raise SystemExit("FAIL: duplicate deferred lead detected")

    print("PASS: selected + deferred form an exact partition of the input")

    print()
    print("ORCHESTRATOR FAIR ALLOCATION REGRESSION TEST: PASS")


if __name__ == "__main__":
    main()
