# Explorer Queue Packet — research_findings/2026-09-09_bartlett-vol2-smith-letter.md

**Finding ID:** `FINDING-f65d4e86cacf`
**Status:** `PENDING_HUMAN_REVIEW`
**Source SHA-256:** `ef45a568125f89d23e5c62ea8ebe33c3073f6f74195812c441376f848a3185c9`
**Stage purpose:** expand sideways context and identify where evidence may be hiding in plain sight.
**Publication rule:** This is a review packet, not evidence and not an approval.

## Required action
Process this finding as stage `04_explorer`. Preserve the exact source path and hash.
Do not edit the source finding or promote any claim to PROOF.

## Image gate
Referenced images: none detected.
Images already staged in `images/_pending_review/`: none.
Referenced images already elsewhere in `images/` and not pending: none.
Referenced images not found in the archive: none.
Any newly supplied image belongs in `images/_pending_review/` until a human reviews and promotes it.

## Finding text
```markdown
# Bartlett Vol. 2 Sweep — the Smith 1664 letter original location, and a wrong-scan self-correction

**Status:** `PENDING_HUMAN_REVIEW`
**Date:** 2026-09-09
**Method:** IA `_djvu.txt` full texts, local greps, full variant clusters. Two scans were involved — and the first one was the wrong book.

---

## The self-correction (logged per Law 4)

The hunt for Bartlett RICR Vol. 2 first pulled `recordsofcolonyo0102newp` ("vols 1 & 2, 1855–1861"). **It is not Bartlett.** Title-page markers identify it as *Records of the Colony of **New Plymouth*** (Shurtleff's series). The identifier's title is misleading. The sweep of it is therefore logged as a **Plymouth** sweep, not an RI one — and it returned its own valid scoped results (below). The real Bartlett Vol. 2 is `recordsofcolonyo02rhod`, identified by preface and content (1663–1677, opens with the charter and the Narragansett-country jurisdiction fight). Everything "RI Vol. 2" below comes from that scan.

*Standing rule added to the sweep method: verify the book before sweeping it. An identifier's title metadata is not the book.*

## Accidental bonus — Plymouth Colony Records vols. 1–2 (1633–1651), swept

- **Joan NULL** (10 hits — all other women: Joane Hucker, Joane Stanley, Joane Swyft of Sandwich ×3 [she administers an estate, gives evidence — a documented *visible* widow, useful for the calibration study], etc.)
- **Greene-person NULL** — 70+ "Green" hits are overwhelmingly **Green's Harbor** (a Plymouth place, named for a different man entirely) — the OCR-collision hazard strikes again, this time in our favor as a warning: *Green place-names pollute Greene-person searches in every colony's records.*
- Quidnessett/Narragansett-cluster: 3 hits, all generic.
- **Calibration value:** Plymouth court orders 1633–1651 name women constantly — wives in incontinency cases, widows as administratrixes. The *genre* records women; our corridor's records just don't record Joan.

## Bartlett RICR Vol. 2 (1663–1677) — the real sweep

### Joan: 0 hits. Post-1663 silence holds at colony level.

### FIND — the Smith letter's ORIGINAL LOCATION (R30 partially resolved)
Bartlett prints Richard Smith Sr.'s **14 May 1664 letter to Capt. Hutchinson in full** (Vol. 2, pp. 47–48 of the print), with the footnote:

> *"From Collection of manuscripts in the Library of the Rhode Island Historical Society."*

**The original manuscript is at RIHS.** R30 (hunt the original, currently "possibly MHS Winthrop Papers — OPEN") is now pointed at the right repository. The physical pull list gains a second RIHS target alongside Mss 461.

The letter's text, now in the archive from a second, colony-published source:
> "Three days since they came to **John Green's house att Aquidnesett** with a warrant from theyre court, under the Governor's hand, and forceably fetched him awaye to Rode Island where he yet remaynes. His goeing was also not known to any here; they have also constituted officers at Petacomscott…"

- "**John Green's house att Aquidnesett**" — our John, the spelling this registry documents, in a letter written from Wickford three days after the event. Firewall-safe: no other John had a house at Aquidnesett.
- The letter is embedded in a packet: Hutchinson & Hudson forwarded copies to the **Governor of Connecticut** — meaning a CT-side copy may survive in Connecticut archives (ties to R26).
- **Richard Smith Jr. adds "a few lines"** to the same 1664 packet — the household's next generation already writing in the network.

### The Hutchinson/Hudson reply (same packet) — Mr. Gould's bond
The reply letter reports the Narragansett men's treatment: "**They have ingaged Mr. Gould to apeare there agayne next October**… the bond to continue till then, as also good behaviour; but we are not tyed within the bowndry of theire colony." — Thomas Gould's 1664 bond-and-appearance, from a second source. Adds to his timeline.

### The 3 Jan 1665 Pumham payment (Vol. 2)
"Mr. Samuel Gorton, Sen'r, **Capt. John Green**, Mr. Walter Todd, **Mr. James Green**, and Mr. John Potter of the towne of Warwicke" deliver £10 in peag to Pumham, witnessed by Edward Marshall, Edmund Calverly, Amos Westcot, Samuel Gorton Jr., **John Wicks Jun'r** — all Surgeon-line/Warwick names. A clean firewall-III cluster (and John Wicks Jr. is one of the suspended-Pawtuxet-deed witnesses — network data, not evidence about that deed).

### Vol. 2's other Greenes — all officeholders (Surgeon line)
"Capt. John Green" and "James Greene" recur as Assistants/committeemen; "Robert Green" appears in a Newport-area list (line 17597, ⚠️ no qualifier — *another* Robert sighting, held separate from ghost G-002); "Mr. Green re—" (truncated, boundary context). None is our John: his Vol. 2 appearances are the warrant (as victim, not officeholder) and the oath (1671, next read).

## Queue movements

| Item | Change |
|---|---|
| R30 (Smith letter original) | 🟡 **Repository found: RIHS manuscript collection** (Bartlett's own footnote). Physical-pull list updated |
| R26 (CT-side records) | New specific target: the Hutchinson/Hudson→CT copy of the 1664 packet |
| Plymouth Colony Records vols. 1–2 (1633–1651) | ✅ Scoped NULL for Joan/Greene-person; calibration value logged |
| Bartlett RI Vol. 2 | ✅ Swept. Joan NULL; John appears as warrant target (1664); oath read queued with Vol. 2 close-read |
| Bartlett RI Vols. 4+ | ❌ queued |
| The 1671 Acquidnessett court record in full | ❌ next read in this volume |

*Bias check: same caveat as the Vol. 1/3 sweep — colony records are the least likely system to name Joan. What Vol. 2 gave instead is the paperwork of the system that arrested her husband.*
```

## Required output
Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.

## Required sideways-context checklist
- Map household people, witnesses, neighbors, in-laws, buyers, sellers, and officials.
- Expand across land, probate, court, church, militia, servant, captivity, shipping, and Indigenous-centered records.
- Test Rhode Island, Massachusetts, Connecticut, Plymouth, New York, Crown, port, and local town repositories.
- Search EVERY variant of EVERY name in the finding — full clusters from methodology/name_variant_registry.md (standard, scribe drift, OCR-plausible, phonetic) — in EVERY repository searched, and log which variants were queried. A name missed for spelling is a name lost.
- Track every John Greene appearance 1600-1750 across English, Irish/Ulster, Scottish, port-book, and local-town paperwork — each is a firewall-relevant capture per methodology/collection_policy.md (the Greene Net).
- Search relationship descriptions ('wife of', 'Goodwife', 'widow', 'son of', 'his marke'), not only the target person's name.
- Follow where the leads point, including jurisdictions and languages the finding does not name.
- For each proposed edge, state the source anchor that would prove it and the record that would disprove it.
