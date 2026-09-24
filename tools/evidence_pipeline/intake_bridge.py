#!/usr/bin/env python3
"""
AI-first Evidence Intake Bridge.

Purpose:
    Convert an AI research observation into an authoritative Evidence Event
    without requiring human verification.

Safety principles:
    - AI provenance is explicit.
    - AI evidence is never treated as human-verified.
    - Proposed claims are never silently inherited from a finding.
    - Interpretation is kept separate from literal observation.
    - The bridge records research work; it does not establish historical truth.
    - All authoritative writes go through append_record("evidence", ...).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from research_control.tools.append_event import append_record


AI_DISCLAIMER = (
    "AI-GENERATED RESEARCH RECORD: this evidence event records work performed "
    "or reported by an AI system. It is not human verification, is not "
    "independent corroboration, and does not by itself establish historical truth."
)

AI_ACTOR_TYPES = {"AI", "SYSTEM"}

FORBIDDEN_AI_SOURCE_STATUSES = {
    "PRIMARY_VERIFIED",
}

ALLOWED_RELATIONSHIP_DEFAULT = []


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_ai_evidence_event(
    *,
    evidence_id: str,
    source: dict[str, Any],
    source_status: str,
    literal_observation: str,
    actor: str,
    platform: str,
    access_method: str,
    finding_id: str | None = None,
    transcription: str | None = None,
    interpretation: str | None = None,
    session: str | None = None,
) -> dict[str, Any]:
    """
    Build an AI-generated Evidence Event.

    Important:
        claim_refs deliberately defaults to [].
        A finding's proposed_claims must be linked later through an explicit
        claim/evidence relationship rather than being silently inherited.
    """

    if not literal_observation or not literal_observation.strip():
        raise ValueError("literal_observation is required")

    if source_status in FORBIDDEN_AI_SOURCE_STATUSES:
        raise ValueError(
            "AI-first intake cannot create PRIMARY_VERIFIED evidence. "
            "Verification is a separate state transition."
        )

    if not actor or not platform:
        raise ValueError("AI provenance requires actor and platform")

    provenance_session = session or "AI-EVIDENCE-INTAKE"

    if finding_id:
        provenance_session = (
            f"{provenance_session};FINDING={finding_id}"
        )

    provenance_session = (
        f"{provenance_session};AI_DISCLAIMER={AI_DISCLAIMER}"
    )

    event: dict[str, Any] = {
        "evidence_id": evidence_id,
        "timestamp": utc_now(),
        "source": source,
        "source_status": source_status,
        "literal_observation": literal_observation,
        "claim_refs": list(ALLOWED_RELATIONSHIP_DEFAULT),
        "provenance": {
            "actor_type": "AI",
            "actor": actor,
            "platform": platform,
            "recorded_at": utc_now(),
            "session": provenance_session,
        },
    }

    if transcription is not None:
        event["transcription"] = transcription

    if interpretation is not None:
        event["interpretation"] = interpretation

    return event


def intake_ai_evidence(
    *,
    evidence_id: str,
    source: dict[str, Any],
    source_status: str,
    literal_observation: str,
    actor: str,
    platform: str,
    access_method: str,
    finding_id: str | None = None,
    transcription: str | None = None,
    interpretation: str | None = None,
    session: str | None = None,
) -> dict[str, Any]:
    """
    Build and append one AI Evidence Event through the authoritative ledger
    writer.
    """

    if source.get("access_method") is None:
        source = dict(source)
        source["access_method"] = access_method

    event = build_ai_evidence_event(
        evidence_id=evidence_id,
        source=source,
        source_status=source_status,
        literal_observation=literal_observation,
        actor=actor,
        platform=platform,
        finding_id=finding_id,
        transcription=transcription,
        interpretation=interpretation,
        session=session,
    )

    append_record("evidence", event)

    return event
