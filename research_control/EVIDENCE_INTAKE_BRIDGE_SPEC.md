# Evidence Intake Bridge Specification

**Status:** DESIGN  
**Version:** 0.1  
**Created:** 2026-09-19

## 1. Purpose

The Evidence Intake Bridge is a narrow intake adapter between a
human-reviewed candidate source and the structured Evidence Event ledger.

Its purpose is to preserve documentary observations in a structured,
auditable form without deciding historical truth.

The bridge is an intake mechanism, not a historical-status engine,
claim generator, identity resolver, synthesis engine, or publication
engine.

Governing principle:

> Evidence records what a source shows. It does not decide what history
> means.

---

## 2. Architectural Position

The Evidence Intake Bridge is an AI-first intake adapter between research activity and the structured Evidence Event ledger.

The canonical path is:

SEARCH / AGENTS
→ EVENT SPINE
→ RESEARCH FINDING
→ AI SEARCH / READING / EXTRACTION / TRANSCRIPTION / ANALYSIS
→ AI EVIDENCE EVENT
→ optional human verification
→ explicit relationship
→ claim
→ review / status
→ public projection

A candidate record may be an upstream input to this process, but a human-authorized candidate is NOT a prerequisite for recording an AI Evidence Event.

The bridge owns the controlled transition from documented source-reading work into an Evidence Event. It does not decide historical truth.

Human verification, when it occurs, is a later verification state or process. It is not an admission requirement for AI research to be recorded.

The bridge must preserve enough upstream lineage to show how the Evidence Event arose, including applicable search, finding, candidate, research-run, and review-packet identifiers.

## 3. Core Invariant

The existence of an Evidence Event does not establish the truth of any
historical claim.

Likewise:

> The existence of a Candidate, Finding, Review Packet, Evidence Event,
> or explicit Evidence–Claim Relationship must not by itself promote a
> claim to a higher historical status.

Historical status remains controlled by the control-plane review/status
architecture.

---

## 4. AI Evidence Admission Gate

An AI-generated Evidence Event may be admitted without prior human verification.

Admission requires:

1. a source identity sufficient to locate the source;
2. a literal observation explicitly reported as source-derived;
3. actor provenance identifying the AI system;
4. platform provenance;
5. recording timestamp;
6. recoverable upstream lineage when the event originated from a finding, search, candidate, research run, or review packet;
7. an explicit AI disclaimer;
8. no attempt to convert inference into literal observation;
9. no attempt to create or promote a claim, relationship, or status.

AI-generated Evidence Events MUST NOT be labeled `PRIMARY_VERIFIED`.

`PRIMARY_READ`, `READ`, `LOCATED_UNREAD`, and other non-verification source states may be used when their semantics are satisfied by the documented work.

The absence of human verification is recorded as an explicit state. It is not treated as a reason to erase or discard the AI research record.

A later human verification process may independently verify an AI-generated Evidence Event. Such verification must remain distinguishable from the original AI event and must not rewrite the original actor provenance.

## 5. Candidate-to-Evidence Mapping

The bridge may copy or normalize source-level facts that are already
authorized by the candidate record.

| Candidate field | Evidence field | Rule |
|---|---|---|
| `candidate_id` | lineage field | Must remain traceable |
| `source_url` | `source.locator` | Preserve source locator |
| `repository` | `source.repository` | Preserve repository |
| `repository_id` | source identity | Preserve when present |
| `document_type` | source metadata | Preserve, do not reinterpret |
| `image_or_page` | `source.page_or_image` | Preserve required anchor |
| `retrieved_at` | provenance context | Preserve access history |
| `ai_outputs` | transcription context | Never treat as human observation |
| `proposed_claims` | none automatically | Never create claims |
| `human_disposition` | none automatically | Never become historical status |
| `negative_result` | none automatically | Do not convert into documentary evidence |

The bridge must not silently convert candidate metadata into historical
claims.

---

## 6. Source Identity Preservation

Every Evidence Event must preserve enough information to identify the
source independently.

Where available, preserve:

- repository
- collection
- document or record identifier
- date
- folio/page/image
- stable locator or URL
- image filename
- digital archive identifier
- access method
- checksum
- relevant access notes

For manuscript evidence, an image/page anchor is required by the
Provenance Gate.

The bridge must never replace an original source identity with a
secondary citation merely because the secondary citation is easier to
process.

---

## 7. Observation Boundary

`literal_observation` is the most important field in the Evidence Event.

It must contain only what the source literally shows or what has been
explicitly established through documented human review.

The bridge must not manufacture observations from:

- proposed claims
- agent summaries
- semantic similarity
- name similarity
- chronology
- locality
- genealogy
- family-tree relationships
- handwriting resemblance
- AI agreement
- secondary narrative
- model inference

