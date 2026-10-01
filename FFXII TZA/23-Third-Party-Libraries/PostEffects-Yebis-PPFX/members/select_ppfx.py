"""select_ppfx.py - EC-7 member selector for the PPFX post-effect library (FABLE, 2026-09-13).

  ppfx-span.tsv   every census entry from 006DA880 up to 007911E0 (exclusive) except entries whose RTTI vtable
                  appearances include a class outside PPFX:: (ICF-folded bodies shared with Yebis:: / Bullet classes),
                  entries already A-measured, and entries declared by another family.

Asserts the provenance evidence and prints the boundary controls the inventory page cites:
  evidence   functions that lea a '..\\src\\...' source path or a 'PPFX' diagnostic, or sit at a PPFX:: vtable slot;
             the distinct source files named (26)
  edges      the entries just outside each edge are not PPFX: 006DA860 is called from a static initialiser, 007911E0
             starts Phyre::PFramework descriptors
  outbound   direct calls from the span to census entries outside it, by target
  globals    .data locations referenced from inside and outside (security cookie removed), by outside zone
Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe, Tools/work/graph/functions.tsv, Tools/work/rtti/methods.tsv;
needs capstone.  Usage: python select_ppfx.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

LO, HI = 0x6DA880, 0x7911E0
NAME = "PPFX post-effect library"
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
sizes = cd.load_functions()
# UC-1 SERIES BREAK (2026-09-28): the default census now also carries the UC-1 frontier bodies,
# which are frontier BY RULING - never A/B/C, and check_dispositions refuses any members file that
# names one. Leave them out of the selection population, so a re-run reproduces the declared family
# (on 2026-09-29 an unpatched re-run admitted 733 of them into PPFX and failed the libvorbis closure
# assertion). They are also absent from the caller/control attribution below. SWE2-EC7 2026-09-29.
import uc1_band
# FABLE ruling, point 4 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): the UC-1 bodies stay IN
# the population, so every caller/closure/control test sees calls made by a UC-1 body; they are removed only from
# the written members files (a UC-1 body is frontier by ruling, declared only by an R1 span row).
UC1 = set(uc1_band.frontier_starts())
_out = lambda xs: [e for e in xs if e not in UC1]
ents = sorted(sizes); eset = set(ents)
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
def cstr(t):
    o = off(t)
    if o is None: return None
    s = d[o:o + 160].split(b"\0")[0]
    return s.decode("latin1") if len(s) >= 4 and all(32 <= c < 127 for c in s) else None

span = [e for e in ents if LO <= e < HI]
evid, srcfiles, refs = set(), set(), collections.defaultdict(set)
DATA = secs[".data"]
for e in ents:
    if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0: continue
    inside = LO <= e < HI
    for x in md.disasm(body(e), e):
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if DATA[0] <= t < DATA[0] + DATA[1]: refs[t].add(e)
        if inside and x.mnemonic == "lea":
            s = cstr(t)
            if s and (s.startswith("..\\src\\") or "PPFX" in s):
                evid.add(e)
                if s.startswith("..\\src\\"): srcfiles.add(s.split("(")[0])
    if inside and any(c.startswith("PPFX::") for c in cls.get(e, ())): evid.add(e)
print("evidence: %d entries (%d by source path or PPFX diagnostic / PPFX:: vtable), %d source files" % (len(evid), len(evid), len(srcfiles)))
assert len(srcfiles) == 25 and "..\\src\\ppfx.cpp" in srcfiles and "..\\src\\UT\\ppfxLicense.cpp" in srcfiles, sorted(srcfiles)
# edges
assert not any(c.startswith("PPFX::") for c in cls.get(0x7911E0, ())) and any("PFramework" in c for c in cls.get(0x7911E0, ()))

text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
out = collections.defaultdict(set); inn = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to)
    t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    si, ti = LO <= src < HI, LO <= t < HI
    if si == ti: continue
    f = owner_of(src)
    if f is not None: (out[t] if si else inn[t]).add(f)
# callers the library can legitimately have: its integration client (006Cxxxx), static initialisers (0016xxxx) and
# teardown / unwind thunks (008Axxxx, 008Bxxxx). An entry also called from anywhere else is a shared body - left out.
def expected_caller(f): return (f >> 16) in (0x6C, 0x16) or 0x8A0000 <= f < 0x8C0000
members, excl = [], collections.defaultdict(list)
for e in span:
    c = cls.get(e, set()); other = {x for x in c if not x.startswith("PPFX::")}
    stray = sorted(f for f in inn.get(e, ()) if not expected_caller(f))
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif other: excl["RTTI outside PPFX:: (" + "/".join(sorted({x.split("::")[0] for x in other}))[:30] + ")"].append(e)
    elif stray: excl["also called from outside the library and its client (%s)" % ",".join("%08X" % f for f in stray[:4])].append(e)
    else: members.append(e)
print("span %08X up to %08X: entries %d, members %d" % (LO, HI, len(span), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-60s %4d  %s" % (k, len(v), " ".join("%08X" % x for x in v[:8]) + (" ..." if len(v) > 8 else "")))

print("control outbound: %d targets:" % len(out), " ".join("%08X(%d)" % (t, len(out[t])) for t in sorted(out)))
print("control inbound: callers by zone", dict(collections.Counter("%04X" % (f >> 16) for v in inn.values() for f in v)))
zones = collections.Counter()
for g, fs in refs.items():
    if g == 0x1F44830: continue
    ins = {f for f in fs if LO <= f < HI}; outs = fs - ins
    if ins and outs: zones[",".join(sorted({"%04X" % (f >> 16) for f in outs}))[:40]] += 1
print("control globals: shared, by outside zone set:", dict(zones))

if "--write" in sys.argv:
    open(os.path.join(HERE, "ppfx-span.tsv"), "w").write(
        "# PPFX span 006DA880 up to 007911E0 less foreign RTTI, A and other families - select_ppfx.py\n"
        + "\n".join("%08X" % e for e in _out(members)) + "\n")
    print("wrote", len(_out(members)))
