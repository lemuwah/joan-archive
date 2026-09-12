# Auto-Agent Handoff — How to Continue the Quest (2026-09-09)

**For any agent picking this up (human or AI, credited or not).** The mission: find Joan's family. This file is the current state of the machine. Read [methodology/agent_orientation.md](../methodology/agent_orientation.md) first for the laws and the four verified facts; this file is what to DO.

---

## The machine, as built today

1. **The Greene Net** ([methodology/collection_policy.md](../methodology/collection_policy.md)): any Greene variant, 1600–1750, any geography → captured as a tagged lead. Capture ≠ claim.
2. **The funnel**: findings land in `research_findings/*.md` → `python3 tools/findings_pipeline/route_findings.py` generates four review packets per finding (Archivist → Hostile Review → Synthesizer → Explorer) in `research_queue/finding_runs/YYYY-MM-DD/<finding>/`. Run with `--check` to verify freshness. **Everything stays PENDING_HUMAN_REVIEW until a human reads the original record.** Nothing promotes to a people page, the index, or the site without passing the steps.
3. **The queue**: [RECON_QUEUE.md](RECON_QUEUE.md) — 51 leads, tiered, each with status. The road map: [research/road_to_joan.md](../research/road_to_joan.md).
4. **The registries**: [methodology/name_variant_registry.md](../methodology/name_variant_registry.md) (people) + [data/geography.yml](../data/geography.yml) + [research/geography_index.md](../research/geography_index.md) (places, with scribal variants). **Every search runs the full variant clusters, not bare modern spellings.** OCR hygiene: subtract "Greenwich"/"Green's Harbor" place-name collisions from Greene-person greps.
5. **The ghost register**: [evidence/ghost_names.md](../evidence/ghost_names.md) — names with no evidence trail, suspended, kept separate, still searched.
6. **The calibration study**: [research/neighbor_wives_comparison.md](../research/neighbor_wives_comparison.md) — the test that tells us what Joan's silence means. 5 of 10 peer wives now visible; 5 unresolved.
7. **The candidate protocol**: any surfaced Joane gets the geographic test — [research/joane_swyft_test.md](../research/joane_swyft_test.md) is the standing example (T1/T2 done, T3–T5 open).

## Free work — no credits needed (verified method)

**The IA `_djvu.txt` method:** find the identifier → `curl -sL "https://archive.org/download/<id>/<id>_djvu.txt"` → grep locally with the full variant clusters. Reproducible, costs nothing but time. Done so far: Minor diary (NULL), Austin 1887 (4 wives resolved), La Mance 1904 (ghost origins), Turner 1877 (NULL), Potter 1835 (Joan NULL + variant verification), Bartlett RI vols. 1–3 (Joan NULL + Smith letter location + Charles Greene find), Savage vols. 1–2 (NULL), Plymouth vols. 1–2 (NULL + Swyft).

**Ready to run, texts identified:**
- Plymouth vols. 3–4 (1651–1668) — closes the Swyft T1 endpoint. The Shurtleff series continues; find the next `recordsofcolony…` identifier pair (v.3–4 per the series description) and sweep for Swyft/Swyft-variants.
- Bartlett RI vols. 4+ (1706+) — `recordsofcolonyo04rhod` and siblings are already identified on IA.
- Narragansett Historical Register issues — `sim_narragansett-historical-register-plantations_*` series on IA (multiple issues found 2026-09-09, not yet swept).
- RIHS Collections — the correct vols. XI–XII scan (Bates) is still unidentified; the identifier `rhodeislandhisto09rhod` is vols. 18–19, wrong.
- F.L. Greene 1894 — not on IA by metadata search; try HathiTrust/Google Books.

**Housekeeping that costs nothing:** queue status updates after each run, NEGATIVE_LOG rows for every null, geography/variant registry maintenance, people-page structure work (never new claims — claims go through the funnel).

## Human-gated (the frontier — short list, high yield)

| # | What | Where | Unlocks |
|---|---|---|---|
| H1 | FamilySearch session: DGS 008204949 — hi-res Image 9 index read (Greene rows → James page), then sweep from Image 13 | any FamilySearch center / affiliate library | The James instrument; possibly more Greene pages |
| H2 | 25 Sep 1685 Clark→Brinley deed | Jamestown Town Clerk (originals) or RI State Archives (microfilm) | C-2 death date; possible "his widow" = Joan's 2nd appearance |
| H3 | RIHS pulls: **Mss 461** ("will complaint") + the **Richard Smith letter of 14 May 1664** original (location confirmed via Bartlett's footnote 2026-09-09) | RI Historical Society, Providence | Post-1682 Joan reference candidate; the full arrest packet |
| H4 | NEHGS americanancestors.org session | paywall | Probate abstracts for the 5 unresolved calibration households (Briggs, Waterman, Greenman, Smith Jr., Carpenter) |
| H5 | Native Northeast Portal browser session | nativenortheastportal.com | The 11-variant Anashuecot sweep (list staged in his page) |
| H6 | MHS Ask-a-Librarian — Winthrop Jr. casebooks query | masshist.org | The "wife of John Greene" class of record; query text staged in research_findings/2026-09-09_sideways-lanes-first-runs.md |

## Standing warnings for agents

- **Verify the book before sweeping it** (the Plymouth scan wore an RI title).
- **Agreement between agents is not corroboration.** Two AIs citing the same bad source = one bad source.
- **La Mance-derived claims are contamination**, including when they arrive via modern compiled trees. The ghost register has the known constructions (Enfield, Welthian, "daughter Joan," Robert, "Nawham's wife," Tocomminon pending its affidavit).
- **Community-governed sources are approached by protocol, never extracted** (D-005; contribute.html consent language).
- The owner reviews pending_human_review.md — that's where human observations go between sessions.

## State at handoff

- 14 findings, 56 review packets, funnel verified clean at commit `4d2578a`+
- Tasks 1, 2, 3, 4, 6 DONE (grep-verified); Task 5 awaiting owner decision; Task 6.5 tooling built, needs `last_known_seq` values
- Joan: still one verified appearance. The silence map is now machine-verified across colony records, genealogies, diaries, and compiled families, 1636–1706. The search continues sideways: households, annuities, witnesses, scribes.
