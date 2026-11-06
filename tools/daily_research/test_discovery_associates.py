"""Regression tests for uncertainty-preserving associate discovery."""

from discovery_key import normalize_field_value
from sweep import _parse_documented_associates


def test_associate_preserves_uncertain_relationship_context():
    atoms = _parse_documented_associates(
        "Elizabeth",
        "Joan Greene (mother-in-law — contact plausible, not documented)",
    )

    assert len(atoms) == 1
    assert atoms[0].value == "Joan Greene"
    assert atoms[0].relationship_context == (
        "mother-in-law — contact plausible, not documented"
    )


def test_household_association_preserves_indirect_context():
    atoms = _parse_documented_associates(
        "Edward Greenman",
        "Joan Greene (household of his longtime associate)",
    )

    assert len(atoms) == 1
    assert atoms[0].value == "Joan Greene"
    assert atoms[0].relationship_context == (
        "household of his longtime associate"
    )


def test_parent_pair_is_split_into_individual_search_atoms():
    atoms = _parse_documented_associates(
        "Henry Greene",
        "John Greene Sr. and Joan Greene (parents)",
    )

    assert [atom.value for atom in atoms] == [
        "John Greene Sr.",
        "Joan Greene",
    ]
    assert all(atom.relationship_context == "parents" for atom in atoms)


def test_descriptive_deed_phrase_is_not_a_name_variant():
    atoms = normalize_field_value(
        "James Greene",
        "Name variants",
        'James Greene; **"natural son of John and Joan Greene"**',
    )

    assert all(
        atom.value != "natural son of John and Joan Greene"
        for atom in atoms
    )


def test_parent_pair_splits_without_losing_qualifier():
    atoms = _parse_documented_associates(
        "Henry Greene",
        "John Greene Sr. and Joan Greene (parents — compilation-sourced)",
    )

    assert [atom.value for atom in atoms] == [
        "John Greene Sr.",
        "Joan Greene",
    ]
    assert all(
        atom.relationship_context == "parents — compilation-sourced"
        for atom in atoms
    )
