# Daily Four-Agent Review

`orchestrate.py` is the second stage of the daily research workflow. It consumes the dated JSONL output from `tools/daily_research/sweep.py` and creates four independent, review-gated outputs:

- `Explorer` — preserves discovery queries, catalog results, and scoped misses.
- `Archivist` — queues stable identifiers, page/image anchors, and deduplication checks.
- `Synthesizer` — groups results into bounded lead proposals; it does not create facts.
- `Hostile Review` — attacks identity, date, OCR, circular-citation, and access assumptions.

## Outputs

- Dated reports: `research_queue/agent_runs/YYYY-MM-DD/`
- Replaceable role logic snapshots: `agents/*/daily_logic.md`
- Run summary: `research_queue/agent_runs/YYYY-MM-DD/run_summary.json`

The static `agents/*/README.md` files are role contracts. They are intentionally not rewritten by findings: allowing findings to rewrite the instructions that govern their own review would contaminate the control layer. `daily_logic.md` is the transparent, replaceable findings-based update that the next run can read.

## Safety rules

- The input sweep is discovery, not verification.
- Agent agreement is not corroboration.
- Search metadata, OCR, and snippets are not quotations.
- Reports remain `PENDING_HUMAN_REVIEW`.
- A human must inspect the original document before updating `evidence/`, `people/`, or public pages.

The GitHub workflow runs the sweep and this orchestrator daily, then opens a PR containing the reports and logic snapshots. It never auto-merges.
