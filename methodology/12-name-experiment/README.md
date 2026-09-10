> This archive documents lives lived between approximately 1600–1750 in Narragansett country (present-day Rhode Island). All records from this period were created within colonial legal systems and reflect their biases, categories, and blind spots. Every name found here — English, Narragansett, Niantic, mixed-heritage, unknown — represents a real person whose full story these records were not designed to capture. Content may include references to war, captivity, enslavement, displacement, legal coercion, and loss. These are documented realities of the period, not abstractions. All cultural and genealogical content is included for research purposes in the quest to identify Joan Unknown Greene and will be revised or removed if requested by descendant communities or tribal representatives.

# The 12-Name Experiment

**Hypothesis:** Colonial land records contain recoverable female identities whose names are individually ambiguous but whose relational and land networks are sufficiently distinctive to reconstruct them without relying on secondary genealogy.

**If this works:** The Joan methodology becomes a reproducible archival method for finding "unknown women" in colonial land records — not a one-off investigation.

**If it doesn't:** We find exactly where the method breaks, which is equally valuable.

**⚠️ SANDBOX EXPERIMENT — nothing here touches the main archive index. Findings migrate to the archive only when proven through the Three Laws.**

---

## The Corpus

Rhode Island Land Evidences, Volume I (1648–1696)
- 445 transcribed instruments: deeds, wills, powers of attorney, settlements, other legal records
- Records frequently preserve spouses, widows, children, witnesses, adjacent landowners, dates
- Rhode Island law makes the female signature particularly interesting: a married woman could join her husband's deed to release dower, and separate releases could be recorded later
- Women aren't just names in this corpus — they are legal nodes in the land network

## The 12 Test Names

Variants kept separate to measure divergence:

| # | Name | Expected Ambiguity | What We're Testing |
|---|------|-------------------|--------------------|
| 1 | Mary | Very high | Can relationships overcome extreme name frequency? |
| 2 | Elizabeth | Very high | Same |
| 3 | Sarah | High | Same |
| 4 | Hannah | Medium/high | Same |
| 5 | Ann | Very high | Variant-specific tracking |
| 6 | Anne | Very high | Does spelling create artificial separate women? |
| 7 | Joan | Lower | Does rarity materially improve reconstruction? |
| 8 | Abigail | Medium | Network recovery |
| 9 | Margaret | Medium | Network recovery |
| 10 | Esther | Medium | Compare against known Smith case |
| 11 | Hester | Low/medium | Does spelling hide identity continuity? |
| 12 | Mercy/Patience/Prudence | Special case | Puritan naming cluster vs actual identity |

## Three Types of Ambiguity Being Measured

1. **Variant ambiguity** — Esther ↔ Hester (same linguistic name, different rendering)
2. **Cultural-frequency ambiguity** — Mercy / Patience / Prudence (different names, same naming culture)
3. **High-frequency ambiguity** — Mary / Elizabeth / Anne (so common the name alone means nothing)
4. **Rarer-name leverage** — Joan (fewer collisions — but we measure this, not assume it)

## The Core Principle

Given-name frequency is NOT identity evidence.

"Mary + Rhode Island + 1670" means almost nothing.

"Mary + husband X + land parcel Y + witness Z + neighboring owner Q" can become an identity.

That's the fundamental Joan rule.

## What Gets Recorded Per Occurrence

For every time one of these names appears in the corpus:

- **Name** → exact wording in the document (Mary, not "Mary Smith" unless the document says Smith)
- **Date** → document date
- **Town** → location
- **Husband** → if stated
- **Children** → if stated
- **Witnesses** → named
- **Neighbors / adjacent owners** → named
- **Land** → parcel, boundaries
- **Indigenous place-name** → if present
- **Role** → wife / widow / grantor / grantee / witness / releasor of dower
- **Later appearance** → same woman in another record?
- **Contradiction** → evidence AGAINST a merge
- **Identity status** → UNIQUE / AMBIGUOUS / MERGED (with evidence) / UNRESOLVED

## What We're Measuring

