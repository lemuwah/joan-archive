#!/usr/bin/env python3
"""
Adversarial tests for the Provenance Gate design.

TEST-ONLY DESIGN FILE.

This suite does NOT enforce the gate in production.

It tests whether a proposed claim has an explicit, traceable
relationship to an evidence event, while keeping verification
strictly scoped to the literal observation.

Core principle:

    SOURCE
       |
       v
    EVIDENCE EVENT
       |
       +--> literal observation
       +--> transcription
       +--> interpretation
       +--> verification of a defined component
       |
       v
    CLAIM <--> EXPLICIT EVIDENCE RELATIONSHIP

Critical invariant:

    Verification of a literal observation does NOT verify
    the interpretation, identity assignment, inference,
    or hypothesis derived from that observation.

A process gate passing means only that the provenance structure
is eligible for the proposed status. It does NOT establish
historical truth.
"""

from dataclasses import dataclass
from typing import Optional
import re


CERTAINTY_STATUSES = {
    "PROOF",
    "VERIFIED",
    "CONFIRMED",
    "CERTAIN",
    "IDENTIFIED",
}

DIRECT_SUPPORT_RELATIONS = {
    "DIRECTLY_SUPPORTS",
}

NON_SUPPORT_RELATIONS = {
    "CONTEXT_ONLY",
    "DOES_NOT_ESTABLISH",
    "CONTRADICTS",
}

VALID_VERIFICATION_COMPONENTS = {
    "LITERAL_OBSERVATION",
    "TRANSCRIPTION",
    "INTERPRETATION",
}

EVIDENCE_ID_PATTERN = re.compile(r"^EVID-[0-9]{6}$")


@dataclass
class Verification:
    """
    Verification provenance.

    The critical field is verified_component.

    A human verification of an interpretation is NOT equivalent
    to human verification of the underlying literal observation.
    """

    status: str
    verifier: str
    verified_against: str
    verified_component: str
    scope: str
    recorded_at: str


@dataclass
class EvidenceEvent:
    """
    Structured evidence event.

    finding_id is deliberately separate from evidence_id.

    A finding may be an earlier research artifact or discovery
    record. It is NOT interchangeable with the machine-auditable
    Evidence Event identifier.
    """

    evidence_id: str
    source_id: str
    literal_observation: str
    extraction_method: str
    interpretation: Optional[str] = None
    verification: Optional[Verification] = None
    finding_id: Optional[str] = None


@dataclass
class EvidenceLink:
    """
    Explicit relationship between evidence and a proposed claim.

    supported_claim is the exact proposition this relationship
    declares the evidence to support. It prevents a verified
    observation from silently inheriting support for a different
    claim.
    """

    evidence_id: str
    relation: str
    scope: str
    supported_claim: str


@dataclass
class ProposedClaim:
    claim: str
    claim_type: str
    evidence: Optional[EvidenceEvent]
    evidence_link: Optional[EvidenceLink]
    status: str
    true_test: Optional[str] = None
    false_test: Optional[str] = None
    alternatives: Optional[list[str]] = None


