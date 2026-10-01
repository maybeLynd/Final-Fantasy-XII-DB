"""sd106_callers.py - SWE2-AUDIT-SPEC: every way code reaches 002B3280 (and the thunk 002B32C0), image-wide, with the
lane's ov31_indep helpers: E8/E9 (rel32_callers), jcc (jcc_callers), stored abs64 / rva32 (data_refs), rip-relative
lea/mov (rip_refs) and image-base-relative disp32 (imagebase_refs).
Control: 002B32D0 must show its two known rel32 sites 002B32B6 / 002B32C0 (the raw index's count).
Also prints the static values of 01E0C1D8, 01E0C1DC, 01E0C0D4, 01E0CDC0.
"""
import json, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

RC = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
for t in (0x002B3280, 0x002B32C0, 0x002B32D0):
    print("%08X  rel32 %s (index %d)" % (t, T.rel32_callers(t), len(RC.get("%X" % t, []))))
    print("          jcc %s  data %s" % (T.jcc_callers(t), T.data_refs(t)))
    print("          rip %s  image-base %s" % (T.rip_refs(t, t + 1), T.imagebase_refs(t, t + 1)))
for a in (0x01E0C1D8, 0x01E0C1DC, 0x01E0C0D4, 0x01E0CDC0):
    print("%08X = %d" % (a, struct.unpack("<i", T.rd(a, 4))[0]))
