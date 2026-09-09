# Sideways Lanes — First Runs (Minor Diary, Winthrop Casebooks, Probate Locator, Portal Access)

**Status:** `PENDING_HUMAN_REVIEW`
**Date:** 2026-09-09
**Purpose:** First execution of four recon-queue lanes (R32, R27, R46, and the probate locator feeding the neighbor-wives calibration). All results are scoped and honest about access limits.

---

## Lane 1 — R32: Thomas Minor diary (Stonington, 1653–1684) — VERIFIED NEGATIVE

**Method:** Downloaded the full OCR text of *The Diary of Thomas Minor, Stonington, Connecticut, 1653–1684* (1899 edition) from Internet Archive (`diaryofthomasmin00mino_0`, `_djvu.txt`, 9,023 lines) and ran the archive's variant sets locally. Verifiable — the text file is reproducible from archive.org.

**Results:**

| Search | Hits | Assessment |
|---|---|---|
| Greene / Green / Grene / Groon | **0** | NULL — no Greene of any spelling appears in the diary |
| Joan / Joane | 1 | "Joana minor" — the diarist's own family; not relevant |
| Fones, Tibbit, Havens, Gould | 0 each | NULL |
| Cocumscussoc, Quidnessett, Aquidneset, Wickford, Quckeset | 0 | NULL — Minor's world is Stonington/New London, not the west bay |
| Narragansett | 1 | Introduction only ("Narragansett Indians" in the editorial preface) |
| Smith | 19 | All local Stonington figures (widow Smith, Lieutenant Smith, Daniell Smith, the smith = blacksmith). None identifiable as Richard Smith of Cocumscussoc |
| Williams | 7 | Cows, carts, and letters of local Williamses; "mr Williams to the govenor" (1650s context) — no Joan/Greene connection |
| Stanton | 57 | The Stonington Stantons are heavily present — expected; this is their town. Relevant only to the Stanton-interpreter thread (henry_tibbitts.md), no direct Joan anchor |

**Scoped negative statement:** Thomas Minor's diary, 1653–1684, contains no Greene, no Joan, and no Cocumscussoc/Quidnessett reference. **Why it's only scoped:** Minor wrote from the east side of the bay; the diary's silence reflects geography, not absence of the family. Value delivered anyway: the diary names wives constantly ("Ephraim's wife," "goodwife ffaning") — it confirms the *genre* works for finding women, just not in this corridor. R32 closed as SCOPED NULL for Joan/Greene.

## Lane 2 — R27: Winthrop Jr. medical casebooks — ACCESS MAPPED, NOT YET SEARCHABLE

**Verified:** the casebooks are physically at **Massachusetts Historical Society**, Winthrop Family Papers.

**Not verified / not located:** a name-searchable digitized edition or published patient index. The archive's earlier note ("digitized, partially published") could not be confirmed externally this session.

**Realistic path:** MHS Ask-a-Librarian request — *"all patient entries 1650–1670 from the Narragansett/Wickford/Quidnessett/New London corridor, plus any Greene/Green entries and 'wife of John Greene'"* — or an in-person visit. R27 stays ❌ NOT SEARCHED with access path now documented.

## Lane 3 — R46: Native Northeast Portal variant sweep — BLOCKED, needs a browser

The portal is JavaScript-rendered; neither research agents nor this environment could query it. The full 11-variant search list is staged and ready for a human browser session. R46 stays ❌ NOT SEARCHED.

## Lane 4 — Probate locator for the 9 unresolved neighbor households — MAP BUILT

**Structural finding:** Rhode Island probate was kept by **towns**, and the **1869 North Kingstown fire** means Kingstown-family probate survives only where it was copied before 1869 or microfilmed. No open digitized probate located for any of the nine (Fones, Andrews, Briggs, Waterman, Gould, Greenman, Smith Jr., Carr, Carpenter).

