#!/usr/bin/env python3
"""Read-only audit of search arrivals and Found Artifact publication."""

from __future__ import annotations

import json
from pathlib import Path

import record_found_artifacts
import record_search_arrivals


def read_jsonl(
    path: Path, kind: str
) -> tuple[list[dict], list[dict], bool]:
    records = []
    findings = []

    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return records, findings, False
    except UnicodeDecodeError as exc:
        findings.append({
            "code": f"INVALID_{kind}_ENCODING",
            "error": str(exc),
            "message": (
                f"The {kind.lower()} ledger is not valid UTF-8 text; "
                "publication completeness could not be audited."
            ),
        })
        return records, findings, True
    except OSError as exc:
        findings.append({
            "code": f"{kind}_READ_ERROR",
            "error": str(exc),
            "message": (
                f"The {kind.lower()} ledger could not be read; "
                "publication completeness could not be audited."
            ),
        })
        return records, findings, True

    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            findings.append({
                "code": f"MALFORMED_{kind}_LINE",
                "line": line_number,
                "error": str(exc),
                "message": "Malformed ledger line; later lines were still checked.",
            })
            continue

        if not isinstance(value, dict):
            findings.append({
                "code": f"INVALID_{kind}_SHAPE",
                "line": line_number,
                "value_type": type(value).__name__,
                "message": "Ledger line is not a JSON object.",
            })
            continue

        records.append(value)

    return records, findings, False


