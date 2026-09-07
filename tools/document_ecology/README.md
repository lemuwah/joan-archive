# Document Ecology Search Model

This model asks where Joan sits inside the records of her time by expanding outward from the March 1682 deed without losing the page-level identity test.

## Zoom levels

- `L0_document`: the exact manuscript page, transcription, witnesses, bounds, and recording metadata.
- `L1_household`: John, Joan, children, annuity, probate, guardianship, dower, creditors, servants, captives, and enslaved people.
- `L2_associates`: witnesses, neighbors, interpreters, trading-post workers, merchants, church associates, and ship associates.
- `L3_locality`: Quidnessett, Cocumscussoc, Pawtuxet, town, church, land, court, militia, survey, archaeology, and community history.
- `L4_jurisdiction`: Rhode Island, Massachusetts, Connecticut, Plymouth, New York, Crown, port, military, and intercolonial records.
- `L5_region_atlantic`: English, Irish/Ulster, Scottish, servant, transportation, enslavement/captivity, port, shipping, Indigenous-authored, and material-culture sources.

The same question is asked at every level: who is involved, how are they connected, what record family could contain the missing relationship, and what would disprove the proposed connection?

## “Fungal” or network logic

Treat the archive as a branching network, not a straight family tree. Joan's location is a **frontier node**: every documented person, witness, place, legal act, household, and institution creates a possible edge. An edge is useful only when anchored to a record. Branches expand from the strongest documented edge and stop when they become name-only association.

The daily workflow generates:

- `research_queue/document_ecology/YYYY-MM-DD.json` — machine-readable search bundles
- `research_queue/document_ecology/YYYY-MM-DD.md` — human checklist with `NOT SEARCHED` markers

The bundle is a lead map. It does not establish that Joan belonged to a household, status group, ethnicity, or network merely because that group appears nearby.
