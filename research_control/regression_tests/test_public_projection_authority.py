#!/usr/bin/env python3
"""
Public Projection Authority Regression Test

Guards the boundary between:
    current control-plane authority
and
    static public editorial projection.

This test does NOT decide historical truth.

It specifically prevents public pages from:
- ranking live identity hypotheses;
- presenting legacy status vocabulary as current control-plane status;
- flattening hypothesis/inference into authoritative fact.

It intentionally permits:
- open hypotheses;
- explicitly preserved historical/suspended material;
- source-attributed uncertainty such as "likely according to F.L. Greene";
- unresolved questions.

Synthetic/static-page test only. No production ledgers are modified.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]

PUBLIC_PAGES = {
    "index.html": ROOT / "index.html",
    "analysis.html": ROOT / "analysis.html",
    "joan-constellation.html": ROOT / "joan-constellation.html",
}


def fail(message: str) -> None:
    print(f"PUBLIC PROJECTION AUTHORITY: FAIL — {message}")
    sys.exit(1)


def load_pages() -> dict[str, str]:
    pages = {}

    for name, path in PUBLIC_PAGES.items():
        if not path.exists():
            fail(f"missing public page: {name}")
        pages[name] = path.read_text(encoding="utf-8")

    return pages


def assert_no_live_hypothesis_ranking(pages: dict[str, str]) -> None:
    """
    A public page must not rank competing live identity hypotheses.

    This deliberately targets comparative ranking language rather than
    banning words such as "likely", which can be legitimate when explicitly
    attributed to a source or confined to a documentary observation.
    """

    ranking_patterns = [
        r"\bmost\s+developed\b.{0,120}\bcase\b",
        r"\bstrongest\s+prior\b",
        r"\bstrongest\s+(?:case|evidence|argument)\b",
        r"\bbest\s+hypothesis\b",
        r"\bmost\s+likely\s+(?:model|hypothesis|identity)\b",
        r"\bpreferred\s+hypothesis\b",
        r"\bpreferred\s+model\b",
        r"\branked?\s+(?:the\s+)?(?:models?|hypotheses?)\b",
    ]

    for page_name, text in pages.items():
        for pattern in ranking_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                excerpt = " ".join(match.group(0).split())
                fail(
                    f"{page_name} contains live-hypothesis ranking language: "
                    f"{excerpt!r}"
                )


def assert_no_unqualified_legacy_status_projection(
    pages: dict[str, str],
) -> None:
    """
    Legacy labels are historical vocabulary unless a current control-plane
    status independently establishes the state.

    We do NOT ban the words outright. We require public prose using them to
    make their historical/editorial nature explicit where the wording would
    otherwise present them as current status.
    """

    legacy_labels = [
        "PROOF",
        "PROBABLE",
        "PLAUSIBLE",
        "DISCREDITED",
        "ELIMINATED",
        "KILLED",
    ]

    # These patterns catch the old "tag" style where a legacy label is
    # presented as an authoritative present-tense status.
    unqualified_patterns = []

    for label in legacy_labels:
        unqualified_patterns.extend(
            [
                rf"<span[^>]*class=[\"'][^\"']*tag[^\"']*[\"'][^>]*>"
                rf"\s*(?:[^<]*\s+)?{label}\b",
                rf"<strong>\s*{label}\s*</strong>",
            ]
        )

    for page_name, text in pages.items():
        for pattern in unqualified_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                excerpt = " ".join(match.group(0).split())
                fail(
                    f"{page_name} presents legacy status vocabulary as a "
                    f"current public status: {excerpt!r}"
                )


def assert_allowed_uncertainty_remains_possible(
    pages: dict[str, str],
) -> None:
    """
    The projection firewall must not become a blanket ban on uncertainty.

    Public pages should remain capable of expressing:
    - open hypotheses;
    - suspended material;
    - source-attributed uncertainty.
    """

    combined = "\n".join(pages.values())

    if "OPEN HYPOTHESIS" not in combined:
        fail("public projection no longer permits explicit OPEN HYPOTHESIS state")

    if "SUSPENDED" not in combined:
        fail("public projection no longer preserves suspended research")

    # Legitimate attributed uncertainty must remain expressible.
    if not re.search(
        r"likely\s+Henry\s+Tibbitts.*(?:per|according to)\s+F\.?L\.?\s+Greene",
        combined,
        re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "source-attributed uncertainty appears to have been over-blocked; "
            "the F.L. Greene / Henry Tibbitts example should remain expressible"
        )


def assert_no_identity_flattening(pages: dict[str, str]) -> None:
    """
    The public projection must not silently turn a contextual relationship
    into an identity assignment.

    This is intentionally narrow: it protects the known Joan/Anashuecot
    boundary without trying to infer all possible historical identities.
    """

    constellation = pages["joan-constellation.html"]

    forbidden_identity_assignments = [
        r"\bAnashuecot\s+(?:was|is)\s+Joan\s+Greene\b",
        r"\bJoan\s+Greene\s+(?:was|is)\s+Anashuecot\b",
    ]

    for pattern in forbidden_identity_assignments:
        if re.search(pattern, constellation, re.IGNORECASE):
            fail(
                "joan-constellation.html collapses Joan and Anashuecot "
                "into an identity assignment"
            )


def assert_no_production_writes_in_test() -> None:
    """
    Structural guard: this regression test must remain a read-only public
    projection audit.
    """

    source = Path(__file__).read_text(encoding="utf-8")

    forbidden_write_patterns = [
        r"open\([^)]*['\"]w",
        r"write_text\(",
        r"append\(",
        r"append_record\(",
    ]

    for pattern in forbidden_write_patterns:
        if re.search(pattern, source, re.IGNORECASE):
            fail(
                "regression test contains a production-data write pattern: "
                f"{pattern}"
            )


def main() -> None:
    pages = load_pages()

    assert_no_live_hypothesis_ranking(pages)
    assert_no_unqualified_legacy_status_projection(pages)
    assert_allowed_uncertainty_remains_possible(pages)
    assert_no_identity_flattening(pages)
    assert_no_production_writes_in_test()

    print("PUBLIC PROJECTION AUTHORITY: PASS")


if __name__ == "__main__":
    main()
