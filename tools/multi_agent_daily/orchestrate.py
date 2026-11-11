#!/usr/bin/env python3
"""Build four daily, Laws-filtered agent reports from one source sweep.

This runner is deliberately deterministic. It does not turn search results into facts,
call one agent to approve another, or edit role READMEs. It produces dated operational
logic files filtered through the Multi Agent Laws, with periodic human review.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
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
    """Load sweep records with verifiable source-location provenance."""
    source_path = path.resolve()
    source_bytes = source_path.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    source_lines = source_bytes.decode("utf-8").splitlines()

    try:
        display_path = source_path.relative_to(ROOT).as_posix()
    except ValueError:
        display_path = str(source_path)

    records = []
    for line_number, line in enumerate(source_lines, 1):
        if line.strip():
            record = json.loads(line)
            record["_source_provenance"] = {
                "source_path": display_path,
                "source_sha256": source_hash,
                "source_line": line_number,
            }
            records.append(record)
    return records


def result_rows(records: list[dict]) -> list[dict]:
    """Expand results while retaining an exact pointer to each source result."""
    rows = []
    for record in records:
        provenance = record.get("_source_provenance")
        parent = {
            key: value
            for key, value in record.items()
            if key != "_source_provenance"
        }

        for result_index, result in enumerate(record.get("results", [])):
            individual_result = dict(result)
            row = {**parent, "result": individual_result}

            if provenance:
                description = individual_result.get("description")
                description_hash = None
                description_length = None

                if isinstance(description, str):
                    description_bytes = description.encode("utf-8")
                    description_hash = hashlib.sha256(
                        description_bytes
                    ).hexdigest()
                    description_length = len(description)

                row["source_reference"] = {
                    **provenance,
                    "result_index": result_index,
                    "description_sha256": description_hash,
                    "description_length": description_length,
                }

            rows.append(row)
    return rows


def recover_deferred_result(lead: dict) -> dict:
    """Recover and verify the complete original result for a deferred lead."""
    reference = lead.get("source_reference")
    if not isinstance(reference, dict):
        raise ValueError("Deferred lead has no source_reference")

    required = (
        "source_path",
        "source_sha256",
        "source_line",
        "result_index",
    )
    missing = [key for key in required if key not in reference]
    if missing:
        raise ValueError(
            f"Deferred lead source_reference is incomplete: {missing}"
        )

    source_path = Path(reference["source_path"])
    if not source_path.is_absolute():
        source_path = ROOT / source_path

    if not source_path.is_file():
        raise FileNotFoundError(
            f"Deferred lead source sweep is missing: {source_path}"
        )

    source_bytes = source_path.read_bytes()
    actual_source_hash = hashlib.sha256(source_bytes).hexdigest()
    if actual_source_hash != reference["source_sha256"]:
        raise ValueError(
            f"Deferred lead source sweep hash mismatch: {source_path}"
        )

    lines = source_bytes.decode("utf-8").splitlines()
    line_number = reference["source_line"]
    if type(line_number) is not int or not 1 <= line_number <= len(lines):
        raise ValueError("Deferred lead source line is invalid")

    source_record = json.loads(lines[line_number - 1])
    results = source_record.get("results", [])
    result_index = reference["result_index"]

    if (
        type(result_index) is not int
        or not 0 <= result_index < len(results)
    ):
        raise ValueError("Deferred lead result index is invalid")

    recovered = dict(results[result_index])

    # Ensure the pointer resolves to the same result represented by this
    # compact deferred lead, not merely another valid result in the source.
    compact_result = lead.get("result", {})
    for key, value in compact_result.items():
        if recovered.get(key) != value:
            raise ValueError(
                f"Recovered result does not match deferred lead field: {key}"
            )

    description = recovered.get("description")

    expected_description_hash = reference.get("description_sha256")
    expected_description_length = reference.get("description_length")

    if expected_description_hash is not None:
        if not isinstance(description, str):
            raise ValueError("Original description is missing or not text")

        actual_description_hash = hashlib.sha256(
            description.encode("utf-8")
        ).hexdigest()

        if actual_description_hash != expected_description_hash:
            raise ValueError("Recovered description hash mismatch")

        if len(description) != expected_description_length:
            raise ValueError("Recovered description length mismatch")

    return recovered


def allocate_fair_leads(
    leads: list[dict],
    budget: int,
) -> tuple[list[dict], list[dict]]:
    """Allocate a bounded processing budget fairly across people.

    Each person's leads retain their existing order. The global budget is
    consumed round-robin across people so that one person's lead volume
    cannot consume the entire processing budget before another person is
    considered.

    The returned lists form an exhaustive partition of the input: selected
    leads are processed now; deferred leads remain preserved for later.
    """
    if budget < 0:
        raise ValueError("budget must be non-negative")

    by_person: dict[str, list[dict]] = defaultdict(list)
    person_order: list[str] = []

    for lead in leads:
        person = lead.get("person_name", "").strip()
        if person not in by_person:
            person_order.append(person)
        by_person[person].append(lead)

    selected: list[dict] = []
    positions = {person: 0 for person in person_order}

    while len(selected) < budget:
        made_progress = False

        for person in person_order:
            pos = positions[person]
            person_leads = by_person[person]

            if pos >= len(person_leads):
                continue

            selected.append(person_leads[pos])
            positions[person] = pos + 1
            made_progress = True

            if len(selected) >= budget:
                break

        if not made_progress:
            break

    selected_keys = {id(lead) for lead in selected}
    deferred = [lead for lead in leads if id(lead) not in selected_keys]

    return selected, deferred

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

    processing_budget = 100
    selected_leads, deferred_leads = allocate_fair_leads(
        leads=leads,
        budget=processing_budget,
    )

    for lead in selected_leads:
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

        question = f"Investigate source record '{title}'"
        if result.get("record_id"):
            question += f" [record ID: {result['record_id']}]"

        reason_parts = [
            "Originating search context is UNVERIFIED and does not establish "
            "that this source concerns the searched person or belongs to the "
            "originating research lens."
        ]

        if person:
            reason_parts.append(
                f"Searched person (unverified context only): {person}."
            )

        if lens:
            reason_parts.append(
                f"Originating research lens (unverified context only): {lens}."
            )

        if query:
            reason_parts.append(
                f"Original search query (discovery provenance only): {query}."
            )

        if source_ref:
            reason_parts.append(f"Source identifier: {source_ref}.")
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
            person_slots=[],
            jurisdictions=[],
            record_families=[],
            date_range={},
            name_variants=[],
            target_file=target_file,
            event_file=event_file,
            source_identifier=source_ref,
            laws=laws,
            disproof_record=(
                "Do not attribute this source to the searched person or "
                "originating research lens based on search context alone. "
                "Verify the underlying source's content, author, date, place, "
                "record family, and identity before linking it to a person "
                "or treating it as evidence."
            ),
        )
        generated.append(target)

    deferred = []
    for lead in deferred_leads:
        preserved = dict(lead)
        preserved.pop("results", None)

        # Keep the individual result's identifiers, but retrieve its potentially
        # enormous description from the original sweep through source_reference.
        individual_result = dict(preserved.get("result", {}))
        individual_result.pop("description", None)
        preserved["result"] = individual_result

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
