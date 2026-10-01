"""basedisp.py - memory operands whose displacement, taken as absolute or as image-base-relative (RVA), falls in
[lo, hi) (ORACLE, 2026-09-30, RC-11). Catches the image-base-indexed form [rX + rY*s + rva] that a rip-relative census
misses. Usage: python basedisp.py <lo_hex> <hi_hex>
Positive control, always run: the selection push's map read 0036C272 ([rax + rbx + 0x21b89a8], rbx = the image base,
so 022D89A8) must be found."""
import sys
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
import img
lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
n = 0
ctl = False
for b, e, _u in img.PDATA:
    for x in img.dis(b, e - b):
        for i, o in enumerate(x.operands):
            if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP:
                d = o.mem.disp & 0xFFFFFFFF
                for t, kind in ((d, "abs"), (d + img.BASE, "rva")):
                    if x.address == 0x0036C272 and t == 0x022D89A8 and kind == "rva":
                        ctl = True
                    if lo <= t < hi and d > 0x10000:
                        n += 1
                        print("%08X  %08X  %s  %-6s %-44s -> %08X" % (img.owner(x.address) or 0, x.address, kind,
                                                                     x.mnemonic, x.op_str, t))
print("%s  control: 0036C272 reads the map 022D89A8 image-base-indexed" % ("PASS" if ctl else "FAIL"))
print("hits: %d" % n)
sys.exit(0 if ctl else 1)
