# Legacy Vocabulary Firewall Contract

**Status:** ACTIVE
**Created:** 2026-09-14
**Purpose:** Prevent historical research labels from silently becoming current truth.

---

## 1. Purpose

The Joan Archive contains older research systems that used labels such as:

- `PROOF`
- `PROOF — AI TRANSCRIPTION`
- `PROVEN`
- `PLAUSIBLE`
- `PROBABLE`
- `UNVERIFIED`
- `ELIMINATED`
- `KILLED`
- `SUSPENDED`
- `NULL`
- `SEARCHED`
- `NOT FOUND`
- `PRIMARY`
- `SECONDARY`
- `TERTIARY`

These labels are part of the archive's research history.

They are **not automatically authoritative for the zero-trust control plane**.

The control plane must preserve what earlier researchers concluded while independently testing whether those conclusions remain supportable.

---

## 2. Non-Destructive Migration

Migration must never:

- delete historical evidence;
- overwrite earlier reasoning;
- silently promote an old status;
- silently demote an old status;
- convert source classification into truth;
- convert absence into proof;
- collapse distinct meanings of `NULL`;
- infer an observation that was not actually recorded;
- treat agreement between AI systems as independent corroboration.

Historical material remains recoverable.

---

## 3. Legacy Status Firewall

The following mappings are historical only:

| Legacy label | Control-plane treatment |
|---|---|
| `PROOF` | Preserve as historical status; no automatic `VERIFIED` |
| `PROOF — AI TRANSCRIPTION` | Preserve as historical AI observation; no automatic `VERIFIED` |
| `PROVEN` | Preserve as historical status; no automatic `VERIFIED` |
| `PLAUSIBLE` | Preserve as historical status; no automatic `PROVISIONALLY_SUPPORTED` |
| `PROBABLE` | Preserve as historical status; no automatic `PROVISIONALLY_SUPPORTED` |
| `UNVERIFIED` | Preserve as historical status |
| `ELIMINATED` | Preserve as historical disposition; no automatic `REJECTED` |
| `KILLED` | Preserve as historical test disposition; no automatic `REJECTED` |
| `SUSPENDED` | Preserve as historical quarantine; no automatic verdict |
| `NULL` | Context-sensitive; never imported as a current conclusion |

A current status must be established through the control-plane evidence and review process.

---

## 4. Source Classification Firewall

Source classification is not claim truth.

Therefore:

- `PRIMARY` does not mean `VERIFIED`.
- `SECONDARY` does not mean `FALSE`.
- `TERTIARY` does not mean `USELESS`.

A primary source still requires a source-to-claim match.

A secondary source may provide a valid lead, context, or independently useful evidence.

A tertiary source may identify a search path.

---

## 5. Search Vocabulary Firewall

`SEARCHED` and `NOT FOUND` describe search activity.

They do not prove that something does or does not exist.

Migration must convert these into documented search information where possible:

**SEARCH SCOPE → QUERY → SOURCE → ACCESS → RESULT → VISIBILITY → BLIND SPOTS → NEXT TEST**

A negative search remains bounded by:

- jurisdiction;
- collection;
- date range;
- record type;
- spelling/name variants;
- source accessibility;
- OCR/index quality;
- surviving records.

Therefore:

> Not located is not the same thing as nonexistent.

---

## 6. NULL Firewall

`NULL` has multiple historical meanings in this archive.

It may mean:

1. a methodological null;
2. a scoped negative search;
3. a literal zero-result observation;
4. an older status vocabulary;
5. a statement that a particular hypothesis currently has no supporting evidence.

These meanings must not be silently collapsed.

### Routing rule

When legacy `NULL` is encountered:

- If it describes a search result → create or propose a `SEARCH_EVENT`.
- If it describes a literal source observation → create or propose an `EVIDENCE_EVENT`.
- If it is an old claim status → preserve under `legacy_history`.
- If it is methodological prose → preserve as methodology.
- If its meaning is ambiguous → flag for review.

**Never guess which meaning was intended.**

`NULL` must never become a current conclusion merely because the word appears in an older file.

---

## 7. KILLED / ELIMINATED Firewall

A historically `KILLED` or `ELIMINATED` hypothesis remains part of the research history.

Migration must preserve, where available:

- original claim or candidate;
- original reasoning;
- law or test applied;
- sources used;
- date;
- actor;
- contradiction;
- expected outcome;
- reason for disposition;
- possibility of reopening.

