# The Six Laws of the Joan Archive

**Status:** Active — supreme authority over all agent and human output.  
**Last updated:** 2026-09-03  
**Companion files:** `AGENT_GUARDRAILS.md`, `methodology/editorial_standards.md`

---

## Law 1 — No Narrative Smoothing

**Lens anchor:** All lenses. This is the master law.

All contradictions logged and held open with status tags until 100% proven. Do not invent narratives.

**Expanded (Sep 3, 2026):**
- A transcribed narrative is not a verbatim quote. Worth's abstract describes the deed. Bates's summary describes the deed. Neither IS the deed. Only the manuscript is the deed. (See `AGENT_GUARDRAILS.md` §1.)
- Two facts that sit near each other do not become one inference. Present them separately. Let the reader draw the line or not.
- Inference is not fact. When a connection between documented facts requires a logical step, that step must be labeled as inference and placed on `analysis.html`, not `index.html`.

---

## Law 2 — La Mance Law

**Lens anchor:** Lens 2 (Secondary Literature)

No claim traceable to La Mance (1904) accepted without independent primary corroboration.

**Scope:** Extends to any secondary compilation that cites La Mance, directly or through intermediaries. Circular citation chains must be traced to their origin and evaluated there.

---

## Law 3 — No Premature Disqualification

**Lens anchor:** All lenses, especially Lens 6 (Negative Space)

No hypothesis eliminated until thoroughly tested against primary sources. Even outlandish and wild ideas need thorough proof of nonexistence before eliminating as an option.

**Expanded (Sep 3, 2026):**
- This applies to ALL competing models about Joan's identity (A–G), not just the ones we find compelling. Model B (English woman) requires the same exhaustive search before elimination as Model A (Narragansett). Model D (indentured servant) and Model E (enslaved person) require the same as Model C (Irish origin).
- A model is not eliminated by the strength of another model. It is eliminated by its own evidence failing.
- See `AGENT_GUARDRAILS.md` §3 for the full model list.

---

## Law 4 — No Algorithmic Contamination

**Lens anchor:** All lenses. Enforcement layer.

Every identified contamination — AI hallucination, fabricated source, algorithmic auto-fill guess, or uncorroborated secondary/circular compilation — must be logged in the AI Contamination Log (`theory/source_spine.md` §6) and/or `contamination_index.md` with its specific vector and the reasoning for its rejection.

Contamination is never silently deleted or quietly corrected in place — it is held on record with the same rigor as proven evidence, so any agent or reader can see not just what is true, but what was tested, where it came from, and why it failed.

Holding contradictions (Law 1) and following the evidence (Law 3) are not enough on their own — the record of what was *rejected* is itself part of the project's evidentiary discipline.

---

## Law 5 — No Jurisdictional Assumption

**Lens anchor:** Lens 1 (Colonial Legal Record), Lens 4 (Material Record), Lens 6 (Negative Space)  
*(Equal priority with Law 2 — added 2026-08-27)*

The Quidnessett/Narragansett region was contested territory documented by Rhode Island, Massachusetts Bay, Plymouth Colony, Connecticut, the Crown (Colonial Office), New York, and Native landholders — each with overlapping and conflicting jurisdictional claims, each generating records, often catalogued in unexpected locations.

No colony, authority, or record repository may be dismissed as "unlikely" to hold evidence of Joan without being checked. Dismissing a repository without checking it is a violation of this law.

**Expanded (Sep 3, 2026):**
- This extends to identity models. No origin hypothesis (English, Irish, Narragansett, indentured, enslaved, widowed) may be dismissed as "unlikely" without the corresponding record types being searched. If you haven't searched Irish parish records, you can't eliminate Model C. If you haven't searched indenture records, you can't eliminate Model D.

---

## Law 6 — No Centering

**Lens anchor:** All lenses. Equal priority with Law 1.  
*(Added 2026-09-03)*

The archive investigates **who Joan was** — not a preferred theory about who Joan was.

No identity model receives more visual space, more confident language, or more prominent placement than its evidence warrants. The absence of English records is not evidence for Narragansett identity — it is evidence of absence from English records, consistent with multiple models.

Every open model starts from the same three verified facts:
1. Joan is named as wife of John Greene in a March 1682 land deed (Worth abstract)
2. A life annuity of 30 shillings per year is reserved to her (Worth abstract)
3. No other record of Joan has been located

See `AGENT_GUARDRAILS.md` §2–3 for implementation rules.

---

## Enforcement: CARE-B Checkpoint

Before any commit that touches public-facing content or analysis, all five checks must pass:

- **C** — Collective benefit?
- **A** — Authority to control respected?
- **R** — Responsibility for harm?
- **E** — Survives ethical review?
- **B** — Bias check: does this output privilege one model over others without evidence?

If any check fails, revise before committing. See `AGENT_GUARDRAILS.md` §5.

---

*These Laws govern all output — human and AI — in the Joan Archive.  
Violation of any Law is treated with the same severity regardless of which Law is broken.*
