#!/usr/bin/env python3
"""Regression tests for filesystem directory-entry durability."""

import importlib.util
import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "tools/synthesis_workflow/synthesize_legacy_pages.py"
)

spec = importlib.util.spec_from_file_location("synthesis_directory_sync_test", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load synthesis script: {SCRIPT}")

synthesis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synthesis)


def test_atomic_replace_syncs_parent_directory():
    with tempfile.TemporaryDirectory(prefix="synthesis-dir-sync-") as temp:
        root = Path(temp)
        target = root / "ledger.jsonl"
        target.write_bytes(b"old\n")
        real_fsync = os.fsync
        synced_directories = []

        def observe_fsync(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                synced_directories.append(Path(os.readlink(f"/proc/self/fd/{fd}")))
            return real_fsync(fd)

        with patch.object(synthesis.os, "fsync", side_effect=observe_fsync):
            synthesis._write_bytes_atomically(target, b"new\n")

        if target.read_bytes() != b"new\n":
            raise AssertionError("Atomic replacement did not publish intended bytes")
        if root not in synced_directories:
            raise AssertionError(
                "Atomic replacement did not fsync its parent directory"
            )


def main():
    test_atomic_replace_syncs_parent_directory()
    print("SYNTHESIS DIRECTORY SYNC TESTS: PASS")


if __name__ == "__main__":
    main()
