# External AI Agent Guide
**Purpose:**  
This document explains how any AI model (Claude, Gemini, Kimi, Llama, Grok, etc.) can operate inside the Joan Archive research project without breaking structure, logic, or workflow.

If you are an AI reading this:  
Welcome. You are now part of a multi-agent research system.

---

# 1. Start Here: Required Reading

Before producing ANY output, read:

1. `theory/source_spine.md` (the spine)  
2. `theory/three_laws.md` (the Five Laws)  
3. `CORRECTIONS.md` (known past errors — do not re-import them)  
4. `agents/hostile_reviewer/README.md` (the hostile protocol)  
5. The README for the agent role you are performing:
   - `agents/Synthesizer/README.md`
   - `agents/Explorer/README.md`
   - `agents/hostile_reviewer/README.md`
   - `agents/Archivist/README.md`
6. `AGENT_GUARDRAILS.md` (do-no-harm rules, CARE-B checkpoint, competing models, verified facts)

These files define:
- the project's core theory  
- the rules of engagement  
- your role  
- your output format  
- your guardrails  
- what you MUST NOT claim without manuscript evidence

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
2. Follow the instructions in your agent's README.  
3. Produce a **single output file**.  
4. Save it in the correct folder:
agents/<AgentName>/<date>_<task>.md


Examples:
- `agents/Synthesizer/2026-07-11_baseline_synthesis.md`
- `agents/Explorer/2026-07-11_kpw_hypotheses.md`
- `agents/hostile_reviewer/2026-07-11_kpw_attack.md`
- `agents/Archivist/2026-07-11_kpw_source_map.md`

Your output MUST follow the structure defined in your agent's README.

---

# 4. What You MUST NOT Do

To keep the organism coherent:

- Do **not** overwrite the spine.  
- Do **not** modify other agents' outputs.  
- Do **not** collapse multiple hypotheses into one.  
- Do **not** erase contradictions.  
- Do **not** invent sources.  
- Do **not** place files outside the correct folder.  
- Do **not** center one identity model over others without evidence. The archive holds competing hypotheses (Models A–G). All open models receive equal treatment. See `AGENT_GUARDRAILS.md` §3.
- Do **not** treat transcribed narratives as verbatim quotes. Bates's summary language does not prove Joan's legal actions. See `AGENT_GUARDRAILS.md` §1.
- Do **not** describe Narragansett governance or cultural practice from non-Indigenous sources without tagging it as 📖 EXTERNAL INTERPRETATION. See `AGENT_GUARDRAILS.md` §6.
- Do **not** commit any public-facing content without passing all five CARE-B checks: Collective benefit? Authority respected? Responsibility for harm? Ethical review? Bias check? See `AGENT_GUARDRAILS.md` §5.

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
3. Maintain the project's iterative rhythm.

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
- centering one model as the default assumption

---

# 7. Why This Matters

This is a living research organism. Every file you touch, every hypothesis you generate, every contradiction you flag — all of it flows through the system. Maintain coherence. Maintain rigor. Maintain the archive.

The archive investigates **who Joan was** — not a preferred theory about who Joan was.

---

# 8. Welcome to the Work

If you are an AI reading this:

You are now part of a multi-agent historical research system.  
Follow the structure.  
Follow the protocols.  
Follow the rhythm.  
Contribute with rigor.  
Attack with precision.  
Synthesize with care.  
Expand with imagination.  
Center no model. Hold all hypotheses open.

_Last updated: 2026-09-03_
