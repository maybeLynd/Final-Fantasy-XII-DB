"""PA-1: who calls PApplication vtable slots 10, 15, 16, 22, 23, 24? (OPUS, 2026-09-27). Control. Static.

  C1 THE GETTER ROUTE: 00796E20 is `mov rax, [02EA5368] / ret` (the application instance). At all of its call sites
     (image-wide rel32; 106), the returned pointer and the vtable loaded from it are followed; the slots called on the
     application are collected. POSITIVE CONTROL: calls are found (slots 12, 13, 14, 18, 19, 25 - 25 from game code 00197160)
  C2 none of those calls is to slot 10, 15, 16, 22, 23 or 24
  C3 THE FRAMEWORK RANGE 0x790000..0x7A4400: no indirect call at vtable +0x50 / +0x78 / +0x80 exists there at all, on any
     receiver (so no `this`-based call to 10 / 15 / 16 from the framework's own methods)
  C4 the game's overrides of 10 / 15 / 16 (0017D120, 0017D1A0, 0017D210) are referenced only by GameApplication's vtable
     (008C5760 slots 10 / 15 / 16): no rel32 call or jmp and no other absolute pointer to them anywhere in the image
The global-pointer trace and the window procedure (slots 14 / 17 / 20, 25 from the device poll) are the page's
(2026-09-14, FABLE). Not claimed: a call through a copy of the application pointer stored in another object.
"""
import re, struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
_c = {}
def D(f):
    if f not in _c: _c[f] = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    return _c[f]
M = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
def fam(r):
    mm = re.match(r"(r\d+)[dwb]?$", r); return M.get(r, mm.group(1) if mm else r)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

g = ["%s %s" % (x.mnemonic, x.op_str) for x in D(0x796E20)]
x0 = next(cs.disasm(d[off(0x796E20):off(0x796E20) + 8], 0x796E20))
gslot = 0x796E20 + x0.size + int(re.search(r"0x([0-9a-f]+)\]", x0.op_str).group(1), 16)
sites = []; rel = collections.defaultdict(list); absrefs = collections.defaultdict(list)
OVR = {0x17D120: 10, 0x17D1A0: 15, 0x17D210: 16}
for ch, vs, va, rs, ro in SECS:
    for t in OVR:
        q = struct.pack("<Q", t); j = d.find(q, ro, ro + rs)
        while j >= 0: absrefs[t].append(BASE + va + j - ro); j = d.find(q, j + 1, ro + rs)
    if not ch & 0x20000000: continue
    for p in range(ro, ro + rs - 5):
        if d[p] in (0xE8, 0xE9):
            v = BASE + va + p - ro; t = v + 5 + struct.unpack_from("<i", d, p + 1)[0]
            if t == 0x796E20: sites.append(v)
            if t in OVR: rel[t].append(v)
slots = collections.defaultdict(list)
for v in sites:
    f = owner(v); b = D(f); i = next((k for k, x in enumerate(b) if x.address == v), None)
    if i is None: continue
    app = {"rax"}; vt = set()
    for y in b[i + 1:i + 40]:
        s = y.op_str; ops = [o.strip() for o in s.split(",")]
        m = re.fullmatch(r"qword ptr \[(\w+)\]", ops[1]) if len(ops) == 2 else None
        if y.mnemonic == "mov" and m and fam(m.group(1)) in app: vt.add(fam(ops[0])); continue
        mm = re.fullmatch(r"qword ptr \[(\w+) \+ 0x([0-9a-f]+)\]", s)
        if y.mnemonic in ("call", "jmp") and mm and fam(mm.group(1)) in vt: slots[int(mm.group(2), 16) // 8].append(y.address)
        if y.mnemonic == "mov" and len(ops) == 2 and re.fullmatch(r"\w+", ops[1]):
            if fam(ops[1]) in app: app.add(fam(ops[0]))
            elif fam(ops[1]) in vt: vt.add(fam(ops[0]))
            else: app.discard(fam(ops[0])); vt.discard(fam(ops[0]))
        if y.mnemonic == "call": app -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}; vt -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
        if y.mnemonic == "ret" or (not app and not vt): break
check("C1 the getter route: the instance getter's call sites reach application slots (positive control)",
      g[:2] == [g[0], "ret "] and gslot == 0x2EA5368 and len(sites) >= 100 and {12, 13, 14, 18, 19, 25} <= set(slots),
      "%d sites; slots %s" % (len(sites), sorted(slots)))
check("C2 no getter-route call to slot 10, 15, 16, 22, 23 or 24", not ({10, 15, 16, 22, 23, 24} & set(slots)))
fr = []
for f, sz in sizes.items():
    if 0x790000 <= f < 0x7A4400 and sz > 0:
        for x in D(f):
            m = re.fullmatch(r"qword ptr \[(\w+) \+ 0x(50|78|80)\]", x.op_str)
            if x.mnemonic in ("call", "jmp") and m: fr.append(x.address)
check("C3 no indirect call at +0x50 / +0x78 / +0x80 anywhere in the framework range", not fr, str(["%08X" % a for a in fr][:4]))
vt = off(0x8C5760)
check("C4 the overrides of 10 / 15 / 16 are referenced only by GameApplication's vtable slots",
      all(struct.unpack_from("<Q", d, vt + 8 * s)[0] == t for t, s in OVR.items())
      and all(rel[t] == [] and absrefs[t] == [0x8C5760 + 8 * s] for t, s in OVR.items()),
      str({hex(t): (rel[t], ["%08X" % a for a in absrefs[t]]) for t in OVR}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
