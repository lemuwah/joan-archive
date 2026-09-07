# Next-Page Tooling

Added 2026-09-07. Automates the "find the next image in the chain" part of the research
process for sources where that's actually automatable, and documents honestly where it isn't.

## Track A — Internet Archive volumes (automatable, do this)

17 of the archive's core printed sources (Bartlett's Colonial Records, Arnold's Records of
the Colony, Potter's Early History, RIHS Collections, the Greene genealogies, etc.) are
already hosted as public-domain scans on archive.org. For these, "next page" is a clean,
scriptable IIIF Image API call — no login, no ToS concern, safe to run in CI.

- `sources.yml` — registry of known volumes. Fill in `last_known_seq` for a volume before
  the fetcher will chase its next page.
- `fetch_next_ia_page.py` — pulls the next unfetched leaf into `images/_pending_review/`,
  or logs "not found" if the volume ends there. Logs every attempt either way to
  `research_queue/next_page_fetch_log.md`.
- `triage_pending_images.py` — optional AI first pass over anything in
  `images/_pending_review/`: rough transcription + flags whether core search terms
  (Greene, Joan, Quidnessett, Fones, etc.) show up. Tagged AI-SOURCED per Law 7 — a
  triage aid, not a citation.
- `.github/workflows/fetch-next-page.yml` — runs both, manually triggered only, opens a
  PR for human review. Never auto-merges. Set an `ANTHROPIC_API_KEY` repo secret to enable
  the triage step; without it the workflow still fetches and logs, just skips triage.

**To run:** Actions tab → "Fetch next archive page(s)" → Run workflow. Leave the volume_id
input blank to check every volume in `sources.yml` at once, or fill in one identifier to
check just that volume.

## Track B — FamilySearch manuscript images (manual, by design)

The deed-book scans (`008204949-*.JPG`) come from FamilySearch's microfilm viewer, which
doesn't expose sequential page browsing through its public API. See
`familysearch_manual_track.md` for why, and for the recommended workflow — you still fetch
these by hand, but `triage_pending_images.py` above works on them too once they're in
`images/_pending_review/`, so the AI-assist still helps on the review side even where it
can't help on the fetching side.

## Either track, the same rule applies

Nothing lands in `images/` or on a `people/` page without a human decision. Both tracks only
ever produce a PR (Track A) or a locally-staged pending file (Track B) — never a direct
commit to a published page. That matches how the archive already treats AI output everywhere
else: leads, not citations, until a human verifies them.
