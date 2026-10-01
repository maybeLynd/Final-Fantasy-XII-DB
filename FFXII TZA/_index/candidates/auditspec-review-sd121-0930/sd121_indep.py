"""sd121_indep.py - SWE2-AUDIT-SPEC independent census for SD-121 (review of OPUS 06230b6a0, 2026-09-30).

Uses this lane's image loader ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted), not retool.py.

  A  every instruction image-wide whose memory/lea operand lands in the window 022D9000..022DA000 (the three arrays
     022D97B0..022D9AB0 plus 0x7B0 below and 0x550 above, so a base formed from a neighbour is also seen):
       - rip-relative (ov31_indep.rip_refs),
       - image-base-relative: any non-rip base/index with disp32 in window-0x120000 (raw disp32 search + back-decode),
     each with its .pdata root function.
  B  stored pointers: DIR64 relocation targets and aligned rva32 values in any section that land in the window.
  C  callers of every accessor, the reset and 0036E080: rel32 E8/E9, jcc 0F 8x, abs64/rva32 slots; compared to
     rawcalls.json.
  Controls: A must return the ten accessor rip sites and the reset's three image-base stores (known positives for
  both forms); C must return 00352270 as a caller of 0036E880 (known positive for rel32).
"""
import os, struct, sys, bisect, json, array
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

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


def R(a):
    r = root(a)
    return "%08X" % r if r else "--------"


LO, HI = 0x022D9000, 0x022DA000
A97, A98, A99 = 0x022D97B0, 0x022D98B0, 0x022D99B0


def arr_of(t):
    for a, n in ((A97, "97B0"), (A98, "98B0"), (A99, "99B0")):
        if a <= t < a + 0x100:
            return n + "[%d]" % ((t - a) // 4)
    return "outside-arrays"


print("== A1 rip-relative operands into %08X..%08X" % (LO, HI))
rip = T.rip_refs(LO, HI)
for a, mn, op, sz in rip:
    i = T.dis(a, count=1)[0]
    t = [i.address + i.size + m.disp for m, s in T.mem_ops(i) if m.base == X86_REG_RIP][0]
    print("  %08X root %s  %-5s %-40s -> %08X %s" % (a, R(a), mn, op, t, arr_of(t)))
print("  rip total %d" % len(rip))

print("== A2 image-base-relative operands (disp32 in window-IB, non-rip base or index)")
ib = []
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    L = len(blob)
    for k0 in range(4):
        n4 = (L - k0) // 4
        ar = array.array("I")
        ar.frombytes(blob[k0:k0 + 4 * n4])
        lo, hi = LO - T.IB, HI - T.IB
        for j, d in enumerate(ar):
            if lo <= d < hi:
                k = k0 + 4 * j
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
                    ms = [m for m, s in T.mem_ops(i) if m.base != X86_REG_RIP and m.disp == d]
                    if ms:
                        best = (i.address, i.mnemonic, i.op_str)
                        break
                    if i.mnemonic in ("mov", "cmp", "lea", "add", "sub") and any(op.type == 2 and op.imm == d for op in i.operands):
                        best = (i.address, i.mnemonic, i.op_str + "   [IMMEDIATE]")
                        break
                if best:
                    ib.append(best)
for a, mn, op in sorted(set(ib)):
    print("  %08X root %s  %-5s %s" % (a, R(a), mn, op))
print("  image-base total %d" % len(set(ib)))

print("== B stored pointers into the window")
T.pe.parse_data_directories(directories=[5])
relhits = []
for blk in getattr(T.pe, "DIRECTORY_ENTRY_BASERELOC", []):
    for e in blk.entries:
        if e.type == 10:
            va = T.IB + e.rva
            ob = T.off(va)
            if ob is None:
                continue
            val = struct.unpack_from("<Q", T.raw, ob)[0]
            if LO <= val < HI:
                relhits.append((va, val))
print("  DIR64 relocated slots -> window: %d %s" % (len(relhits), ["%08X->%08X" % x for x in relhits]))
rv = []
for n, v, vs, p, rs in T.ALL:
    blob = T.raw[p:p + min(vs, rs)]
    ar = array.array("I"); ar.frombytes(blob[:len(blob) // 4 * 4])
    for j, d in enumerate(ar):
        if LO - T.IB <= d < HI - T.IB:
            rv.append("%08X(%s)=%08X" % (v + 4 * j, n, d + T.IB))
print("  aligned rva32 values in any section -> window: %d %s" % (len(rv), rv[:40]))

print("== C callers of the accessors / reset / 0036E080")
RC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work",
                                  "FABLE", "pub140-scratch", "tools", "rawcalls.json")))
NAMES = {0x0036E040: "clear 98B0", 0x0036E160: "clear 97B0", 0x0036E1A0: "clear 99B0",
         0x0036E4B0: "get 98B0", 0x0036E4E0: "get 97B0", 0x0036E620: "get 99B0",
         0x0036E7B0: "set 98B0", 0x0036E7E0: "set 97B0", 0x0036E880: "set 99B0",
         0x0036E080: "clear-by-(h>>16)&15 all three", 0x0036E3B0: "reset"}
for f, nm in NAMES.items():
    r32 = T.rel32_callers(f)
    jc = T.jcc_callers(f)
    dr = T.data_refs(f)
    rj = RC.get("%08X" % f, [])
    print("  %08X %-30s rel32 %s | roots %s | jcc %s | data %s | rawcalls.json %s" % (
        f, nm, r32, sorted(set(R(int(x.split()[0], 16)) for x in r32)), jc, dr, rj))

print("== C2 callers of the verb handlers and readers (who else runs them)")
for f in (0x00352270, 0x00352940, 0x00342010, 0x003423C0, 0x003A40F0, 0x003A4220):
    print("  %08X rel32 %s | jcc %s | data %s" % (f, T.rel32_callers(f), T.jcc_callers(f), T.data_refs(f)))
