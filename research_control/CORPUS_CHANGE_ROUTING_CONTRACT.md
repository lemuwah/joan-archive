# Corpus Change Routing Contract

**Status:** DRAFT — architecture under review  
**Purpose:** Govern how changes to archive artifacts are detected, preserved, classified, and routed for testing without silently changing historical conclusions.

---

## 1. Governing Principle

**Laws govern the machine; evidence governs conclusions.**

The repository contains artifacts of different kinds: source records, transcriptions, evidence records, person pages, hypotheses, contradictions, research notes, generated outputs, operational queues, and review records.

Presence in the repository does not establish historical truth.

A Markdown file, JSON file, YAML file, generated report, transcription, research note, or agent output may contain observations, inherited conclusions, hypotheses, contradictions, or errors.

Therefore:

> **No artifact becomes authoritative merely because it exists in the archive.**

Historical claims must remain subject to the archive's evidence and review rules.

---

## 2. Purpose

The corpus change-routing layer exists to ensure that changes to archive artifacts:

1. are detected;
2. are preserved;
3. are classified by artifact population;
4. are routed to the appropriate existing review or validation machinery;
5. preserve contradictions and competing interpretations;
6. preserve prior states;
7. never silently promote or demote historical conclusions.

The routing layer is an orchestration layer.

It is not a truth engine.

---

## 3. Definitions

### Artifact

Any tracked or intentionally retained repository object that participates in research, evidence, methodology, review, provenance, or historical reconstruction.

### Historical-bearing artifact

An artifact whose contents may contain or affect an observation, source reading, evidence relationship, historical claim, identity hypothesis, contradiction, correction, or reconstruction.

### Change

Any addition, modification, rename, move, or deletion of an artifact.

A change is an event about the artifact.

A change is **not** itself a conclusion about the history.

### Snapshot

An immutable record of a prior artifact state, including sufficient identity and content information to establish what existed at that point.

### Routing

Determining which population-specific process should examine a changed artifact.

Routing does not adjudicate historical truth.

### Contradiction

A documented conflict between observations, readings, records, claims, hypotheses, or interpretations.

Contradictions are retained until evidence resolves them or the archive explicitly records their disposition.

### Untested content

Content that has not yet passed the applicable source, provenance, evidence, paleographic, contradiction, or review requirements.

---

## 4. Untested Markdown Rule

Markdown is a storage format, not an evidence status.

A `.md` file may contain:

- source observations;
- working transcriptions;
- AI-assisted readings;
- researcher notes;
- inherited genealogy;
- hypotheses;
- interpretations;
- corrections;
- contradictions;
- provisional conclusions.

Therefore:

> **The contents of a Markdown file must not be treated as established historical fact solely because the file is present in the archive.**

Where a Markdown artifact contains historical-bearing material, the relevant content must be tested through the appropriate archive process before receiving authoritative status.

---

## 5. Immutable Preservation Rule

When a historical-bearing artifact changes:

**previous state must remain recoverable.**

The system must preserve, as applicable:

- prior path;
- prior content hash;
- new path;
- new content hash;
- change type;
- detection time;
- provenance;
- relevant source or run identifier;
- routing decision;
- resulting review state.

A new version does not erase the existence of the old version.

---

## 6. Contradiction Preservation Rule

Contradictions must never be deleted merely because a newer reading, interpretation, or hypothesis appears preferable.

The system must not silently transform:

**CONTRADICTION → RESOLVED**

merely because one artifact was edited.

Resolution requires the applicable evidence and review process.

Until resolved, competing readings or propositions remain part of the research record.

A contradiction may be:

- confirmed as genuine;
- resolved by primary evidence;
- resolved by correction of a transcription;
- narrowed;
- reclassified;
- suspended pending evidence;
- shown to arise from source contamination;
- shown to remain unresolved.

Each disposition must itself be traceable.

---

## 7. No Truth-by-Edit Rule

Changing or deleting text does not establish that the previous proposition was false.

In particular:

- deleting a claim does not prove the claim false;
- replacing a name does not prove an identity merge;
- replacing a transcription does not prove the earlier reading wrong;
- removing a contradiction does not prove the contradiction resolved;
- changing a hypothesis does not eliminate its historical research value;
- changing a status word does not authorize the status transition.

The routing system preserves the change and sends it for appropriate testing.

---

## 8. Artifact Populations

The corpus is divided into populations because different artifact types require different handling.

