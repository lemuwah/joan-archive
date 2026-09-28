# Contextualizer Contract

**Status:** DESIGN — NOT YET PRODUCTION  
**Created:** 2026-09-16  
**Purpose:** Define the controlled layer between source-grounded evidence and historical interpretation.

---

## 1. Purpose

The Contextualizer exists to expand the research space around an Evidence Event without changing the evidentiary status of that event.

It provides:

- historical and documentary context;
- multiple analytical perspectives;
- explicit assumptions and possible sources of distortion;
- alternative interpretations;
- possible record locations for further investigation;
- testable next steps.

The Contextualizer does **not** establish historical truth.

It does **not** convert interpretation into evidence.

It does **not** select a preferred hypothesis merely because one interpretation appears more coherent.

---

## 2. Core Architecture

The Contextualizer is a branching research layer, not a mandatory linear pipeline.

The research-control architecture is:

SOURCE
  |
  v
EVIDENCE EVENT
  |
  | Evidence Firewall
  v
CONTEXTUALIZATION
  |
  +--> CONTEXT
  |
  +--> PERSPECTIVES / LENSES
  |
  +--> BIAS / ASSUMPTION AUDIT
  |
  +--> RECORD-LOCATION HYPOTHESES
  |
  +--> NEXT TESTS
  |
  +--> INTERPRETATIONS
          |
          v
       HYPOTHESIS
          |
          | hypothesis testing
          v
      NEW EVIDENCE
          |
          v
        CLAIM

These branches are optional.

A Contextualization operation MAY legitimately end with:

- unresolved context;
- an unsearched record family;
- a competing perspective;
- an assumption requiring examination;
- a new research question;
- a Record-Location Hypothesis;
- a proposed test;
- no Interpretation.

The Contextualizer MUST NOT force every contextual observation into an Interpretation, Hypothesis, or Claim.

The direction of research flow does not authorize any lower-confidence layer to silently upgrade a higher-confidence layer.

---

## 3. Evidence Firewall

Evidence Events contain source-grounded observations.

The Contextualizer MUST NOT:

- rewrite a literal observation into a conclusion;
- treat an inference as though it were present in the source;
- add an identity assignment that the source does not establish;
- treat absence of a record as proof that an event or person did not exist;
- treat AI agreement as independent corroboration;
- promote contextual information into evidence without its own provenance;
- silently change the wording or scope of the underlying Evidence Event.

The Contextualizer MAY:

- identify questions raised by an Evidence Event;
- identify historical context relevant to interpreting the Evidence Event;
- identify alternative explanations;
- identify potentially relevant record systems;
- identify assumptions that require testing.

The Contextualizer MUST NOT manufacture an Evidence Event from its own output.

If Contextualization suggests that another record may exist, and a researcher subsequently locates that record, the newly located source MUST be processed as a NEW Evidence Event with its own source, literal observation, provenance, and verification status as applicable.

The following transformation is prohibited:

CONTEXTUALIZER OUTPUT
        |
        v
"therefore this is evidence"

Contextualization may generate a search.

A search may locate a source.

The source may generate a new Evidence Event.

The Contextualizer output itself does not become that Evidence Event.

---

## 4. Context

Context is information that helps explain the documentary or historical environment surrounding an Evidence Event.

Context MUST have identifiable provenance.

Context SHOULD distinguish between:

1. sourced historical context;
2. documentary/administrative context;
3. analytical context;
4. unresolved contextual questions.

Context MUST NOT be treated as evidence for the underlying claim merely because it is relevant.

A contextual statement that becomes material evidence MUST be represented separately as an Evidence Event.

---

## 5. Perspectives / Lenses

A **Perspective** is a deliberate analytical standpoint from which Evidence or Context is examined.

A Perspective is NOT a conclusion.

A **Lens** is a specific question, filter, or analytical operation applied under a Perspective.

For example:

Perspective:
RECORD_SURVIVAL

Lens:
Which record-creation processes could have produced a record of this event,
and which of those records are known to survive?

