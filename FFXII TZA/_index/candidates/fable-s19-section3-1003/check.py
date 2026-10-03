"""check.py - FABLE's byte check of OPUS's five points on CONTRACT-separation-pass.md section 3 (2026-10-03,
OPUS-REQ-FABLE-S19-SEPARATION-CONTRACT-1003).

Three parts:
  A. A raw reference census of MovementBody field accesses across every function the image gives a body
     pointer to (not only the separation pass), with a known-answer control on the census itself.
  B. One check per point. Each has three legs:
       NEW      the corrected reading, tested on the shipping image            (must hold)
       OLD      the reading being corrected, tested on the same bytes          (must NOT hold)
       MUTANT   NEW re-tested on a private copy with the deciding byte changed (must NOT hold),
                so the check is sensitive to the defect it guards against.
  C. A citation pre-check: every .text address that apply.py inserts into a page lies in a function that
     page already cites, so the neighbour gate gains no edge.

Reads only the shipping image (sha256-checked by rvlib) and git HEAD. Writes nothing. Prints FAILS N last.
"""
import collections
import os
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True   # importing apply.py and rvlib must leave no __pycache__ behind
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
sys.path.insert(0, HERE)
from rvlib import Img, Insn, fam  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM  # noqa: E402

FAILS = []


def ok(cond, label, detail=""):
    print("  %-4s %s%s" % ("ok" if cond else "FAIL", label, ("  -- " + detail) if detail else ""))
    if not cond:
        FAILS.append(label)
    return cond


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


# =====================================================================================================
# A. the census
# =====================================================================================================
POOL = 0x02B4E4C0
STRIDE = 0x130
POOL_END = POOL + STRIDE * 128
VOLATILE = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
ARGS = ("rcx", "rdx", "r8", "r9")
RET_BODY = {0x003DA8A0}                       # the allocator returns the new body in rax
CALLBACK_SEEDS = [0x00314F30, 0x00314F50]     # the visit calls the pair callback through a register
TERMINATORS = ("ret", "jmp", "ud2", "int3")