def audit_execution_publications(
    *,
    result_path: Path,
    event_file: Path,
    arrival_file: Path,
    artifact_file: Path,
) -> dict:
    """Audit one execution's downstream publication without writing anything."""
    result_path = Path(result_path)
    base = {
        "result_path": str(result_path),
        "target_id": None,
        "run_id": None,
        "findings": [],
    }
    findings = base["findings"]

    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append({
            "code": "MALFORMED_RESULT_JSON",
            "error": str(exc),
            "message": "The result artifact could not be read as valid JSON.",
        })
        return base

    if not isinstance(result, dict):
        findings.append({
            "code": "INVALID_RESULT_SHAPE",
            "value_type": type(result).__name__,
            "message": "The result artifact's top-level value is not an object.",
        })
        return base

    target_id = result.get("target_id")
    run_id = result.get("run_id")
    base.update({"target_id": target_id, "run_id": run_id})

    events, event_findings, events_unreadable = read_jsonl(
        Path(event_file), "EVENT"
    )
    findings.extend(event_findings)

    if events_unreadable:
        findings.append({
            "code": "DOWNSTREAM_AUDIT_SKIPPED_UNREADABLE_LEDGER",
            "ledger": "EVENT",
            "message": (
                "Downstream attribution was skipped because the execution "
                "event ledger could not be inspected."
            ),
        })
        return base

    matching_events = [
        event for event in events
        if event.get("action") == "SEARCH_TARGET_EXECUTED"
        and event.get("target") == target_id
        and isinstance(event.get("search_scope"), dict)
        and event["search_scope"].get("run_id") == run_id
    ]

    if not matching_events:
        findings.append({
            "code": "MISSING_EXECUTION_EVENT",
            "target_id": target_id,
            "run_id": run_id,
            "message": "No matching SEARCH_TARGET_EXECUTED event was found.",
        })
        return base

    if len(matching_events) > 1:
        findings.append({
            "code": "MULTIPLE_EXECUTION_EVENTS",
            "target_id": target_id,
            "run_id": run_id,
            "message": "Multiple execution events match this target and run.",
        })
        findings.append({
            "code": "DOWNSTREAM_AUDIT_SKIPPED_AMBIGUOUS_EVENT",
            "target_id": target_id,
            "run_id": run_id,
            "message": (
                "Downstream attribution was skipped because multiple "
                "execution events match this target and run."
            ),
        })
        return base

    event = matching_events[0]
    event_id = event.get("event_id")

    if result.get("event_id") != event_id:
        findings.append({
            "code": "RESULT_EVENT_ID_MISMATCH",
            "result_event_id": result.get("event_id"),
            "execution_event_id": event_id,
            "message": "The result event_id does not match its execution event.",
        })

    expected_sources = event["search_scope"].get("sources", [])
    if not isinstance(expected_sources, list):
        findings.append({
            "code": "INVALID_EXPECTED_SOURCES",
            "message": "Execution event search_scope.sources is not a list.",
        })
        expected_sources = []

    invalid_sources = [
        {
            "index": index,
            "value_type": type(source_name).__name__,
        }
        for index, source_name in enumerate(expected_sources)
        if not isinstance(source_name, str)
    ]

    if invalid_sources:
        findings.append({
            "code": "INVALID_EXPECTED_SOURCE",
            "sources": invalid_sources,
            "message": (
                "Execution event search_scope.sources contains "
                "one or more non-string source declarations."
            ),
        })
        findings.append({
            "code": "DOWNSTREAM_AUDIT_SKIPPED_INVALID_SOURCE_DECLARATION",
            "sources": invalid_sources,
            "message": (
                "Downstream attribution was skipped because the execution "
                "event contains an invalid source declaration."
            ),
        })
        return base

    seen_sources = set()
    duplicate_sources = []
    for source_name in expected_sources:
        if not isinstance(source_name, str):
            continue
        if source_name in seen_sources and source_name not in duplicate_sources:
            duplicate_sources.append(source_name)
        seen_sources.add(source_name)

    if duplicate_sources:
        findings.append({
            "code": "DUPLICATE_EXPECTED_SOURCE",
            "sources": duplicate_sources,
            "message": "Execution event declares one or more sources more than once.",
        })
        findings.append({
            "code": "DOWNSTREAM_AUDIT_SKIPPED_DUPLICATE_SOURCE_DECLARATION",
            "sources": duplicate_sources,
            "message": (
                "Downstream attribution was skipped because the execution "
                "event contains duplicate source declarations."
            ),
        })
        return base

    expected_search_ids = {
        record_search_arrivals.search_id(target_id, source_name, event_id)
        for source_name in expected_sources
        if isinstance(source_name, str)
    }

    source_results = result.get("source_results")
    if not isinstance(source_results, dict):
        findings.append({
            "code": "INVALID_SOURCE_RESULTS",
            "message": "Result source_results is not an object.",
        })
        source_results = {}

    for source_name in source_results:
        if source_name not in expected_sources:
            findings.append({
                "code": "UNEXPECTED_SOURCE_RESULT",
                "source": source_name,
                "message": "Result contains a source not declared by the event.",
            })

    arrivals, arrival_findings, arrivals_unreadable = read_jsonl(
        Path(arrival_file), "ARRIVAL"
    )
    findings.extend(arrival_findings)

    artifacts, artifact_findings, artifacts_unreadable = read_jsonl(
        Path(artifact_file), "FOUND_ARTIFACT"
    )
    findings.extend(artifact_findings)

    if arrivals_unreadable or artifacts_unreadable:
        unreadable_ledgers = []
        if arrivals_unreadable:
            unreadable_ledgers.append("ARRIVAL")
        if artifacts_unreadable:
            unreadable_ledgers.append("FOUND_ARTIFACT")

        findings.append({
            "code": "DOWNSTREAM_AUDIT_SKIPPED_UNREADABLE_LEDGER",
            "ledgers": unreadable_ledgers,
            "message": (
                "Downstream completeness checks were skipped because one "
                "or more publication ledgers could not be inspected."
            ),
        })
        return base

    # Match arrivals by target and source first. This allows a wrong event
    # reference to be reported as a mismatch rather than hidden as a missing row.
    relevant_arrivals = [
        arrival for arrival in arrivals
        if isinstance(arrival.get("provenance"), dict)
        and arrival["provenance"].get("session") == target_id
        and isinstance(arrival.get("source"), dict)
        and arrival["source"].get("name") in expected_sources
    ]

    for source_name in expected_sources:
        source_record = source_results.get(source_name)

        if not isinstance(source_record, dict):
            findings.append({
                "code": "MISSING_SOURCE_RESULT",
                "source": source_name,
                "target_id": target_id,
                "run_id": run_id,
                "message": "The event declares this source, but the result has no source entry.",
            })
            continue

        expected_search_id = record_search_arrivals.search_id(
            target_id, source_name, event_id
        )

        source_arrivals = [
            arrival for arrival in relevant_arrivals
            if arrival["source"].get("name") == source_name
            and (
                arrival.get("search_id") == expected_search_id
                or arrival.get("provenance", {}).get("execution_event_id")
                == event_id
            )
        ]

        if not source_arrivals:
            findings.append({
                "code": "MISSING_SOURCE_ARRIVAL",
                "source": source_name,
                "target_id": target_id,
                "run_id": run_id,
                "message": "No source arrival was published for this source.",
            })
            continue

        if len(source_arrivals) > 1:
            findings.append({
                "code": "DUPLICATE_SOURCE_ARRIVAL",
                "source": source_name,
                "search_ids": [
                    arrival.get("search_id") for arrival in source_arrivals
                ],
                "message": "Multiple source arrivals match this target and source.",
            })

        arrival = source_arrivals[0]
        provenance = arrival.get("provenance", {})

        if provenance.get("execution_event_id") != event_id:
            findings.append({
                "code": "ARRIVAL_EVENT_MISMATCH",
                "source": source_name,
                "arrival_event_id": provenance.get("execution_event_id"),
                "execution_event_id": event_id,
                "message": "The arrival points to a different execution event.",
            })

        search_id = arrival.get("search_id")

        if search_id != expected_search_id:
            findings.append({
                "code": "ARRIVAL_ID_MISMATCH",
                "source": source_name,
                "expected_search_id": expected_search_id,
                "actual_search_id": search_id,
                "message": "The arrival search_id does not match its deterministic identity.",
            })

        arrival_result = arrival.get("result")
        result_ref = (
            arrival_result.get("artifact_ref")
            if isinstance(arrival_result, dict)
            else None
        )
        try:
            path_matches = (
                bool(result_ref)
                and Path(result_ref).resolve() == result_path.resolve()
            )
        except (OSError, RuntimeError, TypeError, ValueError):
            path_matches = False

        if not path_matches:
            findings.append({
                "code": "ARRIVAL_RESULT_PATH_MISMATCH",
                "source": source_name,
                "arrival_artifact_ref": result_ref,
                "result_path": str(result_path.resolve()),
                "message": "The arrival does not point to this result artifact.",
            })

        linked_artifacts = [
            artifact for artifact in artifacts
            if isinstance(artifact.get("search_ref"), dict)
            and artifact["search_ref"].get("search_id") == search_id
        ]

        invalid_artifact_ids = [
            {
                "value_type": type(artifact.get("artifact_id")).__name__,
            }
            for artifact in linked_artifacts
            if not isinstance(artifact.get("artifact_id"), str)
        ]

        for invalid_id in invalid_artifact_ids:
            findings.append({
                "code": "INVALID_FOUND_ARTIFACT_ID",
                "source": source_name,
                **invalid_id,
                "message": (
                    "A linked Found Artifact has a non-string artifact_id; "
                    "it cannot be used for artifact identity matching."
                ),
            })

        artifact_ids = [
            artifact.get("artifact_id")
            for artifact in linked_artifacts
            if isinstance(artifact.get("artifact_id"), str)
        ]
        duplicate_ids = {
            value for value in artifact_ids
            if artifact_ids.count(value) > 1
        }

        if duplicate_ids:
            findings.append({
                "code": "DUPLICATE_FOUND_ARTIFACT",
                "source": source_name,
                "artifact_ids": sorted(duplicate_ids),
                "message": "A Found Artifact identity appears more than once.",
            })

        source_records = source_record.get("results")
        if not isinstance(source_records, list):
            findings.append({
                "code": "INVALID_SOURCE_RESULT_LIST",
                "source": source_name,
                "message": "The source results field is not a list.",
            })
            continue

        expected_outcome, expected_visibility = (
            record_search_arrivals.outcome_for(
                result.get("result_status", ""),
                source_records,
                source_record.get("error"),
            )
        )

        actual_outcome = (
            arrival_result.get("outcome")
            if isinstance(arrival_result, dict)
            else None
        )
        actual_visibility = arrival.get("visibility")

        if (
            actual_outcome != expected_outcome
            or actual_visibility != expected_visibility
        ):
            findings.append({
                "code": "SOURCE_OUTCOME_MISMATCH",
                "source": source_name,
                "expected_outcome": expected_outcome,
                "actual_outcome": actual_outcome,
                "expected_visibility": expected_visibility,
                "actual_visibility": actual_visibility,
                "message": "The arrival outcome or visibility disagrees with the source result and error.",
            })

        if source_record.get("error") and linked_artifacts:
            findings.append({
                "code": "ARTIFACT_FOR_ERROR_SOURCE",
                "source": source_name,
                "artifact_ids": [
                    artifact.get("artifact_id")
                    for artifact in linked_artifacts
                ],
                "message": "Found Artifacts are linked to a source arrival that records an error.",
            })

        expected_artifact_ids = set()
        if not source_record.get("error") and source_records:
            expected_artifact_ids = {
                record_found_artifacts.artifact_id(search_id, record, index)
                for index, record in enumerate(source_records)
            }

        for missing_id in sorted(
            expected_artifact_ids - set(artifact_ids)
        ):
            findings.append({
                "code": "MISSING_FOUND_ARTIFACT",
                "source": source_name,
                "artifact_id": missing_id,
                "search_id": search_id,
                "message": "A returned source result has no corresponding Found Artifact.",
            })

        for artifact in linked_artifacts:
            search_ref = artifact.get("search_ref", {})
            artifact_source = artifact.get("source", {})

            if (
                search_ref.get("target_id") != target_id
                or search_ref.get("execution_event_id") != event_id
                or not isinstance(artifact_source, dict)
                or artifact_source.get("name") != source_name
            ):
                findings.append({
                    "code": "FOUND_ARTIFACT_LINKAGE_MISMATCH",
                    "source": source_name,
                    "artifact_id": artifact.get("artifact_id"),
                    "message": "A Found Artifact has inconsistent target, event, or source linkage.",
                })

    for artifact in artifacts:
        search_ref = artifact.get("search_ref")
        if not isinstance(search_ref, dict):
            continue

        if (
            search_ref.get("target_id") != target_id
            or search_ref.get("execution_event_id") != event_id
        ):
            continue

        artifact_search_id = search_ref.get("search_id")

        if not isinstance(artifact_search_id, str):
            findings.append({
                "code": "INVALID_FOUND_ARTIFACT_SEARCH_ID",
                "artifact_id": artifact.get("artifact_id"),
                "value_type": type(artifact_search_id).__name__,
                "message": (
                    "A Found Artifact linked to this execution event has "
                    "a non-string search_id; it cannot be used for "
                    "search identity matching."
                ),
            })
            continue

        if artifact_search_id not in expected_search_ids:
            findings.append({
                "code": "UNEXPECTED_FOUND_ARTIFACT",
                "artifact_id": artifact.get("artifact_id"),
                "search_id": artifact_search_id,
                "message": (
                    "A Found Artifact is linked to this execution event "
                    "but its search_id is not declared by the event."
                ),
            })

    return base