The historical disposition does not automatically become current `REJECTED`.

If the current control plane needs a verdict, the hypothesis receives a fresh test.

---

## 8. PROOF Firewall

A historical `PROOF` label does not automatically become current `VERIFIED`.

The current proof path is:

**SOURCE → SOURCE ACCESS → LITERAL OBSERVATION → CLAIM/SOURCE MATCH → PROVENANCE → CONTRADICTION CHECK → REVIEW → CURRENT STATUS**

This is especially important where:

- a citation points to the wrong volume;
- an abstract differs from the manuscript;
- an AI transcription is provisional;
- a source exists but does not actually say the claimed thing;
- a source is inaccessible;
- a secondary author may have merged two people.

A source can be genuine while still failing to support a particular claim.

---

## 9. PLAUSIBILITY Firewall

Historical `PLAUSIBLE` or `PROBABLE` reasoning must not automatically become current support.

Migration must preserve, where available:

- proposed explanation;
- observations;
- alternatives;
- reasoning;
- contamination concerns;
- expected outcome;
- falsification target;
- supporting evidence;
- contradictory evidence.

The current system then tests both:

**IF TRUE → what should we find?**

and

**IF FALSE → what should we find?**

No hypothesis receives privileged treatment because it was historically favored.

---

## 10. Suspension Firewall

A historical `SUSPENDED` item remains visible.

It must not be:

- deleted;
- silently forgotten;
- silently converted to false;
- silently converted to true;
- removed from the contradiction history.

Its current state must be established through a fresh review if needed.

---

## 11. Symmetric Testing Requirement

Every live hypothesis must have both:

### TRUE TEST

What independent evidence should exist if the hypothesis is correct?

### FALSE TEST

What evidence should exist if the hypothesis is wrong?

A search plan that only seeks confirming evidence is incomplete.

---

## 12. Observation / Inference Firewall

The archive must distinguish:

**OBSERVATION**
What the source literally shows or says.

**INFERENCE**
What follows from the observation.

**HYPOTHESIS**
An explanation that remains testable.

**TEST**
A search or comparison designed to support or challenge the hypothesis.

Agreement between these layers must never be assumed.

---

## 13. Ambiguity Rule

When legacy language has multiple possible meanings:

- preserve the original wording;
- preserve its location;
- preserve its historical context;
- flag the ambiguity;
- do not silently normalize it.

The archive chooses explicit uncertainty over a cleaner but unsupported interpretation.

---

## 14. Provenance Requirement

Every migrated or newly created control-plane event should identify, where available:

- actor type;
- actor;
- platform or wrapper;
- session/run;
- timestamp;
- source/tool;
- search context;
- relevant artifact.

AI provenance must remain visible.

A model's conclusion is not independently corroborated merely because another model agrees with it.

---

## 15. Regression Requirements

The migration system must demonstrate that:

1. `PROVEN` remains historical and does not become current `VERIFIED` automatically.
2. `ELIMINATED` remains historical and does not become `REJECTED` automatically.
3. `KILLED` remains historical and does not become `REJECTED` automatically.
4. `NULL` never becomes a current conclusion automatically.
5. `PRIMARY` / `SECONDARY` / `TERTIARY` cannot become truth values.
6. `SEARCHED` / `NOT FOUND` cannot become proof of nonexistence.
7. Ambiguous legacy language is flagged rather than guessed.
8. Original legacy text and reasoning remain recoverable.
9. Dry-run operations do not modify production ledgers.
10. No migration silently deletes or overwrites prior evidence.

---

## 16. Relationship to the Existing Methodology

The archive remembers what earlier research concluded.

The zero-trust control plane tests whether those conclusions should still be accepted.

Therefore:

> Historical status is evidence about the history of the investigation, not automatic evidence about Joan.

The control plane does not erase the old research.

It makes the distinction between **what was concluded** and **what the evidence currently supports** explicit and machine-auditable.

---

## 17. Migration Order

Migration should proceed in this order:

1. Vocabulary inspection.
2. Legacy vocabulary contract.
3. Regression tests.
4. Dry-run parser.
5. Manual review of ambiguous cases.
6. Controlled event creation.
7. Integrity audit.
8. Reread actual artifacts.
9. Generate the integrated timeline spine.

No step should silently bypass an earlier step.

---

**Core rule:**

> Preserve the history. Test the conclusion. Never let yesterday's label become today's truth without evidence.
