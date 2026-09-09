# Archivist Queue Packet — research_findings/2026-09-08_public_source_provenance_bundle.md

**Finding ID:** `FINDING-7c1fbabe4094`
**Status:** `PENDING_HUMAN_REVIEW`
**Source SHA-256:** `c36388d847ca5b02e181a8353ca46f4d308cb098723f0794be548daf1d29e6ce`
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
# Public Source Provenance Bundle — Greene Identity Comparison

**Date accessed:** 2026-09-08  
**Collector:** Copilot  
**Purpose:** Preserve reproducible public-domain comparison sources for the Surgeon John Greene and the other early Rhode Island Greene lines without allowing secondary genealogy to become proof about Joan.

## Provenance rule

These are public scans and OCR files, not newly examined colonial manuscripts. The Internet Archive item page is the catalog authority; the downloadable OCR hash identifies the exact derivative searched on 2026-09-08. OCR is a finding aid. It is not a quotation unless a reviewer checks the scan page itself.

No source in this bundle establishes Joan's maiden name, parentage, or identity. Clarke is especially important as a firewall: it explicitly limits its genealogy to the descendants of John Greene, surgeon.

## Source inventory

| ID | Work | Stable item | Downloaded derivative | SHA-256 | Use | Status |
|---|---|---|---|---|---|---|
| PUB-001 | George Sears Greene, *The Greenes of Rhode Island*, 1903 | [Internet Archive item](https://archive.org/details/greenesofrhodeis00gree) | `greenesofrhodeis00gree_djvu.txt` | `196e608536244aae797aa83c9394d0b38ade9bdf7b4dac550964b8197e856752` | Surgeon line, scope firewall, Warwick descendants | Secondary genealogy; comparison only |
| PUB-002 | John Osborne Austin, *The Genealogical Dictionary of Rhode Island*, 1887 | [Internet Archive item](https://archive.org/details/genealogicaldict00aust) | `genealogicaldict00aust_djvu.txt` | `d64f1a04bd30cdfc126f43b64038baca260d9f6267a4c76cc2434e1cd4250787` | Independent genealogy comparison and name collisions | Secondary genealogy; comparison only |
| PUB-003 | *Records of the Colony of Rhode Island and Providence Plantations*, 1856, volume 1 | [Internet Archive item](https://archive.org/details/recordscolonyrh01islagoog) | `recordscolonyrh01islagoog_djvu.txt` | `f05ae579badf7ba753492e6874b7c1e52a949643e08ca2a5124d0c76f9fcab8c` | Colony-level record search; official printed edition | Published record edition; verify scan/page |
| PUB-004 | *Records of the Colony of Rhode Island and Providence Plantations*, 1856, volume 3 | [Internet Archive item](https://archive.org/details/recordscolonyrh03bartgoog) | `recordscolonyrh03bartgoog_djvu.txt` | `5721cdd33a2c95f71ea9021f4ca233da7dcc663bcc696ef36eddbb9547f600fd` | Colony-level record search; official printed edition | Published record edition; verify scan/page |
| PUB-005 | Dorothy Worthington, *Rhode Island Land Evidences, vol. I, 1648–1696: Abstracts*, 1921 | [Internet Archive item](https://archive.org/details/rhodeislandlande00wort) | `rhodeislandlande00wort_djvu.txt` | `a2e2b2754a7be20d086d2e386f7bc943a3332a3eaf619e9c94e6b5a2bf4b1bcf` | Existing abstract source; comparison baseline only | Secondary abstract; not the deed manuscript |
| PUB-006 | John Winthrop, *Winthrop's Journal: History of New England, 1630–1649*, 1908 | [Internet Archive item](https://archive.org/details/winthropsjournal00wint) | `winthropsjournal00wint_djvu.txt` | `fd1597cbb690cdb3269b863cbaa831c7533cf3a6f4097acd7f4e49cf59c292cd` | Exact published wording behind the Beggerly reference | Published primary-source edition; verify scan/page |

The source metadata identifies PUB-001 as George Sears Greene, 1903; PUB-002 as John Osborne Austin, 1887; and PUB-005 as Worthington/Rhode Island Historical Society, 1921. The record volumes are cataloged as 1856 Rhode Island publications.

## Verified-from-scan targets

### PUB-001 — Clarke/Greene scope firewall

The OCR around its introductory matter states:

> “There were three distinct families of Greene settled in Rhode Island at an early date, the progenitors of whom all bore the name John. But the present work embraces only the descendants of John Greene, surgeon...”

The same public scan identifies:

> “John Greene, surgeon, born about 1590, of Salisbury, County Wilts. He married November 4, 1619, at St. Thomas Church, Joanne Tattershall. He emigrated to New England with his family in 1635...”

The searchable OCR returned no hits for `Quidnessett`, `Cocumscussoc`, `Beggarly`, or the exact phrase `Joan Greene`. Those are absence results from one OCR derivative, not proof that no related material exists elsewhere in the book or manuscript tradition. A human reviewer should confirm the scope and Surgeon passages against the page images before quoting them publicly.

**Interpretation allowed:** Clarke is useful to separate the Surgeon family from the archive’s Quidnessett John.  
**Interpretation forbidden:** Clarke cannot prove that Joan was English, related to the Surgeon, or “Joan Beggarly.”

### PUB-006 — Winthrop’s Beggerly passage

The public 1908 edition records:

> “one Greene (who hath married the wife of one Beggerly, whose husband is living, and no divorce, etc., but only it was said, that he had lived in adultery, and had confessed it)...”

This is what the source says: Winthrop names “one Greene” and describes the woman as the wife of one Beggerly. It does **not** call her Joan, does not call “Beggarly” her maiden name, and does not identify that Greene as the Quidnessett John. Any later identification of this woman with Joan of the 1682 deed is an inference requiring independent evidence. The archive’s La Mance Law therefore treats “Joan Beggarly” as a contaminated identification, not a source fact.

## Identity comparison map

| Identity | Public comparison evidence | What it can establish | What remains open |
|---|---|---|---|
| Surgeon John Greene of Warwick | Clarke 1903; colonial records volumes; parish/probate material cited by the archive | A distinct Salisbury/Warwick line with Joanne Tattershall and later Phillippa; a Surgeon designation | Every attribution still needs the cited page or manuscript, not just Clarke’s pedigree |
| John Greene of Quidnessett | Worth 1921 abstract; Fones record; 1679 affidavit; 1682 North Kingstown image already held by the archive | A separate Narragansett/Quidnessett documentary trail; Joan is named in the 1682 deed | Joan’s origin and maiden name; full original deed transcription; exact identity of ambiguous Johns |
| John Greene of Newport / other regional Johns | Bates and colonial records as secondary or published trails | Candidate identity collisions requiring source-specific descriptors | Whether aliases refer to Quidnessett John; do not merge on name alone |

## Reproduction instructions

1. Open the stable Internet Archive item link.
2. Download the named `_djvu.txt` derivative.
3. Calculate SHA-256 and compare with this table.
4. Locate the passage in the scan, not only OCR.
5. Record printed page, image/page URL, exact quotation, and reviewer/date in the relevant evidence file.
6. If the scan contradicts OCR, retain the OCR as a failed derivative and cite the scan reading instead.

## Not found in this public pass

No public scan was located for the original North Kingstown deed book, Peirce Manuscripts films 22291–22292, the Jamestown town-record deed cited by Bates, or RIHS Mss 461. Those gaps remain access requests or interactive FamilySearch/archive tasks. See `primary_sources/NEGATIVE_LOG.md` for the scoped search record.

*Maintained under the Multi Agent Laws, especially Law 2 (La Mance Law), Law 4 (No Algorithmic Contamination), and Law 7 (No Trust Without Evidence).*
```

## Required output
Record source anchors, uncertainty, contradictions, and next actions. Keep person identity separate from name similarity.
