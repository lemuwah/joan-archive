#!/usr/bin/env python3
"""Build four daily, Laws-filtered agent reports from one source sweep.

This runner is deliberately deterministic. It does not turn search results into facts,
call one agent to approve another, or edit role READMEs. It produces dated operational
logic files filtered through the Multi Agent Laws, with periodic human review.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROL_DIR = ROOT / "tools" / "research_control"
if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from event_spine import record_event
from search_targets import add_target

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
        "**Evidence state:** AI-assisted working report; all leads are `LAWS_FILTERED`. Periodic human review applies.",
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
        "**Input:** One daily multi-perspective sweep; all outputs are `LAWS_FILTERED`.",
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


def generate_search_targets(
    leads: list[dict],
    origin_event: str,
    laws: list[str],
    target_file: Path | None = None,
    event_file: Path | None = None,
) -> dict:
    """Convert discovered leads into bounded targets while preserving overflow.

    The processing budget limits target generation, not discovery preservation.

    Leads within the current processing budget become READY_SHADOW research
    targets. Leads beyond that budget are explicitly preserved as deferred
    research leads. Deferred leads have not been searched, rejected, or
    evaluated negatively.
    """
    generated = []
    deferred = []

    processing_budget = 100

    for lead in leads[:processing_budget]:
        result = lead.get("result", {})
        person = lead.get("person_name", "").strip()
        lens = lead.get("lens", "").strip()
        query = lead.get("query", "").strip()
        title = (
            result.get("title")
            or result.get("record_id")
            or "untitled source"
        )
        source_ref = result.get("url") or result.get("record_id") or ""

        question = (
            f"Investigate the source lead '{title}' for {person}"
            if person
            else f"Investigate the source lead '{title}'"
        )

        reason_parts = [
            f"Generated from the {lens or 'research'} lens.",
        ]

        if query:
            reason_parts.append(f"Original search query: {query}.")

        if source_ref:
            reason_parts.append(f"Source lead: {source_ref}.")
        else:
            reason_parts.append(
                "No stable source identifier was returned; preserve this "
                "as a lead rather than treating it as evidence."
            )

        target = add_target(
            question=question,
            reason=" ".join(reason_parts),
            origin_event=origin_event,
            target_type="DOCUMENT",
            person_slots=[person] if person else [],
            jurisdictions=[],
            record_families=[lens] if lens else [],
            date_range={},
            name_variants=[person] if person else [],
            target_file=target_file,
            event_file=event_file,
            source_identifier=source_ref,
            laws=laws,
            disproof_record=(
                "Discard or redirect this target if the underlying source "
                "concerns a different person, place, date, or record family."
            ),
        )
        generated.append(target)

    for lead in leads[processing_budget:]:
        preserved = dict(lead)
        preserved["preservation_status"] = "DEFERRED"
        preserved["preservation_reason"] = (
            "Discovered lead was not processed into a search target during "
            "this run because the bounded target-generation budget was reached."
        )
        preserved["preservation_origin_event"] = origin_event
        deferred.append(preserved)

    return {
        "generated": generated,
        "deferred": deferred,
    }


def run(
    date: str,
    sweep_path: Path,
    output_root: Path,
    role_output: Path,
    target_file: Path | None = None,
    event_file: Path | None = None,
) -> Path:
    records = load_records(sweep_path)
    leads = result_rows(records)
    unique = {}
    for lead in leads:
        unique[lead_key(lead)] = lead
    leads = list(unique.values())
    output_dir = output_root / date
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    event_parent = ""
    event_laws = [
        "No Narrative Smoothing",
        "La Mance Law / Follow the Rivers",
        "No Premature Elimination",
        "No Algorithmic Contamination",
        "No Jurisdictional Assumption",
        "No Centering",
        "No Trust Without Evidence",
    ]

    role_order = [
        ("explorer", "EXPLORER"),
        ("archivist", "ARCHIVIST"),
        ("hostile_review", "HOSTILE_REVIEW"),
        ("synthesizer", "SYNTHESIZER"),
    ]

    for role, agent_name in role_order:
        role_leads = leads
        if role == "archivist":
            role_leads = [
                lead for lead in leads
                if lead["result"].get("url") or lead["result"].get("record_id")
            ]

        generated_path = write_logic(
            role,
            date,
            records,
            role_leads,
            output_dir,
            role_output,
        )
        generated.append(generated_path)

        event = record_event(
            agent=agent_name,
            action="AGENT_ROLE_RUN",
            target=f"DAILY-SWEEP-{date}",
            laws=event_laws,
            search_scope={
                "input": str(sweep_path),
                "date": date,
                "lead_count": len(role_leads),
            },
            evidence=str(generated_path),
            result=f"{agent_name} completed daily role report",
            status="LAWS_FILTERED",
            next_action="Continue to next agent in four-agent chain.",
            parent_event=event_parent,
            event_class="RESEARCH",
            event_file=event_file,
        )
        event_parent = event["event_id"]

    target_result = generate_search_targets(
        leads=leads,
        origin_event=event_parent,
        laws=event_laws,
        target_file=target_file,
        event_file=event_file,
    )
    search_targets = target_result["generated"]
    deferred_leads = target_result["deferred"]

    deferred_path = output_dir / "deferred_leads.json"
    deferred_path.write_text(
        json.dumps(deferred_leads, indent=2) + "\n"
    )

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
        "search_targets_generated": len(search_targets),
        "leads_deferred": len(deferred_leads),
        "deferred_leads_artifact": str(deferred_path.relative_to(output_dir)),
        "status": "LAWS_FILTERED",
        "note": "Reports generate leads and review logic only, filtered through the Multi Agent Laws. They do not update facts or role READMEs. Periodic human review applies.",
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
