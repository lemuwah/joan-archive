# Research findings intake

`research_findings/` is the intake/source folder for completed research notes.
New findings are routed in this order:

1. Archivist: provenance, repository identity, page/image anchors, checksums.
2. Hostile Review: identity collisions, circular citations, OCR errors, and unsupported inference.
3. Synthesizer: bounded claims and preserved contradictions.
4. Explorer: a required sideways search for nearby people, institutions, record families, material context, and evidence hiding in plain sight.

Run locally:

```sh
python3 tools/findings_pipeline/route_findings.py
python3 tools/findings_pipeline/route_findings.py --check
```

Packets are written to `research_queue/finding_runs/YYYY-MM-DD/`. The finding
itself is never edited, and every packet remains `PENDING_HUMAN_REVIEW`.

Images referenced by a finding must be supplied to `images/_pending_review/`
first. The router reports missing image references and never promotes an image
into the public archive.