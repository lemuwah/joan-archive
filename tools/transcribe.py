import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.source)
    import yaml
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    source_id = manifest["source_id"]

    source_path = Path(manifest["repository_path"])
    text = source_path.read_text(encoding="utf-8")

    result = {
        "event": "TRANSCRIPTION_OBSERVATION",
        "source_id": manifest["source_id"],
        "method": "existing_archive_working_transcription",
        "status": "WORKING_LEAD_ONLY",
        "verified_by_human": False,
        "professional_paleography": False,
        "literal_text_preserved": True,
        "text": text,
        "warning": "This is an AI-assisted working record, not a verified verbatim transcription."
    }

    outdir = Path("corpus") / source_id
    (outdir / "transcription.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
