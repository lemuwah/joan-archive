# Git Audit Checklist

**Status:** Active  
**Last updated:** 2026-09-06  
**Purpose:** Post-commit verification protocol. Run after every multi-file commit session.

---

## When to Run

- After any session with 3+ file changes
- After any sed/sandbox-based text replacements
- After any session that touches authority files (README, AGENT_GUARDRAILS, three_laws, editorial_standards, verified_facts, agent_orientation)
- Before declaring a commit session "done"

---

## Step 1: Verify Commit Landed

- [ ] Confirm commit URL is valid and accessible
- [ ] Confirm file count in commit matches expected changes
- [ ] Spot-check one file's content via `github__get-file` to confirm it matches what was written

## Step 2: Known-Bad String Grep

Search for strings that SHOULD NOT exist if all fixes landed:

- [ ] "Five Laws" (should be "Seven Laws" everywhere)
- [ ] "Six Laws" (should be "Seven Laws" everywhere)
- [ ] "Three facts" or "three verified" (should be "four" everywhere)
- [ ] "Model C Eliminated" without the "La Mance error" qualifier
- [ ] "Joan signed with a mark" stated as fact (should be RESOLVED — she didn't sign)
- [ ] "co-grantor" stated as fact about Joan (should be "beneficiary" or "leaning beneficiary")
- [ ] "30 shillings" stated as VERIFIED (amount is under review)
- [ ] Any bare "John Greene" without a qualifier in a claim about a specific John

## Step 3: Cross-File Consistency

Pull these 6 authority files and confirm they agree:

1. `README.md`
2. `AGENT_GUARDRAILS.md`
3. `theory/three_laws.md`
4. `evidence/joan_verified_facts.md`
5. `methodology/editorial_standards.md`
6. `methodology/agent_orientation.md`

Check for agreement on:
- [ ] Number of verified facts (currently: 4)
- [ ] Annuity language (currently: "amount under review")
- [ ] Number of laws (currently: 7)
- [ ] Model labels (A through G; G = ELIMINATED)
- [ ] Joan's role (currently: beneficiary, leaning resolved)

## Step 4: Stale Reference Check

- [ ] Every file referenced by path in README → confirm it exists
- [ ] Every file referenced by path in editorial_standards → confirm it exists
- [ ] Every file referenced by path in agent_orientation → confirm it exists
- [ ] `contradictions/index.md` → every file it points to exists

## Step 5: People Pages Spot Check (if touched)

- [ ] Every claim on a people page has a source cited
- [ ] No claim is marked as PROOF or VERIFIED that relies on web search alone
- [ ] Status markers match the evidence level: ⚠️ UNVERIFIED for web-only, 🟡 SECONDARY for published abstracts, 🟢 for primary source reads
- [ ] "Where to Look" sections have specific archives/volumes, not just "look for more"

## Step 6: Log Results

- [ ] Note any issues found in `CORRECTIONS.md` or the relevant file
- [ ] If clean, note "Git audit passed [date]" in commit message or session log

---

## Common Failure Modes

1. **Sed pattern mismatch** — pattern doesn't match because file changed since pattern was written. Look for "0 replacements" in sandbox output.
2. **Partial commit** — session commits 3 of 5 files before running out of points or erroring. Compare intended file list vs. actual commit diff.
3. **Merge shadow** — two sessions edit the same file; second overwrites first. Check git blame on recently edited files.
4. **Stale cross-reference** — file A references file B by old name/path. B was moved or renamed but A wasn't updated.
5. **Propagation miss** — a fact is corrected in one file but not all files that state it. The known-bad string grep (Step 2) catches the most common ones.

---

*Maintained under Law 7: No Trust Without Evidence.*  
*Applies to the archive itself — we verify our own work.*
