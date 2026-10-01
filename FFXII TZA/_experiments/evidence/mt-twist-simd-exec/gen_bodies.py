#!/usr/bin/env python
"""Measure the real-body span for EXP-111 bodies.json.

00866B90 is a self-contained leaf (no calls, no out-of-body jumps):
linear disasm entry -> ret gives the full span.
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

va = check.TWIST
insns = 0
while True:
    b = img(va, 16)
    ins = next(md.disasm(b, va, count=1), None)
    if ins is None:
        break
    insns += 1
    va = ins.address + ins.size
    if ins.mnemonic == "ret":
        break

span = va - check.TWIST
h = hashlib.sha256(img(check.TWIST, span)).hexdigest()
out = {"real": [{
    "name": "twist", "va": "0x%x" % check.TWIST,
    "lo": "0x%x" % check.TWIST, "hi": "0x%x" % va,
    "span": span, "insns": insns, "cov": 1.0,
    "sha256": h, "indirect": []}],
    "scripted": []}

json.dump(out, open("bodies.json", "w"), indent=1)
print("twist %s span=%d insns=%d" % ("0x%x" % check.TWIST, span, insns))
print("sha256 %s" % h)
