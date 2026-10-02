"""rv_avail.py - FABLE independent re-derivation for ASTRA packet ov42-actor-predicate-domain (2b341ca3a).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2 review).  Does not import or
run ASTRA's prove.py, run.py, control.py, metadata.py, capture drivers or the shared role adapter (reg_tracking.py).

Method: complete linear decode of the availability body 002FFCF0 (479 B, six chained .pdata records), the class
query 00322C50 (code + its image-relative jump table), the per-unit leg 00306480 and its two callees' byte +5 reads
(003060E0, 00323EC0); local CFGs from rvlib.Body; a reverse reaching-definition walk for EAX at the shared return;
edge-removal reachability for "a zero return passed the class-success edge"; register-write censuses for the id
(rbx/r14), the record carrier (rdi) and the class-query R8; and the reviewer's own small concrete evaluator that runs
the image's own class-0x14 instructions for every u16 id under an injected descriptor (count 543, 511, or NULL),
recording every R8 read.  Controls patch a private in-memory copy of the image and require a named check to fail.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, SHA256 as SHA_PIN, fam  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG  # noqa: E402

AV = (0x002FFCF0, 0x002FFECF)      # availability, 479 B
CQ = (0x00322C50, 0x00323051)      # class query code, 1025 B (record runs on through the jump table)
CQ_REC_END = 0x003230D4
JT = 0x00323054                    # 32 image-relative dwords
UL = (0x00306480, 0x003064E3)      # per-unit leg, 99 B
CAT = (0x003060E0, 0x00306333)     # category helper, 595 B
LIC = (0x00323EC0, 0x00324012)     # licence helper, 338 B
DESC = 0x02EBF138
SLUG = "ov42-actor-predicate-domain"
PRODUCER = "2b341ca3a"
MANIFEST_SHA = "ca8a35ee40fa75f941fe4feac3d4308f3b55dd1c65fdafc90bf44de02a3babb3"
SHARED_RET = 0x2FFDAD
EARLY_RET = 0x2FFECE
CQ_CALL = 0x2FFD8B
UL_CALL = 0x2FFE9D


class Rep(Report):
    def __init__(self, title):
        Report.__init__(self, title)
        self.n = 0
        self.failed = []

    def check(self, name, cond, detail=""):
        self.n += 1
        if not cond:
            self.failed.append(name)
        return Report.check(self, name, cond, detail)


def T(B, a):
    I = B.ins.get(a)
    return I.text if I else "<no boundary>"


def writers(B, f, lo=None, hi=None):
    return [a for a in B.order if f in B[a].reg_writes and (lo is None or lo <= a) and (hi is None or a < hi)]


def preds(B):
    p = {}
    for a in B.order:
        for s in B.succ(a):
            p.setdefault(s, set()).add(a)
    return p


def on_paths(B, src, dst):
    """Instructions on some path src -> dst that does not pass dst first (dst excluded)."""
    fwd = B.reach(src, avoid=[dst])
    P = preds(B)
    back, st = set(), [dst]
    while st:
        a = st.pop()
        for q in P.get(a, ()):
            if q not in back:
                back.add(q)
                st.append(q)
    return fwd & back


def reach_avoid_edge(B, frm, ea, eb, stop=()):
    seen, st = set(), [frm]
    while st:
        a = st.pop()
        if a in seen or a not in B.ins:
            continue
        seen.add(a)
        if a in stop:
            continue
        for s in B.succ(a):
            if a == ea and s == eb:
                continue
            st.append(s)
    return seen


def writes_rax(I):
    return I.mnemonic == "call" or ("rax" in I.reg_writes and I.mnemonic not in ("push",))


def eax_defs(B, ret):
    """Reverse reaching definitions of EAX at `ret` over the local CFG (a call defines EAX)."""
    P = preds(B)
    defs, seen, st = set(), set(), list(P.get(ret, ()))
    while st:
        a = st.pop()
        if a in seen:
            continue
        seen.add(a)
        if writes_rax(B[a]):
            defs.add(a)
            continue
        st.extend(P.get(a, ()))
    return defs


def frame_at(B, upto):
    fr = 0
    for a in B.order:
        if a >= upto:
            break
        I = B[a]
        if I.mnemonic == "push":
            fr += 8
        elif I.mnemonic == "sub" and I.op_str.startswith("rsp, ") and I.imm:
            fr += I.imm[0]
    return fr


# ---------------------------------------------------------------- own concrete evaluator for 00322C50
class EvalRefused(Exception):
    pass


M64 = (1 << 64) - 1


def _sx(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


class Eval(object):
    """Runs the image's own instructions of 00322C50 for one (class, id) with an injected descriptor.
    Only the instruction forms on the class-0x14 path are modelled; anything else refuses."""

    def __init__(self, img, B, desc_ptr, count):
        self.img, self.B, self.P, self.C = img, B, desc_ptr, count

    def run(self, cls, ident, r8_poison=0x5EED5EED):
        R = dict((r, 0) for r in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp", "r8", "r9", "r10", "r11",
                                   "r12", "r13", "r14", "r15"))
        R["rcx"], R["rdx"], R["r8"], R["rsp"] = cls, ident, r8_poison, 0x7FF000
        self.r8_reads = []
        self.pcs = []
        stack = {}
        fl = {}
        pc = self.B.start
        for _ in range(200):
            I = self.B.ins.get(pc)
            if I is None:
                raise EvalRefused("pc %X off-body" % pc)
            self.pcs.append(pc)
            if "r8" in I.reg_reads:
                self.r8_reads.append(pc)
            ci = I.ci
            ops = ci.operands
            m = I.mnemonic
            nxt = pc + I.size

            def ea(op):
                mm = op.mem
                b = ci.reg_name(mm.base) if mm.base else None
                x = ci.reg_name(mm.index) if mm.index else None
                v = mm.disp
                if b == "rip":
                    v += nxt
                elif b:
                    v += R[fam(b)]
                if x:
                    v += R[fam(x)] * mm.scale
                return v & M64

            def get(op):
                if op.type == X86_OP_IMM:
                    return op.imm & ((1 << (8 * op.size)) - 1)
                if op.type == X86_OP_REG:
                    return R[fam(ci.reg_name(op.reg))] & ((1 << (8 * op.size)) - 1)
                a = ea(op)
                if a == DESC and op.size == 8:
                    return self.P
                if self.P and a == self.P + 4 and op.size == 4:
                    return self.C
                if a in stack:
                    return stack[a]
                try:
                    raw = self.img.read(a, op.size)
                except ValueError:
                    raise EvalRefused("read of %X not modelled" % a)
                return int.from_bytes(raw, "little")

            def put(op, v):
                if op.type == X86_OP_REG:
                    f = fam(ci.reg_name(op.reg))
                    if op.size == 4:
                        R[f] = v & 0xFFFFFFFF
                    elif op.size == 8:
                        R[f] = v & M64
                    else:
                        msk = (1 << (8 * op.size)) - 1
                        R[f] = (R[f] & ~msk) | (v & msk)
                elif op.type == X86_OP_MEM:
                    stack[ea(op)] = v
                else:
                    raise EvalRefused("bad dest")

            def setflags(a, b, res, bits):
                fl["z"] = (res & ((1 << bits) - 1)) == 0
                fl["s"] = bool(_sx(res, bits) < 0)
                fl["sa"], fl["sb"], fl["ua"], fl["ub"] = _sx(a, bits), _sx(b, bits), a, b
                fl["sub"] = True

            if m in ("nop", "push", "pop") and m != "pop":
                if m == "push":
                    R["rsp"] -= 8
                    stack[R["rsp"]] = get(ops[0])
                pc = nxt
                continue
            if m == "pop":
                put(ops[0], stack.get(R["rsp"], 0))
                R["rsp"] += 8
                pc = nxt
                continue
            if m == "ret":
                return R["rax"] & 0xFFFFFFFF
            if m == "mov":
                put(ops[0], get(ops[1]))
            elif m == "movzx":
                put(ops[0], get(ops[1]))
            elif m == "lea":
                put(ops[0], ea(ops[1]))
            elif m == "xor":
                v = get(ops[0]) ^ get(ops[1])
                put(ops[0], v)
                bits = 8 * ops[0].size
                setflags(v, 0, v, bits)
            elif m in ("add", "sub"):
                a, b = get(ops[0]), get(ops[1])
                if ops[1].type == X86_OP_IMM:
                    b = _sx(ops[1].imm, 64) & ((1 << (8 * ops[0].size)) - 1)
                bits = 8 * ops[0].size
                v = (a + b) if m == "add" else (a - b)
                put(ops[0], v)
                setflags(a, b, v, bits)
            elif m == "cmp":
                a, b = get(ops[0]), get(ops[1])
                bits = 8 * ops[0].size
                if ops[1].type == X86_OP_IMM:
                    b = ops[1].imm & ((1 << bits) - 1)
                setflags(a, b, a - b, bits)
            elif m == "test":
                bits = 8 * ops[0].size
                v = get(ops[0]) & get(ops[1])
                fl["z"] = (v & ((1 << bits) - 1)) == 0
                fl["s"] = bool(_sx(v, bits) < 0)
                fl["sub"] = False
            elif m == "cdqe":
                R["rax"] = _sx(R["rax"], 32) & M64
            elif m == "dec":
                put(ops[0], get(ops[0]) - 1)
            elif m == "jmp":
                pc = (get(ops[0]) if ops[0].type == X86_OP_REG else I.direct_target()) & M64
                continue
            elif m.startswith("j"):
                t = I.direct_target()
                if m in ("je", "jne"):
                    take = fl["z"] if m == "je" else not fl["z"]
                elif m in ("ja", "jbe", "jb", "jae"):
                    if not fl.get("sub"):
                        raise EvalRefused("unsigned jcc after test")
                    a, b = fl["ua"], fl["ub"]
                    take = {"ja": a > b, "jbe": a <= b, "jb": a < b, "jae": a >= b}[m]
                elif m in ("jl", "jg", "jle", "jge"):
                    if not fl.get("sub"):
                        raise EvalRefused("signed jcc after test")
                    a, b = fl["sa"], fl["sb"]
                    take = {"jl": a < b, "jg": a > b, "jle": a <= b, "jge": a >= b}[m]
                else:
                    raise EvalRefused("jcc %s" % m)
                pc = t if take else nxt
                continue
            elif m == "call":
                raise EvalRefused("call at %X not modelled" % pc)
            else:
                raise EvalRefused("mnemonic %s at %X" % (m, pc))
            pc = nxt
        raise EvalRefused("step bound")


def accepted(img, B, P, C, ids, cls=0x14):
    E = Eval(img, B, P, C)
    acc, r8, pcs = [], set(), set()
    for i in ids:
        if E.run(cls, i) & 0xFFFFFFFF:
            acc.append(i)
        r8.update(E.r8_reads)
        pcs.update(E.pcs)
    return acc, r8, pcs


def ranges_of(xs):
    out = []
    for x in sorted(xs):
        if out and x == out[-1][1] + 1:
            out[-1][1] = x
        else:
            out.append([x, x])
    return out


BOUNDARY_IDS = sorted(set([0, 1, 2, 0x113, 510, 511, 512, 534, 535, 541, 542, 543, 544, 0x7FFF, 0x8000, 0xFFFE,
                           0xFFFF]))


def checks(img, R, exhaustive=False):
    AVB = Body(img, *AV)
    CQB = Body(img, *CQ)
    ULB = Body(img, *UL)
    CTB = Body(img, *CAT)
    LCB = Body(img, *LIC)

    # ---------------- bodies and extents ----------------
    ents, ok = img.pdata_cover(*AV)
    R.check("body 002FFCF0 + 0x1DF (479 B) decodes exactly; six .pdata records tile it, the first unchained and five "
            "CHAININFO records rooted at 002FFCF0 (%s)" % ", ".join("%08X+0x%X fl%d" % (b, e - b, f) for b, e, f, r in ents),
            AVB.exact and ok and len(ents) == 6 and AV[1] - AV[0] == 479)
    R.check("002FFCF0 is int3-padded on both sides (entry - 1 and the byte after 002FFECE)",
            img.read(AV[0] - 1, 1) == b"\xcc" and img.read(AV[1], 1) == b"\xcc")
    rets, tails, outs = AVB.exits()
    R.check("002FFCF0 local CFG closed: no tail jump, no out-of-body branch; exactly two rets, 002FFDAD and 002FFECE "
            "(the last instruction)", not tails and not outs and rets == [SHARED_RET, EARLY_RET] and
            AVB.order[-1] == EARLY_RET, "rets=%s" % ["%X" % x for x in rets])
    rec = img.pdata(CQ[0])
    R.check("00322C50 + 0x401 (1025 B) decodes exactly; its single .pdata record (00322C50..003230D4) also covers the "
            "3-byte pad and the 32-entry jump table at 00323054",
            CQB.exact and rec == (CQ[0], CQ_REC_END) and img.read(CQ[1], 3) == bytes.fromhex("0f1f00") and
            JT + 32 * 4 == CQ_REC_END)
    jt = [img.u32(JT + 4 * k) + img.base for k in range(32)]
    R.check("all 32 jump-table targets are instruction boundaries inside 00322C50's code",
            all(t in CQB.ins for t in jt), str(["%X" % t for t in jt if t not in CQB.ins]))
    for nm, (s, e), n in (("00306480", UL, 1), ("003060E0", CAT, 5), ("00323EC0", LIC, 5)):
        ents, ok = img.pdata_cover(s, e)
        R.check("%s + 0x%X (%d B) decodes exactly and %d .pdata record(s) tile it" % (nm, e - s, e - s, n),
                Body(img, s, e).exact and ok and len(ents) == n)

    # ---------------- the id carrier ----------------
    R.check("002FFD0C `movzx ebx, cx`: the id is the zero-extended low 16 bits of incoming RCX, with no earlier rcx "
            "or rbx write", T(AVB, 0x2FFD0C) == "movzx ebx, cx" and writers(AVB, "rcx", AV[0], 0x2FFD0C) == [] and
            writers(AVB, "rbx", AV[0], 0x2FFD0C) == [])
    rbxw = writers(AVB, "rbx")
    R.check("002FFCF0 rbx written only at 002FFD0C and the two epilogue restores (002FFD9E, 002FFEBA)",
            rbxw == [0x2FFD0C, 0x2FFD9E, 0x2FFEBA], str(["%X" % x for x in rbxw]))
    r14w = writers(AVB, "r14")
    R.check("class-query id: 002FFD80 `movzx r14d, bx`, 002FFD84 `mov edx, r14d`; r14 written only there and at the "
            "restore 002FFD99", T(AVB, 0x2FFD80) == "movzx r14d, bx" and T(AVB, 0x2FFD84) == "mov edx, r14d" and
            r14w == [0x2FFD80, 0x2FFD99], str(["%X" % x for x in r14w]))
    R.check("002FFD0C dominates the class query 002FFD8B and no rbx/rdx writer lies between 002FFD84 and the call",
            AVB.dominates(0x2FFD0C, CQ_CALL) and
            not [x for x in on_paths(AVB, 0x2FFD0C, CQ_CALL) if x != 0x2FFD0C and "rbx" in AVB[x].reg_writes] and
            writers(AVB, "rdx", 0x2FFD85, CQ_CALL) == [])

    # ---------------- the class query call ----------------
    r8w = writers(AVB, "r8")
    R.check("class-query arguments: 002FFD75 `mov r8d, 1`, 002FFD87 `lea ecx, [r8 + 0x13]` (ECX = 0x14 = class 20), "
            "002FFD8B call 00322C50; r8 written only at 002FFD75 and 002FFE94",
            T(AVB, 0x2FFD75) == "mov r8d, 1" and T(AVB, 0x2FFD87) == "lea ecx, [r8 + 0x13]" and
            AVB[CQ_CALL].direct_target() == CQ[0] and r8w == [0x2FFD75, 0x2FFE94] and
            [a for a in AVB.order if 0x2FFD75 < a < CQ_CALL] == [0x2FFD7B, 0x2FFD80, 0x2FFD84, 0x2FFD87],
            str(["%X" % x for x in r8w]))
    R.check("the class query dominates the shared return 002FFDAD; the early return 002FFECE is not reachable from it",
            AVB.dominates(CQ_CALL, SHARED_RET) and EARLY_RET not in AVB.reach(CQ_CALL))
    P = preds(AVB)
    early_src = sorted(P.get(0x2FFEBA, ()))
    R.check("early return: 002FFEBA..002FFECE sets EAX = 2 (002FFEBF) and is entered only from the five gates before "
            "the class query", T(AVB, 0x2FFEBF) == "mov eax, 2" and
            early_src == [0x2FFD0F, 0x2FFD18, 0x2FFD32, 0x2FFD54, 0x2FFD6F] and
            writers(AVB, "rax", 0x2FFEC4, 0x2FFECF) == [], str(["%X" % x for x in early_src]))
    fail = AVB.reach(0x2FFD94)
    R.check("failed class: 002FFD90 `test eax, eax` / 002FFD92 `jne 0x2ffdae`; the fall-through 002FFD94 `mov eax, 4` "
            "reaches only the shared epilogue and ret, with no call and no further EAX write",
            T(AVB, 0x2FFD90) == "test eax, eax" and T(AVB, 0x2FFD92) == "jne 0x2ffdae" and
            T(AVB, 0x2FFD94) == "mov eax, 4" and not [x for x in fail if AVB[x].mnemonic == "call"] and
            not [x for x in fail if x != 0x2FFD94 and "rax" in AVB[x].reg_writes] and SHARED_RET in fail)

    # ---------------- zero return provenance ----------------
    D = eax_defs(AVB, SHARED_RET)
    R.check("reverse reaching definitions of EAX at 002FFDAD are exactly 002FFD94, 002FFDE6, 002FFE08 and the calls "
            "002FFE6F, 002FFE87, 002FFE9D, 002FFEB0",
            D == {0x2FFD94, 0x2FFDE6, 0x2FFE08, 0x2FFE6F, 0x2FFE87, 0x2FFE9D, 0x2FFEB0}, str(sorted("%X" % x for x in D)))
    consts = [(a, AVB[a].imm[0] if AVB[a].imm else None) for a in sorted(D) if AVB[a].mnemonic == "mov"]
    R.check("the three constant definitions are nonzero (4, 0x24, 0x2C)",
            consts == [(0x2FFD94, 4), (0x2FFDE6, 0x24), (0x2FFE08, 0x2C)], str(consts))
    gated = {}
    for c, jcc in ((0x2FFE6F, 0x2FFE7B), (0x2FFE87, 0x2FFE8E), (0x2FFE9D, 0x2FFEA4)):
        between = [a for a in AVB.order if c < a < jcc]
        okc = (AVB[jcc].mnemonic == "jne" and AVB[jcc].direct_target() == 0x2FFD99 and
               T(AVB, AVB.order[AVB.order.index(jcc) - 1]) == "test eax, eax" and
               not [a for a in between if "rax" in AVB[a].reg_writes])
        r = reach_avoid_edge(AVB, AVB.order[AVB.order.index(c) + 1], jcc, 0x2FFD99,
                             stop=set(x for x in D if x != c))
        gated[c] = okc and SHARED_RET not in r
    R.check("the call definitions 002FFE6F (0030E9C0), 002FFE87 (0031A7B0), 002FFE9D (00306480) reach the ret only "
            "through `test eax, eax; jne 0x2ffd99`, i.e. only when nonzero", all(gated.values()),
            str(dict(("%X" % k, v) for k, v in gated.items())))
    R.check("so the only definition that can give EAX 0 at 002FFDAD is 002FFEB0 call 00303BD0, followed by "
            "002FFEB5 `jmp 0x2ffd99`", AVB[0x2FFEB0].direct_target() == 0x303BD0 and T(AVB, 0x2FFEB5) == "jmp 0x2ffd99")
    R.check("002FFEB0 is unreachable once the class-success edge 002FFD92 -> 002FFDAE is removed (a normal zero return "
            "has passed class 0x14)", 0x2FFEB0 not in reach_avoid_edge(AVB, AV[0], 0x2FFD92, 0x2FFDAE) and
            0x2FFEB0 in AVB.reach(AV[0]))
    R.check("every path to 002FFEB0 also passes 00306480 (002FFE9D) and its zero arm", AVB.dominates(UL_CALL, 0x2FFEB0))

    # ---------------- inside the class query ----------------
    R.check("00322C50 entry: `lea eax, [rcx - 1]`, `cmp eax, 0x1f`, `ja` to the 0 return, image-relative table "
            "`[rdi + rax*4 + 0x203054]` with rdi = image base (00322C64 lea), indirect `jmp rcx`",
            [T(CQB, a) for a in (0x322C5A, 0x322C5F, 0x322C62, 0x322C72, 0x322C7C)] ==
            ["lea eax, [rcx - 1]", "cmp eax, 0x1f", "ja 0x322c8d", "mov ecx, dword ptr [rdi + rax*4 + 0x203054]",
             "jmp rcx"] and 0x322C6B + CQB[0x322C64].mems[0]["disp"] == img.base)
    R.check("class 0x14 selects table entry 19 = 00322F72", jt[0x14 - 1] == 0x322F72, "%X" % jt[0x14 - 1])
    R.check("class-0x14 arm loads descriptor 02EBF138 (00322F72) and count [desc+4] (00322F84); NULL -> count 0",
            0x322F79 + CQB[0x322F72].mems[0]["disp"] == DESC and T(CQB, 0x322F84) == "mov ecx, dword ptr [rcx + 4]"
            and T(CQB, 0x322F7E) == "je 0x32302a" and T(CQB, 0x32302A) == "mov ecx, eax" and
            T(CQB, 0x322F79) == "xor eax, eax")
    R.check("shared tail: 0032302C `mov edx, eax`, `cmp ebx, edx` / `jl` (signed), `lea eax, [rcx - 1]`, "
            "`cmp ebx, eax` / `jg` (signed), `mov eax, 1`; refusals go to 00322C8D `xor eax, eax`",
            [T(CQB, a) for a in (0x32302C, 0x32302E, 0x323030, 0x323036, 0x323039, 0x32303B, 0x323041, 0x322C8D)] ==
            ["mov edx, eax", "cmp ebx, edx", "jl 0x322c8d", "lea eax, [rcx - 1]", "cmp ebx, eax", "jg 0x322c8d",
             "mov eax, 1", "xor eax, eax"] and T(CQB, 0x322C5D) == "mov ebx, edx" and
            writers(CQB, "rbx") == [0x322C5D, 0x322C8F, 0x323046])
    sl = CQB.reach(CQ[0]) | CQB.reach(0x322F72) | CQB.reach(0x322C8D)
    r8s = sorted(a for a in sl if "r8" in CQB[a].reg_reads)
    R.check("static slice for class 0x14 (entry, arm 00322F72, shared tail, 0 return; %d instructions) reads no R8"
            % len(sl), not r8s and not [a for a in sl if CQB[a].mnemonic == "call"], str(["%X" % x for x in r8s]))
    allr8 = sorted(a for a in CQB.order if "r8" in CQB[a].reg_reads)
    R.note("whole 00322C50: R8 read only at %s (class-14 arm, after its own r8 writes at 00322E65/00322E6B); the "
           "class-1 arm's call 00309440 (00322C81) would receive incoming R8 unchanged" % ["%X" % x for x in allr8])

    # own evaluator
    ids = range(0x10000) if exhaustive else BOUNDARY_IDS
    try:
        acc, r8r, pcs = accepted(img, CQB, 0x10000000, 543, ids)
        exp = [i for i in ids if 0 <= i <= 542]
        R.check("own evaluator, count 543: class 0x14 accepts exactly ids %s of %d u16 ids tested, visits 00322F72, "
                "never reads R8 (poisoned)" % (ranges_of(acc), len(ids)),
                acc == exp and 0x322F72 in pcs and not r8r, "r8 reads %s" % sorted("%X" % x for x in r8r))
        R.check("own evaluator: ids 511..534 are all accepted at count 543 (in range; not zero-return feasibility)",
                all(i in acc for i in ids if 511 <= i <= 534))
        acc0, r80, _ = accepted(img, CQB, 0, 0, ids)
        R.check("own evaluator, NULL descriptor: class 0x14 refuses every id", acc0 == [] and not r80)
        acc5, _, _ = accepted(img, CQB, 0x10000000, 511, ids)
        R.check("own evaluator, count 511: accepts exactly 0..510 (the bound follows the runtime count)",
                acc5 == [i for i in ids if i <= 510], str(ranges_of(acc5)))
    except EvalRefused as e:
        R.check("own evaluator runs the class-0x14 path without refusal", False, repr(e))
    try:
        img.off(DESC)
        backed = True
    except ValueError:
        backed = False
    dsec = [s for s in img.secs if s[0] == ".data"][0]
    R.check("02EBF138 lies in .data's virtual tail (past SizeOfRawData): its load value is 0, so the count 543 is "
            "runtime-bound, a premise here", not backed and dsec[1] + dsec[4] <= DESC - img.base < dsec[1] + dsec[2])

    # ---------------- the record carrier into 00306480 ----------------
    R.check("002FFD02 `mov rsi, rdx`; 002FFD05 `mov rdi, qword ptr [rdx + 0x698]` (8-byte read of incoming RDX+698)",
            T(AVB, 0x2FFD02) == "mov rsi, rdx" and T(AVB, 0x2FFD05) == "mov rdi, qword ptr [rdx + 0x698]" and
            AVB[0x2FFD05].mems[0]["size"] == 8 and writers(AVB, "rdx", AV[0], 0x2FFD05) == [])
    rdiw = writers(AVB, "rdi")
    R.check("002FFCF0 rdi written only at 002FFD05 and the two epilogue pops (002FFDAC, 002FFECD)",
            rdiw == [0x2FFD05, 0x2FFDAC, 0x2FFECD], str(["%X" % x for x in rdiw]))
    seg = on_paths(AVB, 0x2FFD05, UL_CALL)
    R.check("002FFD05 dominates 002FFE9D and no rdi writer lies on any path between them (%d instructions)" % len(seg),
            AVB.dominates(0x2FFD05, UL_CALL) and not [x for x in seg if x != 0x2FFD05 and "rdi" in AVB[x].reg_writes])
    rel = sorted(a for a in AVB.order if any(m["base"] == "rsi" and m["disp"] == 0x698 for m in AVB[a].mems))
    R.check("the later unit+698 reloads 002FFD38 (into rcx) and 002FFDB4 (into rax) do not write rdi",
            rel == [0x2FFD38, 0x2FFDB4] and T(AVB, 0x2FFD38) == "mov rcx, qword ptr [rsi + 0x698]" and
            T(AVB, 0x2FFDB4) == "mov rax, qword ptr [rsi + 0x698]", str(["%X" % x for x in rel]))
    R.check("00306480 arguments: 002FFE94 `xor r8d, r8d`, 002FFE97 `mov rdx, rdi`, 002FFE9A `movzx ecx, bx`, "
            "002FFE9D call 00306480",
            T(AVB, 0x2FFE94) == "xor r8d, r8d" and T(AVB, 0x2FFE97) == "mov rdx, rdi" and
            T(AVB, 0x2FFE9A) == "movzx ecx, bx" and AVB[UL_CALL].direct_target() == UL[0])
    seg2 = on_paths(AVB, 0x2FFD0C, UL_CALL)
    R.check("no rbx writer on any 002FFD0C -> 002FFE9D path, so ECX there is the same low-16 id",
            not [x for x in seg2 if x != 0x2FFD0C and "rbx" in AVB[x].reg_writes])
    calls = sorted(set("%X" % AVB[x].direct_target() for x in seg if AVB[x].mnemonic == "call"))
    R.note("callees on 002FFD05 -> 002FFE9D paths (RDI/RBX kept only by the Win64 nonvolatile ABI): %s" % calls)
    recpass = sorted("%X" % x for x in seg if AVB[x].mnemonic == "call" and
                     T(AVB, AVB.order[AVB.order.index(x) - 1]) == "mov rcx, rdi")
    R.note("of those, the record pointer itself is passed in RCX to the calls at %s" % recpass)

    # ---------------- where byte +5 is read: the same record ----------------
    R.check("00306480: rbx = rdx (0030648A); no rdx or r8 write before the 003060E0 call 003064A6; rcx = rbx at the "
            "00323EC0 call 003064C5", T(ULB, 0x30648A) == "mov rbx, rdx" and
            writers(ULB, "rdx", UL[0], 0x3064A6) == [] and writers(ULB, "r8", UL[0], 0x3064A6) == [] and
            ULB[0x3064A6].direct_target() == CAT[0] and T(ULB, 0x3064C2) == "mov rcx, rbx" and
            ULB[0x3064C5].direct_target() == LIC[0] and writers(ULB, "rbx") == [0x30648A, 0x306498, 0x3064B4, 0x3064CA])
    pc1 = on_paths(CTB, 0x306101, 0x306129)
    R.check("003060E0 takes the record from RDX (00306101 `mov rdi, rdx`) and R8 into ebp (003060F8), then reads "
            "byte [rdi + 5] at 00306129; 00306101 dominates it and no rdi writer lies on any path between",
            T(CTB, 0x306101) == "mov rdi, rdx" and T(CTB, 0x3060F8) == "mov ebp, r8d" and
            T(CTB, 0x306129) == "movzx eax, byte ptr [rdi + 5]" and T(CTB, 0x30612F) == "jne 0x30632c" and
            CTB.dominates(0x306101, 0x306129) and
            not [x for x in pc1 if x != 0x306101 and "rdi" in CTB[x].reg_writes])
    pc2 = on_paths(LCB, 0x323ECD, 0x323EF3)
    R.check("00323EC0 takes the record from RCX (00323ECD `mov rsi, rcx`) and reads byte [rsi + 5] at 00323EF3; "
            "00323ECD dominates it and no rsi writer lies on any path between (the `pop rsi` at 00323EE8 is on the "
            "class-refusal return, not on these paths)",
            T(LCB, 0x323ECD) == "mov rsi, rcx" and T(LCB, 0x323EF3) == "movzx eax, byte ptr [rsi + 5]" and
            LCB.dominates(0x323ECD, 0x323EF3) and
            not [x for x in pc2 if x != 0x323ECD and "rsi" in LCB[x].reg_writes] and 0x323EE8 not in pc2)
    R.check("both downstream helpers ask class 0x14 again: 00323EC0 with R8D = 0 (00323ECA `xor r8d, r8d`, 00323ED2 "
            "`lea ecx, [r8 + 0x14]`, 00323ED6) and 003060E0 with R8D = 1 (003060FB, 00306109 `lea ecx, [r8 + 0x13]`, "
            "0030610D)",
            T(LCB, 0x323ECA) == "xor r8d, r8d" and T(LCB, 0x323ED2) == "lea ecx, [r8 + 0x14]" and
            LCB[0x323ED6].direct_target() == CQ[0] and T(CTB, 0x3060FB) == "mov r8d, 1" and
            T(CTB, 0x306109) == "lea ecx, [r8 + 0x13]" and CTB[0x30610D].direct_target() == CQ[0])
    R.check("category reason: 003060E0 returns 5 at 00306300 and 00306480 maps a nonzero 003060E0 result to 0xF "
            "(003064AF)", T(CTB, 0x306300) == "mov eax, 5" and T(ULB, 0x3064AB) == "test eax, eax" and
            T(ULB, 0x3064AD) == "je 0x3064bf" and T(ULB, 0x3064AF) == "mov eax, 0xf")


def packet_side(img, R):
    """Packet-side checks (not part of the control set): retained byte hashes, stated facts, producer commit."""
    ev = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                      "FFXII TZA", "_experiments", "evidence", SLUG)
    mism, got = [], []
    for f in ("retained/action-selector-local-exclusions/action-availability-gates-raw-01.json",
              "retained/ov42-class20-action-admission/action-admission-guards-raw-01.json"):
        for r in json.load(open(os.path.join(ev, f)))["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"]:
                mism.append(r["start"])
    R.check("retained range sha256 values equal this image's bytes (%d ranges, incl. 002FFCF0, 00322C50, 00306480, "
            "003060E0, 00323EC0)" % len(got), not mism and all(x in got for x in (AV, CQ, UL, CAT, LIC)), str(mism))
    res = json.load(open(os.path.join(ev, "result-02.json")))
    f = res["facts"]
    R.check("packet result-02 facts agree with this review: 479 B, normal returns 2FFDAD/2FFECE, call 2FFE9D -> 306480, "
            "R8D 0", f["complete_local_bytes"] == 479 and f["normal_returns"] == ["0x2ffdad", "0x2ffece"] and
            f["later_category_arguments"]["call"] == "0x2ffe9d" and f["later_category_arguments"]["target"] == "0x306480"
            and f["later_category_arguments"]["R8D"] == 0 and res["exe_sha256"] == SHA_PIN)
    root = os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))
    root = os.path.dirname(os.path.dirname(root))
    try:
        sub = subprocess.run(["git", "-C", root, "log", "-1", "--format=%h %s", PRODUCER], capture_output=True,
                             text=True).stdout.strip()
        com = subprocess.run(["git", "-C", root, "show", "%s:Database/FFXII TZA/_experiments/evidence/%s/manifest.json"
                              % (PRODUCER, SLUG)], capture_output=True).stdout
    except Exception as e:
        sub, com = repr(e), b""
    R.check("producer commit %s is ASTRA's and its committed manifest hashes to the working-tree manifest" % PRODUCER,
            sub.startswith(PRODUCER) and " ASTRA:" in sub and hashlib.sha256(com).hexdigest() == MANIFEST_SHA, sub)


CONTROLS = [
    ("002FFD0C `movzx ebx, cx` -> `movsx ebx, cx` (sign-extended id)", 0x2FFD0C, bytes.fromhex("0fbfd9")),
    ("002FFD87 `lea ecx, [r8+0x13]` -> [r8+0x14] (class 0x15)", 0x2FFD8A, bytes([0x14])),
    ("002FFD75 `mov r8d, 1` -> `mov r8d, 2` (R8D and the class both change)", 0x2FFD77, bytes([0x02])),
    ("002FFD92 class-success `jne` -> `je` (failed class falls into the cascade)", 0x2FFD92, bytes([0x74])),
    ("002FFD94 `mov eax, 4` -> `xor eax, eax` + 3 nops (failed class returns 0)", 0x2FFD94, bytes.fromhex("31c0909090")),
    ("002FFD05 carrier `[rdx+0x698]` -> `[rdx+0x6a0]`", 0x2FFD08, bytes([0xA0])),
    ("002FFDB4 reload `mov rax, [rsi+0x698]` -> `mov rdi, [rsi+0x698]` (a later reload replaces RDI)", 0x2FFDB4,
     bytes.fromhex("488bbe98060000")),
    ("002FFE97 `mov rdx, rdi` -> `mov rdx, rsi` (outer unit passed)", 0x2FFE97, bytes.fromhex("488bd6")),
    ("002FFE94 `xor r8d, r8d` -> `mov r8d, ebx` (R8D = id)", 0x2FFE94, bytes.fromhex("448bc3")),
    ("002FFE9A `movzx ecx, bx` -> `movsx ecx, bx`", 0x2FFE9A, bytes.fromhex("0fbfcb")),
    ("00322F84 `mov ecx, [rcx+4]` -> `mov ecx, r8d` (class-0x14 arm reads R8)", 0x322F84, bytes.fromhex("4489c1")),
    ("0032303B `jg` -> `jge` (upper bound becomes count-2)", 0x32303C, bytes([0x8D])),
    ("00322F72 descriptor disp + 8 (another registry slot)", 0x322F75, None),
    ("00306101 `mov rdi, rdx` -> `mov rdi, rcx` (003060E0 reads byte +5 off another carrier)", 0x306101,
     bytes.fromhex("488bf9")),
]


def main():
    img = Img.load()
    R = Rep("rv_avail")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    print("== shipping-image re-derivation")
    checks(img, R, exhaustive=True)
    packet_side(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    same = img.patched(AV[0], img.read(AV[0], 4))
    checks(same, Rn, exhaustive=False)
    R.check("null control: an unchanged private copy (sha check off) passes every image check (boundary id set)",
            Rn.fails == 0 and Rn.n > 0, "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
        if nb is None:
            d = struct.unpack("<i", img.read(va, 4))[0] + 8
            nb = struct.pack("<i", d)
        Pimg = img.patched(va, nb)
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(Pimg, Rc, exhaustive=False)
            failed = Rc.fails
            why = "%d failed: %s" % (failed, "; ".join(Rc.failed[:3]))
        except Exception as e:
            failed = 1
            why = "refused: %r" % e
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
