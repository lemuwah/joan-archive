import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def test_successful_fetch_publishes_complete_intake():
    with tempfile.TemporaryDirectory(prefix="joan-fetch-success-") as temp:
        root = Path(temp)
        source_id = "TEST-COMPLETE-001"

        source = root / "sample.txt"
        source.write_text("Verified test source.\n", encoding="utf-8")

        manifest = root / "manifest.yml"
        manifest.write_text(
            yaml.safe_dump({
                "source_id": source_id,
                "repository_path": "sample.txt",
            }),
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(FETCHER), "--source", "manifest.yml"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        assert result.returncode == 0, (
            "Successful fetch failed:\n" + result.stdout + result.stderr
        )

        intake = root / "corpus" / source_id
        preserved = intake / "original" / "sample.txt"
        source_metadata = intake / "source.json"
        fetch_log = intake / "fetch-log.json"

        assert intake.is_dir(), "Permanent intake directory is missing."
        assert preserved.is_file(), "Preserved source copy is missing."
        assert source_metadata.is_file(), "Source metadata is missing."
        assert fetch_log.is_file(), "Fetch log is missing."
        assert preserved.read_text(encoding="utf-8") == "Verified test source.\n"

        metadata = json.loads(source_metadata.read_text(encoding="utf-8"))
        log = json.loads(fetch_log.read_text(encoding="utf-8"))

        assert metadata["source_id"] == source_id
        assert log["source_id"] == source_id
        assert log["access_status"] == "ACCESSIBLE"
        assert (root / log["copied_to"]).resolve() == preserved.resolve()

        staging_dirs = list((root / "corpus").glob(f".{source_id}.staging-*"))
        assert not staging_dirs, "Staging directory remains after success."

        print("PASS: successful fetch publishes complete, consistent intake")


if __name__ == "__main__":
    test_successful_fetch_publishes_complete_intake()
    print("SUCCESSFUL PUBLICATION TEST: PASS")
