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
- **Status:** NOT STARTED
- **Depends on:** Tasks 1, 2 (need format and disclaimer ready) — ✅ BOTH DONE
- **Priority:** HIGH
- **What to do:**
  - Pass A: Apply universal page format to each people .md (Disclaimer → What We Know → What We Don't Know → Connections → Where To Look Next → Search Log). Add provenance tags. Strip interpretive framing.
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
  - **If interrupted:** Each page is its own sub-task. Mark which are done below:
    - [ ] joan_unknown_greene.md — **file does not exist yet, see correction above**
    - [ ] john_greene_quidnessett.md
    - [ ] anashuecot.md — **file does not exist yet, see correction above**
    - [ ] (list remaining pages from /people/ directory when starting)
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
Three names in active use for the same rule set: "MULTI AGENT Laws" (index.html, about.html, john_greene_warwick.md), "the Seven Laws" (john_greene_newport.md, universal_disclaimer.md footer), and the filename `theory/three_laws.md` itself, which now contains seven laws, not three. Low severity — did not touch, since renaming the file would need every inbound link updated. Worth a pass whenever Task 7's "Repo description update" is picked up.

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
