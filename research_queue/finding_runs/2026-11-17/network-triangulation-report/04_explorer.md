# Explorer Queue Packet — research_findings/network_triangulation_report.md

**Finding ID:** `FINDING-6b74fce0ba56`
**Status:** `LAWS_FILTERED`
**Source SHA-256:** `96ee7c21bae11bd3c0393dd8e760abcc993e66608768533000ef4bd473917ac0`
**Stage purpose:** expand sideways context and identify where evidence may be hiding in plain sight.
**Publication rule:** This is a Laws-filtered review packet, not evidence and not an approval. AI disclaimer applies.

## Required action
Process this finding as stage `04_explorer`. Preserve the exact source path and hash.
Do not edit the source finding or promote any claim to PROOF.

## Image gate
Referenced images: none detected.
Images already staged in `images/_pending_review/`: none.
Referenced images already elsewhere in `images/` and not pending: none.
Referenced images not found in the archive: none.
Any newly supplied image belongs in `images/_pending_review/` until a human reviews and promotes it.

## Finding text
```markdown
# Network Triangulation Findings - CORRECTED after adversarial testing

**Status:** This report replaces the v1 findings of the same name. The v1 report
overclaimed; the test suite (`tools/test_network.py`) shows why. Kept here as a
negative result per NEGATIVE_LOG conventions.

## What v1 claimed
That Joan Greene's `presence_ratio = 0.0`, co-document bridge position, and
similarity to the Awashonks comparator "corroborated H1 (Structural Presence)."

## What the tests found

### T1 - The 0.0 ratio was a coding artifact, not an emergent property
When the network is rebuilt from Tier 1 facts only (6 persons, 2 documents,
8 edges), Joan has TWO edges: `named_wife` (identification) and
`annuity_anchor` (conditional clause). Whether she reads as "structural-only"
depends entirely on how roles are bucketed:

| coding | Joan structural edges | Joan actor/identifying edges | verdict |
|---|---|---|---|
| A strict | 1 | 1 | MIXED |
| B broad | 2 | 0 | STRUCTURAL-ONLY |
| C lenient | 1 | 1 | MIXED |

The v1 headline metric sat on coding A. Under A and C she is MIXED. A finding
that flips when you recode is a coding choice, not a network result.

### T2 - The entire Joan signal lives in ONE document cluster
Leave-one-out: drop the March 1682 deed pair and Joan vanishes from the network
completely. The 1679 affidavit anchors John, not Joan. The "pattern" is a
single-document observation restated as topology.

### T3 - Significance testing is impossible at n=2 documents
With person degrees john=2, all others=1, exactly ONE bipartite configuration
satisfies the degree sequence. The null model is degenerate; the minimum
achievable p-value from exact enumeration is 1.0. No centrality statistic on
this graph can be "significant." Null models require a corpus of dozens of
documents (e.g., all Worth Vol. I deeds), not two.

### T4 - The absence finding is real but is not a network result
The NEGATIVE_LOG sweep (Arnold, Bartlett, Austin, Savage, Plymouth, Minor)
yields zero Joan hits outside the 1682 event. Joan's share of the household's
Tier 1 documentary footprint is 1 of 3 documents. That is a genuine and
carefully established absence - but the graph only displays it; it cannot
amplify or independently confirm it.

## Revised conclusion
- The network method did NOT corroborate H1. At current corpus size it cannot.
- The one legitimate quantified output: Joan's documentary existence is
  single-transaction dependent (T2), which is a sharper statement of the known
  four-facts baseline.
- Path forward: expand the corpus first (Worth Vol. I deeds, North Kingstown
  town series, Fones Record full volume), THEN compute presence ratios and
  centrality against comparator wives who sign/mark. Pre-register predictions
  before running, per the guardrails.
- The Awashonks comparator must stay out of any network until the Drake and
  Church citations are verified against the actual texts (still UNVERIFIED in
  theory/anashuecot_kin_map.md).

## Files
- `tools/test_network.py` - reproducible test suite (requires networkx, pandas)
- `data/network/bipartite_edges.csv`, `data/network/person_metrics.csv` - v1
  corpus (RETAINED for provenance but flagged: contains unverified comparator
  edges; do not cite its metrics as findings)
```

## Required output
Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.

## Required sideways-context checklist
- Map household people, witnesses, neighbors, in-laws, buyers, sellers, and officials.
- Expand across land, probate, court, church, militia, servant, captivity, shipping, and Indigenous-centered records.
- Test Rhode Island, Massachusetts, Connecticut, Plymouth, New York, Crown, port, and local town repositories.
- Search EVERY variant of EVERY name in the finding — full clusters from methodology/name_variant_registry.md (standard, scribe drift, OCR-plausible, phonetic) — in EVERY repository searched, and log which variants were queried. A name missed for spelling is a name lost.
- Track every John Greene appearance 1600-1750 across English, Irish/Ulster, Scottish, port-book, and local-town paperwork — each is a firewall-relevant capture per methodology/collection_policy.md (the Greene Net).
- Search relationship descriptions ('wife of', 'Goodwife', 'widow', 'son of', 'his marke'), not only the target person's name.
- Follow where the leads point, including jurisdictions and languages the finding does not name.
- For each proposed edge, state the source anchor that would prove it and the record that would disprove it.
