# Kimi Hostile Search Audit — 2026-09-06

**Agent:** Kimi (Moonshot AI)
**Role:** Hostile Searcher — Tier 2 in AI Litmus Test
**Date:** 2026-09-06
**Conducted by:** Archive owner via Kimi hostile search protocol
**Purpose:** Search for what SHOULDN'T be there — contamination vectors, false claims propagating, sources that look real but aren't

---

## Methodology

Kimi was tasked with hostile searching: looking for evidence that contradicts, contaminates, or undermines the archive's claims. Unlike validation AIs (which read the repo and report what they find), Kimi searched the open web for what the archive might have missed or what might be poisoning the research.

---

## Key Findings

### Contamination Vectors Identified

1. **alfredgibbs.com** — repeats the La Mance error (Joan = Joan Beggarly / Alice Daniels daughter). No primary source cited. Propagates the wrong-John-Greene conflation.
2. **WikiTree Greene-865** — WikiTree profile for John Greene of Warwick lists "Joan" without source distinction. Conflates Warwick's John (the surgeon) with Quidnessett's John. Tree entries trace to La Mance (1904) or to each other.

### Null Results (Hostile Searches That Found Nothing)

1. **Jamestown deed mentioning Joan** — no deed found in Jamestown records naming Joan Greene
2. **NK 1695/96 deed with Joan reference** — no Joan in the Wightman or Benjamin-to-James deeds
3. **Passenger lists (any) with Joan Greene bound for New England** — NULL across all published lists searched
4. **FamilySearch DGS 008204949 images containing Joan's mark** — images not examined (access restriction); no mark claim can be verified
5. **MA Bay court records naming Joan Greene** — NULL across Shurtleff volumes
6. **Joan Beggarly as a real person in any primary source** — the name "Beggarly" comes only from Winthrop's journal referring to "the wife of one Beggerly" — a husband's surname, never a maiden name for Joan of Quidnessett

### Value of Hostile Search

Kimi's hostile approach caught two live contamination vectors (alfredgibbs.com and WikiTree) that validation-focused AIs would never look for. The null results are equally valuable — they confirm the archive's negative log entries from independent search paths.

---

## Assessment

Kimi earned Tier 2 specifically for hostile search capability. It is the recommended tool for:
- Contamination sweeps after major commits
- Checking whether false claims are still propagating on genealogy platforms
- Finding sources that LOOK authoritative but trace to La Mance or circular citation

Kimi is NOT recommended for repo validation (it doesn't follow the methodology chain the same way Tier 1 AIs do) or for structural auditing (that's Runable/DeepSeek).

---

*Maintained under the Seven Laws of the Joan Archive.*
*Law 4: No Planting — contamination caught is contamination stopped.*