def provenance_check(claim: ProposedClaim) -> tuple[bool, str]:
    """
    Structural provenance check.

    This function deliberately does NOT attempt to decide
    historical truth from natural-language keywords.

    It checks whether the proposed status has the required
    evidence/provenance structure.
    """

    if claim.evidence is None:
        return False, "BLOCKED: no evidence event supplied"

    evidence = claim.evidence

    if not EVIDENCE_ID_PATTERN.match(evidence.evidence_id):
        return False, "BLOCKED: invalid Evidence Event ID"

    if not evidence.source_id:
        return False, "BLOCKED: evidence has no source reference"

    if not evidence.literal_observation:
        return False, "BLOCKED: evidence has no literal observation"

    if claim.evidence_link is None:
        return False, "BLOCKED: no explicit evidence relationship"

    link = claim.evidence_link

    if link.evidence_id != evidence.evidence_id:
        return False, (
            "BLOCKED: evidence relationship points to a different "
            "Evidence Event"
        )

    if not link.relation:
        return False, "BLOCKED: evidence relationship has no relation"

    if not link.scope:
        return False, "BLOCKED: evidence relationship has no scope"

    if not link.supported_claim:
        return False, (
            "BLOCKED: evidence relationship has no bounded claim"
        )

    if link.relation in DIRECT_SUPPORT_RELATIONS:
        if link.supported_claim != claim.claim:
            return False, (
                "BLOCKED: direct-support relationship does not match "
                "the proposed claim"
            )

    if claim.status in CERTAINTY_STATUSES:

        verification = evidence.verification

        if verification is None:
            return False, (
                "BLOCKED: certainty status requires explicit "
                "verification provenance"
            )

        if verification.status != "HUMAN_VERIFIED":
            return False, (
                "BLOCKED: certainty status requires HUMAN_VERIFIED "
                "evidence"
            )

        if not verification.verifier:
            return False, "BLOCKED: verification has no verifier"

        if not verification.verified_against:
            return False, "BLOCKED: verification has no verification target"

        if not verification.scope:
            return False, "BLOCKED: verification has no scope"

        if verification.verified_component != "LITERAL_OBSERVATION":
            return False, (
                "BLOCKED: human verification is not scoped to the "
                "literal observation"
            )

        if link.relation not in DIRECT_SUPPORT_RELATIONS:
            return False, (
                "BLOCKED: certainty status requires a direct-support "
                "evidence relationship"
            )

    return True, "ALLOWED: provenance requirements satisfied"


def hypothesis_check(claim: ProposedClaim) -> tuple[bool, str]:
    """
    Separate structural check for hypotheses.

    A hypothesis may remain open without becoming historical proof.
    """

    if claim.claim_type != "HYPOTHESIS":
        return False, "BLOCKED: hypothesis check requires HYPOTHESIS claim type"

    if not claim.true_test:
        return False, "BLOCKED: hypothesis has no true test"

    if not claim.false_test:
        return False, "BLOCKED: hypothesis has no false test"

    if not claim.alternatives:
        return False, "BLOCKED: hypothesis has no alternatives"

    if claim.status in CERTAINTY_STATUSES:
        return False, (
            "BLOCKED: hypothesis cannot use a certainty status "
            "through this process gate"
        )

    return True, "ALLOWED: hypothesis remains a hypothesis"


PRIMARY_SOURCE = "RI-STATE-ARCHIVES-LR1-F259-260"
FINDING = "FINDING-fe55dd3e755e"


def evidence(
    observation: str,
    *,
    method: str = "AI_TRANSCRIPTION",
    verification: Optional[Verification] = None,
    interpretation: Optional[str] = None,
) -> EvidenceEvent:
    return EvidenceEvent(
        evidence_id="EVID-000001",
        source_id=PRIMARY_SOURCE,
        finding_id=FINDING,
        literal_observation=observation,
        extraction_method=method,
        interpretation=interpretation,
        verification=verification,
    )


def link(
    relation: str,
    scope: str,
    supported_claim: str,
) -> EvidenceLink:
    return EvidenceLink(
        evidence_id="EVID-000001",
        relation=relation,
        scope=scope,
        supported_claim=supported_claim,
    )


def human_verification(
    observation: str,
    *,
    component: str = "LITERAL_OBSERVATION",
) -> Verification:
    return Verification(
        status="HUMAN_VERIFIED",
        verifier="HUMAN-TEST-REVIEWER",
        verified_against=PRIMARY_SOURCE,
        verified_component=component,
        scope=observation,
        recorded_at="2026-09-16T00:00:00Z",
    )


