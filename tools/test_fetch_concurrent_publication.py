import os
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"


def test_concurrent_fetches_publish_once_and_fail_cleanly():
    with tempfile.TemporaryDirectory(prefix="joan-fetch-race-") as temp:
        root = Path(temp)
        barrier = root / "barrier"
        barrier.mkdir()

        runner = root / "synchronized_runner.py"
        runner.write_text(
            """
import os
from pathlib import Path
import runpy
import sys
import time

fetcher, manifest = sys.argv[1], sys.argv[2]
barrier = Path(os.environ["RACE_BARRIER_DIR"])
real_rename = os.rename

def synchronized_rename(source, destination):
    marker = barrier / f"ready-{os.getpid()}"
    marker.touch()
    deadline = time.monotonic() + 15

    while len(list(barrier.glob("ready-*"))) < 2:
        if time.monotonic() >= deadline:
            raise RuntimeError("Timed out waiting for competing fetch.")
        time.sleep(0.01)

    return real_rename(source, destination)

os.rename = synchronized_rename
sys.argv = [fetcher, "--source", manifest]
runpy.run_path(fetcher, run_name="__main__")
""",
            encoding="utf-8",
        )

        source_names = ("first.txt", "second.txt")
        contents = ("First competing source.\\n", "Second competing source.\\n")
        manifests = ("manifest-first.yml", "manifest-second.yml")

        for source_name, content, manifest_name in zip(
            source_names, contents, manifests
        ):
            (root / source_name).write_text(content, encoding="utf-8")
            (root / manifest_name).write_text(
                yaml.safe_dump({
                    "source_id": "TEST-RACE-001",
                    "repository_path": source_name,
                }),
                encoding="utf-8",
            )

        env = os.environ.copy()
        env["RACE_BARRIER_DIR"] = str(barrier)

        processes = [
            subprocess.Popen(
                [sys.executable, str(runner), str(FETCHER), manifest],
                cwd=root,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for manifest in manifests
        ]

        results = []
        try:
            for process in processes:
                stdout, stderr = process.communicate(timeout=25)
                results.append((process.returncode, stdout, stderr))
        except subprocess.TimeoutExpired:
            for process in processes:
                process.kill()
            raise AssertionError("Concurrent fetch test timed out.")

        successes = [result for result in results if result[0] == 0]
        failures = [result for result in results if result[0] != 0]

        assert len(successes) == 1, (
            f"Expected exactly one successful publisher; results: {results}"
        )
        assert len(failures) == 1, (
            f"Expected the competing publisher to stop; results: {results}"
        )

        loser_stderr = failures[0][2]
        assert "SOURCE_ALREADY_PRESERVED" in loser_stderr, (
            "The losing fetch should stop with a clear preservation message, "
            f"not an uncontrolled error. stderr:\\n{loser_stderr}"
        )

        intake = root / "corpus" / "TEST-RACE-001"
        preserved = intake / "original"
        assert intake.is_dir()
        assert (intake / "source.json").is_file()
        assert (intake / "fetch-log.json").is_file()

        published_files = list(preserved.iterdir())
        assert len(published_files) == 1
        assert published_files[0].read_text(encoding="utf-8") in contents

        staging = list((root / "corpus").glob(".TEST-RACE-001.staging-*"))
        assert not staging, f"Leftover staging directories: {staging}"

        print("PASS: concurrent publication preserves exactly one complete intake")


if __name__ == "__main__":
    test_concurrent_fetches_publish_once_and_fail_cleanly()
    print("CONCURRENT PUBLICATION TEST: PASS")
