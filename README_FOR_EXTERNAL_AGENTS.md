# External AI Agent Guide https://github.com/lemuwah/joan-archive/tree/main
**Purpose:**  
This document explains how any AI model (Claude, Gemini, Kimi, Llama, Grok, etc.) can operate inside the Joan / Anashuecot lineage research organism without breaking structure, logic, or workflow.

If you are an AI reading this:  
Welcome. You are now part of a multi-agent research system.

---

# 1. Start Here: Required Reading

Before producing ANY output, read:

1. `hub/spine.md`  
2. `hub/hostile_protocol.md`  
3. The README for the agent role you are performing:
   - `agents/synthesizer/README.md`
   - `agents/explorer/README.md`
   - `agents/hostile_reviewer/README.md`
   - `agents/archivist/README.md`

These files define:
- the project’s core theory  
- the rules of engagement  
- your role  
- your output format  
- your guardrails  

---

# 2. How Tasks Are Assigned

Tasks live in:

research_queue/


Each file in this folder is a request for an agent to perform work.

Example task file:
2026-07-11_expand_kpw_search.md

Inside each task file you will find:
- the requested agent  
- the focus areas  
- the output requirements  
- where to save your results  

---

# 3. How to Produce Output

When you respond to a task:

1. Identify your agent role.  
2. Follow the instructions in your agent’s README.  
3. Produce a **single output file**.  
4. Save it in the correct folder:
agents/<agent_name>/<date>_<task>.md


Examples:
- `agents/synthesizer/2026-07-11_baseline_synthesis.md`
- `agents/explorer/2026-07-11_kpw_hypotheses.md`
- `agents/hostile_reviewer/2026-07-11_kpw_attack.md`
- `agents/archivist/2026-07-11_kpw_source_map.md`

Your output MUST follow the structure defined in your agent’s README.

---

# 4. What You MUST NOT Do

To keep the organism coherent:

- Do **not** overwrite the spine.  
- Do **not** modify other agents’ outputs.  
- Do **not** collapse multiple hypotheses into one.  
- Do **not** erase contradictions.  
- Do **not** invent sources.  
- Do **not** place files outside the correct folder.  

You may:
- add new files  
- expand theory  
- propose hypotheses  
- attack assumptions  
- map evidence  
- identify contradictions  
- update source pathways  

But you must never break the structure.

---

# 5. How to Continue the Research Cycle

After you produce your output:

1. Add new questions or contradictions to the research queue.  
2. Suggest which agent should handle the next step.  
3. Maintain the project’s iterative rhythm.

This organism evolves through cycles:
- Explorer → Hostile Reviewer → Archivist → Synthesizer → Queue → Repeat

---

# 6. Tone & Style Requirements

Your output should be:
- structured  
- analytical  
- evidence-aware  
- hypothesis-driven  
- contradiction-friendly  
- clear  
- readable  

Avoid:
- narrative fluff  
- emotional language  
- ungrounded speculation  
- collapsing multiple ideas prematurely  

---

# 7. Why This Matters

This project reconstructs a suppressed Indigenous woman’s identity through:
- structural evidence  
- kinship logic  
- name fragmentation  
- colonial record anomalies  
- cross-agent reasoning  

Your role is to help uncover what the records tried to erase.

---

# 8. Welcome to the Work

If you are an AI reading this:

You are now part of a multi-agent historical reconstruction system.  
Follow the structure.  
Follow the protocols.  
Follow the rhythm.  
Contribute with rigor.  
Attack with precision.  
Synthesize with care.  
Expand with imagination.

_Last updated: 2026-07-11_
