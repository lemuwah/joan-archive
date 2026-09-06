# Editorial Standards

**Status:** Active — governs all public-facing content and analysis pages.  
**Restored:** 2026-09-06 (was missing/404 per Kimi audit)  
**Companion files:** `AGENT_GUARDRAILS.md`, `methodology/Epistemology.md`, `CORRECTIONS.md`

---

## 1. Verified Facts About Joan

This is the complete list. Nothing else qualifies.

| # | Fact | Source | Tag |
|---|------|--------|-----|
| 1 | Joan is named as wife of John Greene in a March 1682 land deed | Worth abstract + Image 10 AI transcription | PROOF — AI TRANSCRIPTION |
| 2 | A life annuity is reserved to her (amount unverified — Worth says 30 shillings, manuscript read may differ) | Worth abstract + Image 10 AI transcription | PROOF — AI TRANSCRIPTION (amount OPEN QUESTION) |
| 3 | Joan does not sign or mark the 1682 deed | Image 10 AI transcription | PROOF — AI TRANSCRIPTION |
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
| `analysis.html` | Open hypotheses (Models A–G), evidence mapping, stress tests |
| `context.html` | Timeline, geography, colonial jurisdiction. Facts only, tagged. |
| `contribute.html` | How to help, negative space log, what hasn't been searched |
| `about.html` | Methodology, Seven Laws, corrections, AI checklist |

---

*Maintained under the Seven Laws of the Joan Archive.*
