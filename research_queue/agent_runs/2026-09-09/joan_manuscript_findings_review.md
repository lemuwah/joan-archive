# Multi-Agent Review Round — Joan Manuscript Findings (2026-09-09, manual)

> Four-stage review of two findings produced this session:
> - `research_findings/2026-09-09_ri_state_archives_manuscript_found.md`
> - `research_findings/2026-09-09_homeplace_1682_manuscript_transcript_AI.md`
>
> Findings were routed through `tools/findings_pipeline/route_findings.py`
> (packets in `research_queue/finding_runs/2026-09-09/…/`); image gate passes
> (manuscript image staged in `images/_pending_review/` with provenance
> manifest). This file is the review-round output, NOT evidence and NOT an
> approval. Status: **PENDING_HUMAN_REVIEW** throughout. Nothing here promotes a
> claim to PROOF. Agent agreement is not corroboration (safety rule).

---

## 01 — Archivist (provenance, stable IDs, anchors, checksums)

**Manuscript image (primary source):**
- Repository: RI State Archives — Digital Archive (Preservica).
- Collection: Land and Public Notary records, Volume 1, 1648–1696 (RILE-I).
- Volume folder (SO): `SO_55976674-e8f4-44ab-b872-592c9ce4002e`.
- File (IO): `IO_6f6b6c51-8275-4e3a-95d9-c1e205f459f7` (listing image `_133`).
- Anchor: folios 259–260; image `_133` (offset folio = 2 × image − 7).
- Capture: 600 DPI, 10243 × 7320 px, JPEG.
- SHA-256: `49cae1a721558a93b6f23f42f43562590570182e8d3c85018974d887813d5470`.
- Accessed: 2026-09-09. Provenance + checksums recorded in
  `images/_pending_review/MANIFEST.md`. ✓

**Companion sources (re-fetchable, text-staged):**
- Worth 1921 abstract: archive.org item `rhodeislandlande00wort`, printed
  pp. 173–174, abstract [260]; OCR at `worth_djvu.txt`.
- Typed folio index (`Volume 1 Index`, 22 pp): Preservica
  `IO_5628068c-c8fa-486c-bdb8-4ed969f46f61`; text at
  `images/_preservica/vol1_index.txt`.
- Complete Volume PDF (222 pp): Preservica `IO_3d98349c-…`; gitignored,
  re-fetchable.

**Deduplication:** the James instrument exists in three forms — (a) colony
manuscript folios 259–260 (primary), (b) Worth 1921 abstract pp. 173–174
(secondary), (c) NK town book DGS 008204949 Image 10 (tertiary). All describe
the same instrument; no duplicate findings created. ✓

**Image gate:** passes — manuscript image + view staged in
`images/_pending_review/`; no missing references. ✓

---

## 02 — Hostile Review (attack identity, date, OCR, circularity, inference)

