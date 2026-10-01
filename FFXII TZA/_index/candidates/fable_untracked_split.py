# untracked_split.py : split SWE2-AUDIT-SPEC's 71 "unregistered open items" into the two different
# things they are, because they need different remedies.
#
#   ID-PRESENT   the bullet carries a question id that DOES have a row in OPEN-QUESTIONS.md - the
#                item is tracked and the census missed it (an id written at the END of a bullet, as
#                `**AQ-1.**`, is not where a start-of-bullet extractor looks).
#   ID-ORPHAN    the bullet carries an id with NO row in the register - an id was allocated and the
#                row was never written.
#   NO-ID        the bullet carries no id at all - genuinely untracked, and the only group that
#                needs new ids.
#
# Control: the Phyre subsystem map must come back ID-PRESENT (AQ-1..AQ-6 all have rows), and the two
# Glyph-Run-Rendering pages must come back NO-ID. Both were checked by hand first.
import io
import os
import re

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
os.chdir(ROOT)

PAGES = [
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/as7-menu-graphics-containers.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/btm-exfont-bitmaps.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lst-menuquest-list.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mg-worldmap-mesh.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mrp-menu-resource-packages.md",
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/wmap-menumap-world-map-graph.md",
    "02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md",
    "12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md",
    "17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md",
    "17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md",
    "22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md",
    "99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md",
    "99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md",
]

reg = io.open("_index/OPEN-QUESTIONS.md", encoding="utf-8", errors="replace").read()
# a registered id is one that appears as the FIRST cell of a table row
REG_IDS = set(re.findall(r"^\|\s*\*{0,2}([A-Z]{1,4}-\d+)\*{0,2}\s*\|", reg, re.M))
ID_RE = re.compile(r"\b([A-Z]{1,4}-\d+)\b")


def open_items(path):
    """Top-level §7 bullets that are not [x]-answered and not struck through."""
    t = io.open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"^## 7\.[^\n]*\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if not m:
        return []
    out, cur = [], None
    for line in m.group(1).split("\n"):
        if re.match(r"^- ", line):
            if cur:
                out.append(cur)
            cur = line
        elif cur is not None and line.startswith("  "):
            cur += " " + line.strip()
    if cur:
        out.append(cur)
    keep = []
    for b in out:
        if re.match(r"^- \[x\]", b):
            continue
        body = re.sub(r"^- (\[[ x]\] )?", "", b)
        if body.startswith("~~") and body.count("~~") >= 2 and body.rstrip().endswith("~~"):
            continue
        keep.append(b)
    return keep


print("registered ids in OPEN-QUESTIONS.md (first table cell): %d\n" % len(REG_IDS))
tot = {"ID-PRESENT": 0, "ID-ORPHAN": 0, "NO-ID": 0}
for p in PAGES:
    if not os.path.isfile(p):
        print("MISSING %s" % p)
        continue
    counts = {"ID-PRESENT": 0, "ID-ORPHAN": 0, "NO-ID": 0}
    orphans = set()
    for b in open_items(p):
        ids = [i for i in ID_RE.findall(b)]
        if not ids:
            counts["NO-ID"] += 1
        elif any(i in REG_IDS for i in ids):
            counts["ID-PRESENT"] += 1
        else:
            counts["ID-ORPHAN"] += 1
            orphans.update(ids)
    for k in counts:
        tot[k] += counts[k]
    print("%-70s present %d  orphan %d  no-id %d %s"
          % (os.path.basename(p), counts["ID-PRESENT"], counts["ID-ORPHAN"], counts["NO-ID"],
             ("  orphan ids: " + ",".join(sorted(orphans))) if orphans else ""))

print("\nTOTAL  ID-PRESENT %d   ID-ORPHAN %d   NO-ID %d" % (tot["ID-PRESENT"], tot["ID-ORPHAN"], tot["NO-ID"]))
print("\nCONTROL phyre-subsystem-map is ID-PRESENT-dominated and the two Glyph pages are NO-ID:"
      " check the rows above.")
