#!/usr/bin/env python3
"""Regression tests for explicit-path findings routing."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER_PATH = ROOT / "tools" / "findings_pipeline" / "route_findings.py"


def load_router():
    spec = importlib.util.spec_from_file_location("route_findings", ROUTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load findings router")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_explicit_single_path_routes_only_requested_finding():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        findings = root / "research_findings"
        queue = root / "research_queue" / "finding_runs"
        findings.mkdir(parents=True)

        (findings / "alpha.md").write_text("# Alpha\n")
        (findings / "beta.md").write_text("# Beta\n")

        original_root = router.ROOT
        original_findings = router.FINDINGS
        original_queue = router.QUEUE

        try:
            router.ROOT = root
            router.FINDINGS = findings
            router.QUEUE = queue

            result = router.route(
                "2099-01-01",
                False,
                ["research_findings/alpha.md"],
            )

            routed = sorted(
                path.parent.name
                for path in queue.glob(
                    "2099-01-01/*/run_manifest.json"
                )
            )

            assert result == 0
            assert routed == ["alpha"]
        finally:
            router.ROOT = original_root
            router.FINDINGS = original_findings
            router.QUEUE = original_queue


def test_explicit_multiple_paths_route_exactly_requested_findings():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        findings = root / "research_findings"
        queue = root / "research_queue" / "finding_runs"
        findings.mkdir(parents=True)

        for name in ("alpha.md", "beta.md", "gamma.md"):
            (findings / name).write_text(f"# {name}\n")

        original_root = router.ROOT
        original_findings = router.FINDINGS
        original_queue = router.QUEUE

        try:
            router.ROOT = root
            router.FINDINGS = findings
            router.QUEUE = queue

            result = router.route(
                "2099-01-02",
                False,
                [
                    "research_findings/gamma.md",
                    "research_findings/alpha.md",
                ],
            )

            routed = sorted(
                path.parent.name
                for path in queue.glob(
                    "2099-01-02/*/run_manifest.json"
                )
            )

            assert result == 0
            assert routed == ["alpha", "gamma"]
        finally:
            router.ROOT = original_root
            router.FINDINGS = original_findings
            router.QUEUE = original_queue


def test_explicit_path_rejects_non_finding():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        findings = root / "research_findings"
        queue = root / "research_queue" / "finding_runs"
        findings.mkdir(parents=True)

        (root / "research_control").mkdir()
        (root / "research_control" / "not-a-finding.md").write_text(
            "# Not a finding\n"
        )

        original_root = router.ROOT
        original_findings = router.FINDINGS
        original_queue = router.QUEUE

        try:
            router.ROOT = root
            router.FINDINGS = findings
            router.QUEUE = queue

            try:
                router.route(
                    "2099-01-03",
                    False,
                    ["research_control/not-a-finding.md"],
                )
            except SystemExit as exc:
                assert "research_findings" in str(exc)
            else:
                raise AssertionError(
                    "Non-finding path was not rejected"
                )
        finally:
            router.ROOT = original_root
            router.FINDINGS = original_findings
            router.QUEUE = original_queue


def test_no_explicit_paths_preserves_all_findings_behavior():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        findings = root / "research_findings"
        queue = root / "research_queue" / "finding_runs"
        findings.mkdir(parents=True)

        (findings / "alpha.md").write_text("# Alpha\n")
        (findings / "beta.md").write_text("# Beta\n")
        (findings / "README.md").write_text("# README\n")

        original_root = router.ROOT
        original_findings = router.FINDINGS
        original_queue = router.QUEUE

        try:
            router.ROOT = root
            router.FINDINGS = findings
            router.QUEUE = queue

            result = router.route("2099-01-04", False)

            routed = sorted(
                path.parent.name
                for path in queue.glob(
                    "2099-01-04/*/run_manifest.json"
                )
            )

            assert result == 0
            assert routed == ["alpha", "beta"]
        finally:
            router.ROOT = original_root
            router.FINDINGS = original_findings
            router.QUEUE = original_queue


def test_corpus_router_finding_change_can_be_handed_to_findings_router():
    corpus_router = load_router()
    findings_router_path = (
        ROOT / "tools" / "findings_pipeline" / "route_findings.py"
    )
    spec = importlib.util.spec_from_file_location(
        "route_findings_for_handoff",
        findings_router_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load findings router")

    findings_router = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(findings_router)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        findings = root / "research_findings"
        research = root / "research"
        findings.mkdir(parents=True)
        research.mkdir(parents=True)

        changed = findings / "changed.md"
        unchanged = findings / "unchanged.md"
        unrelated = research / "unrelated.md"

        changed.write_text("# Changed finding\n")
        unchanged.write_text("# Unchanged finding\n")
        unrelated.write_text("# Unrelated research record\n")

        original_corpus_root = corpus_router.ROOT
        original_manifest_dir = corpus_router.SOURCE_MANIFEST_DIR

        original_findings_root = findings_router.ROOT
        original_findings_dir = findings_router.FINDINGS
        original_queue = findings_router.QUEUE

        try:
            corpus_router.ROOT = root
            corpus_router.SOURCE_MANIFEST_DIR = (
                root / "research" / "sources"
            )

            report = corpus_router.route(
                [
                    "research_findings/changed.md",
                    "research/unrelated.md",
                ],
                "2099-01-05",
            )

            finding_events = [
                event
                for event in report["changes"]
                if event["population"] == "research_findings"
            ]

            assert len(finding_events) == 1

            event = finding_events[0]

            assert event["artifact_path"] == (
                "research_findings/changed.md"
            )
            assert event["routing_destination"] == "findings_router"
            assert event["required_test"] == "findings_router"

            finding_paths = [
                event["artifact_path"]
                for event in finding_events
            ]

            findings_router.ROOT = root
            findings_router.FINDINGS = findings
            findings_router.QUEUE = (
                root / "research_queue" / "finding_runs"
            )

            result = findings_router.route(
                "2099-01-05",
                False,
                finding_paths,
            )

            routed = sorted(
                path.parent.name
                for path in findings_router.QUEUE.glob(
                    "2099-01-05/*/run_manifest.json"
                )
            )

            assert result == 0
            assert routed == ["changed"]

        finally:
            corpus_router.ROOT = original_corpus_root
            corpus_router.SOURCE_MANIFEST_DIR = original_manifest_dir

            findings_router.ROOT = original_findings_root
            findings_router.FINDINGS = original_findings_dir
            findings_router.QUEUE = original_queue