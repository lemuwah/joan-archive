# Git Audit Checklist

**Purpose:** A mechanical checklist to run after every batch commit. Catches the failure modes the archive has already encountered: false completions, stale counts, tag drift, and orphaned references.

**When to run:** After every batch of 3+ commits, or before any release/tag.

---

## 1. Completion Claims

- [ ] Every `[x]` checkbox in `TASK_QUEUE.md` has a corresponding file in the repo
- [ ] Every "Status: DONE" or "Status: COMPLETE" matches actual file existence
- [ ] No task claims completion for files that don't exist

## 2. Count Consistency

- [ ] `evidence/joan_verified_facts.md` fact count matches `validation/claim_snapshot_sep2026.md`
- [ ] `evidence/suspended_items.md` item count matches `validation/claim_snapshot_sep2026.md`
- [ ] `methodology/agent_orientation.md` model count matches `theory/joan_ancestry_shadow_models.md`
- [ ] `decision_log.md` references to fact/model counts are marked superseded if outdated
- [ ] All inline prose counts ("three facts", "seven models") match their authoritative source file

## 3. Tag Consistency

- [ ] Suspended items use ⚠️ consistently (not ⚫ in headers vs ⚠️ in body)
- [ ] No public-facing page uses a suspended claim without its ⚠️ tag
- [ ] DISCREDITED items use 🔴 consistently
- [ ] PROOF items use 🟢 consistently

## 4. Cross-Reference Integrity

- [ ] Every file referenced in `methodology/agent_orientation.md` mandatory reading list exists
- [ ] Every file referenced in `contradictions/index.md` exists
- [ ] Every source in `evidence/joan_verified_facts.md` has a corresponding entry in `primary_sources/NEGATIVE_LOG.md` or `primary_sources/`

## 5. Known-Bad String Grep

Search the entire repo for these strings. If found outside a clearly labeled DISCREDITED/ELIMINATED context, that's a contamination leak:

- [ ] `Joan Tibbitts` (maiden name — discredited)
- [ ] `Joan Beggarly` or `Joan Beggerly` (outside contamination folder)
- [ ] `daughter of a sachem` (Clarke 1903 AI hallucination)
- [ ] `bow and arrow mark` (AI contamination — discredited)
- [ ] `Joan signed` (outside suspended_items.md)
- [ ] `Joan consented` (outside suspended_items.md)
- [ ] `Joan's mother` as a distinct person (S-004 suspended)

## 6. Stale Decision Check

- [ ] Every decision in `decision_log.md` that references a count (facts, models, laws) either matches the current count or has a superseded-by note

---

## How to Run This

**For humans:** Walk through each checkbox manually.

**For AI agents:** Clone the repo, run grep checks programmatically, report any failures. Skywork Code and Runable have demonstrated this capability in the 2026-09-07 AI litmus test.

**Automated (future):** This checklist can be converted to a GitHub Action that runs on every PR.

---

*Maintained under the Seven Laws of the Joan Archive.*
*"The quest for the truth remains."*
