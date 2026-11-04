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

## Recovery and interrupted publication

The two research ledgers are replaced separately; the pair is not a single
atomic filesystem operation. A transaction journal records the original and
intended bytes of both ledgers, hashes, and original-existence flags before
publication.

Build and check operations share a process lock with recovery. An unresolved
journal blocks another build or check until recovery is attempted. Run:

    python3 tools/synthesis_workflow/synthesize_legacy_pages.py --recover

Recovery compares each ledger with its recorded original and intended states.
If either ledger contains unexpected bytes, recovery refuses to overwrite it
and preserves the journal for investigation. If publication was incomplete,
recovery restores and verifies the original states before clearing the journal.
If both ledgers match the intended bytes, recovery retains that pair and clears
the journal.

The journal is recovery evidence, not a historical research finding. Preserve
it whenever recovery cannot safely resolve the transaction. Atomic replacement
of individual files does not, by itself, guarantee crash durability of the
two-file transaction.
