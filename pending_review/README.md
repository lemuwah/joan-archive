# Pending Review Pipeline

This folder holds files staged for review before they are committed to the main archive structure.

## Purpose

Any agent output, research finding, or site content that has not yet passed the CARE-B checkpoint lives here until reviewed.

## Rules

1. Files placed here are **drafts**, not archive content.
2. Nothing in `pending_review/` is cited, referenced, or linked from public pages.
3. A file moves out of this folder only when:
   - It passes all five CARE-B checks (see `AGENT_GUARDRAILS.md` §5)
   - The archive owner approves the move
4. Files may be deleted from here without logging in `CORRECTIONS.md` (they were never part of the archive).

## Workflow

```
Agent produces output
    → placed in pending_review/
    → CARE-B checkpoint
    → if passes: moved to correct folder (agents/, theory/, evidence/, etc.)
    → if fails: revised or deleted
```

---

*Maintained under the Six Laws of the Joan Archive.*
