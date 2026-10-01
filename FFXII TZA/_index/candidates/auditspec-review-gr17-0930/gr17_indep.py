"""gr17_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the GR-17 review (2026-09-30).

Not the package's checkers and not retool.py: this lane's loader ov31_indep.py (pefile + capstone, sha256 asserted),
raw E8/E9 + jcc (0F 8x) + abs64/rva32 scans, and raw disp32 sweeps with longest valid back-decode.

  A  callers (E8/E9, jcc, abs64/rva32 slots) of the allocation chain 00234480 / 00265A20 / 0026CE60, the release
     chain 00234200 / 0025B070 / 002628B0, the readers' hub 0030E360 / 00312280 and the +0x774 writer 00329F80 /
     the stop 00319420.  Cross-checked against rawcalls.json.
  B  the manager index: every reference to the manager array 02098E10 (+ idx*0x288) in rip, image-base-relative and
     absolute forms, with any +0x28 dword store in the referencing functions; plus every rip store that lands on a
     record's +0x28 directly.
  C  image-wide displacement 0x774 sweep (non-rip base, and rip targets ending ...+0x774 are not meaningful here),
     every width, write/read/lea classification; plus displacement 0x6B0 and 0xC4 sites; control: 00236BE6 and
     0032A045 must appear as writes.
  D  who touches the unit pool base/count cells 0208E688 / 0208E6A0 (rip + image-base forms).
"""
import os, struct, sys, json, bisect
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

RAWCALLS = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "tools", "rawcalls.json")
RC = json.load(open(RAWCALLS))

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


def R(va):
    r = root(va)
    return "%08X" % r if r else "--------"


def func_ins(f):
    """every instruction of every .pdata chunk whose root is f"""
    out = []
    for b, e, u in PD:
        if root(T.IB + b) == f:
            out += T.dis(T.IB + b, T.IB + e)
    return out


def callers(tgt):
    a = T.rel32_callers(tgt)
    j = T.jcc_callers(tgt)
    d = T.data_refs(tgt)
    rc = RC.get("%X" % tgt, [])
    return a, j, d, rc


def disp_sweep(disp, rip_ok=False):
    pat = struct.pack("<i", disp)
    hits = set()
    for n, v, vs, p, rs in T.TEXT:
        blob = T.raw[p:p + min(vs, rs)]
        k = blob.find(pat)
        while k >= 0:
            for back in range(10, 0, -1):
                if k - back < 0:
                    continue
                ins = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if not ins:
                    continue
                i = ins[0]
                if not (i.address < v + k and v + k + 4 <= i.address + i.size):
                    continue
                ops = [op for op in i.operands if op.type == CS_OP_MEM and op.mem.disp == disp and
                       (rip_ok or op.mem.base != X86_REG_RIP)]
                if ops:
                    first_mem = i.operands[0].type == CS_OP_MEM and i.operands[0].mem.disp == disp
                    rd_only = i.mnemonic.startswith(("cmp", "test", "movzx", "movsx", "push", "bt ", "ucomis", "comis"))
                    if i.mnemonic == "lea":
                        kind = "lea"
                    elif first_mem and not rd_only and not i.mnemonic.startswith(("bt",)) or i.mnemonic in ("bts", "btr", "btc"):
                        kind = "w"
                    else:
                        kind = "r"
                    hits.add((i.address, i.mnemonic, i.op_str, ops[0].size, kind))
                    break
            k = blob.find(pat, k + 1)
    return sorted(hits)


