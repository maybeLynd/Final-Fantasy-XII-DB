"""sd107o_extra.py - SWE2-AUDIT-SPEC resume checks for the SD-107 review (lane loader only, no kit tools).

  X1  are the 56 out-of-shape stores of sd107o_indep.py G real instructions? Linear decode from the start of the
      .pdata chunk holding each site; report on-boundary / off-boundary. Control: the 4 known misaligned raw-scan
      extras (0020E76F, 008638FE, 008643DC, 00864922) must come out OFF-boundary, and 007E785C (read by hand) ON.
  X2  rsp-based register mov stores covering +0xA3 (a stack slot at rsp+0x9C..0xA3), same raw scan shape, for the
      narrowing text: counted only, not typed.
  X3  RTTI of the vtable 0019F930 writes before calling 001A0960.
"""
import bisect, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG
import re

IB = T.IB
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def chunk(va):
    j = bisect.bisect_right(ST, va - IB) - 1
    return PD[j] if j >= 0 and PD[j][0] <= va - IB < PD[j][1] else None


def on_boundary(va):
    e = chunk(va)
    if not e:
        return None
    for i in T.dis(IB + e[0], IB + e[1]):
        if i.address == va:
            return True
        if i.address > va:
            return False
    return False


SITES = re.findall(r"^\s+([0-9A-F]{8})  ", open(os.path.join(HERE, "sd107o_indep_G.out")).read(), re.M)
print("== X1. alignment of the %d out-of-shape sites (sd107o_indep_G.out)" % len(SITES))
ctl_off = [0x0020E76F, 0x008638FE, 0x008643DC, 0x00864922]
for a in ctl_off:
    print("  control misaligned %08X -> on-boundary %s" % (a, on_boundary(a)))
print("  control by-hand     007E785C -> on-boundary %s" % on_boundary(0x007E785C))
bad = []
for s in SITES:
    a = int(s, 16)
    b = on_boundary(a)
    if not b:
        bad.append((s, b))
print("  on-boundary %d of %d; not: %s" % (len(SITES) - len(bad), len(SITES), bad))

print("== X2. rsp-based register mov stores covering +0xA3 (raw disp32 scan, same shape as G, base rsp)")
n = 0
rows = []
for n_, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    for dsp in range(0x9C, 0xA4):
        pat = struct.pack("<i", dsp)
        k = blob.find(pat)
        while k >= 0:
            for back in range(10, 0, -1):
                if k - back < 0:
                    continue
                ins = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if not ins:
                    continue
                i = ins[0]
                if i.address + i.size != v + k + 4 or i.mnemonic != "mov" or len(i.operands) != 2:
                    continue
                d, s = i.operands
                if d.type != CS_OP_MEM or s.type != CS_OP_REG or d.mem.disp != dsp:
                    continue
                if d.mem.base and i.reg_name(d.mem.base) == "rsp" and not d.mem.index and dsp <= 0xA3 < dsp + d.size:
                    for b2 in range(1, back + 1):
                        j = list(T.md.disasm(blob[k - b2:k - b2 + 15], v + k - b2, 1))
                        if j and j[0].address + j[0].size == v + k + 4 and (j[0].mnemonic, j[0].op_str) == (i.mnemonic, i.op_str):
                            i = j[0]
                            break
                    rows.append((i.address, i.op_str, on_boundary(i.address)))
                break
            k = blob.find(pat, k + 1)
rows = sorted(set(rows))
print("  raw hits %d, on a .pdata linear-decode boundary %d" % (len(rows), sum(1 for r in rows if r[2])))
for r in rows[:8]:
    print("    %08X  %s  on-boundary %s" % r)

print("== X3. vtable written by 0019F930 before its call to 001A0960")
ins = T.dis(0x0019F930, 0x0019F9A0)
for i in ins:
    s = "    %08X  %-6s %s" % (i.address, i.mnemonic, i.op_str)
    for m, sz in T.mem_ops(i):
        if m.base and i.reg_name(m.base) == "rip":
            tgt = i.address + i.size + m.disp
            s += "   ; -> %08X" % tgt
            if i.mnemonic == "lea":
                colp = struct.unpack("<Q", T.rd(tgt - 8, 8))[0]
                c = T.rd(colp, 16)
                if c and len(c) == 16:
                    sig, ofs, cdo, tdr = struct.unpack("<IIII", c)
                    nm = T.rd(IB + tdr + 16, 80).split(b"\0")[0]
                    s += "  COL %08X sig %d off %#x class %s" % (colp, sig, ofs, nm.decode("latin1"))
    print(s)
    if i.mnemonic == "call" and "0x1a0960" in i.op_str:
        break

print("== X4. what the .rdata rva32 hits on the procedures / dispatcher entries are (sd107o_indep B)")
US = sorted(PD, key=lambda p: p[2])
UK = [p[2] for p in US]
for a in (0x01D6FB68, 0x01D6FB9C, 0x01D6FBB4, 0x01D69CA4, 0x01D69CB4):
    j = bisect.bisect_right(UK, a - IB) - 1
    p = US[j]
    uo = T.off(IB + p[2])
    flags, cnt = T.raw[uo] >> 3, T.raw[uo + 2]
    tail = IB + p[2] + 4 + ((cnt + 1) & ~1) * 2
    chained = struct.unpack("<III", T.rd(tail, 12)) if flags & 4 else None
    print("  %08X: in UNWIND_INFO %08X of chunk %08X-%08X, flags %d (%s), %s" % (
        a, IB + p[2], IB + p[0], IB + p[1], flags, "CHAININFO" if flags & 4 else "not chained",
        ("chained RUNTIME_FUNCTION at %08X = {%08X, %08X, %08X}; hit is its %s" % (
            tail, IB + chained[0], IB + chained[1], IB + chained[2],
            {0: "BeginAddress", 4: "EndAddress", 8: "UnwindData"}.get(a - tail, "offset %d" % (a - tail))))
        if chained else ""))
