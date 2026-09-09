# Joan Archive — Task Queue

## How to use this file
Any AI helper working on this archive: read `methodology/agent_orientation.md` first. Then come here. Pick the highest-priority NOT STARTED task whose dependencies are DONE. Execute it. Update the status when finished. If interrupted mid-task, update "What's already done" before stopping.

Laws, models, and facts evolve as research progresses. Do not assume they match your last session. Re-read before working.

**Verification rule (added 2026-09-07, after a full audit found 3 of 7 task cards had false status claims):** A task may only be marked DONE, or a sub-item checked off, if the grep/file-check command that confirms it is run in the same session and its output matches the claim. Do not mark DONE from memory of intent, from another agent's unverified report, or by generalizing a single failed check across a whole list (see the Task 5 note below for exactly this failure mode). If you didn't run the check this session, the honest status is IN PROGRESS or NOT STARTED, not DONE.

---

## Mission Statement
Every direction gets tested. English, Indigenous, maritime, religious, legal, archaeological, linguistic. We don't know what we don't know until we know it. Follow the rivers. See where they meet for real. We follow the breadcrumbs all the way to Joan.

---

## Task 1: Update editorial_standards.md
- **Status:** DONE (2026-09-07)
- **Depends on:** NONE
- **Priority:** HIGHEST — all other tasks reference these rules
- **What was done:**
  - Added §6 Search Completeness Rule
  - Added §7 Search Direction Bias Check
  - Committed to `methodology/editorial_standards.md`

## Task 2: Create universal disclaimer block
- **Status:** DONE (2026-09-07)
- **Depends on:** NONE
- **Priority:** HIGHEST — needed before any page restructure
- **What was done:**
  - Created `methodology/universal_disclaimer.md` with finalized disclaimer text
  - Text authored by archive owner

## Task 3: Foundation file fixes
- **Status:** DONE (2026-09-07) — verified by grep, see Appendix A of the audit report
- **Depends on:** NONE
- **Priority:** HIGH
- **What was done:**
  - **agent_orientation.md** — DONE (2026-09-07) — canonical onboarding file, NEGATIVE_LOG, Mss461, AI transparency section.
  - **README.md** — DONE (2026-09-07) — full rewrite with mandatory reading pointer.
  - **index.html** — DONE (2026-09-07) — Model H card added after Model G; Law 7 (No Trust Without Evidence) added to laws list. Law-count phrasing and the mother-clause "suspended" language were already correct as of this session.
  - **about.html** — DONE (2026-09-07) — Law 7 (No Trust Without Evidence) added to laws list.
- **Verification note:** A 2026-09-07 file-vs-claim audit found the prior "DONE" mark on index.html and about.html was false — Model H and Law 7 were claimed added but were not present in either file. This entry replaces that false claim; the two missing edits were made and re-verified by grep (`Model [A-H]` returns A–H in index.html; `No Trust Without Evidence` present in both HTML files) on 2026-09-07.
- **Where to find what you need:** Root of repo
- **Done when:** All four files updated, committed — met.

