from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[2]
EVENT_FILE = ROOT / "research_queue" / "research_events.jsonl"

FOUR_AGENTS = [
    "EXPLORER",
    "ARCHIVIST",
    "HOSTILE_REVIEW",
    "SYNTHESIZER",
]

SEVEN_LAWS = {
    "No Narrative Smoothing",
    "La Mance Law / Follow the Rivers",
    "No Premature Elimination",
    "No Algorithmic Contamination",
    "No Jurisdictional Assumption",
    "No Centering",
    "No Trust Without Evidence",
}


def load_events():
    if not EVENT_FILE.exists():
        return []

    events = []

    for line in EVENT_FILE.read_text(
        encoding="utf-8"
    ).splitlines():
        if line.strip():
            events.append(json.loads(line))

    return events


def verify_agent_chain(candidate):
    events = load_events()

    candidate = candidate.strip()

    if not candidate:
        return False, "Candidate is empty"

    matching = [
        event
        for event in events
        if event.get("target", "").strip() == candidate
    ]

    if not matching:
        return False, "No Event Spine events found for candidate"

    by_agent = {}

    for event in matching:
        agent = event.get("agent", "").strip().upper()

        if agent in FOUR_AGENTS:
            by_agent.setdefault(agent, []).append(event)

    missing_agents = [
        agent
        for agent in FOUR_AGENTS
        if agent not in by_agent
    ]

    if missing_agents:
        return False, (
            "Missing agent events: "
            + ", ".join(missing_agents)
        )

    selected = {
        agent: sorted(
            by_agent[agent],
            key=lambda event: event["timestamp"],
        )[-1]
        for agent in FOUR_AGENTS
    }

    explorer = selected["EXPLORER"]
    archivist = selected["ARCHIVIST"]
    hostile = selected["HOSTILE_REVIEW"]
    synthesizer = selected["SYNTHESIZER"]

    if archivist.get("parent_event") != explorer.get("event_id"):
        return False, (
            "Archivist event is not linked to Explorer event"
        )

    if hostile.get("parent_event") != archivist.get("event_id"):
        return False, (
            "Hostile Review event is not linked to Archivist event"
        )

    if synthesizer.get("parent_event") != hostile.get("event_id"):
        return False, (
            "Synthesizer event is not linked to Hostile Review event"
        )

    for agent, event in selected.items():
        laws = set(event.get("laws", []))
        missing_laws = SEVEN_LAWS - laws

        if missing_laws:
            return False, (
                f"{agent} event missing Laws: "
                + ", ".join(sorted(missing_laws))
            )

    return True, "Four-agent Seven-Law evidence chain verified"
