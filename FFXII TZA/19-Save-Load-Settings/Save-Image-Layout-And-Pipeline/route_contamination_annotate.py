"""Annotate the save-payload page's offset table (section 2.3) for census rows removed by the 00307300 path cut.
Strikes each writer/reader citation whose site was removed, and marks every row whose offset lost census rows."""
import re, collections
PAGE = "Database/FFXII TZA/19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md"
DROP = "Database/FFXII TZA/19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/route-contamination-removed.tsv"
KEEP = "Database/FFXII TZA/19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-payload-accesses.tsv"
def rows(p):
    out = []
    for l in open(p, encoding="utf-8"):
        c = l.rstrip("\r\n").split("\t")
        if c[0] != "function": out.append(c)
    return out
dropped = rows(DROP); kept = rows(KEEP)
dsites = set(r[2] for r in dropped)
lost_by_off = collections.Counter(int(r[3], 16) for r in {(r[0], r[2], r[3]): r for r in dropped}.values())
kept_off = set(int(r[3], 16) for r in kept)
raw = open(PAGE, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.replace("\r\n", "\n").split("\n")
start = lines.index("### 2.3 The payload, offset by offset"); end = lines.index("### 2.4 What nobody reaches")
seg = re.compile(r"(?:`[A-Za-z_][A-Za-z0-9_]*` )?`([0-9A-F]{8})` \(`([0-9A-F]{8})`(?: \+\d+)?\)")
changed = 0; struck = 0
for i in range(start, end):
    l = lines[i]
    m = re.match(r"^\| `\+0x([0-9A-F]+)` \|", l)
    if not m: continue
    off = int(m.group(1), 16)
    if off not in lost_by_off: continue
    cells = l.split(" | ")
    def strike(mm):
        global struck
        if mm.group(2) in dsites:
            struck += 1
            return "~~" + mm.group(0) + "~~"
        return mm.group(0)
    # cells: [0]=| offset, [1]=width, [2]=name, [3]=w / r, [4]=writers, [5]=readers |
    for k in (4, 5):
        if k < len(cells): cells[k] = seg.sub(strike, cells[k])
    note = "%d census row(s) removed 2026-09-13 as route-contaminated (§8); counts not regenerated" % lost_by_off[off]
    if off not in kept_off: note += "; **no census access remains at this offset**"
    cells[2] = (cells[2] + " " if cells[2].strip() else "") + "*(" + note + ")*"
    lines[i] = " | ".join(cells); changed += 1
open(PAGE, "w", encoding="utf-8", newline="").write(nl.join(lines))
print("rows annotated", changed, "citations struck", struck, "offsets", len(lost_by_off), "left empty", sum(1 for o in lost_by_off if o not in kept_off))
