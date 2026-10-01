"""gr11_pose_readers.py - GR-11's second question (FABLE, 2026-09-30): who reads camera-context bytes +0x710..+0x79F
(the part of the +0x6F0 pose block that 0025A180's final copy fills from unwritten local space).
Method, image-wide over .text (functions from .pdata, chained unwind fragments folded to their primary):
  (1) every rip-relative operand whose target lies in 02097D20 + k*0x860 + [0x6F0, 0x7A0) for k = 0..7 (direct cells);
  (2) every function that forms the base 02097D20 (rip-relative lea/mov of 02097D20..02097D20+8*0x860), and in those
      functions every memory operand with a displacement in [0x6F0, 0x7A0) - reads and writes listed separately, with
      access width.
Positive control: 0025A180 must be found forming the base and writing +0x6F0 (its final copy, 0025A792-0025A7F9).
This lists CANDIDATES. A register holding a context pointer handed in from another function is not followed."""
import os, struct, sys
import capstone
from capstone import x86
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
BASE, CTX, STRIDE, NCTX = 0x120000, 0x02097D20, 0x860, 8
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; o = struct.unpack_from("<H", d, pe + 20)[0]
S = {}
for i in range(n):
    s = pe + 24 + o + 40 * i
    S[d[s:s + 8].rstrip(b"\0").decode()] = struct.unpack_from("<IIII", d, s + 8)
def off(a):
    r = a - BASE
    for vsz, va, rsz, raw in S.values():
        if va <= r < va + max(vsz, rsz): return raw + r - va
vsz, va, rsz, raw = S[".pdata"]
funcs = []
for k in range(vsz // 12):
    b, e, u = struct.unpack_from("<III", d, raw + 12 * k)
    if b == 0: break
    funcs.append((b + BASE, e + BASE))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
lo_c, hi_c = CTX, CTX + NCTX * STRIDE
direct, bases, acc = [], set(), []
for b, e in funcs:
    code = d[off(b):off(b) + (e - b)]
    insl = list(md.disasm(code, b))
    forms = False
    for i in insl:
        for op in i.operands:
            if op.type == x86.X86_OP_MEM and op.mem.base == x86.X86_REG_RIP:
                t = i.address + i.size + op.mem.disp
                if lo_c <= t < hi_c:
                    rel = (t - CTX) % STRIDE
                    if i.mnemonic == "lea" and rel == 0: forms = True
                    if 0x6F0 <= rel < 0x7A0: direct.append("%08X %s %s (ctx %d +%#x)" % (i.address, i.mnemonic, i.op_str, (t - CTX) // STRIDE, rel))
    if forms:
        bases.add(b)
        for i in insl:
            for op in i.operands:
                if op.type == x86.X86_OP_MEM and op.mem.base not in (x86.X86_REG_RIP, x86.X86_REG_RSP) and 0x6F0 <= op.mem.disp < 0x7A0:
                    _, w = i.regs_access()
                    kind = "W" if (i.operands[0].type == x86.X86_OP_MEM and i.mnemonic.startswith(("mov", "stos"))) else "R"
                    acc.append((b, "%08X %s %-4s %s %s" % (i.address, kind, op.size, i.mnemonic, i.op_str)))
print("functions forming the context base 02097D20: %d" % len(bases))
print("control: 0025A180 forms the base:", 0x25A180 in bases)
print("direct rip-relative cells in +0x6F0..+0x79F: %d" % len(direct))
for x in direct: print("  " + x)
print("in-window accesses in base-forming functions: %d" % len(acc))
for b, x in acc:
    print("  fn %08X  %s" % (b, x))