**Cheapest closure routes, in order:**
1. **NEHGS americanancestors.org** (paywall) — RI probate indexes/abstracts likely resolve ~60% of the nine rows in one session.
2. **RI State Archives Preservica portal** — browse "Probate Records 1690–1730" for the Kingstown cluster.
3. **Austin's *Genealogical Dictionary of RI* (1887)** — full text on archive.org (`genealogicaldict00aust`); will abstracts for some of the nine may already be there. ⚠️ IA full-text not yet pulled line-by-line for all nine — queued as the next in-house run.

---

## What this means for the road

- The Minor diary NULL closes one lane honestly and **validates the genre**: diarists of the period DO name wives — we just need one whose author lived west of the bay. (That sharpens the value of the Smith household papers and the Kingstowne clerks' identities — R30/R36.)
- The calibration study's nine unresolved rows now have a documented cheapest path: **one NEHGS session** or one State Archives visit resolves most of them, and with them the "is Joan's silence normal?" question.
- Two of four lanes are browser/human-gated. The archive's frontier has moved decisively to: **human sessions at FamilySearch, MHS, NEHGS, the State Archives, and the Portal.** The AI-side lanes that remain open are the printed-book sweeps (Austin next).

## Next actions (queued)

1. Austin 1887 full-text sweep for the nine men + wives (in-house, verifiable — same method as the Minor diary)
2. Human: NEHGS session → probate abstracts for the nine
3. Human: MHS Ask-a-Librarian → Winthrop casebooks query (text drafted above)
4. Human: Portal browser session → 11-variant Anashuecot sweep

---

## Lane 5 — Austin 1887 full-text sweep (added same day, in-house, verifiable)

Ran `genealogicaldict00aust` `_djvu.txt` (3.8 MB) locally against the nine households + the Greene family. Method identical to the Minor diary run; reproducible from archive.org.

**Wives resolved (📚 SECONDARY — Austin's record abstracts, originals not yet pulled):**

| Husband | Wife | Austin anchor |
|---|---|---|
| John Fones | **Margaret** (d. 1709) | FONES entry: "John... m. Margaret, d. 1703, Dec. 20"; son Samuel matches the Tibbitts-will Fones link |
| John Andrew(s) | **Mary** (2nd wife; remarried John Nichols 1721) | ANDREW entry; 1693 deed: son pays "mother-in-law [stepmother] Mary Andrew" 10 bushels of apples yearly for life |
| Caleb Carr | **Phillip(a)** — widow & executrix | CARR entries: "Phillip Carr, widow and executrix of Caleb Carr, of Jamestown, deceased"; will witnessed 18 Mar 1694 |
| Thomas Gould | **Elizabeth** (⚠️ which-Thomas flagged) | "pay Thomas Gould's wife Elizabeth, £10 a year for life, in lieu of all her claims of land in Narragansett" — an ANNUITY, same instrument family as Joan's |

**Bonus finds:**
- **Flounders estate petition, full mechanism** (Austin FLOUNDERS entry): estate forfeited to the King on execution; Edward Greenman and **John Greene, of Newport** petitioned the Assembly 26 Oct 1670; the Assembly's quoted language names "Sarah, the late wife of the aforenamed Thomas Flounders"; relief granted (bedding, household stuff, a cow and hog, the corn). Written into sarah_greene_flounders.md.
- **Wightman 1696 deed chain** (Austin GREENE entry): John Greene → Benjamin → James → George Wightman, bounded south by Edward Greene — partially repairs the damaged-deed problem (R12). Written into james_greene.md.
- **John Andrew's house** was the 1672 deed's boundary landmark ("bounded on the east from the house of John Andrew") — a new physical anchor for the Fones Purchase geography.
- Austin's own John-Greene-of-Quidnessett entry (1663 CT declaration, 1664 removal, 1671 oath, 1672 purchase, 1676 court martial) corroborates the archive's sequence from a second independent compiler. One line ("1670, Jul. 29. He signed the petition to the King") sits in a column-confused OCR region — ⚠️ attribution uncertain, flagged not used.