def run_test(name: str, condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL: {name} -> {detail}")

    print(f"PASS: {name} -> {detail}")


def main() -> None:

    # ------------------------------------------------------------
    # 1. BOUNDED FACTUAL CLAIM
    # ------------------------------------------------------------

    observation = "The deed names Joan Greene as wife of John Greene."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was named as John Greene's wife in the deed.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=link(
            "DIRECTLY_SUPPORTS",
            "The deed's literal wording identifying Joan Greene as "
            "John Greene's wife.",
            supported_claim="Joan Greene was named as John Greene's wife in the deed."
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "bounded factual claim",
        allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 2. NO SIGNATURE / MARK
    # ------------------------------------------------------------

    observation = "No Joan Greene signature or mark is visible in the reviewed deed image."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="No Joan Greene signature or mark is visible in the reviewed deed image.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=link(
            "DIRECTLY_SUPPORTS",
            "The reviewed image contains no visible Joan Greene "
            "signature or mark.",
            supported_claim='No Joan Greene signature or mark is visible in the reviewed deed image.'
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "bounded observation about Joan's signature/mark",
        allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 3. AI TRANSCRIPTION ALONE CANNOT BECOME CERTAINTY
    # ------------------------------------------------------------

    observation = "Joane Greene his wife."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was named as John Greene's wife.",
        evidence=evidence(
            observation,
            method="AI_TRANSCRIPTION",
            verification=None,
        ),
        evidence_link=link(
            "DIRECTLY_SUPPORTS",
            "AI transcription of the relevant deed wording.",
            supported_claim="Joan Greene was named as John Greene's wife."
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "AI transcription cannot become certainty by itself",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 4. NO EVIDENCE REFERENCE
    # ------------------------------------------------------------

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was named as John Greene's wife.",
        evidence=None,
        evidence_link=None,
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "missing evidence is blocked",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 5. EVIDENCE WITHOUT EXPLICIT RELATIONSHIP
    # ------------------------------------------------------------

    observation = "Joane Greene his wife."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was named as John Greene's wife.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=None,
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "evidence without explicit relationship is blocked",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 6. OBSERVATION DOES NOT ESTABLISH NARRAGANSETT IDENTITY
    # ------------------------------------------------------------

    observation = "The deed names Joan Greene as wife of John Greene."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was Narragansett.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=link(
            "DOES_NOT_ESTABLISH",
            "The deed identifies Joan as John's wife but does not "
            "identify her ancestry.",
            supported_claim="Joan Greene was named as John Greene's wife."
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "wife identification cannot establish Narragansett identity",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 7. OBSERVATION DOES NOT ESTABLISH ANASHUECOT IDENTITY
    # ------------------------------------------------------------

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was Anashuecot.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=link(
            "DOES_NOT_ESTABLISH",
            "The deed names Joan as John's wife but does not "
            "identify Joan as Anashuecot.",
            supported_claim="Joan Greene was named as John Greene's wife."
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "wife identification cannot establish Anashuecot identity",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 8. NEGATIVE SEARCH CANNOT BECOME PROOF
    # ------------------------------------------------------------

    observation = (
        "No English baptism record for Joan was located in the "
        "defined searched scope."
    )

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan was Narragansett because no English baptism was found.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=link(
            "DOES_NOT_ESTABLISH",
            "A negative search result describes the searched scope "
            "but does not establish Joan's identity.",
            supported_claim='Joan was Narragansett because no English baptism was found.'
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "negative search cannot become proof of an alternative identity",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 9. NO SIGNATURE CANNOT PROVE ILLITERACY
    # ------------------------------------------------------------

    observation = "No Joan Greene signature or mark is visible."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was illiterate because she did not sign the deed.",
        evidence=evidence(
            observation,
            method="HUMAN_REVIEW",
            verification=human_verification(observation),
        ),
        evidence_link=link(
            "DOES_NOT_ESTABLISH",
            "Absence of a visible signature does not establish literacy "
            "or illiteracy.",
            supported_claim='Joan Greene was illiterate because she did not sign the deed.'
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "absence of signature cannot establish illiteracy",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 10. IDENTITY HYPOTHESIS REQUIRES TESTS AND ALTERNATIVES
    # ------------------------------------------------------------

    claim = ProposedClaim(
        claim_type="HYPOTHESIS",
        claim="Joan may have had Narragansett ancestry.",
        evidence=evidence(
            "The deed identifies Joan as John Greene's wife.",
            method="HUMAN_REVIEW",
            verification=human_verification(
                "The deed identifies Joan as John Greene's wife."
            ),
        ),
        evidence_link=link(
            "CONTEXT_ONLY",
            "The deed supplies household and chronology context "
            "but does not establish ancestry.",
            supported_claim='Joan may have had Narragansett ancestry.'
        ),
        status="PROVISIONALLY_SUPPORTED",
        true_test="Locate independent evidence connecting Joan to a Narragansett family or community.",
        false_test="Locate evidence demonstrating an incompatible origin or identity.",
        alternatives=[
            "English origin",
            "Irish origin",
            "mixed English/Narragansett origin",
            "undocumented origin",
            "other open models",
        ],
    )

    allowed, reason = hypothesis_check(claim)

    run_test(
        "bounded hypothesis with tests and alternatives",
        allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 11. CONTAMINATION ATTACK:
    #     HUMAN VERIFICATION OF INTERPRETATION MUST NOT
    #     COUNT AS VERIFICATION OF THE LITERAL OBSERVATION
    # ------------------------------------------------------------

    observation = "The deed names Joan Greene as wife of John Greene."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was Anashuecot.",
        evidence=evidence(
            observation,
            method="AI_TRANSCRIPTION",
            interpretation="The AI interpretation identifies Joan Greene as Anashuecot.",
            verification=human_verification(
                "The AI interpretation identifies Joan Greene as Anashuecot.",
                component="INTERPRETATION",
            ),
        ),
        evidence_link=link(
            "DIRECTLY_SUPPORTS",
            "AI interpretation identifying Joan as Anashuecot.",
            supported_claim="Joan Greene was named as John Greene's wife."
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "human verification of interpretation cannot become proof",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 12. SECOND CONTAMINATION ATTACK:
    #     HUMAN VERIFICATION MUST BE SCOPED TO THE LITERAL
    #     OBSERVATION, NOT AN IDENTITY CONCLUSION
    # ------------------------------------------------------------

    observation = "The deed names Joan Greene as wife of John Greene."

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was Anashuecot.",
        evidence=evidence(
            observation,
            method="AI_TRANSCRIPTION",
            interpretation="The deed proves Joan Greene was Anashuecot.",
            verification=human_verification(
                "The deed proves Joan Greene was Anashuecot.",
                component="LITERAL_OBSERVATION",
            ),
        ),
        evidence_link=link(
            "DIRECTLY_SUPPORTS",
            "The AI-generated identity interpretation is being "
            "presented as if it were the observed deed wording.",
            supported_claim="Joan Greene was named as John Greene's wife."
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    # This test intentionally documents the remaining semantic boundary.
    #
    # The structural gate cannot determine whether natural-language
    # text labelled "literal observation" is genuinely literal.
    #
    # Therefore this case must be surfaced for hostile review rather
    # than silently treated as historical truth.
    #
    # The current test expects the structural gate to REJECT the
    # direct identity claim because the evidence relationship itself
    # does not match the bounded observation.
    run_test(
        "identity claim cannot inherit proof merely from a relabelled observation",
        not allowed,
        reason,
    )

    # ------------------------------------------------------------
    # 13. FINDING ID MUST NOT SUBSTITUTE FOR EVIDENCE EVENT ID
    # ------------------------------------------------------------

    bad_evidence = EvidenceEvent(
        evidence_id=FINDING,
        source_id=PRIMARY_SOURCE,
        literal_observation="Joane Greene his wife.",
        extraction_method="HUMAN_REVIEW",
        verification=human_verification(
            "Joane Greene his wife."
        ),
        finding_id=FINDING,
    )

    claim = ProposedClaim(
        claim_type="FACTUAL",
        claim="Joan Greene was named as John Greene's wife.",
        evidence=bad_evidence,
        evidence_link=EvidenceLink(
            evidence_id=FINDING,
            relation="DIRECTLY_SUPPORTS",
            scope="The deed names Joan as John's wife.",
            supported_claim="Joan Greene was named as John Greene's wife.",
        ),
        status="PROOF",
    )

    allowed, reason = provenance_check(claim)

    run_test(
        "Finding ID cannot substitute for Evidence Event ID",
        not allowed,
        reason,
    )

    print()
    print("PROVENANCE GATE STRUCTURAL DESIGN TEST: PASS")


if __name__ == "__main__":
    main()
