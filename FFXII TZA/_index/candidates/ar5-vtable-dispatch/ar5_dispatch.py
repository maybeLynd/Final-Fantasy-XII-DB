"""ar5_dispatch.py - AR-5: can any vtable slot be shown never dispatched, statically? (FABLE, Claude Opus 5.5, 2026-09-27)

AR-5's 2026-09-16 plan: census the slot indices that dispatch names, and call the slots outside that set statically
never dispatched. This control runs it, and runs the other sound static criterion (a class whose vtable nothing
installs), over every RTTI vtable. Both come out empty.
  A1 the population: the 2,286 RTTI vtables of rtti-class-vtables.tsv, walked slot by slot while each qword points
     into .text, hold 25,801 slots over 6,886 distinct functions, at slot indices 0..76.
  A2 every slot index 0..76 is named by at least one fixed-slot dispatch, `call` or `jmp qword ptr [reg + 8k]` (reg
     not rip or rsp). The 2026-09-16 count missed the tail-dispatch `jmp` form: indices 59, 63 and 73 are named only
     by `jmp` (00616E1B, 00616E4B, 00726F4E). So no slot is outside the dispatched set, and the index census cannot
     show any slot dead.
  A3 no class is provably never constructed: every vtable address but three is referenced by code, through a rip
     operand or an image-base-relative displacement, and those three are referenced from data. So "never installed"
     marks no slot dead either.
  A4 the remaining indirect forms are listed: 14 call/jmp sites through an indexed or two-register address, and 24
     calls through a pointer held in a stack slot.
Controls: A2 must find the index-59 tail dispatch at 00616E1B; A3 must find the constructor reference to a vtable read
by hand, PMotionBlur 00D62170.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(n):
    s = pe + 24 + opt + i * 40
    SECS.append((d[s:s + 8].rstrip(b"\0").decode(), BASE + struct.unpack_from("<I", d, s + 12)[0],
                 struct.unpack_from("<I", d, s + 8)[0], struct.unpack_from("<I", d, s + 20)[0], struct.unpack_from("<I", d, s + 16)[0]))
def off(v):
    for nm, va, vs, ro, rs in SECS:
        if va <= v < va + min(vs, rs): return v - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
TLO, THI = 0x121000, 0x8C0000

vts = set()
for l in open(DB / "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/rtti-class-vtables.tsv", encoding="utf-8"):
    if l.startswith("#") or not l.strip(): continue
    for c in l.rstrip("\n").split("\t"):
        if re.fullmatch(r"[0-9A-F]{8}", c) and 0x8C0000 <= int(c, 16) < 0x1F00000: vts.add(int(c, 16)); break
vts = sorted(vts); vset = set(vts)
slots = collections.defaultdict(set); nslot = 0; maxk = 0
for vt in vts:
    k = 0
    while True:
        a = vt + 8 * k
        if k and a in vset: break
        o = off(a)
        if o is None: break
        v = struct.unpack_from("<Q", d, o)[0]
        if not TLO <= v < THI: break
        slots[v].add((vt, k)); nslot += 1; maxk = max(maxk, k); k += 1
check("A1 2,286 RTTI vtables: 25,801 slots, 6,886 functions, indices 0..76", len(vts) == 2286 and nslot == 25801 and len(slots) == 6886 and maxk == 76,
      "vtables %d slots %d functions %d max index %d" % (len(vts), nslot, len(slots), maxk))

cs = Cs(CS_ARCH_X86, CS_MODE_64)
FIX = re.compile(r"^qword ptr \[(r\w+)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]$")
RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
DISP = re.compile(r"\[(r\w+)(?: \+ r\w+(?:\*\d)?)? \+ (0x[0-9a-f]{6,})\]")
named = collections.defaultdict(list); vref = collections.Counter(); odd = []
for f in sorted(SIZES):
    if not TLO <= f < THI or SIZES[f] <= 0: continue
    o = off(f)
    if o is None: continue
    for x in cs.disasm(d[o:o + SIZES[f]], f):
        s = x.op_str
        if x.mnemonic in ("call", "jmp") and "ptr [" in s:
            m = FIX.match(s)
            if m and m.group(1) not in ("rip", "rsp"):
                disp = int(m.group(3), 0) if m.group(3) else 0
                if m.group(2) == "-": disp = -disp
                if disp % 8 == 0 and len(named[disp // 8]) < 4: named[disp // 8].append((x.address, x.mnemonic))
            elif "rip" not in s: odd.append("%08X %s %s" % (x.address, x.mnemonic, s))
        m = RIP.search(s)
        if m:
            t = x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
            if t in vset: vref[t] += 1
        for m in DISP.finditer(s):
            t = BASE + int(m.group(2), 16)
            if t in vset: vref[t] += 1
missing = [k for k in range(maxk + 1) if not named[k]]
jmp_only = [k for k in range(maxk + 1) if named[k] and all(mn == "jmp" for _, mn in named[k])]
ctl = any(a == 0x616E1B for a, _ in named[59])
check("A2 every slot index 0..76 is named by a fixed-slot call or jmp; control 00616E1B names index 59",
      not missing and ctl, "unnamed %s; named only by jmp in the first sites seen: %s; control %s" % (missing, jmp_only, ctl))

dref = collections.Counter()
for nm, va, vs, ro, rs in SECS:
    if nm == ".text" or rs == 0: continue
    blob = d[ro:ro + min(vs, rs)]
    for i in range(0, len(blob) - 7, 8):
        v = struct.unpack_from("<Q", blob, i)[0]
        if v in vset: dref[v] += 1
nocode = [v for v in vts if not vref[v]]
check("A3 every vtable is referenced: all but 3 by code, those 3 from data; control PMotionBlur 00D62170 has a code reference",
      len(nocode) == 3 and all(dref[v] for v in nocode) and vref[0xD62170] > 0,
      "no code reference: %s; their data references %s" % (["%08X" % v for v in nocode], [dref[v] for v in nocode]))
stack = [x for x in odd if "[rsp" in x]; idx = [x for x in odd if "[rsp" not in x]
check("A4 the other indirect forms are listed: 14 indexed or two-register sites, 24 calls through a stack-held pointer",
      len(idx) == 14 and len(stack) == 24, "%d indexed: %s; %d stack-held" % (len(idx), idx, len(stack)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
