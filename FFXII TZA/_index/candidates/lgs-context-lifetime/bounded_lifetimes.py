"""bounded_lifetimes.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The other two types whose release
cell read 'none identified', given the bounded statement the image supports instead of silence.

  C1 Category's table cell 02EAD008: in every listed body, rip-relative accesses to it are ONE write (007AAAA2, in the
     builder 007AAA40, storing 007AD550(count * 8)) and reads (007AAA2C the getter 007AAA20; 007AAB50 / 007AAB6C / 007AABDD in
     the builder; 007AB000 in the per-frame update 007AAEA0). The builder reads no old table before overwriting the cell
     (its first access to the cell is that store) and has one direct caller, 007A50E7 in 007A4D50. So no listed code frees
     the table or its entries: they live for the process if the build runs once, and a second build would leak the first
     - whether it runs again is not established
  C2 PendingCompletionQueue01F81248's cell 01F81248: accesses are the lazy ensure 001BDA50 (a null test, then the one
     write 001BDA9A) and the getter 001BDAB0 - nothing nulls or frees the cell, and it is built at most once. A release
     through a pointer the getter returned is not excluded here
  S  REGRESSION: both types' dtor cells carry these bounded statements (FAILS before the patch)
Usage: python bounded_lifetimes.py [--patch]
"""
import hashlib, os, re, struct, sys, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
F = {}
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    c = l.split("\t")
    try: F[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
CELLS = {0x2EAD008: [], 0x1F81248: []}; calls = collections.defaultdict(list)
for f, s in F.items():
    o = off(f) if 0x121000 <= f < 0x900000 else None
    if o is None or s <= 0: continue
    for x in cs.disasm(d[o:o + s], f):
        m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
        if m:
            t = x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
            if t in CELLS:
                w = x.op_str.startswith("qword ptr [rip") and x.mnemonic == "mov"
                CELLS[t].append(("w" if w else "r", "%08X" % x.address, "%08X" % f))
        if x.mnemonic == "call" and x.op_str in ("0x7aaa40", "0x1bda50"):
            calls[x.op_str].append("%08X" % x.address)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
cat = sorted(CELLS[0x2EAD008]); pq = sorted(CELLS[0x1F81248])
cw = [a for k, a, f in cat if k == "w"]
first_in_builder = min(a for k, a, f in cat if f == "007AAA40")
check("C1", cw == ["007AAAA2"] and first_in_builder == "007AAAA2" and calls["0x7aaa40"] == ["007A50E7"]
      and {f for k, a, f in cat} == {"007AAA20", "007AAA40", "007AAEA0"},
      "02EAD008: writes %s; accesses %s; builder callers %s" % (cw, [(k, a) for k, a, f in cat], calls["0x7aaa40"]))
pw = [a for k, a, f in pq if k == "w"]
check("C2", pw == ["001BDA9A"] and {f for k, a, f in pq} == {"001BDA50", "001BDAB0"},
      "01F81248: writes %s; accesses %s" % (pw, [(k, a, f) for k, a, f in pq]))
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/lgs-context-lifetime/bounded_lifetimes.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
ADD = {"Category": " || BOUNDED 2026-09-28 (OPUS, %s C1): the table cell 02EAD008 has one writer in listed code, 007AAAA2 in the builder "
                   "007AAA40 (one direct caller, 007A50E7), which overwrites it without reading or releasing an earlier table; no "
                   "listed code frees the table or its entries. Process lifetime if the build runs once; a second build would leak "
                   "the first - whether it runs again is not established" % REC,
       "PendingCompletionQueue01F81248": " || BOUNDED 2026-09-28 (OPUS, %s C2): the cell 01F81248 is written once, by the lazy "
                   "ensure 001BDA50 after its null test (001BDA9A), and otherwise only read by the getter 001BDAB0 - nothing in "
                   "listed code nulls or frees it, so it is built at most once and lives for the process unless a getter caller "
                   "frees it (not excluded here)" % REC}
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in ADD and "BOUNDED 2026-09-28" not in c[6]:
            c[6] += ADD[c[0]]; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
check("S", all("BOUNDED 2026-09-28" in t[k][6] for k in ADD), "both dtor cells carry the bounded statement")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
