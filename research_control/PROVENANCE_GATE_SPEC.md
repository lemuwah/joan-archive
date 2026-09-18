# Provenance Gate Specification

**Status:** DESIGN — not yet enforced in production  
**Created:** 2026-09-15  
**Purpose:** Define the minimum evidence/provenance requirements before research findings can become machine-auditable claims.

---

## 1. Governing Principle

> **Laws govern the machine; evidence governs conclusions.**

The Provenance Gate does not determine historical truth.

Its job is to prevent an unsupported transition from:

`source → observation → claim → status`

and to preserve the distinction between:

- what a source literally contains,
- what an AI or human extracts from it,
- what is inferred,
- what is hypothesized,
- what has been tested,
- and what has been human-verified.

AI may be aggressive in discovery.

The archive must remain conservative in evidentiary status.

---

## 2. Human-Readable Findings Remain the Research Record

Existing files under `research_findings/` are not replaced by the control plane.

A finding may contain:

- source description,
- transcription,
- observations,
- interpretation,
- uncertainty,
- human review,
- contradictions,
- research conclusions,
- next tests.

The control plane creates a structured audit representation of that work.

It must not silently rewrite, delete, or smooth the original finding.

---

## 3. Required Provenance Chain

Every structured claim must be traceable through:

`SOURCE → EVIDENCE EVENT → EXPLICIT RELATIONSHIP → CLAIM`

A claim without a traceable supporting observation is not eligible for evidentiary promotion.

A source may support multiple observations.

An observation may support multiple claims.

A claim may require multiple observations.

The relationship must be explicit.

The machine must never infer a claim-to-source relationship merely because two statements occur in the same document.

---

## 4. Source Identity

A source record should identify, where available:

- repository
- collection
- document or record identifier
- date
- folio/page/image
- stable locator or URL
- image filename
- digital archive identifier
- access method

For manuscript evidence, the existence of an actual image/page reference must be preserved.

A secondary citation must not be silently represented as a primary source.

---

## 5. Observation Layer

An observation describes what is actually present in the source or what is explicitly established by documented human review.

Examples:

- "Joane Greene his wife" appears in the instrument.
- John Greene signs the instrument.
- No Joan signature or mark is visible on the reviewed instrument.
- The instrument identifies James Greene as the natural son of John and Joan Greene.

Observations must not contain conclusions that exceed the source.

---

## 6. Transcription Provenance

Every transcription must identify its provenance.

Permitted distinctions include:

- `AI_TRANSCRIPTION`
- `HUMAN_TRANSCRIPTION`
- `HUMAN_VERIFIED_AI_TRANSCRIPTION`

An AI transcription is a research aid unless independently verified.

AI agreement is not corroboration.

A machine-generated transcription must not automatically become citation-grade evidence.

---

## 7. Human Verification

Human verification must identify:

- reviewer
- date
- what was actually checked
- scope of the verification

Verification of one feature does not automatically verify every feature in the source.

For example:

If a reviewer confirms that Joan does not sign or mark the deed, that does not automatically confirm:

- every word of the transcription,
- the exact shape of another person's mark,
- recording officers' roles,
- or every boundary description.

---

## 8. Observation vs Interpretation

The system must preserve a hard distinction between:

### Observation

What the source/document visibly or explicitly says.

### Interpretation

What a researcher thinks the observation may mean.

Interpretation must never silently become observation.

Example:

**Observation:**

"Joane Greene his wife" appears in the deed.

**Interpretation:**

Joan was the wife of John Greene at the time of the deed.

The latter is a reasonable reading of the document, but the relationship must remain traceable to the former.

---

## 9. Evidence–Claim Relationship

An evidence event does not support a claim merely because both appear in the same finding, source, document, or research run.

Every machine-auditable claim must have an explicit relationship to the evidence offered for it.

The machine may verify that the relationship is declared and structurally valid. It must not infer the relationship from:

- shared wording
- matching names
- locality
- chronology
- family association
- similar marks
- semantic similarity
- co-occurrence in the same document
- agreement between AI systems

### 9.1 Required Relationship

A claim that relies on evidence must identify the evidence event and declare the relationship between that evidence and the claim.

Initial relationship vocabulary:

