# Research Findings Intake

This folder is the source-of-record intake for completed research notes. A finding may contain leads, negative results, context, or contradictions; it is not automatically evidence.

## Review order

Every new finding goes through the ordered queue:

1. **Archivist**: establish repository identity, stable identifiers, page/image anchors, and checksum needs.
2. **Hostile Review**: test identity collisions, circular citations, OCR errors, missing pages, and unsupported inference.
3. **Synthesizer**: propose bounded claims and preserve contradictions. No synthesis promotes a claim to proof.
4. **Explorer**: perform a sideways-context action for that finding: inspect associated people, witnesses, neighbors, institutions, jurisdictions, Indigenous or non-English record families, material evidence, and other places the evidence may be hiding in plain sight.

The router creates review packets with:

```sh
python3 tools/findings_pipeline/route_findings.py
```

Packets are written to `research_queue/finding_runs/YYYY-MM-DD/` and remain
`PENDING_HUMAN_REVIEW`. The source finding is never rewritten by the router.

## Images

New or newly supplied images belong in `images/_pending_review/` first. Include
repository, collection, stable identifier, image/page number, access date, and
any checksum available. Do not link an unreviewed image as public evidence.

## Privacy and consent

Do not name helpers, archivists, descendants, scholars, or contributors without
permission. Use institution-level attribution when it is enough to establish
provenance. Record private correspondence only at the level authorized for
public release.
