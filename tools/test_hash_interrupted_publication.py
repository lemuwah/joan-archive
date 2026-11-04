import importlib.util
import json
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
HASHER = REPO_ROOT / "tools" / "hash_source.py"


def test_interrupted_hash_write_never_publishes_partial_record(
    tmp_path, monkeypatch
):
    spec = importlib.util.spec_from_file_location("hash_source_under_test", HASHER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    source_id = "TEST-HASH-INTERRUPTED-001"
    corpus = tmp_path / "corpus" / source_id
    original_dir = corpus / "original"
    original_dir.mkdir(parents=True)

    preserved = original_dir / "working-source.txt"
    original_bytes = b"PRESERVED SOURCE BYTES\n"
    preserved.write_bytes(original_bytes)

    (corpus / "source.json").write_text(
        json.dumps({
            "source_id": source_id,
            "repository_path": str(tmp_path / "working-source.txt"),
        }),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["hash_source.py", "--source", source_id]
    )

    def interrupted_dump(data, handle, **kwargs):
        handle.write('{"partial":')
        raise OSError("simulated interruption during hash-record write")

    monkeypatch.setattr(module.json, "dump", interrupted_dump)

    with pytest.raises(OSError, match="simulated interruption"):
        module.main()

    assert not (corpus / "hash.json").exists(), (
        "Interrupted publication left a permanent partial hash record."
    )
    assert preserved.read_bytes() == original_bytes, (
        "The preserved source changed during hash publication."
    )
    assert not list(corpus.glob(".hash.json.staging-*")), (
        "Ordinary exception cleanup left a temporary hash staging file."
    )
