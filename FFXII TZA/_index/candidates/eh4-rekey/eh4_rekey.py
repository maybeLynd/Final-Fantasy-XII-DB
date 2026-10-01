"""EH-4 lifetime residual: a storage record takes a new identity without the initialiser (OPUS, 2026-09-27). Static.

  R1 the re-key wrapper 00322050(unit): zeroes the unit's +0xEA4 (dword) and +0xEA8 (byte), then calls 003220E0 on the
     unit's storage record [unit + 0x10] and stores the new packed handle into the unit's +8
  R2 its two callers: BattleUnit_ApplyUnitDefinition 0023A570 and BattleUnit_TeardownAndDespawn 00300E40 - every
     despawn re-keys the record
  R3 003220E0 calls 002659D0, which advances the record's +0x16 handle generation (+1, & 0x7FF, 0 -> 1): old handles
     to the record go stale, the record itself is kept
  R4 none of the three bodies writes the record's flag bytes +0x08..+0x14, and the initialiser 00266530 has one caller
     (ActorStorage_AllocateAndInitializeRecords 002679F0): a re-keyed record is NOT re-initialised
Not claimed: which runtime writers set the flag bits during a record's life (so which values a new identity inherits),
or that a despawned record is re-used by the very next spawn.
"""
import re, struct, sys, bisect
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
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + sizes[f]], f)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
def callers(t):
    out = set()
    for ch, vs, va, rs, ro in SECS:
        if ch & 0x20000000:
            for p in range(ro, ro + rs - 5):
                if d[p] in (0xE8, 0xE9) and BASE + va + p - ro + 5 + struct.unpack_from("<i", d, p + 1)[0] == t:
                    f = owner(BASE + va + p - ro)
                    if f: out.add(f)
    return out
W, K, G = I(0x322050), I(0x3220E0), I(0x2659D0)
check("R1 the wrapper zeroes unit +0xEA4 / +0xEA8 and re-keys the record at [unit+0x10]",
      W.get(0x322059) == "mov dword ptr [rcx + 0xea4], 0" and W.get(0x322063) == "mov byte ptr [rcx + 0xea8], 0"
      and W.get(0x32206A) == "mov rcx, qword ptr [rcx + 0x10]" and W.get(0x32206E) == "call 0x3220e0" and W.get(0x322073) == "mov dword ptr [rbx + 8], eax")
cw = callers(0x322050)
check("R2 its callers are ApplyUnitDefinition and TeardownAndDespawn", cw == {0x23A570, 0x300E40}, str(sorted("%08X" % f for f in cw)))
check("R3 003220E0 advances the record's +0x16 generation through 002659D0 (1..0x7FF, never 0)",
      K.get(0x322107) == "call 0x2659d0" and G.get(0x2659D0) == "movzx eax, word ptr [rcx + 0x16]" and G.get(0x2659DB) == "and eax, 0x7ff"
      and G.get(0x2659E0) == "cmove eax, edx" and G.get(0x2659E3) == "mov word ptr [rcx + 0x16], ax")
flagw = [s for body in (W, K, G) for s in body.values() if re.search(r"ptr \[r(?!sp)\w+ \+ 0x(8|9|a|b|c|d|e|f|1[0-4])\], ", s) and not s.startswith(("cmp", "test"))
         and s.split()[0] in ("mov", "and", "or", "xor", "inc", "dec", "bts", "btr")]
init_callers = callers(0x266530)
check("R4 no flag-byte write on the re-key path, and the initialiser's only caller is the allocator",
      [s for s in flagw if "[rbx + 8]" not in s] == [] and init_callers == {0x2679F0}, str(flagw[:4]) + " " + str(sorted("%08X" % f for f in init_callers)))
import collections
edges = collections.defaultdict(set)
for l in open(ROOT / "Database/Tools/work/graph/edges.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: edges[int(c[0], 16)].add(int(c[1], 16))
    except ValueError: pass
def reach(root, depth):
    seen = {root}; fr = {root}
    for _ in range(depth):
        fr = {g for f in fr for g in edges.get(f, ())} - seen; seen |= fr
    return seen
Wr = collections.defaultdict(list)
for l in open(ROOT / "Database/FFXII TZA/_types/field-access-index.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if len(c) > 6 and c[0] == "ActorStorageRecord" and "w" in c[3]:
        try:
            o = int(c[1], 16)
            if 8 <= o <= 0x14: Wr[int(c[4], 16)].append(c[6])
        except ValueError: pass
onT = {f: Wr[f] for f in Wr if f in reach(0x300E40, 4)}
onA = {f: Wr[f] for f in Wr if f in reach(0x23A570, 4)}
clears = [s for f in list(onT) + list(onA) for s in (onT.get(f, []) + onA.get(f, [])) if s.startswith("and ") or s.startswith("mov byte") or s.startswith("mov dword")]
check("R5 neither re-key path clears a flag: of the flag-byte writer functions, those within four calls of"
      " TeardownAndDespawn only SET bits (+0x0C |= 0x10 at 0026D6F0, +0x08 |= 4 at 002E3AF0), and none lies within four"
      " calls of ApplyUnitDefinition (call graph edges.tsv; tail jumps and thunks it misses are not covered)",
      len(Wr) >= 40 and sorted(onT) == [0x26D6F0, 0x2E3AF0] and not onA and not clears,
      "%d writer functions; teardown-side %s; definition-side %s" % (len(Wr), sorted("%08X" % f for f in onT), sorted("%08X" % f for f in onA)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
