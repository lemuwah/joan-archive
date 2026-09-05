# Integrity Framework

**Status:** Active — governs all evidence handling across the archive.  
**Added:** 2026-09-05  
**Authority:** Equal to the Seven Laws.

---

## The Three Questions

Before any claim is committed, ask:

1. **Can I see it?** — Is there a document I can point to, or am I repeating something I heard?
2. **Does it actually say this?** — Am I reading what's there, or what I want to be there?
3. **Am I sure?** — If not, say so.

---

## The Three Tags

Every claim in the archive carries one of these:

- **PROOF** — Primary source exists. Page number, repository, image reference. The document says this thing in these words.
- **PROOF — AI TRANSCRIPTION** — We read the original image. AI transcription. Working authority, not final authority. Disclaimer attached.
- **PLAUSIBLE** — A named scholar cites it, or multiple secondary sources agree, or the logic holds but the original document hasn't been personally verified.
- **DISCREDITED** — Tested and failed. Source doesn't say what was claimed, citation is broken, chain leads to fabrication, or contradicting primary evidence exists.

No tag = unprocessed. Sits in intake until tagged. No claim reaches the site without a tag.

### AI Transcription Disclaimer

Every AI transcription in the archive gets this footer:

> *Transcribed by AI from manuscript image (FamilySearch DGS 008204949, Image 10). Working research read — not an expert paleographic verification. Verify against the original. This archive does not claim transcription authority.*

### Promotion/Demotion Rules

- **PLAUSIBLE → PROOF:** Found the primary source, can cite it, document says what was claimed (exactly, not close).
- **PLAUSIBLE → DISCREDITED:** Searched and source doesn't exist, or source doesn't say what was claimed, or primary evidence contradicts it.
- **DISCREDITED → PLAUSIBLE:** New evidence reopens it. Rare. Document why.
- **PROOF never demotes** unless the original document itself is shown to be a forgery or misattributed.

---

## Current Master Tag List (Sep 5, 2026)

| Claim | Tag | Basis |
|---|---|---|
| Joan named as wife in 1682 deed | PROOF — AI TRANSCRIPTION | Image 10, DGS 008204949 |
| 30-shilling life annuity | PROOF — AI TRANSCRIPTION | Image 10 |
| "John Green Senr" designation | PROOF — AI TRANSCRIPTION | Image 10 |
| John lived 40+ years in Narragansett | PROOF | 1679 affidavit text |
| Cocumscussoc burned 1676 | PROOF | Multiple primary sources |
| Benjamin as property buyer | PROOF — AI TRANSCRIPTION | Image 10 bottom |
| Joan signed with mark | **DISCREDITED** | Image 10 — Joan does not sign |
| Joan as co-grantor | **DISCREDITED** | Image 10 — John alone in granting clause |
| "Or to her mother if she survive" | **DISCREDITED** | Image 10 reads "him or his Wife or during her natural life" |
| Joan = Anashuecot | PLAUSIBLE | Hypothesis, no document equates them |
| Pawtuxet deed (May 1682) | PLAUSIBLE | Citation chain broken but deed details consistent across secondary sources |
| Vol. VII pp. 177-178 citation | **DISCREDITED** | Searched, contains 1773 Gaspee records |
| John's death before Sept 1685 | PLAUSIBLE | Bates cites "now deceased" in Clark deed — not personally read |
| Tibbitts will names Joan's grandchildren | PROOF — AI TRANSCRIPTION | Tibbitts will 1708/proved 1713 |

---

## Source Trust Hierarchy

| Tier | What | Example |
|---|---|---|
| 1 | Original manuscript, personally viewed | FamilySearch DGS image, archival scan |
| 2 | Published verbatim transcription by named scholar | Worth abstract, Bartlett Colony Records |
| 3 | Published summary/paraphrase by named scholar | Bates (1918), F.L. Greene (1894) |
| 4 | Secondary compilation, genealogy database | Austin (1887), WikiTree, Ancestry |
| 5 | AI-generated, unsourced web content, oral tradition | ChatGPT output, alfredgibbs.com, forum posts |

**Inheritance Rule:** A conclusion can never be more trusted than its least-trusted input.

---

## The Ten Logic Rules

1. **Inheritance** — conclusion trust = weakest input trust
2. **Separation** — findings go in `evidence/`, interpretations go in `theory/`, they never share a file
3. **Null = Data** — a search that finds nothing gets the same documentation as a search that finds something
4. **Contradictions Stay** — when two sources disagree, both stay, neither deleted, contradiction documented
5. **Three-Hop Provenance** — claim → source → original in ≤3 steps; if longer, downgrade to PLAUSIBLE
6. **Model Equity** — every finding tested against ALL models (A-G for Joan, I-V for John), not just the one it seems to support
7. **AI Reads Expire** — AI transcription unverified at 90 days gets reflagged for re-examination
8. **Outside-In** — search the constellation (everyone around Joan/John), not just the target
9. **No Backfill** — never add information to a finding after the fact to make it fit a theory
10. **Plain Language** — if a claim can't be stated in one plain sentence, it's not clear enough to commit

---

## Pipeline Rules

```
New AI read → pending_review/ → human checks against image → digitization/transcriptions/
```

- No AI pass verifies another AI pass
- AI reads carry the disclaimer template
- Image 10 (DGS 008204949) is the authority for the 1682 deed until a higher-resolution or expert read supersedes it

---

## Indigenous Content Protocol

- All descriptions of Narragansett governance or cultural practice from non-Indigenous sources carry the 📖 **EXTERNAL INTERPRETATION** tag
- Content touching Indigenous identity, governance, or cultural practice passes the Tomaquag test: "Would a Narragansett scholar reading this feel their authority is respected?"
- Indigenous scholarly input carries distinct and higher weight — not folded into general feedback
- Contact initiated with Tomaquag Museum. As of Sep 2026, no formal review by Narragansett scholars has occurred.

---

## Dead-End Filter

Before committing time to a search:

**Score = Specificity × Accessibility × Joan-Relevance ÷ Time-Cost**

- High specificity + free online + direct Joan connection = GO
- Vague hunch + paid archive + tangential connection = PARK IT
- Anything scored = documented. Even parked leads stay on the research queue.
