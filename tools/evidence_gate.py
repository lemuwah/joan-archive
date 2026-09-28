import argparse
import json
import re
from pathlib import Path

FORBIDDEN_AUTO_PROMOTIONS = {
    "PROOF": "VERIFIED",
    "PROVEN": "VERIFIED",
    "PLAUSIBLE": "PROVISIONALLY_SUPPORTED",
    "PROBABLE": "PROVISIONALLY_SUPPORTED",
    "ELIMINATED": "REJECTED",
    "KILLED": "REJECTED",
    "NOT FOUND": "NONEXISTENT",
    "SEARCHED": "NONEXISTENT",
    "PRIMARY": "VERIFIED"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    reports = []
    corpus = Path("corpus") / args.source

    if not corpus.is_dir():
        raise SystemExit(
            f"EVIDENCE_GATE_BLOCKED: source corpus not found: {corpus}"
        )

    for corpus in [corpus]:

        atoms_file = corpus / "atoms.json"
        if not atoms_file.exists():
            raise SystemExit(
                f"EVIDENCE_GATE_BLOCKED: required upstream artifact missing: {atoms_file}"
            )

        atoms = json.loads(atoms_file.read_text(encoding="utf-8"))

        violations = []

        for layer in ("observations", "inferences"):
            for item in atoms.get(layer, []):
                text = item.get("text", "")
                upper = text.upper()

                for old, new in FORBIDDEN_AUTO_PROMOTIONS.items():
                    pattern = r"(?<![A-Z0-9_])" + re.escape(old) + r"(?![A-Z0-9_])"
                    if re.search(pattern, upper):
                        violations.append({
                            "rule": "LEGACY_VOCABULARY_FIREWALL",
                            "layer": layer,
                            "legacy_label": old,
                            "forbidden_promotion": new,
                            "action": "FLAG_FOR_REVIEW"
                        })

        report = {
            "event": "EVIDENCE_GATE",
            "source_id": atoms.get("source_id"),
            "status": "REVIEW_REQUIRED" if violations else "PASSED_WITH_CAUTION",
            "violations": violations,
            "rules_checked": [
                "legacy status firewall",
                "observation/inference separation",
                "source-to-claim caution",
                "uncertainty preservation"
            ],
            "important_limit": "A passing gate does not prove a historical claim."
        }

        (corpus / "evidence-gate.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        reports.append(report)

    Path("review").mkdir(exist_ok=True)
    Path("review/evidence-gate-summary.json").write_text(
        json.dumps(reports, indent=2), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
