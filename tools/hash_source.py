import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    # Validate the requested ID before constructing or accessing its path.
    source_id_arg = args.source
    if (
        not source_id_arg
        or source_id_arg in {".", ".."}
        or Path(source_id_arg).name != source_id_arg
        or "/" in source_id_arg
        or "\\" in source_id_arg
    ):
        raise SystemExit(f"HASH_BLOCKED: invalid source ID: {source_id_arg!r}")

    corpus_root = Path("corpus").resolve()
    source_dir = (corpus_root / source_id_arg).resolve()
    try:
        source_dir.relative_to(corpus_root)
    except ValueError:
        raise SystemExit(
            f"HASH_BLOCKED: source path escapes corpus: {source_id_arg!r}"
        )

    source_json = source_dir / "source.json"

    if not source_json.exists():
        raise SystemExit(
            f"HASH_BLOCKED: source metadata not found: {source_json}"
        )

    data = json.loads(source_json.read_text(encoding="utf-8"))
    source_id = data.get("source_id")
    if source_id != source_id_arg:
        raise SystemExit(
            "HASH_BLOCKED: source metadata ID does not match requested ID: "
            f"requested={source_id_arg!r}, metadata={source_id!r}"
        )

    # Hash the preserved copy, not a working file that may later change.
    source_name = Path(data["repository_path"]).name
    preserved_path = (source_json.parent / "original" / source_name).resolve()

    if not preserved_path.is_file():
        raise SystemExit(
            f"HASH_BLOCKED: preserved source missing: {preserved_path}"
        )

    hash_path = source_json.parent / "hash.json"
    if hash_path.exists():
        raise SystemExit(
            f"HASH_ALREADY_PRESERVED: {hash_path}. "
            "Do not overwrite an existing integrity record."
        )

    digest = hashlib.sha256(preserved_path.read_bytes()).hexdigest()

    out = {
        "event": "SOURCE_INTEGRITY",
        "source_id": source_id,
        "algorithm": "SHA-256",
        "sha256": digest,
        "path": str(preserved_path)
    }

    # Stage a complete integrity record before publishing it.
    # The staging file shares the destination filesystem.
    staging_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=hash_path.parent,
            prefix=".hash.json.staging-",
            delete=False,
        ) as handle:
            staging_path = Path(handle.name)
            json.dump(out, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        # Exclusive publication: never replace an existing integrity record.
        try:
            os.link(staging_path, hash_path)
        except FileExistsError:
            raise SystemExit(
                f"HASH_ALREADY_PRESERVED: {hash_path}. "
                "Do not overwrite an existing integrity record."
            ) from None
    finally:
        # Clean up after ordinary success or failure. A hard process kill
        # may leave a hidden staging file, never a partial permanent hash.
        if staging_path is not None:
            staging_path.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