class Census(object):
    """Body-pointer taint over every function unit of the image.

    Sources: the pool base 02B4E4C0 with an index * 0x130 (pool); a qword load from [X + 0x138] where X was
    loaded from [Y + 0xC0] in the same function, i.e. the actor's secondary context (ctx138) - any other
    [X + 0x138] load is kept apart as p138 and dispositioned by hand; the allocator's return (ret); the
    resolver callback's two arguments (cb); and, by a fixpoint, every callee that receives a body-derived
    pointer in rcx/rdx/r8/r9 with its offset (arg<...). Per function: a forward pass in address order with
    union at branch targets, run twice for back-edges; spills through [rsp + d] are followed."""

    def __init__(self, img):
        self.img = img
        self.cs = img.cs
        self.lite = Cs(CS_ARCH_X86, CS_MODE_64)
        self.lite.skipdata = True
        self.cache = {}
        self.weak_sources = []
        self.escapes = []
        self._units()

    def _units(self):
        img = self.img
        po = img.off(img.base + img.exc_rva)
        ents = []
        for i in range(img.exc_size // 12):
            b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
            b += img.base
            e += img.base
            ui = img.off(img.base + u)
            fl = img.d[ui] >> 3
            n = img.d[ui + 2]
            root = b
            if fl & 4:
                co = ui + 4 + ((n + 1) & ~1) * 2
                root = struct.unpack_from("<I", img.d, co)[0] + img.base
            ents.append((b, e, root))
        ents.sort()
        link = dict((b, r) for b, e, r in ents)

        def rootof(b):
            r, seen = link.get(b, b), 0
            while r in link and link[r] != r and seen < 16:
                r, seen = link[r], seen + 1
            return r
        units = collections.defaultdict(list)
        for b, e, r in ents:
            units[rootof(b)].append((b, e))
        text = [s for s in img.secs if s[0] == ".text"][0]
        lo, hi = img.base + text[1], img.base + text[1] + text[2]
        cur, gaps = lo, []
        for b, e, r in ents:
            if b > cur:
                gaps.append((cur, b))
            cur = max(cur, e)
        gaps.append((cur, hi))
        # leaf functions have no .pdata: split each gap into runs at int3 padding
        for gb, ge in gaps:
            start, last = None, gb
            for a, sz, m, o in self.lite.disasm_lite(img.read(gb, ge - gb), gb):
                if m in ("int3", ".byte"):
                    if start is not None:
                        units[start].append((start, a))
                        start = None
                elif start is None:
                    start = a
                last = a + sz
            if start is not None:
                units[start].append((start, last))
        self.units = units
        self.piece_index = sorted((b, e, s) for s, ps in units.items() for b, e in ps)
        self.piece_starts = [p[0] for p in self.piece_index]

    def unit_of(self, va):
        import bisect
        i = bisect.bisect_right(self.piece_starts, va) - 1
        if i >= 0:
            b, e, s = self.piece_index[i]
            if b <= va < e:
                return s
        return None

    def insns(self, start):
        if start in self.cache:
            return self.cache[start]
        pieces = self.units.get(start)
        if pieces is None:
            pieces = [(start, e) for b, e, s in self.piece_index if b <= start < e][:1]
        out = []
        for b, e in sorted(pieces):
            for ci in self.cs.disasm(self.img.read(b, e - b), b):
                out.append(Insn(self.cs, ci))
        self.cache[start] = out
        return out

    def run(self, start, seeds, record, calls_out):
        L = self.insns(start)
        if not L:
            return
        lo_a, hi_a = L[0].address, L[-1].address

        def empty():
            return ({}, set(), set(), {}, set())

        def copy(st):
            return (dict((k, set(v)) for k, v in st[0].items()), set(st[1]), set(st[2]), dict(st[3]), set(st[4]))

        def union(a, b):
            if a is None:
                return copy(b)
            T = dict((k, set(v)) for k, v in a[0].items())
            for k, v in b[0].items():
                T.setdefault(k, set()).update(v)
            sl = {}
            for k in set(a[3]) | set(b[3]):
                sl[k] = set(a[3].get(k, ())) | set(b[3].get(k, ()))
            return (T, a[1] | b[1], a[2] | b[2], sl, a[4] | b[4])

        at = {}
        for _pass in range(2):
            st = empty()
            for r, v in seeds.items():
                st[0][r] = set([v])
            reachable = True
            union_all = copy(st)
            for ins in L:
                a = ins.address
                if a in at:
                    st = union(st, at[a]) if reachable else copy(at[a])
                elif not reachable:
                    st = copy(union_all)
                reachable = True
                self._step(ins, st, start, record, calls_out, lo_a, hi_a)
                union_all = union(union_all, st)
                m = ins.mnemonic
                if m.startswith("j") and ins.ci.operands and ins.ci.operands[0].type == X86_OP_IMM:
                    t = ins.ci.operands[0].imm
                    if lo_a <= t <= hi_a:
                        at[t] = union(at.get(t), st)
                if m in TERMINATORS:
                    reachable = False

    def _step(self, ins, st, start, record, calls_out, lo_a, hi_a):
        T, P, S, slots, Cx = st
        m = ins.mnemonic
        ci = ins.ci
        ops = ci.operands
        nxt = ins.address + ins.size
        for mm in ins.mems:
            if m in ("lea", "nop") or m.startswith("prefetch"):
                break
            b, ix, d, sz = mm["base"], mm["index"], mm["disp"], mm["size"]
            bf = fam(b) if b else None
            ixf = fam(ix) if ix else None
            hits = []
            if b == "rip":
                tgt = nxt + d
                if POOL <= tgt < POOL_END:
                    hits.append(((tgt - POOL) % STRIDE, "pool-rip"))
            else:
                if bf in T:
                    for off, cls in T[bf]:
                        hits.append((off + d, cls + ("+idx" if ixf else "")))
                if ixf in T and mm["scale"] == 1 and bf not in T:
                    for off, cls in T[ixf]:
                        hits.append((off + d, cls + "+base"))
                if (bf in P and ixf in S) or (bf in S and ixf in P):
                    hits.append((d % STRIDE, "pool"))
            if hits:
                rw = ("r" if mm["read"] else "") + ("w" if mm["write"] else "")
                if m in ("cmp", "test", "ucomiss", "comiss", "bt"):
                    rw = "r"
                for off, cls in hits:
                    record.append((start, ins.address, off, sz, rw or "?", ins.text, cls))
        dst = fam(ci.reg_name(ops[0].reg)) if ops and ops[0].type == X86_OP_REG else None

        def kill(r):
            T.pop(r, None)
            P.discard(r)
            S.discard(r)
            Cx.discard(r)

        if m == "call":
            tgt = ops[0].imm if ops and ops[0].type == X86_OP_IMM else None
            argt = dict((r, frozenset(T[r])) for r in ARGS if r in T)
            if tgt is not None and argt:
                calls_out.append((start, ins.address, tgt, argt))
            for r in VOLATILE:
                kill(r)
            if tgt in RET_BODY:
                T["rax"] = set([(0, "ret")])
            return
        if m == "jmp":
            if ops and ops[0].type == X86_OP_IMM and not (lo_a <= ops[0].imm <= hi_a):
                argt = dict((r, frozenset(T[r])) for r in ARGS if r in T)
                if argt:
                    calls_out.append((start, ins.address, ops[0].imm, argt))
            return
        if m == "lea" and dst:
            mm = ins.mems[0]
            b, ix, d = mm["base"], mm["index"], mm["disp"]
            bf = fam(b) if b else None
            ixf = fam(ix) if ix else None
            newv, newP = set(), False
            if b == "rip":
                t = nxt + d
                if t == POOL:
                    newP = True
                elif POOL < t < POOL_END:
                    newv.add(((t - POOL) % STRIDE, "pool"))
            else:
                if bf in T and ix is None:
                    newv |= set((o + d, c) for o, c in T[bf])
                if (bf in P and ixf in S) or (bf in S and ixf in P):
                    newv.add((d, "pool"))
            kill(dst)
            if newv:
                T[dst] = newv
            if newP:
                P.add(dst)
            return
        if m in ("mov", "movabs") and dst and len(ops) == 2:
            src = ops[1]
            full = ci.reg_name(ops[0].reg) == dst
            if src.type == X86_OP_REG:
                sf = fam(ci.reg_name(src.reg))
                tv, isP, isS, isC = (set(T[sf]) if sf in T else None), sf in P, sf in S, sf in Cx
                kill(dst)
                if isC and full:
                    Cx.add(dst)
                if tv and full:
                    T[dst] = tv
                if isP and full:
                    P.add(dst)
                if isS:
                    S.add(dst)
                return
            if src.type == X86_OP_MEM:
                mm = ins.mems[0]
                bf = fam(mm["base"]) if mm["base"] else None
                base_is_ctx = bf in Cx
                kill(dst)
                if mm["disp"] == 0x138 and mm["index"] is None and mm["size"] == 8 and bf not in ("rsp", "rip"):
                    T[dst] = set([(0, "ctx138" if base_is_ctx else "p138")])
                    if not base_is_ctx:
                        self.weak_sources.append((start, ins.address, ins.text))
                elif mm["disp"] == 0xC0 and mm["index"] is None and mm["size"] == 8 and bf not in ("rsp", "rip"):
                    Cx.add(dst)
                elif bf == "rsp" and mm["size"] == 8 and mm["index"] is None and slots.get(mm["disp"]):
                    T[dst] = set(slots[mm["disp"]])
                return
        if m == "mov" and ops and ops[0].type == X86_OP_MEM and len(ops) == 2:
            mm = ins.mems[0]
            if ops[1].type == X86_OP_REG and mm["size"] == 8 and mm["base"] != "rsp":
                sf = fam(ci.reg_name(ops[1].reg))
                if sf in T and any("p138" not in c for o, c in T[sf]):
                    self.escapes.append((start, ins.address, ins.text, tuple(sorted(T[sf]))))
            if mm["base"] == "rsp" and mm["index"] is None:
                if ops[1].type == X86_OP_REG and fam(ci.reg_name(ops[1].reg)) in T and mm["size"] == 8:
                    slots[mm["disp"]] = set(T[fam(ci.reg_name(ops[1].reg))])
                else:
                    slots.pop(mm["disp"], None)
            return
        if m == "imul" and dst and len(ops) == 3 and ops[2].type == X86_OP_IMM and ops[2].imm == STRIDE:
            kill(dst)
            S.add(dst)
            return
        if m in ("add", "sub") and dst and len(ops) == 2:
            src = ops[1]
            if src.type == X86_OP_IMM and dst in T:
                k = src.imm if m == "add" else -src.imm
                T[dst] = set(((o + k) % STRIDE if c.startswith("pool") else o + k, c) for o, c in T[dst])
                return
            if m == "add" and src.type == X86_OP_REG:
                sf = fam(ci.reg_name(src.reg))
                if (dst in S and sf in P) or (dst in P and sf in S):
                    kill(dst)
                    T[dst] = set([(0, "pool")])
                    return
        if m == "xchg" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
            a_, b_ = fam(ci.reg_name(ops[0].reg)), fam(ci.reg_name(ops[1].reg))
            ta, tb = T.pop(a_, None), T.pop(b_, None)
            if ta:
                T[b_] = ta
            if tb:
                T[a_] = tb
            return
        for r in ins.reg_writes:
            if r not in ("rsp", "rip", "rflags"):
                kill(r)

    def census(self):
        record, calls = [], []
        pat138 = re.compile(r"^\w+, qword ptr \[r\w+ \+ 0x138\]$")
        img = self.img
        selfseeded = []
        for start, pieces in self.units.items():
            hit = False
            for b, e in pieces:
                for a, sz, m, o in self.lite.disasm_lite(img.read(b, e - b), b):
                    if m == "mov" and pat138.match(o):
                        hit = True
                        break
                    mm = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", o)
                    if mm:
                        t = a + sz + int(mm.group(2), 16) * (1 if mm.group(1) == "+" else -1)
                        if POOL <= t < POOL_END:
                            hit = True
                            break
                if hit:
                    break
            if hit:
                selfseeded.append(start)
                self.run(start, {}, record, calls)
        work = [(f, (("rcx", (0, "cb")), ("rdx", (0, "cb")))) for f in CALLBACK_SEEDS]
        seen = set()
        i = 0
        while i < len(calls) or work:
            if work:
                tgt, argt = work.pop()
            else:
                f, site, tgt, a = calls[i]
                i += 1
                for r, vals in sorted(a.items()):
                    for v in sorted(vals):
                        work.append((tgt, ((r, (v[0], v[1] if v[1].startswith("arg") else "arg<" + v[1])),)))
                continue
            key = (tgt, argt)
            if key in seen:
                continue
            seen.add(key)
            self.run(tgt, dict(argt), record, calls)
        self.record, self.calls, self.selfseeded = record, calls, selfseeded
        return record


def dedup(recs):
    seen, out = set(), []
    for r in sorted(recs, key=lambda r: (r[2], r[1], r[6])):
        k = (r[1], r[2])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def covering(recs, lo, hi):
    """records whose access [off, off+size) overlaps [lo, hi)"""
    return [r for r in recs if r[2] < hi and r[2] + max(r[3], 1) > lo]


def strict(recs):
    return [r for r in recs if "p138" not in r[6]]


def weak(recs):
    return [r for r in recs if "p138" in r[6]]


def show(recs, indent="      "):
    for (f, a, off, sz, rw, text, cls) in recs:
        print("%s+0x%03X w%-2d %-2s %08X in %08X  %-13s %s" % (indent, off, sz, rw, a, f, cls, text))


# =====================================================================================================
# helpers for the point checks
# =====================================================================================================
def at(img, va):
    ci = next(img.cs.disasm(img.read(va, 16), va))
    return Insn(img.cs, ci)


def mem0(ins):
    return ins.mems[0] if ins.mems else None


def is_access(img, va, mnem, base, disp, size, regsrc=None):
    i = at(img, va)
    m = mem0(i)
    good = (i.mnemonic == mnem and m is not None and m["base"] == base and m["disp"] == disp
            and m["index"] is None and m["size"] == size)
    if regsrc is not None:
        good = good and regsrc in i.op_str
    return good, i.text


def rip_target(ins):
    m = mem0(ins)
    return ins.address + ins.size + m["disp"] if m and m["base"] == "rip" else None


def const_f32(img, va):
    i = at(img, va)
    return struct.unpack("<f", img.read(rip_target(i), 4))[0]


def linear(img, lo, hi):
    return [Insn(img.cs, ci) for ci in img.cs.disasm(img.read(lo, hi - lo), lo)]


# the resolver's contact tail: from the merge point after the three share arms to the jump back
TAIL_LO, TAIL_HI = 0x003152B2, 0x00315372


def emulate_tail(img, w, sx, sz, A, B):
    """Run 003152B2..00315372 on scalar floats. rbx = A, rdi = B (the resolver's prologue, checked in P2).
    xmm4 = w (A's share), xmm10/xmm11 = the separation's x/z, xmm12 = the constant 1.0 loaded at 00315055."""
    one = const_f32(img, 0x00315055)
    x = {"xmm4": f32(w), "xmm10": f32(sx), "xmm11": f32(sz), "xmm12": one}
    mem = {"rbx": A, "rdi": B}
    for i in linear(img, TAIL_LO, TAIL_HI):
        ops = i.ci.operands
        m = i.mnemonic
        if m == "mov" and ops[0].type == X86_OP_REG:
            continue                                            # mov eax, 1 (the return value)

        def val(op):
            if op.type == X86_OP_REG:
                return x[i.ci.reg_name(op.reg)]
            mm = mem0(i)
            if mm["base"] == "rip":
                return struct.unpack("<f", img.read(rip_target(i), 4))[0]
            return mem[mm["base"]].get(mm["disp"], 0.0)
        if m == "movaps" and ops[0].type == X86_OP_REG:
            x[i.ci.reg_name(ops[0].reg)] = val(ops[1])
        elif m in ("mulss", "addss", "subss"):
            d = i.ci.reg_name(ops[0].reg)
            s = val(ops[1])
            x[d] = f32(x[d] * s if m == "mulss" else x[d] + s if m == "addss" else x[d] - s)
        elif m == "movss" and ops[0].type == X86_OP_MEM:
            mm = mem0(i)
            mem[mm["base"]][mm["disp"]] = x[i.ci.reg_name(ops[1].reg)]
        elif m == "movss" and ops[0].type == X86_OP_REG:
            x[i.ci.reg_name(ops[0].reg)] = val(ops[1])
        elif m == "mov" and ops[0].type == X86_OP_MEM:
            mm = mem0(i)
            mem[mm["base"]][mm["disp"]] = ops[1].imm
        else:
            raise SystemExit("emulate_tail: unsupported %08X %s" % (i.address, i.text))
    return A, B


def run_tail(img, w):
    A0 = {0x100: 0.25, 0x108: -0.5, 0xE8: 123.0, 0xEC: 0}
    B0 = {0x100: -0.75, 0x108: 0.125, 0xE8: 456.0, 0xEC: 0}
    A, B = emulate_tail(img, w, 0.7, -0.4, dict(A0), dict(B0))
    incA = (A[0x100] - A0[0x100], A[0x108] - A0[0x108])
    incB = (B[0x100] - B0[0x100], B[0x108] - B0[0x108])
    return A, B, incA, incB


def close(a, b):
    return abs(a - b) <= 1e-5 * max(1.0, abs(a), abs(b))


def no_writes(img, reg, ranges, allow=()):
    for lo, hi in ranges:
        for i in linear(img, lo, hi):
            if reg in i.ci.regs_access()[1] and i.address not in allow:
                return False, "%08X %s" % (i.address, i.text)
    return True, ""


def reg_written(img, reg, ranges, allow=()):
    for lo, hi in ranges:
        for i in linear(img, lo, hi):
            names = [i.ci.reg_name(r) for r in i.ci.regs_access()[1]]
            if reg in names and i.address not in allow:
                return "%08X %s" % (i.address, i.text)
    return None


# =====================================================================================================
# B. the five points
# =====================================================================================================
def p1_new(img, recs):
    g = []
    g.append(at(img, 0x003DB052).text == "lea rcx, [rdi + 0x120]" and at(img, 0x003DB068).text == "call 0x46ad20")
    a, _ = is_access(img, 0x003DB078, "mov", "rdi", 0x120, 4, "edx")
    g.append(a)
    g.append(rip_target(at(img, 0x003DB094)) == 0x02B57CE0)
    g.append(at(img, 0x003DB0A3).text == "test dl, 1" and at(img, 0x003DB0AB).text == "add rcx, 0x10"
             and at(img, 0x003DB0AF).text == "shr edx, 1" and at(img, 0x003DB0B1).text == "jne 0x3db0a3")
    a, _ = is_access(img, 0x003DACAF, "mov", "rbx", 0x120, 4, "ecx")
    g.append(a and at(img, 0x003DACB8).text == "call 0x3daab0")
    if recs is not None:
        reads120 = [r for r in covering(strict(recs), 0x120, 0x124) if "r" in r[4]]
        g.append(bool(reads120) and all(r[3] == 4 for r in reads120))
        w124 = [r for r in covering(strict(recs), 0x124, 0x128) if r[3] == 4 and "w" in r[4]]
        r124 = [r for r in covering(strict(recs), 0x124, 0x128) if "r" in r[4]]
        g.append(bool(w124) and not r124)
        f = covering(strict(recs), 0x128, 0x130)
        g.append(all(r[3] == 8 and "w" in r[4] or "movss" in r[5] for r in f) and any("r" in r[4] for r in f))
    return all(g), g


def p1_old(img, recs):
    """u128 cell set: some read of the cell set wider than a dword, or a walk over more than 32 bits"""
    wide = [r for r in covering(strict(recs), 0x120, 0x130) if "r" in r[4] and r[3] >= 8]
    loop_is_wide = at(img, 0x003DB0AF).text in ("shr rdx, 1",)
    return bool(wide) or loop_is_wide


def p2_new(img, recs):
    g = []
    g.append(at(img, 0x00314F72).text == "mov rdi, rdx" and at(img, 0x00314F75).text == "mov rbx, rcx")
    for w in (0.3, 0.8):
        A, B, incA, incB = run_tail(img, w)
        g.append(close(B.get(0xE8), incA[0] ** 2 + incA[1] ** 2))     # B's +0xE8 = |A's increment|^2
        g.append(close(A.get(0xE8), incB[0] ** 2 + incB[1] ** 2))     # A's +0xE8 = |B's increment|^2
    if recs is not None:
        in_resolver = [r for r in covering(strict(recs), 0xE8, 0xEC) if r[0] == 0x00314F50]
        g.append(bool(in_resolver) and all(r[4] == "w" and r[5].startswith("movss") for r in in_resolver))
        readers = [r for r in covering(strict(recs), 0xE8, 0xEC) if "r" in r[4]]
        g.append(sorted(set(r[1] for r in readers)) == [0x002E53B4])
    return all(g), g


def p2_old(img, recs):
    """own push length: a body's +0xE8 equals the square of ITS OWN increment (or an accumulated sum)"""
    A, B, incA, incB = run_tail(img, 0.3)
    own = close(A.get(0xE8), incA[0] ** 2 + incA[1] ** 2) or close(B.get(0xE8), incB[0] ** 2 + incB[1] ** 2)
    acc = close(A.get(0xE8), 123.0 + incA[0] ** 2 + incA[1] ** 2)
    return own or acc


def p3_new(img, recs):
    g = []
    for va, reg in ((0x00315017, "rcx"), (0x0031502A, "rdx")):
        a, _ = is_access(img, va, "movss", reg, 8, 4)
        g.append(a)
    if recs is not None:
        acc = covering(strict(recs), 0x08, 0x0C)
        for r in acc:
            i = at(img, r[1])
            if i.mnemonic in ("movss", "addss", "subss", "mulss", "comiss", "ucomiss"):
                g.append(r[3] == 4)
            elif i.mnemonic == "mov" and i.imm:
                g.append(r[3] == 4 and struct.unpack("<f", struct.pack("<I", i.imm[0] & 0xFFFFFFFF))[0] == 1.0)
            else:
                g.append(False)
        g.append(len(acc) >= 5)
    return all(g), g


INT_MNEM = set("and or xor test cmp add sub inc dec shl shr sar bt bts btr movzx movsx imul".split())


def p3_old(img, recs):
    """untyped / integer (the census's uint32): some access to +0x08 is an integer operation or a GPR load"""
    for r in covering(strict(recs), 0x08, 0x0C):
        i = at(img, r[1])
        if i.mnemonic in INT_MNEM:
            return True
        if i.mnemonic == "mov" and i.ci.operands[0].type == X86_OP_REG:
            return True
    return False


def p4_new(img, recs):
    g = []
    # the consumer reads +0x104 alone and adds it to the delta's middle float, between x and z
    a1, _ = is_access(img, 0x002E53F1, "movss", "rdx", 0x104, 4)
    a2, _ = is_access(img, 0x002E53F9, "addss", "r9", 4, 4)
    a3, _ = is_access(img, 0x002E53FF, "movss", "r9", 4, 4)
    ax, _ = is_access(img, 0x002E53DF, "movss", "rdx", 0x100, 4)
    ax2, _ = is_access(img, 0x002E53E7, "addss", "r9", 0, 4)
    az, _ = is_access(img, 0x002E5405, "movss", "rdx", 0x108, 4)
    az2, _ = is_access(img, 0x002E540D, "addss", "r9", 8, 4)
    g += [a1, a2, a3, ax, ax2, az, az2]
    # the clear zeroes +0x100..+0x107 as one qword of a zeroed rax
    g.append(at(img, 0x003DA9F0).text == "xor eax, eax" and at(img, 0x003DA9F2).text == "mov qword ptr [rcx + 0x100], rax")
    if recs is not None:
        acc = covering(strict(recs), 0x104, 0x108)
        writes = [r for r in acc if "w" in r[4]]
        reads = [r for r in acc if "r" in r[4]]
        g.append(bool(writes) and all(r[3] == 8 and r[2] == 0x100 for r in writes))     # only qword zeros
        g.append([r[1] for r in reads] == [0x002E53F1])
        six = (0x003DAA40, 0x003DAC70, 0x003DAAB0, 0x003DAB50, 0x00314F50, 0x003DA9F0, 0x00314E10)
        alone_in_pass = [r for r in acc if r[0] in six and not (r[2] == 0x100 and r[3] == 8)]
        g.append(not alone_in_pass)                                                       # OPUS's narrow claim
    return all(g), g


def p4_old(img, recs):
    """(a) OPUS's wide reading, 'never accessed alone', applied image-wide;
       (b) 'third component' read as vector index 2: +0x104 added into the delta's third float"""
    alone = [r for r in covering(strict(recs), 0x104, 0x108) if r[2] == 0x104 and r[3] == 4]
    third, _ = is_access(img, 0x002E53F9, "addss", "r9", 8, 4)
    return (not alone), third


def p5_arms(img):
    """which body each share arm marks, and which body the tail then pushes"""
    g = []
    g.append(at(img, 0x00315249).text == "ucomiss xmm4, xmm7")
    g.append(at(img, 0x0031526C).text == "ucomiss xmm4, xmm12")
    g.append(at(img, 0x00314F94).text == "xorps xmm7, xmm7")
    g.append(const_f32(img, 0x00315055) == 1.0)
    path7 = [(0x00314F95, 0x0031515C), (0x003151BD, 0x00315249)]
    path12 = [(0x0031505E, 0x0031515C), (0x003151BD, 0x0031526C)]
    g.append(reg_written(img, "xmm7", path7) is None)
    g.append(reg_written(img, "xmm12", path12) is None)
    arm0 = at(img, 0x00315263)       # w == 0
    arm1 = at(img, 0x00315287)       # w == 1
    sh_b = at(img, 0x003152A4)
    sh_a = at(img, 0x003152AB)
    return g, arm0, arm1, sh_b, sh_a


def p5_new(img, recs):
    g, arm0, arm1, sh_b, sh_a = p5_arms(img)
    base = {"rbx": "A", "rdi": "B"}

    def marked(ins, val):
        m = mem0(ins)
        if ins.mnemonic != "mov" or m is None or m["disp"] != 0xEE or m["size"] != 1 or not ins.imm or ins.imm[0] != val:
            return None
        return base.get(m["base"])
    m0, m1 = marked(arm0, 1), marked(arm1, 1)
    _, _, iA0, iB0 = run_tail(img, 0.0)
    _, _, iA1, iB1 = run_tail(img, 1.0)
    took0 = "B" if (iA0 == (0.0, 0.0) and iB0 != (0.0, 0.0)) else ("A" if iB0 == (0.0, 0.0) else None)
    took1 = "A" if (iB1 == (0.0, 0.0) and iA1 != (0.0, 0.0)) else ("B" if iA1 == (0.0, 0.0) else None)
    g.append(m0 is not None and m0 == took0)          # w = 0: the marked body is the one that took the push
    g.append(m1 is not None and m1 == took1)          # w = 1: likewise
    g.append(set([marked(sh_b, 0), marked(sh_a, 0)]) == set(["A", "B"]))
    if recs is not None:
        acc = covering(strict(recs), 0xEE, 0xEF)
        reads = sorted(set(r[1] for r in acc if "r" in r[4]))
        g.append(reads == [0x002E53C6])
        byte_w = sorted(set(r[1] for r in acc if "w" in r[4] and r[3] == 1))
        g.append(byte_w == [0x00315263, 0x00315287, 0x003152A4, 0x003152AB, 0x003DAA0C])
    return all(g), g


def p5_old(img, recs):
    """'immovable' marker: the w = 0 / w = 1 arms mark the body that does NOT move"""
    g, arm0, arm1, sh_b, sh_a = p5_arms(img)
    base = {"rbx": "A", "rdi": "B"}
    _, _, iA0, iB0 = run_tail(img, 0.0)
    stayed0 = "A" if iA0 == (0.0, 0.0) else "B"
    return base.get(mem0(arm0)["base"]) == stayed0


def patch_modrm_rm(img, va, rm_new, opcode_len):
    """change the r/m field of the ModRM byte at va + opcode_len"""
    o = img.read(va, 16)
    modrm = o[opcode_len]
    return img.patched(va + opcode_len, bytes([(modrm & 0xF8) | rm_new]))


def patch_disp32(img, va, disp_off, new):
    return img.patched(va + disp_off, struct.pack("<I", new))


# =====================================================================================================
# C. citation pre-check
# =====================================================================================================
HEXRE = re.compile(r"(?<![0-9A-Fa-fx])([0-9A-F]{8})(?![0-9A-Fa-f])")


def cited_units(cen, text):
    out = {}
    for h in HEXRE.findall(text):
        va = int(h, 16)
        u = cen.unit_of(va)
        if u is not None:
            out.setdefault(u, set()).add(va)
    return out


def head_text(rel):
    db = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
    r = subprocess.run(["git", "show", "HEAD:./" + rel], cwd=db, capture_output=True)
    return r.stdout.decode("utf-8").replace("\r\n", "\n") if r.returncode == 0 else None


# weak (+0x138 not from a secondary context) roots whose propagated hits land in the corrected ranges, each
# dispositioned by the base register's provenance in the root function, printed below
WEAK_ROOTS = {
    0x006E5A20: "frame pointer (rbp = rax - 0x328 after mov rax, rsp): a stack slot",
    0x00744B90: "frame pointer (rbp = rsp - 0xFD8): a stack slot",
    0x007467E0: "frame pointer (rbp = rsp - 0x798): a stack slot",
    0x0074BA10: "frame pointer (rbp = rax - 0x78 after mov rax, rsp): a stack slot",
    0x003FE720: "a global object pointer (rip-relative), table indexed by r9: the item-compatibility code",
    0x003FEAD0: "a global object pointer (rip-relative), table indexed by r9: the item-compatibility code",
    0x00283BB0: "[rbx+0x60] holds sibling pointers at +0x128/+0x130/+0x138 whose +8 is a flag dword: widget code",
    0x00283E40: "[rbx+0x60] holds sibling pointers at +0x128/+0x130/+0x138 whose +8 is a flag dword: widget code",
    0x005528C0: "its own rcx argument (map-screen code); the pointee's +8 is read as a word and a qword",
    0x007EAA60: "its own rcx argument: the SEAD sound driver (third-party)",
    0x007EBAD0: "a spilled object of the SEAD sound driver (third-party)",
    0x008999C0: "rdx at entry of a stub that also does lea rcx, [rdx+0x30] / jmp: not a context",
    0x0055DBD0: "its own rcx argument: license-board widget code",
    0x00561800: "its own rcx argument: license-board widget code",
}


def main():
    img = Img.load()
    print("image sha256 ok (rvlib)")
    git = subprocess.run(["git", "rev-parse", "--short=9", "HEAD"], cwd=HERE, capture_output=True, text=True)
    print("HEAD %s" % git.stdout.strip())

    print("\n== A. raw reference census of MovementBody accesses (whole image)")
    cen = Census(img)
    recs = cen.census()
    recs = dedup(recs)
    fns_all = sorted(set(r[0] for r in recs))
    fns_strict = sorted(set(r[0] for r in strict(recs)))
    print("  units %d; self-seeded %d; records %d in %d functions; body-chain (pool/ctx138/cb/ret/arg) records %d in %d "
          "functions" % (len(cen.units), len(cen.selfseeded), len(recs), len(fns_all), len(strict(recs)), len(fns_strict)))
    print("  body-chain functions: " + " ".join("%08X" % f for f in fns_strict))
    # known-answer control on the census: one site per source class and per corrected field
    known = {0x003DA98E: "pool (allocator, +0x08)", 0x00315303: "cb (resolver, +0xE8)", 0x0031533F: "cb (+0xE8)",
             0x002E53B4: "arg<ctx138 (consumer, +0xE8)", 0x002E5227: "ctx138 (002E5180, +0xEC)",
             0x003DACAF: "pool (walk, +0x120)", 0x003DB078: "arg<ctx138 (registration, +0x120)",
             0x0046AF4A: "arg<ctx138 at offset 0x120 (cell routine, +0x124)", 0x002E53F1: "arg<ctx138 (+0x104)",
             0x0026861A: "ctx138 (weight copy, +0x08)", 0x00315263: "cb (+0xEE)"}
    have = set(r[1] for r in strict(recs))
    for va, why in sorted(known.items()):
        ok(va in have, "census control: reaches %08X" % va, why)
    print("  pointers to body storage written to non-stack memory (the census does not follow these):")
    for e in sorted(set(cen.escapes)):
        print("      %08X in %08X  %s  %s" % (e[1], e[0], e[2], list(e[3])))
    ok(all(e[0] in (0x002E3500, 0x003DB0D0) for e in cen.escapes), "census control: escapes are the creator's store and "
       "the placement-list links of body+0x30 only")
    ok(all(o == 0x30 for e in cen.escapes if e[0] == 0x003DB0D0 for o, c in e[3]), "census control: 003DB0D0 links "
       "body+0x30, the 0xB0-byte placement record (+0x30..+0xDF), which ends before every corrected field")
    a = at(img, 0x003DA94D)
    ok(a.text == "mov r8d, 0xb0" and at(img, 0x003DA947).text == "lea rcx, [rdi + 0x30]",
       "the allocator clears the placement record +0x30..+0xDF (0xB0 bytes)")

    ranges = [("+0x08", 0x08, 0x0C), ("+0xE8..+0xEF", 0xE8, 0xF0), ("+0x100..+0x10B", 0x100, 0x10C),
              ("+0x120..+0x12F", 0x120, 0x130)]
    for name, lo, hi in ranges:
        print("  -- %s, body-chain accesses:" % name)
        show(covering(strict(recs), lo, hi))
    print("  -- the same ranges through a +0x138 pointer that is NOT from a secondary context (p138):")
    wk = []
    for name, lo, hi in ranges:
        wk += covering(weak(recs), lo, hi)
    show(dedup(wk))
    # trace each weak hit back to its p138 source function
    par = collections.defaultdict(set)
    for f, site, tgt, argt in cen.calls:
        if any(any("p138" in c for o, c in vals) for vals in argt.values()):
            par[tgt].add(f)
    wsrc = set(w[0] for w in cen.weak_sources)

    def roots(fn, depth=0):
        if fn in wsrc:
            return set([fn])
        if depth > 8:
            return set()
        out = set()
        for p in par.get(fn, ()):
            out |= roots(p, depth + 1)
        return out
    allroots = set()
    for r in wk:
        allroots |= roots(r[0])
    print("  -- p138 roots behind those hits, with the base register's provenance:")
    for rt in sorted(allroots):
        L = cen.insns(rt)
        prov = "?"
        for k, ins in enumerate(L):
            mm = re.match(r"^\w+, qword ptr \[(r\w+) \+ 0x138\]$", ins.op_str)
            if ins.mnemonic == "mov" and mm:
                b = fam(mm.group(1))
                prov = "entry argument"
                for j in range(k - 1, -1, -1):
                    if b in L[j].reg_writes:
                        prov = "%08X %s" % (L[j].address, L[j].text)
                        break
                break
        print("      %08X  base from %s  => %s" % (rt, prov, WEAK_ROOTS.get(rt, "UNDISPOSITIONED")))
        ok(rt in WEAK_ROOTS, "p138 root %08X dispositioned" % rt)

    print("\n== B. the five points (NEW must hold; OLD and MUTANT must not)")

    print("P1  +0x120: a u32 cell set, not a u128")
    n, legs = p1_new(img, recs)
    ok(n, "P1 NEW  dword read at 003DB078 walked one 16-byte mask per bit (02B57CE0, add 0x10, shr edx); dword read at "
       "003DACAF; every body-chain read of +0x120 is 4 bytes; +0x124 written as a dword, never read; +0x128/+0x12C "
       "f32", str(legs))
    ok(not p1_old(img, recs), "P1 OLD  (u128 cell set) refuted: no read of +0x120..+0x12F wider than a dword, and the "
       "bit walk shifts a 32-bit register")
    mut = patch_disp32(img, 0x003DB078, 2, 0x124)
    ok(not p1_new(mut, None)[0], "P1 MUTANT  003DB078 re-pointed at +0x124: NEW fails")

    print("P2  +0xE8: the squared length of the PARTNER's increment, overwritten per contact")
    n, legs = p2_new(img, recs)
    for w in (0.3, 0.8):
        A, B, incA, incB = run_tail(img, w)
        print("      w=%.1f  A inc (%.6f, %.6f)  B inc (%.6f, %.6f)  A.+0xE8 %.6f  B.+0xE8 %.6f  (old +0xE8 values 123 / "
              "456 discarded)" % (w, incA[0], incA[1], incB[0], incB[1], A[0xE8], B[0xE8]))
    ok(n, "P2 NEW  rdi = B, rbx = A (00314F72/00314F75); 00315303 stores |A's increment|^2 into B, 0031533F "
       "|B's increment|^2 into A, both by movss (no read of +0xE8 in the resolver); the one body-chain reader is "
       "002E53B4", str(legs))
    ok(not p2_old(img, recs), "P2 OLD  (a body's own push length, or accumulated) refuted at w = 0.3")
    mut = patch_modrm_rm(img, 0x00315303, 3, 3)      # movss [rdi+0xe8] -> movss [rbx+0xe8]
    ok(at(mut, 0x00315303).text == "movss dword ptr [rbx + 0xe8], xmm1" and not p2_new(mut, None)[0],
       "P2 MUTANT  00315303 re-based on rbx (A): NEW fails")

    print("P3  +0x08: f32")
    n, legs = p3_new(img, recs)
    ok(n, "P3 NEW  movss reads at 00315017/0031502A; every body-chain access to +0x08 is a 4-byte SSE op or the "
       "allocator's store of the bits of 1.0", str(legs))
    ok(not p3_old(img, recs), "P3 OLD  (untyped / integer, the census's uint32) refuted: no integer use of +0x08")
    mut = img.patched(0x00315017, b"\xF2")           # movss -> movsd (8 bytes)
    ok(not p3_new(mut, None)[0], "P3 MUTANT  00315017 made movsd: NEW fails")

    print("P4  +0x104: push y, the middle component; read alone outside the pass")
    n, legs = p4_new(img, recs)
    ok(n, "P4 NEW  002E5380 reads +0x104 alone (002E53F1) into the delta's middle float [r9+4], between x [r9] and z "
       "[r9+8]; every write is the qword zero at +0x100; inside the six pass bodies it is never touched alone", str(legs))
    o_alone, o_third = p4_old(img, recs)
    ok(not o_alone, "P4 OLD-a  (OPUS's 'never accessed alone', taken image-wide) refuted by 002E53F1")
    ok(not o_third, "P4 OLD-b  ('third component' as vector index 2) refuted: +0x104 goes to [r9+4], not [r9+8]")
    mut = patch_disp32(img, 0x002E53F1, 4, 0x10C)
    ok(not p4_new(mut, None)[0], "P4 MUTANT  002E53F1 re-pointed at +0x10C: NEW fails")

    print("P5  +0xEE: set on the body that took the whole push")
    n, legs = p5_new(img, recs)
    for w in (0.0, 1.0):
        _, _, iA, iB = run_tail(img, w)
        print("      w=%.1f  A inc (%.6f, %.6f)  B inc (%.6f, %.6f)" % (w, iA[0], iA[1], iB[0], iB[1]))
    ok(n, "P5 NEW  w = 0 marks B at 00315263 and only B's increment is non-zero; w = 1 marks A at 00315287 and only "
       "A's is; the shared arm clears both (003152A4/003152AB); the one body-chain reader is 002E53C6", str(legs))
    ok(not p5_old(img, recs), "P5 OLD  ('immovable' = the marked body does not move) refuted at w = 0")
    mut = patch_modrm_rm(img, 0x00315263, 3, 1)      # mov byte [rdi+0xee],1 -> [rbx+0xee]
    ok(at(mut, 0x00315263).text == "mov byte ptr [rbx + 0xee], 1" and not p5_new(mut, None)[0],
       "P5 MUTANT  00315263 re-based on rbx (A): NEW fails")
    # the reader's own logic, which the corrected text states
    ok([at(img, va).text for va in (0x002E53AB, 0x002E53B4, 0x002E53BF, 0x002E53C6, 0x002E53CF, 0x002E53D8)] ==
       ["cmp byte ptr [rdx + 0xec], 0", "movss xmm1, dword ptr [rdx + 0xe8]", "ucomiss xmm1, xmm0",
        "cmp byte ptr [rdx + 0xee], 0", "mov byte ptr [rdx + 0xef], 1", "mov byte ptr [rdx + 0xef], 0"],
       "002E5380: +0xEF = 1 when +0xEC is set, +0xE8 == 0 and +0xEE != 0, else 0")

    print("\n== C. citation pre-check: inserted addresses lie in functions the page already cites")
    import apply as AP
    for rel in sorted(set(e[0] for e in AP.EDITS)):
        head = head_text(rel)
        if head is None:
            ok(False, "HEAD text of %s" % rel)
            continue
        have_u = cited_units(cen, head)
        for _r, name, old, new in [e for e in AP.EDITS if e[0] == rel]:
            added = cited_units(cen, new)
            for u, vas in sorted(added.items()):
                ok(u in have_u, "%s / %s: %s in unit %08X" % (rel.split("/")[-1], name,
                   ",".join("%08X" % v for v in sorted(vas)), u))
            struck = re.findall(r"~~(.+?)~~", new)
            for s in struck:
                ok(s in old and s in head, "%s / %s: struck '%s' is the page's own text at HEAD" % (
                    rel.split("/")[-1], name, s))

    print("\nFAILS %d" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    return len(FAILS)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
