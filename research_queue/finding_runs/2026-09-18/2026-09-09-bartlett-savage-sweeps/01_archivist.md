# Archivist Queue Packet — research_findings/2026-09-09_bartlett-savage-sweeps.md

**Finding ID:** `FINDING-da4cc6a2c49a`
**Status:** `LAWS_FILTERED`
**Source SHA-256:** `24204182be8f9c157b935f371efb39ed1cbd522b5517c54ba5b755eaabc58610`
**Stage purpose:** establish provenance, stable identifiers, page/image anchors, and checksum needs.
**Publication rule:** This is a Laws-filtered review packet, not evidence and not an approval. AI disclaimer applies.

## Required action
Process this finding as stage `01_archivist`. Preserve the exact source path and hash.
Do not edit the source finding or promote any claim to PROOF.

## Image gate
Referenced images: none detected.
Images already staged in `images/_pending_review/`: none.
Referenced images already elsewhere in `images/` and not pending: none.
Referenced images not found in the archive: none.
Any newly supplied image belongs in `images/_pending_review/` until a human reviews and promotes it.

## Finding text
```markdown
# Colony-Record Sweeps: Bartlett RICR Vols 1 & 3, Savage Vol 1 — with OCR-hygiene correction

**Status:** `PENDING_HUMAN_REVIEW`
**Date:** 2026-09-09
**Method:** Full `_djvu.txt` scans from Internet Archive, grepped locally (reproducible). Texts: `recordsofcolonyo01rhod` (Bartlett Vol. 1, 1636–1663), `recordscolonyrh03bartgoog` (Bartlett Vol. 3, 1678–1706), `genealogicaldic01savarich` (Savage Vol. 1).

---

## The OCR-hygiene correction (this changes an earlier sweep's meaning)

My first variant grep used `\bgreen` word-anchors and found "0 Quidnessett variants, 4 Green hits" in Bartlett Vol. 1. **But Bartlett's own spelling is "Green"** — and the archive's name registry documents period scribes writing *Greane, Grene, Creene, Greeu*, none of which a bare `\bgreen` catches. A first-class sweep searches the whole cluster. Re-ran:

| Text | `green` only | full cluster (green\|grene\|greane\|creene\|greeu…) | Quidnessett cluster (incl. Quidneset/Quoheset/…) |
|---|---|---|---|
| Bartlett Vol. 1 | 4 | **5** (+ "Wm. Green[e]"); Quidnesett variants: 0 | 0 |
| Bartlett Vol. 3 | 23 | **26** (+ "Henry Greene," "Mr. Greene"); Quidnesett variants: 0 (but see OCR-collision note) | 0 raw — **"Greenwich" absorbs the Quidnessett-region spellings; see below** |
| Savage Vol. 1 | 20 | 21 | 0 (vol. 1 covers A–B surnames only — Greene is Vol. 2) |

**OCR-collision finding (structural):** in Bartlett Vol. 3's print, **"East Greenwich" is itself spelled "East Green- / Greenwich"** — meaning place-name searches for the Quidnessett family's later records must subtract the town of Greenwich from Greene-person hits line by line. Most Vol. 3 "Green" hits are the *town*, not a person. This is the geography-index problem running in reverse, and it's now logged.

## Verified results

### Bartlett Vol. 1 (1636–1663) — Joan NULL confirmed
- **Joan: 2 hits, both other women** (Joan Tyler; "widow Joan" in a Newport inventory). **No Joan Greene, no wife-of-John-Greene.** Machine-verified against the earlier web-search NULL.
- **Greene cluster: 5 hits, all Surgeon-line or town context**: "John Green" (signs as *Clarke of the Assembly*, 1654 — the Warwick line's John, not ours), "Peter Green" (Surgeon's son), "William Field, John Green, John Smith, John Lippitt" (Providence arbitration list), "Wm. Green," and one index entry. **No Quidnessett John in Vol. 1** — consistent with the record: his first colony-record appearance is the 1664 warrant (Vol. 2 territory). The earlier NEGATIVE_LOG row stands, now with a reproducible method.

### Bartlett Vol. 3 (1678–1706) — person-level hits
- **"Henry Greene"** — appears in a 1690s list context (line ~4700s region includes East Greenwich/Kingstown freemen lists; the Henry row needs the line-level read, queued).
- **"Mr. Greene"** — referenced in a boundary-dispute narrative (Connecticut line papers). Context reads as Major John of Warwick's orbit, not ours — **flagged, not assigned**, pending the passage read.
- **"Edward Greenman and his son"** — 1721: Hauxey & Peckham delivered £494 in bills of credit "upon the account of Edward Greenman and his son"; colony action against Greenman abated. **This is OUR Edward Greenman's family** (the 1682 deed witness) — proof the Greenman household remained in the colony record to 1721, and that a son existed (the wife question in the calibration study stays unresolved, but the household now has a dated financial footprint).
- **"John Tibbets… of Greenwich, admitted freeman"** — the Tibbitts network (Joan's in-law line) appears in the Vol. 3 freemen lists. Noted for the network map.
- **Joan: 0 hits.** The colony record between 1678 and 1706 — covering the entire window after the 1682 deed — contains no Joan at all. **The post-1682 silence is now verified at the colony-record level with a reproducible search.**

### Added on the line-level pass (same session)
- **The Charles Greene + John Fones deed (Bartlett Vol. 3, 1708 session, pp. 51–52 of the print).** The Assembly, disposing of East Greenwich land petitions, enacts that lands in "the deeds of **Cojanaquant** to Capt. Cranston and company" were already confirmed "to the township of East Greenwich, and **John Fones and partners**" — and rules likewise on "the deed of **Charles Greene** and John Fones and partners," citing a plat by Capt. Peleg Sanford and Mr. John Smith, surveyor. Three things fall out: (1) a **Greene we have never catalogued — Charles** — held a deed with John Fones in the East Greenwich/Quidnessett land complex; (2) this is the **second** Greene+Fones land partnership on record (the other is 1672); (3) **Cojanaquant/Coginaquand's grant chain is confirmed into East Greenwich by a colony act**, not just by Potter. ⚠️ Which Charles, and whether he belongs to the Quidnessett line, the Surgeon line, or neither: UNRESOLVED, firewall rules apply.
- **"Henry Green" admitted freeman** (Vol. 3, a William-Wanton-speaker Assembly, freemen list): sits in a Newport/Portsmouth-heavy list (Caseys, Carrs, Shearmans, Clarkes). No identifier attaches him to Quidnessett — **could be ours (the compiled Henry), the Warwick line, or a third man. Flagged, not assigned.** This is exactly the class of record La Mance turned into "Robert, freeman 1674" — this time we keep the man and the list honest and separate.
- **Second line-level pass (Swyft T2 spin-off):** Vol. 3's freemen lists also yielded **"John Greene, son of James Greene, deceased," of Warwick** — a clean Surgeon-line datapoint (the Major's son, third generation); and the **John Wing + Jonathan Fish adjacency** in a Portsmouth list, logged to the Swyft test file as a non-collision. No Quidnessett-line Greene appears anywhere in Vol. 3's freemen lists — consistent with the record that our line never sought colony freemanship after 1671.

### Savage Vol. 1 — N/A by construction + a method note
Vol. 1 covers surnames A–B; the Greene entry is Vol. 2. The 41 "Joan" hits are other families' Joans. **Scoped no-result, not a negative** — Vol. 2 remains unsearched and is queued.

## What changed / what's queued

| Item | Status |
|---|---|
| Joan NULL in colony records 1636–1663 and 1678–1706 | ✅ Machine-verified (cluster searched, both volumes) |
| The 1664 warrant + 1671 oath volume (Bartlett Vol. 2) | ❌ queued — the one volume where our John IS expected |
| Savage Vol. 2 (Greene entry) | ❌ queued |
| **Charles Greene identity** (Fones deed partner, 1708 enactment) | ❌ queued — new person-question, firewall rules |
| "Henry Green" freeman list (Wanton Assembly) — which Henry | ❌ queued |
| Bartlett Vols. 4+ (1706+) | ❌ queued |
| Bates vols. XI–XII correct scan (the 1918–19 Greene articles) | ❌ still not identified on IA |
| OCR-hygiene rule added to sweep method: search the full registry cluster + subtract "Greenwich" collisions | ✅ applied from this run forward |

---

## Second wave (same session, 2026-09-09 late): Savage Vol. 2 + Swyft T1/T2 + the Swyft network's own corridor

### Savage Vol. 2 (D–G surnames — the GREENE volume), IA `agenealogicaldi02unkngoog`
- **Joan: 46 hits, zero co-occurring with Greene.** Quidnessett/Cocumscussoc variants: 0. **The strongest genealogist of the period knew nothing of our John or Joan.** The 2026-09-05 web-search NULL is now machine-verified.
- **The Warwick corridor is confirmed as Surgeon-line territory in print:** Savage's GORTON entry — Samuel Gorton "in 1643, with Holden, **Greene**, and others, made the great movem. to purchase of Warwick from the Ind." — and his daughter Mary "m. perhaps, **Peter Greene**, first, and, next, John Sanford." Peter Greene = Surgeon's son; the Gorton–Greene intermarriage documented here is all Warwick-line.
- One John Greene in vol. 2 is a **Boston mariner taken by the Turks, 1681** (per Roadiah Russell's diary, Gen. Reg. VII.54) — a *fifth* colonial John Greene for the firewall's census, noted so nobody mistakes him for ours.

### Swyft T1/T2 — run, in-house, free
Results written into [../research/joane_swyft_test.md](../research/joane_swyft_test.md). Headlines: still "Joane Swyft, widdow" through 1651 (window narrowing); **zero Swyft/Wing/Barnes collision with the Quidnessett network** in RI vols. 1–3; one Portsmouth Wing–Fish adjacency logged as NOT a collision. Candidate remains open, leaning unrelated.

### Swyft network check (the follow-the-truth leg)
Her documented associates — Daniell Wing and John Barnes — are **Sandwich** men (Wing: town-founder stock; Barnes: Plymouth-Sandwich corridor). No Narragansett tie located. Where they *do* intersect RI records is Portsmouth (Aquidneck) freemen lists of the 1690s — interesting geography, wrong town, wrong decade, no deed.

### Firewall ledger, updated
Colonial John Greenes now on the board: I Surgeon · II Quidnessett (ours) · III Major John of Warwick · IV Newport · V Kingstown · **VI the Boston mariner (taken by Turks 1681, Savage v2)** · Charles Greene of the Fones deed (uncatalogued line). Each kept separate. Each is a door.

*Bias check: these are the colony's own printed records — the system least likely to name a woman like Joan by design. Verifying her absence here is calibration (how far the silence extends), not discovery. The discovery lanes remain the household/sideways records queued in the road.*
```

## Required output
Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.
