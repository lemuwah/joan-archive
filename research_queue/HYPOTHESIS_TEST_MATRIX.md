# Hypothesis Test Matrix

**Status:** Active  
**Added:** 2026-09-06  
**Purpose:** Track what has actually been searched for each model. A model is not exhausted until every row in its section has been run. See `AGENT_GUARDRAILS.md` §9.

---

## How to Use This File

1. Before claiming a model is IMPLAUSIBLE or ELIMINATED, check its section below.
2. If a search target shows ⬜ NOT STARTED or 🟡 PARTIAL, the model has not been fully tested.
3. Update status **in the same commit** as the search that changed it.
4. Add new search targets as they are identified — this matrix grows with the research.

---

## Model A — Narragansett Sachem-Line Woman

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| RI Land Evidences Vol. I — all women named in deeds 1648–1696 | 🟡 PARTIAL | 2026-09-03 | Image 10 read (Joan). Other images not systematically searched for comparable women. |
| Potter 1835 — Narragansett sachems' family trees | 🟡 PARTIAL | 2026-08-30 | Tomanick/Awashousse investigated. No Joan equivalent found. |
| Fones Record — all named women | 🟡 PARTIAL | 2026-08-30 | Awassuocitt cluster investigated. No direct Joan link. |
| Church records (Baptist, Quaker) — Narragansett country 1660–1700 | ⬜ NOT STARTED | — | Quaker meetings may have recorded Indigenous wives. |
| Comparative deed analysis — "his wife" clauses 1660–1690 | ⬜ NOT STARTED | — | Are other Narragansett-area deeds structured like the 1682 deed? |
| Ninigret II / Narragansett sachem genealogy — named women | ⬜ NOT STARTED | — | Cross-reference with known sachem-line women. |

## Model B — English Woman, Undocumented

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| Ship passenger lists 1640–1670 — "Joan" arrivals to RI/CT/MA | ⬜ NOT STARTED | — | Hotten, Banks, Coldham compilations. |
| English parish records — Joan + Greene marriage | ⬜ NOT STARTED | — | Would need to know which parish. Broad search impractical without leads. |
| CT/MA vital records — Joan marriages 1650–1675 | ⬜ NOT STARTED | — | If she came through another colony first. |
| Wickford/Cocumscussoc English settler women — named wives | ⬜ NOT STARTED | — | Are other English wives in the area similarly undocumented? |

## Model C — Irish Origin

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| Irish servant/emigrant lists — RI bound 1650–1675 | ⬜ NOT STARTED | — | Cromwellian-era transportation records. |
| Barbados–RI connection — Irish via Caribbean | ⬜ NOT STARTED | — | Known migration path. |
| Catholic/recusant records — Narragansett country | ⬜ NOT STARTED | — | Longstanding Catholic presence in RI due to religious freedom. |

## Model D — Indentured Servant

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| RI court records — indenture releases 1660–1680 | ⬜ NOT STARTED | — | Would show completion of service. |
| Richard Smith trading post records — servants/workers | ⬜ NOT STARTED | — | John "lived with" Smith. Was Joan there too? |
| Comparative: other servant-to-wife cases in RI | ⬜ NOT STARTED | — | How common was this pattern? |

## Model E — Enslaved Person

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| Post-1676 disposition records — women assigned/sold | 🟡 PARTIAL | 2026-08-31 | 1676 Disposal Act researched. No Joan found. Sarah + Marcy repo searched. |
| Richard Smith household — enslaved persons | ⬜ NOT STARTED | — | Smith was a major landholder. |
| Narragansett Planters — enslaved women records 1670s–1690s | ⬜ NOT STARTED | — | The Planter class held both Indigenous and African enslaved people. |

## Model F — Widow of Prior Marriage

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| RI/CT probate records — widows named Joan 1660–1680 | ⬜ NOT STARTED | — | Could identify a prior husband. |
| Land records — dower rights / widow's thirds involving Joan | ⬜ NOT STARTED | — | If she had prior property rights. |
| Comparative: second marriages in Narragansett country | ⬜ NOT STARTED | — | How common, how documented? |

## Model G — Beggarly / La Mance — 🔴 ELIMINATED

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| La Mance (1904) chain traced | ✅ COMPLETE | 2026-08-28 | Wrong John Greene, wrong town, timeline impossible. See `contamination/la_mance_chain.md`. |
| Alice Daniels identity verified | ✅ COMPLETE | 2026-08-28 | She married John Greene of Warwick (the Surgeon's son), not our John. |

## Model H — Mixed-Heritage (English/Narragansett)

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| Documented English–Narragansett unions pre-1680 | ⬜ NOT STARTED | — | Williams, Gorton, trading post communities. |
| Children of mixed unions — naming patterns | ⬜ NOT STARTED | — | How were they recorded? English name? Native name? Both? |
| Northern Node community composition 1650–1680 | 🟡 PARTIAL | 2026-08-30 | Awassuocitt/Baker investigation touched this. |
| Baptismal records — mixed-heritage children | ⬜ NOT STARTED | — | If any were baptized in English churches. |

## Cross-Cutting: Origin Outside RI

| Search Target | Status | Last Checked | Notes |
|---|---|---|---|
| CT colony records — Joan + Greene | ⬜ NOT STARTED | — | John had CT connections (jurisdiction dispute). |
| Plymouth colony records — Joan + Greene | ⬜ NOT STARTED | — | Adjacent jurisdiction. |
| MA Bay colony records — Joan + Greene | ⬜ NOT STARTED | — | Hartford/Springfield connection? |
| Crown records — marriage licenses 1660–1680 | ⬜ NOT STARTED | — | If marriage occurred under Crown authority. |

---

## Five-John Firewall — Search Verification

The same "no default to unidentified" rule applies to each John. Before attributing a record to a specific John, the qualifying identifier must be present in the source.

| John | Key Identifier | Verified Sources | Unresolved Attributions |
|---|---|---|---|
| #1 Surgeon of Warwick | "surgeon", Gillingham, will 1658 | Will, Warwick deeds | — |
| #2 Quidnessett (OUR JOHN) | "lived with" Smith, wife Joan, "Senr" | 1679 affidavit, 1682 deed (Image 10), 1672 Fones deed | 1686 address (🟡 PROBABLE = Warwick John, not ours), 1692 witness deed (⚠️ OPEN) |
| #3 Jr of Warwick | "Junr" in deeds | Warwick deeds, 1686 agent to England | — |
| #4 Newport | May = #2 | Bates says so (PLAUSIBLE) | Newport records not independently searched |
| #5 Kingstown | May = #2 | Post-incorporation name | Kingstown freemen list 1696 |

---

*Maintained under Law 3 (No Premature Disqualification) and Law 7 (No Trust Without Evidence).*  
*Update status in the same commit as the search. A blank row is an open question, not a negative result.*