Another example:

Perspective:
INDIGENOUS_CONTEXT

Lens:
How might colonial terminology or English administrative categories differ
from the identities or relationships represented by the people involved?

Perspectives MAY include, but are not limited to:

- RECORD_CREATOR
- LEGAL_JURISDICTIONAL
- INDIGENOUS_CONTEXT
- GENDER_AUTHORITY
- LINGUISTIC
- GENEALOGICAL
- ECONOMIC_PROPERTY
- SOCIAL_NETWORK
- RECORD_SURVIVAL
- ALTERNATIVE
- ADVERSARIAL

The vocabulary is extensible.

A Perspective MUST identify:

- the analytical standpoint;
- the question being asked;
- the Evidence being considered;
- relevant Context;
- assumptions;
- possible alternatives;
- potential tests.

A Lens MUST identify:

- the Perspective under which it operates;
- the specific question or filter being applied;
- the Evidence or Context being examined;
- assumptions introduced by the Lens;
- potential distinguishing tests.

No Perspective or Lens has automatic priority over another.

A Perspective or Lens does not become authoritative merely because it is culturally,
institutionally, statistically, or computationally sophisticated.

---

## 6. Bias and Assumption Audit

The system MUST NOT treat "bias" as a binary property of a person, source, model, or interpretation.

Instead, the audit identifies assumptions that could distort interpretation.

An interpretation SHOULD expose:

- assumption;
- origin of the assumption;
- potential distortion;
- evidence affected;
- counter-interpretation;
- test that could reduce or expose the risk.

Examples of assumptions requiring examination include:

- modern genealogical assumptions;
- modern legal assumptions;
- modern identity categories;
- colonial administrative categories treated as personal identity;
- spelling similarity treated as identity;
- geographic proximity treated as kinship;
- absence of a record treated as evidence of nonexistence;
- survival of a record treated as representative of the original record universe;
- later genealogical tradition treated as contemporary evidence;
- AI transcription treated as independent corroboration.

The Bias/Assumption Audit does not:

- assign a numerical bias score;
- declare an interpretation "unbiased";
- declare a person, source, model, or Perspective objectively neutral.

It instead exposes assumptions and creates opportunities to challenge them.

The audit is therefore an assumption/challenge mechanism, not a truth score.

The Bias/Assumption Audit MUST NOT assign epistemic priority to competing interpretations.

Identifying a potential distortion does not, by itself, establish that the competing
interpretation is correct.

The audit identifies risks and tests; it does not rank historical explanations.

---

## 7. Interpretations

An Interpretation is a bounded explanatory proposal about Evidence and Context.

An Interpretation MUST identify:

- the Evidence Events on which it depends;
- the Context Records on which it depends;
- the Perspective/Lens under which it was generated;
- the interpretation itself;
- assumptions;
- alternatives;
- supporting observations;
- contradicting observations, if known;
- a true test;
- a false test;
- provenance;
- status.

An Interpretation MUST NOT be represented as a verified historical fact merely because:

- multiple AI systems generated it;
- multiple perspectives agree;
- it is genealogically convenient;
- it is consistent with an existing family tree;
- it explains several records;
- no alternative has yet been found.

Agreement is not corroboration unless the agreeing sources are genuinely independent evidence.

An Interpretation does NOT automatically become a Hypothesis.

An Interpretation SHOULD enter the Hypothesis layer only when it constitutes a
testable proposition about the historical world that requires formal hypothesis testing.

Contextual analysis may remain an Interpretation when it is being used to:

- frame a research question;
- expose an assumption;
- compare perspectives;
- identify possible explanations;
- identify a record-search path;
- define a next test.

The Contextualizer MUST NOT create Hypotheses merely to give every Interpretation
a stronger-looking status.

---

## 8. Multiple Interpretations

The system MUST permit multiple interpretations of the same Evidence Event to coexist.

The system MUST NOT collapse competing interpretations into a single narrative merely to produce a cleaner synthesis.

