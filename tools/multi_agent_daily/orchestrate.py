#!/usr/bin/env python3
"""Build four daily, review-gated agent reports from one source sweep.

This runner is deliberately deterministic. It does not turn search results into facts,
call one agent to approve another, or edit role READMEs. It produces dated operational
logic files that humans can review and use as the next run's input.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SWEEP = ROOT / "research_queue" / "daily_sweep"
DEFAULT_OUTPUT = ROOT / "research_queue" / "agent_runs"
MODEL_PROFILES = Path(__file__).with_name("model_profiles.json")
ROLE_DIRS = {
    "explorer": ROOT / "agents" / "Explorer",
    "archivist": ROOT / "agents" / "Archivist",
    "synthesizer": ROOT / "agents" / "Synthesizer",
    "hostile_review": ROOT / "agents" / "hostile_reviewer",
}


def load_records(path: Path) -> list[dict]:
    records = []
    for line in path.read_text().splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def result_rows(records: list[dict]) -> list[dict]:
    rows = []
    for record in records:
        for result in record.get("results", []):
            rows.append({**record, "result": result})
    return rows


def lead_key(row: dict) -> tuple[str, str, str]:
    result = row["result"]
    return (row["person_name"], row["lens"], result.get("url") or result.get("record_id") or "")


def model_leads(profile: dict, leads: list[dict]) -> list[dict]:
    terms = [term.lower() for term in profile["search_terms"]]
    matching = []
    for lead in leads:
        haystack = " ".join([
            lead.get("person_name", ""), lead.get("lens", ""), lead.get("query", ""),
            json.dumps(lead.get("result", {}), ensure_ascii=True),
        ]).lower()
        if any(term in haystack for term in terms):
            matching.append(lead)
    return matching


def write_model_report(model_id: str, profile: dict, date: str, leads: list[dict], output_dir: Path, role_output: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"model_{model_id.lower()}.md"
    lines = [
        f"# Model {model_id} Agent — {profile['name']} — {date}",
        "",
        f"**Status:** {profile['status']}",
        "**Evidence state:** AI-assisted working report; all leads remain `PENDING_HUMAN_REVIEW`.",
        "",
        "## 1. Document pass",
        "Read the original page/image before treating any catalog result as evidence. Record repository, stable identifier, page/leaf, access date, and exact wording.",
        "",
        "## 2. Historian context pass",
        f"**Repositories and record families:** {', '.join(profile['repositories'])}.",
        f"**What could confirm this model:** {profile['confirm']}",
        f"**Context caution:** {profile['caution']}",
        "",
        "## 3. Hostile facts-only pass",
        f"**What could disconfirm this model:** {profile['disconfirm']}",
        "Test identity, date, place, status wording, and citation independence separately. Do not infer a result from silence.",
        "",
        "## 4. Continuing conflict/context layer",
        "Record parties, witnesses, jurisdiction, legal setting, Indigenous and non-English context, competing Johns, and every unresolved contradiction. Preserve the strongest alternative explanation.",
        "",
        f"## Leads matching this model's search vocabulary ({len(leads)})",
    ]
    if leads:
        for lead in leads[:100]:
            result = lead["result"]
            lines.append(
                f"- **{lead['person_name']}** / `{lead['lens']}` — "
                f"{result.get('title') or result.get('record_id') or 'untitled'}; "
                f"{result.get('url') or 'no URL'}. Original-document review required."
            )
    else:
        lines.append("- No matching catalog lead in this run. Keep the model open or eliminated only according to its documented status and continue the scoped search.")
    content = "\n".join(lines) + "\n"
    path.write_text(content)
    model_path = role_output / "agents" / "models" / f"model_{model_id.lower()}_daily_logic.md"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(content)
    return path


def write_logic(
    role: str,
    date: str,
    records: list[dict],
    leads: list[dict],
    output_dir: Path,
    role_output: Path,
) -> Path:
    statuses = Counter(record.get("status") for record in records)
    lenses = Counter(record.get("lens") for record in records if record.get("status") == "FOUND")
    path = output_dir / f"{role}.md"
    role_title = role.replace("_", " ").title()
    lines = [
        f"# {role_title} Daily Logic — {date}",
        "",
        "**Status:** AI-assisted working report. Not a source, citation, or approval.",
        "**Input:** One daily multi-perspective sweep; all outputs remain `PENDING_HUMAN_REVIEW`.",
        "",
    ]
    if role == "explorer":
        lines += [
            "## Discovery logic",
            "- Preserve the exact query, repository, URL, and run date for every lead.",
            "- Treat `NO_RESULTS` as scoped only to this query and catalog.",
            f"- Sweep status counts: {dict(statuses)}.",
            "",
            "## Leads to carry forward",
        ]
    elif role == "archivist":
        lines += [
            "## Provenance logic",
            "- Require a stable repository identifier and page/image anchor before verification.",
            "- Deduplicate by URL or repository identifier; do not count catalog duplicates as corroboration.",
            "- Preserve access limitations and failed requests as part of the record.",
            "",
            "## Provenance queue",
        ]
    elif role == "synthesizer":
        lines += [
            "## Synthesis logic",
            "- Group leads by person and lens; propose questions, never facts.",
            "- Keep identity, date, place, and status as separate fields until independently anchored.",
            "- No result becomes `PROOF` from search metadata or agent agreement.",
            "",
            "## Bounded lead proposals",
        ]
    else:
        lines += [
            "## Hostile-review logic",
            "- Attack name collision, date mismatch, repository duplication, OCR error, and circular citation risk.",
            "- Ask what source would disprove the lead and whether a non-English, Indigenous, material, or oral-history path was skipped.",
            "- Keep rejected and negative results; do not delete failed searches.",
            "",
            "## Review targets",
        ]
    if lenses:
        lines.append(f"Found-lead lens counts: {dict(lenses)}.")
        lines.append("")
    if not leads:
        lines.append("- No catalog leads in this run. Preserve the negative result and expand repository coverage before changing the hypothesis.")
    else:
        for lead in leads[:100]:
            result = lead["result"]
            lines.append(
                f"- **{lead['person_name']}** / `{lead['lens']}` — "
                f"{result.get('title') or result.get('record_id') or 'untitled'}; "
                f"{result.get('url') or 'no URL returned'}. "
                "Requires original-document review."
            )
    content = "\n".join(lines) + "\n"
    path.write_text(content)
    # Keep role READMEs stable; this is the reviewed, replaceable logic snapshot
    # each role can read on the next run.
    role_logic = role_output / ROLE_DIRS[role].relative_to(ROOT) / "daily_logic.md"
    role_logic.parent.mkdir(parents=True, exist_ok=True)
    role_logic.write_text(content)
    return path


def run(date: str, sweep_path: Path, output_root: Path, role_output: Path) -> Path:
    records = load_records(sweep_path)
    leads = result_rows(records)
    unique = {}
    for lead in leads:
        unique[lead_key(lead)] = lead
    leads = list(unique.values())
    output_dir = output_root / date
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for role in ROLE_DIRS:
        role_leads = leads
        if role == "archivist":
            role_leads = [lead for lead in leads if lead["result"].get("url") or lead["result"].get("record_id")]
        generated.append(write_logic(role, date, records, role_leads, output_dir, role_output))

    profiles = json.loads(MODEL_PROFILES.read_text())["models"]
    model_counts = {}
    for model_id, profile in profiles.items():
        matching = model_leads(profile, leads)
        model_counts[model_id] = len(matching)
        generated.append(write_model_report(model_id, profile, date, matching, output_dir / "models", role_output))

    try:
        input_name = str(sweep_path.relative_to(ROOT))
    except ValueError:
        input_name = str(sweep_path)
    summary = {
        "run_date": date,
        "input": input_name,
        "records": len(records),
        "unique_catalog_leads": len(leads),
        "statuses": dict(Counter(record.get("status") for record in records)),
        "roles": [path.stem for path in generated],
        "model_leads": model_counts,
        "status": "PENDING_HUMAN_REVIEW",
        "note": "Reports generate leads and review logic only; they do not update facts or role READMEs.",
    }
    (output_dir / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--sweep", help="Daily sweep JSONL; defaults to research_queue/daily_sweep/<date>.jsonl")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--role-output", default=str(ROOT), help="Root for agents/*/daily_logic.md")
    args = parser.parse_args()
    sweep_path = Path(args.sweep) if args.sweep else DEFAULT_SWEEP / f"{args.date}.jsonl"
    if not sweep_path.exists():
        raise SystemExit(f"Sweep file does not exist: {sweep_path}")
    output_dir = run(args.date, sweep_path, Path(args.output), Path(args.role_output))
    print(f"Wrote four agent reports to {output_dir}")


if __name__ == "__main__":
    main()
