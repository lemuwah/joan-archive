#!/usr/bin/env python3
"""Snapshot legacy people pages and create review-only synthesis proposals.

This tool preserves page history by content hash. It never edits source pages,
promotes claims, or writes to public-facing files.
"""

from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "people"
OBSERVATIONS = ROOT / "data/research/legacy_observations.jsonl"
PROPOSALS = ROOT / "data/research/synthesis_proposals.jsonl"

def synthesis_lock_path() -> Path:
    """Return the process-lock path for synthesis and recovery operations."""
    return ROOT / "data/research/synthesis_pair.lock"


@contextmanager
def synthesis_process_lock():
    """Serialize cooperating synthesis operations on Linux."""
    path = synthesis_lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def transaction_journal_path() -> Path:
    """Resolve the journal relative to the active repository root."""
    return ROOT / "data/research/synthesis_pair_transaction.json"
STATUS_TAGS = ("PROOF", "PLAUSIBLE", "DISCREDITED", "SUSPENDED", "UNVERIFIED", "UNKNOWN")


def load_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    records = {}
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {error.msg}") from error
        key = record.get("observation_id") or record.get("proposal_id")
        if not key:
            raise ValueError(f"{path}:{line_number}: missing record ID")
        if key in records:
            raise ValueError(
                f"{path}:{line_number}: duplicate record ID {key!r}"
            )
        records[key] = record
    return records


