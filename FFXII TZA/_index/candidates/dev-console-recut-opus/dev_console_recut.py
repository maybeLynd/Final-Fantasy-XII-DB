"""dev_console_recut.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
DeveloperConsoleSettings01F81428's twenty 'unnamed stretch' rows (spanXXXX u8[N], DISCOVERED) cut into fields from a receiver
census seeded at the getter 001D50D0 and the constructor 001CCB20, keeping only instructions whose displacement IS the field.

  C  the census: SEED=call 001D50D0 and SEED=ctor 001CCB20 (census_receiver_fixpoint.py, extent 0x10E8), literal-displacement
     accesses only, enumerated (loop over-reach) sites excluded. Control: it reaches the type's already-declared rows
  R  THE CUT, derived here and not hand-kept: inside each span, a field starts at every accessed offset; its width is the
     narrowest access there, capped at the next accessed offset and the span end - so a wider store across two fields (the
     constructor's qword zeroing of dword pairs) is a packed store, not a field; the bytes between fields are declared gaps.
     A field read anywhere is typed from its reads (float for ss-class instructions, signed for movsx / movsxd) and PROVEN;
     a field only written is typed from the write and PROBABLE
  W  REGRESSION (FAILS before): no spanXXXX u8[N] stretch row is left; the rows tile the type
Not claimed: what any field holds.
Usage: python dev_console_recut.py [--patch]
"""
import collections, hashlib, json, os, subprocess, sys, tempfile
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = "DeveloperConsoleSettings01F81428"; EXT = 0x10E8
TOOL = os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "census_receiver_fixpoint.py")
acc = collections.defaultdict(lambda: collections.defaultdict(lambda: {"r": set(), "w": set(), "ins": set()}))
for kind, addr in (("call", "0x1D50D0"), ("ctor", "0x1CCB20")):
    tf = tempfile.NamedTemporaryFile(suffix=".json", delete=False); tf.close()
    subprocess.run([sys.executable, TOOL, addr, "0", hex(EXT)], env=dict(os.environ, SEED=kind, CAP="4000", EMIT_JSON=tf.name), capture_output=True, cwd=ROOT)
    j = json.load(open(tf.name)); os.unlink(tf.name); enum = set(j.get("enumerated_sites", []))
    for k, v in j["sites"].items():
        o, w = map(int, k.split(":"))
        if k in enum: continue
        for s, (rd, wr) in v.items():
            a = int(s, 16); x = next(cs.disasm(d[off(a):off(a) + 16], a, 1))
            if ("0x%x]" % o) not in x.op_str: continue
            e = acc[o][w]
            if rd: e["r"].add(s)
            if wr: e["w"].add(s)
            e["ins"].add(x.mnemonic)
FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
declared = [int(c[1], 16) for c in F if c[0] == T and c[6] != "DISCOVERED" and not c[3].startswith(("span", "unobserved"))]
check("C", len(acc) > 100 and sum(1 for o in declared if o in acc) >= 20, "%d accessed offsets; %d of the type's %d declared rows reached" % (len(acc), sum(1 for o in declared if o in acc), len(declared)))
SPANS = [(int(c[1], 16), int(c[2]), c) for c in F if c[0] == T and c[3].startswith("span") and c[4].startswith("u8[")]
def ctype(ins, w):
    if any(m.endswith("ss") or m in ("comiss", "ucomiss") or m.startswith("cvtss") for m in ins): return "float"
    if "movsxd" in ins: return "int32"
    if "movsx" in ins: return {1: "int8", 2: "int16"}.get(w, "int%d" % (8 * w))
    return {1: "uint8", 2: "uint16", 4: "uint32", 8: "uint64"}[w]
def cut(s0, n):
    offs = sorted(o for o in acc if s0 <= o < s0 + n); out = []; pos = s0
    for i, o in enumerate(offs):
        nxt = offs[i + 1] if i + 1 < len(offs) else s0 + n
        w = min(acc[o]); w = min(w, nxt - o, s0 + n - o)
        while w not in (1, 2, 4, 8): w //= 2
        if o > pos: out.append(("gap", pos, o - pos, None))
        out.append(("field", o, w, acc[o])); pos = o + w
    if pos < s0 + n: out.append(("gap", pos, s0 + n - pos, None))
    return out
