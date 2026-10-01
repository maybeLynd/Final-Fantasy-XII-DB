"""sd62o_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the SD-62 ORACLE record (sd62-registry-list-links-0930,
dedfaf0d7) and OPUS's F3 adjudication (5a6b2eed3). pefile + capstone through this lane's ov31_indep loader (sha256
asserted there); not the package's retool.py census. Static only.

  A  callers of the link writer 00639160 in all forms (E8/E9 rel32, jcc, abs64/rva32 slots), each site's .pdata root, and
     the last in-function writes of rcx (owner) and rdx (descriptor) before the call (linear back-walk, candidates).
  B  every rip-relative and image-base-relative reference into the root 01F2E330..01F2E367, stores classified; stored
     pointers (abs64) to the root's cells.
  C  the same for 01F2E780..01F2E7F7 (the tree header and the record(s) above it), grouped by function root; and the
     thread-safe-static guard cells each initialiser tests.
  D  the ordering of 00639160's no-base-in-owner splice: which neighbour of owner+0x10 the new node becomes.
Controls: A must return the 12 sites the package lists (its own positive) and 00639450's 471 callers must reach it
through one site; B must return the three 00638C90 initialiser triples; C must return 00635B80's stores at 01F2E7B0.
"""
import os, re, struct, sys, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG

dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def entry(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return PD[j]


def root(va):
    e = entry(va)
    if e is None:
        return None
    while True:
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)


def chunk_of(va):
    e = entry(va)
    return (T.IB + e[0], T.IB + e[1])


def say(*a):
    print(" ".join(str(x) for x in a))


def writes_reg(i, names):
    try:
        regs_w = {i.reg_name(r) for r in i.regs_access()[1]}
    except Exception:
        regs_w = set()
    return regs_w & names


# ---------------- A
say("== A  callers of 00639160")
rc = T.rel32_callers(0x00639160); jc = T.jcc_callers(0x00639160); dr = T.data_refs(0x00639160)
say("rel32:", len(rc), " jcc:", len(jc), jc, " abs64:", dr["abs64"], " rva32:", len(dr["rva32"]))
FAM = {"rcx": {"rcx", "ecx", "cx", "cl"}, "rdx": {"rdx", "edx", "dx", "dl"}}
for s in rc:
    a = int(s.split()[0], 16)
    r = root(a); c0, c1 = chunk_of(a)
    ins = [i for i in T.dis(c0, a + 5) if i.address < a]
    last = {}
    for i in ins:
        for k, fam in FAM.items():
            if writes_reg(i, fam):
                last[k] = "%08X %s %s" % (i.address, i.mnemonic, i.op_str)
    say("  %s  root %08X  rcx<- [%s]  rdx<- [%s]" % (s, r, last.get("rcx", "entry/other chunk"), last.get("rdx", "entry/other chunk")))
    # resolve: rcx loaded from a rip cell X, rdx = a rip lea D (directly or through one register lea'd in the function)
    def riptgt(txt_addr):
        i = next(T.md.disasm(T.rd(txt_addr, 16), txt_addr, 1))
        for mm, _ in T.mem_ops(i):
            if mm.base == T.X86_REG_RIP:
                return i.address + i.size + mm.disp, i
        return None, i
    X = D = None
    if "rcx" in last:
        X, _ = riptgt(int(last["rcx"].split()[0], 16))
    if "rdx" in last:
        D, i = riptgt(int(last["rdx"].split()[0], 16))
        if D is None and i.mnemonic == "mov" and i.operands[1].type == CS_OP_REG:
            reg = i.reg_name(i.operands[1].reg)
            cands = set()
            for s0, s1 in [c for c in [chunk_of(r)]]:
                for j in T.dis(r, a):
                    if j.mnemonic == "lea" and j.op_str.startswith(reg + ","):
                        for mm, _ in T.mem_ops(j):
                            if mm.base == T.X86_REG_RIP:
                                cands.add(j.address + j.size + mm.disp)
            D = sorted(cands)[0] if len(cands) == 1 else ("regs:%s" % sorted("%08X" % c for c in cands))
    if isinstance(X, int) and isinstance(D, int):
        say("      owner cell %08X = descriptor %08X + 0x%X" % (X, D, X - D))
    else:
        say("      owner cell %s, descriptor %s" % (X if X is None else "%08X" % X, D))
rc45 = T.rel32_callers(0x00639450)
say("00639450 rel32 callers:", len(rc45), " jcc:", len(T.jcc_callers(0x00639450)))

