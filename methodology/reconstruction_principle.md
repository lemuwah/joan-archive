> This archive documents lives lived between approximately 1600–1750 in Narragansett country (present-day Rhode Island). All records from this period were created within colonial legal systems and reflect their biases, categories, and blind spots. Every name found here — English, Narragansett, Niantic, mixed-heritage, unknown — represents a real person whose full story these records were not designed to capture. Content may include references to war, captivity, enslavement, displacement, legal coercion, and loss. These are documented realities of the period, not abstractions. All cultural and genealogical content is included for research purposes in the quest to identify Joan Unknown Greene and will be revised or removed if requested by descendant communities or tribal representatives.

# Law 8 — The Recursive Pass

**Status:** Active methodology component — completes the cycle the Seven Laws begin.  
**Supersedes:** Previous "Reconstruction Principle" (2026-09-11).  
**Evolution driven by:** Claude stress-test feedback (Martin Guerre, Anne Frank Cold Case Team failure modes), Pawtuxet citation walkback, Jack the Ripper negative control.

---

## The Problem

Laws 1–7 are **subtractive**. They strip contamination. They correctly return null when the evidence doesn't support a conclusion. That's a mechanical operation: does this claim trace to a primary source? Yes → keep. No → strip. No judgment call required. The Ripper stress test proved this works universally.

But the Joan Archive doesn't stop at null. It attempts **reconstruction** — building identity from converging edges after the stripping is done. And reconstruction requires someone to decide that two edges are *independent* of each other. That's a judgment call, not a mechanical check.

**Every archive error in this project has come from that judgment call:**

- **Pawtuxet citation walkback** — treated something as independently confirmed when it traced back to one source
- **Martin Guerre** — neighbors who "independently" recognized the imposter were all under the same social pressure; same source dressed as multiple data points
- **Anne Frank Cold Case Team** — AI treated downstream inferences as independent when they all traced back to one uncorroborated note

The pattern: **convergence that feels independent but isn't.**

## The Law

> When edges from the primary corpus appear to converge on the same identity, the convergence itself becomes a new claim. Run Laws 1–7 on the convergence. Then run the four falsification tests. The convergence is accepted only when it survives the full recursive pass with no unresolved flags.

### The Recursive Pass

Apply each law to the convergence claim, not just the individual edges:

- **Law 1 on the convergence:** Does a document state the convergence, or did we smooth it into existence? "These two edges point to the same person" — does a document SAY that, or did we infer it?
- **Law 2 on the convergence:** Can we trace the convergence to independent primary sources? Or does it only exist because we connected two records that don't reference each other?
- **Law 3 on the convergence:** Are we prematurely eliminating alternative convergence targets? Could these edges converge on a *different* identity?
- **Law 4 on the convergence:** Is the convergence contaminated by shared sourcing? Did one source generate the other? Did a secondary tree connect them?
- **Law 5 on the convergence:** Have we checked all jurisdictions? Could the convergence break if we look at a record from a different court, colony, or parish?
- **Law 6 on the convergence:** Are we centering a preferred theory? Are we *looking* for this convergence because we want Joan to be someone specific?
- **Law 7 on the convergence:** Does the convergence carry a verified evidence chain from its own primary source chain? Or is it sitting on unverified claims that happened to point the same direction?

### The Four Falsification Tests

After the recursive pass, the convergence must survive these four tests:

**8a — Source Independence**  
Do all edges in the convergence trace to separate, non-derived primary sources? For every edge, trace it backward. If two edges share any ancestor in their source chains — same document, same informant, same institutional record, same chain of inference — they are not independent. They collapse to one edge.

**8b — Alternative Target**  
Could a different person satisfy the same edge set? Generate the list of alternative people who could fit the same edges. If more than one person fits, the convergence is ambiguous, not identifying. (This is the 5-Johns problem formalized.)

**8c — Environmental Noise**  
Would random individuals in the same time, place, and circumstance produce the same convergence? If yes, the convergence is geography and shared context, not identity. The Ripper stress test proved this: five victims converged on Whitechapel because they all lived in Whitechapel, not because a single person connected them.

**8d — Breaking Evidence**  
What specific document, if found, would dissolve this convergence? State it explicitly. Then look for it. If you don't look for the breaking evidence, you haven't tested the claim.

## System-Generated Directions

