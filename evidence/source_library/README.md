> This archive documents lives lived between approximately 1600–1750 in Narragansett country (present-day Rhode Island). All records from this period were created within colonial legal systems and reflect their biases, categories, and blind spots. Every name found here — English, Narragansett, Niantic, mixed-heritage, unknown — represents a real person whose full story these records were not designed to capture. Content may include references to war, captivity, enslavement, displacement, legal coercion, and loss. These are documented realities of the period, not abstractions. All cultural and genealogical content is included for research purposes in the quest to identify Joan Unknown Greene and will be revised or removed if requested by descendant communities or tribal representatives.

# Source Library — Large Document Fetch & Transcription Pipeline

**Purpose:** Make large compiled primary sources searchable and local. Pure archivist work — no interpretation, no synthesis. Just making the source material available so any agent can search across the whole collection.

---

## Pipeline

1. **Fetch** the full PDF/DjVu from Internet Archive / Wikimedia Commons / institutional repository
2. **Chunk** into searchable sections (by page range, by topic, by name cluster)
3. **Transcribe** each chunk to plain text with page references preserved
4. **Tag** primary vs derivative content within each chunk
5. **Store** in `evidence/source_library/<volume_key>/` with an index file
6. **Spot-check** transcription accuracy against source images (hostile reviewer protocol)

## Priority Targets

### Tier 1 — Directly relevant to Joan and the 12-name experiment

1. **RI Land Evidences Vol. I (Worth, 1921)** — ✅ ALREADY ON REPO as `worth_djvu.txt` (528 KB, 15,396 lines). Needs chunking and indexing only.
   - Internet Archive: https://archive.org/details/rhodeislandlande00rhod
   - Status: Raw text on repo, not yet chunked or indexed

2. **Fones Record** — The Fones family compilation with Narragansett country connections
   - Wikimedia Commons URL: [TO BE CONFIRMED]
   - Status: Not yet fetched

3. **Narragansett Historical Register, Vols. 1–4** — Mixed primary/derivative, heavy on NK/Narragansett families
   - Internet Archive: search `narragansett historical register`
   - Status: Not yet fetched
   - ⚠️ Contains both primary transcriptions AND secondary analysis — must be tagged per chunk

4. **Arnold's Vital Records of Rhode Island** — Compiled vital records (births, marriages, deaths)
   - Internet Archive: multiple volumes
   - Status: Not yet fetched
   - ⚠️ Derivative compilation — Arnold extracted from town records, not original documents

### Tier 2 — Contextual / supporting

5. **Rhode Island Colonial Records (RICR)** — General Assembly acts, colonial administration
   - Where digitized: varies by volume; some on Google Books, some Internet Archive
   - Critical for: 1676 legislation, jurisdictional disputes, captive dispositions
   - Status: Not yet fetched

6. **RIHS Collections Guides** — Finding aids for Rhode Island Historical Society collections
   - Status: Not yet fetched
   - Note: These tell us what EXISTS, not what the documents SAY

## File Structure

```
evidence/source_library/
├── README.md                          ← this file
├── worth_1921_ri_land_evidences/
│   ├── index.md                       ← volume-level metadata, chunk inventory
│   ├── chunks/
│   │   ├── docs_001-050.md            ← instruments 1–50 with page refs
│   │   ├── docs_051-100.md
│   │   ├── docs_101-150.md
│   │   └── ...
│   └── spot_checks/
│       └── accuracy_log.md            ← hostile reviewer transcription checks
├── fones_record/
│   ├── index.md
│   ├── chunks/
│   └── spot_checks/
├── nhr_vol1/
│   ├── index.md
│   ├── chunks/
│   └── spot_checks/
├── nhr_vol2/
├── nhr_vol3/
├── nhr_vol4/
├── arnold_vital_records/
│   ├── index.md
│   ├── chunks/
│   └── spot_checks/
└── ricr/
    ├── index.md
    ├── chunks/
    └── spot_checks/
```

## Chunking Rules

- Each chunk is a self-contained markdown file
- Page references from the original are preserved in the text (e.g., `[p. 47]`, `[p. 48]`)
- Chunk boundaries follow the source's own structure (by instrument number, by page range, by section heading) — never mid-document
- Each chunk header contains: volume title, chunk range, page range, date range covered, source URL
- Chunk filenames follow the pattern: `docs_NNN-NNN.md` or `pages_NNN-NNN.md`

## Tagging Rules

Every chunk gets tagged at the top:

```markdown
---
source_type: PRIMARY | DERIVATIVE | MIXED
original_repository: [where the original documents live]
this_transcription: [who made this transcription — Worth? Arnold? Unknown?]
transcription_date: [when was this transcription made]
digitization_source: [Internet Archive / Wikimedia / Google Books / etc.]
digitization_url: [URL]
spot_checked: false
---
```

- **PRIMARY** = the text is a direct transcription of an original document (deed, will, court record)
- **DERIVATIVE** = the text is someone's compilation, summary, or analysis of original documents
- **MIXED** = the volume contains both (common for NHR)

## Quality Control — Hostile Reviewer Protocol

For each volume, a sample of chunks gets spot-checked against the source images:

1. Pick 3–5 chunks at random
2. Compare transcribed text against the original page image
3. Log discrepancies in `spot_checks/accuracy_log.md`
4. Rate: RELIABLE / CAUTION / UNRELIABLE
5. If UNRELIABLE, flag the entire volume and note specific error patterns

This is not about perfection — it's about knowing how much to trust each transcription.

## What This Pipeline Does NOT Do

- ❌ Does not interpret documents
- ❌ Does not synthesize findings across documents
- ❌ Does not add names to the people/ index
- ❌ Does not merge identities
- ❌ Does not touch the main archive index
- ❌ Does not replace primary_sources/ (which holds individually curated, Joan-relevant documents)

This is the raw material shelf. Agents and researchers pull from it; it doesn't push to anything.

---

> **Search direction bias check:** When an agent recommends "where to look next," ask: is this recommendation biased toward digitized, English-language, colonial-framework sources? What record types exist that this agent might not know to suggest? What would a Narragansett historian, a maritime historian, an archaeologist, a linguist look for that a genealogist wouldn't?

This pipeline is explicitly biased toward digitized, English-language, colonial-framework sources — it's fetching published compilations of colonial legal records. It cannot capture: undigitized town records still in local vaults, Narragansett oral history, archaeological evidence, maritime records not compiled by these editors, or documents in languages other than English. The pipeline makes searchable what's already been published; it does not discover what hasn't.

---

*Joan Archive — evidence/source_library/README.md*
*Nothing is proven until original proof images are on the archive.*