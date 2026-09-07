# Daily Four-Agent Review

`orchestrate.py` is the second stage of the daily research workflow. It consumes the dated JSONL output from `tools/daily_research/sweep.py` and creates four independent, review-gated outputs:

- `Explorer` — preserves discovery queries, catalog results, and scoped misses.
- `Archivist` — queues stable identifiers, page/image anchors, and deduplication checks.
- `Synthesizer` — groups results into bounded lead proposals; it does not create facts.
- `Hostile Review` — attacks identity, date, OCR, circular-citation, and access assumptions.

After those role passes, the runner applies the same four layers to every origin model A–H:

1. **Document pass** — inspect the original page/image and record exact anchors and wording.
2. **Historian context pass** — explain the period, parties, jurisdiction, status language,
	and comparable records without turning context into identity proof.
3. **Hostile facts-only pass** — test identity, date, place, status, and citation independence.
4. **Continuing conflict/context pass** — preserve contradictions, competing Johns, missing
	jurisdictions, Indigenous/non-English context, and the strongest alternative explanation.

Model G remains an eliminated citation-contamination audit unless a primary source genuinely
overturns its chronology. It is included so the daily process can detect reintroduced La Mance
claims without silently treating that model as live.

## Outputs

- Dated reports: `research_queue/agent_runs/YYYY-MM-DD/`
- Replaceable role logic snapshots: `agents/*/daily_logic.md`
- Replaceable model logic snapshots: `agents/models/model_[a-h]_daily_logic.md`
- Run summary: `research_queue/agent_runs/YYYY-MM-DD/run_summary.json`

The static `agents/*/README.md` files are role contracts. They are intentionally not rewritten by findings: allowing findings to rewrite the instructions that govern their own review would contaminate the control layer. `daily_logic.md` is the transparent, replaceable findings-based update that the next run can read.

## Safety rules

- The input sweep is discovery, not verification.
- Agent agreement is not corroboration.
- Search metadata, OCR, and snippets are not quotations.
- Reports remain `PENDING_HUMAN_REVIEW`.
- A human must inspect the original document before updating `evidence/`, `people/`, or public pages.

The GitHub workflow runs the sweep and this orchestrator daily, then opens a PR containing the reports and logic snapshots. It never auto-merges.
