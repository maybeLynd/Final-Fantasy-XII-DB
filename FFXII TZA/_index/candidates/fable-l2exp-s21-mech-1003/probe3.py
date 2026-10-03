"""probe3.py - FABLE, 2026-10-03: the instruction that sets edx (the event id) before each poster site."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, decode_fn  # noqa: E402

img = Img.load()
refs, _ = text_refs(img, 0x0046AB10)
for r in refs:
    s = r["site"]
    pd, ins = decode_fn(img, s)
    seq = [ins[a] for a in sorted(ins) if a < s]
    for ci in reversed(seq):
        _, w = ci.regs_access()
        names = set(ci.reg_name(x) for x in w)
        if names & {"edx", "rdx", "dx", "dl"}:
            print("%08X fn=%08X  edx <- %08X %s %s" % (s, r["func"], ci.address, ci.mnemonic, ci.op_str))
            break
    else:
        print("%08X no edx write in fragment" % s)
