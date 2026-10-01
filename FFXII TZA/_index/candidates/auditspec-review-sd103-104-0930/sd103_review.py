"""SWE2-AUDIT-SPEC independent read for SD-103/104 (2026-09-30), from the bytes, not from pinned text.
R1 002B3480: the two builder loops - context global, row stride, row bias, loop bounds, the call after them.
R2 002B5C90: every load of [reg+0x1060/0x1078/0x1090].
R3 002432B0: the stores to the row (+0x00 / +0x08 / +0x10) and the count mask.
R4 arithmetic: 24*row+0x10 for rows 42, 174..176, and rows that fit below +0x10C8.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
def rip_target(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and x.reg_name(op.mem.base) == "rip":
            return x.address + x.size + op.mem.disp
    return None
print("R1 002B3480 (%s bytes)" % tk.fsize(0x002B3480))
for x in tk.fdis(0x002B3480):
    t = rip_target(x)
    if x.mnemonic in ("call", "cmp", "add") or t or "rax*2" in x.op_str:
        print("   %08X %s %s%s" % (x.address, x.mnemonic, x.op_str, "   ; global %08X" % t if t else ""))
print("R2 002B5C90 slot loads:")
for x in tk.fdis(0x002B5C90):
    if any(("0x%x]" % v) in x.op_str for v in (0x1060, 0x1078, 0x1090)):
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R3 002432B0 row stores / count:")
for x in tk.fdis(0x002432B0):
    if "[r15" in x.op_str and x.op_str.split(",")[0].find("[r15") >= 0 or "0x3ff" in x.op_str or "0x1c" in x.op_str:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R4 rows: 42 -> +0x%X; 174..176 -> %s; rows below 0x10C8: %d" % (
    24 * 42 + 0x10, ", ".join("+0x%X" % (24 * r + 0x10) for r in (174, 175, 176)), 0x10C8 // 24))
