import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def test_fetch_preserves_exact_source_bytes(tmp_path):
    source_id = "TEST-FETCH-BYTES-001"
    source = tmp_path / "source.txt"

    # Include CRLF line endings and UTF-8 characters to detect text rewriting.
    original_bytes = "First line\r\nCafé — Narragansett\r\n".encode("utf-8")
    source.write_bytes(original_bytes)

    manifest = tmp_path / "manifest.yml"
    manifest.write_text(
        yaml.safe_dump({
            "source_id": source_id,
            "repository_path": str(source),
        }),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(FETCHER), "--source", str(manifest)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, (
        "Initial fetch should succeed:\n" + result.stdout + result.stderr
    )

    preserved = (
        tmp_path / "corpus" / source_id / "original" / source.name
    )
    assert preserved.read_bytes() == original_bytes, (
        "Fetch changed the source bytes; preservation must be byte-for-byte."
    )

    print("PASS: fetch preserved exact source bytes")


if __name__ == "__main__":
    with __import__("tempfile").TemporaryDirectory() as temp:
        test_fetch_preserves_exact_source_bytes(Path(temp))
