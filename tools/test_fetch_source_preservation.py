import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def run_fetch(root: Path, manifest: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(FETCHER), "--source", str(manifest)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def test_second_fetch_does_not_replace_preserved_material():
    with tempfile.TemporaryDirectory(prefix="joan-fetch-test-") as temp:
        root = Path(temp)

        source = root / "sample_record.txt"
        source.write_text("FIRST SOURCE VERSION\n", encoding="utf-8")

        manifest = root / "manifest.yml"
        manifest.write_text(
            yaml.safe_dump({
                "source_id": "TEST-SOURCE-001",
                "repository_path": "sample_record.txt",
            }),
            encoding="utf-8",
        )

        first = run_fetch(root, manifest)
        assert first.returncode == 0, (
            "Initial fetch should succeed:\n" + first.stdout + first.stderr
        )

        corpus = root / "corpus" / "TEST-SOURCE-001"
        preserved = corpus / "original" / "sample_record.txt"
        metadata = corpus / "source.json"
        fetch_log = corpus / "fetch-log.json"

        assert preserved.read_text(encoding="utf-8") == "FIRST SOURCE VERSION\n"
        original_metadata = metadata.read_bytes()
        original_log = fetch_log.read_bytes()

        # Simulate the repository file changing before a repeat fetch.
        source.write_text("SECOND SOURCE VERSION\n", encoding="utf-8")

        second = run_fetch(root, manifest)

        assert second.returncode != 0, (
            "A repeat fetch unexpectedly succeeded; it may have overwritten "
            "the existing preserved copy and provenance records."
        )
        assert preserved.read_text(encoding="utf-8") == "FIRST SOURCE VERSION\n"
        assert metadata.read_bytes() == original_metadata
        assert fetch_log.read_bytes() == original_log

        print("PASS: repeat fetch did not replace preserved material")


if __name__ == "__main__":
    test_second_fetch_does_not_replace_preserved_material()
    print("FETCH SOURCE PRESERVATION TEST: PASS")