Example:

    literal_observation:
    "Joane Greene his wife"

may support an Evidence Event derived from the actual document.

It must not be automatically transformed into:

    "Joan was Narragansett."

Nor:

    "Joan was Anashuecot."

Nor:

    "Joan was the daughter of X."

Those are interpretive or hypothetical claims requiring separate
control-plane treatment.

---

## 8. Transcription Boundary

AI transcription is a research aid and must remain distinguishable from the source itself.

The bridge may preserve:

- AI-generated working transcription;
- human-produced transcription;
- human verification of an AI transcription;
- uncertainty markers;
- image or page anchors;
- transcription-specific provenance.

An AI transcription does not become a verified transcription merely because the text is plausible, agrees with another AI system, resembles a known name, or supports an existing hypothesis.

Multiple AI systems producing the same transcription or interpretation do not constitute independent documentary corroboration.

If transcription provenance is uncertain or cannot be distinguished from interpretation, the bridge must fail closed or quarantine the affected field rather than silently upgrading it.

The Evidence Event must keep transcription separate from `literal_observation` and must keep interpretation separate from both.

## 9. Interpretation Boundary

`interpretation` is not `literal_observation`.

The bridge must preserve the distinction.

If a candidate contains both a literal observation and an interpretation:

- the literal observation belongs in the observation layer
- the interpretation remains separately labeled
- neither may silently replace the other

A bridge implementation must reject or quarantine ambiguous input rather
than deciding which layer a statement belongs in.

---

## 10. Claim Firewall

The bridge must never create `CLAIM-*` records.

In particular, it must never:

- transform `proposed_claims` into claims
- assign a claim identifier
- promote a claim
- change claim status
- infer claim text from an observation
- select a preferred hypothesis
- eliminate a competing hypothesis

Claim creation belongs to a separate control-plane operation.

The Evidence Event may contain `claim_refs` only when those references
are explicitly supplied through an authorized control-plane process.

The bridge itself must not invent them.

---

## 11. Relationship Firewall

The bridge must never create `REL-*` records.

An Evidence–Claim relationship is a separate, explicit act.

The bridge must not infer relationships from:

- wording
- name similarity
- locality
- chronology
- co-occurrence
- family association
- similar marks
- AI agreement
- semantic similarity

The relationship vocabulary remains:

- `DIRECTLY_SUPPORTS`
- `CONTEXT_ONLY`
- `DOES_NOT_ESTABLISH`
- `CONTRADICTS`

The bridge does not decide which relationship is historically correct.

---

## 12. Status Firewall

The bridge must never create `STATUS-*` records.

In particular:

- candidate `VERIFIED_PRIMARY` does not become claim `VERIFIED`
- candidate `VERIFIED_SECONDARY` does not become claim `VERIFIED`
- human source disposition does not become historical claim status
- evidence existence does not become historical proof
- intake does not equal promotion

The distinction must remain explicit:

    source verified
        !=
    claim verified

---

## 13. Identity Firewall

The bridge must not resolve identity.

It must not merge people because they share:

- a first name
- a surname
- a place
- a date
- an occupation
- witnesses
- relatives
- a handwriting mark
- a household
- a geographic pattern

A source may contain a person name without establishing which
historical person that name represents.

Identity disambiguation belongs to a separate review process.

This is especially important for the Joan Greene research, where name
collision and family-tree inference are active research risks.

---

## 14. Contradiction Preservation

If an authorized candidate contains a contradiction, uncertainty, or
contamination warning, the bridge must preserve it.

The bridge must not:

- remove inconvenient observations
- choose the cleaner reading
- collapse competing interpretations
- rewrite a disputed transcription as certain
- delete contradictory evidence
- convert uncertainty into a positive claim

Contradiction fields should remain traceable through the Evidence Event
where supported by the schema.

A contradiction is research information, not an error to be cleaned up.

---

## 15. Negative Results

Negative searches are not automatically documentary Evidence Events.

A negative-result candidate may remain in the research/search layer with:

- query
- repository searched
- scope searched
- date searched
- search method
- result

A separate design may later define how negative evidence is represented
in the evidence layer.

The bridge must not fabricate a documentary source for a negative search.

---

## 16. Provenance and Work Traceability

Evidence provenance and actor provenance are distinct but connected.

Source provenance answers:

- What source was used?
- Where is it located?
- What repository or collection holds it?
- What document, folio, page, image, or stable locator identifies it?
- How was it accessed?
- What digital image or archive identifier permits recovery?

Actor provenance answers:

- Who or what recorded the Evidence Event?
- Which AI system or human actor performed the work?
- On what platform?
- When was the event recorded?
- What upstream research activity produced it?

The bridge MUST preserve recoverable lineage from the Evidence Event back to its upstream research activity.

