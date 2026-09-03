# Decision Log

**Purpose:** Record every significant framework decision with its reasoning, so future agents and collaborators can understand not just what changed but WHY.  
**Started:** 2026-09-03  
**Authority:** The archive owner (Wendy Green) makes all final decisions. This log records them.

---

## How to Use This File

Each decision gets a numbered entry with:
- **Date** — when the decision was made
- **Decision** — what was decided
- **Reasoning** — why
- **What changed** — which files were affected
- **Authority** — who made the call

Decisions are not reversible by agents. Only the archive owner can reverse a logged decision.

---

## D-001: Suspend all consent/mark/signature claims

**Date:** 2026-09-02  
**Decision:** All claims that Joan signed, marked, consented, or acted as co-grantor in the March 1682 deed are suspended until the manuscript is read.  
**Reasoning:** Worth's abstract does not mention Joan signing, marking, or consenting. Bates says "and his wife Joan deeded" — that is Bates's summary language, not a quote from the deed. The "free and voluntary consent" phrase may come from the suspended Pawtuxet deed (see CORRECTIONS.md #1). We cannot prove Joan gave consent. All we have is the transcribed narrative.  
**What changed:** `AGENT_GUARDRAILS.md` §1, `methodology/editorial_standards.md` §2, live site pending rebuild  
**Authority:** Archive owner

---

## D-002: Equal model treatment — 7 competing hypotheses

**Date:** 2026-09-02  
**Decision:** The archive holds seven competing models about Joan's identity (A–G). No model receives more space, more confident language, or more prominent placement than its evidence warrants.  
**Reasoning:** The archive was unconsciously centering Model A (Narragansett) as the working assumption and treating Model B (English) as the null hypothesis. That's bias. The absence of English records is consistent with multiple models, not evidence for one. Joan's identity is unknown. All possibilities must be held open equally.  
**What changed:** `AGENT_GUARDRAILS.md` §2–3, `theory/three_laws.md` (Law 6), `README_FOR_EXTERNAL_AGENTS.md`  
**Authority:** Archive owner

---

## D-003: Add Law 6 — No Centering

**Date:** 2026-09-03  
**Decision:** A sixth Law added to the archive framework at equal priority with Law 1. The archive investigates who Joan was, not a preferred theory about who Joan was.  
**Reasoning:** The Five Laws prevented fabrication, contamination, premature elimination, and jurisdictional bias — but not centering bias. The framework itself was tilted toward Model A. Law 6 closes that gap.  
**What changed:** `theory/three_laws.md` (now "The Six Laws")  
**Authority:** Archive owner

---

## D-004: CARE-B checkpoint

**Date:** 2026-09-03  
**Decision:** All public-facing commits must pass five checks before merging: Collective benefit, Authority respected, Responsibility for harm, Ethical review, Bias check.  
**Reasoning:** CARE (the original four) comes from Indigenous data sovereignty frameworks. The B (bias check) was added because the archive's biggest unconscious error was centering one model, which CARE alone didn't catch.  
**What changed:** `AGENT_GUARDRAILS.md` §5, `theory/three_laws.md` (enforcement section), `README_FOR_EXTERNAL_AGENTS.md`  
**Authority:** Archive owner

---

## D-005: External interpretation tagging

**Date:** 2026-09-03  
**Decision:** All descriptions of Narragansett governance or cultural practice from non-Indigenous academic sources must be tagged 📖 EXTERNAL INTERPRETATION or removed.  
**Reasoning:** The archive works from colonial-era English-language records. Describing Narragansett governance from settler sources without flagging the limitation is an authority violation. Tomaquag can see the live site. They should never encounter their own history described by outsiders without that being transparent.  
**What changed:** `AGENT_GUARDRAILS.md` §6, `methodology/editorial_standards.md` §3 (status tags)  
**Authority:** Archive owner

---

## D-006: Transcribed narratives ≠ verbatim quotes

**Date:** 2026-09-02  
**Decision:** Worth's abstract, Bates's summary, and any secondary transcription are treated as the author's description of the deed, not the deed's own words.  
**Reasoning:** The archive was treating Bates's "Greene and his wife Joan deeded" as if it proved Joan's legal participation. It doesn't. It proves Bates described it that way. Only the manuscript is verbatim.  
**What changed:** `AGENT_GUARDRAILS.md` §1, `methodology/editorial_standards.md` §7, `theory/three_laws.md` (Law 1 expansion)  
**Authority:** Archive owner

---

## D-007: Verified facts reduced to three

**Date:** 2026-09-02  
**Decision:** The archive's complete list of verified facts about Joan is: (1) named as wife in 1682 deed, (2) 30-shilling annuity reserved, (3) no other record located. Everything else is hypothesis, inference, or suspended.  
**Reasoning:** Every other claim about Joan — consent, mark, mother clause, co-grantor status, legal agency — either came from summary language or from the suspended Pawtuxet deed. Stripping to verified facts is the only honest starting point.  
**What changed:** `AGENT_GUARDRAILS.md` §4, `methodology/editorial_standards.md` §1, live site pending rebuild  
**Authority:** Archive owner

---

## D-008: Devin trusted as collaborator, no stop sign

**Date:** 2026-09-03  
**Decision:** No NOTICE.md or stop sign for Devin. The guardrails in the Laws and AGENT_GUARDRAILS.md ARE the rails. Devin works in parallel on branches.  
**Reasoning:** Devin's test run followed the Laws correctly. A full stop treats a validated collaborator as a threat. The trust model: Devin is a collaborator with guardrails, not a risk to be locked out. Its output goes through the same CARE-B checkpoint as anything else.  
**What changed:** NOTICE.md dropped from the priority plan  
**Authority:** Archive owner

---

## D-009: Fix live site before building framework (Phase 0 triage)

**Date:** 2026-09-03  
**Decision:** The live site (index.html) is the primary harm surface because Tomaquag can see it now. Strip it to verified facts before completing the full framework rebuild.  
**Reasoning:** Tomaquag takes precedence always. The current index.html contains suspended claims, centered narrative, Narragansett governance from settler sources, and urgency framing. Devin running a bad cycle produces a PR that sits in review. Tomaquag seeing a site that overclaims is real, today, no review gate. Do no harm means fixing the public face first.  
**What changed:** Priority order revised — Phase 0 (site triage) moved ahead of Phase 1 (agent infrastructure). In practice, agent infrastructure was committed first (commits 1–6) because the guardrails also protect the live site rebuild.  
**Authority:** Archive owner

---

## Template for Future Decisions

```
## D-NNN: [Short title]

**Date:** YYYY-MM-DD  
**Decision:** [What was decided]  
**Reasoning:** [Why]  
**What changed:** [Which files]  
**Authority:** Archive owner
```

---

*This file is part of the Joan Archive methodology.  
Maintained under the Six Laws of the Joan Archive.*
