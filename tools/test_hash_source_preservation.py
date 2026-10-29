import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HASHER = REPO_ROOT / "tools" / "hash_source.py"


def test_hash_describes_preserved_copy_and_does_not_overwrite():
    with tempfile.TemporaryDirectory(prefix="joan-hash-test-") as temp:
        root = Path(temp)
        source_id = "TEST-HASH-001"

        corpus = root / "corpus" / source_id
        original_dir = corpus / "original"
        original_dir.mkdir(parents=True)

        working_source = root / "working-source.txt"
        working_source.write_text("WORKING VERSION\n", encoding="utf-8")

        preserved = original_dir / "working-source.txt"
        preserved.write_text("PRESERVED VERSION\n", encoding="utf-8")

        metadata = {
            "source_id": source_id,
            "repository_path": str(working_source),
        }
        (corpus / "source.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )

        first = subprocess.run(
            [sys.executable, str(HASHER), "--source", source_id],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        assert first.returncode == 0, (
            "Initial hash should succeed:\n" + first.stdout + first.stderr
        )

        hash_path = corpus / "hash.json"
        result = json.loads(hash_path.read_text(encoding="utf-8"))
        expected = hashlib.sha256(preserved.read_bytes()).hexdigest()

        assert result["sha256"] == expected, (
            "Hash does not match the preserved copy."
        )
        assert result["path"] == str(preserved), (
            "Hash provenance should point to the preserved copy."
        )

        first_hash_record = hash_path.read_bytes()
        second = subprocess.run(
            [sys.executable, str(HASHER), "--source", source_id],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        assert second.returncode != 0, (
            "A repeat hash unexpectedly succeeded; the existing hash record "
            "may have been overwritten."
        )
        assert hash_path.read_bytes() == first_hash_record

        print("PASS: hash verifies preserved bytes and refuses overwrite")


if __name__ == "__main__":
    test_hash_describes_preserved_copy_and_does_not_overwrite()
    print("HASH SOURCE PRESERVATION TEST: PASS")