The bridge MUST NOT overload a free-text session field as the sole machine-readable lineage mechanism.

A dedicated structured lineage representation should be used for identifiers such as:

- `finding_id`
- `candidate_id`
- `search_event_id`
- `research_event_id`
- `review_packet_id`

The exact schema representation must be resolved before production implementation.

AI-generated records must carry the archive's explicit AI disclaimer. The disclaimer is provenance information, not a substitute for verification and not a statement that the underlying historical proposition is true.

## 17. Lineage Requirement

Every Evidence Event produced through the bridge must be traceable to the research work that produced it.

Where applicable, the lineage chain is:

SEARCH
→ EVENT
→ FINDING
→ CANDIDATE
→ EVIDENCE

An AI agent may enter the Evidence Event path directly from a documented finding or research run when no candidate record exists.

A candidate identifier must never be replaced by free-text description when a candidate record exists.

Lineage identifies the history of the research artifact. It does not establish the truth of the historical proposition contained in or associated with that artifact.

Loss of required lineage must fail closed when the missing identifier is necessary to reconstruct how the Evidence Event was produced.

## 18. Idempotency

The bridge must prevent accidental duplicate intake.

Repeated processing of the same candidate must not silently create
multiple indistinguishable Evidence Events.

The implementation should use a deterministic intake key based on the
candidate identity and relevant source/version information.

If an equivalent Evidence Event already exists, the bridge should
report that condition rather than silently append another event.

Any exception must be explicit and auditable.

---

## 19. Failure-Closed Conditions

The bridge must fail closed or quarantine the affected record when any of the following occurs:

- source identity is absent or materially incomplete;
- literal observation is absent;
- the purported observation is actually an inference, interpretation, hypothesis, or narrative conclusion;
- actor provenance is absent;
- AI platform provenance is absent for an AI-generated event;
- required AI disclaimer is absent;
- source location cannot be recovered when required by the applicable provenance rule;
- AI-generated work is labeled `PRIMARY_VERIFIED`;
- AI-generated work is represented as human verification;
- transcription and observation provenance cannot be distinguished;
- an attempted claim is silently created from `proposed_claims`;
- an attempted relationship is silently created;
- an attempted historical status promotion occurs;
- contradictory source identity or lineage cannot be resolved without silently choosing one;
- duplicate intake cannot be distinguished from a new Evidence Event;
- schema or vocabulary requirements are incompatible.

Failure-closed means the bridge does not silently repair, infer, promote, or narratively smooth the record.

The research work may remain visible as a finding, search result, review artifact, or quarantined intake even when an Evidence Event cannot safely be created.

## 20. Write Boundary

The bridge may write only through the approved Evidence Event append
mechanism.

It must not directly modify:

- `index.html`
- `analysis.html`
- `context.html`
- published timeline pages
- `evidence/`
- `people/`
- public research summaries
- `research_control/claims.jsonl`
- `research_control/review_events.jsonl`
- `research_control/status_events.jsonl`
- `research_control/relationships.jsonl`

It must not bypass `research_control/tools/append_event.py`.

It must not use direct file writes to the Evidence Event ledger.

---

## 21. Public Projection Boundary

The Evidence Intake Bridge has no public-page authority.

In particular:

    Candidate found
        !=
    Evidence accepted
        !=
    Claim established
        !=
    Public historical state

Public pages will eventually receive information only through a
separate Public Projection Layer.

The projection layer must consume eligible control-plane state rather
than reading raw research findings and deciding what they mean.

---

## 22. Relationship to the Research Event Spine

The Research Event Spine and Evidence Event ledger serve different
purposes.

The Event Spine answers:

> What research activity happened, who performed it, what was its
> parent event, and what happened next?

The Evidence Event answers:

> What documentary source was examined and what literal observation was
> recorded from it?

Therefore:

    EVENT SPINE
        |
        | research lineage
        v
    FINDING / CANDIDATE
        |
        | documentary intake
        v
    EVIDENCE EVENT

The bridge connects these layers through preserved lineage.

It does not collapse them into one event stream.

---

## 23. Relationship to Findings

A `research_findings/*.md` file remains the source-of-record research
artifact.

The bridge does not rewrite, replace, delete, or smooth findings.

A finding may contain:

- leads
- negative results
- context
- contradictions
- proposed interpretations
- source candidates
- uncertainty

Only an appropriately authorized candidate source may enter Evidence
Event intake.

A finding itself is not documentary evidence merely because it was
reviewed by four agents.

---

## 24. Relationship to Agent Review

The four-stage review funnel remains:

1. Archivist
2. Hostile Review
3. Synthesizer
4. Explorer

Their outputs are research and review artifacts.

They do not collectively vote a claim into proof.

Agent agreement is not independent corroboration.

