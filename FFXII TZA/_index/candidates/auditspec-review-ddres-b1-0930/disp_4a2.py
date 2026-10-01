"""disp_4a2.py - SWE2-AUDIT-SPEC (DDRES-B1 review, 2026-09-29). Every instruction image-wide with a memory operand of
displacement exactly 0x4A2 (non-rip base), found by raw disp32 search + longest valid back-decode, with width, access
kind (write = first operand is the memory operand of a mov/store form) and the .pdata chain root of the site.
Control: the package's writer 001C977B and reader 0018F316 must both appear.
"""
import os, struct, sys, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM

dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    e = PD[j]
    while True:
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)


pat = struct.pack("<i", 0x4A2)
hits = set()
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    k = blob.find(pat)
    while k >= 0:
        best = None
        for back in range(10, 0, -1):
            if k - back < 0:
                continue
            ins = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
            if not ins:
                continue
            i = ins[0]
            if not (i.address < v + k and v + k + 4 <= i.address + i.size):
                continue
            ops = [op for op in i.operands if op.type == CS_OP_MEM and op.mem.disp == 0x4A2 and op.mem.base != T.X86_REG_RIP]
            if ops:
                w = i.operands[0].type == CS_OP_MEM and i.mnemonic.startswith(("mov", "and", "or", "xor", "add", "sub", "inc", "dec", "set"))
                w = w and not i.mnemonic.startswith(("movzx", "movsx"))
                best = (i.address, i.mnemonic, i.op_str, ops[0].size, "w" if w else ("lea" if i.mnemonic == "lea" else "r"))
                break
        if best:
            hits.add(best)
        k = blob.find(pat, k + 1)
rows = sorted(hits)
for a, mn, op, sz, kind in rows:
    r = root(a)
    print("%08X  root %s  %-3s %dB  %s %s" % (a, "%08X" % r if r else "--------", kind, sz, mn, op))
ws = [x for x in rows if x[4] == "w"]
print("total %d sites, %d writes, %d byte-width writes" % (len(rows), len(ws), sum(1 for x in ws if x[3] == 1)))
addrs = {x[0] for x in rows}
print("control 001C977B (writer) %s, 0018F316 (reader) %s" % ("PASS" if 0x001C977B in addrs else "FAIL", "PASS" if 0x0018F316 in addrs else "FAIL"))