- **Relational density** per name — how many edges (husband, witnesses, land, neighbors) does each occurrence carry?
- **Collision rate** — how many distinct women share the same given name in the same corpus?
- **Reconstruction rate** — for how many can we build a unique identity signature from relationships alone, without a surname?
- **Variant divergence** — do Ann and Anne, Esther and Hester, behave as one population or two?
- **Joan's position** — does her lower frequency actually give her more identifying power, or is that an assumption?

## The Control Case

Esther Smith, wife of Richard Smith Jr., is our first control. Her name alone isn't particularly useful. But her network signature is:

- husband (Richard Smith Jr.)
- property (Cocumscussoc/Wickford estate)
- location (Narragansett country)
- kinship language ("cousin" of Richard, sends love to "her uncle" William Barton)
- correspondence (wrote to John Winthrop Jr.)
- later estate participation (1690/91 probate)

That's an identifiable node even though "Esther Smith" is not unique. The experiment tests whether we can build equivalent signatures for the other 11 names.

## The Spelling Split Experiment

The Ann/Anne and Esther/Hester splits test what genealogy databases routinely do automatically (and shouldn't):

- **DO NOT normalize spelling initially.** Treat each variant as a separate population.
- If Esther A and Hester B share the same husband, property, witnesses, location, and continuous chronology → evidence for variant equivalence.
- If they have different husbands, different properties, different towns, overlapping lifetimes → collapsing them would create a false identity.
- This is a much stronger test than simply saying "Esther and Hester are variants."

## The Identity Firewall

When two occurrences of the same name appear:

**STOP. Show the edges.**

If the edges diverge (different husband, different land, different witnesses, different town) → keep them separate. Two people until evidence says otherwise.

If the edges converge independently (same husband, same parcel, same neighbor, continuous chronology) → evidence for one identity.

Collapse the graph ONLY when independent evidence warrants it.

## What This Experiment Does NOT Do

- ❌ Does not attempt to prove Joan's identity
- ❌ Does not search secondary genealogy databases
- ❌ Does not normalize spellings before testing
- ❌ Does not merge records based on name alone
- ❌ Does not touch the main archive index

## Unproven Premise (Hypothesis, Not Fact)

The claim that "the untraced names overwhelmingly consist of these names" is a hypothesis this experiment will test. We have not yet counted the entire female-name population in the corpus. The experiment will produce that census.

## The Real Research Question

> What is the minimum amount of network evidence needed to recover an unidentified woman from colonial land records?

Joan becomes one trial in a population of 12, not the special case the method was designed to prove.

If the methodology survives, it's worth publishing independently.

If it doesn't, we find where it breaks — and that's equally valuable.

---

## File Structure

```
methodology/12-name-experiment/
├── README.md              ← this file (design doc)
├── data/
│   ├── mary.csv           ← one CSV per name
│   ├── elizabeth.csv
│   ├── sarah.csv
│   ├── hannah.csv
│   ├── ann.csv
│   ├── anne.csv
│   ├── joan.csv
│   ├── abigail.csv
│   ├── margaret.csv
│   ├── esther.csv
│   ├── hester.csv
│   └── mercy-patience-prudence.csv
├── analysis/
│   └── variance-report.md ← results when populated
└── controls/
    └── esther-smith.md    ← known identity as control
```

---

> **Search direction bias check:** When an agent recommends "where to look next," ask: is this recommendation biased toward digitized, English-language, colonial-framework sources? What record types exist that this agent might not know to suggest? What would a Narragansett historian, a maritime historian, an archaeologist, a linguist look for that a genealogist wouldn't?

This experiment uses a colonial English-language legal corpus by design — it's testing whether the Joan methodology works within that framework. But the bias check still applies: what relational edges exist in non-colonial records that this corpus cannot capture? Indigenous kinship, maritime connections, church records, oral history, and archaeological evidence are all outside this test — and any of them could provide the bridge this corpus misses.

---

*Joan Archive — methodology/12-name-experiment/README.md*
*Nothing is proven until original proof images are on the archive.*
*Created: 2026-09-09 — Wendy Green + ChatGPT (experiment design) + Migoo (documentation)*