| Population | Primary concern | Default routing |
|---|---|---|
| `corpus/` | source-derived records | source integrity / corpus review |
| `digitization/` | transcription and digitization | transcription review |
| `evidence/` | evidentiary records | evidence validation / status review |
| `primary_sources/` | curated source records | source validation |
| `staging/` | temporary research material | staging / CARE-B review |
| `theory/` | hypotheses and reconstruction | hypothesis testing / hostile review |
| `people/` | person research pages | immutable snapshot / synthesis review |
| `research/` | working research records | source integrity / research audit |
| `research_findings/` | findings | findings router |
| `data/` | structured research data | data validation / evidence review |
| `research_queue/` | operational research outputs | run/provenance validation |
| `agents/` | agent logic and outputs | agent audit / logic snapshot |
| `contamination/` | quarantined material | contamination review |
| `contradictions/` | contradiction records | contradiction review |
| `corrections/` | correction records | correction review |
| `pending_review/` | disposable drafts | CARE-B review |
| `review/` | review results | review-trail validation |
| `reports/` | generated reports | regeneration / validation |

This table defines routing responsibility, not historical status.

---

## 9. Historical vs Ephemeral Artifacts

The routing system must distinguish between:

### Historical-bearing artifacts

These preserve research history and must not be silently discarded.

Examples include:

- evidence;
- source records;
- person pages;
- contradictions;
- corrections;
- hypotheses;
- research findings;
- research observations;
- structured historical data;
- source/transcription records.

### Ephemeral artifacts

These exist primarily as temporary working material and may be discarded according to their own contract.

Examples may include:

- temporary drafts;
- disposable staging material;
- intermediate generated files;
- temporary operational artifacts.

An artifact must not be treated as ephemeral merely because deletion is convenient.

---

## 10. Generated vs Authored Content

Generated content must be distinguished from authored historical records.

A generated report changing does not necessarily mean the underlying historical evidence changed.

Likewise, a source-derived Markdown file changing may require source/transcription review rather than immediate claim revision.

Where possible, routing records:

- generator;
- input artifacts;
- generation run;
- generation timestamp;
- content hash;
- upstream dependencies.

Generated output must not silently become independent evidence.

---

## 11. Population-Specific Routing

The routing layer should compose existing specialized tools rather than replace them with one universal validator.

Examples:

### `people/`

Changed person pages should enter the immutable snapshot/synthesis mechanism.

Existing historical page content remains recoverable.

### `research_findings/`

Changed findings should pass through the findings routing process.

### `evidence/`

Changed evidentiary records should pass through evidence validation and appropriate review.

### `research/`

Changed source-working records should pass through source/integrity review.

### `theory/`

Changed hypotheses or reconstruction records should enter hypothesis testing and hostile review.

### `contradictions/`

Changed contradiction records require contradiction review.

### `corrections/`

Changed corrections require correction-trail review.

### `agents/`

Changed agent logic requires logic snapshotting and run-provenance review.

The router should invoke or record the appropriate process rather than duplicate its logic.

---

## 12. Routing Must Not Determine Historical Status

The routing layer must never independently assign:

- PROOF;
- PLAUSIBLE;
- DISPROVEN;
- SUSPENDED;
- REJECTED;
- verified identity;
- ancestry;
- cultural affiliation;
- historical relationship;
- final interpretation.

Routing answers:

> **What changed, what was affected, and what process must examine it?**

Evidence and review processes answer:

> **What does the evidence establish?**

---

## 13. Provenance Gate Boundary

The Provenance Gate may determine whether required provenance and record structure exist.

It must not use a file change as evidence that a historical proposition is true or false.

A changed artifact may therefore:

- pass provenance requirements while remaining historically untested;
- fail provenance requirements while remaining historically possible;
- require additional source inspection;
- remain pending human review.

Provenance is necessary infrastructure, not historical adjudication.

---

## 14. Status Gate Boundary

Status transitions remain governed by the status/evidence machinery.

A change-routing event must not itself trigger a historical status transition merely because content changed.

For example:

**edited Markdown ≠ false claim**

**new transcription ≠ proven transcription**

**new hypothesis ≠ eliminated competitor**

**deleted sentence ≠ disproven proposition**

**new source lead ≠ evidence**

---

## 15. AI-Generated or AI-Assisted Changes

AI output is treated as research material requiring appropriate testing.

AI agreement does not constitute independent corroboration.

AI-generated or AI-assisted changes must retain, where applicable:

- model/agent identity;
- run identifier;
- source/input reference;
- date;
- working status;
- uncertainty;
- human review state.

