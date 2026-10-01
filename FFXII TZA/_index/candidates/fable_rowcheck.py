# rowcheck.py : check every verdict row's GAP TEXT against what its contracts actually contain.
#
# Twice today a row understated its system because the gap sentence outran the evidence: S-01's said
# "static" after EXP-142 executed it, and S-34's says "nothing executed" when its contract's own
# section 13 was rewritten on 2026-09-12 to correct exactly that phrase. This looks for more of the
# same, mechanically, on two tests a human reading the row cannot do quickly:
#
#   EXEC   the row's gap says nothing/none executed, but a contract it names says otherwise
#          (an execution instrument, a differential, or an EXP-### citation in its section 13).
#   PAGES  the row's gap counts pages, but the mechanisms of the "uncovered" pages are already
#          entries of SOME contract - the page-coverage artefact, measured rather than assumed.
#
# It reports CANDIDATES, not findings: every hit has to be read before it is filed. The point is to
# put the twenty-odd rows in an order, not to score anything.
import io
import os
import re
import sys

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
os.chdir(ROOT)

VERD = io.open("_index/L2-VERDICTS.md", encoding="utf-8", errors="replace").read()
TSV = io.open("_index/important-subsystems.tsv", encoding="utf-8", errors="replace").read()

# --- the registry: system -> (pages, contracts) ---------------------------------------------------
reg = {}
for line in TSV.split("\n"):
    f = line.split("\t")
    if len(f) < 6 or not f[0].startswith("S-"):
        continue
    pages = [p.strip() for p in f[4].split(";") if p.strip()]
    contracts = [c.strip() for c in f[5].split(";") if c.strip()]
    reg[f[0]] = (pages, contracts)


def resolve(p):
    q = os.path.normpath(os.path.join("_index", p))
    return q if os.path.isfile(q) else None


def read(p):
    q = resolve(p)
    return io.open(q, encoding="utf-8", errors="replace").read() if q else ""


def entries_of(text):
    m = re.search(r"^entries:\s*\[(.*?)\]", text, re.M | re.S)
    if not m:
        return set()
    return {x.strip().strip('"\'').upper() for x in m.group(1).split(",") if x.strip()}


def addrs(text):
    a = {x.upper() for x in re.findall(r"(?<![0-9A-Za-z_])([0-9A-Fa-f]{8})(?![0-9A-Za-z_])", text)}
    return {x for x in a if 0x121000 <= int(x, 16) < 0x8C2000}


# every contract in the tree, so PAGES can ask "contracted ANYWHERE", not just by this row
ALL_ENTRIES = {}
for dirpath, _, files in os.walk("."):
    if ".git" in dirpath:
        continue
    for fn in files:
        if fn.startswith("CONTRACT-") and fn.endswith(".md"):
            p = os.path.join(dirpath, fn)
            ALL_ENTRIES[p] = entries_of(io.open(p, encoding="utf-8", errors="replace").read())
ALL = set().union(*ALL_ENTRIES.values()) if ALL_ENTRIES else set()

EXEC_HINT = re.compile(r"EXP-\d{3}|diff_[a-z_]+\.py|differential|executed (?:as shipped|against the shipped)"
                       r"|isolated original-code|NATIVE-REPLAY", re.I)
GAP_NONE = re.compile(r"nothing (?:is )?executed|no(?:thing)? live|has no execution|are all static"
                      r"|unexecuted|not executed|no runtime", re.I)
GAP_PAGES = re.compile(r"\b(\d+) of (\d+) pages|uncontracted|page coverage", re.I)

rows = []
for line in VERD.split("\n"):
    m = re.match(r"\|\s*\*\*(S-\d+)\*\*([^|]*)\|(.*)", line)
    if not m:
        continue
    cells = [c.strip() for c in m.group(3).split("|")]
    if len(cells) < 7:
        continue
    rows.append((m.group(1), m.group(2).strip(), cells[0], cells[6]))

print("rows checked: %d   contracts scanned: %d   distinct contract entries: %d\n"
      % (len(rows), len(ALL_ENTRIES), len(ALL)))

for sid, name, contract_cell, gap in rows:
    pages, contracts = reg.get(sid, ([], []))
    flags = []
    if GAP_NONE.search(gap):
        for c in contracts:
            t = read(c)
            sec13 = t.split("## 13.")[-1].split("## 14.")[0] if "## 13." in t else ""
            if sec13 and EXEC_HINT.search(sec13):
                hint = EXEC_HINT.search(sec13).group(0)
                flags.append("EXEC: %s section 13 cites %r" % (os.path.basename(c), hint))
    if GAP_PAGES.search(gap) and pages:
        own = set().union(*[entries_of(read(c)) for c in contracts]) if contracts else set()
        for p in pages:
            pa = addrs(read(p))
            if not pa:
                continue
            uncovered_here = pa - own
            covered_elsewhere = uncovered_here & ALL
            if own and not (pa & own) and covered_elsewhere:
                flags.append("PAGES: %s has 0 entries in this row's contracts but %d of its addresses "
                             "are entries elsewhere" % (os.path.basename(p), len(covered_elsewhere)))
    if flags:
        print("%-6s %-38s gap: %s" % (sid, name[:38], gap[:90]))
        for f in flags:
            print("        %s" % f)
        print()
