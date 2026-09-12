# The FamilySearch track — why it isn't automated, and what to do instead

The `008204949-*.JPG` images (North Kingstown Land Records, the deed images already in
`images/`) come from FamilySearch's microfilm/digital-image browser, not from Internet
Archive. That's a different system, and it doesn't have a clean automation path the way
`tools/next_page/fetch_next_ia_page.py` does for the archive.org-hosted printed volumes.

## Why this one's hard

FamilySearch does have a public developer API (OAuth 2, requires registering an app and a
logged-in FamilySearch user account — see `developers.familysearch.org`). But the resources
that work *without* a signed-in user are limited to Places, the Date Authority, Person
Search, Person Matches, and Relationship Finder. Browsing a specific reel of unindexed
microfilm images page-by-page — which is what "the next image in the 008204949 chain" means
— isn't one of those, and isn't part of the documented public API at all as far as this audit
found. It's the internal image viewer, reachable only through a signed-in browser session.

That means the only way to script it is to replay a logged-in session's requests — cookie-based
scraping. That's explicitly against automation norms most archives (FamilySearch included) set
for their viewers, and it's the kind of thing that gets an account rate-limited or locked. Not
worth building into a GitHub Action that could run unattended.

## What to do instead

The manual chase you're already doing is genuinely the right approach here — the automation
that's worth adding is on the AI side of the *pipeline*, once you already have the image, not
on the *fetching* side:

1. You (logged in) browse to the next image in the film and download or screenshot it — same
   as with image 10, 11, 12 already in the repo.
2. Drop it in `images/_pending_review/` (same staging folder the Internet Archive track uses).
3. Run `python tools/next_page/triage_pending_images.py` locally (with `ANTHROPIC_API_KEY` set)
   — it'll rough-transcribe it and flag whether any of the archive's core search terms
   (Greene, Joan, Quidnessett, Fones, etc.) show up, the same way it would for an
   automatically-fetched Internet Archive page. That's the part that actually saves you time —
   deciding whether a manuscript image is worth a close read, not the fetching.
4. If it's a hit, promote it into `images/` with a descriptive name and write it up on the
   relevant `people/` page's Search Log, same as the existing workflow.
5. If it's a miss — wrong page, blank, unrelated deed — log that in
   `primary_sources/NEGATIVE_LOG.md` the same way you already log other negative results.
   A "checked image N, not relevant" line is worth exactly as much as a positive hit, per
   Law 7 — it's what keeps the next person (human or AI) from re-checking the same page.

## If you want to push further on FamilySearch itself

Two options exist, both with real caveats:

- **Register a FamilySearch developer app** and use the official OAuth API for anything that
  *is* covered by it — Person Search and Family Tree lookups, mainly. This is legitimate and
  automatable, but it's a different kind of research (indexed persons/records) from browsing
  raw microfilm, so it wouldn't replace the manual chase described above.
- **A community-built FamilySearch MCP server exists** (by David Ulbrich, not an Anthropic or
  FamilySearch product) that lets an AI assistant call the FamilySearch API directly once you've
  registered your own app and credentials. Worth a look if the Person Search / Family Tree side
  becomes useful, but it doesn't cover the microfilm browsing case either — same API limits apply.
