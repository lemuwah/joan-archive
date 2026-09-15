from pathlib import Path
import json
import hashlib
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTROL_DIR = ROOT / "tools" / "research_control"
if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from event_spine import record_event

TARGET_FILE = ROOT / "research_queue" / "SEARCH_TARGETS.yml"

def add_target(question, reason, origin_event="", target_type="DOCUMENT", person_slots=None, jurisdictions=None, record_families=None, date_range=None, name_variants=None, laws=None, disproof_record=""):
    payload = {
        "question": question,
        "reason": reason,
        "origin_event": origin_event,
        "target_type": target_type,
        "person_slots": person_slots or [],
        "jurisdictions": jurisdictions or [],
        "record_families": record_families or [],
        "date_range": date_range or {},
        "name_variants": name_variants or [],
        "laws": laws or [],
        "disproof_record": disproof_record,
    }

    identity_payload = {
        "question": question,
        "target_type": target_type,
        "person_slots": person_slots or [],
        "jurisdictions": jurisdictions or [],
        "record_families": record_families or [],
        "date_range": date_range or {},
        "name_variants": name_variants or [],
    }

    raw = json.dumps(
        identity_payload,
        sort_keys=True,
        ensure_ascii=False,
    )

    target = {
        "target_id": "ST-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12],
        **payload,
        "status": "READY_SHADOW",
    }

    if TARGET_FILE.exists():
        data = yaml.safe_load(TARGET_FILE.read_text(encoding="utf-8")) or {}
    else:
        data = {}

    data.setdefault("targets", [])

    target_exists = any(
        x.get("target_id") == target["target_id"]
        for x in data["targets"]
    )

    if not target_exists:
        data["targets"].append(target)

        record_event(
            agent="SEARCH_TARGET_GENERATOR",
            action="NEW_SEARCH_TARGET",
            target=target["target_id"],
            laws=target["laws"],
            search_scope={
                "target_type": target["target_type"],
                "person_slots": target["person_slots"],
                "jurisdictions": target["jurisdictions"],
                "record_families": target["record_families"],
                "date_range": target["date_range"],
                "name_variants": target["name_variants"],
            },
            evidence=target["reason"],
            result=target["question"],
            status=target["status"],
            contradiction=target["disproof_record"],
            next_action="Execute target search when target status is promoted from READY_SHADOW.",
            parent_event=target["origin_event"],
            event_class="RESEARCH",
        )

    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    TARGET_FILE.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    return target

def mark_target_executed(target_id, target_file=None):
    path = Path(target_file) if target_file else TARGET_FILE

    if not path.exists():
        raise ValueError(f"TARGET_FILE_NOT_FOUND: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    targets = data.setdefault("targets", [])

    for target in targets:
        if target.get("target_id") != target_id:
            continue

        current_status = target.get("status")

        if current_status != "READY":
            raise ValueError(
                f"TARGET_STATUS_TRANSITION_BLOCKED: "
                f"{target_id} status={current_status}"
            )

        target["status"] = "EXECUTED"

        path.write_text(
            yaml.safe_dump(
                data,
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

        return target

    raise ValueError(f"TARGET_NOT_FOUND: {target_id}")
