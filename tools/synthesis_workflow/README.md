# Legacy-page synthesis workflow

This workflow makes the broad `/people/` pages usable as historical notes without
silently turning their older assumptions into current facts.

## Run

```sh
python3 tools/synthesis_workflow/synthesize_legacy_pages.py
python3 tools/synthesis_workflow/synthesize_legacy_pages.py --check
```

The first command scans each top-level people page and writes:

- `data/research/legacy_observations.jsonl` — immutable content-hash snapshots
- `data/research/synthesis_proposals.jsonl` — bounded, review-only proposals

The generator never edits a people page, changes a claim status, or promotes a
source. If a page changes, its new hash creates a new observation while the old
snapshot remains in the record. A human may later link an observation to a
source-backed claim through the normal evidence pipeline.

## Review boundary

Every proposal starts as `PENDING_HUMAN_REVIEW`, has
`promotion_allowed: false`, and proposes only `RETAIN_AS_LEGACY_NOTE`. The
existing candidate-source validator and human review gates remain authoritative
for source verification.