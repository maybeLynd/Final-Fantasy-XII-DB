"""UQ-2 caller route (OPUS, 2026-09-27). Control.

Seeds: sites-BattleUnit.tsv beside this file, written by type-flow-census/type_flow_census.py with
  POOL=0208E688 GETTERS=00236820,00263E30,0031B760,002367A0,0031B770,0031B7E0,0031B860,00321170,003272A0 TYPE_SIZE=0xF50
  SITES_OUT=sites-BattleUnit.tsv
Rule: position 1 of f is T* when f is not address-taken (outside .pdata) and
EVERY direct call / tail-jump site of f passes T+0 in rcx on a record that holds either in the empty-entry context
(a getter / pool / cell in the caller itself) or in a context where the caller's own rcx was T+0 and the caller is
itself typed T by the same rule (fixpoint)."""
import struct, re, glob, os, collections, bisect
DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
S = os.path.dirname(os.path.abspath(__file__))
d = open(DB + r"\Tools\work\exe\FFXII_TZA.exe", "rb").read(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    SECS.append((d[o:o + 8].rstrip(bytes(1)), ) + struct.unpack_from("<IIII", d, o + 8) + (struct.unpack_from("<I", d, o + 36)[0],))
pd = [(ro, ro + rs) for nm, vs, va, rs, ro, ch in SECS if nm == b".pdata"]
sizes = {}
for l in open(DB + r"\Tools\work\graph\functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
keys = sorted(sizes)
def owner(a):
    k = keys[bisect.bisect_right(keys, a) - 1]; return k if a < k + sizes[k] else None
ABI = DB + r"\FFXII TZA\00-Engine-Core-Runtime\ABI-Recovery"
rows = [l.rstrip("\r\n").split("\t") for l in open(ABI + r"\derived-call-signatures.tsv", encoding="utf-8") if l[:1].isalnum() and not l.startswith("addr")]
typed0 = set()
for fn in ("derived-signatures-this-types.tsv", "derived-signatures-ctor-types.tsv"):
    for l in open(ABI + "\\" + fn, encoding="utf-8"):
        if l[:1].isalnum() and not l.startswith("addr"): typed0.add(l.split("\t")[0])
untyped = [r for r in rows if r[0] not in typed0]
rec = collections.defaultdict(set)   # (site, callee) -> {(T, arg, k, ctx)}
for p in glob.glob(os.path.join(S, "sites-*.tsv")):
    T = os.path.basename(p)[6:-4]
    for l in open(p):
        c = l.rstrip("\n").split("\t")
        if len(c) < 5: continue
        rec[(int(c[0], 16), int(c[1], 16))].add((T, int(c[2]), int(c[3]), c[4]))
callees = {t for (a, t) in rec}
# direct sites of every callee of interest
sites = collections.defaultdict(list)
for nm, vs, va, rs, ro, ch in SECS:
    if not ch & 0x20000000: continue
    lo = BASE + va
    for i in range(ro, ro + rs - 5):
        if d[i] in (0xE8, 0xE9):
            t = lo + (i - ro) + 5 + struct.unpack_from("<i", d, i + 1)[0]
            if t in callees: sites[t].append(lo + (i - ro))
def taken(t):
    c = 0
    for pat in (struct.pack("<Q", t), struct.pack("<I", t - BASE)):
        c += sum(1 for m in re.finditer(re.escape(pat), d) if not any(a <= m.start() < b for a, b in pd))
    return c
tk = {t: taken(t) for t in callees}
typed = {}   # f -> T
changed = True
while changed:
    changed = False
    for f in callees:
        if f in typed or tk[f] or not sites[f]: continue
        cand = None; ok = True
        for a in sites[f]:
            good = set()
            for (T, arg, k, ctx) in rec.get((a, f), ()):
                if arg != 0 or k != 0: continue
                if ctx == "": good.add(T)
                elif ctx == "rcx=0" and typed.get(owner(a)) == T: good.add(T)
            if len(good) != 1: ok = False; break
            g = next(iter(good))
            if cand is None: cand = g
            elif cand != g: ok = False; break
        if ok and cand: typed[f] = cand; changed = True
hits = [(r[0], typed[int(r[0], 16)], r[1], r[2]) for r in untyped if int(r[0], 16) in typed and "rcx" in r[2]]
print("functions typed by callers (fixpoint):", len(typed), "; of them untyped signature rows:", len(hits))
for h in hits: print("  %s position1 = %s*  (arity %s, regs %s)" % h)
nt = sum(1 for r in untyped if sites.get(int(r[0], 16)) is not None)
print("untyped rows among the seeded callees that are not address-taken (outside .pdata):", sum(1 for r in untyped if int(r[0], 16) in tk and not tk[int(r[0], 16)]))

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
got = sorted(h[0] for h in hits)
check("C1 four untyped signature rows take BattleUnit* in position 1", got == ["002FFEF0", "00306B10", "0030B8E0", "0030DA30"], str(got))
s306 = sites.get(0x306B10, [])
check("P1 positive control: 00306B10's one caller (0030CDCA) passes a BattleUnit in the empty context",
      s306 == [0x30CDCA] and any(ctx == "" and T == "BattleUnit" and arg == 0 for (T, arg, k, ctx) in rec[(0x30CDCA, 0x306B10)]))
check("N1 an address-taken callee is not typed (0030AB40)", tk.get(0x30AB40, 0) > 0 and 0x30AB40 not in typed)
naive_extra = [0x307CE0, 0x309230, 0x30B950, 0x30BB30, 0x32A4D0]
check("N2 the context-free rule's five extra rows are NOT typed here (their callers are not proven)",
      all(f not in typed for f in naive_extra))
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
