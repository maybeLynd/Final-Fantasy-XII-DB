"""absence_recut.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
CORRECTION of 'no access at these displacements' rows (OPUS, 2026-09-20 .. 09-22) on 16 widget types. Those rows were
written from a census that did not yet walk the control flow (FRONTIER 57f9d58ab). A handler-seeded census
(census_receiver_fixpoint.py SEED=ctor on each type's own handler, CFG walk, loop-enumerated sites excluded) reaches
displacements inside them. The hits are frozen in census-hits.json, with the instruction text of every site.

  C  every frozen site still decodes to the recorded instruction in the certified image (the receipt is live, not quoted);
     --census re-runs the census and compares
  R  RE-CUT RULE, per contradicted row: each accessed offset becomes a field as wide as its widest access, clipped at the
     next accessed offset; a run of 16-byte SSE copies becomes one block row; untouched bytes stay a span, now worded
     'not reached by the handler-seeded census'; ctype from the access - uint8 / uint16 (int16 when read with movsx) /
     uint32 (float when read or written with SSE scalar ops) / uint64 / u8[16] block. Names give width and offset only;
     no meaning is claimed beyond the cited accesses
  N  PaneListWidget0B68 +0x180: the hits are 002465F0 / 002475D0 / 00247930 writing base + 0x40 / 0x44 / 0x48 / 0x7C /
     0x98 / 0x9C / 0xA0..0xAD / 0xB4 / 0xB8 for base = +0x180 - the Widget header's initialisation signature, and
     0029698B hands this + 0x180 to 002475D0 - so +0x180..+0x23F is a nested Widget (its row qword0180 is its handler slot)
  W  REGRESSION (FAILS before): no row named 'unobserved*' covers a frozen hit on these types, and every type still tiles
Usage: python absence_recut.py [--patch] [--census]
"""
import hashlib, json, os, re, subprocess, sys, tempfile
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
def ins(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
H = json.load(open(os.path.join(HERE, "census-hits.json"), encoding="utf-8"))
bad = [(t, a) for t, v in H.items() for k, sites in v["hits"].items() for a, (r, w, txt) in sites.items() if ins(int(a, 16)) != txt]
check("C", not bad and len(H) == 16, "%d frozen sites on %d types decode as recorded%s" % (sum(len(s) for v in H.values() for s in v["hits"].values()), len(H), (": " + str(bad[:3])) if bad else ""))
if "--census" in sys.argv:
    K = os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "census_receiver_fixpoint.py"); miss = []
    for t, v in H.items():
        got = set()
        for h in v["handlers"]:
            tf = tempfile.NamedTemporaryFile(suffix=".json", delete=False); tf.close()
            size = next(int(l.split("\t")[1], 16) for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8") if l.split("\t")[0] == t)
            subprocess.run([sys.executable, K, h, "0", hex(size)], env=dict(os.environ, SEED="ctor", CAP="600", EMIT_JSON=tf.name), capture_output=True, cwd=os.path.dirname(DB))
            j = json.load(open(tf.name)); os.unlink(tf.name); got |= {k.upper() for k in j["sites"]}
        miss += [(t, k) for k in v["hits"] if ("%X:%s" % (int(k.split(":")[0], 16), k.split(":")[1])).upper() not in {("%X:%s" % (int(g.split(":")[0]), g.split(":")[1])).upper() for g in got}]
    check("C2", not miss, "the live census reproduces every frozen hit%s" % ((": " + str(miss[:3])) if miss else ""))
PL_NEST = [0x40, 0x44, 0x48, 0x7C, 0x98, 0x9C, 0xA0, 0xA1, 0xAC, 0xAD, 0xB4, 0xB8]
plh = {int(k.split(":")[0], 16) for k in H["PaneListWidget0B68"]["hits"]}
check("N", all(0x180 + o in plh for o in PL_NEST) and ins(0x29698B) == "lea rcx, [rbx + 0x180]" and ins(0x296994) == "call 0x2475d0",
      "PaneListWidget0B68: the Widget initialisation signature lands at base +0x180, and 0029698B hands this + 0x180 to 002475D0")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/absence-recut-opus/absence_recut.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
SSE_F = re.compile(r"^(movss|addss|subss|mulss|divss|comiss|ucomiss|cvtss2sd|minss|maxss)\b")
def ctype_for(w, txts):
    if w == 16: return "u8[16]"
    if w == 4 and any(SSE_F.match(t) for t in txts): return "float"
    if w == 2 and any(t.startswith("movsx") for t in txts): return "int16"
    return {1: "uint8", 2: "uint16", 4: "uint32", 8: "uint64"}.get(w, "u8[%d]" % w)
def recut(t, row, hits, handlers):
    s, n = int(row[1], 16), int(row[2]); was = "%s %s (%s)" % (row[3], row[4], row[5][:140])
    ev = "RE-CUT 2026-09-28 (OPUS, %s R): the handler-seeded census (%s, CFG walk) reaches this row. was %s. %s" % (REC, " / ".join(handlers), was, EXE)
    acc = {}
    for k, sites in hits.items():
        o, w = int(k.split(":")[0], 16), int(k.split(":")[1])
        if s <= o < s + n: acc.setdefault(o, []).append((w, sites))
    starts = sorted(acc); out = []; cur = s; i = 0; W = 4 if len(row[1]) <= 6 else 5
    fmt = lambda o: ("0x%0" + str(W - 2) + "X") % o if False else row[1][:2] + ("%0" + str(len(row[1]) - 2) + "X") % o
    def gap(a, b):
        if b > a: out.append([t, fmt(a), str(b - a), "unobservedSpan%04X" % a, "u8[%d]" % (b - a), "not reached by the handler-seeded census (%s, CFG walk)" % " / ".join(handlers), "DISCOVERED", "PROBABLE", ev])
    while i < len(starts):
        o = starts[i]; ws = [w for w, _ in acc[o]]; w = max(ws)
        txts = [v[2] for _, sites in acc[o] for v in sites.values()]
        if w == 16:   # merge a run of contiguous 16-byte SSE copies into one block
            j = i; e = o + 16; srcs = list(txts)
            while j + 1 < len(starts) and starts[j + 1] == e and max(ww for ww, _ in acc[starts[j + 1]]) == 16:
                j += 1; e += 16; srcs += [v[2] for _, st in acc[starts[j]] for v in st.values()]
            gap(cur, o); nb = e - o
            sites = sorted({a for q in range(i, j + 1) for _, st in acc[starts[q]] for a in st})
            out.append([t, fmt(o), str(nb), "block%04X" % o, "u8[%d]" % nb, "copied in 16-byte SSE moves (%d access(es): %s); what it holds is not claimed" % (len(sites), ", ".join(sites[:4])), "TYPE RESOLVED", "PROVEN", ev])
            cur = e; i = j + 1; continue
        nxt = starts[i + 1] if i + 1 < len(starts) else s + n
        w = min(w, nxt - o, s + n - o); gap(cur, o)
        sites = {a: v for _, st in acc[o] for a, v in st.items()}
        r = sum(1 for v in sites.values() if v[0]); wr = sum(1 for v in sites.values() if v[1])
        clipped = "" if w == max(ws) else " (also accessed %d bytes wide, clipped at the next accessed offset)" % max(ws)
        ex = "; ".join("%s `%s`" % (a, v[2]) for a, v in list(sorted(sites.items()))[:2])
        nm = {1: "byte", 2: "word", 4: "dword", 8: "qword"}.get(w, "bytes") + "%04X" % o
        out.append([t, fmt(o), str(w), nm, ctype_for(w, txts), "reached by the handler path: %d access(es), %d read, %d written, widest %d%s; e.g. %s. What it holds is not claimed" % (len(sites), r, wr, max(ws), clipped, ex), "TYPE RESOLVED", "PROVEN", ev])
        cur = o + w; i += 1
    gap(cur, s + n)
    return out
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in H and REC not in c[8] and len(c) > 7:
            o, n = int(c[1], 16), int(c[2]) if c[2].isdigit() else 0
            if c[0] == "PaneListWidget0B68" and o in (0x180, 0x188):
                if o == 0x180:
                    out.append("\t".join([c[0], c[1], "192", "nestedWidget180", "Widget", "a widget header at +0x180: the initialisation signature of 002465F0 / 002475D0 / 00247930 lands at base + 0x180, and 0029698B hands this + 0x180 to 002475D0; its old handler-slot row qword0180 is its +0x00", "TYPE RESOLVED", "PROVEN",
                                          "RE-CUT 2026-09-28 (OPUS, %s N). was qword0180 void* and unobservedSpan0188 u8[184]. %s" % (REC, EXE)]) + e)
                continue
            hits = H[c[0]]["hits"]
            if re.search(r"no access at (these|this) displacement", c[5]) and any(o <= int(k.split(":")[0], 16) < o + n for k in hits):
                out += ["\t".join(x) + e for x in recut(c[0], c, hits, H[c[0]]["handlers"])]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
over = []
for t, v in H.items():
    rows = [c for c in F if c[0] == t]
    for k in v["hits"]:
        o = int(k.split(":")[0], 16)
        r = next((c for c in rows if int(c[1], 16) <= o < int(c[1], 16) + int(c[2])), None)
        if r is None or r[3].startswith("unobserved"): over.append((t, hex(o), r[3] if r else None))
tiles = [t for t in H if sum(int(c[2]) for c in F if c[0] == t) != int(T[t][1], 16)]
check("W", not over and not tiles, "no unobserved row covers a frozen hit%s; all 16 types tile%s" % ((": " + str(over[:4])) if over else "", (": " + str(tiles)) if tiles else ""))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
