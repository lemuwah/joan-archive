#!/usr/bin/env python3
"""Read-only integrity audit for the Joan Archive research-control ledgers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research_control.tools import append_event


def main() -> int:
    failures = 0

    print("JOAN ARCHIVE RESEARCH-CONTROL INTEGRITY AUDIT")
    print("READ-ONLY: no files will be modified")
    print()

    for kind, ledger in append_event.LEDGERS.items():
        schema = append_event.load_schema(kind)
        id_field = append_event.ID_FIELDS[kind]
        id_pattern = append_event.ID_PATTERNS[kind]

        count = 0
        unique_ids: set[str] = set()

        if not ledger.exists():
            print(f"FAIL {kind}: ledger missing: {ledger}")
            failures += 1
            continue

        for line_number, line in enumerate(
            ledger.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                print(
                    f"FAIL {kind}: invalid JSON at line "
                    f"{line_number}: {exc}"
                )
                failures += 1
                continue

            if not isinstance(record, dict):
                print(
                    f"FAIL {kind}: line {line_number} "
                    "is not an object"
                )
                failures += 1
                continue

            count += 1

            errors = append_event.validate(
                record,
                schema,
                "record",
            )

            event_id = record.get(id_field)

            if not isinstance(event_id, str):
                errors.append(
                    f"record.{id_field}: missing or not a string"
                )
            elif not id_pattern.fullmatch(event_id):
                errors.append(
                    f"record.{id_field}: invalid ID {event_id!r}"
                )

            if event_id in unique_ids:
                errors.append(
                    f"duplicate {id_field}: {event_id}"
                )
            elif event_id is not None:
                unique_ids.add(event_id)

            if errors:
                for error in errors:
                    print(
                        f"FAIL {kind}: line {line_number}: "
                        f"{error}"
                    )
                failures += len(errors)

        print(
            f"OK   {kind}: {count} record(s), "
            f"{len(unique_ids)} unique ID(s)"
        )

    print()

    if failures:
        print(f"INTEGRITY FAILURES: {failures}")
        return 1

    print("INTEGRITY CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())