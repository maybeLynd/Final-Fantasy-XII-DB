"""bq5_phase_writers.py - BQ-5: does any writer outside the executor 002621D0 leave the command phase byte at 2 or 3
before entry? (FABLE, Claude Opus 5.5, 2026-09-26)

The phase byte is cmdState[0x15], where cmdState = *(b + 0xA8) + s8(b[0x11]) * 40. Callbacks receive cmdState + 0x18
in r8, so for them the byte is [r8 - 3].
  Q1 every byte write to the phase byte, image-wide, by addressing shape:
     - [base + idx*8 + 0x15], the result writers' form;
     - [reg + 0x15] in any function that loads both [x+0xA8] and s8 [x+0x11];
     - [reg - 3] in any lifecycle callback.
     The only non-zero writers are VMResult_WriteFloat32 (3), VMResult_WriteInt32 (2) and 002651A0 (2, a
     write-and-read-back), plus the executor's own 1. Everything else writes 0.
  Q2 the three non-zero writers run only inside a lifecycle callback. Every function that calls them is a callback
     from scriptvm-verb-table.tsv, or a helper reached only from callbacks. A callback with a direct caller is called
     only by another callback. No callback's pointer appears in .rdata/.data more times than its verb-table roles, so
     no other table dispatches them.
  Q3 no callback writes b[0x11], the current-slot byte, so a result written during a callback lands on the slot the
     executor is running. Control: the same matcher finds the one writer of b[0x11] among the functions that load
     [x+0xA8]: ActorResource_StartEntryScriptExecution (003DBDC0), which is not a callback.
  Q4 controls: the executor writes 1 on the running path (0026230B) and 0 on every result path (00262382), the
     page's own figures.
So inside the executor's call a 2 or 3 is either read and reset, or overwritten by 1. The byte on entry is 0 or 1,
and the >= 2 entry arm is unreachable from any writer in this image. Static.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, collections, csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = {struct.unpack_from("<8s", d, pe + 24 + optsz + i * 40)[0].rstrip(b"\0").decode():
        struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(n)}
def off(v):
    for vs, va, rs, ro in secs.values():
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}; NAME = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2]); NAME[int(r[0], 16)] = r[1]
    except (ValueError, IndexError): pass
ST = sorted(F)
def owner(a):
    i = bisect.bisect_right(ST, a) - 1
    return ST[i] if i >= 0 and a < ST[i] + F[ST[i]] else None
def body(f): return list(cs.disasm(d[off(f):off(f) + F[f]], f)) if f in F and off(f) is not None else []
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
K = collections.Counter()
for r in csv.DictReader(open(HERE.parents[1] / "Verb-Dispatch/scriptvm-verb-table.tsv", encoding="utf-8"), delimiter="\t"):
    for c in ("begin", "poll", "slot2", "result"):
        if r.get(c): K[int(r[c], 16)] += 1
WR = ("mov", "or", "and", "add", "inc", "dec", "sub", "xor")
def is_bw(x, disp):
    o = x.operands
    return o and o[0].type == X86_OP_MEM and o[0].mem.disp == disp and o[0].size == 1 and x.mnemonic in WR \
        and cs.reg_name(o[0].mem.base) not in ("rsp", "rbp", "rip")
src = lambda x: x.op_str.split(", ", 1)[1] if ", " in x.op_str else x.op_str
q1 = []
for f in F:
    L = body(f)
    if not L: continue
    a8 = any(x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_MEM and x.operands[1].mem.disp == 0xA8
             and x.operands[1].size == 8 for x in L)
    s11 = any(x.mnemonic.startswith("movs") and len(x.operands) == 2 and x.operands[1].type == X86_OP_MEM and x.operands[1].mem.disp == 0x11
              and x.operands[1].size == 1 for x in L)
    for x in L:
        if is_bw(x, 0x15) and ((x.operands[0].mem.index != 0 and x.operands[0].mem.scale == 8) or (a8 and s11) or f == 0x2621D0):
            q1.append((f, x.address, src(x)))
        if f in K and is_bw(x, -3):
            q1.append((f, x.address, src(x)))
nonzero = sorted({(f, a, v) for f, a, v in q1 if v != "0"})
print("   non-zero phase writes:", [("%08X" % f, "%08X" % a, v) for f, a, v in nonzero])
EXPECT = {(0x26B4C0, 0x26B4D6, "3"), (0x26B4E0, 0x26B4F0, "2"), (0x2651A0, 0x2651B0, "2"), (0x2621D0, 0x26230B, "1")}
check("Q1 the non-zero writers are exactly VMResult_WriteFloat32, VMResult_WriteInt32, 002651A0 and the executor's 1",
      set(nonzero) == EXPECT, "zero writes elsewhere: %d" % sum(1 for f, a, v in q1 if v == "0"))
# Q2
vs, va, rs, ro = secs[".text"]; T0 = BASE + va; text = d[ro:ro + rs]
callers = collections.defaultdict(set)
for i in range(len(text) - 6):
    b0 = text[i]
    L = 1 if b0 in (0xE8, 0xE9) else 2 if (b0 == 0x0F and 0x80 <= text[i + 1] <= 0x8F) else 0
    if not L: continue
    t = T0 + i + L + 4 + int.from_bytes(text[i + L:i + L + 4], "little", signed=True)
    if t in F: callers[t].add(owner(T0 + i))
def only_from_callbacks(f, seen=None, depth=0):
    seen = seen if seen is not None else set()
    if f in K: return True
    if depth > 5 or f in seen or not callers.get(f): return False
    seen.add(f)
    return all(only_from_callbacks(g, seen, depth + 1) for g in callers[f])
writers = (0x26B4C0, 0x26B4E0, 0x2651A0)
C = {g for w in writers for g in callers[w]}
bad = sorted(g for g in C if not only_from_callbacks(g))
direct_bad = sorted(f for f in (C & set(K)) if any(g not in K for g in callers.get(f, ())))
absref = collections.Counter()
for nm in (".rdata", ".data"):
    _, sva, srs, sro = secs[nm]; blob = d[sro:sro + srs]
    for k in range(0, len(blob) - 7, 8):
        v = struct.unpack_from("<Q", blob, k)[0]
        if v in C: absref[v] += 1
extra = sorted(f for f in C & set(K) if absref[f] > K[f])
taken = []   # rip-relative lea/mov forming a writer's address (branch displacements are callers, counted above)
for i in range(len(text) - 4):
    t = T0 + i + 4 + int.from_bytes(text[i:i + 4], "little", signed=True)
    if t in writers:
        f = owner(T0 + i)
        x = next((x for x in body(f) if x.address < T0 + i < x.address + x.size), None) if f else None
        if x is not None and x.mnemonic in ("lea", "mov") and x.address + x.size == T0 + i + 4 \
                and any(op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip" for op in x.operands):
            taken.append("%08X" % x.address)
wabs = [nm for nm in (".rdata", ".data") for w in writers if d[secs[nm][3]:secs[nm][3] + secs[nm][2]].find(struct.pack("<Q", w)) != -1]
check("Q2 the writers run only inside lifecycle callbacks (%d calling functions)" % len(C),
      bad == [] and direct_bad == [] and extra == [] and taken == [] and wabs == [],
      "not-from-callbacks %s; callbacks with outside callers %s; extra table refs %s; writers address-taken %s %s"
      % (["%08X" % g for g in bad], ["%08X" % f for f in direct_bad], ["%08X" % f for f in extra], taken[:3], wabs))
# Q3
cb11 = [("%08X" % f, "%08X" % x.address) for f in K for x in body(f) if is_bw(x, 0x11)]
ctrl11 = [x.address for x in body(0x3DBDC0) if is_bw(x, 0x11)]
check("Q3 no callback writes the current-slot byte b[0x11]; control: the matcher finds the one writer, 003DBDC0 (not a callback)",
      cb11 == [] and ctrl11 != [] and 0x3DBDC0 not in K, "callback writes %s; control %s" % (cb11[:3], ["%08X" % a for a in ctrl11]))
# Q4
X = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body(0x2621D0)}
check("Q4 controls: the executor writes 1 at 0026230B and 0 at 00262382",
      X.get(0x26230B) == "mov byte ptr [rdi + 0x15], 1" and X.get(0x262382) == "mov byte ptr [rdi + 0x15], 0")
print("FAILS", fails)
sys.exit(1 if fails else 0)
