# Research Effect Contract

**Status:** ACTIVE — research-process classification only

## Purpose

A Research Effect records what a research action materially changed in the
research process.

It does not establish historical truth.

It does not identify Joan Greene.

It does not rank hypotheses.

It does not assign confidence.

It does not promote a claim.

Research effects sit between research activity/results and the existing
evidence, review, claim, and status machinery.

## Controlled effects

The only permitted Research Effect values are:

- `NEW_DOCUMENTARY_EVIDENCE`
- `NEGATIVE_SEARCH_RESULT`
- `CORROBORATION`
- `CONTRADICTION`
- `IDENTITY_SHAPING_INFERENCE`
- `LEAD_ONLY`
- `NO_MATERIAL_CHANGE`

## Definitions

### NEW_DOCUMENTARY_EVIDENCE

A source or documentary record was located and provides new information
relevant to the research question.

This does not establish identity, authenticity, interpretation, or truth by
itself.

### NEGATIVE_SEARCH_RESULT

A defined search path produced no relevant located result.

This means only that the specified search produced no located result.

It does not establish that a person, event, document, relationship, or record
did not exist.

### CORROBORATION

A genuinely independent documentary source supports an already-defined
proposition.

Agreement between AI systems, agents, catalog records, duplicate
transcriptions, or copies derived from the same source is not independent
corroboration.

### CONTRADICTION

A source or research result conflicts with an existing observation,
interpretation, claim, chronology, identity assignment, or documentary
description.

Contradictions must remain visible.

### IDENTITY_SHAPING_INFERENCE

A research result materially changes the shape of the identity problem without
identifying a person or establishing an identity assignment.

Examples include discovering a mechanism by which a later genealogy may have
derived a person-name from a speculative place association.

This effect may change what should be tested next, but it cannot promote or
eliminate an identity hypothesis.

### LEAD_ONLY

A result provides a plausible research lead but does not materially change
the evidence state or identity problem.

### NO_MATERIAL_CHANGE

A defined research action completed but produced no material change to the
current research state.

This is a valid research result.

## Structural prohibitions

A Research Effect must not contain or imply machine-assigned:

- person identity
- identity confidence
- hypothesis ranking
- best hypothesis
- historical certainty
- proof status
- elimination of a hypothesis
- absence-of-existence conclusion

A Research Effect must preserve provenance and identify the research action
from which the effect arose.

## Observation and inference remain separate

A literal observation must remain distinguishable from an inference about
that observation.

The Research Effect layer may record an inference about the research
consequence of an observation, but it must not silently convert that inference
into a historical fact.

## Ghost-name rule

A later genealogical person-name must not become a historical person merely
because an earlier source contains a matching place-name or speculative
geographic association.

For example:

- La Mance speculates that John of Quidnessett probably lived at Enfield.
- A later genealogy contains a person called "Enfield Greene."

The Research Effect may record that this reveals a possible place-name
generation mechanism requiring further testing.

It may not record that "Enfield Greene" was fabricated, nor may it identify
that person as fictional, real, or unrelated without independent documentary
evidence.

## Negative-search rule

`NEGATIVE_SEARCH_RESULT` describes the search performed.

It must never be interpreted as proof that the searched-for person, event,
document, relationship, or identity did not exist.

## Corroboration rule

`CORROBORATION` requires documentary independence.

The following do not constitute independent corroboration by themselves:

- multiple AI agents reaching the same conclusion
- duplicate catalog entries
- duplicate transcriptions
- genealogies copying one another
- citations that all derive from one source
- search-result agreement

## Relationship to evidence and status

Research Effect is not an evidence status and is not a claim status.

A Research Effect may cause a reviewer to create or update an evidence event,
claim, review event, status event, or next test through the existing control
plane.

Those downstream transitions remain subject to their existing provenance
requirements.

## Core invariant

> Research can change what should be tested next without changing what has
> been proven.
