"""dis.py - FABLE, 2026-10-03: print a whole .pdata function (or [va, va+n)) with rip targets resolved."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

img = Img.load()
va = int(sys.argv[1], 16)
if len(sys.argv) > 2:
    s, e = va, va + int(sys.argv[2], 16)
else:
    s, e = img.pdata(va)
print("; %08X..%08X (%d B)" % (s, e, e - s))
for ci in img.cs.disasm(img.read(s, e - s), s):
    extra = ""
    for op in ci.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            extra = "  ; [%08X]" % (ci.address + ci.size + op.mem.disp)
    print("%08X  %-40s %s%s" % (ci.address, ci.bytes.hex(), (ci.mnemonic + " " + ci.op_str), extra))
