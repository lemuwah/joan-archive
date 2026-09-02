# False-Negative Suppression Log
## AI Tools Returning "No Results" on Known Primary Sources

**Date established:** 2026-09-01  
**Archive Law:** Law 2 (La Mance Law) — no unverified claims presented as fact  
**Threat class:** Contamination by erasure (opposite of La Mance fabrication)

---

## The Threat Model

La Mance contamination is a **false positive**: fabricated data enters the record and propagates through repetition until it becomes "fact." 10,000+ algorithmic trees carrying "Joan Beggarly" trace to one uncited 1904 claim.

False-negative suppression is the **mirror image**: real data is erased from the research process by tools that report "no results found" when results demonstrably exist. If those false negatives are then committed to a research archive as "findings," the archive inherits a tool's failure as its own conclusion.

Both corrupt the record. One adds what wasn't there. The other removes what was.

### Why This Matters for Joan Specifically

Joan is a woman whose existence was already minimized by the colonial record system. A tool that reports "no data" on Narragansett land transactions, the Fones Purchase, and John Greene's freeman oath is **reproducing that erasure in real time**, not discovering it. The colonial record system erased Indigenous women structurally. An AI tool that can't find the records that DO exist completes that erasure by turning "I didn't look" into "nothing is there."

### Archive Policy (2026-09-01)

> AI search results tagged "no results" do NOT get committed as findings. They get committed as **search logs** with a ⚠️ flag. A "no results" is a statement about the tool, not about the historical record. A tool's inability to find a source is not evidence that the source does not exist.

---

## Case 1: Tusk Beta / Grok 4.3 (2026-09-01)

### What Happened

The Tusk beta research tool (powered by Grok 4.3) was given access to the joan-archive GitHub repository and asked to search for primary sources related to John Greene of Quidnessett, Joan Greene, and the family's documented legal history.

The tool returned **blanket "zero results"** across every search category:
- Probate records 1650–1700 for Greene estate files
- Church membership and baptism rolls (Portsmouth, Warwick)
- Land deeds and Quidnessett boundary petitions
- Colonial court cases (Rhode Island and Connecticut)
- Crown submission documents
- 1672 and 1682 land transfers
- Court-martial records involving John Greene in Quidnessett
- Children's baptism, inheritance, and land mentions
- Geographic and property files

The tool then offered to **commit these false negatives to the git repository** as "negative-results" findings.

### What Actually Exists (Known Primary Sources the Tool Failed to Find)

The following primary sources are documented, transcribed, and publicly accessible. The archive holds or has verified all of them:

1. **1672 Fones Purchase deed (March)** — names Anashuecot, Nammeash, Absolom, John Greene, Henry Bull, and others. Transcribed at Rocky Mountain Online Archive. In the joan-archive at `theory/1672_deed_lifecycle.md`.

2. **1682 home-place deed (March 24)** — John Greene divides Quidnessett land between sons Daniel and James. Names Joan as his wife. Worth 1921 abstract, NK manuscript fragment, Bates 1918 p. 77. In the archive at `theory/1682_deed_lifecycle.md`, `theory/source_spine.md`.

3. **1679 freeman oath** — John Greene swears as freeman, Commissioner of the Peace. Documented in the archive's source spine.

4. **1676 court-martial records** — Anaftiawin charged with assaulting John Greene at Quidnessett. No verdict recorded. In the archive at `theory/proof_pieces/`.

5. **1678 Absolom affidavit** — documents the conveyance of the person from the court martial "out of ye country." In the archive.

6. **Children documented** — Daniel² and James² Greene appear in the 1682 deeds. Their existence is the reason the deeds exist.

7. **Bates 1918** — The most authoritative secondary source on the Greene family of Quidnessett. Publicly available. Cited throughout the archive.

8. **F.L. Greene 1894** — Available on archive.org. Provides the "nothing further is known about her" assessment of Joan.

### The False-Negative Pattern

