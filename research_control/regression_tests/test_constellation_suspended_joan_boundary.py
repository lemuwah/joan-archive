from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "joan-constellation.html"

text = HTML.read_text(encoding="utf-8")


# ------------------------------------------------------------
# 1. Locate the suspended record and verify that its public
#    description explicitly excludes it as a Joan appearance.
# ------------------------------------------------------------

node = re.search(
    r'id:"deedmay1682".*?seeking:',
    text,
    re.DOTALL,
)

assert node, "Could not locate deedmay1682 constellation node."

node_block = node.group(0)

assert "SUSPENDED" in node_block, (
    "deedmay1682 is no longer explicitly marked SUSPENDED."
)

assert re.search(
    r'Not counted as an appearance\s*of Joan',
    node_block,
), (
    "deedmay1682 no longer explicitly states that it is not "
    "counted as an appearance of Joan."
)


# ------------------------------------------------------------
# 2. A suspended record explicitly excluded as a Joan appearance
#    must not have a 'together' relationship to Joan.
# ------------------------------------------------------------

forbidden_link = re.search(
    r'\{\s*source:"deedmay1682",\s*target:"joan",\s*type:"together"\s*\}',
    text,
)

assert not forbidden_link, (
    "Suspended deedmay1682 is incorrectly projected as a "
    "'together' relationship with Joan."
)


print("CONSTELLATION SUSPENDED JOAN BOUNDARY: PASS")
