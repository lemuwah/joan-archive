# Joan Archive Research-Control Architecture Contract

**Status:** ACTIVE
**Created:** 2026-09-16
**Purpose:** Define the non-negotiable architectural boundaries of the Joan Archive research-control system.

---

## 1. Governing Principle

> **Laws govern the machine; evidence governs conclusions.**

The control plane exists to preserve provenance, uncertainty, contradiction, transparency, and auditability.

The control plane must never silently convert:

- observation into interpretation,
- interpretation into fact,
- AI agreement into corroboration,
- contextual association into identity,
- relationship into truth,
- or machine eligibility into historical proof.

Those transitions must remain explicit and auditable.

---

## 2. Core Evidence Chain

The canonical evidence chain is:

**SOURCE → EVIDENCE EVENT → RELATIONSHIP → CLAIM → STATUS / REVIEW**

Reverse lookup traverses the same records:

**CLAIM → RELATIONSHIP → EVIDENCE EVENT → SOURCE**

The two directions are views over the same underlying records, not separate evidence systems.

---

## 3. Source

A Source identifies historical or documentary material.

Where available, preserve:

- repository,
- collection,
- document or record identifier,
- date,
- folio/page/image,
- stable locator or URL,
- image filename,
- digital archive identifier,
- access method.

A secondary citation must not silently become primary evidence.

Manuscript evidence should preserve the actual image, page, folio, or other verifiable locator whenever available.

---

## 4. Evidence Event

An Evidence Event records a bounded observation about a source.

Evidence answers:

> **What is directly observable in, explicitly stated by, or otherwise traceable to a documented source?**

An Evidence Event may contain:

- source reference,
- finding reference,
- literal observation,
- extraction method,
- transcription provenance,
- verification information,
- bounded metadata.

An Evidence Event must not silently contain conclusions exceeding the observation.

Example:

> “Joane Greene his wife”

is an evidence observation.

Claims about Joan's origin, ancestry, cultural affiliation, identity as another named person, birthplace, literacy, or other inferred characteristics are separate propositions requiring their own claims and explicit relationships.

---

## 5. Claim

A Claim is a proposition being investigated, tested, supported, contradicted, suspended, discounted, or rejected.

A Claim is not an Evidence Event.

Current claim types are:

- `FACTUAL`
- `HYPOTHESIS`

A Claim may exist before it is proven. Existence does not imply acceptance.

The authoritative claim text lives in the Claim record.

Relationships reference `claim_id`; they must not create a second authoritative copy of the claim text.

A Claim must not duplicate a literal observation as a substitute for evidence provenance.

---

## 6. Claim–Evidence Relationship

A Claim–Evidence Relationship explicitly records how a specific Evidence Event is being used in relation to a specific Claim.

A relationship must identify:

- `relationship_id`,
- `evidence_id`,
- `claim_id`,
- relation type,
- bounded scope,
- provenance.

The canonical relation vocabulary is:

- `DIRECTLY_SUPPORTS`
- `CONTEXT_ONLY`
- `DOES_NOT_ESTABLISH`
- `CONTRADICTS`

No probabilistic relationship vocabulary such as `PROBABLY_SUPPORTS`, `LIKELY_SUPPORTS`, or `MOSTLY_SUPPORTS` is permitted.

---

## 7. Relationship Semantics

### DIRECTLY_SUPPORTS

The literal evidence directly supports the bounded claim as stated.

It does not authorize broader inference.

`DIRECTLY_SUPPORTS` does not mean that the claim is proven, verified, or historically true.

For example:

> “Joane Greene his wife”

may directly support:

> “Joan/Joane Greene is named as the wife of John Greene.”

It does not, by itself, establish Joan's origin, ancestry, culture, birthplace, literacy, identity as another named person, or any other broader proposition.

### CONTEXT_ONLY

The evidence provides relevant historical or documentary context but does not itself establish the claim.

### DOES_NOT_ESTABLISH

The evidence is relevant to the investigation but explicitly does not establish the claim.

This is first-class negative knowledge and must remain preserved.

### CONTRADICTS

The evidence conflicts with the claim or with another evidentiary assertion relevant to the claim.

Contradictory evidence must not be silently discarded.

---

## 8. No Silent Evidence Inheritance

The machine must not infer a relationship merely because:

- evidence and claim occur in the same finding,
- evidence and claim occur in the same source,
- evidence and claim occur in the same research run,
- names appear similar,
- locations appear similar,
- dates appear compatible,
- family relationships appear compatible,
- wording appears semantically similar,
- multiple AI systems agree.

The relationship must be explicit.

Required chain:

**SOURCE → EVIDENCE EVENT → EXPLICIT RELATIONSHIP → CLAIM**

---

## 9. Boundedness Rule

A relationship must remain bounded to the claim actually stated.

The machine must not silently broaden:

**observation → claim A → claim B → claim C**

