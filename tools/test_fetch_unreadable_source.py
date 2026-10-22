import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def test_unreadable_source_does_not_leave_false_intake():
    with tempfile.TemporaryDirectory(prefix="joan-unreadable-source-") as temp:
        root = Path(temp)
        source_id = "TEST-UNREADABLE-001"

        source = root / "source.txt"
        source.write_bytes(b"Exact source bytes; UTF-8 is not required.\n")

        manifest = root / "manifest.yml"
        manifest.write_text(
            yaml.safe_dump({
                "source_id": source_id,
                "repository_path": "source.txt",
            }),
            encoding="utf-8",
        )

        runner = root / "runner.py"
        runner.write_text(
            """
from pathlib import Path
import runpy
import sys

fetcher, manifest, source = sys.argv[1:4]
real_read_bytes = Path.read_bytes
target = Path(source).resolve()

def controlled_read_failure(path):
    if path.resolve() == target:
        raise PermissionError("synthetic read failure for regression test")
    return real_read_bytes(path)

Path.read_bytes = controlled_read_failure
sys.argv = [fetcher, "--source", manifest]
runpy.run_path(fetcher, run_name="__main__")
""",
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                str(runner),
                str(FETCHER),
                str(manifest),
                str(source),
            ],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        assert result.returncode != 0, "Read failure should be rejected."
        assert "SOURCE_READ_FAILED" in result.stderr, (
            f"Expected controlled read failure; stderr:\n{result.stderr}"
        )

        intake = root / "corpus" / source_id
        assert not intake.exists(), "Failed read published a false intake."
        assert not (root / "corpus").exists(), (
            "Failed read created a corpus staging directory."
        )

        print("PASS: source read failure leaves no false intake")


if __name__ == "__main__":
    test_unreadable_source_does_not_leave_false_intake()
    print("UNREADABLE SOURCE PRESERVATION TEST: PASS")
