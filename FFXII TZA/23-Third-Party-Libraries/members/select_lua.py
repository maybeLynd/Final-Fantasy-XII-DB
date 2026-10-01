"""select_lua.py - EC-7 member selector for the embedded Lua 5.2.1 library (FABLE, 2026-09-13).

  lua.tsv   every census entry from 0080F2E0 up to 00830760 (exclusive), except entries carrying any RTTI (Lua is C: a
            vtable slot here would be foreign, folded code), entries joined to the object by nothing (no direct call to
            or from another entry of the range, no rip-relative reference to Lua's string pool 01CCA080-01CCD37F, no
            .rdata slot in a registration table), A-measured entries and entries declared by another family.

Asserts: the banner '$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio' at 01CCA080; luaopen_base
00814F90 leas 'Lua 5.2' and '_VERSION'; Lua's pool ends where Bullet's serialisation names begin (01CCD380
'btCollisionShapeData'); the entries just below the range are zlib (crc32_z 0080E910) and four import thunks
(0080F2BC-0080F2CE); 00830760 is Bullet's (called from Bullet 0083B580).
Prints the controls: outbound targets, inbound caller zones, shared .data globals.
Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe, graph/functions.tsv, rtti/methods.tsv; needs capstone.
Usage: python select_lua.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "Lua 5.2.1 library"
LO, HI = 0x80F2E0, 0x830760
POOL = (0x1CCA080, 0x1CCD380)
d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)
sizes = cd.load_functions(); ents = sorted(sizes); eset = set(ents)
names = {}
for line in open(os.path.join(W, "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try: names[int(p[0], 16)] = p[1]
    except ValueError: pass
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
rtti = set()
for line in open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"):
    try: rtti.add(int(line.split("\t")[0], 16))
    except ValueError: pass
def body(e): return d[off(e):off(e) + sizes[e]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")
inr = lambda a: LO <= a < HI

assert d[off(POOL[0]):off(POOL[0]) + 80].startswith(b"$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio")
assert d[off(POOL[1]):off(POOL[1]) + 20].startswith(b"btCollisionShapeData")
assert names.get(0x80E910) == "crc32_z" and all(sizes.get(a) == 6 for a in (0x80F2BC, 0x80F2C2, 0x80F2C8, 0x80F2CE))

text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set); callees = collections.defaultdict(set); out = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner_of(src)
    if f is None or f == t: continue
    callers[t].add(f); callees[f].add(t)
    if inr(src) and not inr(t): out[t].add(f)
assert 0x83B580 in callers[0x830760]

span = [e for e in ents if inr(e)]
poolref, lea_to, refs = set(), collections.defaultdict(set), collections.defaultdict(set)
DATA = secs[".data"]
for e in ents:
    if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0: continue
    inside = inr(e)
    for x in md.disasm(body(e), e):
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if DATA[0] <= t < DATA[0] + DATA[1]: refs[t].add(e)
        if inside:
            if POOL[0] <= t < POOL[1]: poolref.add(e)
            if x.mnemonic == "lea" and inr(t): lea_to[t].add(e)
luaopen_base = {t for x in md.disasm(body(0x814F90), 0x814F90) for m in [rx.search(x.op_str)] if m and x.mnemonic == "lea"
                for t in [x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)]}
assert d[off(0x1CCA898):off(0x1CCA898) + 8] == b"Lua 5.2\0" and 0x1CCA898 in luaopen_base and 0x1CCA8A0 in luaopen_base
slot = collections.Counter()
ro_ = off(0x8C2000)
for k in range(0, 0x152D7FC - 8, 8):
    q = struct.unpack_from("<Q", d, ro_ + k)[0]
    if inr(q): slot[q] += 1

members, excl = [], collections.defaultdict(list)
for e in span:
    joined = (any(inr(f) for f in callers[e]) or any(inr(t) for t in callees[e]) or e in poolref or slot[e]
              or any(inr(f) for f in lea_to.get(e, ())))
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif e in rtti: excl["carries RTTI (foreign, folded)"].append(e)
    elif not joined: excl["joined to Lua by nothing"].append(e)
    else: members.append(e)
print("Lua range: entries %d, string-pool referencers %d, members %d" % (len(span), len(poolref), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-50s %4d  %s" % (k, len(v), " ".join("%08X" % x for x in v[:10]) + (" ..." if len(v) > 10 else "")))
print("control outbound: %d targets:" % len(out), " ".join("%08X(%d)" % (t, len(out[t])) for t in sorted(out)))
inb = collections.Counter("%04X" % (f >> 16) for e in span for f in callers[e] if not inr(f))
print("control inbound caller zones (top):", dict(inb.most_common(10)), "entries called from outside:", sum(1 for e in span if any(not inr(f) for f in callers[e])))
zones = collections.Counter()
for g, fs in refs.items():
    if g == 0x1F44830: continue
    ins = {f for f in fs if inr(f)}; outs = fs - ins
    if ins and outs: zones[",".join(sorted({"%04X" % (f >> 16) for f in outs}))[:48]] += 1
print("control globals: shared, by outside zone set:", dict(zones))
if "--write" in sys.argv:
    open(os.path.join(HERE, "lua.tsv"), "w").write(
        "# Lua 5.2.1, 0080F2E0 up to 00830760, less RTTI-carrying, unjoined, A and other families - select_lua.py\n"
        + "\n".join("%08X" % e for e in members) + "\n")
    print("wrote", len(members))