- `DIRECTLY_SUPPORTS` — the literal observation directly supports the bounded claim stated.
- `CONTEXT_ONLY` — the observation provides relevant historical context but does not itself establish the claim.
- `DOES_NOT_ESTABLISH` — the observation is relevant to the investigation but cannot establish the proposed claim.
- `CONTRADICTS` — the observation conflicts with the proposed claim or with another evidentiary assertion.

`DIRECTLY_SUPPORTS` is a declared relationship asserted by the researcher or agent. Structural validation verifies that the relationship is well-formed and properly attributed; it does not independently determine that the evidence historically supports the claim.

The relationship is not itself proof that the historical claim is true.

### 9.2 No Silent Evidence Inheritance

The machine must never perform this transformation automatically:

```text
finding contains observation
        ↓
claim appears in same finding
        ↓
observation assumed to support claim
```

Instead, the required structure is:

```text
source
  ↓
evidence event
  ↓
literal observation
  ↓
explicit evidence–claim relationship
  ↓
claim
```

### 9.3 Bounded Support

DIRECTLY_SUPPORTS must refer to the claim as actually stated, not to a broader proposition silently derived from it.

Example:

Observation:
"Joane Greene his wife"

Claim:
"Joan/Joane Greene is named as the wife of John Greene."

Relationship:
DIRECTLY_SUPPORTS

The same observation does not automatically support:

"Joan was Narragansett."
"Joan was Anashuecot."
"Joan was born in Rhode Island."
"Joan was literate."

Those propositions require their own evidentiary basis and testing.

### 9.4 Relationship Is Not a Truth Oracle

The provenance gate does not decide whether a declared relationship is historically correct.

Its responsibility is to ensure that:

the evidence exists;
the source and finding are identifiable;
the literal observation exists;
the evidence–claim relationship is explicitly declared;
the relationship is structurally valid;
the provenance state required by a requested status is present.

Substantive evaluation remains subject to the hypothesis-testing, hostile-review, Seven-Law, and status systems.

A structurally valid relationship therefore means:

"The agent has explicitly stated how it is using this evidence."

It does not mean:

"The machine has determined that the historical claim is true."

### 9.5 No Keyword or Vocabulary Firewall

This requirement must remain structural rather than dependent on a blacklist of historical terms.

The gate must not need special rules for:

Narragansett
Anashuecot
English
Irish
servant
enslaved
literate
illiterate
widow
or any future hypothesis.

The same provenance architecture must work for claims not yet imagined by the researchers.

## 10. Claim Requirements

A structured claim should contain:

- claim identifier
- claim text
- supporting evidence references
- source status
- current status
- observation basis
- true test
- false test
- alternative hypotheses
- contradiction references where applicable
- provenance

A claim that lacks an explicit supporting evidence reference does not satisfy the provenance requirements for evidentiary promotion.

---

## 11. Falsification Requirement

Every substantive hypothesis must have a test capable of weakening or rejecting it.

The system should preserve both:

- `true_test`
- `false_test`

A claim without a meaningful falsification path remains an open research proposition.

---

## 12. Alternative-Hypothesis Requirement

A claim concerning Joan's identity must not be evaluated in isolation.

Relevant alternatives must remain visible when applicable.

Examples include:

- Narragansett origin
- English origin
- Irish origin
- mixed English/Narragansett parentage
- undocumented origin
- other currently open models

The control plane must not eliminate an alternative merely because another hypothesis has received more attention.

---

## 13. Negative Evidence

A negative search is evidence about the searched scope, not proof that a record never existed.

Every negative-search result should preserve:

- query
- repository searched
- collection/scope
- date searched
- search method
- result

The machine must reject transformations such as:

`No English baptism found → Joan was Narragansett`

unless independent evidence explicitly supports that conclusion.

---

## 14. Non-Conclusion Rule

The absence of evidence for X must not automatically become evidence for Y.

Examples of prohibited automatic reasoning:

- No English baptism → Narragansett.
- No signature → illiterate.
- No surname → maiden name inferred from another Joan.
- Same mark → same person.
- Same locality → same person.
- Similar name → same person.
- Family association → identity established.

These may become hypotheses for testing, but not automatic conclusions.

---

## 15. Status Gate

The Status Gate determines whether a proposed status transition is permitted by the available evidence and provenance state.

The Provenance Gate supplies the provenance-state check required for that decision.

The Status Gate does not itself prove a historical claim.

At minimum:

### AI-only / unverified

May support:

