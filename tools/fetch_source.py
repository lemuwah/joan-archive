import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    manifest_path = (repo_root / args.source).resolve()

    try:
        manifest_path.relative_to(repo_root)
    except ValueError:
        raise SystemExit(f"SOURCE_MANIFEST_OUTSIDE_REPOSITORY: {args.source}")

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    source_id = manifest["source_id"]
    repo_path = (repo_root / manifest["repository_path"]).resolve()

    try:
        repo_path.relative_to(repo_root)
    except ValueError:
        raise SystemExit(
            f"SOURCE_PATH_OUTSIDE_REPOSITORY: {manifest['repository_path']}"
        )
    # Source IDs must name one directory, not escape the corpus.
    if not source_id or Path(source_id).name != source_id or source_id in {".", ".."}:
        raise SystemExit(f"INVALID_SOURCE_ID: {source_id!r}")

    outdir = Path("corpus") / source_id

    # Fail closed: never silently replace an existing source intake.
    if outdir.exists():
        raise SystemExit(
            f"SOURCE_ALREADY_PRESERVED: {outdir}. "
            "Review the existing record and create a separately identified "
            "intake if a new version must be preserved."
        )

    # Reject missing or unreadable source files before creating any intake.
    if not repo_path.is_file():
        raise SystemExit(f"SOURCE_MISSING: {repo_path}")

    try:
        source_bytes = repo_path.read_bytes()
    except OSError as exc:
        raise SystemExit(
            f"SOURCE_READ_FAILED: {repo_path}: {exc}"
        ) from exc

    # Build the entire intake privately, then publish it as one directory.
    corpus_root = outdir.parent
    corpus_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(
        prefix=f".{source_id}.staging-", dir=corpus_root
    ))

    copied = outdir / "original" / repo_path.name

    try:
        staged_original = staging / "original"
        staged_original.mkdir()
        (staged_original / repo_path.name).write_bytes(source_bytes)

        access = {
            "event": "SOURCE_ACCESS",
            "source_id": source_id,
            "source_path": str(repo_path),
            "copied_to": str(copied),
            "access_status": "ACCESSIBLE",
            "content_type": "repository_textual_working_record",
            "note": "This pipeline does not claim direct access to the external manuscript image."
        }

        (staging / "source.json").write_text(
            json.dumps(manifest, indent=2, default=str), encoding="utf-8"
        )
        (staging / "fetch-log.json").write_text(
            json.dumps(access, indent=2), encoding="utf-8"
        )

        # Check again immediately before publication.
        if outdir.exists():
            raise SystemExit(
                f"SOURCE_ALREADY_PRESERVED: {outdir}. "
                "Staged intake was not published."
            )

        try:
            os.rename(staging, outdir)
        except OSError as exc:
            # Another fetch may have published this source after our last check.
            if outdir.exists():
                raise SystemExit(
                    f"SOURCE_ALREADY_PRESERVED: {outdir}. "
                    "A competing fetch published the intake first; "
                    "this staged intake was not published."
                ) from exc
            raise

    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

if __name__ == "__main__":
    main()