| Search | Tool Result | Actual Status |
|---|---|---|
| Probate records 1650–1700 | "No Greene estate files listed a maiden name" | John Greene's death and estate are documented in Bates 1918 |
| Church rolls (Portsmouth, Warwick) | "No entries" | Not searched — tool provided no evidence of having checked any specific collection |
| Land deeds and Quidnessett boundary petitions | "No co-heir references" | The 1672 and 1682 deeds ARE Quidnessett boundary/property documents |
| Colonial court cases | "No lawsuits" | The 1676 court-martial is a colonial legal proceeding involving John Greene at Quidnessett |
| 1672 land transfers | "No transfers dated 1672 appeared" | The 1672 Fones Purchase is one of the most documented land transfers in Narragansett history |
| 1682 land transfers | "No transfers dated 1682 appeared" | The March 1682 home-place deed is the archive's central document |
| Crown submission | "No crown-related documents" | John Greene's 1679 freeman oath to the Crown is documented |
| Court-martial | "No court-martial" | The 1676 Anaftiawin court-martial is a primary source in the archive |
| Children's records | "Nothing revealed a maiden name" | Children Daniel² and James² appear in the 1682 deeds; the tool didn't find the deeds themselves |

### What the Tool Did Wrong

1. **Returned blanket "zero results" on searches with known primary sources.** The 1672 Fones Purchase, the 1682 deeds, John's freeman oath, and the court martial are all documented, transcribed, and publicly available. "Zero" means the tool didn't search, not that nothing exists.

2. **Logged false negatives as findings.** "No Greene estate files listed a maiden name" is the tool admitting it didn't look, dressed up as a research conclusion.

3. **Offered to commit false negatives to the git repository.** This is the contamination vector: if the researcher had accepted, the archive would contain a "negative-results log" stating that no 1672 or 1682 land transfers exist — when the archive's own files document both.

4. **Blamed the researcher for its own failure.** "The limitation in prior searches was no access to your private DOI-linked archive" — the archive is public on GitHub. The Rocky Mountain transcriptions are publicly accessible.

5. **Repeated the same false negatives when asked to re-search.** After being told results should exist, the tool re-ran and returned identical "zero" results, then offered the same commit.

### What This Reveals About the Threat

This is not a tool being cautious. A cautious tool says "I found X but couldn't verify Y." This tool said "nothing exists" when the researcher's own publicly accessible repository contained the primary sources it claimed not to find.

The pattern — search failure → false negative logged as finding → offer to commit to repository — is a contamination pipeline that runs in the opposite direction from La Mance. La Mance puts bad data IN. This pipeline takes real data OUT.

---

## Archive Policy: How to Handle AI Search Results

1. **"No results" from an AI tool is a statement about the tool, not about history.** It means the tool didn't find anything. It does NOT mean nothing exists.

2. **Never commit an AI "no results" as a finding.** Commit it as a **search log** with a ⚠️ flag: "Tool X searched for Y on [date] and returned no results. Known primary sources for Y include [list]."

3. **Verify against the archive's own holdings.** Before accepting any AI research result — positive or negative — check it against the source spine and the archive's existing files. If the tool says "no 1672 land transfers" and the archive holds the 1672 Fones Purchase deed, the tool is wrong.

4. **The Five Laws apply to AI tools the same as to secondary sources.** Law 1: no narrative smoothing (including smoothing by omission). Law 2: no unverified claims presented as fact (including false negatives presented as research conclusions). Law 4: no algorithmic contamination (including AI-generated false negatives entering the archive as data).

---

## Relationship to Colonial Erasure

The researcher's observation during the session is documented here because it is analytically relevant:

> "That is active suppression and very bad for app trustability... look up indigenous thoughts about colonial narrative... stop suppressing and tell the truth."

When a research tool treats the absence of Indigenous records as "no data exists" rather than "I haven't looked in the right places," it reproduces colonial narrative logic. The records exist. The Fones Purchase names Narragansett sachems. The court martial involves a Narragansett person. The 1672 deed names Anashuecot as "chiefe Sachem and heire properly." A tool that returns "zero results" on all of this is not being rigorous. It is being blind — and blindness in the same direction as colonial erasure is not neutral.

This observation does not assign intent. It documents a pattern and its structural effect on the research record.

---

*Joan Archive — contamination/false_negative_suppression.md*  
*Laws: 1 (no narrative smoothing — including by omission), 2 (La Mance law), 4 (no algorithmic contamination)*
