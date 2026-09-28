import argparse
import hashlib
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    source_json = Path("corpus") / args.source / "source.json"

    if not source_json.exists():
        raise SystemExit(
            f"HASH_BLOCKED: source metadata not found: {source_json}"
        )

    data = json.loads(source_json.read_text(encoding="utf-8"))
    source_id = data["source_id"]
    source_path = Path(data["repository_path"])

    if not source_path.exists():
        raise SystemExit(f"HASH_BLOCKED: source missing: {source_path}")

    digest = hashlib.sha256(
        source_path.read_bytes()
    ).hexdigest()

    out = {
        "event": "SOURCE_INTEGRITY",
        "source_id": source_id,
        "algorithm": "SHA-256",
        "sha256": digest,
        "path": str(source_path)
    }

    (source_json.parent / "hash.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
