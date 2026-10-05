from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "joan-constellation.html"

text = HTML.read_text(encoding="utf-8")


# ------------------------------------------------------------
# 1. Joan and Anashuecot must remain separate person nodes.
# ------------------------------------------------------------

joan = re.search(
    r'id:"joan",\s*label:"Joan Greene",\s*type:"person"',
    text,
)
anashuecot = re.search(
    r'id:"anashuecot",\s*label:"Anashuecot",\s*type:"person"',
    text,
)

assert joan, "Joan Greene person node is missing or changed."
assert anashuecot, "Anashuecot person node is missing or changed."


# ------------------------------------------------------------
# 2. Their direct relationship must remain explicitly
#    unresolved: type:"differs".
# ------------------------------------------------------------

identity_links = re.findall(
    r'\{source:"(?:joan|anashuecot)",\s*'
    r'target:"(?:joan|anashuecot)",\s*'
    r'type:"([^"]+)"\}',
    text,
)

assert identity_links == ["differs"], (
    "Joan/Anashuecot must have exactly one direct relationship "
    f"and it must be type:'differs'; found {identity_links!r}."
)


# ------------------------------------------------------------
# 3. The Anashuecot description must continue to frame the
#    identity as an unresolved question.
# ------------------------------------------------------------

anashuecot_block = re.search(
    r'id:"anashuecot".*?seeking:',
    text,
    re.DOTALL,
)

assert anashuecot_block, "Could not locate complete Anashuecot node block."

assert re.search(
    r'Is Anashuecot the same person as Joan Greene\?',
    anashuecot_block.group(0),
), "Anashuecot/Joan identity question is no longer explicitly unresolved."


# ------------------------------------------------------------
# 4. Interaction code must not mutate relationship semantics.
# ------------------------------------------------------------

highlight_block = re.search(
    r'function highlightNeighbors\(d\)\{.*?\n\}',
    text,
    re.DOTALL,
)

assert highlight_block, "highlightNeighbors() not found."

assert "type:" not in highlight_block.group(0), (
    "highlightNeighbors() appears to mutate relationship semantics."
)

detail_block = re.search(
    r'function showDetail\(d\)\{.*?\n\}',
    text,
    re.DOTALL,
)

assert detail_block, "showDetail() not found."

assert "type:" not in detail_block.group(0), (
    "showDetail() appears to construct or mutate relationship semantics."
)


print("CONSTELLATION IDENTITY BOUNDARY: PASS")