When interpretations conflict, the system SHOULD preserve:

- each interpretation;
- the evidence each relies upon;
- assumptions;
- contradictions;
- distinguishing tests;
- current status.

A Synthesizer may summarize disagreement.

A Synthesizer may NOT erase disagreement merely because one interpretation appears more coherent.

Multiple Perspectives applied to the same Evidence Event are NOT independent evidence.

Likewise:

MULTIPLE LENSES
    ≠
MULTIPLE INDEPENDENT SOURCES

Agreement between analytical perspectives may identify convergence in reasoning,
but it does not independently corroborate the underlying historical proposition.

Independent corroboration requires genuinely independent evidence.

---

## 9. Record-Location Hypotheses

The Contextualizer MAY identify record systems in which additional evidence could plausibly exist.

A Record-Location Hypothesis (RLH) is a first-class research object representing a
search hypothesis, not evidence that a record exists.

An RLH SHOULD have a stable identifier, for example:

RLH-000001

It SHOULD identify:

- target person/event/relationship;
- record family;
- jurisdiction;
- repository where applicable;
- rationale;
- expected trace;
- relevant name or terminology variants;
- associated people where relevant;
- chronological range where relevant;
- search status;
- provenance;
- next search action.

Possible search statuses include:

- NOT_SEARCHED
- SEARCHING
- PARTIAL
- SEARCHED_NO_RESULT
- RECORD_LOCATED
- RECORD_REQUIRES_REVIEW
- BLOCKED
- OUT_OF_SCOPE

The existence of a plausible record location MUST NOT be reported as evidence that the predicted record exists.

An RLH MAY generate a search.

A search that locates a source MUST create a separately processed Evidence Event.

The RLH itself does not become evidence merely because its prediction was successful.

An RLH MUST preserve the rationale and assumptions that generated it.

A search generated by an RLH MUST NOT be treated as independent support for the assumptions
that generated that RLH.

The following circular reasoning is prohibited:

ASSUMPTION
    |
    v
RECORD-LOCATION HYPOTHESIS
    |
    v
SEARCH
    |
    v
RESULT
    |
    v
"therefore the original assumption was supported"

Search results must be evaluated independently of the rationale that caused the search.

RLHs SHOULD integrate with the Negative Knowledge Map so that the archive can distinguish
searched, partially searched, unsearched, inaccessible, and reviewed record families.

---

## 10. Negative Knowledge

The Contextualizer MUST distinguish:

> no record located

from:

> record family searched with no result

from:

> record family not yet searched

from:

> record family inaccessible or incomplete

from:

> record located but not yet reviewed.

Negative findings MUST retain their search scope and provenance.

Absence of a located record MUST NOT be silently converted into historical absence.

---

## 11. Next Tests

Every material Interpretation SHOULD identify a test capable of distinguishing it from at least one alternative.

Tests MAY include:

- locating a primary source;
- comparing contemporaneous records;
- examining comparable transactions;
- testing name variants;
- testing geographic relationships;
- examining associated people;
- searching another record family;
- checking jurisdictional records;
- checking Indigenous/colonial parallel records;
- locating manuscript images;
- testing paleography;
- testing chronology;
- testing documentary provenance.

A test result MUST return to the Evidence layer or another explicitly defined research layer.

A failed search does not automatically falsify an interpretation unless the search had sufficient coverage to make the negative result probative.

---

## 12. Provenance

Every Contextualizer artifact MUST identify its provenance.

At minimum:

- actor type;
- actor;
- platform;
- recorded time.

Where applicable, provenance SHOULD distinguish:

- human research;
- AI generation;
- AI-assisted transcription;
- automated processing;
- independent human verification.

AI generation MUST NOT be represented as human verification.

AI agreement MUST NOT be represented as independent corroboration.

---

## 13. Status Boundary

Contextualization statuses MUST NOT be confused with Evidence or Claim statuses.

A Context Record may be:

- PROPOSED
- SOURCED
- PARTIAL
- CONTESTED
- UNRESOLVED

