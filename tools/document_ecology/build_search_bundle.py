#!/usr/bin/env python3
"""Build an outward search bundle from the archive's documented network."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = Path(__file__).with_name("collection_model.json")
NETWORK = ROOT / "evidence" / "network_map.md"
DEFAULT_OUTPUT = ROOT / "research_queue" / "document_ecology"

DEFAULT_NODES = [
    "Joan Greene", "John Greene", "Daniel Greene", "James Greene", "H. Tibbits",
    "Edward Greene", "Mary Tibbitts", "Henry Tibbitts", "Benjamin Greene", "Havens",
    "Richard Smith", "Roger Williams", "Anashuecot", "Awawsunks", "Cakochawhunt",
    "John Wickes", "Samuel Gorton", "William Carpenter",
]


def network_nodes() -> list[str]:
    if not NETWORK.exists():
        return DEFAULT_NODES
    text = NETWORK.read_text(errors="replace")
    found = set(DEFAULT_NODES)
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("| Person A") or line.startswith("|---"):
            continue
        columns = [part.strip() for part in line.strip("|").split("|")]
        if len(columns) >= 2:
            found.update(value for value in columns[:2] if value and value != "[Havens]")
    return sorted(found)


def build(date: str, output: Path) -> tuple[Path, Path]:
    model = json.loads(MODEL.read_text())
    nodes = network_nodes()
    bundles = []
    for level in model["zoom_levels"]:
        for node in nodes:
            bundles.append({
                "run_date": date,
                "zoom_level": level["id"],
                "node": node,
                "question": level["question"],
                "record_families": level["record_families"],
                "status": "PENDING_HUMAN_REVIEW",
                "search_scope": "Repository, date range, jurisdiction, and exact record family must be recorded before a negative result is accepted.",
            })
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / f"{date}.json"
    md_path = output / f"{date}.md"
    json_path.write_text(json.dumps({"run_date": date, "nodes": nodes, "bundles": bundles}, indent=2) + "\n")
    lines = [
        f"# Document Ecology Search Bundle — {date}",
        "",
        "**Status:** PENDING_HUMAN_REVIEW. This is a search map, not evidence or a claim.",
        "**Center:** Joan Greene in the March 1682 deed.",
        "",
        "## How to use this bundle",
        "",
        """Move outward only after preserving the exact page-level question. At each level, search every listed record family, record the repository and scope, and keep identity collisions open. The purpose is to find Joan's documentary position in a network, not to turn proximity into proof.""",
        "",
        "## Network nodes",
        "",
        ", ".join(nodes),
        "",
    ]
    for level in model["zoom_levels"]:
        lines += [f"## {level['id']} — {level['question']}", ""]
        lines.append("**Record families:** " + "; ".join(level["record_families"]))
        lines.append("")
        for node in nodes:
            terms = f'"{node}" AND (' + " OR ".join(f'"{family}"' for family in level["record_families"]) + ")"
            lines.append(f"- [ ] **{node}** — `{terms}` — ❌ NOT SEARCHED")
        lines.append("")
    lines += ["## Record rules", ""]
    lines.extend(f"- {rule}" for rule in model["record_rules"])
    lines.append("")
    md_path.write_text("\n".join(lines))
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    json_path, md_path = build(args.date, Path(args.output))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
