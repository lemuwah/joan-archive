# Joan Archive — Research Control Plane

**Status:** ACTIVE — zero-trust research orchestration layer
**Created:** 2026-09-14

## Purpose

The Research Control Plane is the machine-auditable layer connecting the Joan Archive research queues, evidence, hypotheses, searches, reviews, and timeline.

It does not replace the existing research machinery. It does not inherit the truth status of existing claims.

Existing claims, queues, hypotheses, findings, and historical status labels enter this system as material to be re-tested.

## Core Rule

> Nothing inherits status merely because an older file calls it verified, proven, probable, eliminated, or null.

Every claim must pass through the current evidence process.

## Event model

Every meaningful research action should record, where applicable:

- WHO — researcher, human, AI model, wrapper/platform
- WHAT — claim, search, observation, inference, hypothesis, test, review, or status change
- WHEN — timestamp
- WHERE — repository, collection, jurisdiction, document, page/image, or search scope
- WHY — research question or purpose
- SOURCE — exact source trail
- LITERAL OBSERVATION — what the source actually shows/says
- REASONING — interpretation kept separate from observation
- ALTERNATIVES — competing explanations
- TRUE TEST — evidence that would support the proposition
- FALSE TEST — evidence that would contradict it
- RESULT — what the search/test actually produced
- CONTRADICTIONS — conflicts with other evidence
- CONTAMINATION — known circular, fabricated, inferred, or compromised input
- STATUS — current evidence-based state
- NEXT TEST — what should happen next

## Observation / Inference / Hypothesis / Test

These are separate.

**Observation:** what was actually seen, read, retrieved, or documented.

**Inference:** a reasoned interpretation of observations.

**Hypothesis:** a proposition being tested.

**Test:** a defined attempt to find evidence for or against the hypothesis.

Agreement between agents is not independent corroboration.

## Status principles

The control plane does not use NULL as a conclusion.

A negative search is recorded as a search event.

Useful states include:

- UNTESTED
- OPEN
- SEARCHING
- PARTIAL
- EVIDENCE_LOCATED
- SOURCE_UNREAD
- SOURCE_MISMATCH
- NEGATIVE_SEARCH
- CONFLICT
- SUSPENDED
- PROPOSED
- PROVISIONALLY_SUPPORTED
- VERIFIED
- DISCOUNTED
- REJECTED

NEGATIVE_SEARCH means a defined search produced no located result. It does not mean the underlying person, event, document, or relationship did not exist.

SOURCE_MISMATCH means the located source does not support the claim as previously represented. It does not mean the underlying event is necessarily false.

## AI writing rule

AI may write research events: searches performed, sources located, literal observations, candidate leads, contradictions, hypotheses, proposed next searches, provenance, and proposed status changes.

AI may not silently create a verified fact, identify Joan, eliminate a hypothesis, delete evidence, overwrite an earlier event, convert absence into proof of absence, or treat another AI conclusion as independent verification.

## Append-only principle

Historical research events are never silently rewritten.

Corrections create new events explaining the correction.

The archive should make it possible to reconstruct what was believed, why it was believed, what challenged it, and what changed.

## Existing archive integration

The control plane works alongside the existing guardrails, methodology, evidence files, hypothesis matrix, research queues, findings funnel, and public timeline.

Existing status labels are historical inputs and must be revalidated when imported.

## Transparency requirement

A reviewer should be able to follow:

SOURCE → OBSERVATION → INFERENCE → HYPOTHESIS → TRUE/FALSE TEST → RESULT → REVIEW → STATUS → NEXT TEST

without relying on hidden AI reasoning or an invisible agent decision.

## No narrative smoothing

The control plane makes the research trail more visible, not more elegant.

Contradictions remain visible. Failed searches remain visible. Suspended theories remain visible. Contamination remains visible. Uncertainty remains visible.

The goal is not to make Joan’s story neat.

The goal is to make the path toward the truth auditable.