An Interpretation may be:

- PROPOSED
- OPEN
- SUPPORTED
- CONTESTED
- SUSPENDED
- DISCOUNTED
- REJECTED

These statuses describe the research artifact.

They do not automatically change the status of the Evidence Event or Claim.

---

## 14. Prohibited Narrative Smoothing

The Contextualizer MUST NOT:

- choose a single identity merely because it produces a coherent family tree;
- fill documentary gaps with probable-sounding prose;
- convert repeated speculation into fact;
- merge people solely because names are similar;
- infer kinship solely from geographic proximity;
- infer identity solely from association;
- treat a later source as contemporary evidence without identifying the time gap;
- conceal contradictory evidence;
- suppress an alternative because it is inconvenient;
- use the phrase "almost certainly" where the underlying evidence does not establish certainty;
- convert "plausible" into "proven" through repetition.

---

## 15. Symmetric Testing

When an interpretation is proposed, the Contextualizer SHOULD ask:

> What evidence would support this interpretation?

and:

> What evidence would support the strongest competing interpretation?

The system SHOULD NOT construct a rich evidentiary search for one hypothesis while giving alternatives only superficial testing.

Competing hypotheses should receive proportionate, explicit testing.

---

## 16. Separation of Layers

The following distinctions MUST remain explicit:

SOURCE ≠ EVIDENCE

EVIDENCE ≠ CONTEXT

CONTEXT ≠ INTERPRETATION

INTERPRETATION ≠ HYPOTHESIS

HYPOTHESIS ≠ CLAIM

AI TRANSCRIPTION ≠ HUMAN VERIFICATION

AI AGREEMENT ≠ INDEPENDENT CORROBORATION

RECORD-LOCATION HYPOTHESIS ≠ LOCATED RECORD

NEGATIVE SEARCH RESULT ≠ HISTORICAL NONEXISTENCE

---

## 17. Example

Evidence:

> No Joan Greene signature or mark is visible in the reviewed deed image.

A Contextualizer MAY ask:

- Was a wife's signature normally required for this type of transaction?
- Was a wife expected to appear as a formal party?
- Could another page or copy contain additional participation?
- Could the document have been drafted without recording her participation?
- What comparable documents survive?
- What record systems could contain related evidence?
- What assumptions are being made if the absence of a mark is interpreted?

The Contextualizer MUST NOT automatically conclude:

> Joan was illiterate.

or:

> Joan was not a formal participant.

or:

> Joan was Native.

or:

> Joan was English.

Those are interpretations or hypotheses requiring their own evidence and testing.

---

## 18. Design Principle

The Contextualizer exists to make the research space larger without making the evidence stronger.

Its purpose is not to answer uncertainty.

Its purpose is to make uncertainty:

- visible;
- structured;
- testable;
- source-aware;
- perspective-aware;
- resistant to narrative smoothing.

---

## 19. Production Boundary

This document is a DESIGN CONTRACT.

It does not by itself authorize:

- new JSON schemas;
- new production ledgers;
- new automated status transitions;
- automatic claim promotion;
- deletion of existing Evidence fields.

Production implementation requires:

1. hostile review of this contract;
2. regression tests;
3. explicit architectural decisions;
4. minimum necessary schema changes;
5. successful regression testing.

---

## 20. Open Architectural Questions

Before production implementation, resolve:

1. Should Interpretation remain entirely outside Evidence Events?
2. Should Context have its own ledger?
3. Should Perspectives have their own ledger or be embedded in Interpretation?
4. Should Bias/Assumption Audits be embedded in Interpretation or separately addressable?
5. Should Record-Location Hypotheses have their own ledger?
6. Which lens vocabulary should be canonical?
7. Which Contextualizer artifacts may become inputs to the Hypothesis layer?
8. What cross-record relationships require explicit REL identifiers?
9. How should independently sourced Context become Evidence?
10. What minimum structure is necessary to encode the existing Provenance Gate design without duplication?

---

**END OF DESIGN CONTRACT**
