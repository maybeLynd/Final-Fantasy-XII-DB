"""probe3.py - FABLE scratch: for each function holding a qword store at +0x6F0, which battle-unit hallmark
displacements (+0x698 stats, +0x714 order id, +0x6B4 dispatch byte, +0xEA9 lane, +0x708 context) it also uses."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rawref import Img, disp_sweep, decode_fn  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402

img = Img.load()
HALL = {0x698, 0x714, 0x6B4, 0xEA9, 0x708, 0xE60, 0x6E8, 0x6F8, 0x748}
seen = set()
for r in disp_sweep(img, 0x6F0, 8):
    if not (r[3] & 2) or r[4] is None or r[4] in seen:
        continue
    seen.add(r[4])
    pd, ins = decode_fn(img, r[0])
    hits = set()
    for ci in ins.values():
        for op in ci.operands:
            if op.type == X86_OP_MEM and op.mem.disp in HALL and op.mem.base != 0:
                hits.add(op.mem.disp)
    print("%08X fn=%08X..%08X size=%d store %s; hallmarks %s" % (r[0], pd[0], pd[1], pd[1] - pd[0], r[1],
                                                              sorted("+0x%X" % h for h in hits)))
