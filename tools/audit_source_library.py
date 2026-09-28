#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve())
    except ValueError:
        raise SystemExit(
            f"SOURCE_LIBRARY_AUDIT_BLOCKED: path outside repository: {path}"
        )


def audit(root: Path) -> dict:
    source_dir = root / "research" / "sources"

    if not source_dir.is_dir():
        raise SystemExit(
            f"SOURCE_LIBRARY_AUDIT_BLOCKED: source library missing: {source_dir}"
        )

    sources = []

    for manifest_path in sorted(source_dir.glob("*.yml")):
        manifest = yaml.safe_load(
            manifest_path.read_text(encoding="utf-8")
        )

        if not isinstance(manifest, dict):
            raise SystemExit(
                f"SOURCE_LIBRARY_AUDIT_BLOCKED: invalid manifest: {manifest_path}"
            )

        source_id = manifest.get("source_id")
        repository_path = manifest.get("repository_path")

        if not source_id:
            raise SystemExit(
                f"SOURCE_LIBRARY_AUDIT_BLOCKED: source_id missing: {manifest_path}"
            )

        if not repository_path:
            raise SystemExit(
                f"SOURCE_LIBRARY_AUDIT_BLOCKED: repository_path missing: {manifest_path}"
            )

        manifest_relative = inside(root, manifest_path)
        repository_absolute = (root / repository_path).resolve()
        repository_relative = inside(root, repository_absolute)

        if not repository_absolute.exists():
            raise SystemExit(
                f"SOURCE_LIBRARY_AUDIT_BLOCKED: referenced source missing: "
                f"{repository_relative}"
            )

        sources.append(
            {
                "source_id": source_id,
                "manifest_path": manifest_relative.as_posix(),
                "manifest_sha256": sha256(manifest_path),
                "repository_path": repository_relative.as_posix(),
                "repository_sha256": sha256(repository_absolute),
            }
        )

    return {
        "event": "SOURCE_LIBRARY_INTEGRITY",
        "algorithm": "SHA-256",
        "source_count": len(sources),
        "sources": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the current source library against the existing integrity snapshot",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = audit(root)

    output = root / "research_control" / "source_library_integrity.json"

    if args.check:
        if not output.exists():
            print(f"SOURCE_LIBRARY_AUDIT_FAIL: integrity snapshot missing: {output}")
            return 1

        expected = json.loads(output.read_text(encoding="utf-8"))

        if report != expected:
            print("SOURCE_LIBRARY_AUDIT_FAIL: integrity snapshot mismatch")
            print(f"Integrity report: {output}")
            return 1

        print(f"Source library integrity check passed: {report['source_count']}")
        print(f"Integrity snapshot: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Source library audited: {report['source_count']}")
    print(f"Integrity report: {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
