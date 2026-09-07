# AI Provenance Log

**Purpose:** Document every AI tool that has contributed to this archive, what it did, and how reliable it proved. Required by Law 7 (No Trust Without Evidence) — if an AI produced content that entered the archive, that AI's identity and limitations are part of the provenance chain.

**Last updated:** 2026-09-07

---

## Primary Research AI

| AI | Platform | Role | Sessions | Reliability | Notes |
|---|---|---|---|---|---|
| Claude Sonnet 5 | Migoo | Primary research, commits, analysis | Ongoing since Aug 2026 | Tier 3 on cold litmus test (accumulated context advantage, credit-gated) | Cannot be independently cold-tested. All commits attributed to this AI. |

## Validation AIs (Litmus Test 2026-09-06/07)

| AI | Platform | Role | Tier | Key Strength |
|---|---|---|---|---|
| Runable (Claude Sonnet 4.5) | Runable | Structural audit | Tier 1 | Deepest read. Commit-verified, 3 drift catches, dependency mapping. New benchmark. |
| GPT | OpenAI | Cold validation | Tier 1 | Prior benchmark. Clean full pass on all test questions. |
| Notion AI | Notion | Cold validation | Tier 1 | Full pass, matches GPT. |
| AskROI | AskROI | Cold validation | Tier 1 | Perfect litmus, credits limited suspended items. |
| Gemini | Google (direct) | Cold validation | Tier 1 | Correctly identified beneficiary not co-grantor. |
| Skywork Code | Liner (Skywork) | Structural audit | Tier 1 | Commit-verified via git, grep-searched repo. |
| Zapia | Zapia.com | Cold validation | Tier 1 | Clean full pass, all 8 suspended items. |
| Perplexity | Perplexity.ai | Bias analysis | Tier 2 | Best bias analysis of any AI tested. |
| Kimi | Moonshot AI | Hostile search | Tier 2 | Best hostile searcher. Found contamination vectors. |
| Meta AI | Meta | Recovery reader | Tier 3 | Failed initial fetch, recovered, all 8 suspended. |
| Vincen | Liner (Vincen) | Honest partial | Tier 3 | Litmus correct, refused to fabricate suspended items. |
| Liner | Liner | Honest partial | Tier 3 | Fact count drifted (5 vs 4), refused to fabricate. |
| DeepSeek | DeepSeek | Structural audit | Tier 3 | Caught TASK_QUEUE false completions. |
| Monica | Monica | N/A | Tier 4 | Could not access repo. |
| Microsoft Copilot | Microsoft | N/A | Tier 4 | Could not access repo. |
| Gemini via Jetkite | Jetkite | N/A | Tier 4 | Same model as direct Gemini but different wrapper — could not access repo. |

## AI Transcription

| AI | What It Read | Status | Notes |
|---|---|---|---|
| Claude (via Migoo) | FamilySearch DGS 008204949, Image 10 | PROOF — AI TRANSCRIPTION | Working research read. NOT paleographic verification. All claims from this read carry the AI TRANSCRIPTION tag. |
| Kimi | FamilySearch DGS 008204949, Image 10 | Cross-check | Independent read attempted, access restricted. |

## Other AI Tools Used

| AI | What For | Date | Notes |
|---|---|---|---|
| DeepExa | Autonomous research investigations | Aug 2026 | Free credits depleted. Not re-engaged. |
| Suno AI | Music generation ("Keep Swimming") | Jun 2026 | Creative output, not research. |

---

## Failed AI Claims Log

| Date | AI / Tool | Claim | Reality | Likely mechanism |
|---|---|---|---|---|
| 2026-09-06 | DeepSeek (repo audit) | "5 John separation files do not exist in the repo" | 4 of 5 already exist (john_greene_warwick.md, john_greene_quidnessett.md, john_greene_potowomut.md, john_greene_son_of_john.md all present; only the exact filename `john_greene_warwick_surgeon.md` was missing) | Searched for one literal filename, got a miss, generalized the miss across the whole list. Classic false-negative from a filename mismatch — see `contamination/false_negative_suppression.md`. |
| 2026-09-07 (recorded 2026-09-07, unknown origin session) | Unattributed | TASK_QUEUE.md Task 3 marked index.html and about.html as done: "model count + Model H + Law 7," "Law 7 added" | Neither Model H nor Law 7 was present in either file as of 2026-09-07 audit | Status recorded from intent (what was meant to be done) rather than from re-reading the file after editing. Fixed same day — see Task 3 in TASK_QUEUE.md. |

## Key Finding from AI Provenance

**The wrapper matters more than the model.** Claude via Runable = Tier 1. Claude via Migoo = Tier 3. Gemini direct = Tier 1. Gemini via Jetkite = Tier 4. Same underlying models, different tool access and methodology chains, completely different results. This is documented in `agents/Archivist/ai_litmus_scorecard.md`.

---

*Maintained under the Seven Laws of the Joan Archive.*
*Law 7: No Trust Without Evidence — including AI evidence.*