def write_jsonl(path: Path, records: dict[str, dict]) -> None:
    """Publish one complete JSONL ledger without exposing a partial write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(
        json.dumps(records[item], ensure_ascii=True, sort_keys=True) + "\n"
        for item in sorted(records)
    )

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass



def _fsync_directory(directory: Path) -> None:
    """Persist directory-entry changes after filesystem mutations."""
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    fd = os.open(directory, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _file_snapshot(path: Path, intended_bytes: bytes) -> dict:
    """Capture exact original state and intended bytes for transaction recovery."""
    existed = path.exists()
    original = path.read_bytes() if existed else b""
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "original_existed": existed,
        "originals": base64.b64encode(original).decode("ascii"),
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "intended": base64.b64encode(intended_bytes).decode("ascii"),
        "intended_sha256": hashlib.sha256(intended_bytes).hexdigest(),
    }


def _write_bytes_atomically(path: Path, content: bytes) -> None:
    """Durably stage bytes and atomically replace one file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _write_transaction_journal(observations_bytes: bytes, proposals_bytes: bytes) -> None:
    """Record both ledger states before either ledger can be replaced."""
    if transaction_journal_path().exists():
        raise RuntimeError(
            f"Unresolved synthesis transaction at {transaction_journal_path()}; "
            "recover it before another build or check"
        )

    journal = {
        "version": 1,
        "status": "RECOVERY_REQUIRED",
        "originals": {
            OBSERVATIONS.name: base64.b64encode(
                OBSERVATIONS.read_bytes() if OBSERVATIONS.exists() else b""
            ).decode("ascii"),
            PROPOSALS.name: base64.b64encode(
                PROPOSALS.read_bytes() if PROPOSALS.exists() else b""
            ).decode("ascii"),
        },
        "files": [
            _file_snapshot(OBSERVATIONS, observations_bytes),
            _file_snapshot(PROPOSALS, proposals_bytes),
        ],
    }
    content = (json.dumps(journal, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode("utf-8")
    _write_bytes_atomically(transaction_journal_path(), content)



def _publish_ledger_pair(observations_bytes: bytes, proposals_bytes: bytes) -> None:
    """Publish both ledgers with durable evidence retained on any failure."""
    _write_transaction_journal(observations_bytes, proposals_bytes)
    _write_bytes_atomically(OBSERVATIONS, observations_bytes)
    _write_bytes_atomically(PROPOSALS, proposals_bytes)
    # The journal is evidence until both replacements have completed.
    transaction_journal_path().unlink()
    _fsync_directory(transaction_journal_path().parent)




def _recover_transaction_unlocked() -> int:
    """Verify transaction evidence, then finalize or safely roll back."""
    journal_path = transaction_journal_path()
    if not journal_path.exists():
        print("No unresolved synthesis transaction.")
        return 0

    try:
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Cannot read transaction journal; preserved at {journal_path}"
        ) from exc

    if (
        not isinstance(journal, dict)
        or journal.get("version") != 1
        or journal.get("status") != "RECOVERY_REQUIRED"
    ):
        raise RuntimeError(
            f"Unsupported or invalid transaction journal; preserved at {journal_path}"
        )

    entries = journal.get("files")
    expected_paths = {
        OBSERVATIONS.relative_to(ROOT).as_posix(): OBSERVATIONS,
        PROPOSALS.relative_to(ROOT).as_posix(): PROPOSALS,
    }
    if not isinstance(entries, list) or len(entries) != 2:
        raise RuntimeError(
            f"Journal must describe exactly two ledgers; preserved at {journal_path}"
        )

    by_path = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise RuntimeError(f"Invalid journal entry; preserved at {journal_path}")
        relative = entry.get("path")
        if relative not in expected_paths or relative in by_path:
            raise RuntimeError(
                f"Unexpected or duplicate journal path {relative!r}; "
                f"preserved at {journal_path}"
            )
        by_path[relative] = entry

    if set(by_path) != set(expected_paths):
        raise RuntimeError(
            f"Journal does not name both expected ledgers; preserved at {journal_path}"
        )

    top_originals = journal.get("originals")
    if not isinstance(top_originals, dict):
        raise RuntimeError(
            f"Journal original-state map is missing; preserved at {journal_path}"
        )

    states = []
    for relative, path in expected_paths.items():
        entry = by_path[relative]
        try:
            original = base64.b64decode(entry["originals"], validate=True)
            intended = base64.b64decode(entry["intended"], validate=True)
        except (KeyError, ValueError, TypeError) as exc:
            raise RuntimeError(
                f"Invalid encoded bytes for {relative}; journal preserved"
            ) from exc

        if (
            hashlib.sha256(original).hexdigest() != entry.get("original_sha256")
            or hashlib.sha256(intended).hexdigest() != entry.get("intended_sha256")
        ):
            raise RuntimeError(
                f"Hash mismatch for {relative}; journal preserved at {journal_path}"
            )

        original_existed = entry.get("original_existed")
        if not isinstance(original_existed, bool):
            raise RuntimeError(
                f"Invalid original-existence flag for {relative}; journal preserved"
            )

        try:
            top_original = base64.b64decode(top_originals[path.name], validate=True)
        except (KeyError, ValueError, TypeError) as exc:
            raise RuntimeError(
                f"Invalid top-level original bytes for {path.name}; journal preserved"
            ) from exc

        if top_original != original:
            raise RuntimeError(
                f"Conflicting original snapshots for {path.name}; journal preserved"
            )

        current_exists = path.exists()
        current = path.read_bytes() if current_exists else b""
        is_original = (
            current_exists == original_existed
            and (not current_exists or current == original)
        )
        is_intended = current_exists and current == intended

        if not is_original and not is_intended:
            raise RuntimeError(
                f"Unexpected current bytes for {relative}; refusing to overwrite; "
                f"journal preserved at {journal_path}"
            )

        states.append((path, original, original_existed, is_intended))

    # If both replacements completed, retain the published pair and clear
    # the journal. Otherwise restore both recorded original states.
    if all(state[3] for state in states):
        journal_path.unlink()
        _fsync_directory(journal_path.parent)
        print("Both ledgers match the intended transaction; cleared recovery journal.")
        return 0

    for path, original, originally_existed, _ in states:
        if originally_existed:
            _write_bytes_atomically(path, original)
        elif path.exists():
            path.unlink()

    # Verify every original state before removing the recovery evidence.
    for path, original, originally_existed, _ in states:
        exists_now = path.exists()
        bytes_now = path.read_bytes() if exists_now else b""
        if exists_now != originally_existed or (
            exists_now and bytes_now != original
        ):
            raise RuntimeError(
                f"Rollback verification failed for {path}; "
                f"journal preserved at {journal_path}"
            )

    journal_path.unlink()
    _fsync_directory(journal_path.parent)
    print("Both ledgers restored to their recorded original states.")
    print("Recovery journal cleared after verification.")
    return 0


def page_record(path: Path) -> tuple[dict, dict]:
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_text()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    observation_id = f"OBS-PEOPLE-{hashlib.sha256(f'{relative}:{digest}'.encode()).hexdigest()[:12]}"
    headings = re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    linked_paths = sorted(set(re.findall(r"\(([^()\s]+\.md)(?:#[^)]+)?\)", text)))
    status_tags = sorted({tag for tag in STATUS_TAGS if re.search(rf"\b{tag}\b", text, re.IGNORECASE)})
    title = next((heading.lstrip("# ").strip() for heading in text.splitlines() if heading.startswith("#")), path.stem)
    observation = {
        "observation_id": observation_id,
        "observation_type": "LEGACY_PAGE_SNAPSHOT",
        "source_path": relative,
        "title": title,
        "content_sha256": digest,
        "byte_count": len(text.encode("utf-8")),
        "headings": headings,
        "linked_paths": linked_paths,
        "status_tags": status_tags,
        "legacy_preserved": True,
    }
    proposal_id = f"SYNTH-PEOPLE-{hashlib.sha256(observation_id.encode()).hexdigest()[:12]}"
    proposal = {
        "proposal_id": proposal_id,
        "status": "PENDING_HUMAN_REVIEW",
        "proposal_type": "LEGACY_PAGE_RECONCILIATION",
        "observation_ids": [observation_id],
        "source_path": relative,
        "subject": title,
        "proposed_action": "RETAIN_AS_LEGACY_NOTE",
        "summary": "Keep the page as historical project context; review its statements against source-linked claims before any public promotion.",
        "indicators": {
            "heading_count": len(headings),
            "linked_markdown_count": len(linked_paths),
            "status_tags": status_tags,
        },
        "promotion_allowed": False,
        "human_disposition": None,
    }
    return observation, proposal


def build_unlocked(check: bool) -> int:
    if transaction_journal_path().exists():
        raise RuntimeError(
            f"Unresolved synthesis transaction at {transaction_journal_path()}; "
            "run with --recover before another build or check"
        )

    observations = load_jsonl(OBSERVATIONS)
    proposals = load_jsonl(PROPOSALS)
    current_observation_ids = set()
    current_proposal_ids = set()
    pages = sorted(PEOPLE_DIR.glob("*.md"))
    for page in pages:
        observation, proposal = page_record(page)
        observations[observation["observation_id"]] = observation

        # Preserve an existing proposal and any recorded disposition.
        # A repeated synthesis run must not reset prior review history.
        if proposal["proposal_id"] not in proposals:
            proposals[proposal["proposal_id"]] = proposal

        current_observation_ids.add(observation["observation_id"])
        current_proposal_ids.add(proposal["proposal_id"])

    before_observations = OBSERVATIONS.read_text() if OBSERVATIONS.exists() else ""
    before_proposals = PROPOSALS.read_text() if PROPOSALS.exists() else ""
    new_observations = "".join(json.dumps(observations[item], ensure_ascii=True, sort_keys=True) + "\n" for item in sorted(observations))
    new_proposals = "".join(json.dumps(proposals[item], ensure_ascii=True, sort_keys=True) + "\n" for item in sorted(proposals))
    if check:
        stale = []
        if before_observations != new_observations:
            stale.append(str(OBSERVATIONS.relative_to(ROOT)))
        if before_proposals != new_proposals:
            stale.append(str(PROPOSALS.relative_to(ROOT)))
        if stale:
            print("Generated outputs are stale; run the synthesis tool:", *stale, sep="\n- ", file=sys.stderr)
            return 1
    else:
        _publish_ledger_pair(
            new_observations.encode("utf-8"),
            new_proposals.encode("utf-8"),
        )
    print(f"People pages scanned: {len(pages)}")
    print(f"Current snapshots: {len(current_observation_ids)}; historical snapshots retained: {len(observations)}")
    print(f"Current proposals: {len(current_proposal_ids)}; historical proposals retained: {len(proposals)}")
    return 0


def _recover_transaction() -> int:
    """Recover an interrupted publication while holding the process lock."""
    with synthesis_process_lock():
        return _recover_transaction_unlocked()


def build(check: bool) -> int:
    """Build or check synthesis outputs while holding the process lock."""
    with synthesis_process_lock():
        return build_unlocked(check)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check generated files without writing them")
    mode.add_argument("--recover", action="store_true", help="Recover an interrupted paired-ledger publication")
    args = parser.parse_args()
    if args.recover:
        return _recover_transaction()
    return build(args.check)


if __name__ == "__main__":
    raise SystemExit(main())