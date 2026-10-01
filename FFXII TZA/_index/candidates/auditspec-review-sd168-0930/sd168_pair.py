"""sd168_pair.py - SWE2-AUDIT-SPEC (2026-09-30): SD-168 re-derived with arena_ix only.
  P1 pair each 0036D240 allocation in 0022A0B0 with the global its result is stored to, and each 00369D30 call with the
     global its rdx is loaded from, so backing <-> (arena, size, count) is exact, not set membership.
  P2 every other caller of 00369D30: what it allocates and what (size, count) it initialises with.
  P3 the initializer's layout end and the initial free block (0036A490) - printed instruction texts.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-sd164-167-0930"))
import arena_ix as X  # noqa: E402
from capstone import CS_OP_MEM
from capstone.x86 import X86_REG_RIP

ins = X.dis(0x0022A0B0, 0x0022A480)


def rip_t(i):
    for op in i.operands:
        if op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


alloc = {}   # global -> size
pend = None
for k, i in enumerate(ins):
    if i.mnemonic == "mov" and i.op_str.startswith("ecx, 0x"):
        pend = int(i.op_str.split(", ")[1], 16)
    if i.mnemonic == "call" and i.op_str == "0x36d240":
        for j in ins[k + 1:k + 6]:
            if j.mnemonic == "mov" and j.op_str.startswith("qword ptr [rip") and j.op_str.endswith(", rax"):
                alloc[rip_t(j)] = pend
                break
inits = []
st = {}
for k, i in enumerate(ins):
    if i.mnemonic == "mov" and i.op_str.startswith("rdx, qword ptr [rip"):
        st["g"] = rip_t(i)
    if i.mnemonic == "mov" and i.op_str.startswith("r9d, "):
        st["n"] = int(i.op_str.split(", ")[1], 0)
    if i.mnemonic == "mov" and i.op_str.startswith("r8d, "):
        st["s"] = int(i.op_str.split(", ")[1], 0)
    if i.mnemonic == "mov" and i.op_str.startswith("ecx, ") and not i.op_str.startswith("ecx, dword"):
        st["a"] = int(i.op_str.split(", ")[1], 0)
    if i.mnemonic == "lea" and i.op_str.startswith("ecx, [r9 - "):
        st["a"] = st["n"] - int(i.op_str.split(" - ")[1].rstrip("]"), 0)
    if i.mnemonic == "call" and i.op_str == "0x369d30":
        inits.append((i.address, st.get("a"), st.get("g"), st.get("s"), st.get("n")))
print("P1 0022A0B0: %d allocations stored to globals, %d initializer calls" % (len(alloc), len(inits)))
ok = 0
for a, h, g, s, n in inits:
    b = alloc.get(g)
    m = b == s + n
    ok += m
    print("   %08X heap %#x  rdx=[%08X] = alloc(%#x)  size %#x  count %#x  alloc == size + count: %s" % (a, h, g, b, s, n, m))
print("   exact pairs: %d of %d; allocations not used as a backing here: %s" % (
    ok, len(inits), ["%#x -> [%08X]" % (v, k) for k, v in alloc.items() if k not in {x[2] for x in inits}]))

print("P2 other callers of 00369D30:")
for s, k in sorted(X.rel32([0x00369D30])[0x00369D30]):
    if X.root(s) == 0x0022A0B0:
        continue
    r = X.root(s)
    for i in X.dis(r, s + 5)[-14:]:
        if i.mnemonic in ("call", "jmp") or i.op_str.startswith(("ecx", "r8d", "r9d", "rdx")):
            print("   %08X %08X %s %s" % (r, i.address, i.mnemonic, i.op_str))
    print("   --")

print("P3 initializer layout end and the initial free block:")
for a in (0x00369E73, 0x00369E77, 0x00369E7E, 0x00369E86, 0x00369E8A, 0x00369E91, 0x00369E95, 0x00369E99, 0x00369EA1,
          0x00369EA4, 0x00369EAC, 0x00369EB3, 0x00369EB7, 0x00369EBB, 0x00369EBE, 0x00369EC2, 0x00369EC6, 0x00369F5D,
          0x00369F65, 0x00369F6C, 0x00369F74, 0x00369F85, 0x00369F88, 0x00369FC7, 0x00369FD0, 0x00369FD4,
          0x0036A4B9, 0x0036A50F, 0x0036A554):
    print("   %08X %s" % (a, X.txt(a)))
