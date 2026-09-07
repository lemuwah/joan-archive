> This archive documents lives lived between approximately 1600–1750 in Narragansett country (present-day Rhode Island). All records from this period were created within colonial legal systems and reflect their biases, categories, and blind spots. Every name found here — English, Narragansett, Niantic, mixed-heritage, unknown — represents a real person whose full story these records were not designed to capture. Content may include references to war, captivity, enslavement, displacement, legal coercion, and loss. These are documented realities of the period, not abstractions.
>
> All cultural and genealogical content is included for research purposes in the quest to identify Joan Unknown Greene and will be revised or removed if requested by descendant communities or tribal representatives. Search direction bias check: When an agent recommends "where to look next," ask: is this recommendation biased toward digitized, English-language, colonial-framework sources? What record types exist that this agent might not know to suggest? What would a Narragansett historian, a maritime historian, an archaeologist, a linguist look for that a genealogist wouldn't?
> # Synthesizer — Site/Theory Reconciliation Pass
**Date:** 2026-07-15
**Agent:** Synthesizer
**Trigger:** User request to synchronize `index.html`'s embedded data against `theory/`
before queuing further Explorer/Archivist/Hostile Reviewer work.

---

## Summary of New Input

Diffed the live site's embedded JS data objects (`TIMELINE_DATA`, `OPEN_THREADS`,
`CONTAMINATIONS`, `JOHN_GREENE_ORIGINS`, `AWASHONKS_PARALLEL`, `NAME_FRAGMENTS`,
`PHONETIC_VARIANTS`, `COMPARATOR_WOMEN`, `CONVERGENCES`, `BEHAVIORAL_ANOMALIES`)
against `theory/source_spine.md`, `theory/john_firewall.md`, and
`theory/anashuecot_kin_map.md`. The site and the theory files had drifted in both
directions — the site was ahead in some places, behind in others.

## What Changed in the Theory

- `theory/source_spine.md` §6 (AI Contamination Log): added two entries present on
  the site but missing from theory (YourRoots "Alice Daniels" parentage fabrication;
  La Mance circular pedigrees).
- `theory/source_spine.md` §7 (Open Threads): added threads #8 and #9 from the site
  (DNA/haplogroup audit; Coginiquant name-cluster), and flagged an unresolved
  contradiction on thread #4 (site marks it done, theory files don't).
- **New file** `theory/john_greene_origins.md`: the site's `JOHN_GREENE_ORIGINS`
  Y-DNA/alias-surname thesis had zero presence anywhere in `theory/` before this pass.
  Filed as its own thread, explicitly unreviewed, with an internal haplogroup
  contradiction (R-Z255 vs. R-FTB79899) flagged as the first thing to resolve.
- `theory/anashuecot_kin_map.md` §4: added the Awashonks external-comparator entry
  from the site's `AWASHONKS_PARALLEL`, marked unverified pending citation check.

## What Stayed the Same

- Tier 1/Tier 2 status unchanged.
- No status tag (🟢/🟡/⚪/⚫) on any existing anchor was upgraded or downgraded —
  everything synced in from the site was added at ⚪ UNVERIFIED or as a held-open
  contradiction, never as confirmed fact. Per Law 1, none of this was smoothed.
- Joan Firewall and John Firewall entries unchanged (John Greene Origins was filed
  as a separate thread, not merged into the John Firewall, pending resolution).

## Where Updates Were Written

- `theory/source_spine.md` (edited)
- `theory/john_greene_origins.md` (new)
- `theory/anashuecot_kin_map.md` (edited)

## New Open Questions

1. Which haplogroup figure is correct for Kit B2778 — R-Z255 or R-FTB79899 — and are
   they even describing the same test?
2. Who marked site `OPEN_THREADS` item 4 (Fones "her marke" audit) as done, and where
   is that result recorded? It isn't in `gender_pattern_analysis.md`.
3. Have the Drake/Church citations behind the Awashonks parallel actually been
   checked by anyone, or only asserted?

## Contradictions Discovered

- Site vs. theory: two contamination entries and two open threads existed on the site
  only (now synced in, see above).
- Site vs. site: `JOHN_GREENE_ORIGINS` haplogroup (R-Z255) conflicts with
  `OPEN_THREADS` item 8's haplogroup (R-FTB79899) for what is presented as the same
  audit.

## Recommendation

The theory folder and the live site should now be reasonably aligned for the
Explorer/Archivist/Hostile Reviewer to work from. Before queuing new KPW-cycle work,
consider a dedicated queue item asking the Hostile Reviewer to attack
`theory/john_greene_origins.md` first — it's the single largest unreviewed claim now
sitting in the theory folder.

_Synthesizer reconciliation complete. No narrative smoothing applied._
