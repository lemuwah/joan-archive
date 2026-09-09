# Editorial Standards

**Status:** Active — governs all public-facing content and analysis pages.  
**Restored:** 2026-09-06 (was missing/404 per Kimi audit)  
**Last updated:** 2026-09-07 — added §6 Search Completeness Rule, §7 Search Direction Bias Check (Task 1)  
**Companion files:** `AGENT_GUARDRAILS.md`, `methodology/Epistemology.md`, `CORRECTIONS.md`

---

## 1. Verified Facts About Joan

This is the complete list. Nothing else qualifies.

| # | Fact | Source | Tag |
|---|------|--------|-----|
| 1 | Joan is named as wife of John Greene in a March 1682 land deed | Worth abstract + human-verified Image 10 source; detailed reading paleography-pending | SOURCE VERIFIED / PALEOGRAPHY PENDING |
| 2 | A life annuity is reserved to her (amount unverified — Worth says 30 shillings, manuscript read may differ) | Worth abstract + human-verified Image 10 source; detailed reading paleography-pending | SOURCE VERIFIED / PALEOGRAPHY PENDING (amount OPEN QUESTION) |
| 3 | No Joan signature or mark is visible in the checked Image 10 crop | Human visual check of Image 10 crop; full instrument requires expert review | SOURCE VERIFIED / PALEOGRAPHY PENDING |
| 4 | No other record of Joan has been located | Negative search result (as of Sep 2026) | Methodological |

**Rule:** Only these four facts may appear on `index.html` as statements about Joan. Everything else belongs on `analysis.html` with appropriate status tags.

---

## 2. Suspended Claims

See `evidence/suspended_items.md` for the complete list with reasons and resolution paths.

---

## 3. Status Tags

The canonical tag system is defined in `methodology/integrity_framework.md`. The authoritative tags are:

- **PROOF** — Primary source seen, page cited
- **PROOF — AI TRANSCRIPTION** — Original image read by AI, disclaimer attached
- **PLAUSIBLE** — Scholar cites it or logic holds, not personally verified
- **DISCREDITED** — Tested and failed

Legacy tags in older files (PROVEN/PROBABLE/UNVERIFIED/NULL/SUSPENDED) are recognized as equivalent but the canonical system governs.

**Tag-change documentation rule:** Every status tag change — promotion, demotion, or lateral reclassification — must be documented with: (a) which source triggered the change, (b) the date of the change, (c) who or what agent made the change, and (d) what the source actually says. Log the change in `CORRECTIONS.md` and update the relevant contradiction file in `contradictions/` if applicable. Undocumented tag changes violate Law 7.

---

## 4. Source Hierarchy

| Tier | What | Example |
|---|---|---|
| 1 | Original manuscript, personally viewed | FamilySearch DGS image |
| 2 | Published verbatim transcription by named scholar | Worth abstract, Bartlett |
| 3 | Published summary/paraphrase by named scholar | Bates (1918), F.L. Greene |
| 4 | Secondary compilation, genealogy database | Austin, WikiTree, Ancestry |
| 5 | AI-generated, unsourced web content | ChatGPT output, alfredgibbs.com |

---

## 5. Content Placement Rules

| Page | What goes here |
|---|---|
| `index.html` | Four verified facts only. No interpretation. No hypotheses. |
| `analysis.html` | Open hypotheses (Models A–H), evidence mapping, stress tests |
| `context.html` | Timeline, geography, colonial jurisdiction. Facts only, tagged. |
| `contribute.html` | How to help, negative space log, what hasn't been searched |
| `about.html` | Methodology, Multi Agent Laws, corrections, AI checklist |

---

## 6. Search Completeness Rule

**Added:** 2026-09-07 (Task 1)

Every `.md` page in `/people/`, `/context/`, and `/research_queue/` must maintain a search log documenting:
- Which tools searched which record types
- What was found
- What was NOT searched

A tool that searches one category and doesn't document categories it didn't search has introduced bias by omission. The ❌ NOT SEARCHED tag is an honest map of where to go next, not a failure.

**Format:**

```
## Search Log
| Date | Tool/Agent | What was searched | What was found | What was NOT searched |
|------|------------|-------------------|----------------|----------------------|
```

Every page must include this table. An empty "What was NOT searched" column is a red flag — every search has blind spots.

---

## 7. Search Direction Bias Check

**Added:** 2026-09-07 (Task 1)

When any agent recommends "where to look next," the recommendation must be checked for bias toward digitized, English-language, colonial-framework sources.

The page must ask:
- What record types exist that this agent might not know to suggest?
- What would a Narragansett historian, a maritime historian, an archaeologist, a linguist, a material culture specialist look for that a genealogist wouldn't?

This check applies to all recommendations in `/research_queue/`, all "Where To Look Next" sections in `/people/` pages, and all agent session logs that suggest next steps.

**Rule:** A recommendation list composed entirely of English-language colonial archives is not wrong, but it IS incomplete, and the incompleteness must be flagged.

---

*Maintained under the Multi Agent Laws of the Joan Archive.*
