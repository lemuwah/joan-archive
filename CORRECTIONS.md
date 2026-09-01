# Corrections Log

This archive makes mistakes. When we find them, we document the fix publicly — what was wrong, how we caught it, what changed, and what's still open. This is what peer-reviewed journals do. It's what keeps the archive credible.

---

## Correction #1: Pawtuxet Deed Citation Invalidated

**Date identified:** 2026-08-31  
**Date confirmed:** 2026-09-01  
**Severity:** CRITICAL — affected core evidence claims across the entire archive

### What was wrong

The archive listed a deed dated 19 May 1682 (John Greene → William Carpenter, £10, Joan's "free & voluntary consent") as **Tier 1 — Primary**, citing "Records of RI & Providence Plantations Vol. VII, pp. 177–178."

This was presented as Joan's second legal appearance — making her documentary footprint "two independent legal acts, five weeks apart." The README, live site, source spine, lifecycle matrix, and multiple research files all treated this as proven fact.

### How we caught it

During a Pawtuxet land investigation on 2026-08-31, the verbatim deed text could not be located in any digitized primary source (Worth's RI Land Evidences Vol. I, Chapin's Early Records of Warwick, Carpenter genealogy, Early Records of Providence, Bartlett Colony Records Vol. III). The citation was then tested directly:

- **Bartlett's Vol. VII covers 1770–1776** (Revolutionary era), not the 1680s
- **Pages 177–178 contain 1773 Gaspee commission records** — Chief Justice Smythe's request and the commissioners' letter to Lord Dartmouth
- **Bates (1918–19)** — the most authoritative secondary source on John Greene of Quidnessett — does not mention a Pawtuxet deed at all

The citation is definitively dead. It points to the wrong century.

### What changed

**Files corrected (13+):**
- `index.html` (live site) — 20 patches: all "two appearances" → "one verified appearance"; Pawtuxet entries marked SUSPENDED; Documents table badge changed
- `README.md` — complete rewrite: "appears twice" → "appears once"
- `theory/source_spine.md` — Pawtuxet entry downgraded from 🟢 to ⚠️ SUSPENDED; new status tag added
- `theory/1682_deed_lifecycle.md` — Node 3 (Pawtuxet) suspended throughout
- `theory/proof_pieces/09_pawtuxet_problem.md` — created (full search documentation)
- `theory/proof_pieces/10_independent_john.md` + addendum — single-appearance analysis
- `primary_sources/index.md` — Pawtuxet entry downgraded
- `primary_sources/source_intake_queue.md` — hero priority flipped to home-place deed
- `research/pawtuxet_deed_investigation.md` — Vol. VII kill documented with page contents
- `research/open_leads.md` — citation killed, status updated
- `contamination/vol_vii_citation_kill.md` — created (full contamination trace)
- `notes/` files — suspension notices added to dated research notes
- `contradictions/warwick-pawtuxet-overlap.md` — C1 suspension notice added
- `primary_sources/greene-certificate-1679.md` — Pawtuxet reference flagged

**What we did NOT change:** Dated agent cycle outputs (`agents/` folder) are preserved as-is. They represent what we believed on that date. Editing them retroactively would be narrative smoothing — a Law 1 violation. The git history shows when the error was introduced and when it was caught.

### What's still open

The Pawtuxet deed is **SUSPENDED, not deleted.** It may still exist in:
1. RI Land Evidences Vol. I original manuscript (FamilySearch Film 564389)
2. A Providence town-level deed book (Pawtuxet was under Providence jurisdiction)
3. Peirce Manuscripts (FamilySearch films 22291–22292)
4. North Kingstown town records (if they survived the fire)

A direct query to RI State Archives would resolve this definitively.

### The impact on Joan

If the Pawtuxet deed doesn't exist, Joan has **ONE verified legal appearance** — the March 24, 1682 home-place deed. This makes her documentary footprint uniquely thin among comparable Quidnessett wives and strengthens Model A (Indigenous woman who entered the English record system through marriage). See `theory/proof_pieces/10_independent_john_addendum_single_appearance.md`.

---

*This log is maintained under the 5 Laws of the Joan Archive.*  
*If you find an error in this archive, please report it via [GitHub Issues](https://github.com/lemuwah/joan-archive/issues).*
