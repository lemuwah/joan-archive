# Person Identity Authority

**Status:** Contract
**Purpose:** Define the narrow boundary for documentary person objects and same-person relationships.

---

## 1. Purpose

The Person Identity Authority defines when the archive may maintain a
documentary person as a distinct research object and how identity
relationships between documentary appearances are represented.

It does **not** determine a person's ancestry, ethnicity, origin,
social status, historical importance, or relationship to a hypothesis.

It does **not** solve the identity of Joan Greene.

---

## 2. Core distinction

The archive must distinguish:

1. **Name appearance**
   - A literal name or person reference occurring in a source.
   - This is discovery data.
   - A name appearance does not establish identity.

2. **Documentary person**
   - A research object representing an individual sufficiently
     distinguished by documentary evidence to warrant a separate
     person profile.
   - Documentary personhood is not the same as complete biography.

3. **Same-person relationship**
   - An explicit research relationship asserting that two documentary
     appearances are being treated as referring to the same individual.
   - The relationship requires an identified documentary basis.
   - Similarity alone is not authority.

4. **Historical hypothesis**
   - A proposed interpretation about a person's identity, origin,
     ancestry, ethnicity, status, or relationship to another person.
   - Hypotheses remain outside the person object's identity authority.

---

## 3. Identity authority is not heuristic matching

The following are not, by themselves, sufficient to establish
SAME_PERSON:

- same or similar name;
- same surname;
- same locality;
- same occupation;
- same associates;
- same property;
- same mark or signature form;
- overlapping chronology;
- similar family structure;
- agreement between secondary genealogies;
- agreement between AI systems;
- database or catalog matching;
- repeated search results.

These may generate leads or identity-shaping research effects.

They do not constitute identity authority.

---

## 4. Documentary person objects

A documentary person object may be maintained when the archive has a
documentary basis for treating the individual as a distinct research
object.

The person object should identify:

- a stable internal person identifier;
- a display name;
- documentary source basis;
- known name forms or variants;
- relevant documented relationships;
- unresolved identity questions;
- explicit firewall constraints where conflation is a known risk.

A person object must not silently inherit conclusions from:

- search arrivals;
- Found Artifacts;
- Research Effects;
- Best Hypothesis state;
- name similarity;
- secondary genealogy alone;
- another person's profile.

---

## 5. Name appearance remains separate

A source occurrence may remain:

    NAME_APPEARANCE_ONLY

even when the archive already maintains a person with the same name.

The existence of a documentary person object must not cause every future
name match to be automatically assigned to that person.

New appearances require their own documentary identity assessment.

---

## 6. Same-person relationships

A SAME_PERSON relationship must be explicit.

It must identify:

- the two documentary appearances or person objects being related;
- the documentary basis for the relationship;
- the source or sources supporting that basis;
- the current state of the relationship.

The relationship must remain distinguishable from:

- "possible";
- "similar";
- "associated";
- "same locality";
- "same family name";
- "research lead";
- "hypothesis."

If the documentary basis is insufficient, the archive must preserve the
relationship as unresolved rather than silently resolving it.

Contradictory evidence must remain capable of reopening or preventing
the relationship.

---

## 7. Person objects do not absorb hypotheses

A person object must not encode an unresolved historical hypothesis as
an identity fact.

For example:

    PERSON-JOAN-001
        display_name: Joan Greene

does not imply:

    Joan = Anashuecot
    Joan = Narragansett
    Joan = English
    Joan = Irish
    Joan = Beggarly
    Joan = any other Joan Greene

Those propositions require separate claims or hypotheses.

The person object may link to those research questions without adopting
their conclusions.

---

## 8. Joan Greene boundary

The archive may maintain Joan Greene as a documentary research object
based on the verified documentary appearance in the 1682 Quidnessett
instrument.

That does not authorize:

- treating every "Joan Greene" as the same woman;
- treating the suspended May 1682 record as her appearance;
- assigning a maiden name;
- assigning an ethnicity or ancestry;
- assigning an origin;
- identifying her as Anashuecot;
- importing La Mance-derived identity claims;
- treating later compiled genealogy as automatic identity authority.

The current documentary basis must remain exactly as strong as the
underlying source evidence.

---

## 9. Multi-person firewall

Known same-name or potentially conflated people must remain separate
unless a documentary identity relationship authorizes convergence.

This includes, but is not limited to:

- multiple John Greenes;
- multiple Joan/Joane/Jane Greenes;
- Indigenous names with phonetic similarity;
- genealogical identities constructed from later compilations.

The existence of a plausible convergence is a reason to investigate,
not permission to merge.

---

## 10. Authority ordering

Identity authority follows this order:

    SOURCE APPEARANCE
          |
          v
    DOCUMENTARY PERSON OBJECT
          |
          v
    EXPLICIT IDENTITY RELATIONSHIP
          |
          v
    SEPARATE HISTORICAL CLAIM / HYPOTHESIS

No lower-level research artifact may silently promote itself into a
higher-level identity authority.

In particular:

    Search Result
        != Person Identity

    Found Artifact
        != Person Identity

    Research Effect
        != Person Identity

    Best Hypothesis
        != Person Identity

    Name Variant
        != Same Person

---

## 11. Failure-closed rule

If the documentary basis for a person identity or same-person
relationship cannot be established, the authority layer must preserve
the uncertainty.

It must not manufacture a person match to complete a graph, fill a
genealogy, satisfy an agent, or improve search recall.

**Unresolved is an allowed state.**

---

## 12. Relationship to the Seven Laws

This contract implements the identity side of the archive's existing
laws:

- Laws govern the machine.
- Evidence governs conclusions.
- No Premature Elimination.
- No Algorithmic Contamination.
- No Jurisdictional Assumption.
- No Centering.
- No Trust Without Evidence.
- No Narrative Smoothing.

The authority layer exists to prevent identity inference from being
silently converted into identity fact.

---

## 13. Non-goals

This contract does not:

- rank hypotheses;
- assign confidence scores;
- determine the "most likely" identity;
- eliminate competing hypotheses;
- infer ancestry;
- infer ethnicity;
- infer social status;
- infer Indigenous identity;
- determine parentage;
- determine a maiden name;
- replace source-level evidence;
- replace specialist review where Indigenous identity is concerned.

---

## 14. Required future regression coverage

Before this authority is connected to production workflows, regression
tests must demonstrate that:

1. identical names do not automatically establish SAME_PERSON;
2. identical locality does not automatically establish SAME_PERSON;
3. shared associates do not automatically establish SAME_PERSON;
4. similar marks do not automatically establish SAME_PERSON;
5. search results cannot create person identity;
6. Found Artifacts cannot create person identity;
7. Research Effects cannot create person identity;
8. Best Hypothesis cannot create person identity;
9. Joan and Anashuecot remain separate documentary person objects;
10. the Joan/Anashuecot question remains a separate unresolved
    identity hypothesis unless documentary evidence changes that state;
11. the suspended May 1682 record cannot become a Joan appearance merely
    because it contains a compatible name or narrative;
12. unresolved identity remains representable without forced resolution.

---

## 15. Governing principle

> The archive may decide to investigate a person before it can prove
> who that person was.

> It may maintain a person object before it can reconstruct the person's
> life.

> It may investigate whether two appearances are the same person
> without declaring that they are.

> It must never confuse the existence of a research object with proof
> of the historical identity assigned to it.