and treat the original observation as supporting every downstream proposition.

Each proposition requiring evidentiary support must have an explicit evidentiary relationship.

---

## 10. Append Boundary

`append_event.py` is a structural boundary only.

It may:

- load the applicable schema,
- validate required fields,
- validate field types and formats,
- validate IDs,
- reject malformed records,
- reject unknown fields,
- reject duplicate IDs,
- append valid records.

It must not:

- determine historical truth,
- determine evidentiary sufficiency,
- determine claim status,
- determine source credibility,
- determine identity,
- determine ancestry,
- determine cultural affiliation,
- infer relationships across records,
- or decide whether a historical proposition is true.

In particular, the append layer must not require referenced Claim or Evidence records to exist merely to append a structurally valid Relationship.

Cross-record provenance belongs to the Provenance Gate.

---

## Discovery, Preservation, and Promotion Separation

Research discovery, research preservation, search priority, evidentiary
eligibility, hypothesis promotion, and historical status are distinct
operations.

A research lead may be preserved even when it is:

- unverified,
- unsupported by currently located evidence,
- contradicted by some evidence,
- not selected for the current search run,
- deferred by a processing budget,
- blocked by a provenance gate,
- blocked by a promotion gate,
- or not selected as a Best Hypothesis.

Failure of an evidence gate or promotion gate is not, by itself,
failure of the research lead.

In particular:

- `DEFERRED` does not mean `REJECTED`.
- `NOT PROMOTED` does not mean `FALSE`.
- `UNSUPPORTED` does not mean `DISPROVEN`.

`UNSUPPORTED` is a conceptual research condition in this contract unless and until it is explicitly defined as a machine-readable status. It must not be treated as an implicit Claim status or silently mapped to a terminal status.
- `NOT SELECTED` does not mean `DISCARDED`.
- `BEST_HYPOTHESIS` does not mean competing hypotheses are eliminated.

A lead may enter a negative, rejected, discounted, or otherwise terminal
historical status only through the explicit process applicable to that
status and with its supporting reasoning and evidence preserved.

No processing budget, ranking mechanism, synthesis step, provenance
failure, or Best Hypothesis decision may silently convert a preserved
research lead into a terminal research status.

This establishes the following separation:

    DISCOVERY
        ↓
    PRESERVATION
        ↓
    SEARCH PRIORITY
        ↓
    EVIDENCE ELIGIBILITY
        ↓
    HYPOTHESIS PROMOTION
        ↓
    HISTORICAL STATUS

These layers may interact through explicit, auditable transitions, but
one layer must not silently substitute for another.

## 11. Provenance Gate

The Provenance Gate determines whether a proposed claim has an explicit and traceable evidentiary chain.

It may verify that:

- referenced Claim records exist,
- referenced Evidence records exist,
- referenced Relationships exist,
- identifiers resolve to the referenced records,
- Evidence contains required provenance and bounded observation,
- the Relationship contains an allowed relation type,
- the Relationship scope is present and bounded,
- provenance information is present.

Identifier resolution is structural: it means confirming that the referenced record exists and has the referenced identifier. It does not mean judging whether the record's content supports the claim.

The Provenance Gate verifies that the provenance state required by a requested status is present; it does not authorize the status transition.

The Provenance Gate must not determine historical truth.

Its output is a provenance judgment such as:

- `PROVENANCE PASS`
- `PROVENANCE BLOCKED`

It must not output a historical truth judgment such as TRUE/FALSE.

---

## 12. Status Gate

The Status Gate answers a different question:

> Given the available provenance and applicable research-control rules, is a requested status transition structurally permitted?

The Status Gate must not independently determine historical truth.

Status vocabulary must not be silently invented, renamed, collapsed, or migrated by the Provenance Gate.

Current and legacy status vocabularies must be explicitly reconciled before machine enforcement changes are made.

---

## 13. Legacy Vocabulary Firewall

Historical terminology must remain distinguishable from current machine status.

In particular:

`legacy_history.historical_status` is historical metadata only.

It has no authority over the current Claim `status`.

The machine must never automatically promote, translate, or reinterpret a legacy status such as `PROVEN`, `PROBABLE`, `UNVERIFIED`, `NULL`, or `SUSPENDED` as a current status merely because that vocabulary appears in historical research records.

Any migration or reconciliation must be explicit, tested, and auditable.

---

## 14. Verification Scope

Verification is always scoped.

Human verification of one feature does not verify all features of a source.

For example, verifying that Joan does not sign or mark a particular image does not automatically verify:

- every word,
- every name,
- every boundary,
- every mark,
- every officer role,
- or the complete transcription.

Verification records should identify reviewer, date, object checked, and verification scope.

---

## 15. AI Provenance

AI may create Evidence Events, Claims, Relationships, Reviews, and Research Events when the applicable schema and process permit.

