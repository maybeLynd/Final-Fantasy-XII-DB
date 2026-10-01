"""UQ-353 probe (OPUS, 2026-09-26): run the box cell drawer 002DC7F0 and capture what it hands to 00181460.

002DC7F0(rcx, matrix=rdx, colours=r8, x=r9d, [y, w, h, flags] on the stack) projects its two corners through 00202B70,
builds four 0x30-byte vertices on its stack and calls 00181460(vertices, 4). 00181460 is a RECORDED STOP BOUNDARY
(discarded from the allowed set): the run stops at its entry with rcx/rdx intact, and the vertex array is read there.
Nothing is stubbed. Exploratory: prints each case so check.py can assert on what is seen.
"""
import json
import os
import struct
import sys

from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
CELL, EMIT = 0x2DC7F0, 0x181460
W.ALLOWED |= W.closure(CELL)
W.ALLOWED.discard(EMIT)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
MAT, COL = 0x76280000, 0x76281000
ident = struct.pack("<16f", 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
uc.mem_write(MAT, ident)
uc.mem_write(COL, struct.pack("<4I", 0x44332211, 0x88776655, 0xCCBBAA99, 0x10FFEEDD))


def run(x, y, w, h, flags):
    ok = S.call(CELL, 0, MAT, COL, x, stack=(y, w, h, flags))
    stop = S.st["bad"][:1]
    out = {"returned": ok, "stop": stop, "faults": S.st["faults"][:1]}
    if stop == ["%08X" % EMIT]:
        va, n = uc.reg_read(UC_X86_REG_RCX), uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
        raw = bytes(uc.mem_read(va, 0x30 * n))
        out["count"] = n
        out["vertices"] = []
        for i in range(n):
            v = raw[0x30 * i:0x30 * (i + 1)]
            f = struct.unpack_from("<4f", v, 0)
            c = struct.unpack_from("<4I", v, 0x10)
            uv = struct.unpack_from("<2f", v, 0x20)
            fl, pad = struct.unpack_from("<2I", v, 0x28)
            out["vertices"].append({"xyzw": f, "rgba": ["%X" % q for q in c], "uv": uv, "flags": "%X" % fl, "pad2C": "%08X" % pad})
    return out


if __name__ == "__main__":  # exploratory listing
    for flags in (0, 4, 8, 0xC, 0x10):
        print(flags, json.dumps(run(100, 50, 20, 30, flags)))
