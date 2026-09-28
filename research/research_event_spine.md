# Research Event Spine

**Status:** ACTIVE — SHADOW MODE

This is the chronological flight recorder for the Joan Archive research process.

It records what the research system did, what it found, what it tested,
what contradicted it, and what it recommends investigating next.

This is separate from the claims/evidence spine.

## Core rules

1. Nothing is silently deleted.
2. A search result is not automatically a historical fact.
3. Negative results are scoped to the search actually performed.
4. Hostile Review attacks interpretations; it does not act as a truth gate.
5. Search targets are research actions, not conclusions.
6. Human verification status is never fabricated.
7. The Seven Laws and `AGENT_GUARDRAILS.md` remain supreme.

## Event types

- SEARCH_STARTED
- SEARCH_PERFORMED
- SOURCE_FOUND
- SOURCE_NOT_FOUND
- SOURCE_READ
- SOURCE_AUTHENTICITY_CHECK
- CLAIM_CREATED
- CLAIM_TESTED
- CLAIM_SUPPORTED
- CLAIM_CONTRADICTED
- CLAIM_KILLED
- CLAIM_RESURRECTED
- RELATIONSHIP_FOUND
- RELATIONSHIP_TESTED
- CITATION_TRACED
- CITATION_BROKEN
- FABRICATION_DETECTED
- CIRCULAR_SOURCE_DETECTED
- HOSTILE_ATTACK
- MODEL_TEST
- JURISDICTION_TEST
- SEARCH_EXHAUSTED
- NEW_SEARCH_TARGET

## Event record

Each event should preserve:

- event ID
- timestamp
- agent
- action
- target
- Laws invoked
- search scope
- source
- evidence
- result
- status
- contradiction
- next action
- parent event

## Shadow-mode status

Patch 1 is infrastructure only.

It does not:
- rewrite historical conclusions
- promote evidence to PROOF
- erase rejected hypotheses
- automatically declare Joan identified
- replace human verification

