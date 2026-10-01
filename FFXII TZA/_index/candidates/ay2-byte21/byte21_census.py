"""byte21_census.py - AY-2: a second, independent instrument for the action row's +0x21 (FABLE, Claude Opus 5.5, 2026-09-26).

The hop census (07-Combat-Action/Action-Definition-Row/members/action_row_reader_hops.py) follows the row pointer from
the registry-slot idiom through two call levels and finds no reader of +0x21. This instrument does not follow pointers.
It takes every function that references the action table's registry slot 02EBF138 (rip-relative) and lists every
operand at displacement 0x1F / 0x20 / 0x21 of width <= 4 on a non-stack base.
  C1 the population is the slot's referencing functions (printed count).
  C2 sensitivity: the sweep sees byte accesses at +0x20 in these bodies, so a +0x21 read would be visible the same way.
  C3 every +0x21 operand in the population is a STORE, and each stores a byte loaded from another record: 0031C5D0
     copies [rdi+5] (0031E09A) and [rbp+0x26] (0031E233) into its query record's +0x21. None reads the action row.
Scope: a +0x21 read in a function that neither references 02EBF138 nor is reached by the hop census is not seen.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
SLOT = 0x2EBF138
pop, acc = [], []
for a, sz in F.items():
    o = off(a)
    if o is None or sz <= 0: continue
    L = list(cs.disasm(d[o:o + sz], a))
    if not any(op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip" and x.address + x.size + op.mem.disp in (SLOT, SLOT + 4)
               for x in L for op in x.operands):
        continue
    pop.append(a)
    for x in L:
        for k, op in enumerate(x.operands):
            if op.type == X86_OP_MEM and op.mem.disp in (0x1F, 0x20, 0x21) and op.size <= 4 \
                    and cs.reg_name(op.mem.base) not in ("rip", "rsp", "rbp"):
                acc.append((x.address, op.mem.disp, k, "%s %s" % (x.mnemonic, x.op_str)))
check("C1 population: functions referencing 02EBF138", len(pop) > 100, str(len(pop)))
check("C2 sensitivity: +0x20 byte accesses are seen", sum(1 for a in acc if a[1] == 0x20) > 0,
      str(sum(1 for a in acc if a[1] == 0x20)))
b21 = [a for a in acc if a[1] == 0x21]
print("  +0x21 operands:", ["%08X %s" % (a[0], a[3]) for a in b21])
S = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x31E090):off(0x31E090) + 0x1B0], 0x31E090)}
check("C3 every +0x21 operand is a store, copying from another record",
      b21 != [] and all(a[2] == 0 and a[3].startswith("mov byte ptr [") for a in b21)
      and S.get(0x31E09A) == "movzx eax, byte ptr [rdi + 5]" and S.get(0x31E233) == "movzx eax, byte ptr [rbp + 0x26]")
print("FAILS", fails)
sys.exit(1 if fails else 0)