# ---------------- B
say("== B  references into the root 01F2E330..01F2E367")
rr = T.rip_refs(0x01F2E330, 0x01F2E368)
by = {}
for a, m, op, sz in rr:
    by.setdefault(root(a), []).append((a, m, op, sz))
stores0 = []
for a, m, op, sz in rr:
    i = next(T.md.disasm(T.rd(a, 16), a, 1))
    tgt = None
    for mm, _ in T.mem_ops(i):
        if mm.base == T.X86_REG_RIP:
            tgt = i.address + i.size + mm.disp
    first_mem = i.operands and i.operands[0].type == CS_OP_MEM
    if tgt in (0x01F2E330, 0x01F2E338) and first_mem and m.startswith("mov"):
        stores0.append((a, op))
say("rip refs:", len(rr), "in", len(by), "functions")
for f in sorted(by, key=lambda x: x or 0):
    say("  %08X: %d refs" % (f or 0, len(by[f])))
say("rip stores to root+0x00/+0x08:", len(stores0))
# the value stored: every rip lea into the source register anywhere in the store's function (all .pdata chunks).
# Not flow-aware (a candidate check): it passes a store only when that register is lea'd to 01F2E330 and to nothing else
# by rip in that function. The hot paths restore callee-saved registers before the cold init chunk, so a linear
# "last write" walk is wrong here; the flow is read by hand for 006318A0 and 00638C90 in REVIEW.md.
ROOTS = {}
for e in PD:
    ROOTS.setdefault(root(T.IB + e[0]), []).append((T.IB + e[0], T.IB + e[1]))
bad, fn_seen = [], set()
for a, op in stores0:
    src = op.split(", ")[-1]
    f = root(a); fn_seen.add(f)
    vals = set()
    for s0, s1 in ROOTS[f]:
        for i in T.dis(s0, s1):
            if i.mnemonic == "lea" and i.op_str.startswith(src + ","):
                for mm, _ in T.mem_ops(i):
                    if mm.base == T.X86_REG_RIP:
                        vals.add(i.address + i.size + mm.disp)
    if vals != {0x01F2E330}:
        bad.append(("%08X" % a, op, sorted("%08X" % v for v in vals)))
say("  in %d functions; stores whose source register is not lea'd only to 01F2E330 in its function: %s" % (len(fn_seen), bad))
ib = T.imagebase_refs(0x01F2E330, 0x01F2E368)
say("image-base-relative refs:", ib)
for q in range(0x01F2E330, 0x01F2E368, 8):
    d = T.data_refs(q)
    say("  abs64 refs to %08X: %s" % (q, d["abs64"]))
say("root static qwords:", " ".join("%016X" % x for x in struct.unpack("<7Q", T.rd(0x01F2E330, 56))))

# ---------------- C
say("== C  references into 01F2E780..01F2E7F7")
rr = T.rip_refs(0x01F2E780, 0x01F2E7F8)
for a, m, op, sz in rr:
    i = next(T.md.disasm(T.rd(a, 16), a, 1))
    tgt = [i.address + i.size + mm.disp for mm, _ in T.mem_ops(i) if mm.base == T.X86_REG_RIP][0]
    w = "W" if (i.operands and i.operands[0].type == CS_OP_MEM and not m.startswith("cmp") and not m.startswith("test")) else "r"
    say("  %08X root %08X  %s  +%02X of 01F2E780  %-5s %s" % (a, root(a) or 0, w, tgt - 0x01F2E780, m, op))
say("image-base-relative refs:", T.imagebase_refs(0x01F2E780, 0x01F2E7F8))
for q in range(0x01F2E780, 0x01F2E7F8, 8):
    d = T.data_refs(q)
    say("  abs64 refs to %08X: %s   static q=%016X" % (q, d["abs64"], struct.unpack("<Q", T.rd(q, 8))[0]))
for g in (0x02CF94EC, 0x02CF9524, 0x02CF9528):
    fs = sorted(set("%08X" % (root(a) or 0) for a, m, op, sz in T.rip_refs(g, g + 4)))
    say("guard %08X referenced by %s" % (g, fs))

# ---------------- D
say("== D  00639160 splice ordering (no-base path 0063922E-00639244)")
for i in T.dis(0x0063922E, 0x00639247):
    say("  %08X %s %s" % (i.address, i.mnemonic, i.op_str))
say("  r14 = owner+0x10 (head), rdx = descriptor+0x50 (self-linked by 00632D80), rcx = [head+0] (old first)")
say("  => [head+0] = node, [node+0] = old first, [node+8] = head, [old first+8] = node: node becomes head's +0 neighbour")
say("  the walkers 008AF490/00637A70/00638C90 start from [01F2E340] (= head+0) and step by [node+0]")
