"""sd100_ctx.py - print the instructions leading into each given site (default: the dword stores to +0xB0 in the text
cluster that sd100_census.out lists and the package's census does not), decoded from the site's .pdata root so the
decode is on true instruction boundaries.  Usage: python sd100_ctx.py [SITE ...]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
import bisect, struct  # noqa: E402
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, _o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    e = PD[j]
    for _ in range(32):
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return None

DEF = [0x002A781B, 0x002A96CC, 0x002A96E2, 0x002A97DD, 0x002A9877, 0x002A9A10, 0x002A9A7D, 0x002A9A9C, 0x002A9C9A,
       0x002A9EE7, 0x002B0838, 0x002B35E0, 0x002B364C, 0x002B36DC, 0x002B3D1B]
sites = [int(a, 16) for a in sys.argv[1:]] or DEF
for s in sites:
    r = root(s) or (s - 0x60)
    ins = T.dis(r, s + 16)
    k = [j for j, i in enumerate(ins) if i.address == s]
    if not k:
        print("%08X: not on a boundary decoded from %08X" % (s, r)); continue
    k = k[0]
    print("=== %08X (root %08X)" % (s, r))
    for i in ins[max(0, k - 9):k + 2]:
        print("  %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
