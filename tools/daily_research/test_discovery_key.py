from discovery_key import (
    EXCLUDED,
    EXPLICIT,
    POSSIBLE_UNPROVEN,
    normalize_field_value,
)


def test_name_variants_preserve_status():
    value = """\
- **Anashuecot**
- **Awashuwett**
- Possible, UNPROVEN: **Anashusett**
- Removed as probable AI fabrication: **BogusName**
"""

    atoms = normalize_field_value(
        "Anashuecot",
        "Name variants",
        value,
    )

    assert [(atom.value, atom.status) for atom in atoms] == [
        ("Anashuecot", EXPLICIT),
        ("Awashuwett", EXPLICIT),
        ("Anashusett", POSSIBLE_UNPROVEN),
        ("BogusName", EXCLUDED),
    ]


def test_unsupported_fields_produce_no_atoms():
    atoms = normalize_field_value(
        "Anashuecot",
        "Place anchors",
        "- Quidnessett",
    )

    assert atoms == []


def test_excluded_atom_is_not_reclassified():
    atoms = normalize_field_value(
        "Anashuecot",
        "Name variants",
        "Removed as probable AI fabrication: **BogusName**",
    )

    assert len(atoms) == 1
    assert atoms[0].value == "BogusName"
    assert atoms[0].status == EXCLUDED
