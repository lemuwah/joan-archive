# Editorial Standards

**Status:** Active — governs all public-facing content and analysis pages.  
**Added:** 2026-09-03  
**Companion files:** `AGENT_GUARDRAILS.md`, `methodology/Epistemology.md`, `CORRECTIONS.md`

---

## 1. Verified Facts About Joan

This is the complete list. Nothing else qualifies.

| # | Fact | Source | Tier |
|---|------|--------|------|
| 1 | Joan is named as wife of John Greene in a March 1682 land deed | Worth abstract, RI Land Evidences | Tier 1 — Primary abstract |
| 2 | A life annuity of 30 shillings per year is reserved to her | Worth abstract, RI Land Evidences | Tier 1 — Primary abstract |
| 3 | No other record of Joan has been located | Negative search result | Methodological |

**Rule:** Only these three facts may appear on `index.html` as statements about Joan. Everything else belongs on `analysis.html` with appropriate status tags.

---

## 2. Suspended Claims

These were previously stated or implied across the archive. All are suspended until the manuscript (FamilySearch DGS 008204949, images 9–12) is read.

| Claim | Why suspended | What would resolve it |
|-------|---------------|----------------------|
| "Joan signed with a mark" | No source says this for the March 1682 deed | Manuscript examination |
| "Joan gave consent" | Worth doesn't mention consent; Bates's "and his wife Joan deeded" is his narration, not a quote | Manuscript examination |
| "Free and voluntary consent" | May come from the suspended Pawtuxet deed (see CORRECTIONS.md #1) | Pawtuxet deed verification OR manuscript examination |
| "Or to her mother if she survive" | Not in any source we hold; see `contradictions/mother-clause-wording.md` | Manuscript examination |
| Joan as co-grantor | Bates's summary language; not confirmed by Worth abstract | Manuscript examination |
| Joan as legal actor | Inference from co-grantor assumption | Manuscript examination |

**Rule:** Suspended claims must not appear on any public-facing page without a ⚫ SUSPENDED tag and a cross-reference to this file.

---

## 3. Status Tags

Used throughout the archive:

- 🟢 **VERIFIED** — Confirmed by primary source citation. Can appear on `index.html`.
- 🟡 **PROBABLE** — Supported by multiple sources but not explicitly confirmed. `analysis.html` only.
- 🟡 **OPEN HYPOTHESIS** — Plausible, testable, not yet confirmed or eliminated. `analysis.html` only.
- ⚫ **SUSPENDED** — Previously stated but source support withdrawn or insufficient. Must not appear on `index.html` without the tag.
- 🔴 **ELIMINATED** — Disproven by primary sources. Retained in the record for transparency.
- 📖 **EXTERNAL INTERPRETATION** — Derived from non-Indigenous academic sources. Not verified by Narragansett authority.
- ⚠️ **CORRECTION** — A claim that was wrong and has been fixed. See `CORRECTIONS.md` for details.

---

## 4. Source Hierarchy

When sources conflict, this hierarchy governs:

1. **Manuscript original** — the deed itself (unread as of Sep 2026)
2. **Primary abstract** — Worth's transcription in RI Land Evidences
3. **Contemporary secondary** — Bates (RIHS Collections), Potter (1835), Chapin (1931)
4. **Later secondary** — F.L. Greene (1903), Austin genealogies
5. **Compilations / databases** — Ancestry, FamilySearch trees, Find A Grave
6. **AI-generated content** — never a source; always requires independent verification

**Rule:** A lower-tier source cannot override a higher-tier source. When a secondary source claims something the primary abstract does not contain, the claim is ⚫ SUSPENDED until the manuscript is read.

---

## 5. Content Placement Rules

### index.html (the reading room)
- Only 🟢 VERIFIED facts about Joan
- No identity claims
- No urgency framing
- No personal names without consent
- Competing models listed equally with no centering
- Narragansett perspectives: held, not filled
- Indigenous review disclosure

### analysis.html (the hypothesis space)
- All open models with equal treatment
- Each model gets: evidence for, evidence against, what would confirm, what would eliminate
- All status tags visible
- Inferences clearly labeled as inferences
- Cross-lens synthesis by the reader, not the archive

### context.html (the historical setting)
- Colonial and Narragansett context from documented sources
- All Narragansett governance descriptions tagged 📖 EXTERNAL INTERPRETATION unless from Narragansett sources
- No synthesis with Joan's identity

### about.html (the methodology)
- Review status disclosure
- Epistemological stance (see `Epistemology.md`)
- Corrections policy
- How to contribute

---

## 6. The Inference Test

Before any claim appears on a public page, ask:

> **Can I point to one specific document that says this?**

- **Yes** → cite it, tag 🟢 VERIFIED or 🟡 PROBABLE with the source
- **No, but multiple documents imply it** → `analysis.html` with 🟡 tag, present each document separately, label the connection as inference
- **No** → it doesn't go on a public page

---

## 7. The Transcription Rule

From `AGENT_GUARDRAILS.md` §1, restated here for emphasis:

> A transcribed narrative is not a verbatim quote. Worth's abstract describes the deed. Bates's summary describes the deed. Neither IS the deed. Only the manuscript is the deed.

Quotation marks may only be used around text when the source itself uses those exact words. Paraphrasing by a secondary author is cited as "[Author] describes..." or "[Author] states that..." — never presented as the deed's own language.

---

*This file is referenced in `AGENT_GUARDRAILS.md` and `README_FOR_EXTERNAL_AGENTS.md`.*  
*Maintained under the Five Laws of the Joan Archive.*
