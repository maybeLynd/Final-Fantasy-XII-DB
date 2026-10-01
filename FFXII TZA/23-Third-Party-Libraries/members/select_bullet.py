"""select_bullet.py - EC-7 member selector for the Bullet physics library (FABLE, 2026-09-13).

  bullet.tsv   every census entry in the two Bullet link ranges
                 00830760 up to 00861E90 (collision, shapes, narrowphase, LinearMath hull library)
                 0087F180 up to 008800C0 (btSimulationIslandManager and its union-find)
               except entries whose RTTI includes a class that is not Bullet's (folded bodies), entries called only from
               code outside Bullet, its Phyre physics client and unwind thunks (folded stubs), A-measured entries and entries
               declared by another family.

Bullet class names: any RTTI name containing a 'bt' + capital token (including function-local classes decorated with a
Bullet method), plus Bullet's helper structs DebugDrawcallback and SupportVertexCallback.
Asserts: btCollisionWorld::updateSingleAabb 00840DF0 references Bullet's own 'Overflow in AABB, object removed from
simulation' / continuousphysics.com text; the entry before each range is not Bullet's (008306C0 is called from the CRT
at 0082EDA0; 0087EBF0 is zlib's, called from zlib's 0087E970) and 00861E90 is a 6-byte import thunk.
Prints the controls: outbound targets, inbound caller zones, shared-global zones.
Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe, graph/functions.tsv, rtti/methods.tsv; needs capstone.
Usage: python select_bullet.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "Bullet physics library"
R = ((0x830760, 0x861E90), (0x87F180, 0x8800C0))
def inr(a): return any(lo <= a < hi for lo, hi in R)
def client(f): return 0x680000 <= f < 0x6B0000 or 0x8A0000 <= f < 0x8C0000   # Phyre physics object; unwind / teardown thunks
BT = re.compile(r"(^|[^A-Za-z])bt[A-Z]")
HELPERS = ("DebugDrawcallback", "SupportVertexCallback")

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
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
cls = collections.defaultdict(set)
for line in open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: cls[int(p[0], 16)].add(p[1])
    except ValueError: pass
def body(e): return d[off(e):off(e) + sizes[e]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")

# fingerprint
txt = d[off(0x1CCE6A0):off(0x1CCE6A0) + 200]
assert txt.startswith(b"Overflow in AABB, object removed from simulation") and b"continuousphysics.com" in txt
hits = set()
for x in md.disasm(body(0x840DF0), 0x840DF0):
    m = rx.search(x.op_str)
    if m and x.mnemonic == "lea": hits.add(x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1))
assert 0x1CCE6A0 in hits
assert body(0x861E90)[:2] == b"\xff\x25" and sizes[0x861E90] == 6

text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set); out = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner_of(src)
    if f is None or f == t: continue
    if inr(t) or t in (0x8306C0, 0x87EBF0): callers[t].add(f)
    if inr(src) and not inr(t): out[t].add(f)
assert 0x82EDA0 in callers[0x8306C0] and 0x87E970 in callers[0x87EBF0] and not any(inr(f) for f in callers[0x87EBF0] | callers[0x8306C0])

span = [e for e in ents if inr(e)]
bt_rtti = sum(1 for e in span if any(BT.search(c) or c in HELPERS for c in cls.get(e, ())))
members, excl = [], collections.defaultdict(list)
for e in span:
    c = cls.get(e, set()); foreign = {x for x in c if not (BT.search(x) or x in HELPERS)}
    outside = callers[e] and not any(inr(f) for f in callers[e]) and any(not client(f) for f in callers[e])
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif foreign: excl["RTTI not Bullet's (" + "/".join(sorted(foreign))[:40] + ")"].append(e)
    elif outside: excl["called only from outside Bullet and its client"].append(e)
    else: members.append(e)
print("Bullet ranges: entries %d (%d at Bullet vtable slots), members %d" % (len(span), bt_rtti, len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-60s %4d  %s" % (k, len(v), " ".join("%08X" % x for x in v[:8]) + (" ..." if len(v) > 8 else "")))
print("control outbound: %d targets outside Bullet:" % len(out), " ".join("%08X(%d)" % (t, len(out[t])) for t in sorted(out)))
inb = collections.Counter("%04X" % (f >> 16) for e in span for f in callers[e] if not inr(f))
print("control inbound caller zones:", dict(inb))
DATA = secs[".data"]; refs = collections.defaultdict(set)
for e in ents:
    if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0: continue
    for x in md.disasm(body(e), e):
        m = rx.search(x.op_str)
        if not m: continue
        g = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if DATA[0] <= g < DATA[0] + DATA[1]: refs[g].add(e)
zones = collections.Counter()
for g, fs in refs.items():
    if g == 0x1F44830: continue
    ins = {f for f in fs if inr(f)}; outs = fs - ins
    if ins and outs: zones[",".join(sorted({"%04X" % (f >> 16) for f in outs}))[:48]] += 1
print("control globals: shared, by outside zone set:", dict(zones))
if "--write" in sys.argv:
    open(os.path.join(HERE, "bullet.tsv"), "w").write(
        "# Bullet physics, 00830760 up to 00861E90 and 0087F180 up to 008800C0, less foreign RTTI, outside-only stubs, A and other families - select_bullet.py\n"
        + "\n".join("%08X" % e for e in members) + "\n")
    print("wrote", len(members))
