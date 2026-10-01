"""lifetime_propagation.py - OPUS (Claude Opus 5.5), 2026-09-28. A consistency check between release cells, no image read.

An embedded type (route EMBED <owner> ...) has no release of its own; its lifetime is its owner's. When the owner's release
cell is later ESTABLISHED, a child cell that still says 'the owner's destructor is unestablished' is stale.
  P1 REGRESSION: no EMBED type's release cell says its owner's destructor is unestablished while the owner's release cell
     does not itself read 'not established' / 'unestablished' (FAILS before the patch: BootSubBlock0338, whose owner
     BootSingleton01F7F598 is an established 'NONE - the object is never released', single install-only writer 00189067)
Usage: python lifetime_propagation.py [--patch]
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TY = sys.argv[sys.argv.index("--types") + 1] if "--types" in sys.argv else os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/lgs-context-lifetime/lifetime_propagation.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
T = {cells(l)[0]: cells(l) for l in tl[1:]}
STALE = re.compile(r"(?<!~~)the owner's destructor is itself unestablished", re.I)
OPEN = re.compile(r"^\W*(not established|unestablished)", re.I)   # the cell's LEADING status, not words in its history
def stale():
    out = []
    for k, c in T.items():
        m = re.search(r"EMBED (\S+)", c[12] if len(c) > 12 else "")
        if not m or not STALE.search(re.sub(r"~~.*?~~", "", c[6])): continue
        own = T.get(m.group(1))
        if own and not OPEN.search(own[6]): out.append((k, m.group(1)))
    return out
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "BootSubBlock0338" and "~~the owner's destructor is itself unestablished~~" not in c[6]:
            c[6] = c[6].replace("the owner's destructor is itself unestablished",
                                "~~the owner's destructor is itself unestablished~~ the owner is never released - BootSingleton01F7F598's "
                                "release cell is an established NONE (its cell 01F7F598 has one install-only writer, 00189067), so these "
                                "three elements live for the process (propagated 2026-09-28, OPUS, %s)" % REC, 1)
            tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
s = stale()
print("%s  P1 embedded release cells that still call an established owner's release unestablished: %s" % ("PASS" if not s else "FAIL", s))
sys.exit(1 if s else 0)
