"""probe1.py - FABLE, 2026-10-03: raw index survey for the S-21 poster / realiser (scratch; the check re-derives)."""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, fmt_ref  # noqa: E402

img = Img.load()
for name, lo, hi in [("poster 0046AB10", 0x0046AB10, 0x0046AB11), ("realiser 005369C0", 0x005369C0, 0x005369C1),
                     ("filter 00469570", 0x00469570, 0x00469571), ("dispatcher 00469EC0", 0x00469EC0, 0x00469EC1),
                     ("gate 00385BA0", 0x00385BA0, 0x00385BA1),
                     ("ring 02EBB560..02EBB6A0", 0x02EBB560, 0x02EBB6A0), ("ring index 02EBB54C", 0x02EBB54C, 0x02EBB550),
                     ("steal list 02EBB540..02EBB54C", 0x02EBB540, 0x02EBB54C), ("02EBB550..02EBB560", 0x02EBB550, 0x02EBB560),
                     ("0035B990", 0x0035B990, 0x0035B991), ("00536410", 0x00536410, 0x00536411)]:
    refs, unc = text_refs(img, lo, hi)
    print("== %s: %d refs, %d unconfirmed, data consts %s" % (name, len(refs), len(unc), data_refs(img, lo, hi)))
    fns = Counter(r["func"] for r in refs)
    print("   functions: %d %s" % (len(fns), sorted("%08X:%d" % (f or 0, n) for f, n in fns.items())))
    if len(refs) < 70:
        for r in refs:
            print("   " + fmt_ref(r))
