import argparse
import hashlib
import json
from pathlib import Path
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
    outdir = Path("corpus") / source_id
    outdir.mkdir(parents=True, exist_ok=True)

    if not repo_path.exists():
        raise SystemExit(f"SOURCE_MISSING: {repo_path}")

    source_text = repo_path.read_text(encoding="utf-8")

    (outdir / "original").mkdir(exist_ok=True)
    copied = outdir / "original" / repo_path.name
    copied.write_text(source_text, encoding="utf-8")

    access = {
        "event": "SOURCE_ACCESS",
        "source_id": source_id,
        "source_path": str(repo_path),
        "copied_to": str(copied),
        "access_status": "ACCESSIBLE",
        "content_type": "repository_textual_working_record",
        "note": "This pipeline does not claim direct access to the external manuscript image."
    }

    (outdir / "source.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )
    (outdir / "fetch-log.json").write_text(
        json.dumps(access, indent=2), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
