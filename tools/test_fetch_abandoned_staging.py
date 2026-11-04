import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def test_fetch_preserves_abandoned_staging_directory(tmp_path):
    source_id = "TEST-FETCH-STAGING-001"
    source = tmp_path / "working-source.txt"
    source.write_text("CURRENT SOURCE VERSION\n", encoding="utf-8")

    manifest_dir = tmp_path / "manifests"
    manifest_dir.mkdir()
    manifest = manifest_dir / "source.yml"
    manifest.write_text(
        json.dumps({
            "source_id": source_id,
            "repository_path": str(source),
        }),
        encoding="utf-8",
    )

    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir()
    abandoned = corpus_root / f".{source_id}.staging-abandoned"
    abandoned.mkdir()
    sentinel = abandoned / "recovery-note.txt"
    sentinel_bytes = b"Keep this abandoned staging material.\n"
    sentinel.write_bytes(sentinel_bytes)

    result = subprocess.run(
        [sys.executable, str(FETCHER), "--source", str(manifest)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, (
        "Fetch should succeed without deleting abandoned staging material:\n"
        + result.stdout + result.stderr
    )

    published = corpus_root / source_id
    assert (published / "original" / source.name).read_text(
        encoding="utf-8"
    ) == "CURRENT SOURCE VERSION\n"
    assert sentinel.read_bytes() == sentinel_bytes, (
        "The abandoned staging material was altered."
    )
    assert abandoned.is_dir(), (
        "The abandoned staging directory was deleted automatically."
    )
