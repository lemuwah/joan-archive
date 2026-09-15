import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    Path("reports").mkdir(exist_ok=True)

    lines = [
        "# Historical Source Audit Report",
        "",
        "> This report records pipeline activity. It is not a historical conclusion.",
        ""
    ]

    corpus = Path("corpus") / args.source

    if not corpus.is_dir():
        raise SystemExit(
            f"REPORT_BLOCKED: source corpus not found: {corpus}"
        )

    for corpus in [corpus]:

        required = [
            corpus / "source.json",
            corpus / "evidence-gate.json",
            corpus / "atoms.json",
        ]

        missing = [str(p) for p in required if not p.exists()]
        if missing:
            raise SystemExit(
                "REPORT_BLOCKED: required upstream artifacts missing: "
                + ", ".join(missing)
            )

        source = json.loads(
            (corpus / "source.json").read_text(encoding="utf-8")
        )
        gate = json.loads(
            (corpus / "evidence-gate.json").read_text(encoding="utf-8")
        )
        atoms = json.loads(
            (corpus / "atoms.json").read_text(encoding="utf-8")
        )

        lines.extend([
            f"## {source['source_id']}",
            "",
            f"- Source: `{source['repository_path']}`",
            f"- External image: `{source.get('image_reference', 'not supplied')}`",
            f"- Gate status: **{gate['status']}**",
            f"- Observations: {atoms['observation_count']}",
            f"- Inferences: {atoms['inference_count']}",
            f"- Hypotheses: {atoms['hypothesis_count']}",
            f"- Tests: {atoms['test_count']}",
            ""
        ])

        if gate["violations"]:
            lines.append("### Review flags")
            for violation in gate["violations"]:
                lines.append(
                    f"- `{violation['legacy_label']}` must not automatically become "
                    f"`{violation['forbidden_promotion']}`."
                )
            lines.append("")

        lines.extend([
            "### Control-plane warning",
            "",
            "The source image and its repository identification were verified by the archive owner; the pipeline does not independently verify the external manuscript.",
            "The available image is the best available capture and preserves the visible evidence; image readability is limited.",
            "The existing transcription remains a working lead and is not a professional paleographic transcription.",
            "No AI agreement is treated as independent corroboration.",
            ""
        ])

    Path("reports/historical-source-audit.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
