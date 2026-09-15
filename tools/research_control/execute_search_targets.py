#!/usr/bin/env python3
"""Execute explicitly READY research targets without promoting historical claims."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path

import requests
import yaml

from event_spine import record_event
from search_targets import mark_target_executed

ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "research_queue" / "SEARCH_TARGETS.yml"
RESULT_DIR = ROOT / "research_queue" / "search_results"

IA_ENDPOINT = "https://archive.org/advancedsearch.php"
LOC_ENDPOINT = "https://www.loc.gov/search/"


def load_targets(path: Path) -> dict:
    if not path.exists():
        return {"targets": []}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data.setdefault("targets", [])
    return data


def build_query(target: dict) -> str:
    parts = []

    people = target.get("person_slots") or []
    variants = target.get("name_variants") or []
    families = target.get("record_families") or []
    jurisdictions = target.get("jurisdictions") or []

    names = []
    for value in people + variants:
        value = str(value).strip()
        if value and value not in names:
            names.append(value)

    if names:
        parts.append("(" + " OR ".join(f'"{name}"' for name in names) + ")")

    if families:
        parts.append(
            "(" + " OR ".join(f'"{family}"' for family in families) + ")"
        )

    if jurisdictions:
        parts.append(
            "(" + " OR ".join(f'"{place}"' for place in jurisdictions) + ")"
        )

    return " ".join(parts) or target.get("question", "").strip()


def ia_search(session: requests.Session, query: str, rows: int) -> list[dict]:
    response = session.get(
        IA_ENDPOINT,
        params={
            "q": query,
            "fl[]": ["identifier", "title", "creator", "date", "description"],
            "rows": rows,
            "page": 1,
            "output": "json",
        },
        timeout=30,
    )
    response.raise_for_status()

    docs = response.json().get("response", {}).get("docs", [])

    return [
        {
            "source": "internet_archive",
            "record_id": doc.get("identifier"),
            "title": doc.get("title"),
            "creator": doc.get("creator"),
            "date": doc.get("date"),
            "url": (
                f"https://archive.org/details/{doc.get('identifier')}"
                if doc.get("identifier")
                else None
            ),
            "description": doc.get("description"),
        }
        for doc in docs
    ]


def loc_search(session: requests.Session, query: str, rows: int) -> list[dict]:
    response = session.get(
        LOC_ENDPOINT,
        params={"q": query, "fo": "json", "c": rows},
        timeout=30,
    )
    response.raise_for_status()

    return [
        {
            "source": "library_of_congress",
            "record_id": item.get("id"),
            "title": item.get("title"),
            "creator": item.get("contributor")
            or item.get("contributor_names"),
            "date": item.get("date"),
            "url": item.get("id"),
            "description": item.get("description"),
        }
        for item in response.json().get("results", [])
    ]


def execute_target(
    target: dict,
    rows: int,
    delay: float,
    dry_run: bool,
) -> dict:
    target_id = target["target_id"]
    query = build_query(target)
    executed_at = dt.datetime.now(dt.timezone.utc).isoformat()

    record = {
        "target_id": target_id,
        "question": target.get("question", ""),
        "target_status": target.get("status"),
        "execution_status": "DRY_RUN" if dry_run else "EXECUTED",
        "executed_at": executed_at,
        "query": query,
        "results": [],
        "errors": [],
        "note": (
            "Search output is a source lead only. It does not establish "
            "historical proof, identity, or certainty."
        ),
    }

    if dry_run:
        return record

    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "joan-archive-target-executor/1.0 "
            "(research use; contact repository owner)"
        )
    })

    for source_name, search in (
        ("internet_archive", ia_search),
        ("library_of_congress", loc_search),
    ):
        try:
            record["results"].extend(search(session, query, rows))
        except Exception as error:
            record["errors"].append({
                "source": source_name,
                "error": str(error),
            })
        time.sleep(delay)

    if record["results"]:
        record["result_status"] = "FOUND"
    elif record["errors"]:
        record["result_status"] = "ERROR"
    else:
        record["result_status"] = "NO_RESULTS"

    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Execute one target ID")
    parser.add_argument(
        "--targets-file",
        default=str(TARGET_FILE),
        help="Path to the target YAML file",
    )
    parser.add_argument("--rows", type=int, default=10)
    parser.add_argument("--delay", type=float, default=0.25)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build the execution record without network calls",
    )
    args = parser.parse_args()

    targets_file = Path(args.targets_file)
    data = load_targets(targets_file)
    targets = data["targets"]

    selected = [
        target for target in targets
        if target.get("status") == "READY"
        and (not args.target or target.get("target_id") == args.target)
    ]

    if args.target and not selected:
        matching = [
            target for target in targets
            if target.get("target_id") == args.target
        ]

        if not matching:
            raise SystemExit(f"TARGET_NOT_FOUND: {args.target}")

        raise SystemExit(
            f"TARGET_NOT_EXECUTABLE: {args.target} "
            f"status={matching[0].get('status')}"
        )

    if not selected:
        print("NO_READY_TARGETS")
        return

    system_tests = [
        target for target in selected
        if target.get("target_type") == "SYSTEM_TEST"
    ]

    if system_tests and not args.dry_run:
        ids = ", ".join(target["target_id"] for target in system_tests)
        raise SystemExit(
            f"SYSTEM_TEST_NETWORK_BLOCKED: {ids}"
        )

    if args.dry_run:
        for target in selected:
            result = execute_target(
                target=target,
                rows=args.rows,
                delay=args.delay,
                dry_run=True,
            )
            print(
                f"DRY_RUN {target['target_id']} "
                f"query={result['query']!r}"
            )
        return

    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    for target in selected:
        result = execute_target(
            target=target,
            rows=args.rows,
            delay=args.delay,
            dry_run=args.dry_run,
        )

        output_path = RESULT_DIR / f"{target['target_id']}.json"
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        event = record_event(
            agent="SEARCH_EXECUTOR",
            action="SEARCH_TARGET_EXECUTED",
            target=target["target_id"],
            laws=target.get("laws", []),
            search_scope={
                "query": result["query"],
                "sources": [
                    "internet_archive",
                    "library_of_congress",
                ],
                "rows": args.rows,
            },
            evidence=str(output_path),
            result=result.get("result_status", result["execution_status"]),
            status=result["execution_status"],
            contradiction=target.get("disproof_record", ""),
            next_action=(
                "Send captured search results through the four-agent "
                "review chain; do not promote directly to proof."
            ),
            parent_event=target.get("origin_event", ""),
            event_class="RESEARCH",
        )

        result["event_id"] = event["event_id"]
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        if result.get("result_status") in {"FOUND", "NO_RESULTS"}:
            mark_target_executed(
                target["target_id"],
                target_file=targets_file,
            )

        print(f"EXECUTED {target['target_id']} -> {output_path}")


if __name__ == "__main__":
    main()
