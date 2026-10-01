#!/usr/bin/env python
"""Measure the real-body spans for EXP-112 bodies.json.

Bodies are walked linearly from entry until the first `ret`, or until a
direct `jmp` whose target leaves the body window (tail-call, e.g. the
ctor's `jmp 003DB280`). Jump-table bodies (RMAP/KINIT) keep their arms
inside the linear span; the jt data after `ret` is excluded.
"""
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

import check

raw, secs = check.load_image()


def img(va, n):
    rva = va - check.IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + vs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("va %x not in image" % va)


md = Cs(CS_ARCH_X86, CS_MODE_64)


def measure(name, va0, hi=None):
    va, insns = va0, 0
    while True:
        ins = next(md.disasm(img(va, 16), va, count=1), None)
        if ins is None:
            break
        insns += 1
        va = ins.address + ins.size
        if hi is not None:
            if va >= hi:
                break
            continue
        if ins.mnemonic == "ret":
            break
        if ins.mnemonic == "jmp" and ins.op_str.startswith("0x"):
            tgt = int(ins.op_str, 16)
            if not (va0 <= tgt < va0 + 0x2000):
                break           # tail-call jmp -> end of body
    span = va - va0
    h = hashlib.sha256(img(va0, span)).hexdigest()
    return {"name": name, "va": "0x%x" % va0,
            "lo": "0x%x" % va0, "hi": "0x%x" % va,
            "span": span, "insns": insns, "cov": 1.0,
            "sha256": h, "indirect": []}


# kinit's five arm bodies each end in ret; the true body runs to the
# last arm's ret at 0x266C2E (jt data starts at 0x266C30).
BODIES = [("ctor", check.CTOR, None), ("rmap", check.RMAP, None),
          ("kinit", check.KINIT, 0x266C2F), ("sinit", check.SINIT, None),
          ("tail", check.TAIL, None), ("qwalk", check.QWALK, None),
          ("base", check.BASE, None)]
SCRIPTED = [("cff0", check.CFF0), ("cb60", check.CB60),
            ("c380", check.C380), ("c1e0", check.C1E0),
            ("dbb60", check.DBB60), ("c8ea0", check.C8EA0),
            ("cdc0", check.CDC0)]

out = {"real": [measure(n, v, h) for n, v, h in BODIES],
       "scripted": [{"name": n, "va": "0x%x" % v}
                    for n, v in SCRIPTED]}
json.dump(out, open("bodies.json", "w"), indent=1)
for b in out["real"]:
    print("%s %s span=%d insns=%d" % (b["name"], b["va"], b["span"],
                                    b["insns"]))
print("scripted: %d" % len(out["scripted"]))