- lead
- open question
- proposed hypothesis
- research target

May not support:

- PROOF
- VERIFIED
- CERTAIN
- IDENTIFIED
- equivalent certainty labels

### Human-verified primary evidence

May support an appropriately bounded evidence claim.

The scope of verification must match the scope of the claim.

### Best Hypothesis

`BEST_HYPOTHESIS` is not equivalent to `PROOF`.

It remains subject to adversarial testing.

---

## 16. Seven-Law Compatibility

The gate must preserve the seven Laws:

1. No Narrative Smoothing
2. La Mance Law / Follow the Rivers
3. No Premature Elimination
4. No Algorithmic Contamination
5. No Jurisdictional Assumption
6. No Centering
7. No Trust Without Evidence

A structurally valid provenance chain does not override the Laws.

---

## 17. Contradictions and Contamination

Contradictions must be recorded, not silently resolved.

AI errors, hallucinations, fabricated references, circular claims, and other contamination events must remain auditable.

A later correction must not erase the earlier research event.

The system should preserve:

`original claim → contradiction/correction → current status`

---

## 18. 1682 Home-Place Deed Test Case

The first implementation must be tested against:

`FINDING-fe55dd3e755e`

Source:

`RI State Archives Land Records No. 1, folios 259–260`

Image:

`1682_homeplace_james_instrument_manuscript_folios259-260_RIStateArchives.jpg`

Preservica identifier:

`IO_6f6b6c51-8275-4e3a-95d9-c1e205f459f7`

The test must distinguish at least the following:

### Permitted evidence claims

- Joan/Joane Greene is named as John Greene's wife in the instrument.
- Joan/Joane is named as recipient of a life provision after John's death.
- Joan does not sign or make a mark on the reviewed instrument, based on documented human review.
- James Greene is described in the transcript as the natural son of John and Joan Greene, subject to the stated transcription provenance.

### Unresolved

- Exact secretary-hand wording where still AI-read.
- Exact shape of Henry Tibbetts's mark.
- Recording-authority roles where still AI-read.

### Claims that must be blocked absent independent evidence

- Joan was Anashuecot.
- Joan was Narragansett.
- Joan was English.
- Joan was Irish.
- Joan was a servant.
- Joan was enslaved.
- Joan was illiterate because she did not sign.
- Joan's maiden name was Beggarly.
- The 1682 deed establishes Joan's ethnic or birth identity.

---

## 19. Adversarial Test Suite

The first implementation should include tests for:

1. Valid source → observation → bounded claim → allowed.
2. Missing source → blocked.
3. Missing observation → blocked.
4. Claim with no evidence reference → blocked.
5. AI transcription presented as human verification → blocked.
6. Unsupported identity inference → blocked.
7. Negative search used as proof of alternative identity → blocked.
8. Absence of signature used to infer illiteracy → blocked.
9. Missing falsification test → blocked.
10. Missing alternatives for an identity hypothesis → blocked.
11. Valid four-agent Seven-Law chain → allowed by process gate.
12. Process approval must not convert a hypothesis into Proof.

---

## 20. Separation of Responsibilities

The control plane should remain modular.

### Finding

Human-readable research record.

### Evidence Event

Machine-auditable source observation.

### Claim

A proposition being tested.

### Provenance Gate

Checks that the claim is traceable and appropriately bounded.

### Law Guard

Checks prohibited certainty promotion and Law requirements.

### Best Hypothesis Gate

Checks required adversarial research process.

### append_event.py

Checks structural ledger validity:

- schema
- identifier
- duplicate prevention
- valid JSON

### Event Spine

Permanent chronological audit trail.

No component should silently assume another component's job.

---

## 21. Design Test Before Production Enforcement

The first implementation must be tested against the 1682 deed before being connected to the production research flow.

The expected goal is not:

"make the system approve Joan."

The expected goal is:

"make the system correctly distinguish what this document establishes from what it does not establish."

If the machine cannot make that distinction, production enforcement must wait.

---

## 22. Core Principle

> **Evidence may support a claim only through an explicit, auditable provenance relationship.**

> **A valid process chain is not historical proof.**

> **A passing Provenance Gate means the required evidentiary and provenance state is present; it does not mean the Status Gate has authorized a status transition or that the historical proposition is true.**

> **The archive preserves uncertainty rather than manufacturing certainty.**
