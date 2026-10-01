"""widget_header_more.py - OPUS (Claude Opus 5.5), 2026-09-28. Two more widget types get the shared header as one row.
widget_header.py H1a listed them unverified only because their records named the construction site in a form its parser does
not read; the sites themselves verify.

  S  HelpMessageWidget0500: 002BF60B `call 00245000` after `mov edx, 0x500` (002BF5FF) - whole object, in place;
     WidgetConsumer02AEE4C8: 0039457D `call 00244F50` after `mov ecx, 0x1d0` (0039456C) - whole object, heap
  P  each type's ctor cell names its site as '<constructor> at <site>' (the parseable form); the rows below +0xC0 become one
     row, widgetBase0000 Widget, and every replaced row's name / ctype is kept in its evidence
  W  REGRESSION (FAILS before): both types have exactly one row below +0xC0, widgetBase0000 Widget, and still tile
Usage: python widget_header_more.py [--patch]
"""
import hashlib, os, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
import struct
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    return all(A.get(a) == v for a, v in pairs)
check("S", has(0x2BF5FA, 0x2BF610, [(0x2BF5FF, ("mov", "edx, 0x500")), (0x2BF60B, ("call", "0x245000"))])
      and has(0x394562, 0x394582, [(0x39456C, ("mov", "ecx, 0x1d0")), (0x39457D, ("call", "0x244f50"))]),
      "002BF60B builds HelpMessageWidget0500 whole (0x500, in place); 0039457D builds WidgetConsumer02AEE4C8 whole (0x1D0, heap)")
REC = "_index/candidates/widget-header-embedding/widget_header_more.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
SITE = {"HelpMessageWidget0500": "00245000 at 002BF60B (`mov edx, 0x500` at 002BF5FF)", "WidgetConsumer02AEE4C8": "00244F50 at 0039457D (`mov ecx, 0x1d0` at 0039456C)"}
FI = DB / "_types/fields.tsv"; TY = DB / "_types/types.tsv"
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = FI.read_bytes().decode("utf-8").splitlines(keepends=True); out = []; done = set()
    old = {t: [cells(l) for l in fl if cells(l)[0] == t and int(cells(l)[1], 16) < 0xC0] for t in SITE}
    for t, rs in old.items(): assert sum(int(c[2]) for c in rs) == 0xC0, (t, sum(int(c[2]) for c in rs))
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in SITE and int(c[1], 16) < 0xC0:
            if c[0] not in done:
                was = "; ".join("+0x%X %s %s" % (int(x[1], 16), x[3], x[4]) for x in old[c[0]])
                w = len(c[1]) - 2
                out.append("\t".join([c[0], "0x" + "0" * w, "192", "widgetBase0000", "Widget", "the shared Widget header the constructor at %s writes on every widget" % SITE[c[0]],
                                      "TYPE RESOLVED", "PROVEN", "EMBEDDED 2026-09-28 (OPUS, %s S P). was the header rows %s. %s" % (REC, was, EXE)]) + e); done.add(c[0])
            continue
        out.append(l)
    FI.write_bytes("".join(out).encode("utf-8"))
    tl = TY.read_bytes().decode("utf-8").splitlines(keepends=True); to = []
    for l in tl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in SITE and SITE[c[0]].split(" (")[0] not in c[5]:
            c[5] = "built whole by " + SITE[c[0]] + " - " + c[5]; c[10] += " || HEADER EMBEDDED 2026-09-28 (OPUS, %s)" % REC
        to.append("\t".join(c) + e)
    TY.write_bytes("".join(to).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in FI.read_bytes().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in TY.read_bytes().decode("utf-8").splitlines()}
ok = True
for t in SITE:
    below = [c for c in F if c[0] == t and int(c[1], 16) < 0xC0]
    ok &= len(below) == 1 and below[0][3:5] == ["widgetBase0000", "Widget"] and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16) and SITE[t].split(" (")[0] in T[t][5]
check("W", ok, "both types: one row below +0xC0 (widgetBase0000 Widget), the site named in the ctor cell, tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
