from pathlib import Path
import json
import hashlib
import yaml

ROOT = Path(__file__).resolve().parents[2]
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

    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)

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

    if not any(x.get("target_id") == target["target_id"] for x in data["targets"]):
        data["targets"].append(target)

    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    TARGET_FILE.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    return target
