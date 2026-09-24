"""
Controlled normalization of person-page Discovery Keys.

This module converts the human-readable Discovery Key into bounded,
status-preserving search atoms.

It does NOT:
- establish identity
- merge people
- promote hypotheses
- execute searches
- write SEARCH_TARGETS.yml
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiscoveryAtom:
    person: str
    field: str
    value: str
    status: str


EXPLICIT = "EXPLICIT"
POSSIBLE_UNPROVEN = "POSSIBLE_UNPROVEN"
CONDITIONAL = "CONDITIONAL"
DISPUTED = "DISPUTED"
EXCLUDED = "EXCLUDED"
UNKNOWN = "UNKNOWN"


def normalize_field_value(
    person: str,
    field: str,
    value: str,
) -> list[DiscoveryAtom]:
    """
    Convert one raw Discovery Key field into bounded atoms.

    This initial implementation deliberately handles only clearly
    structured name variants. Other fields remain untouched until
    their syntax is tested separately.
    """
    if field != "Name variants":
        return []

    atoms: list[DiscoveryAtom] = []

    for line in value.splitlines():
        text = line.strip().lstrip("-").strip()
        if not text:
            continue

        status = EXPLICIT

        if "Possible, UNPROVEN:" in text:
            status = POSSIBLE_UNPROVEN
            text = text.split("Possible, UNPROVEN:", 1)[1].strip()

        if "Removed as probable AI fabrication:" in text:
            status = EXCLUDED
            text = text.split(
                "Removed as probable AI fabrication:", 1
            )[1].strip()

        # Pull the bolded searchable names from the remaining line.
        # Multiple bold spans are preserved as separate atoms.
        parts = text.split("**")
        for index in range(1, len(parts), 2):
            candidate = parts[index].strip()
            if not candidate:
                continue

            # Split comma-separated variants without changing their status.
            for variant in candidate.split(","):
                variant = variant.strip().strip('"').strip()
                if not variant:
                    continue

                atoms.append(
                    DiscoveryAtom(
                        person=person,
                        field=field,
                        value=variant,
                        status=status,
                    )
                )

    return atoms
