"""w2_table.py - SWE2-AUDIT-SPEC: the second holder of the slot-header table.
00582860 creates a 0xF0-byte widget with handler 0057F360 (lea 00582E0D, factory call 00582E46, stored at
[ctrl+0xF8] 00582E52), whose create parameter +0x10 is [ctrl+0x590] (00582E27/00582E2E), the same pointer 00583040 gives
the save menu as [widget+0x1C0]. 0057F360 stores it at [W2+0xD8] (0057F5B2/0057F5B9).
This lists, in 0057F360 and every function it reaches by direct call (depth 3), plus every save-module function
(0057C000-00586000), each 8-byte load of [reg+0xD8] and follows the loaded register linearly (to its first
redefinition) for memory accesses through it, with displacement, width, and displacement mod 0xA0. A hit on field
+0x48, +0x4C, +0x58 or +0x60 (mod 0xA0) is flagged FIELD.
Linear, not flow-aware: it can miss an access after a join and it over-reports [reg+0xD8] loads of other objects.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
import capstone
SEED = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0xD8
ALL = len(sys.argv) > 2 and sys.argv[2] == "all"
FIELDS = {0x48, 0x4C, 0x58, 0x60}
def fam(r):
    r = r or ""
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
    return m.get(r, r[:-1] if r.endswith("d") and r.startswith("r") else r)
def callees(f):
    out = set()
    if not tk.fsize(f): return out
    for i in tk.fdis(f):
        if i.mnemonic in ("call", "jmp") and i.operands[0].type == X86_OP_IMM:
            t = i.operands[0].imm
            if tk.fsize(t): out.add(t)
    return out
seen = {0x0057F360}; frontier = [0x0057F360]
for depth in range(3):
    nxt = []
    for f in frontier:
        for t in callees(f):
            if t not in seen: seen.add(t); nxt.append(t)
    frontier = nxt
mod = set(e for e, s in tk.flist if 0x0057C000 <= e < 0x00586000)
fns = sorted(seen | mod)
print("functions scanned: %d (closure of 0057F360 depth 3: %d, save module: %d)" % (len(fns), len(seen), len(mod)))
nload = 0; flagged = []
for f in fns:
    body = tk.fdis(f)
    for n, x in enumerate(body):
        if not (x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_MEM
                and x.operands[1].size == 8 and x.operands[1].mem.disp == SEED and tk.md.reg_name(x.operands[1].mem.base) != "rip"):
            continue
        nload += 1
        taint = {fam(tk.md.reg_name(x.operands[0].reg))}
        for y in body[n + 1: n + 80]:
            for op in y.operands:
                if op.type == X86_OP_MEM and taint & {fam(tk.md.reg_name(op.mem.base)), fam(tk.md.reg_name(op.mem.index))}:
                    dm = op.mem.disp % 0xA0
                    if (ALL or dm in FIELDS) and y.mnemonic != "lea":
                        flagged.append("%08X %s %s  (disp %#x, mod A0 %#x, w%d) after load %08X in %s" % (
                            y.address, y.mnemonic, y.op_str, op.mem.disp, dm, op.size, x.address, tk.fname(x.address)))
            if y.mnemonic.startswith("ret") or y.mnemonic == "jmp" or not taint: break
            try: r, w = y.regs_access()
            except capstone.CsError: r, w = [], []
            rd = {fam(tk.md.reg_name(a)) for a in r}; wr = {fam(tk.md.reg_name(a)) for a in w}
            # a pointer-arithmetic write that reads a tainted register keeps/extends the taint (add/lea/mov/imul);
            # a load THROUGH a tainted pointer produces a value, not the table pointer
            derives = y.mnemonic in ("mov", "lea", "add", "sub", "movsxd") and (rd & taint) and not (
                y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[1].type == X86_OP_MEM)
            if y.mnemonic == "call":
                taint -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
            elif derives:
                taint |= (wr - {"rflags"})
            else:
                taint -= wr
print("seed disp %#x, all=%s; 8-byte [reg+seed] loads followed: %d" % (SEED, ALL, nload))
print("FIELD hits (+0x48/+0x4C/+0x58/+0x60 mod 0xA0) through a loaded [reg+0xD8]: %d" % len(flagged))
for s in flagged: print("  " + s)