def fmt_callers(name, tgt):
    a, j, d, rc = callers(tgt)
    T.say("  %s %08X: E8/E9 %s | jcc %s | abs64 %s | rva32 %d | rawcalls.json %s" %
          (name, tgt, [x + " in " + R(int(x[:8], 16)) for x in a], j, d["abs64"], len(d["rva32"]), rc))
    T.say("      rva32 slots: %s" % d["rva32"])


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "ABCD"
    if "A" in part:
        T.say("== A. callers (E8/E9 with .pdata root, jcc, stored abs64 pointers, rva32 count, rawcalls.json)")
        for nm, t in (("allocator", 0x00234480), ("manager-init step", 0x00265A20), ("init", 0x0026CE60),
                      ("release", 0x00234200), ("release loop", 0x0025B070), ("unload", 0x002628B0),
                      ("reward computer", 0x00312280), ("KO hub", 0x0030E360), ("unit finder", 0x0031B860),
                      ("+0x774 writer", 0x00329F80), ("effect stop", 0x00319420), ("setup", 0x0026C8C0),
                      ("rebind", 0x003EA6E0), ("rebind body", 0x003EA820), ("deferred mode req", 0x0032FC30),
                      ("post-rebind", 0x0032FCA0), ("setup caller", 0x0032F850), ("unit getter", 0x00263E30)):
            fmt_callers(nm, t)
    if "B" in part:
        T.say("== B. manager array 02098E10 (+idx*0x288): references and +0x28 stores")
        base = 0x02098E10
        lo, hi = base, base + 5 * 0x288
        r = T.rip_refs(lo, hi)
        T.say("  rip refs into the 5-record array: %d" % len(r))
        for h in r:
            off_in = None
            T.say("    %08X in %s  %s %s (%dB)" % (h[0], R(h[0]), h[1], h[2], h[3]))
        ib = T.imagebase_refs(lo, lo + 1)
        T.say("  image-base-relative disp 0x%X (array base): %d" % (lo - T.IB, len(ib)))
        for h in ib:
            T.say("    %08X in %s  %s %s (%dB)" % (h[0], R(h[0]), h[1], h[2], h[3]))
        d = T.data_refs(lo)
        T.say("  stored pointers to the array base: %s" % d["abs64"])
        # rip stores landing on record k's +0x28
        for k in range(5):
            c = base + k * 0x288 + 0x28
            rr = T.rip_refs(c, c + 4)
            T.say("  record %d +0x28 (%08X) direct rip refs: %s" % (k, c, ["%08X %s %s" % h[:3] for h in rr]))
        # every +0x28 dword store in the functions that form a manager-record pointer
        fns = sorted(set(root(h[0]) for h in r + ib if root(h[0])))
        T.say("  functions forming a manager pointer: %s" % ["%08X" % f for f in fns])
        s28 = []
        for f in fns:
            for i in func_ins(f):
                if i.operands and i.operands[0].type == CS_OP_MEM and i.operands[0].mem.disp == 0x28 and                         i.operands[0].size == 4 and i.operands[0].mem.base not in (X86_REG_RIP, T.X86_REG_INVALID) and                         not i.mnemonic.startswith(("cmp", "test")) and i.operands[0].mem.base != 0 and                         i.reg_name(i.operands[0].mem.base) not in ("rsp", "rbp") or                         (i.operands and i.operands[0].type == CS_OP_MEM and i.operands[0].mem.disp == 0x28 and
                         i.operands[0].size == 4 and i.reg_name(i.operands[0].mem.base) == "rbp" and
                         not i.mnemonic.startswith(("cmp", "test"))):
                    s28.append((i.address, i.mnemonic, i.op_str))
        T.say("  dword stores at +0x28 inside those functions: %s" % ["%08X %s %s" % x[:3] for x in s28])
        # the current-manager pointer cell 02099D70
        c = 0x02099D70
        rr = T.rip_refs(c, c + 8)
        T.say("  current-manager cell 02099D70 rip refs: %d; writes %s" %
              (len(rr), ["%08X %s %s" % h[:3] for h in rr if h[2].startswith("qword ptr [rip")]))
    if "C" in part:
        T.say("== C. displacement sweeps")
        rows = disp_sweep(0x774)
        T.say("  disp 0x774 sites: %d" % len(rows))
        for a, mn, op, sz, kind in rows:
            T.say("    %08X root %s %-3s %dB  %s %s" % (a, R(a), kind, sz, mn, op))
        ws = [x for x in rows if x[4] == "w"]
        T.say("  writes: %s" % ["%08X" % x[0] for x in ws])
        T.say("  CONTROL 00236BE6 in writes: %s; 0032A045 in writes: %s" %
              (any(x[0] == 0x00236BE6 for x in ws), any(x[0] == 0x0032A045 for x in ws)))
        for dsp in (0x6B0, 0xB88):
            rows = disp_sweep(dsp)
            T.say("  disp 0x%X sites: %d; lea %s; writes %s" % (
                dsp, len(rows), ["%08X(%s) %s" % (x[0], R(x[0]), x[2]) for x in rows if x[4] == "lea"],
                ["%08X(%s) %s %s" % (x[0], R(x[0]), x[1], x[2]) for x in rows if x[4] == "w"]))
    if "D" in part:
        T.say("== D. unit pool cells")
        for c in (0x0208E688, 0x0208E6A0):
            rr = T.rip_refs(c, c + 8)
            ib = T.imagebase_refs(c, c + 1)
            T.say("  %08X rip refs %d in %s; image-base %d %s" % (
                c, len(rr), sorted(set(R(h[0]) for h in rr)), len(ib), ["%08X %s" % (h[0], h[2]) for h in ib]))
            for h in rr:
                if h[2].startswith(("qword ptr [rip", "dword ptr [rip")):
                    T.say("    store? %08X %s %s" % h[:3])


def imm_sweep(val):
    """instructions with an immediate operand == val (add/sub/lea-less address forming, mov r8d size args)"""
    pat = struct.pack("<i", val)
    hits = set()
    for n, v, vs, p, rs in T.TEXT:
        blob = T.raw[p:p + min(vs, rs)]
        k = blob.find(pat)
        while k >= 0:
            for back in range(10, 0, -1):
                if k - back < 0:
                    continue
                ins = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if not ins:
                    continue
                i = ins[0]
                if not (i.address < v + k and v + k + 4 <= i.address + i.size):
                    continue
                if any(op.type == 2 and op.imm == val for op in i.operands):
                    hits.add((i.address, i.mnemonic, i.op_str))
                    break
            k = blob.find(pat, k + 1)
    return sorted(hits)


if __name__ == "__main__" and "E" in (sys.argv[1] if len(sys.argv) > 1 else ""):
    T.say("== E. immediate forms")
    for val in (0x774, 0x6B0, 0xF50):
        rows = imm_sweep(val)
        T.say("  imm 0x%X: %d sites" % (val, len(rows)))
        for a, mn, op in rows:
            T.say("    %08X root %s  %s %s" % (a, R(a), mn, op))