The human authorization gate remains necessary before source-level
evidence intake.

---

## 25. Human Review Boundary

The bridge does not replace the human editor.

Human review establishes the source-level authorization required for
intake.

The human reviewer should be able to identify:

- what source was inspected
- what image/page was inspected
- what literal observation was verified
- what transcription was checked
- what remains uncertain
- what contradictions remain
- what source identity was confirmed

The bridge records that authorized documentary layer.

It does not reinterpret the reviewer's historical conclusions.

---

## 26. Synthetic Test Requirements

Before production use, the implementation must have tests covering at
least:

1. Valid verified-primary candidate enters intake.
2. Valid verified-secondary candidate enters intake.
3. Pending candidate is rejected.
4. Suspended candidate is rejected.
5. Rejected candidate is rejected.
6. Missing human disposition is rejected.
7. Missing repository ID is rejected for verified source.
8. Missing image/page anchor is rejected.
9. Invalid candidate schema is rejected.
10. Proposed claim is never converted into `CLAIM-*`.
11. Human disposition is never converted into `STATUS-*`.
12. Bridge never creates `REL-*`.
13. AI transcription remains visibly AI-derived.
14. Ambiguous transcription provenance fails closed.
15. Literal observation remains separate from interpretation.
16. Contradiction metadata survives intake.
17. Negative-result candidate is not fabricated into documentary evidence.
18. Candidate lineage is preserved.
19. Duplicate intake is detected.
20. Bridge cannot write to public pages or unrelated control ledgers.

Tests must use synthetic records where possible.

Regression tests must not modify production ledgers.

---

## 27. Production Safety Invariant

No research artifact becomes public historical state merely because it was:

- found;
- extracted;
- transcribed;
- synthesized;
- reviewed;
- repeated by multiple AI systems;
- judged plausible by an AI system;
- converted into an Evidence Event.

An AI Evidence Event records documented research work and a bounded source observation. It does not by itself establish historical truth.

Claims require explicit claim records.

Claim–Evidence relationships require explicit relationship records.

Historical status requires the separate status/control-plane process.

Public projection requires the approved control-plane path.

The archive therefore preserves the complete distinction:

AI work
≠ human verification
≠ documentary corroboration
≠ historical proof
≠ public historical status.

The purpose of the bridge is not to make AI conclusions authoritative. Its purpose is to make AI research auditable without requiring the researcher to manually reproduce every step.

## 28. Vocabulary Reconciliation Required Before Implementation

The current architecture contains a known vocabulary mismatch.

Evidence Event source access currently permits:

- `DIGITAL_IMAGE`
- `DIGITAL_TEXT`
- `PHYSICAL`
- `SECONDARY_REFERENCE`
- `AI_TRANSCRIPTION`
- `OTHER`

The Provenance Gate design separately distinguishes:

- `AI_TRANSCRIPTION`
- `HUMAN_TRANSCRIPTION`
- `HUMAN_VERIFIED_AI_TRANSCRIPTION`

These are not necessarily equivalent concepts.

Before implementation, determine whether transcription provenance belongs:

- in `access_method`
- in a dedicated transcription field
- in provenance metadata
- or in another explicit schema layer

Do not solve this mismatch implicitly inside the bridge.

---

## 29. Open Design Questions

The following remain intentionally unresolved:

1. Exact Evidence Event lineage field.
2. Exact transcription-provenance schema.
3. Whether source checksums are mandatory or conditional.
4. How human authorization is represented structurally.
5. How candidate version changes affect idempotency.
6. Whether multiple literal observations from one candidate become one or
   multiple Evidence Events.
7. How negative-search evidence should eventually be modeled.
8. How the future Provenance Gate will validate cross-record lineage.

These questions must be resolved through design review rather than
silently answered by implementation convenience.

---

## 30. Explicit Non-Goals

The Evidence Intake Bridge is not:

- a genealogy engine
- an identity resolver
- a best-hypothesis selector
- a source-ranking engine
- a truth detector
- an AI consensus mechanism
- a claim generator
- a status engine
- a relationship inference engine
- a publication engine
- a narrative generator
- a replacement for human source inspection

---

## 31. Governing Principle

The architecture must preserve the following separation:

    DISCOVERY
        !=
    SOURCE VERIFICATION
        !=
    DOCUMENTARY OBSERVATION
        !=
    INTERPRETATION
        !=
    HYPOTHESIS
        !=
    CLAIM
        !=
    HISTORICAL STATUS
        !=
    PUBLIC NARRATIVE

The bridge exists only to move authorized documentary observations into
the structured evidence layer while preserving those boundaries.

> No narrative smoothing.
>
> No inference laundering.
>
> No automatic promotion.
>
> Preserve the contradiction.
>
> Preserve the source.
>
> Preserve the uncertainty.
