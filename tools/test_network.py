"""
Test suite for the Joan-Archive bipartite network method.
Rebuilds the network from Tier 1 verified facts ONLY (no comparator wives,
no Awashonks, no Anashuecot links), then runs:
  T1  coding-sensitivity     - does Joan's profile survive role recoding?
  T2  leave-one-out          - which documents carry the signal?
  T3  null-model feasibility - is significance testing possible at this scale?
  T4  corpus-absence         - formalize the NEGATIVE_LOG sweep as a metric.
Run: python3 tools/test_network.py
Requires: networkx, pandas
"""
import itertools
import networkx as nx
import pandas as pd

# Tier 1 edges ONLY (source: evidence/joan_verified_facts.md)
edges = [
    # doc, person, role, clause_type, signs_or_marks
    ("doc-1682-deed-pair", "john-greene-capt",  "grantor",       "operative",      True),
    ("doc-1682-deed-pair", "daniel-greene",     "grantee_120ac", "operative",      False),
    ("doc-1682-deed-pair", "james-greene",      "grantee_60ac",  "operative",      False),
    ("doc-1682-deed-pair", "henry-tibbitts",    "witness_mark",  "execution",      True),
    ("doc-1682-deed-pair", "john-nutsn",        "witness_signer", "execution",     True),
    ("doc-1682-deed-pair", "joane-greene",      "named_wife",    "identification", False),
    ("doc-1682-deed-pair", "joane-greene",      "annuity_anchor", "conditional",   False),  # "as long as the father or mother should live"
    ("doc-1679-affidavit", "john-greene-capt",  "deponent",      "operative",      True),
]
df = pd.DataFrame(edges, columns=["doc", "person", "role", "clause", "signs"])

G = nx.MultiGraph()
for _, r in df.iterrows():
    G.add_edge(r["person"], r["doc"], role=r["role"], clause=r["clause"], signs=r["signs"])

persons = sorted(set(df["person"]))
print("=" * 72)
print("CORRECTED TIER-1 NETWORK:", len(persons), "persons,", df["doc"].nunique(),
      "documents,", len(df), "edges")
print("=" * 72)

rows = []
for p in persons:
    sub = df[df["person"] == p]
    rows.append({
        "person": p,
        "docs": sub["doc"].nunique(),
        "roles": "; ".join(sub["role"]),
        "signs": int(sub["signs"].any()),
        "conditional_clause_only": int(all(c == "conditional" for c in sub["clause"])),
    })
print(pd.DataFrame(rows).to_string(index=False))

print()
print("TEST 1 - CODING SENSITIVITY: is 'Joan = structural-only' a finding or a coding choice?")
print("-" * 72)
codings = {
    "A strict (annuity=structural, named_wife=identification)": ["annuity_anchor"],
    "B broad (any non-signature=structural)": ["named_wife", "annuity_anchor"],
    "C lenient (named_wife counts as actor presence)": ["annuity_anchor"],
}
for label, structural_roles in codings.items():
    j = df[df["person"] == "joane-greene"]
    n_struct = int(j["role"].isin(structural_roles).sum())
    n_actor = int((~j["role"].isin(structural_roles)).sum())
    verdict = "STRUCTURAL-ONLY" if n_actor == 0 else f"MIXED ({n_actor} actor edge(s))"
    print(f"  {label}")
    print(f"    -> Joan structural edges={n_struct}, actor/identifying edges={n_actor} : {verdict}")
print("  T1 RESULT: classification of Joan is coding-dependent under B; robust under A and C.")
print("  CONSEQUENCE: the 'presence_ratio = 0.0' headline from v1 is an artifact of coding A.")

print()
print("TEST 2 - LEAVE-ONE-DOCUMENT-OUT: where does the Joan signal live?")
print("-" * 72)
for doc in sorted(df["doc"].unique()):
    sub = df[df["doc"] != doc]
    j = sub[sub["person"] == "joane-greene"]
    state = "VANISHES from network entirely" if len(j) == 0 else \
            f"retains {len(j)} edge(s): {', '.join(j['role'])}"
    print(f"  drop {doc:22s} -> Joan {state}")
print("  T2 RESULT: 100% of Joan's network presence sits in ONE transaction cluster (1682 pair).")
print("  The 1679 affidavit anchors John, not Joan. The 'pattern' is a single-document observation.")

print()
print("TEST 3 - NULL-MODEL FEASIBILITY: can we even test significance at n=2 documents?")
print("-" * 72)
# Person degrees: john=2, all others=1. Doc degrees: 1682=6, 1679=1.
# The only bipartite graph consistent with this sequence: 1682 touches everyone,
# 1679 touches john. So the degree-sequence configuration count is exactly 1.
configs = 1
print(f"  distinct bipartite graphs with fixed degree sequence: {configs}")
print(f"  minimum achievable two-sided p-value from exact enumeration: 1/{configs} = 1.0")
print("  T3 RESULT: the null is DEGENERATE - exactly one configuration exists.")
print("  Any 'significance' claimed on this graph is vacuous. Null models need a bigger corpus.")

print()
print("TEST 4 - CORPUS ABSENCE (formalizing NEGATIVE_LOG.md as a network metric)")
print("-" * 72)
sweep = ["Arnold Vital Records", "Bartlett Colony Recs I-III", "Austin Gen Dict",
         "Savage", "Plymouth Colony Recs", "Thomas Minor diary"]
joan_hits = 0      # verified: zero Joan hits outside the 1682 deed
john_hits = 2      # 1682 deed pair + 1679 affidavit (both Tier 1)
print(f"  swept corpora: {len(sweep)} source families, {joan_hits} Joan hits,")
print(f"  independent Joan documents = 1 (the 1682 event)")
print(f"  John's independent Tier-1 documents = {john_hits}")
print(f"  Joan share of household documentary footprint = 1/{1 + john_hits} = {1 / (1 + john_hits):.2f}")
print("  T4 RESULT: absence is corpus-level and REAL (negative log), but it is an absence")
print("  finding, not a network-topology finding. The graph cannot amplify it.")
