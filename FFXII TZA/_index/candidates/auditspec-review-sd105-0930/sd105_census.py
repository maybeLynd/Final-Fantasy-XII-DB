"""sd105_census.py - SWE2-AUDIT-SPEC: writers of the text element's +0x50 (fade step, f32), +0x90 (reveal target, s16)
and +0x9E (lag bound, s8) inside the text cluster 0029E000..002B6000.

Linear decode of every .pdata range whose chain root lies in the cluster (so disp8 forms are seen, which a raw
disp32 search misses), plus the window-embedded element (+0xD0) and the stack copy [rbp-0x70] of 002AC5F0 shifted
offsets. Every write whose operand covers the field's bytes, any base; rsp-based writes are listed separately.
Controls: the package's writers 002B33F0 (+0x50), 002B33DC / 002B3CF8 / 002B3DB4 (+0x90), 002AC232 (+0x9E) and the
copy 002A48C5 (movups covering +0x50) must appear.
"""
import bisect, collections, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_AC_WRITE
from capstone.x86 import X86_REG_RSP, X86_REG_RIP


def is_w(i, op):
    """capstone 5.0.7 marks the memory destination of movups / movq / movlps / movhps as READ; a mov-family
    instruction whose FIRST operand is this memory operand is a store."""
    if op.access & CS_AC_WRITE:
        return True
    o0 = i.operands[0] if len(i.operands) else None
    return (o0 is not None and o0.type == CS_OP_MEM and o0.mem.base == op.mem.base and o0.mem.disp == op.mem.disp
            and o0.mem.index == op.mem.index and i.mnemonic.startswith(("mov", "vmov"))
            and i.mnemonic not in ("movzx", "movsx", "movsxd"))

dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, _o + 12 * k) for k in range(dd.Size // 12))


def chain_root(e):
    for _ in range(32):
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return None


LO, HI = 0x0029E000, 0x002B6000
ranges = sorted((chain_root(e), T.IB + e[0], T.IB + e[1]) for e in PD if LO <= T.IB + e[0] < HI)
FIELDS = {"+0x50": (0x50, 4), "+0x90": (0x90, 2), "+0x9E": (0x9E, 1)}
SHIFTS = {"elem": 0, "window+0xD0": 0xD0, "rbp-0x70 copy": -0x70}
hits = collections.defaultdict(list)
n = 0
for r, a, b in ranges:
    for i in T.dis(a, b):
        n += 1
        for op in i.operands:
            if op.type != CS_OP_MEM or not is_w(i, op) or op.mem.base in (0, X86_REG_RIP):
                continue
            d, w = op.mem.disp, op.size
            for fn, (fo, fw) in FIELDS.items():
                for sn, sh in SHIFTS.items():
                    lo = fo + sh
                    if d < lo + fw and lo < d + w:
                        if sn == "rbp-0x70 copy" and i.reg_name(op.mem.base) != "rbp":
                            continue
                        if sn == "window+0xD0" and i.reg_name(op.mem.base) in ("rsp", "rbp"):
                            continue
                        hits[(fn, sn)].append((r, i.address, "%s %s" % (i.mnemonic, i.op_str), op.mem.base == X86_REG_RSP))
print("decoded %d instructions in %d .pdata ranges rooted in %08X..%08X" % (n, len(ranges), LO, HI))
ctl = {("+0x50", "elem"): [0x002B33F0, 0x002A48C5], ("+0x90", "elem"): [0x002B33DC, 0x002B3CF8, 0x002B3DB4],
       ("+0x9E", "elem"): [0x002AC232]}
for k, want in ctl.items():
    got = {h[1] for h in hits[k]}
    print("control %s %s: %s" % (k, ["%08X" % a for a in want], "PASS" if all(a in got for a in want) else "FAIL"))
for (fn, sn), L in sorted(hits.items()):
    ns = [h for h in L if not h[3]]
    print("== %s via %s: %d writes (%d rsp-based omitted)" % (fn, sn, len(ns), len(L) - len(ns)))
    for r, a, t, s in ns:
        print("   %08X  %08X  %s" % (r, a, t))
