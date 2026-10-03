"""probe2.py - FABLE, 2026-10-03: return-value use at the 48 poster sites; ctx +0x2C at each site; 02089340 writers."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, decode_fn  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP  # noqa: E402

img = Img.load()
RAX = {"rax", "eax", "ax", "al", "ah"}


def regs(ci):
    r, w = ci.regs_access()
    return set(ci.reg_name(x) for x in r), set(ci.reg_name(x) for x in w)


refs, _ = text_refs(img, 0x0046AB10)
print("== return value after each of the %d sites" % len(refs))
for r in refs:
    s = r["site"]
    used = "unused"
    for ci in img.cs.disasm(img.read(s + 5, 64), s + 5):
        rd, wr = regs(ci)
        if ci.mnemonic.startswith("j") or ci.mnemonic in ("ret", "call"):
            if ci.mnemonic == "ret":
                used = "RET-PASSES-RAX? (%08X ret)" % ci.address
            elif ci.mnemonic == "call":
                used = "unused (next call %08X)" % ci.address
            else:
                used = "branch %08X %s %s before any rax access" % (ci.address, ci.mnemonic, ci.op_str)
            break
        if rd & RAX and not (ci.mnemonic == "xor" and ci.op_str.split(",")[0].strip() == ci.op_str.split(",")[-1].strip()):
            used = "READ at %08X %s %s" % (ci.address, ci.mnemonic, ci.op_str)
            break
        if wr & RAX:
            used = "overwritten at %08X %s %s" % (ci.address, ci.mnemonic, ci.op_str)
            break
    print("  %08X fn=%08X  %s" % (s, r["func"], used))

print("== the r8 context at each site and stores at ctx+0x2C..+0x2F in the function")
for r in refs:
    s = r["site"]
    pd, ins = decode_fn(img, s)
    seq = [ins[a] for a in sorted(ins) if a < s]
    ctx = None
    for ci in reversed(seq):
        if ci.mnemonic in ("lea", "mov") and ci.op_str.startswith("r8,"):
            ctx = ci
            break
    if ctx is None or ctx.mnemonic != "lea":
        print("  %08X ctx: %s" % (s, (ctx.mnemonic + " " + ctx.op_str) if ctx else None))
        continue
    m = [op for op in ctx.operands if op.type == X86_OP_MEM][0].mem
    base, disp = ctx.reg_name(m.base), m.disp
    hits = []
    for a in sorted(ins):
        ci = ins[a]
        for op in ci.operands:
            if op.type == X86_OP_MEM and ci.reg_name(op.mem.base) == base and op.access & 2:
                lo, hi = op.mem.disp, op.mem.disp + op.size
                if lo < disp + 0x30 and hi > disp + 0x2C:
                    hits.append("%08X %s %s" % (a, ci.mnemonic, ci.op_str))
    print("  %08X fn=%08X ctx=[%s%+#x] (%08X)  writes over +0x2C: %s" % (s, r["func"], base, disp, ctx.address, hits))

print("== 02089340..02089344 writers")
refs, _ = text_refs(img, 0x02089340, 0x02089344)
for r in refs:
    ci = next(img.cs.disasm(img.read(r["site"], 16), r["site"], 1))
    op0 = ci.operands[0]
    if op0.type == X86_OP_MEM and ci.mnemonic not in ("cmp", "test", "bt"):
        print("  %08X fn=%s %s %s" % (r["site"], "%08X" % r["func"] if r["func"] else "-", ci.mnemonic, ci.op_str))
print("  total refs %d" % len(refs))
