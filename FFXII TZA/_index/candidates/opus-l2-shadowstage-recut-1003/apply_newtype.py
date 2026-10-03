"""apply_newtype.py [--apply] - declare ShadowConstantsStage02CB8160 (0x2C0), the undeclared stretch between
CharacterLightingTuningBank (ends 02CB8160) and SssLightingParams02CB8420 (OPUS, 2026-10-03; measured by repos-91, a
local helper; all 208 cited code addresses checked as instruction starts by OPUS). Takes the types row and 30 field
rows from research.json "new_type"; inserts both immediately before SssLightingParams02CB8420 in each store.

Refuses when the type already has other rows, when a field overlaps another or runs past 0x2C0, or when either store
carries an uncommitted line that is not this record's (lines named in the file at $OPUS_APPLY_ALLOWED - sibling records
apply_l2_set.py applied earlier from a clean store - excepted). Idempotent (ALREADY). Prints FAILS n."""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TY = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types"))
NAME, SIZE, NEXT = "ShadowConstantsStage02CB8160", 0x2C0, "SssLightingParams02CB8420\t"
nt = json.load(io.open(os.path.join(HERE, "research.json"), encoding="utf-8"))["new_type"]
trow = nt["types_row"].replace("PROPOSED 2026-10-03 (OPUS L2 survey).",
                               "DECLARED 2026-10-03 (OPUS L2 survey; measured by repos-91, re-read by OPUS; record "
                               "_index/candidates/opus-l2-shadowstage-recut-1003).")
frows = sorted(nt["fields"], key=lambda l: int(l.split("\t")[1], 16))
allowed = set()
if os.environ.get("OPUS_APPLY_ALLOWED"):
    allowed = set(io.open(os.environ["OPUS_APPLY_ALLOWED"], encoding="utf-8").read().splitlines())
fails = 0
end = 0
for f in frows:
    c = f.split("\t")
    o, s = int(c[1], 16), int(c[2])
    if c[0] != NAME or len(c) != 9 or o < end or o + s > SIZE:
        print("BAD FIELD ROW: " + f[:120].replace("\t", " | "))
        fails += 1
    end = max(end, o + s)
stores = {}
for fn, mine in (("types.tsv", [trow]), ("fields.tsv", frows)):
    p = os.path.join(TY, fn)
    b = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in b else "\n"
    lines = b.rstrip("\r\n").split(nl)
    stores[fn] = (p, nl, lines, mine)
    d = subprocess.run(["git", "-C", TY, "diff", "--", fn], capture_output=True, text=True, encoding="utf-8").stdout
    foreign = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))
               and l[1:] not in set(mine) and l[1:] not in allowed]
    if foreign:
        print("REFUSED: %s has %d uncommitted lines that are not this record's" % (fn, len(foreign)))
        fails += 1
present = [all(m in st[2] for m in st[3]) for st in stores.values()]
if all(present) and not fails:
    print("ALREADY (%s declared, %d field rows)" % (NAME, len(frows)))
    print("FAILS 0")
    sys.exit(0)
for fn, (p, nl, lines, mine) in stores.items():
    other = [l for l in lines if l.startswith(NAME + "\t") and l not in mine]
    if other:
        print("REFUSED: %s already has %d other %s rows" % (fn, len(other), NAME))
        fails += 1
    if not any(l.startswith(NEXT) for l in lines):
        print("REFUSED: %s has no %s row to insert before" % (fn, NEXT.strip()))
        fails += 1
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
for fn, (p, nl, lines, mine) in stores.items():
    lines = [l for l in lines if l not in mine]
    i = next(k for k, l in enumerate(lines) if l.startswith(NEXT))
    lines[i:i] = mine
    tmp = p + ".opus-tmp"
    io.open(tmp, "w", encoding="utf-8", newline="").write(nl.join(lines) + nl)
    os.replace(tmp, p)
print("APPLIED: %s declared (types 1 row, fields %d rows)" % (NAME, len(frows)))
print("FAILS 0")
