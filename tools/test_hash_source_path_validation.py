import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HASHER = REPO_ROOT / "tools" / "hash_source.py"


def run_hasher(root: Path, source_id: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HASHER), "--source", source_id],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def test_hash_rejects_path_traversal_source_id(tmp_path):
    # This record is outside corpus and must never be treated as a valid target.
    outside = tmp_path / "outside"
    original = outside / "original"
    original.mkdir(parents=True)
    (outside / "source.json").write_text(
        json.dumps({
            "source_id": "outside",
            "repository_path": "outside.txt",
        }),
        encoding="utf-8",
    )
    (original / "outside.txt").write_bytes(b"DO NOT HASH VIA TRAVERSAL\n")

    result = run_hasher(tmp_path, "../outside")

    assert result.returncode != 0, (
        "Hasher accepted a source ID that escapes the corpus directory."
    )
    assert not (outside / "hash.json").exists(), (
        "Traversal created an integrity record outside corpus."
    )


def test_hash_rejects_mismatched_metadata_source_id(tmp_path):
    requested_id = "TEST-HASH-REQUESTED-001"
    corpus = tmp_path / "corpus" / requested_id
    original = corpus / "original"
    original.mkdir(parents=True)

    (corpus / "source.json").write_text(
        json.dumps({
            "source_id": "TEST-HASH-DIFFERENT-999",
            "repository_path": "working-source.txt",
        }),
        encoding="utf-8",
    )
    (original / "working-source.txt").write_bytes(b"PRESERVED BYTES\n")

    result = run_hasher(tmp_path, requested_id)

    assert result.returncode != 0, (
        "Hasher accepted metadata whose source_id differs from the request."
    )
    assert not (corpus / "hash.json").exists(), (
        "Hasher published an integrity record for mismatched metadata."
    )


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
