#!/usr/bin/env python3
"""Classify corpus changes and route them to existing specialized audits.

This router identifies what changed and which review process owns that change.
It does not assign historical status, validate historical truth, or replace
specialized audit tools.

Failure principle:
    PRESERVE -> FLAG -> ROUTE FOR REVIEW
rather than
    GUESS -> NORMALIZE -> DELETE
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_MANIFEST_DIR = ROOT / "research" / "sources"
SOURCE_AUDITOR = ROOT / "tools" / "audit_source_library.py"
EVENT_SPINE = ROOT / "research_queue" / "research_events.jsonl"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_manifest_paths() -> list[Path]:
    if not SOURCE_MANIFEST_DIR.exists():
        return []
    return sorted(SOURCE_MANIFEST_DIR.glob("*.yml"))


def referenced_source_records() -> dict[str, list[str]]:
    """Return repository-path -> manifest paths for source-library references."""
    references: dict[str, list[str]] = {}

    for manifest in source_manifest_paths():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped.startswith("repository_path:"):
                continue

            value = stripped.split(":", 1)[1].strip().strip("'\"")
            if not value:
                continue

            references.setdefault(value, []).append(repo_path(manifest))

    return references


def classify_path(path: str, referenced: dict[str, list[str]]) -> dict:
    normalized = path.replace("\\", "/")

    if normalized.startswith("research/sources/") and normalized.endswith(".yml"):
        return {
            "population": "research/sources",
            "change_type": "source_library_manifest_change",
            "routing_destination": "source_library_integrity_audit",
            "upstream_dependency": "source manifest",
            "referencing_manifests": [normalized],
        }

    if normalized in referenced:
        return {
            "population": "research",
            "change_type": "source_library_referenced_record_change",
            "routing_destination": "source_library_integrity_audit",
            "upstream_dependency": "source-library manifest declaration",
            "referencing_manifests": referenced[normalized],
        }

    if normalized.startswith("research_control/"):
        return {
            "population": "research_control",
            "change_type": "control_plane_change",
            "routing_destination": "control_plane_integrity_and_regression",
            "upstream_dependency": "research control plane",
            "referencing_manifests": [],
        }

    if normalized.startswith("research_findings/") and normalized.endswith(".md"):
        return {
            "population": "research_findings",
            "change_type": "finding_change",
            "routing_destination": "findings_router",
            "upstream_dependency": "findings pipeline",
            "referencing_manifests": [],
        }

    if normalized.startswith("research/"):
        return {
            "population": "research",
            "change_type": "research_record_change",
            "routing_destination": "research_audit",
            "upstream_dependency": "research corpus",
            "referencing_manifests": [],
        }

    return {
        "population": "unclassified",
        "change_type": "unclassified_change",
        "routing_destination": "manual_review",
        "upstream_dependency": "",
        "referencing_manifests": [],
    }


def changed_paths() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-status", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    paths: list[str] = []

    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        fields = line.split("\t")

        # Modified / added / deleted: status + path.
        if fields[0][0] not in {"R", "C"}:
            if len(fields) >= 2:
                paths.append(fields[1])

        # Rename/copy: status + old path + new path.
        if fields[0][0] in {"R", "C"} and len(fields) >= 3:
            paths.extend([fields[1], fields[2]])

    # Include untracked files because they are still corpus changes that need
    # routing before they disappear into an unreviewed commit.
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    paths.extend(
        line.strip()
        for line in untracked.stdout.splitlines()
        if line.strip()
    )

    return sorted(set(paths))


def head_hash(path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        text=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return hashlib.sha256(result.stdout).hexdigest()


def build_event(path: str, referenced: dict[str, list[str]], run_date: str) -> dict:
    classification = classify_path(path, referenced)
    absolute = ROOT / path

    old_hash = head_hash(path)
    new_hash = sha256(absolute) if absolute.exists() and absolute.is_file() else None

    return {
        "event_id": "CCR-"
        + hashlib.sha256(
            f"{path}:{new_hash}:{run_date}".encode("utf-8")
        ).hexdigest()[:12],
        "event": "CORPUS_CHANGE_ROUTING",
        "detection_date": run_date,
        "artifact_path": path,
        "population": classification["population"],
        "change_type": classification["change_type"],
        "old_hash": old_hash,
        "new_hash": new_hash,
        "source_or_run_identifier": "",
        "upstream_dependency": classification["upstream_dependency"],
        "affected_historical_bearing_content": True,
        "historical_status_authority": False,
        "required_test": classification["routing_destination"],
        "routing_destination": classification["routing_destination"],
        "preservation_result": "PRESERVED",
        "review_status": "PENDING_REVIEW",
        "contradictions_affected": [],
        "referencing_manifests": classification["referencing_manifests"],
        "next_action": (
            "Run the routed specialized audit/review process; "
            "do not infer historical status from this routing event."
        ),
    }


def append_routing_events(events: list[dict], event_file: Path) -> None:
    """Append corpus-routing audit events to the existing Event Spine."""
    import sys

    event_spine_dir = Path(__file__).resolve().parent
    if str(event_spine_dir) not in sys.path:
        sys.path.insert(0, str(event_spine_dir))

    from event_spine import record_event

    for event in events:
        routing_context = {
            "routing_event_id": event["event_id"],
            "artifact_path": event["artifact_path"],
            "population": event["population"],
            "change_type": event["change_type"],
            "old_hash": event["old_hash"],
            "new_hash": event["new_hash"],
            "routing_destination": event["routing_destination"],
            "required_test": event["required_test"],
            "preservation_result": event["preservation_result"],
            "review_status": event["review_status"],
            "historical_status_authority": event["historical_status_authority"],
            "referencing_manifests": event["referencing_manifests"],
        }

        record_event(
            agent="CORPUS_CHANGE_ROUTER",
            action="CORPUS_CHANGE_ROUTED",
            target=event["artifact_path"],
            source="corpus_change_routing.json",
            result=json.dumps(routing_context, sort_keys=True),
            status=event["review_status"],
            next_action=event["next_action"],
            event_class="SYSTEM_TEST",
            event_file=event_file,
        )


def route(
    paths: list[str],
    run_date: str,
    event_file: Path | None = None,
) -> dict:
    referenced = referenced_source_records()

    events = [
        build_event(path, referenced, run_date)
        for path in paths
    ]

    if event_file is not None:
        append_routing_events(events, event_file)

    return {
        "event": "CORPUS_CHANGE_ROUTING_RUN",
        "run_date": run_date,
        "router_version": "1",
        "historical_status_authority": False,
        "failure_principle": "PRESERVE -> FLAG -> ROUTE FOR REVIEW",
        "change_count": len(events),
        "changes": events,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--output",
        default="research_control/corpus_change_routing.json",
    )
    args = parser.parse_args()

    paths = sorted(set(args.path)) if args.path else changed_paths()

    # --check is read-only: never append an Event Spine audit event.
    event_file = None if args.check else EVENT_SPINE
    report = route(paths, args.date, event_file)

    output = ROOT / args.output

    if args.check:
        if not output.exists():
            print("CORPUS ROUTER: no routing report exists")
            return 1

        expected = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if output.read_text(encoding="utf-8") != expected:
            print("CORPUS ROUTER: routing report is stale")
            return 1

        print("CORPUS ROUTER: report is current")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"CORPUS ROUTER: {len(paths)} changes classified")
    for event in report["changes"]:
        print(
            f"- {event['artifact_path']} -> "
            f"{event['routing_destination']} "
            f"({event['change_type']})"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