REC = "_index/candidates/dev-console-recut-opus/dev_console_recut.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def rows_for(s0, n, c):
    out = []; was = "%s %s (%s)" % (c[3], c[4], c[5][:120])
    for kind, o, w, a in cut(s0, n):
        ev = "CARVED 2026-09-28 (OPUS, %s C R). was %s. %s" % (REC, was, EXE)
        if kind == "gap":
            out.append([T, "0x%04X" % o, str(w), "unobservedSpan%04X" % o, "u8[%d]" % w, "declared gap inside the old stretch: no literal access by the getter or constructor census", "DISCOVERED", "UNKNOWN", ev]); continue
        own = [v for ww, v in a.items() if ww == w]                     # accesses of the field's own width
        reads = sorted(set().union(set(), *(v["r"] for v in own))); writes = sorted(set().union(set(), *(v["w"] for v in own)))
        ins = set().union(set(), *(v["ins"] for v in own))
        wider = sorted(ww for ww in a if ww > w)
        if not own:                                                      # only a wider access starts here: type from it, packed
            ins = set().union(*(v["ins"] for v in a.values())); writes = sorted(set().union(*(v["w"] for v in a.values())))
        ct = ctype(ins, w)
        nm = {"float": "float", "int8": "byte", "uint8": "byte", "int16": "word", "uint16": "word", "int32": "dword", "uint32": "dword", "uint64": "qword"}[ct] + "%04X" % o
        pk = " A wider %s-byte access here spans the next field (a packed store or copy, not the field)." % "/".join(str(x) for x in wider) if wider else ""
        if not own:
            m = ("reached only by a wider %s access starting here (%s) that spans the next field - a packed store or copy; the width is "
                 "the distance to that field; what it holds is not claimed." % ("/".join(str(x) for x in wider), ", ".join(sorted(set().union(*(v["r"] | v["w"] for v in a.values())))[:3])))
            rd = ("TYPE RESOLVED", "PROBABLE")
        elif reads:
            m = "read as %s at %d site(s), e.g. %s; written at %d. Width and type from the read side; what it holds is not claimed.%s" % (ct, len(reads), ", ".join(reads[:3]), len(writes), pk)
            rd = ("TYPE RESOLVED", "PROVEN")
        else:
            m = "written only (%d site(s), e.g. %s); width and type from the write; what it holds is not claimed.%s" % (len(writes), ", ".join(writes[:3]), pk)
            rd = ("TYPE RESOLVED", "PROBABLE")
        out.append([T, "0x%04X" % o, str(w), nm, ct, m, rd[0], rd[1], ev])
    return out
NEW = {s0: rows_for(s0, n, c) for s0, n, c in SPANS}
tile_ok = all(sum(int(r[2]) for r in NEW[s0]) == n for s0, n, c in SPANS)
check("R", tile_ok and all(r[3].startswith(("unobservedSpan", "byte", "word", "dword", "qword", "float")) for rs in NEW.values() for r in rs),
      "%d stretch rows -> %d rows (%d fields, %d gaps); each cut tiles its span" % (len(SPANS), sum(len(v) for v in NEW.values()),
      sum(1 for v in NEW.values() for r in v if not r[3].startswith("unobserved")), sum(1 for v in NEW.values() for r in v if r[3].startswith("unobserved"))))
if "--patch" in sys.argv:
    assert tile_ok and SPANS
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == T and c[3].startswith("span") and c[4].startswith("u8[") and int(c[1], 16) in NEW:
            out += ["\t".join(x) + e for x in NEW[int(c[1], 16)]]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
R = sorted((int(c[1], 16), int(c[2])) for c in F if c[0] == T)
check("W", not SPANS and all(a[0] + a[1] == b[0] for a, b in zip(R, R[1:])), "no stretch row left; the type's rows tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
