from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
AUDIT_TOOL = ROOT / "tools" / "audit_source_library.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_test() -> None:
    assert AUDIT_TOOL.exists(), "audit_source_library.py must exist"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        source_dir = tmp_path / "research" / "sources"
        source_dir.mkdir(parents=True)

        record = tmp_path / "research" / "record.md"
        record.write_text("working record\n", encoding="utf-8")

        manifest = source_dir / "example.yml"
        manifest.write_text(
            "\n".join(
                [
                    "source_id: EXAMPLE-001",
                    "repository_path: research/record.md",
                    "source_type: manuscript_image_with_working_transcription",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        subprocess.run(
            [
                sys.executable,
                str(AUDIT_TOOL),
                "--root",
                str(tmp_path),
            ],
            check=True,
        )

        output = (
            tmp_path
            / "research_control"
            / "source_library_integrity.json"
        )

        assert output.exists(), "integrity report was not created"

        baseline = json.loads(output.read_text(encoding="utf-8"))

        assert len(baseline["sources"]) == 1

        item = baseline["sources"][0]

        assert item["source_id"] == "EXAMPLE-001"
        assert item["manifest_path"] == "research/sources/example.yml"
        assert item["repository_path"] == "research/record.md"
        assert item["manifest_sha256"] == sha256(manifest)
        assert item["repository_sha256"] == sha256(record)

        baseline_snapshot = output.read_text(encoding="utf-8")

        subprocess.run(
            [
                sys.executable,
                str(AUDIT_TOOL),
                "--root",
                str(tmp_path),
                "--check",
            ],
            check=True,
        )

        assert (
            output.read_text(encoding="utf-8") == baseline_snapshot
        ), "successful integrity check must not rewrite snapshot"

        record.write_text(
            "working record\nTEMPORARY CHANGE\n",
            encoding="utf-8",
        )

        failed_check = subprocess.run(
            [
                sys.executable,
                str(AUDIT_TOOL),
                "--root",
                str(tmp_path),
                "--check",
            ],
            capture_output=True,
            text=True,
        )

        assert failed_check.returncode != 0, (
            "integrity check must fail when referenced source changes"
        )

        assert (
            "SOURCE_LIBRARY_AUDIT_FAIL: integrity snapshot mismatch"
            in failed_check.stdout
        ), "failure must identify an integrity snapshot mismatch"

        assert (
            output.read_text(encoding="utf-8") == baseline_snapshot
        ), "failed integrity check must not rewrite snapshot"

        record.write_text("working record\n", encoding="utf-8")

        subprocess.run(
            [
                sys.executable,
                str(AUDIT_TOOL),
                "--root",
                str(tmp_path),
                "--check",
            ],
            check=True,
        )

        assert (
            output.read_text(encoding="utf-8") == baseline_snapshot
        ), "restored integrity check must preserve snapshot"


if __name__ == "__main__":
    run_test()
    print("PASS: source library audit regression test")
