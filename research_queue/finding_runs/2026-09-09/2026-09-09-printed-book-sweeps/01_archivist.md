# Archivist Queue Packet — research_findings/2026-09-09_printed-book-sweeps.md

**Finding ID:** `FINDING-3666ba387117`
**Status:** `PENDING_HUMAN_REVIEW`
**Source SHA-256:** `67f3391eff55e728818ae2b587bd9409d09b0cfacc5e82bad89eedfa78196c60`
**Stage purpose:** establish provenance, stable identifiers, page/image anchors, and checksum needs.
**Publication rule:** This is a review packet, not evidence and not an approval.

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
# Printed-Book Sweeps: Potter 1835, La Mance 1904, Turner 1877, RIHS Collections

**Status:** `PENDING_HUMAN_REVIEW` — the La Mance readings below restate a contaminated source for audit purposes only; nothing from La Mance is evidence.
**Date:** 2026-09-09
**Method:** Full `_djvu.txt` scans downloaded from Internet Archive and grepped locally. Every count is reproducible. Texts: `earlyhistoryofna00pott_0` (Potter 1835), `greenefamilyitsb01lama` (La Mance 1904), `greenesofwarwick00turn` (Turner 1877), `rhodeislandhisto09rhod` (RIHS Collections, OCR-metadata volume tag unverified — Joan/Quidnessett NULL in this scan either way).

---

## Result 1 — Three ghost names traced to birth. All La Mance. All invented from PLACE NAMES.

**G-003 "Enfield Greene" — mechanism found, word for word.** La Mance 1904 (scan lines 3179–3190):
- John of Quidnessett "resided at or near London; **probably his home was at Enfield**, one of the suburb towns of the great city." (emphasis on *probably* — La Mance's own hedge)
- "He was a man given to commemorating family events by the names of his children… **A daughter was Enfield, a most singular name for a girl, but understandable if given in honor of the dear old English home.**"
- Elsewhere (line 4059): "There was **almost certainly a daughter Enfield**…"

There is no record. There is a *story*: La Mance guessed a home town, then invented a daughter named after it. The compiled trees copied the daughter. **G-003 resolved as La Mance-manufactured, promotion path closed barring a primary record.**

**G-001 "Joan Greene, daughter" — La Mance contains NO daughter Joan of Quidnessett.** The only daughter Joan in the book is the Surgeon's (who died young — and La Mance's own text at 3765 uses her to argue against claims about the Quidnessett Joan). The compiled-list "daughter Joan (c. 1649–1715)" does not even have La Mance behind it. **G-001 has no source at any tier. Register entry stands; origins note updated.**

**G-002 "Robert Greene" — traced to La Mance's inference, and the detail that fed it:** "then came **Robert, born in 1653, for he was a freeman in 1674**" (line ~4055). That's the entire evidence: a freeman-list name, attributed to a son. The compiled "Virginia records" tag is unconnected to anything in La Mance. **G-002 = La Mance inference from an uncited freeman list; the Virginia flavoring is later decoration.**

Also newly documented from the same passage: La Mance invented **"Welthian"** as a probable daughter ("It was a Gillingham family name") — a *fourth* ghost, never before in this archive. Logged in the register as G-006 so she can never walk in unannounced.

**Honesty note:** these are readings of a contaminated source to document contamination — not evidence about the family. Law 2 applies to every line above.

## Result 2 — The "I. G." gravestone lead (La Mance 1904, lines 3735–3749)

La Mance records **three old graves "in what was once a part of John of Quidnessett's land"**: two rude headstones marked **D. G.** and **R. G.** (identified by La Mance as son Daniel and *his wife Rebecca*), and a third — the oldest — marked **"I. G."** which La Mance says "is believed to mark the grave of Mrs. Joan Greene, wife of John of Quidnessett" (I/J letterforms were interchangeable).

- **Evidence tier:** 🌐 TERTIARY at best — a 1904 antiquarian's "is believed to," with no survey, no photo, no location precision, no verification the stones survive or existed.
- **Why it matters anyway:** if the plot exists and can be surveyed, it is the only candidate **physical** trace of Joan anywhere. Feeds R48 (archaeology/material culture).
- **Contamination check:** note the same passage claims D.G./R.G. are Daniel + wife Rebecca — the archive has "Daniel's wife unknown (F.L. Greene: m. ——)." La Mance's Rebecca is unsourced. Flagged, not adopted.
- **Also in this passage:** "John Greene's wife was alive when these deeds were executed" — La Mance commenting on the deeds without quoting them. Worthless as evidence; noted only because it's the closest La Mance comes to describing the 1682 instruments.

## Result 3 — Potter 1835: Joan NULL, and a new name-variant question

- **Joan NULL verified:** two "Joan" hits in all of Potter — both other men's daughters (Viall of Boston's; a later genealogy). **No Joan-as-wife, no Joan+Greene, zero.** The Potter Joan-null is now machine-verified rather than read-in-spots.
- **Anashuecot cluster verified in-print:** Awashouse (5), Awashous (2+1), Awashwash (1), Awashshous (1) — matches the archive's phonetic registry counts.
- **⚠️ New question:** **"Awashequin"** — in Potter's account of the **27 Aug 1645 treaty at Boston** (Pessicus, Mixanno eldest son of Canonicus, "Awashequin, deputy of the Nyantics"). Phonetically adjacent to the Anashuecot cluster, but the *documented* identity here is a **Niantic deputy** — likely a different person entirely. Logged as an open variant-cluster question in the registry, NOT merged. If anyone ever equates them, they need a document.

## Result 4 — Turner 1877 (*Greenes of Warwick in Colonial History*): clean NULL for our Joan

Both "Joan" hits are the Surgeon's line (Joan Tattersall, first wife of the Surgeon; and their daughter Joan, d. young). Zero Quidnessett content. **The Warwick-side compiler knew nothing of our Joan** — consistent with the firewall.

## Result 5 — RIHS Collections scan: NULL but volume unverified

The `rhodeislandhisto09rhod` scan (IA metadata: "volumes 18–19," 1918) returned zero Joan and zero Quidnessett hits — **unexpected if this were the vols. XI–XII Bates text**, which we know contains "Joan Greene of Newport and Aquednesit." Probable wrong-volume scan or an OCR artifact. Treated as no-result, not negative. The Bates line-by-line sweep remains open until the correct scan is identified.

## What changes

| Register/queue item | Change |
|---|---|
| G-001, G-002, G-003 | Origins documented (La Mance mechanisms); register updated |
| G-006 "Welthian" | New ghost registered preemptively |
| R48 | Adds the "I. G." gravestone survey as the physical-trace lead |
| Anashuecot variant registry | Awashequin question logged, unmerged |
| Bates sweep | Still open — correct RIHS scan not yet identified |
| F.L. Greene 1894 sweep | Still open — not located on Internet Archive by metadata search |

*Bias check: every text swept this round is an English-language compiled genealogy or antiquarian history — by design; these are the contamination sources themselves, being audited, not consulted as authority. The community-governed and original-record lanes remain queued at R46/R47 and the human-step list.*
```

## Required output
Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.