AI-created records must preserve actor and platform provenance.

AI transcription is an aid unless independently verified.

Agreement between AI systems is not independent historical corroboration.

Multiple AI systems repeating the same inference do not create additional documentary evidence.

AI reasoning may generate leads, hypotheses, comparisons, challenges, and proposed relationships, but those outputs must remain distinguishable from source-derived evidence.

---

## 16. Append-Only Research History

Research-control assertions are historical records.

Once recorded, an AI or human assertion must not be silently rewritten to make the historical record cleaner.

When an assertion is challenged or corrected, preserve the sequence:

**ORIGINAL ASSERTION → CHALLENGE / REVIEW → CORRECTION OR NEW EVIDENCE → CURRENT INTERPRETATION**

Corrections should normally be represented by new records or events rather than destructive rewriting.

---

## 17. Contradiction Preservation

Contradiction is research data.

Preserve:

- supporting evidence,
- contradictory evidence,
- rejected interpretations,
- suspended hypotheses,
- negative findings,
- failed tests,
- challenged relationships.

A later interpretation must not erase the evidentiary history that preceded it.

---

## 18. Negative Knowledge

Meaningful negative results must remain discoverable.

Examples include:

- `DOES_NOT_ESTABLISH`,
- `CONTRADICTS`,
- failed searches,
- rejected identity paths,
- suspended hypotheses,
- source mismatches,
- unsuccessful tests.

Negative knowledge prevents future agents from reconstructing reasoning that has already been tested and rejected or shown to be insufficient.

---

## 19. No Historical Keyword Firewall

The architecture is domain-neutral.

No special machine rule may privilege or suppress hypotheses concerning:

- Narragansett,
- Anashuecot,
- English,
- Irish,
- Black,
- servant,
- enslaved,
- literate,
- illiterate,
- widow,
- immigrant,
- or any other historical identity or classification.

The same provenance, evidence, contradiction, and status rules must apply regardless of the hypothesis being tested.

---

## 20. No Algorithmic Contamination

The machine must not manufacture documentary evidence through inference chains.

The following are not independent historical evidence merely because an algorithm produces them:

- name similarity,
- geographic proximity,
- chronological compatibility,
- family-tree proximity,
- similar handwriting or marks,
- semantic similarity,
- repeated AI conclusions,
- database co-occurrence,
- inferred kinship,
- inferred identity.

Such outputs may generate leads or hypotheses, but must remain distinguishable from source-derived Evidence Events.

---

## 21. Human and AI Roles

AI may aggressively search, extract, compare, challenge, test, and propose.

Humans and AI may disagree.

Disagreement must remain visible.

The control plane is not intended to prevent AI participation. Its purpose is to prevent invisible AI reasoning from becoming indistinguishable from documentary evidence.

---

## 22. Event Spine

The Event Spine is an audit representation.

It may aggregate:

- source events,
- evidence events,
- relationships,
- claims,
- reviews,
- status events,
- contradictions,
- corrections,
- research events.

The Event Spine is not an independent truth source.

It must not silently rewrite underlying records.

Its purpose is chronological transparency and auditability.

---

## 23. Separation of Concerns

The architectural responsibilities are:

| Component | Responsibility |
|---|---|
| `append_event.py` | Structural validity |
| Provenance Gate | Evidentiary traceability |
| Status Gate | Permitted status transitions |
| Hostile Review | Challenge, contradiction, and alternative testing |
| Event Spine | Chronological audit representation |
| Research Process | Interpretation, testing, and documented conclusions |

No component may silently assume another component's responsibilities.

---

## 24. Synthetic Testing Firewall

Control-plane tests should use synthetic Claims, Evidence Events, and Relationships whenever possible.

Historical Joan evidence is not required to prove that the machinery works.

Architecture tests must remain independent of historical conclusions so that the control system does not become contaminated by assumptions about Joan's identity, origin, ancestry, or affiliation.

---

## 25. Change Discipline

Before changing a control-plane rule:

1. State the architectural rule being changed.
2. Add or modify a regression test describing the intended behavior.
3. Confirm the test fails for the old behavior when appropriate.
4. Implement the smallest production change necessary.
5. Run the relevant regression suite.
6. Inspect resulting records.
7. Preserve unrelated working-tree changes.
8. Do not silently migrate, delete, or rewrite historical research records.
9. Document consequential architectural changes.

---

## 26. Final Rule

Always preserve the distinction between:

**WHAT THE SOURCE SHOWS**

→ **WHAT THE RESEARCHER OR AI OBSERVES**

→ **HOW THE OBSERVATION IS USED**

→ **WHAT CLAIM IS TESTED**

→ **WHAT STATUS THE SYSTEM PERMITS**

→ **WHAT HISTORICAL CONCLUSION THE RESEARCH SUPPORTS**

These are different layers.

The machine must never silently collapse them.

---

**End of Architecture Contract**
