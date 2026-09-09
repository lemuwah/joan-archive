# Evidence Pipeline

This is the operating contract for AI-assisted discovery of primary documents about Joan Unknown Greene and the Narragansett region.

The pipeline separates **finding** a source from **trusting** a source. Agents may discover, extract, compare, and challenge. They may not publish a claim as verified.

## Flow

```text
seed questions
  -> research_findings intake
  -> archivist provenance pass
  -> hostile review
  -> synthesizer bounded proposal
  -> explorer sideways-context action
  -> human decision
    -> evidence/ and timeline update
```

Every candidate starts in `PENDING_HUMAN_REVIEW`. Only a human can move it to `VERIFIED_PRIMARY`, `VERIFIED_SECONDARY`, `REJECTED`, or `SUSPENDED`.

## Agent roles

### Explorer / Collector

Searches approved repositories and records candidate URLs, search terms, dates, jurisdictions, and negative results. It must never silently treat search-result snippets, OCR, or a secondary citation as the document itself.

Output: candidate source record.

### Archivist

Checks the candidate's provenance, downloads or links the actual document when permitted, records repository identifiers, page or image numbers, checksum, and access date, then maps proposed claims to exact document locations.

Output: provenance record and claim-to-source map.

### Transcription assistant

Produces a rough transcription or image description. It must preserve uncertainty with `[?]`, `[illegible]`, and omissions. Its output is a lead, never a quotation.

Output: AI-SOURCED working transcription.

### Specialist agents

Run these alongside the general Explorer and Archivist when the question requires a
different perspective:

- **Identity disambiguator** — separates same-name people using dates, places, kinship,
  witnesses, and documentary context; it never merges on a name alone.
- **Historical-status agent** — tests servant, indentured, captive, enslaved, free, and
  colonial status terminology while preserving the source's exact wording and limits.
- **Paleography and variants agent** — compares letterforms, marks, aliases, scribal
  formulas, and spelling variants against the original image and the name registry.
- **Irish/Scottish migration agent** — tests Ireland, Ulster, Scotland, servant migration,
  apprenticeship, and transport records against a dated regional timeline.
- **Negative-space auditor** — records repositories, jurisdictions, date ranges, and
  record types searched without treating a scoped miss as proof of absence.

These are independent challenges, not a voting system. Agreement between agents does not
upgrade a candidate to verified evidence.

### Synthesizer

Compares verified source records across the timeline and proposes a bounded statement. It must separate `PROOF`, `PLAUSIBLE`, and `DISCREDITED`, and preserve contradictions rather than resolve them by narrative smoothing.

Output: proposed timeline event with source references.

### Explorer follow-up

Explorer runs after synthesis for every finding. It does not reopen a claim as
fact. It expands the context sideways: associated people, witnesses, neighbors,
institutions, jurisdictions, material records, Indigenous or non-English record
families, and other places the evidence may be hiding in plain sight.

### Hostile reviewer

Attempts to falsify the proposed event: wrong person, duplicate person, wrong date, retrospective source, colonial naming ambiguity, OCR error, missing page, or unsupported inference.

Output: review report and disposition recommendation.

### Human editor

Verifies the original scan or authoritative record, resolves the disposition, and makes any change to published evidence or timeline files.

## Candidate record contract

Store machine-generated candidates in `data/research/sources.jsonl` or a pending-review sidecar. Each record should contain:

```json
{
  "candidate_id": "CAND-2026-0001",
  "status": "PENDING_HUMAN_REVIEW",
  "source_url": "https://example.org/item",
  "repository": "Repository name",
  "repository_id": "stable identifier",
  "document_type": "deed|court|letter|map|genealogy|secondary",
  "date_range": "1674-09-29",
  "jurisdiction": "Narragansett country",
  "people_or_terms": ["John Greene", "Joan", "Quidnessett"],
  "retrieved_at": "2026-09-07T00:00:00Z",
  "sha256": "checksum of downloaded file when permitted",
  "image_or_page": "p. 49 or leaf 52",
  "access_notes": "public scan, login required, or manual capture",
  "ai_outputs": [],
  "proposed_claims": [],
  "negative_result": false,
  "human_disposition": null
}
```

Do not use `VERIFIED_PRIMARY` merely because an AI found a URL, produced OCR, or matched a name.

## Automated checks

- `data/research/source.schema.json` defines the candidate-record shape.
- `tools/evidence_pipeline/validate_records.py` validates candidate JSONL files, rejects
  duplicate IDs, requires scoped fields for negative searches, and requires human anchors
  before a record can be marked verified.
- `.github/workflows/validate-evidence-records.yml` runs the validator on pull requests that
  change research data or the evidence tooling. It deliberately ignores the legacy
  `sources.jsonl` catalog until those records are migrated to the candidate contract.

## Search strategy

Run collectors against independent source families, not only Google-style web search:

- Internet Archive and HathiTrust for public-domain printed volumes
- Rhode Island state and local archive catalogs
- Library of Congress and Chronicling America for maps, newspapers, and later references
- Indigenous history and language collections where access and cultural protocols permit
- Court, land, probate, military, maritime, church, and town records
- FamilySearch only through its permitted manual workflow for the deed-book image chain

Each run records both hits and meaningful misses. A miss is scoped to the repository, query, date range, and record type searched; it is not evidence that the record does not exist.

## Verification gates

A proposed timeline event cannot be promoted until all applicable checks pass:

1. The source is identified by a stable repository citation or image.
2. The relevant page, leaf, or image is available for human inspection.
3. The transcription is checked against the original; OCR remains labeled as AI-SOURCED.
4. Person identity, date, place, and document type are distinguished from similarly named people.
5. The claim is classified as `PROOF`, `PLAUSIBLE`, or `DISCREDITED`.
6. A hostile review records the strongest alternative explanation.
7. A human records the disposition and links the evidence into the archive.

## Recommended run model

Use one issue or research question per run. Give every agent the same immutable input bundle:

- current `theory/source_spine.md`
- `AGENT_GUARDRAILS.md`
- relevant `evidence/` files
- the current research queue item
- prior candidate records for deduplication

Agents should write new findings to `research_findings/` and new images to
`images/_pending_review/`. The ordered queue writes review packets to a
run-specific workspace first. A final consolidation job may produce a PR, but
it must never auto-merge or write directly to `evidence/`, `people/`, or
published timeline pages.

The existing `tools/next_page/` workflow is the first collector implementation. Its images belong in `images/_pending_review/` and its results require the same gates above.
