Cite this archive: Green, W. (2026). Joan Archive open source research project. Zenodo. https://doi.org/10.5281/zenodo.21482575

# The Joan Archive — Open Access Research Library

**No narrative smoothing.**

🔗 **Live site:** https://lemuwah.github.io/joan-archive/

Joan, wife of John Greene of Quidnessett, appears nowhere in the English documentary record for the entire documented span of her husband's life — and then, in 1682, appears twice: two independent legal acts, five weeks apart, each requiring her own consent and her own mark. This archive exists to ask why, and to make the surviving evidence around that question easier for anyone to check.

This is not a genealogy website. It is an open-access research library — primary sources, identity firewalls, a contamination index, and a research thesis that stays labeled as a hypothesis until it earns something stronger.

### Her two known appearances

| Date | Document | What happened |
|---|---|---|
| 24 March 1682 | Home-place deed (RI Land Evidence) | John Greene divides his Quidnessett land among his sons. Joan's consent is required; a 30-shilling life-estate is reserved to her — "or to her mother if she survive." |
| 19 May 1682 | Pawtuxet deed (RI Land Evidence, Vol. VII, pp.177–178) | John Greene sells inherited Pawtuxet land to William Carpenter for £10. Joan gives separate "free & voluntary consent" and signs with her mark. Witnesses: John Wickes, Samuel Gorton. |

Forty years of total invisibility to English law doesn't end with a single mention that could be a scribal fluke. It ends with two separate transactions, two different tracts, two different sets of witnesses — both requiring her, in the same season. That pattern is the core anomaly this archive is built around.

---

## Digitization is the main event

**Less than 5% of colonial-era records in North America are digitized and searchable.** That's the actual reason this archive exists. Joan isn't lost — she's undigitized, along with almost everything else from this period:

- **60%** of microfilm produced before 1990 already shows vinegar syndrome or redox blemish (Image Permanence Institute, RIT) — it is actively failing, not just sitting in storage.
- **3–5%** annual loss rate for uncatalogued manuscript collections without climate control.
- **0** institutions currently hold a complete digitization of 17th-century land evidence across all four colonial jurisdictions that governed this exact territory.

The document that could resolve the biggest open question here — Record of a court martial held at Newport, R.I., in August, 1676 — has never been systematically digitized. It may be sitting, readable, in a library right now.

**You don't need expertise to help with this.** A phone camera exceeds the resolution of many institutional scanners. If you're near an archive that touches Narragansett Country, John Greene of Quidnessett, or Anashuecot/Absolom Counsellor between 1670–1690, a single photo of a relevant page is a real, permanent contribution — see **How to Help** on the live site for a menu of asks ranging from 60 seconds to a full afternoon. "No record found" counts too: log it in the Negative Space Log so nobody else burns six hours on the same dead end.

## Contamination is the other half of the problem

Since 1904, one uncited claim — "Joan Beggarly" — has been copied into more than 10,000 family trees across Ancestry, FamilySearch, and MyHeritage. It is chronologically impossible. It is also, right now, easier to find online than anything true. Bad sourcing doesn't just sit quietly next to good sourcing; it outcompetes it. Fixing that means both getting more primary material online *and* building tools that flag what's fabricated before it gets copied again.

Neither the digitization problem nor the contamination problem is solved by believing (or disbelieving) any hypothesis on this site. Both are solved by more eyes on more original documents.

## The working hypothesis

| | Status |
|---|---|
| **Tier 1** — Joan (wife of John Greene of Quidnessett) was a woman connected to the Narragansett sachem lineage, not an English settler's daughter with a lost paper trail | Working hypothesis |
| **Tier 2** — Joan was specifically **Anashuecot**, named "chiefe Sachem and heire" in the 1 January 1671/72 Fones Purchase deed | More speculative — suggestive, not proven |

Every claim on the site carries a status tag (Tier 1 Primary → Tier 4 Invalidated) so you can see at a glance how much weight it can bear. Open contradictions — places where the sources genuinely disagree — are marked and left open rather than resolved for the sake of a clean story.

## The four laws

1. **No Smoothing** — contradictions in the sources are displayed, not resolved away for narrative convenience.
2. **La Mance Sieve** — any claim traceable to Lora Sarah Nichols La Mance's uncited 1904 compilation is quarantined until it's independently verified from a primary source.
3. **No Early Exclusion** — hypotheses aren't ruled out just because they're inconvenient or unfamiliar.
4. **No Algorithmic Contamination** — claims that exist only because they were copied between genealogy platforms don't count as evidence, no matter how many trees repeat them.

## What's in this repository

- `index.html` — the site itself. Single file, no build step, no framework dependency — open it in a browser or serve it as-is.
- `images/` — primary source photographs and scans referenced by the site's galleries.
- `theory/`, `data/`, `notes/`, `research_queue/`, `primary_sources/` — working research files behind the public claims: source tracking, open threads, and archival targets not yet checked in person.
- `contamination/` — quarantined material: compilations and claims that trace back to uncited or fabricated sources, kept visible rather than deleted so the contamination pattern itself stays documented.
- `digitization/` — notes on how sources get photographed, transcribed, and prepared for the site.
- `agents/`, `widgets/`, `js/` — supporting research/build tooling. See `README_FOR_EXTERNAL_AGENTS.md` if you're an AI agent contributing to this project.

## How to contribute

You do not need to believe any hypothesis on this site to help. The most useful things anyone can do, roughly in order of impact:

- **Photograph something.** If you're near RI State Archives, RIHS, Kings County probate, or any regional archive touching Narragansett Country 1670–1690, a phone photo of a relevant page is a real contribution. Modern phone cameras exceed the resolution of many institutional scanners.
- **Check an archive and report back — even a negative result.** A systematic search that finds nothing narrows the field for everyone. Log it via [GitHub Issues](https://github.com/lemuwah/joan-archive/issues/new?labels=%F0%9F%94%8D+negative-space&title=Negative+Space%3A+%5BArchive+Name%5D).
- **If you work at or volunteer for an institution:** digitization capacity, cataloguing expertise, or pointers to unprocessed collections are exactly what's needed — this project exists to point people toward archives, not compete with them.

All discussion happens through [GitHub Issues](https://github.com/lemuwah/joan-archive/issues) — no account needed to read, and a GitHub login gets your note archived permanently as part of the project record. See `CONTRIBUTING.md` for format details.

If you have a Narragansett or other Indigenous research background, correction or context on kinship, land, and succession practices is treated as higher-weight input, not folded into general feedback — reach out via Issues if you'd prefer a direct conversation first.

## License

[MIT](LICENSE)

---

*This repository retains the name `joan-archive` for link continuity.*
