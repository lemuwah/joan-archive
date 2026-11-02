# Hostile Review Queue Packet — research_findings/2026-09-05_bates_deep_read.md

**Finding ID:** `FINDING-cf1026f626d4`
**Status:** `LAWS_FILTERED`
**Source SHA-256:** `68c0f7494b6541a50942de7f1f2b83f48d0d44646d182e220449036607611993`
**Stage purpose:** attack identity collisions, circular citations, OCR error, and unsupported inference.
**Publication rule:** This is a Laws-filtered review packet, not evidence and not an approval. AI disclaimer applies.

## Required action
Process this finding as stage `02_hostile_review`. Preserve the exact source path and hash.
Do not edit the source finding or promote any claim to PROOF.

## Image gate
Referenced images: none detected.
Images already staged in `images/_pending_review/`: none.
Referenced images already elsewhere in `images/` and not pending: none.
Referenced images not found in the archive: none.
Any newly supplied image belongs in `images/_pending_review/` until a human reviews and promotes it.

## Finding text
```markdown
> This archive documents lives lived between approximately 1600–1750 in Narragansett country (present-day Rhode Island). All records from this period were created within colonial legal systems and reflect their biases, categories, and blind spots. Every name found here — English, Narragansett, Niantic, mixed-heritage, unknown — represents a real person whose full story these records were not designed to capture. Content may include references to war, captivity, enslavement, displacement, legal coercion, and loss. These are documented realities of the period, not abstractions.
>
> All cultural and genealogical content is included for research purposes in the quest to identify Joan Unknown Greene and will be revised or removed if requested by descendant communities or tribal representatives. Search direction bias check: When an agent recommends "where to look next," ask: is this recommendation biased toward digitized, English-language, colonial-framework sources? What record types exist that this agent might not know to suggest? What would a Narragansett historian, a maritime historian, an archaeologist, a linguist look for that a genealogist wouldn't?
> # Bates Deep Read — Full Article Mapped
**Date:** 2026-09-05 (round 4)
**Source:** Bates, Louise Prosser. "John Greene of Newport and Narragansett." *Collections of the Rhode Island Historical Society*, Vol. XI, No. 3, July 1918, pp. 69–78; continued Vol. XII, No. 1, January 1919, pp. 15–25.
**Internet Archive:** https://archive.org/details/rhodeislandhistv11v12rhod
**Law 7 applied:** Bates is secondary compilation, not primary. She summarizes deeds, does not reproduce them.

---

## EVERY JOAN MENTION IN BATES — COMPLETE

| Location | Exact Wording | Context |
|----------|---------------|----------|
| XI p. 77 | "Greene and his wife **Joan** deeded to their sons, Daniel² and James², land in Quidnisset in return for thirty shillings a year paid by each of them so long as either parent lived. This was March 24, 1681/2." | The homeplace deed — our Image 10. |
| XI p. 78 | "The children of John¹ Greene and his wife **Joan** were Lieut. John² Greene of Newport; Henry² Greene of Quidnisset and 'New Gearsey'; Daniel² Greene of Quidnisset; James² Greene of Quidnisset; Benjamin² Greene of Quidnisset; Sarah² Greene, who married Thomas Flounders about 1668." | Children list. |
| XII p. 15 | "Henry (2) Greene, son of John (i) and **Joan Greene of Newport and Aquednesit or Quidneset**, was born in Newport, R. I., about 1650." | Henry's biography — gives Joan as identifier only. |
| XII pp. 24–25 | "The lines of Daniel (2) and Edward (2) Greene, sons of **John and Joan Greene of Newport and Quidneset** have not been followed out." | Closing note — Joan as identifier. |
| XII p. 25 | James identified as son of "John and **Joan Greene of Newport and Quidnisset**" | James's biography — Joan as identifier. |

**Total: 5 mentions. Zero contain any information about Joan beyond her name and role as wife/mother.**

### What Bates Does NOT Say About Joan
- ❌ No maiden name
- ❌ No parentage
- ❌ No place of origin
- ❌ No ethnicity or tribal identity
- ❌ No marriage date or place
- ❌ No death date
- ❌ No death place
- ❌ No description of any kind
- ❌ No speculation about her identity
- ❌ No post-1682 reference to Joan's status (alive or dead)

**Tag:** 🟢 PROOF — Bates's published article contains no information about Joan's identity beyond her name.

---

## BATES'S CHILDREN LIST — Verified Against Image 10

Bates (XI p. 78) names these children of John¹ and Joan:

| Child | Bates Says | Image 10 Says | Match? |
|-------|-----------|---------------|--------|
| John² | Lieut., of Newport | NOT in Image 10 deed | ⚠️ Not in our primary source |
| Henry² | Of Quidnisset and "New Gearsey" | NOT in Image 10 deed | ⚠️ Not in our primary source |
| Daniel² | Of Quidnisset | ✅ Named as grantee | ✅ |
| James² | Of Quidnisset | ✅ Named as "natural son" | ✅ |
| Benjamin² | Of Quidnisset | Beny in Image 10 deed | 🟡 PLAUSIBLE Beny might equal Benjamin-needs professonial insight |
| Sarah² | Married Thomas Flounders ~1668 | NOT in Image 10 deed | ⚠️ Not in our primary source |
| Edward² | Mentioned XII pp. 24–25 | NOT in Image 10 deed | ⚠️ Not in our primary source |

**Only Beny, Daniel and James are confirmed by Image 10.** The other 5 children come from Bates citing other records (unnamed). Until we find those records, the full children list is 🟡 PLAUSIBLE.

---

## BATES'S KEY DEED SUMMARIES — What She Actually Says

### Clark-to-Brinley 1685 (XI p. 74)
Bates quotes: "John Greene, sr., of Narragansett, now deceased"
Source cited: "Jamestown Records"
**She does NOT reproduce the deed.** She provides a narrative summary.
**Joan is NOT mentioned.**
**Tag:** 🟡 PLAUSIBLE — Bates quoting from local records we haven't seen.

### James-to-Wightman 1695/96 (XII p. 25)
Bates says: "February 15, 1695/6. James Greene sold to George Wightman of Rochester, R. I., 18¾ acres of land in the Quidneset Purchase that Atherton & Co. had granted to John (1) Greene of Newport, bounded by his brothers, Benjamin (2) Greene and Edward (2) Greene."
**She does NOT reproduce the deed.** Narrative summary only.
**Joan is NOT mentioned.** No annuity reference in this passage.
**Tag:** 🟡 PLAUSIBLE — Bates citing local records.

### John-to-Brothers 1675 (Worthington p. 102)
Worthington says: "my two Brothers Mr James Greene and Mr Thomas Greene"
**These are John's BROTHERS, not his sons.**
**Joan is NOT mentioned.**
**Tag:** 🟡 PLAUSIBLE — Worthington abstract.

---

## THE TWO-JAMES SEPARATION — Critical

| James Greene | Relationship | Source | Key Deed |
|-------------|-------------|--------|----------|
| James Greene (brother) | John's brother | Worthington p. 102 (1675 deed) | Receives land as "Mr James Greene" |
| James Greene (son) | John and Joan's son | Image 10 (1682 deed) | Receives homeplace as "natural son" |

**These are two different people.** Uncle and nephew, same name. Every genealogical database that doesn't separate them is contaminated.

Bates herself may have confused them — she identifies James the son born 1655, but the 1675 deed calls James the brother "Mr" (a status title). A 20-year-old son would not typically receive "Mr." in 1675.

**Action needed:** Audit every "James Greene" reference in the archive. Tag each as BROTHER or SON.

---

## BATES'S SOURCES — What She Cites

1. Newport Town Records
2. Jamestown Town Records
3. North Kingstown Town Records
4. Portsmouth Town Records
5. Shrewsbury, NJ records
6. Rhode Island Colonial Records (= Bartlett)
7. Fones's Records
8. Potter's *Narragansett*
9. State Records
10. Rehoboth records
11. J. O. Austin (genealogist)
12. General George S. Greene (family papers/correspondence)

**None of these are manuscript images. All are secondary or printed compilations.**

---

*Joan Archive — research_findings/2026-09-05_bates_deep_read.md*
*Law 7: No Trust Without Evidence*
```

## Required output
Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.
