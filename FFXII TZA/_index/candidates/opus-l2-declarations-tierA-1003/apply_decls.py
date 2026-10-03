"""apply_decls.py [--apply] - declare the contract-cited statics in decls.json beside this file (OPUS, 2026-10-03;
drafted by repos-91, a local helper; every type and field row re-read at the bytes by a non-drafting verifier, whose
FIX rows are already folded in - see README.md). Appends the types rows to types.tsv and the field rows to fields.tsv,
each type's rows together in offset order.

Refuses when a type name is already declared with other rows, when a type's fields do not tile its size exactly, or
when either store carries an uncommitted line that is not this record's (lines named in $OPUS_APPLY_ALLOWED -
sibling records apply_l2_set.py applied earlier from a clean store - excepted). Idempotent (ALREADY). Prints FAILS n."""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TY = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types"))
D = json.load(io.open(os.path.join(HERE, "decls.json"), encoding="utf-8"))
TROWS, FROWS = D["types"], D["fields"]
NAMES = [t.split("\t")[0] for t in TROWS]
allowed = set()
if os.environ.get("OPUS_APPLY_ALLOWED"):
    allowed = set(io.open(os.environ["OPUS_APPLY_ALLOWED"], encoding="utf-8").read().splitlines())
fails = 0
for t in TROWS:
    n = t.split("\t")[0]
    # a VARIABLE-size type (e.g. WeaponRecipeBlob) has no fixed extent to tile against
    size = int(t.split("\t")[1], 16) if t.split("\t")[1].lower().startswith("0x") else None
    rows = sorted((int(r.split("\t")[1], 16), int(r.split("\t")[2])) for r in FROWS if r.split("\t")[0] == n)
    end = 0
    for o, s in rows:
        if o != end:
            print("TILING %s at +0x%X" % (n, o)); fails += 1
        end = o + s
    # '|' is allowed only in a types row's route column (13th) - the store's multi-instance form
    if (size is not None and end != size) or any("|" in r for r in FROWS) \
            or any("|" in c for t2 in TROWS for c in t2.split("\t")[:12]):
        print("TILING/PIPE %s" % n); fails += 1
stores = {}
for fn, mine in (("types.tsv", TROWS), ("fields.tsv", FROWS)):
    p = os.path.join(TY, fn)
    b = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in b else "\n"
    lines = b.rstrip("\r\n").split(nl)
    stores[fn] = (p, nl, lines, mine)
    d = subprocess.run(["git", "-C", TY, "diff", "--", fn], capture_output=True, text=True, encoding="utf-8").stdout
    ms = set(mine)
    foreign = [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))
               and l[1:] not in ms and l[1:] not in allowed]
    if foreign:
        print("REFUSED: %s has %d uncommitted lines that are not this record's" % (fn, len(foreign))); fails += 1
    other = [l for l in lines if l.split("\t", 1)[0] in NAMES and l not in ms]
    if other:
        print("REFUSED: %s already has %d other rows for these type names" % (fn, len(other))); fails += 1
if not fails and all(all(m in st[2] for m in st[3]) for st in stores.values()):
    print("ALREADY (%d types, %d field rows)" % (len(TROWS), len(FROWS)))
    print("FAILS 0")
    sys.exit(0)
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
for fn, (p, nl, lines, mine) in stores.items():
    lines = [l for l in lines if l not in set(mine)] + list(mine)
    tmp = p + ".opus-tmp"
    io.open(tmp, "w", encoding="utf-8", newline="").write(nl.join(lines) + nl)
    os.replace(tmp, p)
print("APPLIED: %d types, %d field rows" % (len(TROWS), len(FROWS)))
print("FAILS 0")
