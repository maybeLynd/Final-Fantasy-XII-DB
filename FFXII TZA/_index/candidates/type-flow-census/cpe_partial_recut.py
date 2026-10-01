"""CPostEffect PARTIAL re-cut (OPUS, 2026-09-28). cpe_recut.py re-cuts a DISCOVERED span only when the census's reads
tile ALL of it; a span whose reads cover part of it stayed a 'mixed ... overlapping widths' row although the reads
settle every width they cover. This splits such a span into the fields its reads define plus DISCOVERED remainders for
the unread bytes. Nothing unread is typed.

A span qualifies when, in the committed flow census (cpe-flow-accesses.tsv, the shared-policy receipt):
  - its reads (width <= 8) do not overlap one another;
  - every other access that touches it is a 16-byte move or starts and ends on the new boundaries, and no access
    reaches outside the span;
  - each field's type comes from its reads (cpe_recut.ctype).
Usage:  python cpe_partial_recut.py            the check (C1 + S; exits 1 on a failed check)
        python cpe_partial_recut.py --patch    applies the re-cut to _types/fields.tsv (mixed EOLs, per line)
  C1 controls: overlapping reads (+0x730) and a crossing 4-byte write (+0xAFC, 00704A19 at +0xB00) are rejected;
     a fully tiled span is left to cpe_recut.py
  S  REGRESSION: every qualifying span is re-cut in the store (FAILS before the patch)
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
from cpe_recut import ctype
FIELDS = os.path.join(DB, "_types", "fields.tsv")
REC = "_index/candidates/type-flow-census/cpe_partial_recut.py"
rows = list(csv.DictReader(open(os.path.join(HERE, "cpe-flow-accesses.tsv"), encoding="utf-8"), delimiter="\t"))
ACC = [(int(r["field"], 16), int(r["width"]), r["kind"], r["instruction"], r["site"]) for r in rows
       if r["kind"] != "addr" and not r["field"].startswith("-")]


def plan(o, n):
    acc = [a for a in ACC if a[0] < o + n and a[0] + a[1] > o]
    rd = [a for a in acc if "r" in a[2] and a[1] <= 8 and o <= a[0] and a[0] + a[1] <= o + n]
    rl = sorted({(a[0], a[1]) for a in rd})
    if not rl: return None, "no reads"
    if any(x[0] < y[0] + y[1] and y[0] < x[0] + x[1] and x != y for x in rl for y in rl): return None, "overlapping reads"
    tiles = rl[0][0] == o and sum(w for _, w in rl) == n and all(rl[i][0] + rl[i][1] == rl[i + 1][0] for i in range(len(rl) - 1))
    if tiles: return None, "fully tiled (cpe_recut's case)"
    bounds = {f for f, _ in rl} | {f + w for f, w in rl} | {o, o + n}
    for a in acc:
        if a[1] == 16: continue
        if a[0] < o or a[0] + a[1] > o + n or a[0] not in bounds or a[0] + a[1] not in bounds:
            return None, "crossing access %s %d %s at %s" % (hex(a[0]), a[1], a[2], a[4])
    out, cur = [], o
    for f, w in rl:
        if f > cur: out.append(("gap", cur, f - cur, None, [], []))
        ts = sorted({ctype(a[3], w) for a in rd if (a[0], a[1]) == (f, w)})
        t = ts[0] if len(ts) == 1 else next((x for x in ts if x.startswith("int")), ts[0])
        if len(ts) > 1 and not all(x.lstrip("u") == t.lstrip("u") for x in ts): return None, "conflicting read types"
        sites = sorted({a[4] for a in rd if (a[0], a[1]) == (f, w)})
        wsites = sorted({a[4] for a in acc if "w" in a[2] and (a[0], a[1]) == (f, w)})
        out.append(("field", f, w, t, sites, wsites))
        cur = f + w
    if cur < o + n: out.append(("gap", cur, o + n - cur, None, [], []))
    return out, "ok"


lines = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
disc = [(int(cells(l)[1], 16), int(cells(l)[2]), i) for i, l in enumerate(lines)
        if cells(l)[0] == "CPostEffect" and cells(l)[6] == "DISCOVERED" and cells(l)[3].startswith("mixed")]
todo = [(o, n, i, plan(o, n)) for o, n, i in disc]
qual = [(o, n, i, p) for o, n, i, (p, why) in todo if p]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

if "--patch" in sys.argv:
    out = list(lines)
    for o, n, i, p in sorted(qual, key=lambda x: -x[2]):
        c = cells(lines[i]); eol = lines[i][len(lines[i].rstrip("\r\n")):]; width = len(c)
        new = []
        for kind, f, w, t, sites, wsites in p:
            if kind == "field":
                name = "field%X" % f
                mean = ("read as %s at %d site(s), e.g. %s%s. Width and type from the read side; what it holds is not claimed."
                        % (t, len(sites), ", ".join(sites[:2]), ("; written at " + ", ".join(wsites[:2])) if wsites else ""))
                r = ["CPostEffect", "0x%X" % f, str(w), name, t, mean, "TYPE RESOLVED", "PROVEN",
                     "CPOSTEFFECT PARTIAL RE-CUT 2026-09-28 (OPUS, %s): the flow census's reads cover part of the span and "
                     "no other access crosses the new boundaries. || WAS %s %s %s %s: %s" % (REC, c[1], c[2], c[3], c[4], c[5])]
            else:
                r = ["CPostEffect", "0x%X" % f, str(w), "unobservedSpan%X" % f, "u8[%d]" % w,
                     "the unread bytes of the former span %s; no read in the flow census" % c[3], "DISCOVERED", "UNKNOWN",
                     "CPOSTEFFECT PARTIAL RE-CUT REMAINDER 2026-09-28 (OPUS, %s)" % REC]
            new.append("\t".join(r + [""] * (width - len(r))) + eol)
        out[i:i + 1] = new
    open(FIELDS, "wb").write("".join(out).encode("utf-8"))
    print("re-cut %d spans" % len(qual)); sys.exit(0)

ctl = [plan(0x730, 4)[1], plan(0xAFC, 8)[1]]
check("C1", ctl[0] == "overlapping reads" and ctl[1].startswith("crossing access 0xb00 4 w at 00704A19"),
      "controls: +0x730 -> %s; +0xAFC -> %s" % tuple(ctl))
check("S", not qual, "qualifying spans still carried as 'mixed' rows: %d %s" % (len(qual), [hex(o) for o, n, i, p in qual][:8]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
