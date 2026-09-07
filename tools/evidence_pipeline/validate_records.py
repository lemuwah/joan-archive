#!/usr/bin/env python3
"""Validate candidate source JSONL records without publishing or modifying them."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "data/research/source.schema.json"
REQUIRED = {
    "candidate_id", "status", "source_url", "repository", "document_type",
    "people_or_terms", "retrieved_at", "ai_outputs", "proposed_claims",
    "negative_result", "human_disposition",
}
STATUSES = {"PENDING_HUMAN_REVIEW", "VERIFIED_PRIMARY", "VERIFIED_SECONDARY", "REJECTED", "SUSPENDED"}
DISPOSITIONS = {"VERIFIED", "REJECTED", "SUSPENDED", None}
DOCUMENT_TYPES = {"deed", "court", "letter", "map", "church", "probate", "military", "maritime", "genealogy", "secondary", "other"}
CANDIDATE_ID = re.compile(r"^CAND-[0-9]{4}-[0-9]{4,}$")
SHA256 = re.compile(r"^[A-Fa-f0-9]{64}$")


def validate(record: dict, line_number: int) -> list[str]:
    errors = []
    missing = REQUIRED - record.keys()
    if missing:
        errors.append(f"line {line_number}: missing {', '.join(sorted(missing))}")
    if not isinstance(record.get("candidate_id"), str) or not CANDIDATE_ID.fullmatch(record.get("candidate_id", "")):
        errors.append(f"line {line_number}: candidate_id must match CAND-YYYY-NNNN")
    if record.get("status") not in STATUSES:
        errors.append(f"line {line_number}: invalid status")
    url = record.get("source_url")
    if not isinstance(url, str) or not url or (url and urlparse(url).scheme not in {"http", "https"}):
        errors.append(f"line {line_number}: source_url must be an HTTP(S) URL or documented placeholder")
    if not isinstance(record.get("repository"), str) or not record.get("repository", "").strip():
        errors.append(f"line {line_number}: repository is required")
    if record.get("document_type") not in DOCUMENT_TYPES:
        errors.append(f"line {line_number}: invalid document_type")
    if not isinstance(record.get("people_or_terms"), list) or not record.get("people_or_terms"):
        errors.append(f"line {line_number}: people_or_terms must be a non-empty list")
    try:
        dt.datetime.fromisoformat(str(record.get("retrieved_at")).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"line {line_number}: retrieved_at must be ISO-8601")
    for field in ("ai_outputs", "proposed_claims"):
        if not isinstance(record.get(field), list):
            errors.append(f"line {line_number}: {field} must be a list")
    if not isinstance(record.get("negative_result"), bool):
        errors.append(f"line {line_number}: negative_result must be boolean")
    if record.get("human_disposition") not in DISPOSITIONS:
        errors.append(f"line {line_number}: invalid human_disposition")
    if record.get("sha256") and not SHA256.fullmatch(record["sha256"]):
        errors.append(f"line {line_number}: sha256 must be 64 hexadecimal characters")
    if record.get("negative_result"):
        for field in ("query", "searched_repository", "searched_scope"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"line {line_number}: negative result requires {field}")
    if record.get("status") in {"VERIFIED_PRIMARY", "VERIFIED_SECONDARY"}:
        for field in ("repository_id", "image_or_page"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"line {line_number}: verified record requires {field}")
        if record.get("human_disposition") != "VERIFIED":
            errors.append(f"line {line_number}: verified record requires human_disposition=VERIFIED")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="JSONL files to validate")
    args = parser.parse_args()
    errors = []
    seen = set()
    for raw_path in args.paths:
        path = Path(raw_path)
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"{path}:{line_number}: invalid JSON: {error.msg}")
                continue
            if not isinstance(record, dict):
                errors.append(f"{path}:{line_number}: record must be an object")
                continue
            candidate_id = record.get("candidate_id")
            if candidate_id in seen:
                errors.append(f"{path}:{line_number}: duplicate candidate_id {candidate_id}")
            seen.add(candidate_id)
            errors.extend(f"{path}: {error}" for error in validate(record, line_number))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(seen)} candidate record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
