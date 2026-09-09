# Collection Policy — The Standing Logic of What We Gather and How

**Status:** ACTIVE — adopted 2026-09-09 by the archive owner
**Authority:** The Multi Agent Laws ([theory/three_laws.md](../theory/three_laws.md)) and [AGENT_GUARDRAILS.md](../AGENT_GUARDRAILS.md) are supreme. This file operationalizes them for collection work. It does not override them.
**Purpose:** One place that states what enters the archive, how it is filed, how consent is protected, and how every page doubles as a discovery surface for searchers — human and AI.

---

## §1 The Greene Net — the capture rule

> **If a record says Greene (in any spelling) and was created 1600–1750, we want to see it. No matter where it is from.**

- **Scope:** any record, any repository, any geography, any language, dated 1600–1750, naming **Greene / Green / Grene / Greane / Groon / Groen / Creene / Creen / Greeu / Greeue** or any variant listed in [name_variant_registry.md](name_variant_registry.md).
- **Capture ≠ claim.** A capture is a *lead*, not evidence about Joan or our John. Every capture enters as a dated lead card tagged with its provenance level (📔 📚 🌐 ⚠️) and `PENDING_HUMAN_REVIEW`.
- **No pre-filtering by plausibility.** A Greene in Barbados shipping records in 1661 or a Greene in a New Amsterdam court minute in 1649 gets captured and filed, not judged at the door. Relevance is decided *after* filing, in hostile review, with the reason recorded either way.
- **Discard only with a reason.** A lead may be closed only by a scoped negative or a documented elimination — never by vibe. Closed leads stay in the record so the next agent does not re-chase them.
- **Date rationale:** 1600 opens the net before any plausible birth year of Joan's parents' generation; 1750 closes it after the death of the last person who could have known her. Adjust only by owner decision.

## §2 Geography-first filing — with the scribe's own spellings

- Every captured lead is filed under **every** region it touches, using the geographic index:
  - machine-readable: [data/geography.yml](../data/geography.yml)
  - human-readable: [research/geography_index.md](../research/geography_index.md)
- **Each region carries every spelling variant found in period records, attributed to who wrote it down and when, wherever that attribution is known.** Colonial scribes spelled by ear and by habit; the same place appears under a dozen forms across jurisdictions. A search that uses only the modern spelling is a partial search.
- **Variant attribution is honest.** If the archive has not yet tied a spelling to a specific scribe or record, the variant is listed as `unattributed` — never invented. Scribe attributions are tagged like any other claim.
- **Same place, different label ≠ same label, different place.** Both errors are recorded in [contradictions/](../contradictions/index.md) when found. The index distinguishes identity-of-place claims from spelling variants.

## §3 Names — the variant search rule

- Every search of a person uses the full variant cluster from [name_variant_registry.md](name_variant_registry.md): standard, scribe drift, OCR-plausible, phonetic.
- **Log what was searched.** Variants actually queried are recorded in the page's `## Search Log` and, for negatives, in [primary_sources/NEGATIVE_LOG.md](../primary_sources/NEGATIVE_LOG.md) — repository, query string, date range, record type. A negative is only as wide as its logged query.

## §4 Consent and confidentiality — non-negotiable

- **Living people appear at institution level only, unless they have given written consent.** No helper, custodian, librarian, researcher, or family member is named in the public archive beyond their stated consent level. No personal emails, phone numbers, or addresses ever.
- **The dead deserve care too.** Indigenous persons described in colonial records carry the 📖 EXTERNAL INTERPRETATION tag (D-005). Descendant communities and tribal representatives can request revision or removal of any content (universal disclaimer, [methodology/universal_disclaimer.md](universal_disclaimer.md)).
- **Suspended claims stay suspended** until the document is read (D-001, D-006). Consent, mark, and signature claims about Joan require the manuscript.
- **CARE-B checkpoint** (D-004) applies to every public-facing commit: Collective benefit, Authority respected, Responsibility for harm, Ethical review, Bias check.
- **Standing scan.** Before any merge to the public site, run the confidentiality scan (names of known helpers, email patterns, phone patterns) and confirm zero unconsented hits. The scan command lives in [methodology/git_audit_checklist.md](git_audit_checklist.md).

## §5 Every page is a discovery surface — the AI search bot rule

People pages are written so that **any** search bot — an external AI research agent, a genealogy crawler, or our own funnel — can match a new record to the right person slot.

Each person page therefore carries, in machine-friendly plain text:

1. **All name variants** (from the registry) — so "Aquednesit Green" or "Goodwife Grene" still lands.
2. **Date range of documented activity** — so a 1661 record can be included or excluded honestly.
3. **All geographic anchors with variants** — so a record filed under "Acquidnessett" matches a page filed under "Quidnessett."
4. **Documented associates** — witnesses, neighbors, co-purchasers — because sideways records often name the associate when they do not name the target.
5. **Record anchors** — exact repository / volume / page / image identifiers for what we already hold, so bots do not re-offer us what we have and can verify what we cite.
6. **Honest status tags** — 🟢 PROOF / 🟡 PLAUSIBLE / ⚠️ UNVERIFIED / 🔴 ELIMINATED and the provenance tags. **Discoverability never inflates confidence.** A bot that lands here must leave knowing exactly what is and is not proven — that honesty is what makes the archive a trustworthy node in the wider search ecology.

The same block is our own agents' search key. One structure, two directions.

## §6 Zoom alignment

Collection follows the document ecology zoom model ([tools/document_ecology/collection_model.json](../tools/document_ecology/collection_model.json)): **L0** the exact page → **L1** household → **L2** associates → **L3** locality → **L4** jurisdiction → **L5** region/Atlantic. A capture at any zoom level names the level it belongs to. The network roadmap ([research_findings/2026-09-09_network-roadmap.md](../research_findings/2026-09-09_network-roadmap.md)) is the current expansion plan.

## §7 Nothing is promoted without the document

Law 7: no claim, person, place-variant attribution, or scribe identification is promoted past ⚠️ UNVERIFIED / 🌐 TERTIARY without the original or an authoritative reproduction being read. AI transcription remains AI transcription. Agreement between agents is not corroboration.

---

*Filed leads feed the findings funnel ([research_findings/README.md](../research_findings/README.md)): Archivist → Hostile Review → Synthesizer → Explorer. This policy governs what enters that funnel and how it is filed.*
