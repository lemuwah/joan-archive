# Joan Archive — Task Queue

## How to use this file
Any AI helper working on this archive: read `methodology/agent_orientation.md` first. Then come here. Pick the highest-priority NOT STARTED task whose dependencies are DONE. Execute it. Update the status when finished. If interrupted mid-task, update "What's already done" before stopping.

Laws, models, and facts evolve as research progresses. Do not assume they match your last session. Re-read before working.

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
- **Status:** IN PROGRESS
- **Depends on:** NONE
- **Priority:** HIGH
- **What to do:**
  - **index.html** — Replace specific law count with "governed by the Laws of the Joan Archive." Add Model H to models section. Add Law 7 to list. Fix "What We Do Not Know" inconsistency (mother clause suspended, not unknown).
  - **agent_orientation.md** — ✅ DONE (2026-09-07) — Made canonical onboarding file. Added NEGATIVE_LOG, Mss461, AI transparency section.
  - **README.md** — ✅ DONE (2026-09-07) — Full rewrite with mandatory reading pointer.
  - **about.html** — Add Law 7 to Laws list.
- **What's already done:** agent_orientation.md, README.md, index.html (model count + Model H + Law 7), about.html (Law 7 added)
- **Where to find what you need:** Root of repo
- **Done when:** All four files updated, committed

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
  - **If interrupted:** Each page is its own sub-task. Mark which are done below:
    - [ ] joan_unknown_greene.md
    - [ ] john_greene_quidnessett.md
    - [ ] anashuecot.md
    - [ ] (list remaining pages from /people/ directory when starting)
- **What's already done:** Nothing
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
  - Files:
    - [ ] people/john_greene_warwick_surgeon.md
    - [ ] people/john_greene_son_of_john.md
    - [ ] people/john_greene_potowomut.md
    - [ ] people/john_greene_occupessuatuxet.md
    - [ ] people/john_greene_quidnessett.md (already exists — restructure to match)
  - **Note:** Items were previously marked [x] in error. DeepSeek audit (2026-09-06) confirmed these files do not exist in the repo. Status corrected to [ ] on 2026-09-07.
- **What's already done:** five_john_primary_source_trail.md exists but is a combined doc, not individual pages
- **Where to find what you need:** /people/, /research/
- **Done when:** All 5 pages exist with universal format, initial backward mining notes, collision points flagged

## Task 6: Compile recon queue from Tasks 4–5
- **Status:** NOT STARTED
- **Depends on:** Tasks 4, 5
- **Priority:** MEDIUM — this is the bridge to active research sessions
- **What to do:** Collect all search leads extracted during Tasks 4–5. Organize into a prioritized research queue. Apply bias check: are these all English-language colonial-framework leads? What's missing?
- **What's already done:** Nothing
- **Where to find what you need:** Search logs on every restructured page
- **Done when:** research_queue/ has a prioritized, bias-checked list of next searches

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
