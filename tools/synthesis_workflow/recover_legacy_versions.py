#!/usr/bin/env python3
"""Recover exact legacy Markdown versions from Git, verified by registry hashes.

Default behavior is a dry run. Use --write to publish recovered copies.
This tool never modifies source pages or synthesis registries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/research/legacy_observations.jsonl"
RECOVERY_ROOT = ROOT / "data/research/recovered_page_versions"
MANIFEST = RECOVERY_ROOT / "manifest.jsonl"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(*args: str, cwd: Path) -> bytes | None:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def safe_source_path(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        return None
    if path.as_posix() != value:
        return None
    return value


def find_matching_commit(
    source_path: str, expected_hash: str, root: Path
) -> tuple[str, bytes] | None:
    history = git_bytes(
        "rev-list", "--all", "--", source_path, cwd=root
    )
    if history is None:
        return None

    for commit in history.decode("ascii", errors="ignore").splitlines():
        content = git_bytes("show", f"{commit}:{source_path}", cwd=root)
        if content is not None and sha256(content) == expected_hash:
            return commit, content
    return None


def load_registry(path: Path) -> list[dict]:
    records = []
    seen = set()
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{path}:{line_number}: invalid JSON: {error.msg}"
            ) from error

        observation_id = record.get("observation_id")
        if not isinstance(observation_id, str) or not observation_id:
            raise ValueError(
                f"{path}:{line_number}: missing observation_id"
            )
        if observation_id in seen:
            raise ValueError(
                f"{path}:{line_number}: duplicate observation_id "
                f"{observation_id!r}"
            )
        seen.add(observation_id)
        records.append(record)
    return records


def load_manifest(path: Path) -> dict[str, dict]:
    entries = {}
    if not path.exists():
        return entries

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{path}:{line_number}: invalid JSON: {error.msg}"
            ) from error

        observation_id = entry.get("observation_id")
        if not isinstance(observation_id, str) or not observation_id:
            raise ValueError(
                f"{path}:{line_number}: missing observation_id"
            )
        if observation_id in entries:
            raise ValueError(
                f"{path}:{line_number}: duplicate manifest observation "
                f"{observation_id!r}"
            )
        entries[observation_id] = entry
    return entries


def publish_exclusive(path: Path, content: bytes) -> bool:
    """Create a new file without replacing an existing path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(
            path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644
        )
    except FileExistsError:
        existing = path.read_bytes()
        if sha256(existing) != sha256(content):
            raise FileExistsError(
                f"Destination exists with different content: {path}"
            )
        return False

    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        # Leave any partial file in place for investigation. Never silently
        # delete or replace it; a later run will fail closed on its hash.
        raise
    return True


def run(write: bool = False) -> int:
    records = load_registry(REGISTRY)
    manifest = load_manifest(MANIFEST) if MANIFEST.exists() else {}
    failures = 0
    recovered = 0
    already_present = 0
    prepared = []

    # Phase 1: preflight every record. Do not write anything in this phase.
    for record in sorted(
        records, key=lambda item: item.get("observation_id", "")
    ):
        observation_id = record["observation_id"]
        source_path = safe_source_path(record.get("source_path"))
        expected_hash = record.get("content_sha256")

        if (
            source_path is None
            or not isinstance(expected_hash, str)
            or len(expected_hash) != 64
            or any(ch not in "0123456789abcdef" for ch in expected_hash)
        ):
            print(f"INVALID_RECORD {observation_id}")
            failures += 1
            continue

        match = find_matching_commit(source_path, expected_hash, ROOT)
        if match is None:
            print(f"NO_VERIFIED_GIT_VERSION {observation_id} {source_path}")
            failures += 1
            continue

        commit, content = match
        if sha256(content) != expected_hash:
            print(f"HASH_MISMATCH {observation_id}")
            failures += 1
            continue

        destination = RECOVERY_ROOT / f"{observation_id}.md"
        expected_entry = {
            "observation_id": observation_id,
            "source_path": source_path,
            "content_sha256": expected_hash,
            "git_commit": commit,
            "recovered_path": destination.relative_to(ROOT).as_posix(),
        }

        prior_entry = manifest.get(observation_id)
        if prior_entry is not None and prior_entry != expected_entry:
            print(f"MANIFEST_CONFLICT {observation_id}")
            failures += 1
            continue

        exists = destination.exists()
        if exists and sha256(destination.read_bytes()) != expected_hash:
            print(f"DESTINATION_CONFLICT {destination}")
            failures += 1
            continue

        prepared.append(
            (observation_id, destination, content, expected_entry, exists,
             prior_entry is not None)
        )

    # Fail closed: even one preflight problem prevents all publication.
    if failures:
        print(
            f"\nPREFLIGHT FAILED: {failures} problem(s); "
            "no files were published."
        )
        return 1

    # Dry run ends after verification; it never creates directories or files.
    for observation_id, destination, _content, _entry, exists, _logged in prepared:
        if exists:
            print(f"ALREADY_PRESENT {observation_id} {destination}")
            already_present += 1
        else:
            print(f"WOULD_RECOVER {observation_id} {destination}")

    if not write:
        print(
            f"\nDRY RUN SUMMARY: records={len(records)} "
            f"already_present={already_present} failures=0"
        )
        print("Dry run: no files were written.")
        return 0

    # Phase 2a: publish verified page bytes without overwriting files.
    try:
        for observation_id, destination, content, _entry, exists, _logged in prepared:
            if exists:
                continue
            created = publish_exclusive(destination, content)
            if created:
                print(f"RECOVERED {observation_id} {destination}")
                recovered += 1
            else:
                print(f"ALREADY_PRESENT {observation_id} {destination}")
                already_present += 1
    except OSError as error:
        print(
            f"PUBLICATION INTERRUPTED: {error}. "
            "No manifest entries were appended in this phase."
        )
        return 1

    # Phase 2b: append manifest entries only after all page files verify.
    try:
        for observation_id, destination, _content, entry, _exists, logged in prepared:
            if logged:
                continue
            if sha256(destination.read_bytes()) != entry["content_sha256"]:
                raise OSError(f"Post-publication hash mismatch: {destination}")
            MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            line = json.dumps(entry, sort_keys=True) + "\n"
            descriptor = os.open(
                MANIFEST, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644
            )
            try:
                with os.fdopen(descriptor, "a", encoding="utf-8") as stream:
                    stream.write(line)
                    stream.flush()
                    os.fsync(stream.fileno())
            except Exception:
                raise
            manifest[observation_id] = entry
    except OSError as error:
        print(
            f"MANIFEST APPEND INTERRUPTED: {error}. "
            "Recovered page files are preserved; inspect before retrying."
        )
        return 1

    print(
        f"\nWRITE SUMMARY: records={len(records)} "
        f"recovered={recovered} already_present={already_present} failures=0"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Publish verified historical copies; default is dry run.",
    )
    args = parser.parse_args()
    try:
        return run(write=args.write)
    except (OSError, ValueError) as error:
        print(f"RECOVERY ABORTED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
