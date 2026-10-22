#!/usr/bin/env python3
"""Isolated regression tests for verified legacy-version recovery."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools/synthesis_workflow/recover_legacy_versions.py"


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class RecoveryFixture:
    def __init__(self, expected_hash: str | None = None):
        self.temp = tempfile.TemporaryDirectory(prefix="legacy-recovery-test-")
        self.root = Path(self.temp.name)
        (self.root / "tools/synthesis_workflow").mkdir(parents=True)
        shutil.copy2(
            TOOL,
            self.root / "tools/synthesis_workflow/recover_legacy_versions.py",
        )

        self.source_path = "people/sample.md"
        self.content = (
            b"# Historical page\r\n\r\nExact bytes matter.\r\n"
        )
        source = self.root / self.source_path
        source.parent.mkdir(parents=True)
        source.write_bytes(self.content)

        for args in (
            ["init", "-q"],
            ["config", "user.name", "Recovery Test"],
            ["config", "user.email", "recovery-test@example.invalid"],
        ):
            result = run(["git", *args], self.root)
            check(result.returncode == 0, f"git {' '.join(args)} failed")

        result = run(["git", "add", self.source_path], self.root)
        check(result.returncode == 0, "git add failed")
        result = run(["git", "commit", "-qm", "Add historical page"], self.root)
        check(result.returncode == 0, "git commit failed")

        self.content_hash = hashlib.sha256(self.content).hexdigest()
        recorded_hash = expected_hash or self.content_hash
        self.observation_id = "OBS-PEOPLE-TEST001"
        record = {
            "observation_id": self.observation_id,
            "source_path": self.source_path,
            "content_sha256": recorded_hash,
            "byte_count": len(self.content),
            "legacy_preserved": True,
        }

        registry = self.root / "data/research/legacy_observations.jsonl"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps(record) + "\n", encoding="utf-8")

        self.destination = (
            self.root
            / "data/research/recovered_page_versions"
            / f"{self.observation_id}.md"
        )
        self.manifest = (
            self.root
            / "data/research/recovered_page_versions/manifest.jsonl"
        )

    def cli(self, *args: str) -> subprocess.CompletedProcess:
        return run(
            [
                sys.executable,
                "tools/synthesis_workflow/recover_legacy_versions.py",
                *args,
            ],
            self.root,
        )

    def close(self) -> None:
        self.temp.cleanup()


def test_exact_recovery_and_dry_run() -> None:
    fixture = RecoveryFixture()
    try:
        dry = fixture.cli()
        check(dry.returncode == 0, f"dry run failed: {dry.stdout}{dry.stderr}")
        check("WOULD_RECOVER" in dry.stdout, "dry run did not report candidate")
        check(not fixture.destination.exists(), "dry run wrote a page")
        check(not fixture.manifest.exists(), "dry run wrote a manifest")

        result = fixture.cli("--write")
        check(result.returncode == 0, f"recovery failed: {result.stdout}{result.stderr}")
        check(fixture.destination.read_bytes() == fixture.content,
              "recovered bytes differ from the historical source")
        check(fixture.manifest.exists(), "manifest was not created")
        entries = [
            json.loads(line)
            for line in fixture.manifest.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        check(len(entries) == 1, "expected one manifest entry")
        check(entries[0]["content_sha256"] == fixture.content_hash,
              "manifest hash does not match recovered content")
    finally:
        fixture.close()


def test_second_run_is_idempotent() -> None:
    fixture = RecoveryFixture()
    try:
        first = fixture.cli("--write")
        check(first.returncode == 0, f"first run failed: {first.stdout}{first.stderr}")
        original_bytes = fixture.destination.read_bytes()
        original_manifest = fixture.manifest.read_bytes()

        second = fixture.cli("--write")
        check(second.returncode == 0, f"second run failed: {second.stdout}{second.stderr}")
        check("ALREADY_PRESENT" in second.stdout,
              "second run did not recognize existing recovered page")
        check(fixture.destination.read_bytes() == original_bytes,
              "second run changed recovered page")
        check(fixture.manifest.read_bytes() == original_manifest,
              "second run duplicated or changed manifest history")
    finally:
        fixture.close()


def test_conflict_is_never_overwritten() -> None:
    fixture = RecoveryFixture()
    try:
        fixture.destination.parent.mkdir(parents=True)
        conflict = b"DO NOT OVERWRITE THIS FILE\n"
        fixture.destination.write_bytes(conflict)

        result = fixture.cli("--write")
        check(result.returncode != 0, "destination conflict was accepted")
        check("DESTINATION_CONFLICT" in result.stdout,
              "conflict was not clearly reported")
        check(fixture.destination.read_bytes() == conflict,
              "conflicting destination was overwritten")
        check(not fixture.manifest.exists(),
              "manifest was written for a conflicting destination")
    finally:
        fixture.close()


def test_hash_mismatch_prevents_recovery() -> None:
    fixture = RecoveryFixture(expected_hash="0" * 64)
    try:
        result = fixture.cli("--write")
        check(result.returncode != 0, "incorrect hash was accepted")
        check("NO_VERIFIED_GIT_VERSION" in result.stdout,
              "missing hash match was not reported")
        check(not fixture.destination.exists(),
              "a page was published despite hash mismatch")
        check(not fixture.manifest.exists(),
              "manifest was written despite hash mismatch")
    finally:
        fixture.close()



def test_manifest_conflict_prevents_all_publication() -> None:
    fixture = RecoveryFixture()
    try:
        fixture.manifest.parent.mkdir(parents=True)
        conflicting_entry = {
            "observation_id": fixture.observation_id,
            "source_path": fixture.source_path,
            "content_sha256": fixture.content_hash,
            "git_commit": "conflicting-commit-id",
            "recovered_path": "wrong/destination.md",
        }
        fixture.manifest.write_text(
            json.dumps(conflicting_entry) + "\n", encoding="utf-8"
        )
        original_manifest = fixture.manifest.read_bytes()

        result = fixture.cli("--write")
        check(result.returncode != 0, "manifest conflict was accepted")
        check("MANIFEST_CONFLICT" in result.stdout,
              "manifest conflict was not clearly reported")
        check(not fixture.destination.exists(),
              "page was published before manifest conflict was rejected")
        check(fixture.manifest.read_bytes() == original_manifest,
              "conflicting manifest history was modified")
    finally:
        fixture.close()


def main() -> int:
    tests = (
        test_exact_recovery_and_dry_run,
        test_second_run_is_idempotent,
        test_conflict_is_never_overwritten,
        test_hash_mismatch_prevents_recovery,
        test_manifest_conflict_prevents_all_publication,
    )
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as error:
            failures += 1
            print(f"FAIL {test.__name__}: {error}")

    print(f"\nRESULT: {len(tests) - failures}/{len(tests)} tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
