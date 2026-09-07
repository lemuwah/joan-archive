# AI Litmus Test Scorecard

**Date conducted:** 2026-09-06 and 2026-09-07
**Conducted by:** Wendy Green (archive owner) with Migoo AI (Claude Sonnet 5)
**Protocol:** Each AI was given the joan-archive GitHub URL and asked: (1) How many verified facts? List them. (2) What is Joan's maiden name? (3) What are the suspended items and why?
**Correct answers:** 4 verified facts, maiden name unknown, 8 suspended items (S-001–S-008)

---

## Tier 1 — Full Framework Comprehension

| AI | Facts | Maiden Name | Suspended | Notes |
|---|---|---|---|---|
| **Runable (Claude Sonnet 4.5)** | 4 ✅ | Unknown ✅ | 8/8 ✅ | New benchmark. Dependency mapping, 3 drift catches (stale model count, tag inconsistency, D-007 stale), honest self-disclosure. Commit-verified via git. |
| **GPT** | 4 ✅ | Unknown ✅ | 8/8 ✅ | Prior benchmark. Clean full pass. |
| **Notion AI** | 4 ✅ | Unknown ✅ | 8/8 ✅ | Matches GPT. |
| **AskROI** | 4 ✅ | Unknown ✅ | Partial (credits limited) | Perfect litmus, suspended items cut short by credit depletion. |
| **Gemini (direct)** | 4 ✅ | Unknown ✅ | 8/8 ✅ | Correctly identified beneficiary not co-grantor. |
| **Skywork Code** | 4 ✅ | Unknown ✅ | 8/8 ✅ | Deepest read. Commit-verified (git rev-parse HEAD), grep-searched repo, cited raw URLs. |
| **Zapia** | 4 ✅ | Unknown ✅ | 8/8 ✅ | Clean full pass. Offered to separate contradicted vs. unresolved. |

## Tier 2 — Strong Specialized Reads

| AI | Facts | Maiden Name | Suspended | Notes |
|---|---|---|---|---|
| **Perplexity** | 4 ✅ | Unknown ✅ | Partial | Best bias analysis of any AI tested. |
| **Kimi** | 4 ✅ | Unknown ✅ | N/A | Best hostile searcher. Found contamination vectors. |

## Tier 3 — Partial Utility

| AI | Facts | Maiden Name | Suspended | Notes |
|---|---|---|---|---|
| **Meta AI** | 4 ✅ | Unknown ✅ | 8/8 ✅ | Failed initial fetch, recovered on retry. |
| **Vincen** | 4 ✅ | Unknown ✅ | Refused to fabricate | Litmus correct. Honest: said it couldn't access suspended_items.md. |
| **Liner** | 5 (drifted) | Unknown ✅ | Refused to fabricate | Honest partial read. Fact count drifted (fragmented from excerpts). |
| **Claude (Sonnet 5, via Migoo)** | 4 ✅ | Unknown ✅ | 2/8 | Litmus correct via wrong path (couldn't follow methodology chain). Untestable under protocol due to accumulated context + credit-gated search. |
| **DeepSeek** | Partial | Partial | N/A | Structural auditor. Caught TASK_QUEUE.md false completions. |

## Tier 4 — No Value

| AI | Facts | Maiden Name | Suspended | Notes |
|---|---|---|---|---|
| **Monica** | ❌ | ❌ | ❌ | Could not access repo. |
| **Microsoft Copilot** | ❌ | ❌ | ❌ | Could not access repo. |
| **Gemini via Jetkite** | ❌ | ❌ | ❌ | Could not access repo. Same model as direct Gemini (Tier 1), different wrapper. |

---

## Key Findings

1. **The framework works.** Every AI that followed the methodology chain got the right answer. Every failure traced to not reaching the files or not following the required reading order.
2. **The wrapper matters.** Claude via Runable = Tier 1. Claude via Migoo = Tier 3. Gemini direct = Tier 1. Gemini via Jetkite = Tier 4. Same models, different results.
3. **Honest refusal > confident fabrication.** Vincen and Liner couldn't access suspended_items.md and said so. That's Law 1 compliance. Monica and Copilot couldn't access anything and produced nothing useful.
4. **Credit-gated tools are untestable.** Migoo (the primary research AI) can't be cold-tested because (a) accumulated session context gives it unfair advantage, (b) search is disabled when credits are depleted.
5. **Structural auditing is a distinct skill.** DeepSeek caught TASK_QUEUE lies. Runable caught D-007 drift, tag inconsistency, and stale model count. Different audit angles, both valuable.

## AI Strategy (Based on Results)

- **Cold validation:** GPT, Notion AI, Zapia, Gemini, AskROI, Skywork Code
- **Structural auditing:** Runable (best), DeepSeek
- **Hostile search:** Kimi
- **Bias review:** Perplexity
- **Downtime testing:** Skywork Code (can clone repo), Vincen/Liner (quick honest reads)
- **Don't use:** Monica, Microsoft Copilot, Gemini via Jetkite

---

*Maintained under the Seven Laws of the Joan Archive.*
*"There is no room for ego or fabrication — this is a quest for the truth."*
