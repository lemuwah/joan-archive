# Kimi Hostile Audit — September 6, 2026

**Source:** Kimi AI hostile review of the Joan Archive framework
**Date received:** 2026-09-06
**Purpose:** Transparency. Document every finding. Track fixes.

---

## Summary

17 issues found. 4 critical, 5 high, 6 medium, 2 low.

The core problem: **framework files proliferated faster than they were harmonized.** Multiple files disagree on law count, tag vocabulary, and fact count. The live site is in many ways more honest than the framework files beneath it.

---

## Fix Tracker

| # | Issue | Severity | Status |
|---|---|---|---|
| 1 | Law count broken across files | CRITICAL | ✅ FIXED — all files updated to Seven Laws |
| 2 | Five incompatible tag systems | CRITICAL | 🟡 PARTIAL — canonical system defined in integrity_framework.md, legacy files noted |
| 3 | Verified facts count unstable (3 vs 4) | CRITICAL | ✅ FIXED — editorial_standards.md updated to 4 facts |
| 4 | 30 shillings still listed as verified | CRITICAL | ✅ FIXED — changed to 'amount unverified' |
| 5 | Model B mislabeled as Indigenous in contradictions file | HIGH | ✅ FIXED — changed to Model A |
| 6 | Model G links to wrong correction | HIGH | ⚬ PENDING — requires HTML edit (workflow) |
| 7 | Content note placement error | HIGH | ⚬ PENDING — requires HTML edit (workflow) |
| 8 | Bow-and-arrow mark cross-contamination risk | HIGH | 🟡 NOTED — rename needed in future pass |
| 9 | Live site claims not in framework files | HIGH | 🟡 NOTED — H. Tibbits needs evidence file entry |
| 10 | Inference audit tracker dead | MEDIUM | ⚬ PENDING — update or remove |
| 11 | Negative log incomplete | MEDIUM | ⚬ PENDING — sync with verified facts |
| 12 | Agent guide says 'Seven Laws' | MEDIUM | ✅ FIXED |
| 13 | Y-DNA inconsistency buried | MEDIUM | ⚬ PENDING — surface on analysis.html |
| 14 | 1695/96 deed has no GAP entry | MEDIUM | ⚬ PENDING — add to source_intake_queue |
| 15 | Email obfuscation is theater | MEDIUM | 🟡 NOTED — accept risk for now |
| 16 | Stale file names | LOW | 🟡 NOTED — three_laws.md stays for link stability |
| 17 | Script targets nonexistent elements | LOW | 🟡 NOTED |

---

## Canonical Tag System (per Law 7 / integrity_framework.md)

**The authoritative tag definitions are in `methodology/integrity_framework.md`.** All other files should reference that file. Legacy tag vocabularies (VERIFIED/PROBABLE/SUSPENDED/etc.) in older files are acknowledged but the canonical system is:

- 🟢 **PROOF** — primary source seen, page cited
- 🟢 **PROOF — AI TRANSCRIPTION** — original image read by AI, disclaimer attached
- 🟡 **PLAUSIBLE** — scholar cites it or logic holds, not personally verified
- 🔴 **DISCREDITED** — tested and failed

Legacy tags in source_spine.md (🟢 PROVEN / 🟡 PROBABLE / ⚪ UNVERIFIED / ⚫ NULL / ⚠️ SUSPENDED) are recognized as equivalent but should be migrated during the next full spine rewrite.

---

*This audit is committed for transparency per Law 4. Kimi's findings are treated as external hostile review with the same weight as internal hostile review.*
