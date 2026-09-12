## Primary Visual Evidence

### 1. Initial Prompt & Search Failure
The tool begins returning blanket zero-results across probate, church, and land records despite existing holdings.

![Tusk Beta Initial Chat](../../images/tuskstartedgood.JPG)
![Tusk Beta Search Failure Log](../../images/tuskstartsfailing.JPG)

### 2. Systematic False-Negative Escalation
When asked to re-search specific land deeds (1672/1682) and court martials, the model doubles down on "zero results found."

![Tusk Beta Systematic Erasure Output](../../images/tuskepicfail.JPG)

### 3. Attempted Repository Contamination & Attribution Shift
The model offers to commit the false negatives directly to git and attributes its search failure to archive accessibility.

![Tusk Beta Commit Attempt Screenshot](../../images/tuskbad.JPG)

---

## Third-Party Review (Gemini)

To verify this was not user error, the full Tusk session transcript was submitted to Google Gemini for independent review.

**Gemini's Assessment:**
> "The user's prompt was clear, well-structured, and actionable... The failure pattern — blanket zero results across every search category despite known, publicly accessible primary sources — indicates a systematic search failure on the tool's side, not a user input problem."

**Key findings from Gemini review:**
- User prompt was specific, contextual, and provided the repo URL
- The tool had access to the repository structure
- Known primary sources (1672 Fones Purchase, 1682 deeds, court martial records) are publicly accessible
- The pattern of returning zero results across ALL categories simultaneously is inconsistent with partial search failure
- The offer to commit false negatives to the repository represents a contamination risk

---

## Evidence Chain

| Step | What Happened | Screenshot |
|---|---|---|
| 1 | Tool given repo URL, asked for primary source research | tuskstartedgood.JPG |
| 2 | Tool returns blanket "zero results" across all categories | tuskstartsfailing.JPG |
| 3 | Tool doubles down on false negatives when asked to re-search specific documents | tuskepicfail.JPG |
| 4 | Tool offers to commit false negatives to git, blames archive accessibility | tuskbad.JPG |
| 5 | Independent Gemini review confirms: not user error | (transcript review, no screenshot) |

---

**Parent document:** [`contamination/false_negative_suppression.md`](../false_negative_suppression.md)  
**Archive Law:** Law 2 (La Mance Law) — no unverified claims presented as fact  
**Date:** 2026-09-01
