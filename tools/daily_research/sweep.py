#!/usr/bin/env python3
"""Run a reproducible, review-gated daily source sweep for every people page."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "people"
DEFAULT_OUTPUT = ROOT / "research_queue" / "daily_sweep"

LENSES = {
    "irish_scottish_migration": [
        "Irish", "Ireland", "Ulster", "Scotland", "Scottish", "Donegal", "servant"
    ],
    "servant_indentured_status": [
        "servant", "indentured", "bond servant", "redemptioner", "apprentice", "master"
    ],
    "enslavement_captivity_status": [
        "enslaved", "slave", "captive", "Negro", "Indian", "mulatto", "redemption"
    ],
    "narragansett_indigenous_context": [
        "Narragansett", "Niantic", "sachem", "kin", "mark", "interpreter", "Indian"
    ],
    "legal_property_records": [
        "deed", "land evidence", "probate", "will", "court", "testimony", "dower"
    ],
    "maritime_trade_network": [
        "ship", "vessel", "seaman", "merchant", "Newport", "Boston", "London"
    ],
    "church_civil_registration": [
        "church", "baptism", "marriage", "burial", "parish", "Quaker", "meeting"
    ],
    "regional_geography_variants": [
        "Quidnessett", "Cocumscussoc", "Warwick", "Kingstown", "Pawtuxet", "Narragansett"
    ],
}

IA_ENDPOINT = "https://archive.org/advancedsearch.php"
LOC_ENDPOINT = "https://www.loc.gov/search/"


def person_names() -> list[dict[str, str]]:
    people = []
    for path in sorted(PEOPLE_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        title = next(
            (line.removeprefix("# ").strip() for line in path.read_text(errors="replace").splitlines()
             if line.startswith("# ")),
            path.stem.replace("_", " ").replace("-", " "),
        )
        people.append({"page": str(path.relative_to(ROOT)), "name": title})
    return people


def query_text(name: str, terms: list[str]) -> str:
    # Quotes keep multi-word names together while the lens terms broaden the search.
    return f'"{name}" ("' + '" OR "'.join(terms) + '")'


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
            "url": f"https://archive.org/details/{doc.get('identifier')}" if doc.get("identifier") else None,
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
            "creator": item.get("contributor") or item.get("contributor_names"),
            "date": item.get("date"),
            "url": item.get("id"),
            "description": item.get("description"),
        }
        for item in response.json().get("results", [])
    ]


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:80]


def run(args: argparse.Namespace) -> tuple[Path, Path]:
    run_date = args.date or dt.date.today().isoformat()
    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / f"{run_date}.jsonl"
    summary_path = output_dir / f"{run_date}.summary.json"
    people = person_names()
    lenses = list(LENSES.items())
    session = requests.Session()
    session.headers.update({"User-Agent": "joan-archive-daily-research/1.0 (research use; contact repository owner)"})
    records = []
    query_count = 0

    with result_path.open("w") as output:
        for person in people:
            for lens, terms in lenses:
                if args.max_queries and query_count >= args.max_queries:
                    break
                query = query_text(person["name"], terms)
                base = {
                    "run_date": run_date,
                    "person_page": person["page"],
                    "person_name": person["name"],
                    "lens": lens,
                    "query": query,
                    "status": "DRY_RUN" if args.dry_run else "PENDING_HUMAN_REVIEW",
                    "results": [],
                }
                if not args.dry_run:
                    for source_name, search in (("internet_archive", ia_search), ("library_of_congress", loc_search)):
                        try:
                            base["results"].extend(search(session, query, args.rows))
                        except Exception as error:  # keep the full sweep auditable if one catalog fails
                            base.setdefault("errors", []).append({"source": source_name, "error": str(error)})
                        time.sleep(args.delay)
                    base["status"] = "FOUND" if base["results"] else ("ERROR" if base.get("errors") else "NO_RESULTS")
                output.write(json.dumps(base, ensure_ascii=True) + "\n")
                records.append(base)
                query_count += 1
            if args.max_queries and query_count >= args.max_queries:
                break

    summary = {
        "run_date": run_date,
        "people_pages": len(people),
        "lenses": len(lenses),
        "queries_run": query_count,
        "dry_run": args.dry_run,
        "found_queries": sum(item["status"] == "FOUND" for item in records),
        "no_result_queries": sum(item["status"] == "NO_RESULTS" for item in records),
        "error_queries": sum(item["status"] == "ERROR" for item in records),
        "note": "Candidates and negative results require human review; no claim is verified by this sweep.",
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    return result_path, summary_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="UTC run date, defaults to today")
    parser.add_argument("--output", help="Output directory, defaults to research_queue/daily_sweep")
    parser.add_argument("--rows", type=int, default=10, help="Results per catalog and query")
    parser.add_argument("--delay", type=float, default=0.25, help="Seconds between catalog requests")
    parser.add_argument("--max-queries", type=int, default=0, help="Limit queries for a smoke test; 0 means all")
    parser.add_argument("--dry-run", action="store_true", help="Generate the full query matrix without network calls")
    args = parser.parse_args()
    result_path, summary_path = run(args)
    print(f"Wrote {result_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