AI must not silently:

- create verified historical fact;
- identify Joan;
- merge identities;
- eliminate a competing identity;
- delete contradictions;
- convert absence into proof;
- convert AI agreement into corroboration.

---

## 16. Deletion Handling

Deletion of a historical-bearing artifact is itself a change event.

The router must preserve sufficient information to establish:

- that the artifact existed;
- its prior path;
- its prior content identity/hash;
- when deletion was detected;
- whether it was intentional;
- what historical-bearing material may have been affected.

Deletion must not automatically mean:

**FALSE**

**REJECTED**

**DISPROVEN**

or

**NO LONGER RELEVANT**.

A deletion may be administrative, corrective, accidental, generated-file cleanup, or part of a legitimate archival transition.

Its historical meaning must be determined separately.

---

## 17. Renames and Moves

A rename or move must not be interpreted as deletion plus unrelated creation when repository history or content identity establishes continuity.

The routing layer should preserve:

**OLD PATH → NEW PATH**

along with content hashes where available.

Population changes caused by a move must be detected and routed appropriately.

---

## 18. Cross-Population Changes

A single research change may affect multiple populations.

Example:

A transcription in `research/` changes.

That may affect:

- `corpus/`;
- `digitization/`;
- `evidence/`;
- `people/`;
- `theory/`;
- contradictions;
- generated reports.

The router must not assume that the changed file is the only affected artifact.

Where dependencies are known, downstream artifacts should be identified for review.

However, dependency detection must not manufacture historical relationships.

---

## 19. Name and Identity Changes

Names are especially sensitive historical-bearing content.

A changed name may represent:

- spelling normalization;
- paleographic correction;
- transcription correction;
- alias;
- variant spelling;
- separate person;
- proposed identity merge;
- proposed identity split;
- inherited genealogical assertion;
- unresolved ambiguity.

Therefore:

> **A name change must never automatically merge or split historical identities.**

The appropriate identity-disambiguation process must test the relationship.

This applies to Joan and to every other person represented in the archive.

---

## 20. Absence and Negative Knowledge

A changed or missing file must not automatically create a negative historical conclusion.

Examples:

**file absent ≠ record absent**

**search result absent ≠ historical absence**

**no Markdown page ≠ no person**

**no transcription ≠ no document**

**no result from an AI search ≠ no record exists**

Negative knowledge must remain tied to the actual search scope and methodology that produced it.

---

## 21. Routing Event Requirements

A corpus-change event should record, where applicable:

- event ID;
- artifact path;
- population;
- change type;
- old hash;
- new hash;
- detection time;
- source/run identifier;
- upstream dependency;
- affected historical-bearing content;
- required test;
- routing destination;
- preservation result;
- review status;
- contradictions affected;
- next action.

The event records what happened.

It does not declare the historical conclusion.

---

## 22. Auditability

A reviewer must be able to trace:

**ARTIFACT → CHANGE → SNAPSHOT → ROUTE → TEST → RESULT → REVIEW → STATUS**

If a change cannot be traced through that chain, the routing system has failed its audit requirement.

---

## 23. Regression Requirements

The routing system must be regression-tested against at least:

1. new historical Markdown;
2. modified historical Markdown;
3. deleted historical Markdown;
4. renamed historical Markdown;
5. modified transcription;
6. modified evidence record;
7. modified person page;
8. modified hypothesis;
9. modified contradiction;
10. modified correction;
11. generated-output change;
12. AI-assisted change;
13. unchanged file;
14. simultaneous changes across populations;
15. conflicting changes;
16. attempted contradiction deletion;
17. attempted historical-status change through Markdown alone;
18. source-library manifest change;
19. source-library referenced-record change;
20. stale generated artifact.

Regression tests must verify preservation and routing without granting historical authority to the changed content.

---

## 24. Failure Principle

When the routing system cannot determine what changed or where the change belongs, it must prefer:

**PRESERVE → FLAG → ROUTE FOR REVIEW**

over:

**GUESS → NORMALIZE → DELETE**

Ambiguity is a research condition, not a machine error to be hidden.

---

## 25. Final Rule

The corpus change-routing system exists to protect the research record while moving evidence through the archive's existing controls.

It must make the archive better at remembering:

- what was said;
- what was observed;
- what changed;
- what contradicted it;
- what was tested;
- what survived;
- what failed;
- what remains unknown.

The archive does not need to know the answer before the evidence does.

**Preserve the record. Preserve the contradiction. Test the claim. Let the evidence decide.**
