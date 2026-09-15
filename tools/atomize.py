import argparse
import json
import re
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    source_id = Path(args.source).stem
    corpus = Path("corpus") / source_id

    transcription_path = corpus / "transcription.json"
    if not transcription_path.exists():
        raise SystemExit(
            f"ATOMIZE_BLOCKED: required upstream artifact missing: {transcription_path}"
        )

    transcription = json.loads(
        transcription_path.read_text(encoding="utf-8")
    )

    text = transcription["text"]

    observations = []
    inferences = []
    hypotheses = []
    tests = []

    # Explicitly harvest the archive's own labeled sections.
    sections = re.split(r"\n(?=## |\*\*Assessment|\*\*Research queue)", text)

    for section in sections:
        lower = section.lower()

        if "assessment" in lower:
            inferences.append({
                "type": "INFERENCE",
                "text": section.strip(),
                "status": "UNVERIFIED"
            })

        elif "research queue" in lower:
            for line in section.splitlines():
                if line.strip().startswith("- ["):
                    tests.append({
                        "type": "TEST",
                        "text": line.strip(),
                        "status": "OPEN"
                    })

        elif section.strip():
            observations.append({
                "type": "OBSERVATION",
                "text": section.strip(),
                "status": "WORKING_SOURCE_RECORD"
            })

    # Known hypothesis language is preserved as hypothesis, never promoted.
    for phrase in [
        "same transaction",
        "companion transaction",
        "different John",
        "Anashuecot",
        "new source"
    ]:
        if phrase.lower() in text.lower():
            hypotheses.append({
                "type": "HYPOTHESIS",
                "trigger": phrase,
                "status": "TEST_REQUIRED"
            })

    result = {
        "event": "ATOMIZATION",
        "source_id": source_id,
        "observation_count": len(observations),
        "inference_count": len(inferences),
        "hypothesis_count": len(hypotheses),
        "test_count": len(tests),
        "observations": observations,
        "inferences": inferences,
        "hypotheses": hypotheses,
        "tests": tests,
        "rule": "Atomization separates layers; it does not decide historical truth."
    }

    (corpus / "atoms.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
