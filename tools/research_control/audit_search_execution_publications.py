#!/usr/bin/env python3
"""Read-only audit of search-result and execution-event publication."""

from __future__ import annotations

import json
from pathlib import Path


def audit_result_event(*, result_path: Path, event_file: Path) -> dict:
    result_path = Path(result_path)
    event_file = Path(event_file)

    try:
        result_text = result_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return {
            "result_path": str(result_path),
            "target_id": None,
            "run_id": None,
            "findings": [{
                "code": "RESULT_INVALID_ENCODING",
                "error": str(exc),
                "message": (
                    "The result artifact is not valid UTF-8 text."
                ),
            }],
        }
    except OSError as exc:
        return {
            "result_path": str(result_path),
            "target_id": None,
            "run_id": None,
            "findings": [{
                "code": "RESULT_READ_ERROR",
                "error": str(exc),
                "message": (
                    "The result artifact could not be read."
                ),
            }],
        }

    try:
        result = json.loads(result_text)
    except json.JSONDecodeError as exc:
        return {
            "result_path": str(result_path),
            "target_id": None,
            "run_id": None,
            "findings": [{
                "code": "MALFORMED_RESULT_JSON",
                "error": str(exc),
                "message": (
                    "The result artifact does not contain valid JSON."
                ),
            }],
        }

    if not isinstance(result, dict):
        return {
            "result_path": str(result_path),
            "target_id": None,
            "run_id": None,
            "findings": [{
                "code": "INVALID_RESULT_SHAPE",
                "value_type": type(result).__name__,
                "message": (
                    "The result artifact contains valid JSON, "
                    "but its top-level value is not an object."
                ),
            }],
        }

    events = []
    event_parse_findings = []

    try:
        event_text = event_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        event_text = ""
    except UnicodeDecodeError as exc:
        return {
            "result_path": str(result_path),
            "target_id": result.get("target_id"),
            "run_id": result.get("run_id"),
            "findings": [{
                "code": "EVENT_LEDGER_INVALID_ENCODING",
                "error": str(exc),
                "message": (
                    "The event ledger is not valid UTF-8 text; "
                    "execution publication could not be audited."
                ),
            }],
        }
    except OSError as exc:
        return {
            "result_path": str(result_path),
            "target_id": result.get("target_id"),
            "run_id": result.get("run_id"),
            "findings": [{
                "code": "EVENT_LEDGER_READ_ERROR",
                "error": str(exc),
                "message": (
                    "The event ledger could not be read; "
                    "execution publication could not be audited."
                ),
            }],
        }

    for line_number, line in enumerate(event_text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            event_parse_findings.append({
                "code": "MALFORMED_EVENT_LINE",
                "event_line": line_number,
                "error": str(exc),
                "message": (
                    "An event ledger line contains invalid JSON; "
                    "the audit continued with subsequent lines."
                ),
            })
            continue
        if not isinstance(event, dict):
            event_parse_findings.append({
                "code": "INVALID_EVENT_SHAPE",
                "event_line": line_number,
                "value_type": type(event).__name__,
                "message": (
                    "An event ledger line contains valid JSON "
                    "but its top-level value is not an object; "
                    "the audit continued with subsequent lines."
                ),
            })
            continue

        if (
            event.get("action") == "SEARCH_TARGET_EXECUTED"
            and "search_scope" in event
            and not isinstance(event["search_scope"], dict)
        ):
            event_parse_findings.append({
                "code": "INVALID_EVENT_SEARCH_SCOPE",
                "event_line": line_number,
                "value_type": type(event["search_scope"]).__name__,
                "message": (
                    "A search execution event has a search_scope "
                    "that is not an object; the event was excluded "
                    "from matching."
                ),
            })
            continue

        event_id = event.get("event_id")
        if (
            event.get("action") == "SEARCH_TARGET_EXECUTED"
            and (
                not isinstance(event_id, str)
                or not event_id.strip()
            )
        ):
            event_parse_findings.append({
                "code": "INVALID_EVENT_ID",
                "event_line": line_number,
                "value_type": type(event_id).__name__,
                "message": (
                    "A search execution event has a missing, empty, "
                    "or non-string event_id; the event was excluded "
                    "from matching."
                ),
            })
            continue

        events.append((line_number, event))

    target_id = result.get("target_id")
    run_id = result.get("run_id")

    matching_events = [
        (line_number, event)
        for line_number, event in events
        if event.get("action") == "SEARCH_TARGET_EXECUTED"
        and event.get("target") == target_id
        and (event.get("search_scope") or {}).get("run_id") == run_id
    ]

    findings = list(event_parse_findings)

    if not matching_events:
        findings.append({
            "code": "RESULT_MISSING_EVENT",
            "target_id": target_id,
            "run_id": run_id,
            "result_path": str(result_path),
            "message": (
                "Result artifact exists, but no matching "
                "SEARCH_TARGET_EXECUTED event was found."
            ),
        })
    else:
        if len(matching_events) > 1:
            findings.append({
                "code": "MULTIPLE_MATCHING_EXECUTION_EVENTS",
                "target_id": target_id,
                "run_id": run_id,
                "event_lines": [
                    line_number
                    for line_number, _ in matching_events
                ],
                "event_ids": [
                    event.get("event_id")
                    for _, event in matching_events
                ],
                "message": (
                    "Multiple execution events match the same "
                    "target and run; publication history is ambiguous."
                ),
            })
            findings.append({
                "code": "DOWNSTREAM_AUDIT_SKIPPED_AMBIGUOUS_EVENT",
                "target_id": target_id,
                "run_id": run_id,
                "message": (
                    "Further publication attribution was skipped because "
                    "multiple execution events match this target and run."
                ),
            })
            return {
                "result_path": str(result_path),
                "target_id": target_id,
                "run_id": run_id,
                "findings": findings,
            }

        event_ids = {
            event.get("event_id")
            for _, event in matching_events
            if event.get("event_id")
        }
        result_event_id = result.get("event_id")

        if (
            "event_id" in result
            and not isinstance(result_event_id, str)
        ):
            findings.append({
                "code": "INVALID_RESULT_EVENT_ID",
                "target_id": target_id,
                "run_id": run_id,
                "value_type": type(result_event_id).__name__,
                "message": (
                    "The result artifact contains a non-string event_id; "
                    "publication attribution cannot be verified."
                ),
            })
        elif not result_event_id:
            findings.append({
                "code": "RESULT_MISSING_EVENT_ID",
                "target_id": target_id,
                "run_id": run_id,
                "message": (
                    "A matching execution event exists, but the "
                    "result does not contain its event_id."
                ),
            })
        elif result_event_id not in event_ids:
            findings.append({
                "code": "RESULT_EVENT_ID_MISMATCH",
                "target_id": target_id,
                "run_id": run_id,
                "result_event_id": result_event_id,
                "matching_event_ids": sorted(event_ids),
                "message": (
                    "The result event_id does not match the "
                    "matching execution event."
                ),
            })

        expected_evidence_path = str(result_path.resolve())
        for line_number, event in matching_events:
            event_evidence_path = event.get("evidence")
            try:
                normalized_event_evidence_path = (
                    str(Path(event_evidence_path).resolve())
                    if event_evidence_path
                    else None
                )
            except (OSError, RuntimeError, TypeError, ValueError):
                normalized_event_evidence_path = None

            if normalized_event_evidence_path != expected_evidence_path:
                findings.append({
                    "code": "EVENT_EVIDENCE_PATH_MISMATCH",
                    "target_id": target_id,
                    "run_id": run_id,
                    "event_line": line_number,
                    "event_evidence": event.get("evidence"),
                    "result_path": expected_evidence_path,
                    "message": (
                        "The execution event evidence path does not "
                        "match the result artifact path."
                    ),
                })

    return {
        "result_path": str(result_path),
        "target_id": target_id,
        "run_id": run_id,
        "findings": findings,
    }
