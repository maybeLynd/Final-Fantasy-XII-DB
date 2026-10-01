"""sd100_instances.py - where text elements live: for each E8/E9 call site of the element entry points, the last write
of rcx before the call (decoded from the site's .pdata root), so embedded elements (rcx = obj + K) and static elements
(rip / image-base lea) are found. Also lists 002ABF70's callers. Lane loader; raw index + own rel32 scan.
"""
import bisect, json, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

RC = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
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


TARGETS = [0x002ABF70, 0x002AC1E0, 0x002B3D50, 0x002B3C30, 0x002B32D0, 0x002A9980, 0x002A8C50, 0x002B3950]
for t in TARGETS:
    sites = [int(s, 16) for s in RC.get("%X" % t, [])]
    print("== %08X  %d E8/E9 sites" % (t, len(sites)))
    for s in sites:
        r = root(s)
        if r is None:
            print("   %08X  (no .pdata root)" % s); continue
        ins = T.dis(r, s + 5)
        k = [j for j, i in enumerate(ins) if i.address == s]
        if not k:
            print("   %08X  root %08X  (not on a boundary)" % (s, r)); continue
        last = None
        for i in reversed(ins[:k[0]]):
            if i.op_str.startswith(("rcx,", "rcx ,")) and i.mnemonic in ("mov", "lea", "add", "sub", "xor", "cmov", "movsxd") \
                    or i.op_str.startswith("ecx,"):
                last = i; break
            if i.mnemonic == "call" or i.mnemonic.startswith("j"):
                last = None; break
        print("   %08X  root %08X  %s" % (s, r, ("%08X  %s %s" % (last.address, last.mnemonic, last.op_str)) if last else "(rcx set before a call/branch)"))
