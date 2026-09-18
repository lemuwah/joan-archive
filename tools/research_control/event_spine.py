from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

ROOT = Path(__file__).resolve().parents[2]
EVENT_FILE = ROOT / "research_queue" / "research_events.jsonl"


def record_event(
    agent,
    action,
    target="",
    laws=None,
    search_scope=None,
    source="",
    evidence="",
    result="",
    status="RECORDED",
    contradiction="",
    next_action="",
    parent_event="",
    event_class="RESEARCH",
    event_file=None,
):
    event = {
        "event_id": "EVT-" + uuid.uuid4().hex[:12],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_class": event_class,
        "agent": agent,
        "action": action,
        "target": target,
        "laws": laws or [],
        "search_scope": search_scope or {},
        "source": source,
        "evidence": evidence,
        "result": result,
        "status": status,
        "contradiction": contradiction,
        "next_action": next_action,
        "parent_event": parent_event,
    }

    path = Path(event_file) if event_file else EVENT_FILE
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    return event