After running Laws 1–7 and tests 8a–8d on a convergence, the system generates **specific, testable directions** — archives to check, documents to find, alternative explanations to rule out. The convergence status stays open until every direction has been pursued or explicitly parked.

Example output:

> "The convergence between Edge A (1682 deed) and Edge B (1679 affidavit) survives Laws 1, 3, 5, 6, and 7. It **fails** Law 2 (no primary source independently confirms the connection between these two documents) and is **untested** on 8a (we haven't verified the two documents were produced by different scribes/courts). **Recommended tests:**
>
> 1. Check whether the 1682 deed clerk had access to the 1679 affidavit
> 2. Search for a third document from a different jurisdiction naming Joan in the same relational position
> 3. Test 8b: which other women named Joan in Narragansett country 1670–1690 could satisfy the same edges?"

## Anti-Theory Protocol

For every convergence theory about Joan's identity, the spine holds two entries:

1. **The theory** — the convergence claim with its edge set
2. **The anti-theory** — a deliberately constructed alternative that uses the same edges to point somewhere else

If the edges can support both, neither is confirmed. If only one survives the full recursive pass + falsification, that's signal. If neither survives, the identity is genuinely unknown — which is honest.

## Multi-Agent Bias Check

Different AIs have different biases. Log which agent built the convergence case and which tested it. Same-agent build-and-test is flagged as single-agent bias risk — not disqualified, but flagged.

- One agent builds the convergence case ("prosecutor")
- A different agent tries to break it ("defense")
- A third evaluates whether the break attempt was genuinely adversarial ("judge")

## Status Tags for Convergence Claims

- 🟢 **RECONSTRUCTED** — survived the full recursive pass (Laws 1–7) + all four falsification tests (8a–8d). All directions pursued.
- 🟡 **CONVERGENCE FLAGGED** — recursive pass completed, one or more flags remain. Specific laws/tests that failed are listed with the specific test that would resolve them.
- 🟠 **CONVERGENCE PENDING** — recursive pass not yet complete. Directions generated but not yet pursued.
- 🔴 **CONVERGENCE KILLED** — recursive pass failed. Specific law/test that killed it is documented. Claim stays on the spine. Never deleted.
- 🔵 **CONVERGENCE UNTESTABLE** — no known archive or surviving record could confirm or deny. Not false, not confirmed. Parked.

## Comparison to Previous Version

| | Old Reconstruction Principle | Law 8 — Recursive Pass |
|---|---|---|
| Tests convergence? | Asserted convergence = confirmed | Convergence = new claim, tested by Laws 1–7 |
| Tests independence? | Assumed | Explicitly tested (8a) |
| Tests alternatives? | Identity Firewall only | Formalized (8b) |
| Tests environmental noise? | No | Formalized (8c) |
| Looks for breaking evidence? | No | Formalized (8d) |
| System generates directions? | No | Yes — specific, testable |
| Anti-theory protocol? | No | Yes — strongest alternative constructed |
| Multi-agent bias check? | No | Yes — logged per convergence |

## Where It's Being Tested

- **12-Name Experiment** (`methodology/12-name-experiment/`) — testing whether relational density can recover identities that names alone cannot. Law 8 recursive pass applies to every convergence the experiment produces.
- **Esther Smith control** (`methodology/12-name-experiment/controls/esther-smith.md`) — known identity used as positive control.
- **Gorton daughters control** (`methodology/12-name-experiment/controls/gorton-daughters.md`) — six known identities showing maximum achievable relational density.
- **Ripper stress test** (`methodology/stress-tests/ripper-case.md`) — negative control proving the laws correctly return null. Also proved that environmental convergence (Whitechapel geography) is a complete alternative explanation for edge overlap — the 8c test formalized.

---

> **Search direction bias check:** When an agent recommends "where to look next," ask: is this recommendation biased toward digitized, English-language, colonial-framework sources? What record types exist that this agent might not know to suggest? What would a Narragansett historian, a maritime historian, an archaeologist, a linguist look for that a genealogist wouldn't?

---

*Joan Archive — methodology/reconstruction_principle.md*  
*Nothing is proven until original proof images are on the archive.*  
*Evolved: 2026-09-12 — Wendy Green (methodology design) + Claude (stress-test feedback that exposed the structural failure) + DeepSeek (Ripper analysis that proved stripping works) + Migoo (documentation)*  
*Previous version: 2026-09-11 — archived in git history*