**MAIN VULNERABILITY — transcription is AI, not paleography (Law 7).**
The verbatim secretary-hand wording is a vision-model read of a 600-DPI scan.
Per Law 7 it is a lead, not a citation. The findings correctly flag this
(🟡 AI-READ). Every quoted clause must be confirmed by the owner (the
project's only paleographer) before citation. This is the single highest-risk
item; it is not overclaimed in the findings.

**"Page 173 → folios 259–260" correction — SOUND.** Three independent anchors
concur: (1) typed folio-index entry names the deed at folios 259–260; (2) image
`_133` visibly shows folio numbers 259–260; (3) deed content matches the Worth
1921 abstract (grantor/grantee, 60 ac, Quidnessett harbour, Daniel Greene
boundary, 24 March 1681/2, Tibbitts/Aylsworth/Nutsn, Fones). The earlier
"page 173 = Joan's deed" note was a conflation of Worth's printed page with the
manuscript folio; the correction is well-evidenced. ✓

**Daniel (120 ac) absence — strong negative, not absolute.** A comprehensive
sweep of the typed folio index finds no John Greene → Daniel Greene 120-acre
grantee entry; every "Daniel Greene" reference is as a boundary neighbor.
CAVEAT: the folio index is a typed modern compilation whose OCR (`.txt`) is
garbled; a Daniel entry mangled beyond recognition cannot be fully excluded
from OCR text, and the Complete Volume PDF's text layer is non-searchable OCR.
The negative is strong but a human should eyeball the folio-index **PDF** (not
just the OCR) for any Daniel Greene grantee before treating absence as proven.
Flagged as 🟢 NEGATIVE-pending-visual-confirm in the finding.

**Mark analysis — AI-read.** "No bow-and-arrow mark; only Tibbitts's capital
'H'" is well-supported (Joan does not sign or mark at all on this instrument),
but the exact shape of Tibbitts's mark and the absence of any Joan mark must be
confirmed by human eyes on the full-res image. The bow-and-arrow tradition
belongs to the separate Anashuecot attestation, not this deed — correctly
stated.

**Circular citation check — clean.** Finding cites Worth 1921 + the colony
manuscript + the folio index as independent anchors; no source cites another in
a loop. ✓

**"Joan ux/Henry [Brightman]" Name Index entry — correctly flagged** as a likely
index error pending visual confirmation; not overclaimed as a second Joan. ✓

**Unsupported inference / narrative smoothing — none detected.** The finding
locates a document and reads it; it does not resolve Joan's identity or
eliminate any of models A–H. No premature elimination, no centering. ✓

---

## 03 — Synthesizer (bounded claims, preserved contradictions, status tags)

| # | Bounded claim | Status |
|---|---|---|
| 1 | Joan's deed is located in the original manuscript at RI State Archives Land Records No. 1, folios 259–260 (image `_133`). | 🟢 PROOF (location) |
| 2 | Joan = wife of John Greene, named as life-annuity beneficiary ("after his decease to Joane Greene his wife for and Dureing her naturall life"); she does not sign/mark. | 🟢 Joan's non-signature / no mark CONFIRMED by owner (2026-09-09); verbatim wording still 🟡 AI-read |
| 3 | No "or to her mother if she survive" / matrilineal reverter clause in this instrument. | 🟢 CONFIRMED by owner (2026-09-09) — no mother clause (matches AI read) |
| 4 | No bow-and-arrow mark on this deed; the only mark is Henry Tibbitts's "H." | 🟡 AI-read (Joan's *absence* of a mark is confirmed; the exact shape of Tibbetts's mark remains AI-read) |
| 5 | Daniel (120 ac) instrument absent from the colony volume (folio-index sweep). | 🟢 NEGATIVE-pending-visual-confirm |
| 6 | Recording authorities: acknowledged before John Fones (Warden), entered by John Sanford (Recorder). | 🟡 AI-read; Fones/Tibbetts/John Greene *visible* confirmed by owner (2026-09-09); the Warden/Recorder *roles* remain AI-read |

**Preserved contradiction (PARTIALLY RESOLVED):** the "or to her mother if she
survive" clause is **owner-confirmed ABSENT** from the colony original (folios
259–260, 2026-09-09). The phrase remains unattributed to any primary or
secondary source, so as an *evidence claim* it is effectively killed. What is
**not** resolved: the NK town-book copy (Image 10) has been AI-read **twice with
conflicting results** (Read A: "him or his Wife"; Read B: standard "John then
Joan his wife" form). **Both NK reads are retained as conflicting and PENDING
HUMAN REVIEW; neither is privileged.** The colony original and the NK copy are
different physical documents; do not conflate them.

**Identity scope:** this finding advances Joan's **document location and
reading**, NOT her identity (models A–H unaffected). Correctly bounded. ✓

**No claim here promotes to PROOF for the transcription.** All transcription
claims remain 🟡 pending the owner. ✓

---

## 04 — Explorer (sideways context, where evidence hides)

**Witness cluster (ties Joan's deed to the Quidnessett/Narragansett network):**
- Henry Tibbitts (mark "H") — recurring Quidnessett witness; appears in the
  18 Oct 1686 associate-purchase lead (RECON_QUEUE R4). Cross-reference his
  other attestations.
- Arthur Aylworth/Aylsworth — Narragansett/Punkatest family; relevant to the
  Indigenous-context and Anashuecot threads. An Aylsworth attested sachem
  deeds nearby (folios 262–263: Mamanuett/Saconet).
- John Nutsn/Nuton (Newton) — trace across Greene-family deeds.

**Neighbors/boundaries:** Daniel Greene (southerly) = the 120-acre Daniel
instrument holder; Quidnessett harbour (easterly); John Greene's own land
(northerly); highway (westerly). The 60-acre James tract sits within the Greene
home-place complex beside Daniel's 120 acres.

**Officials:** John Fones (Warden) and John Sanford (Recorder) are recurring
colonial clerks — index every Greene deed they acknowledged/recorded for
pattern (recording-clerk consistency across the James vs Daniel instruments).

**Jurisdiction (Law 5 — No Jurisdictional Assumption):** the deed frames the
land as "Aquednesett in the King's Province in the Narragansett Country" — the
contested Narragansett Country (RI/CT/Mass/Plymouth claims). "King's Province"
is itself a jurisdictional claim; record it as the deed's framing, not as
settled jurisdiction.

**Where evidence may be hiding in plain sight:**
- **The Daniel 120-ac instrument (NK town book, DGS 008204949 Image 10):** the
  colony version has no "mother" clause; the NK town-book copy may word it
  differently. Re-read Image 10's AI transcription against this colony read — a
  discrepancy between the two copies would be material.
- **R1 — 1685 Clark→Brinley deed:** may name who held the Greene land in 1685
  ("his widow" would give Joan a second appearance + a death window). Custody
  located (Jamestown Town Clerk / RI State Archives microfilm); still unread.
- **Folio-index "Mary Green wife of John, Sarah Barker wife of James, Priscilla"
  (1674 probate):** a possible second Greene-woman appearance — trace which
  John and whether it touches Joan's household.
- **Complete Volume PDF (222 pp):** a human could visually scan folios around
  259–260 and the Daniel-neighbor region for any unindexed Greene instrument
  the typed index missed.

**Indigenous context:** the Greene land at Quidnessett/Aquednessett sits on
ancestral Narragansett territory; nearby sachem deeds (Mamanuett/Saconet,
folios 262–263) contextualize the colonial land regime. The Anashuecot /
bow-and-arrow tradition is a separate attestation, not this deed.

**Disprove paths:**
- Disprove "no mother clause" → paleographer finds the clause in the manuscript.
- Disprove "Daniel absent" → human finds a Daniel Greene grantee entry in the
  folio-index PDF or the manuscript itself.
- Disprove "Joan doesn't sign" → human finds a Joan mark on the deed (the AI
  read says none).

---

## Sign-off status

**Status:** PENDING_HUMAN_REVIEW (partially advanced). The owner (Wendy Green)
paleographically confirmed three points against the colony original on
2026-09-09 — (1) Joan does not sign and makes no mark; (2) no "or to her mother"
clause; (3) Fones, Tibbetts, and John Greene are visible. Those three are now
🟢 owner-confirmed. The verbatim secretary-hand **wording** of the annuity clause,
the exact shape of Tibbetts's mark ("H"), and the recording authorities'
**roles** (Warden / Recorder) remain 🟡 AI-read, pending the owner's separate
confirmation. The NK town-book copy (Image 10) is a separate, still-unverified
manuscript. Per the safety rules, a human must inspect the original before
anything updates `evidence/`, `people/`, or public pages; the owner's
paleography of the remaining transcription tokens is the next gating step.
