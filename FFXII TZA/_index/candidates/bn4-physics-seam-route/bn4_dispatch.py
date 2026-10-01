"""BN-4 part 2: who dispatches a class descriptor's +0x70 hook on an instance, and which instances reach it (OPUS, 2026-09-27).

The seam 006883A0 is PPhysicsWorld's descriptor slot +0x70 (part 1, bn4_seam_route.py). This reads the dispatchers:
  D1 0059E300 (called only by the cluster loader 0059E070), after the fixup passes, walks the loaded objects and calls
     [[obj+0x50]] +0x70 ONLY when obj+0x50 is 02D3E680 (PAssetReference) or 02CF8580 (0059E574-0059E585).
  D2 0063B040 (wrapped by 0063B010) walks each node's +0x38 object chain and calls [[obj+0x50]] +0x70 for EVERY object
     whose +0x50 is not one of the three sentinels 02D3E680 / 02D3E780 / 02CF8580 (0063B382-0063B39B), then sets bit 1
     of +0x80 so the pass runs once.
  D3 0063AFF0 is a descriptor method that forwards +0x70 to the base-class descriptor (+0x78).
  D4 census: every indirect call or jump through [reg+0x70] in 00580000-00700000 (the Phyre reflection, serialisation
     and rendering bodies) - 22 sites; D1-D3 are the three whose receiver is a class descriptor (loaded from an object's
     +0x50 or a descriptor's +0x78); the other 19 load their receiver from renderer/object fields.
  D5 btRigidBody's vtable (RTTI) is written by exactly four functions: 00852DB0 (called only by the seam builder
     0069FB10), 00852E10 (called only by 00859D20, every caller chain of which roots at the solver virtual 0085CED0
     btSequentialImpulseConstraintSolver::solveGroup - Bullet's internal fixed body), and the destructor pair
     00852FD0 / 008B90A0.
  D6 btDiscreteDynamicsWorld's constructor 00854980 is called only by 006A0310, whose callers are 00698C80 (the seam's
     per-instance walk) and 0069F070 (the seam chain) - so no dynamics world, and hence no solver step, exists
     without a PPhysicsWorld instance.
So a PPhysicsWorld reaches its hook only as an object of a loaded cluster (D2), and part 1 plus the 2026-09-22 corpus
census found none in any shipped .phyre.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]


def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True


def body(a, size):
    return list(cs.disasm(d[off(a):off(a) + size], a))


def rip(i, k=1):
    o = i.operands[k]
    return i.address + i.size + o.value.mem.disp if o.type == X86_OP_MEM and o.value.mem.base == X86_REG_RIP else None


fails = 0


def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)


b1 = {i.address: i for i in body(0x0059E300, 1141)}
check("D1 0059E300 dispatches +0x70 only for 02D3E680 / 02CF8580",
      rip(b1[0x0059E551]) == 0x02CF8580 and rip(b1[0x0059E561]) == 0x02D3E680
      and b1[0x0059E574].op_str == "rcx, qword ptr [rdx + 0x50]" and b1[0x0059E585].op_str == "qword ptr [rax + 0x70]"
      and b1[0x0059E580].mnemonic == "jne")
b2 = {i.address: i for i in body(0x0063B040, 916)}
check("D2 0063B040 dispatches +0x70 for every object except three sentinel descriptors",
      rip(b2[0x0063B374]) == 0x02D3E680 and rip(b2[0x0063B34F]) == 0x02D3E780 and rip(b2[0x0063B37B]) == 0x02CF8580
      and b2[0x0063B382].op_str == "rcx, qword ptr [rbx + 0x50]" and b2[0x0063B39B].op_str == "qword ptr [rax + 0x70]")
b3 = body(0x0063AFF0, 16)
check("D3 0063AFF0 forwards +0x70 to the base descriptor (+0x78)",
      b3[0].op_str == "rcx, qword ptr [rcx + 0x78]" and b3[4].mnemonic == "jmp" and b3[4].op_str == "qword ptr [rax + 0x70]")
funcs = []
allf = []
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = line.split("\t")
    try:
        e, sz = int(c[0], 16), int(c[2])
    except (ValueError, IndexError):
        continue
    if 0 < sz <= 0x20000 and off(e) is not None:
        allf.append((e, sz))
    if 0x00580000 <= e < 0x00700000 and 0 < sz <= 0x20000:
        funcs.append((e, sz))
sites = []
for e, sz in funcs:
    for i in body(e, sz):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_MEM \
                and i.operands[0].value.mem.disp == 0x70 and i.operands[0].value.mem.base != X86_REG_RIP:
            sites.append(i.address)
check("D4 22 [reg+0x70] dispatch sites in 00580000-00700000, including the three above",
      len(sites) == 22 and {0x0059E585, 0x0063B39B, 0x0063AFFC} <= set(sites), "(%d)" % len(sites))
calls = {}
for e, sz in [(e, sz) for e, sz in allf]:
    for i in body(e, sz):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == 2:
            calls.setdefault(i.operands[0].imm, set()).add(e)
def vt_writers(vt):
    out = set()
    for e, sz in allf:
        for i in body(e, sz):
            for k, o in enumerate(i.operands):
                if o.type == X86_OP_MEM and o.value.mem.base == X86_REG_RIP and i.address + i.size + o.value.mem.disp == vt:
                    out.add(e)
    return out
def roots(f, seen=frozenset()):
    cs = calls.get(f, set()) - {f}
    if not cs:
        return {f}
    r = set()
    for c in cs - seen:
        r |= roots(c, seen | {f})
    return r
w = vt_writers(0x01CCF348)
check("D5 btRigidBody vtable writers and their callers",
      w == {0x00852DB0, 0x00852E10, 0x00852FD0, 0x008B90A0} and calls.get(0x00852DB0) == {0x0069FB10}
      and calls.get(0x00852E10) == {0x00859D20} and roots(0x00859D20) == {0x0085CED0} and 0x0085CED0 not in calls,
      " ".join("%08X" % x for x in sorted(w)) + " | " + " ".join("%08X<-%s" % (a, sorted("%08X" % x for x in calls.get(a, ())))
      for a in (0x00852DB0, 0x00852E10, 0x00859D20, 0x0085CED0)))
check("D6 btDiscreteDynamicsWorld ctor 00854980 <- 006A0310 <- {00698C80, 0069F070}",
      calls.get(0x00854980) == {0x006A0310} and calls.get(0x006A0310) == {0x00698C80, 0x0069F070})
print("FAILS", fails)
sys.exit(1 if fails else 0)
