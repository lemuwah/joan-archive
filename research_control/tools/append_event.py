#!/usr/bin/env python3
"""Validate and append one zero-trust research-control event."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LEDGERS = {
    "claim": ROOT / "research_control/claims.jsonl",
    "search": ROOT / "research_control/search_events.jsonl",
    "evidence": ROOT / "research_control/evidence_events.jsonl",
    "review": ROOT / "research_control/review_events.jsonl",
    "status": ROOT / "research_control/status_events.jsonl",
}

SCHEMAS = {
    "claim": ROOT / "research_control/schemas/claim.schema.json",
    "search": ROOT / "research_control/schemas/search_event.schema.json",
    "evidence": ROOT / "research_control/schemas/evidence_event.schema.json",
    "review": ROOT / "research_control/schemas/review_event.schema.json",
    "status": ROOT / "research_control/schemas/status_event.schema.json",
}

ID_FIELDS = {
    "claim": "claim_id",
    "search": "search_id",
    "evidence": "evidence_id",
    "review": "review_id",
    "status": "status_id",
}

ID_PATTERNS = {
    "claim": re.compile(r"^CLAIM-[0-9]{6}$"),
    "search": re.compile(r"^SEARCH-[0-9]{6}$"),
    "evidence": re.compile(r"^EVID-[0-9]{6}$"),
    "review": re.compile(r"^REVIEW-[0-9]{6}$"),
    "status": re.compile(r"^STATUS-[0-9]{6}$"),
}


def load_schema(kind: str) -> dict:
    return json.loads(SCHEMAS[kind].read_text(encoding="utf-8"))


def validate(value, schema: dict, path: str = "record") -> list[str]:
    errors: list[str] = []

    expected = schema.get("type")

    if expected == "object":
        if not isinstance(value, dict):
            return [f"{path}: expected object"]

        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path}: missing required field {field}")

        properties = schema.get("properties", {})

        if schema.get("additionalProperties") is False:
            unknown = set(value) - set(properties)
            for field in sorted(unknown):
                errors.append(f"{path}: unknown field {field}")

        for field, field_value in value.items():
            if field in properties:
                errors.extend(
                    validate(field_value, properties[field], f"{path}.{field}")
                )

    elif expected == "array":
        if not isinstance(value, list):
            return [f"{path}: expected array"]

        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(
                f"{path}: requires at least {schema['minItems']} item(s)"
            )

        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(
                    validate(item, item_schema, f"{path}[{index}]")
                )

    elif expected == "string":
        if not isinstance(value, str):
            return [f"{path}: expected string"]

        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(
                f"{path}: shorter than minimum length {schema['minLength']}"
            )

        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            errors.append(f"{path}: does not match pattern {pattern}")

        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"{path}: invalid enum value {value!r}")

        if schema.get("format") == "date-time":
            try:
                dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{path}: invalid date-time")

    elif expected == "boolean":
        if not isinstance(value, bool):
            errors.append(f"{path}: expected boolean")

    elif expected == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{path}: expected integer")

    elif expected == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{path}: expected number")

    return errors


def existing_ids(path: Path, id_field: str) -> set[str]:
    ids: set[str] = set()

    if not path.exists():
        return ids

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"REFUSING TO APPEND: existing ledger has invalid JSON "
                f"at {path}:{line_number}: {exc}"
            )

        if not isinstance(record, dict):
            raise SystemExit(
                f"REFUSING TO APPEND: existing ledger has a non-object "
                f"record at {path}:{line_number}"
            )

        if id_field in record:
            ids.add(record[id_field])

    return ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=LEDGERS)
    parser.add_argument("json_file")
    parser.add_argument("--dry-run", action="store_true", help="validate without modifying the ledger")
    args = parser.parse_args()

    kind = args.kind
    ledger = LEDGERS[kind]
    schema = load_schema(kind)
    id_field = ID_FIELDS[kind]

    try:
        record = json.loads(
            Path(args.json_file).read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        print(
            f"ERROR: input file not found: {args.json_file}",
            file=sys.stderr,
        )
        return 1
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: input JSON is invalid: {exc}",
            file=sys.stderr,
        )
        return 1

    errors = validate(record, schema)

    if not isinstance(record, dict):
        errors.append("record: expected object")

    event_id = record.get(id_field) if isinstance(record, dict) else None

    if not isinstance(event_id, str):
        errors.append(f"record.{id_field}: missing or not a string")
    elif not ID_PATTERNS[kind].fullmatch(event_id):
        errors.append(
            f"record.{id_field}: invalid ID {event_id!r}"
        )

    if errors:
        print("REFUSING TO APPEND:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    ids = existing_ids(ledger, id_field)

    if event_id in ids:
        print(
            f"REFUSING TO APPEND: duplicate {id_field} {event_id}",
            file=sys.stderr,
        )
        return 1

    ledger.parent.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print(f"DRY-RUN OK: {event_id} would append -> {ledger.relative_to(ROOT)}")
        return 0

    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                record,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        handle.write("\n")

    print(
        f"APPENDED {event_id} -> {ledger.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
