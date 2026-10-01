"""sd1_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-1 (OPUS, 473de1075). Read-only on the image.
Uses this lane's loader (../auditspec-review-ov31-type-store-0929/ov31_indep.py, sha256 asserted), not the author's tool.
  A  readers of the force-fight flag 01E0C2B8 (rip-relative + image-base-relative, image-wide, all widths)
  B  every caller of 00253B90, the thunk 0030C0D0 and 00253BA0: raw E8/E9 rel32, jcc rel32, abs64/rva32 slots
  C  the kind tests the record cites, decoded: 002FFDAE, 00301A6E, 00307E0A, 0030BFED, 00339C24, 00305BA5
  D  the P1 route edges, decoded: 00233F70 -> 00308610, 00308610 -> 0030FA00, 0030FA00 -> 0030C010,
     00308610 -> 00305AB0, 00233F70 at 00234076 -> 0033A240, 0030E360 -> 00307D10 (direct call/jmp present in body)
  E  the engagement arm 00307D63..00307D7C decoded (what flag-off clears)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T

FLAG = 0x01E0C2B8
print("A  readers/writers of 01E0C2B8..+4")
for kind, fn in (("rip", T.rip_refs), ("imagebase", T.imagebase_refs)):
    hits = fn(FLAG - 3, FLAG + 4)
    print("  %s: %d" % (kind, len(hits)))
    for h in hits:
        print("    ", h)
print("  data slots:", T.data_refs(FLAG))

def callers(t):
    r = T.rel32_callers(t); j = T.jcc_callers(t); d = T.data_refs(t)
    return r, j, d
print("B  callers")
tot = 0
for t in (0x00253B90, 0x0030C0D0, 0x00253BA0):
    r, j, d = callers(t)
    tot += len(r)
    print("  %08X rel32 %d jcc %d abs64 %d rva32 %d" % (t, len(r), len(j), len(d["abs64"]), len(d["rva32"])))
    for x in r: print("     ", x)
    for x in j: print("      jcc", x)
print("  total rel32 sites:", tot)

def show(a, n=4, back=0):
    for i in T.dis(a - back, a + 0x30)[: n + 6]:
        if i.address >= a - back:
            print("     %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
print("C  kind tests")
for a in (0x002FFDAE, 0x00301A6E, 0x00307E0A, 0x0030BFED, 0x00339C24, 0x00305BA5):
    print("  at %08X" % a); show(a, 3)

print("D  route edges (direct call/jmp from caller body to callee)")
for src, dst in ((0x00233F70, 0x00308610), (0x00308610, 0x0030FA00), (0x0030FA00, 0x0030C010),
                 (0x00308610, 0x00305AB0), (0x00233F70, 0x0033A240), (0x0030E360, 0x00307D10),
                 (0x00233F70, 0x00310DB0), (0x00310DB0, 0x003112F0), (0x003112F0, 0x0030E360),
                 (0x00305AB0, 0x00305CC0), (0x00305CC0, 0x003014C0), (0x003014C0, 0x00301830), (0x00301830, 0x00309A90)):
    ins = T.dis_func(src)
    sites = [i.address for i in ins if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x") and int(i.op_str, 16) == dst]
    print("  %08X -> %08X : %s" % (src, dst, " ".join("%08X" % s for s in sites) or "NONE (not a direct edge in the decoded body)"))

print("E  engagement arm 00307D50..00307D90")
for i in T.dis(0x00307D50, 0x00307D90):
    print("     %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