## Task 4: Restructure all people pages — DUAL PASS
- **Status:** DONE (2026-09-09) — verified by grep this session, see verification block below
- **Depends on:** Tasks 1, 2 (need format and disclaimer ready) — ✅ BOTH DONE
- **Priority:** HIGH
- **What to do:**
  - Pass A: Apply universal page format to each people .md (Disclaimer → What We Know → What We Don't Know → Connections → Where To Look Next → Search Log). Add provenance tags. Strip interpretive framing. Standardize each page's "Laws apply throughout" header line to say "Multi Agent Laws" (not "Seven Laws," not "MULTI AGENT Laws," no numeral) per the 2026-09-07 naming standard above.
  - Pass B: While page is open, extract one concrete search lead driven by the page's own content. Add to search log with ❌ NOT SEARCHED tags for unchecked record types.
  - Universal page format:
    ```
    # [Name / Subject]
    ## Disclaimer
    [Universal block from Task 2]
    ## What We Know
    [Sourced claims only. Tagged: 📔 PRIMARY, 📚 SECONDARY, 🌐 TERTIARY, ⚠️ AI-SOURCED]
    ## What We Don't Know
    [Honest blanks — research directions, not failures]
    ## Connections
    [Documented overlaps. No interpretation — "X appears in the same record as Y"]
    ## Where To Look Next
    [Specific records/archives driven by findings, not theory]
    ## Search Log
    Date | Tool/Agent | What was searched | What was found | What was NOT searched
    ```
  - **⚠️ Correction (2026-09-07 audit):** `joan_unknown_greene.md` does not exist in `/people/` and `anashuecot.md` does not exist either. Confirm with Lem whether Joan/Anashuecot content is intentionally kept in `evidence/joan_verified_facts.md` and `theory/joan_firewall.md` instead of a `/people/` page (deliberate) or a gap (oversight) before checking this box against a file that isn't there.
  - **If interrupted:** Each page is its own sub-task. Status as of 2026-09-09:
    - [x] All 20 person pages in /people/ (benjamin, daniel, edward, edward_greenman, elizabeth_wife_of_james, george_havens, george_vaughan, henry_greene, henry_tibbitts, james, John_Nawham, john_greene_newport, john_greene_occupessuatuxet, john_greene_potowomut, john_greene_quidnessett, john_greene_son_of_john, john_greene_warwick, joseph_clark_francis_brinley, sarah_greene_flounders, thomas_gould)
    - [ ] joan_unknown_greene.md — **file does not exist; owner question from 2026-09-07 audit still open (deliberate vs. gap)**
    - [ ] anashuecot.md — **file does not exist; same open owner question**
- **What's already done (corrected 2026-09-07 — was recorded as "Nothing," which was false):** Compliance audit across the 23 files in /people/ (20 person pages + README.md, two-john-firewall.md, five_john_primary_source_trail.md) found:

  | Required section | Files conforming |
  |---|---|
  | `## Disclaimer` (as its own heading, vs. raw top blockquote) | 0 / 23 |
  | `## What We Know` | 12 / 23 |
  | `## What We Don't Know` | 0 / 23 |
  | `## Connections` | 0 / 23 |
  | `## Where To Look Next` | 0 / 23 |
  | `## Search Log` | 0 / 23 |

  Practical read: this is a heading-and-reflow job on the 12 pages that already have "What We Know" content, not authorship from scratch on all 23. `## Search Log` is missing everywhere (0/23) and is the one Task 6 depends on entirely — prioritize that section first across all pages before doing a full Pass A/B on every page.

  **✅ VERIFIED DONE 2026-09-09 (Kimi/Copilot, this-session grep):** all 20 person pages carry all six universal sections (Disclaimer, What We Know, What We Don't Know, Connections, Where To Look Next, Search Log), a `## Discovery Key` search-bot block (added to the format by owner directive 2026-09-09 — decision log D-010), and the standardized "The Multi Agent Laws apply throughout" header. Every Search Log carries the restructure row plus one Pass B ❌ NOT SEARCHED lead. Verification: per-file grep of all 7 section headings + header line — 20/20 OK. Framework docs (README.md, two-john-firewall.md, five_john_primary_source_trail.md) intentionally exempt from person-page format. The audit table above is preserved as the historical snapshot it was.
- **Where to find what you need:** All files in /people/
- **Done when:** All people pages restructured with disclaimer, search log, provenance tags. Recon leads extracted.

## Task 5: Create 5 John separation pages — simultaneous backward mining
- **Status:** NOT STARTED
- **Depends on:** Tasks 1, 2 (need format and disclaimer) — ✅ BOTH DONE
- **Priority:** HIGH — equal to Task 4, can run in parallel
- **What to do:**
  - Create all 5 simultaneously. Same universal format. Same disclaimer. Same search log. Same provenance tags. No head start for any.
  - Build each page BY searching — the backward mining IS the research.
  - Document collision points honestly: "this record could be either" gets flagged, not assigned.
  - **⚠️ DO NOT EXECUTE THIS FILE LIST AS WRITTEN.** A 2026-09-07 file-vs-claim audit found two problems, both unresolved — see full report in `methodology/ai_provenance.md` (2026-09-07 entry):
    1. The DeepSeek 2026-09-06 note below ("files do not exist") is **false** — 4 of 5 already exist. Corrected state:

    | Queue filename | Repo file | Lines | Substance |
    |---|---|---|---|
    | `john_greene_warwick_surgeon.md` | `john_greene_warwick.md` *(filename differs — see below)* | 84 | Substantive |
    | `john_greene_quidnessett.md` | present | 170 | Substantive |
    | `john_greene_potowomut.md` | present | 18 | Stub |
    | `john_greene_son_of_john.md` | present | 15 | Stub |
    | `john_greene_occupessuatuxet.md` | present | 6 | Placeholder only |

    2. **Naming/identity collision, unresolved:** the existing `john_greene_warwick.md` documents "Major John Greene of Occupasuetuxet," son of the Surgeon (born 1620, d. 1708) — this matches Firewall **III** (John Jr of Warwick) in `methodology/agent_orientation.md`, not Firewall I (the Surgeon himself, d. 1658/9, no page yet). Its own text uses "Occupasuetuxet" as an epithet for this same man. The queue's proposed `john_greene_occupessuatuxet.md` would therefore likely duplicate `john_greene_warwick.md`'s subject rather than cover a distinct person. Separately, the queue's 5-file list does not match the Firewall's 5 identities: Newport (Firewall IV, page already exists, 77 lines, not listed here) and Kingstown (Firewall V, no page, not listed here — and per the Firewall, Kingstown may be an alias of Our John, arguably the most decision-relevant unresolved identity in the archive) are both absent from this task's file list.
    - **This is a genealogical call, not a mechanical one — needs Lem's confirmation before the file list below is trustworthy.** Recommended (not yet applied) rewrite of the file list to track the Firewall directly:
      - [ ] `john_greene_warwick_surgeon.md` — Firewall I, the Surgeon (d. 1658/9) — genuinely new, no existing page
      - [x] `john_greene_quidnessett.md` — Firewall II, Our John — exists (170 lines), restructure to universal format only
      - [ ] rename/reframe `john_greene_warwick.md` → Firewall III, John Jr of Warwick / Occupasuetuxet — exists (84 lines) under a name that collides with the proposed occupessuatuxet.md; needs a rename decision, not a new page
      - [x] `john_greene_newport.md` — Firewall IV — exists (77 lines), was missing from the original task list entirely
      - [ ] Firewall V, John of Kingstown — no page exists under any name; genuinely missing and unflagged by the original task
      - `john_greene_potowomut.md`, `john_greene_son_of_john.md`, `john_greene_occupessuatuxet.md` — none of these three map cleanly onto a Firewall slot; each is currently an open question note (potowomut: unresolved whether real distinct person or a reused location label; son_of_john: unresolved whether Surgeon's son or Lt. John²; occupessuatuxet: 6-line placeholder, likely = Firewall III per above). Keep them as scratch/open-question pages rather than folding them into the 5-slot Firewall list until Lem confirms each is (or isn't) a distinct person.
  - **Note (superseded):** ~~Items were previously marked [x] in error. DeepSeek audit (2026-09-06) confirmed these files do not exist in the repo. Status corrected to [ ] on 2026-09-07.~~ This claim was itself false — see corrected state above. Logged as a failed AI claim in `methodology/ai_provenance.md`.
- **What's already done:** five_john_primary_source_trail.md exists but is a combined doc, not individual pages. 4 of 5 originally-listed files already exist (see table above) but none carry the universal page format or a search log.
- **Where to find what you need:** /people/, /research/
- **Done when:** All 5 Firewall identities have pages in universal format with initial backward mining notes; naming/identity collision above resolved by Lem first.

## Task 6: Compile recon queue from Tasks 4–5
- **Status:** NOT STARTED
- **Depends on:** Tasks 4, 5
- **Priority:** MEDIUM — this is the bridge to active research sessions
- **What to do:** Collect all search leads extracted during Tasks 4–5. Organize into a prioritized research queue. Apply bias check: are these all English-language colonial-framework leads? What's missing?
- **What's already done:** Nothing
- **Where to find what you need:** Search logs on every restructured page
- **Done when:** research_queue/ has a prioritized, bias-checked list of next searches

## Minor / Low Priority — Terminology drift (flagged 2026-09-07, not fixed)
## Naming standard (added 2026-09-07, per archive owner): the public-facing and instructional name for the rule set is always **"Multi Agent Laws"** — never "Seven Laws," "Three Laws," or a numeral. The count is deliberately not surfaced anywhere, because the laws are still evolving; law-list `<ol>` elements should render as unordered lists so no number is implied. `theory/three_laws.md` keeps its filename and internal content untouched — do not rename it or edit its law text, only refer to it via link text that says "Multi Agent Laws."

**Done 2026-09-07:** all 5 site-facing HTML pages (index.html, about.html, context.html, contribute.html, analysis.html) and the core instructional docs (README.md, README_FOR_EXTERNAL_AGENTS.md, AGENT_GUARDRAILS.md, CONTRIBUTING.md, methodology/editorial_standards.md, methodology/universal_disclaimer.md, methodology/integrity_framework.md, contamination/README.md) — standardized to "Multi Agent Laws," law lists converted from numbered `<ol>` to unordered `<ul>` on index.html and about.html.

**Not yet done — still says "Seven Laws" or is otherwise unstandardized:** dated session/agent logs (`agents/*`, `research/*`, `research_findings/*`), `decision_log.md`, `contradictions/*`, `evidence/*`, `validation/*`, `roadmap/*`, `pending_review/*`, `primary_sources/NEGATIVE_LOG.md`, `research_queue/*`, `theory/source_spine.md`, `methodology/kimi_hostile_audit.md`, `methodology/ai_provenance.md`, `methodology/inference_audit.md`, `methodology/git_audit_checklist.md`, `methodology/name_variant_registry.md`, and the individual `/people/*.md` pages (several say "Seven Laws" or "MULTI AGENT Laws" inconsistently in their per-page header). Left alone deliberately this pass — most of these are dated session records, and the people pages are already queued for a full rewrite under Task 4, where the header line should be standardized as part of that pass rather than touched twice.

## Task 6.5: Next-page fetch tooling (added 2026-09-07)
- **Status:** BUILT, UNTESTED — needs a first real run before it's trusted
- **Depends on:** NONE
- **Priority:** MEDIUM — accelerates ongoing research, doesn't gate other tasks
- **What was done:** Built `tools/next_page/` — automated "next page" fetching for the 17
  Internet Archive volumes already cited in the repo (Track A), plus documentation of why
  the FamilySearch deed-book images (008204949-*) can't be automated the same way and what
  to do instead (Track B). GitHub Action at `.github/workflows/fetch-next-page.yml`, manual
  trigger only, opens a PR — never auto-commits to a published page.
- **What's NOT done / needs attention first:**
  - `tools/next_page/sources.yml` has all 17 volumes with `last_known_seq: null` — needs a
    human pass filling in the actual last-checked page for each, from existing citations, before
    the fetcher can run against any of them.
  - The IIIF manifest URL pattern (`iiif.archive.org/iiif/{id}/manifest.json`) was written from
    documented archive.org IIIF support but has not been live-tested against any of this
    archive's specific 17 identifiers — first run should be treated as a test, not a trusted fetch.
  - `ANTHROPIC_API_KEY` repo secret needs to be set for the AI triage step to run; without it,
    fetching + logging still works, just skips the relevance triage.
- **Where to find what you need:** `tools/next_page/README.md` is the entry point.
- **Done when:** At least one successful test run against a volume with a filled-in
  `last_known_seq`, confirmed to produce a real page image in `images/_pending_review/`.

## Task 6.75: Truth-quest search synthesis and next actions (added 2026-09-07)
- **Status:** ACTIVE — synthesis only; no search below is marked complete by this card
- **Depends on:** Tasks 4–6 remain incomplete. This card does not override their statuses.
- **Priority:** HIGHEST ACTIVE SEARCH CARD
- **Governing laws:** Law 1 (hold contradictions open), Law 3 (test every model before
  disqualification), Law 5 (check every jurisdiction), Law 6 (no centering), and Law 7
  (no promotion without the document). Search direction must also satisfy `editorial_standards.md`
  §§6–7 and record what was not searched.

### Current evidence boundary

The archive currently has four defensible Joan facts, all with an AI-transcription caveat:

1. Joan is named as John Greene's wife in the March 1682 deed.
2. A life annuity is reserved to her; the amount and exact wording remain under review.
3. Joan does not sign or mark the confirmed 1682 deed image.
4. No other record of Joan has been located in the searches listed in `evidence/joan_verified_facts.md`.

The Pawtuxet deed citation is broken and remains suspended. The five-John firewall is useful
for preventing conflation, but its DNA and lineage inputs still require independent source
verification. The archive must therefore search for Joan's identity and documentary context,
not search for confirmation of a preferred origin.

### Ordered next searches

| Rank | Search | Record families / repositories | Question tested | Promotion condition |
|---|---|---|---|---|
| 1 | Recover the orphan Pawtuxet citation | RI State Archives, Providence colonial deed books, Warwick/North Kingstown clerks, RIHS MSS 1210, FamilySearch films, Providence Vol. 14 | Does the May 1682 deed exist, and what volume/series does “Vol. VII, pp. 177–178” mean? | Original image or authoritative catalog record; otherwise log a scoped negative and keep S-007 suspended. |
| 2 | Verify the March 1682 manuscript | FamilySearch DGS 008204949 Images 9–12; compare Image 10 with Worth and F.L. Greene | Exact annuity amount, parties, formula, witnesses, and whether any clause concerns Joan's mother | Human inspection of the image with page/line or image anchor; AI text remains working transcription. |
| 3 | Resolve the five-John identity firewall | 1658 Pawtuxet signing cluster, 1671 freeman list, 1678 council order, 1679 certificate, 1682 deed, 1685 deed, full witnesses and land descriptions | Which John appears in each record: Surgeon, Quidnessett, Warwick/Occupasuetuxet, Newport, or Kingstown? | Full record text plus at least two independent identity anchors, not name-only matching. |
| 4 | Trace the earliest Pawtuxet citation | F.L. Greene 1894, Austin 1887, Updike 1907/1937, Bates 1918–19, later compilations | Is the citation independent, circular, or a transcription error introduced by a later compiler? | Earliest citable source and explicit citation chain. |
| 5 | Test Irish/Scottish and servant models | Bristol servant registers, Cromwellian transportation lists, Irish/Ulster and Scottish migration records, apprenticeship/bond records, port books, New England court and probate records | Can any record connect Joan, a plausible alias, or the Quidnessett household to Ireland, Ulster, Scotland, or servitude? | A contemporaneous record naming the person or a bounded household link; surname resemblance is insufficient. |
| 6 | Test enslavement/captivity and status models | King Philip's War captivity/deportation records, RI/Massachusetts/Connecticut disposal records, manumissions, probate inventories, court records, church records | Is there documentary evidence for enslaved, captive, servant, or free status, without inferring from race or absence? | Exact source language plus context separating colonial legal category from lived identity. |
| 7 | Search Indigenous and non-English knowledge systems | Narragansett/Niantic community histories, Indigenous-authored scholarship, language/name studies, oral-history protocols, archaeological and material-culture collections | What names, kinship terms, places, or documentary absences are invisible in English colonial searches? | Repository or community-authorized source with provenance and cultural-access notes; do not extract restricted knowledge. |
| 8 | Search women’s and household records sideways | Widowhood, dower, annuity payments, probate, guardianship, church, midwife, neighbor, witness, and children’s records | Can Joan be located through household relationships rather than her own name? | Record names Joan or an identity-linked household with a clear date/place bridge. |
| 9 | Search maritime and trade networks | Newport/Boston port records, merchant correspondence, Richard Smith trading-post records, ships, customs, seamen, coastal court cases | Could movement through the trading network explain Joan's appearance and documentary silence? | Dated record tied to the household or a documented associate; general regional trade context is not identity proof. |
| 10 | Build the regional geography baseline | Quidnessett, Cocumscussoc, Pawtuxet, Warwick, Kingstown, Narragansett place-name variants; maps, surveys, deeds, archaeology | Which place labels refer to the same location, and which mark distinct jurisdictions or communities? | Map/deed anchor with date and repository; never use modern boundaries as a proxy for colonial identity. |

### Required search output

Each completed search writes a dated entry to the relevant page's `## Search Log` and, when
machine-generated, a candidate record under `data/research/` with:

- repository, stable identifier, URL, access date, and page/image anchor;
- exact query, date range, jurisdiction, and record type searched;
- what was found and what was not searched;
- identity collisions and alternative explanations;
- `PENDING_HUMAN_REVIEW` until a human inspects the original or authoritative record.

The daily multi-perspective sweep is a discovery aid, not a verification pass. Its results must
feed this queue only after deduplication, source-level review, and hostile challenge. Agreement
between agents is not corroboration.

### Bias check before closing this card

The current queue is strongest on digitized English-language colonial records and weakest on:

- Indigenous-authored or community-governed sources;
- material culture, archaeology, and landscape evidence;
- Irish/Scottish migration and servant-status records outside Rhode Island;
- women’s household, church, widowhood, and annuity records;
- maritime and port records connecting the Narragansett region to wider movement.

Do not mark this card DONE until each gap has either a documented search, a scoped negative result,
or an explicit access/permissions barrier recorded in the queue.

## Task 7: Phase 7+ (future — do not start before Tasks 1–6 are DONE)
- **Status:** IN PROGRESS (some items completed early during framework build)
- **Depends on:** ALL above
- **What to do:**
  - ✅ AI provenance log (methodology/ai_provenance.md) — DONE 2026-09-07
  - Source spine §1 restructure — remove thesis framing
  - Repo description update (browser needed)
  - Workflow YML cleanup
  - HTML: Trust But Verify banners
  - PR #12 discussion
  - Context expansion pages (trade hub, regional politics, immigration, religious landscape, maritime, the sloop, Smith's trading post)
  - Replit's good ideas: search page with deterministic ranking, claim-level provenance model, workflows to check-and-PR, asset validation in CI — all built around THIS archive's provenance tag system, not generic schemas
- **Done when:** Each sub-item gets its own task card when we reach this phase

---

## Provenance Tags Reference
- 📔 PRIMARY — archive has read the original
- 📚 SECONDARY — archive has read a published transcription
- 🌐 TERTIARY — internet source, not independently verified
- ❌ NOT SEARCHED — this record type has not been checked
- 🔍 SEARCHED, NOT FOUND — checked [specific source], not present
- ⚠️ AI-SOURCED — claim originated from an AI tool, verification required
