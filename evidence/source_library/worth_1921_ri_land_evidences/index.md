---
source_type: PRIMARY
original_repository: Rhode Island State Archives / Town Clerk offices
this_transcription: Henry R. Worth (1921)
transcription_date: 1921
digitization_source: Internet Archive
digitization_url: https://archive.org/details/rhodeislandlande00rhod
raw_file_on_repo: worth_djvu.txt
spot_checked: false
---

# RI Land Evidences Vol. I (Worth, 1921) — Index

**Full title:** Rhode Island Land Evidences, Vol. I, 1648–1696
**Editor:** Henry R. Worth
**Published:** Providence, 1921
**Corpus:** 445 instruments — deeds, wills, powers of attorney, settlements, dower releases, other legal records
**Raw text:** `worth_djvu.txt` in repo root (528 KB, 15,396 lines)

## Status

- ✅ Raw text on repo
- ⬜ Needs chunking into searchable sections by instrument number
- ⬜ Needs page reference preservation
- ⬜ Needs spot-check against source images
- ⬜ Needs cross-reference to 12-name experiment data CSVs

## Chunk Plan

Chunk by instrument number, ~50 instruments per chunk:

- `chunks/docs_001-050.md`
- `chunks/docs_051-100.md`
- `chunks/docs_101-150.md`
- `chunks/docs_151-200.md`
- `chunks/docs_201-250.md`
- `chunks/docs_251-300.md`
- `chunks/docs_301-350.md`
- `chunks/docs_351-400.md`
- `chunks/docs_401-445.md`

## Known Issues with the Transcription

- DjVu OCR quality varies — some pages may have character errors
- Worth's 1921 transcription modernized some spellings (need to verify against originals)
- Page numbers from the original volume may not map perfectly to the DjVu page numbers
- The raw file does not have clean instrument-number delimiters — chunking will require pattern matching on instrument headers

## Connection to 12-Name Experiment

This is the test corpus for the 12-name experiment (`methodology/12-name-experiment/`). Every female name occurrence in this volume gets logged in the experiment's data CSVs. The source library chunks provide the searchable text; the experiment CSVs provide the structured extraction.

---

*Joan Archive — evidence/source_library/worth_1921_ri_land_evidences/index.md*