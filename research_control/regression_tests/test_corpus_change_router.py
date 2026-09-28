#!/usr/bin/env python3
"""Regression tests for corpus-change routing."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER_PATH = ROOT / "tools" / "research_control" / "route_corpus_changes.py"


def load_router():
    spec = importlib.util.spec_from_file_location("route_corpus_changes", ROUTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load corpus change router")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_manifest_routes_to_source_audit():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research" / "sources").mkdir(parents=True)
        (root / "research").mkdir(parents=True, exist_ok=True)

        manifest = root / "research" / "sources" / "example.yml"
        record = root / "research" / "record.md"

        manifest.write_text(
            "source_id: EXAMPLE-1\n"
            "repository_path: research/record.md\n"
        )
        record.write_text("# Example record\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            events = router.route(
                ["research/sources/example.yml"],
                "2026-09-18",
            )["changes"]

            event = events[0]

            assert event["change_type"] == "source_library_manifest_change"
            assert event["routing_destination"] == "source_library_integrity_audit"
            assert event["required_test"] == "source_library_integrity_audit"
            assert event["referencing_manifests"] == [
                "research/sources/example.yml"
            ]
            assert event["historical_status_authority"] is False
        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_manifest_dir


def test_referenced_record_routes_to_source_audit():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research" / "sources").mkdir(parents=True)
        (root / "research").mkdir(parents=True, exist_ok=True)

        manifest = root / "research" / "sources" / "example.yml"
        record = root / "research" / "record.md"

        manifest.write_text(
            "source_id: EXAMPLE-1\n"
            "repository_path: research/record.md\n"
        )
        record.write_text("# Example record\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            events = router.route(
                ["research/record.md"],
                "2026-09-18",
            )["changes"]

            event = events[0]

            assert event["change_type"] == (
                "source_library_referenced_record_change"
            )
            assert event["routing_destination"] == "source_library_integrity_audit"
            assert event["referencing_manifests"] == [
                "research/sources/example.yml"
            ]
            assert event["historical_status_authority"] is False
        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_root / "research" / "sources"


def test_unrelated_research_record_does_not_route_to_source_audit():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research" / "sources").mkdir(parents=True)
        (root / "research").mkdir(parents=True, exist_ok=True)

        manifest = root / "research" / "sources" / "example.yml"
        referenced = root / "research" / "record.md"
        unrelated = root / "research" / "other.md"

        manifest.write_text(
            "source_id: EXAMPLE-1\n"
            "repository_path: research/record.md\n"
        )
        referenced.write_text("# Referenced\n")
        unrelated.write_text("# Unrelated\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            events = router.route(
                ["research/other.md"],
                "2026-09-18",
            )["changes"]

            event = events[0]

            assert event["change_type"] == "research_record_change"
            assert event["routing_destination"] == "research_audit"
            assert event["referencing_manifests"] == []
        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_manifest_dir


def test_simultaneous_manifest_and_referenced_record_changes():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research" / "sources").mkdir(parents=True)
        (root / "research").mkdir(parents=True, exist_ok=True)

        manifest = root / "research" / "sources" / "example.yml"
        record = root / "research" / "record.md"

        manifest.write_text(
            "source_id: EXAMPLE-1\n"
            "repository_path: research/record.md\n"
        )
        record.write_text("# Example record\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            report = router.route(
                [
                    "research/sources/example.yml",
                    "research/record.md",
                ],
                "2026-09-18",
            )

            assert report["change_count"] == 2

            destinations = {
                event["artifact_path"]: event["routing_destination"]
                for event in report["changes"]
            }

            assert destinations == {
                "research/sources/example.yml": "source_library_integrity_audit",
                "research/record.md": "source_library_integrity_audit",
            }
        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_manifest_dir


def test_routing_preserves_review_state_without_assigning_status():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research" / "sources").mkdir(parents=True)
        (root / "research").mkdir(parents=True, exist_ok=True)

        manifest = root / "research" / "sources" / "example.yml"
        record = root / "research" / "record.md"

        manifest.write_text(
            "source_id: EXAMPLE-1\n"
            "repository_path: research/record.md\n"
        )
        record.write_text("# Example record\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            event = router.route(
                ["research/record.md"],
                "2026-09-18",
            )["changes"][0]

            assert event["preservation_result"] == "PRESERVED"
            assert event["review_status"] == "PENDING_REVIEW"
            assert event["next_action"].startswith("Run the routed")
            assert "PROOF" not in json.dumps(event)
            assert "PLAUSIBLE" not in json.dumps(event)
        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_manifest_dir



def test_routing_appends_system_test_event_without_touching_canonical_ledger():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research" / "sources").mkdir(parents=True)
        (root / "research").mkdir(parents=True, exist_ok=True)

        manifest = root / "research" / "sources" / "example.yml"
        record = root / "research" / "record.md"
        event_file = root / "events.jsonl"

        manifest.write_text(
            "source_id: EXAMPLE-1\n"
            "repository_path: research/record.md\n"
        )
        record.write_text("# Example record\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            report = router.route(
                ["research/record.md"],
                "2026-09-18",
                event_file=event_file,
            )

            event = report["changes"][0]

            assert event_file.exists()

            lines = event_file.read_text(encoding="utf-8").splitlines()
            assert len(lines) == 1

            spine_event = json.loads(lines[0])

            assert spine_event["event_class"] == "SYSTEM_TEST"
            assert spine_event["agent"] == "CORPUS_CHANGE_ROUTER"
            assert spine_event["action"] == "CORPUS_CHANGE_ROUTED"
            assert spine_event["target"] == "research/record.md"
            assert spine_event["status"] == "PENDING_REVIEW"

            routing_context = json.loads(spine_event["result"])

            assert routing_context["routing_event_id"] == event["event_id"]
            assert routing_context["artifact_path"] == event["artifact_path"]
            assert routing_context["old_hash"] == event["old_hash"]
            assert routing_context["new_hash"] == event["new_hash"]
            assert routing_context["routing_destination"] == (
                "source_library_integrity_audit"
            )
            assert routing_context["historical_status_authority"] is False
            assert routing_context["review_status"] == "PENDING_REVIEW"

            assert "PROOF" not in json.dumps(spine_event)
            assert "PLAUSIBLE" not in json.dumps(spine_event)

        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_manifest_dir


def test_control_plane_change_routes_to_control_plane_review():
    router = load_router()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "research_control").mkdir(parents=True)

        contract = root / "research_control" / "ARCHITECTURE_CONTRACT.md"
        contract.write_text("# Synthetic control-plane contract\n")

        original_root = router.ROOT
        original_manifest_dir = router.SOURCE_MANIFEST_DIR

        try:
            router.ROOT = root
            router.SOURCE_MANIFEST_DIR = root / "research" / "sources"

            event = router.route(
                ["research_control/ARCHITECTURE_CONTRACT.md"],
                "2026-09-18",
            )["changes"][0]

            assert event["population"] == "research_control"
            assert event["change_type"] == "control_plane_change"
            assert event["routing_destination"] == (
                "control_plane_integrity_and_regression"
            )
            assert event["required_test"] == (
                "control_plane_integrity_and_regression"
            )
            assert event["historical_status_authority"] is False
            assert event["preservation_result"] == "PRESERVED"
            assert event["review_status"] == "PENDING_REVIEW"
            assert "PROOF" not in json.dumps(event)
            assert "PLAUSIBLE" not in json.dumps(event)
        finally:
            router.ROOT = original_root
            router.SOURCE_MANIFEST_DIR = original_manifest_dir


def main():
    test_manifest_routes_to_source_audit()
    test_referenced_record_routes_to_source_audit()
    test_unrelated_research_record_does_not_route_to_source_audit()
    test_simultaneous_manifest_and_referenced_record_changes()
    test_routing_preserves_review_state_without_assigning_status()
    test_routing_appends_system_test_event_without_touching_canonical_ledger()
    test_control_plane_change_routes_to_control_plane_review()
    print("PASS: corpus change router regression tests")


if __name__ == "__main__":
    main()
