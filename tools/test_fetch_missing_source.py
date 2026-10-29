import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def test_missing_source_does_not_leave_a_false_preserved_intake():
    with tempfile.TemporaryDirectory(prefix="joan-missing-source-") as temp:
        root = Path(temp)
        source_id = "TEST-MISSING-001"

        manifest = root / "manifest.yml"
        manifest.write_text(
            yaml.safe_dump({
                "source_id": source_id,
                "repository_path": "does-not-exist.txt",
            }),
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(FETCHER), "--source", str(manifest)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        assert result.returncode != 0, "Missing source should be rejected."

        intake = root / "corpus" / source_id
        assert not intake.exists(), (
            "Failed intake left a directory that blocks a clean retry."
        )

        print("PASS: missing source leaves no false preserved intake")


if __name__ == "__main__":
    test_missing_source_does_not_leave_a_false_preserved_intake()
    print("MISSING SOURCE PRESERVATION TEST: PASS")
