import importlib.util
import json
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
FETCHER = REPO_ROOT / "tools" / "fetch_source.py"

spec = importlib.util.spec_from_file_location("fetch_source", FETCHER)
fetch_source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch_source)


def test_interrupted_write_does_not_publish_partial_intake():
    with tempfile.TemporaryDirectory(prefix="joan-interrupted-fetch-") as temp:
        root = Path(temp)
        source_id = "TEST-INTERRUPTED-001"

        source = root / "sample.txt"
        source.write_text("A preserved test source.\n", encoding="utf-8")

        manifest = root / "manifest.yml"
        manifest.write_text(
            yaml.safe_dump({
                "source_id": source_id,
                "repository_path": "sample.txt",
            }),
            encoding="utf-8",
        )

        original_write_text = Path.write_text

        def fail_during_fetch_log(self, *args, **kwargs):
            if self.name == "fetch-log.json":
                raise OSError("Simulated interruption during metadata write")
            return original_write_text(self, *args, **kwargs)

        Path.write_text = fail_during_fetch_log
        original_cwd = Path.cwd()

        try:
            import os
            os.chdir(root)
            sys.argv = ["fetch_source.py", "--source", "manifest.yml"]

            try:
                fetch_source.main()
            except OSError as exc:
                assert "Simulated interruption" in str(exc)
            else:
                raise AssertionError(
                    "The simulated write failure did not occur."
                )
        finally:
            Path.write_text = original_write_text
            os.chdir(original_cwd)

        intake = root / "corpus" / source_id
        assert not intake.exists(), (
            "Interrupted fetch left a partial permanent intake."
        )

        print("PASS: interrupted write does not publish partial intake")


if __name__ == "__main__":
    test_interrupted_write_does_not_publish_partial_intake()
    print("INTERRUPTED WRITE PRESERVATION TEST: PASS")
