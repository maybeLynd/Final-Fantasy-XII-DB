"""gr45_census.py - SWE2-AUDIT-SPEC independent reader census for action row +0x0B / +0x0A / +0x28 (GR-4/GR-5 review,
2026-09-30). Nothing from the reviewed package or the kit is imported: img45.py only (certified image, sha asserted).

Different method from the package's rowflow.py (a forward taint): a BACKWARD reaching-definition typing of the base.
  functions  .pdata extents that hold a rip load of the action slot 02EBF138 (the 720 sites of pkg_slot_sites.txt,
             which gr45_refs.py re-derived: 719 loads + the binder's lea), then every .pdata function they reach by a
             direct E8 call, E9 tail jump or 0F 8x conditional tail jump, to 3 levels (S0..S3).
  accesses   every memory operand in those extents with a non-rip, non-rsp base whose byte span covers the field,
             exactly (disp .. disp+w-1 contains F) or modulo the 60-byte stride for disp 60..0x3FF.
  typing     the base register's reaching definitions on the function's CFG (direct branches; blocks with no
             predecessor, e.g. jump-table arms, are reported as NOPRED), followed through mov / movsxd / cmov /
             lea (base and scale-1 index) / add / sub-imm / xchg, stack slots (every store to the same [rsp|rbp + d] in
             the function), direct-call returns (the callee's ret values, recursively) and arguments (every raw E8/E9
             caller's register at its call site, recursively, any caller in the image; a non-argument register
             only across jumps into the function: raw E9 / 0F 8x and decoded rel8 jumps from .pdata neighbours
             within 0x4000, which is how a compiler-split chunk is entered). MSVC jump tables are decoded into CFG
             edges. A leaf `call 0020E600` whose rcx is the action header's +0x0C dword (`mov r32, [H + 0xC]`, H
             a qword rip load of 02EBF138) marks the row base (ROWBASE; any other 0020E600 return is OTHERBASE);
             a base whose leaves include ROWBASE is ROW-REACHING.
             Leaves that cannot be followed (NOPRED, indirect-call returns, non-stack loads) are counted, not dropped.
  escapes    every store of a register (dword or wider) to non-stack memory in those extents whose value is
             row-reaching (checks the package's "0 escapes").
Controls: F = 0x0A must return the five MP-cost byte reads; F = 0x28 must return 0030A209 inside 0030A190, which gets
the row only as an argument (the defect a body-only census has).
"""
import sys, os, bisect, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img45 as I
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM

sys.setrecursionlimit(20000)
RESOLVE = 0x0020E600
SLOT = 0x02EBF138
P = sorted(I.pdata())
PB = [b for b, e in P]
PSET = {b: e for b, e in P}
ARGS = ("rcx", "rdx", "r8", "r9")
FAM = {}
for fam in (("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"), ("rcx", "ecx", "cx", "cl", "ch"),
            ("rdx", "edx", "dx", "dl", "dh"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
            ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")):
    for r in fam:
        FAM[r] = fam[0]
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAM["r%d%s" % (n, suf)] = "r%d" % n
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")


def fam(x, r):
    if not r:
        return None
    n = x.reg_name(r)
    return FAM.get(n, n)


def owner(a):
    k = bisect.bisect_right(PB, a) - 1
    if k >= 0 and P[k][0] <= a < P[k][1]:
        return P[k][0]
    return None


_F = {}
JT_COUNT = [0, 0]
UNFOLLOWED = ("NOPRED", "ENTRY", "ARG-NOCALLER", "ARG-TRUNC", "ARG-UNOWNED", "ARG-MISDECODE", "ARG-DEEP", "DEEP",
              "STACK?", "ICALL", "NONE", "LOAD", "POP")


def func(b):
    """(ins list, index by addr, preds by block-leader index, leader-of index)"""
    if b in _F:
        return _F[b]
    e = PSET[b]
    ins = I.dis(b, e)
    idx = {x.address: k for k, x in enumerate(ins)}
    if not ins:
        _F[b] = (ins, idx, {}, {})
        return _F[b]
    lead = {0}
    for k, x in enumerate(ins):
        if x.mnemonic.startswith("j") or x.mnemonic in ("ret", "int3"):
            if k + 1 < len(ins):
                lead.add(k + 1)
            if x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm in idx:
                lead.add(idx[x.operands[0].imm])
    # MSVC jump tables: `jmp reg` after `mov r32, dword ptr [rB + rI*4 + D]` (rB = image base): D + 0x120000 holds
    # dword RVAs of the arms; the bound comes from the nearest `cmp r, imm` before it (else read while in extent)
    jt = {}
    for k, x in enumerate(ins):
        if x.mnemonic == "jmp" and x.operands and x.operands[0].type == X86_OP_REG:
            tab, bound = None, None
            for y in ins[max(0, k - 14):k]:
                if y.mnemonic == "cmp" and len(y.operands) == 2 and y.operands[1].type == X86_OP_IMM:
                    bound = y.operands[1].imm
                for op in y.operands:
                    if op.type == X86_OP_MEM and op.mem.scale == 4 and op.mem.index and op.mem.base \
                            and y.mnemonic in ("mov", "movsxd"):
                        tab = 0x120000 + op.mem.disp
            if tab is None:
                continue
            arms = []
            for n in range((bound + 1) if bound is not None and 0 <= bound < 1024 else 1024):
                rv = I.rd(tab + 4 * n, 4)
                if not rv:
                    break
                v = 0x120000 + int.from_bytes(rv, "little")
                if v not in idx:
                    break
                arms.append(idx[v])
            jt[k] = arms
            lead.update(arms)
    JT_COUNT[0] += len(jt)
    JT_COUNT[1] += sum(len(a) for a in jt.values())
    leaders = sorted(lead)
    blk_of = {}
    cur = 0
    for k in range(len(ins)):
        if k in lead:
            cur = k
        blk_of[k] = cur
    preds = collections.defaultdict(set)
    for n, s in enumerate(leaders):
        endk = (leaders[n + 1] - 1) if n + 1 < len(leaders) else len(ins) - 1
        last = ins[endk]
        m = last.mnemonic
        if m.startswith("j"):
            if last.operands and last.operands[0].type == X86_OP_IMM and last.operands[0].imm in idx:
                preds[idx[last.operands[0].imm]].add(endk)
            if m != "jmp" and endk + 1 < len(ins):
                preds[endk + 1].add(endk)
            for a in jt.get(endk, ()):
                preds[a].add(endk)
        elif m not in ("ret", "int3") and endk + 1 < len(ins):
            preds[endk + 1].add(endk)
    _F[b] = (ins, idx, preds, blk_of)
    return _F[b]


def writes(x):
    try:
        return {FAM.get(x.reg_name(r), x.reg_name(r)) for r in x.regs_access()[1]}
    except Exception:
        return set()


def reaching(b, k, reg):
    """definitions of reg reaching instruction k of function b: list of def indexes, plus 'ENTRY' / 'NOPRED' markers"""
    ins, idx, preds, blk_of = func(b)
    out, seen = set(), set()
    if blk_of[k] == k:          # k starts a block: its reaching values come from the predecessors, not from k - 1
        if k == 0:
            out.add("ENTRY")
        ps = preds.get(k, set())
        if not ps and k != 0:
            out.add("NOPRED")
        stack = list(ps)
    else:
        stack = [k - 1]
    while stack:
        j = stack.pop()
        while True:
            if j < 0:
                out.add("ENTRY")
                break
            if j in seen:
                break
            seen.add(j)
            x = ins[j]
            if x.mnemonic == "call" or reg in writes(x):
                if x.mnemonic == "call" and reg not in VOL:
                    pass
                else:
                    out.add(j)
                    break
            if blk_of[j] == j:     # at a block start: go to predecessors
                ps = preds.get(j, set())
                if j == 0:
                    out.add("ENTRY")
                elif not ps:
                    out.add("NOPRED")
                stack.extend(ps)
                break
            j -= 1
    return out


_memo = {}
BUDGET = {"n": 0}


def src(b, k, reg, depth=0):
    """set of leaf labels for the value of reg just before instruction k of function b"""
    key = (b, k, reg)
    if key in _memo:
        return _memo[key]
    if depth > 14:
        return {"DEEP"}
    _memo[key] = {"CYCLE"}
    ins = func(b)[0]
    res = set()
    for d in reaching(b, k, reg):
        if d == "ENTRY":
            res |= arg_src(b, reg, depth + 1)
            continue
        if d == "NOPRED":
            res.add("NOPRED")
            continue
        res |= def_src(b, d, reg, depth + 1)
    res.discard("CYCLE")
    _memo[key] = res or {"NONE"}
    return _memo[key]


def def_src(b, j, reg, depth):
    ins = func(b)[0]
    x = ins[j]
    m, ops = x.mnemonic, x.operands
    if m == "call":
        if reg != "rax":
            return {"CLOB"}
        if ops and ops[0].type == X86_OP_IMM:
            if ops[0].imm == RESOLVE:
                return {"ROWBASE"} if "ACTREF" in src(b, j, "rcx", depth) else {"OTHERBASE"}
            return ret_src(ops[0].imm, depth)
        return {"ICALL"}
    if m in ("xor", "sub") and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG \
            and fam(x, ops[0].reg) == fam(x, ops[1].reg):
        return {"CONST"}
    if len(ops) >= 1 and ops[0].type == X86_OP_REG and fam(x, ops[0].reg) == reg:
        s = ops[1] if len(ops) > 1 else None
        if m in ("mov", "movsxd", "movsx", "movzx") or m.startswith("cmov"):
            r = set()
            if m.startswith("cmov"):
                r |= src(b, j, reg, depth)
            if s.type == X86_OP_REG:
                return r | src(b, j, fam(x, s.reg), depth)
            if s.type == X86_OP_IMM:
                return r | {"CONST"}
            if s.size < 4:
                return r | {"INT"}
            sb = fam(x, s.mem.base)
            if sb in ("rsp", "rbp") and not s.mem.index:
                return r | slot_src(b, sb, s.mem.disp, depth)
            if sb == "rip":
                return r | ({"SLOT"} if x.address + x.size + s.mem.disp == SLOT and s.size == 8 else {"LOAD:rip"})
            if s.mem.disp == 0xC and not s.mem.index and s.size == 4 and "SLOT" in src(b, j, sb, depth):
                return r | {"ACTREF"}
            return r | {"LOAD"}
        if m == "lea":
            r = set()
            sb, si = fam(x, s.mem.base), fam(x, s.mem.index)
            if sb and sb != "rip":
                r |= src(b, j, sb, depth)
            if si and s.mem.scale == 1:
                r |= src(b, j, si, depth)
            return r or {"CONST"}
        if m in ("add", "adc"):
            r = src(b, j, reg, depth)
            if s.type == X86_OP_REG:
                r |= src(b, j, fam(x, s.reg), depth)
            elif s.type == X86_OP_MEM:
                r |= {"LOAD"}
            return r
        if m in ("sub", "and", "or", "inc", "dec", "neg", "not", "btr", "bts") and (s is None or s.type == X86_OP_IMM):
            return src(b, j, reg, depth)
        if m == "sub" and s is not None and s.type == X86_OP_REG:
            return {"INT"}       # row - base -> an id
        if m == "xchg" and s is not None and s.type == X86_OP_REG:
            return src(b, j, fam(x, s.reg), depth)
        if m == "pop":
            return {"POP"}
        return {"INT:" + m} if m in ("imul", "shl", "shr", "sar", "mul", "div", "idiv", "movd", "cvttss2si",
                                      "setne", "sete", "bsf", "bsr", "popcnt") else {"OTHER:" + m}
    if len(ops) == 2 and ops[1].type == X86_OP_REG and fam(x, ops[1].reg) == reg and m == "xchg":
        return src(b, j, fam(x, ops[0].reg), depth) if ops[0].type == X86_OP_REG else {"LOAD"}
    return {"OTHER:" + m}


_slot = {}


def slot_src(b, base, disp, depth):
    ins = func(b)[0]
    r = set()
    n = 0
    for j, x in enumerate(ins):
        ops = x.operands
        if x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG \
                and fam(x, ops[0].mem.base) == base and ops[0].mem.disp == disp and not ops[0].mem.index \
                and ops[0].size >= 4:
            r |= src(b, j, fam(x, ops[1].reg), depth)
            n += 1
    return r if n else {"STACK?"}


_ret = {}


def ret_src(t, depth):
    if t in _ret:
        return _ret[t]
    if t not in PSET or depth > 10:
        return {"CALL:%08X" % t}
    _ret[t] = {"CYCLE"}
    ins = func(t)[0]
    r = set()
    for j, x in enumerate(ins):
        if x.mnemonic == "ret":
            r |= src(t, j, "rax", depth)
        elif x.mnemonic == "jmp" and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm not in func(t)[1]:
            if x.operands[0].imm == RESOLVE:
                r |= {"ROWBASE"} if "ACTREF" in src(t, j, "rcx", depth) else {"OTHERBASE"}
            else:
                r |= ret_src(x.operands[0].imm, depth + 1)
    r.discard("CYCLE")
    rowish = "ROWBASE" in r
    _ret[t] = ({"ROWBASE"} if rowish else set()) | ({"CALL:%08X" % t} if not rowish else set())
    return _ret[t]


_callers = None


def callers_of(t):
    """raw rel32 transfers to t: [(site, kind)] with kind E8 / E9 / JCC"""
    global _callers
    if _callers is None:
        _callers = collections.defaultdict(list)
        tx = I._text_np()
        import numpy as np
        v, bb, d, L = tx["v"], tx["b"], tx["d"], tx["L"]
        m = np.zeros(L, dtype=bool)
        m[:L - 5] = (bb[:L - 5] == 0xE8) | (bb[:L - 5] == 0xE9)
        for k in np.nonzero(m)[0]:
            tg = int(v + k + 5 + d[k + 1])
            if tg in PSET:
                _callers[tg].append((int(v + k), "E8" if bb[k] == 0xE8 else "E9"))
        m = np.zeros(L, dtype=bool)
        m[:L - 6] = (bb[:L - 6] == 0x0F) & (bb[1:L - 5] >= 0x80) & (bb[1:L - 5] <= 0x8F)
        for k in np.nonzero(m)[0]:
            tg = int(v + k + 6 + d[k + 2])
            if tg in PSET:
                _callers[tg].append((int(v + k), "JCC"))
    return _callers.get(t, [])


_near = {}


def near_jumpers(b):
    """decoded direct jmp / jcc (any encoding, incl. rel8) to b from .pdata functions starting within 0x4000 of b -
    a chunk split off by the compiler is entered this way"""
    if b in _near:
        return _near[b]
    out = []
    k0 = bisect.bisect_left(PB, b - 0x4000)
    while k0 < len(P) and P[k0][0] <= b + 0x4000:
        fb = P[k0][0]
        k0 += 1
        if fb == b:
            continue
        for x in func(fb)[0]:
            if x.mnemonic.startswith("j") and x.operands and x.operands[0].type == X86_OP_IMM                     and x.operands[0].imm == b:
                out.append(x.address)
    _near[b] = out
    return out


_arg = {}


def arg_src(b, reg, depth):
    key = (b, reg)
    if key in _arg:
        return _arg[key]
    if depth > 14:
        return {"ARG-DEEP"}
    _arg[key] = {"CYCLE"}
    r = set()
    cs = [c for c in callers_of(b) if reg in ARGS or c[1] != "E8"]   # a non-argument register is followed only
    have = {c[0] for c in cs}
    cs += [(a, "SHORT") for a in near_jumpers(b) if a not in have]
    if not cs:                                                       # across jumps into b (a chunk / tail jump)
        r.add(("ARG-NOCALLER:" if reg in ARGS else "ENTRY:") + reg)
    for site, kind in cs[:60]:
        ob = owner(site)
        if ob is None:
            r.add("ARG-UNOWNED")
            continue
        ins, idx, _, _ = func(ob)
        if site not in idx:
            r.add("ARG-MISDECODE")
            continue
        r |= src(ob, idx[site], reg, depth)
    if len(cs) > 60:
        r.add("ARG-TRUNC")
    r.discard("CYCLE")
    _arg[key] = r
    return r


def reach(roots, levels):
    got = set(roots)
    frontier = set(roots)
    for _ in range(levels):
        nxt = set()
        for b in frontier:
            ins, idx, _, _ = func(b)
            for x in ins:
                if (x.mnemonic in ("call", "jmp") or x.mnemonic.startswith("j")) and x.operands \
                        and x.operands[0].type == X86_OP_IMM:
                    t = x.operands[0].imm
                    if t in PSET and t != b and t not in got and t != RESOLVE:
                        nxt.add(t)
        got |= nxt
        frontier = nxt
    return got


def covers(disp, w, F):
    if disp <= F < disp + w:
        return "exact"
    if 60 <= disp < 0x400 and any((disp + j) % 60 == F for j in range(w)):
        return "mod60"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    sites = [int(l, 16) for l in open(os.path.join(here, "pkg_slot_sites.txt")) if l.strip()]
    S0 = {owner(a) for a in sites}
    assert None not in S0
    allf = reach(S0, 3)
    print("slot sites %d; S0 .pdata functions %d; S0..S3 functions %d" % (len(sites), len(S0), len(allf)))
    for b in sorted(allf):
        func(b)
    print("jump tables decoded %d, arms %d" % tuple(JT_COUNT))
    for F in (0x0B, 0x0A, 0x28):
        acc = []
        for b in sorted(allf):
            ins = func(b)[0]
            for j, x in enumerate(ins):
                if x.mnemonic in ("lea", "nop") or x.mnemonic.startswith("prefetch"):
                    continue
                for op in x.operands:
                    if op.type != X86_OP_MEM:
                        continue
                    bs = fam(x, op.mem.base)
                    if bs in (None, "rip", "rsp"):
                        continue
                    c = covers(op.mem.disp, op.size, F)
                    if c:
                        acc.append((b, j, x, bs, op, c))
        leafc = collections.Counter()
        rows, unf = [], []
        for b, j, x, bs, op, c in acc:
            s = src(b, j, bs)
            si = fam(x, op.mem.index)
            if si and op.mem.scale == 1:
                s = s | src(b, j, si)
            for l in s:
                leafc[l.split(":")[0]] += 1
            if "ROWBASE" in s:
                rows.append((b, x, c, op.size, sorted(s)))
            elif any(l.split(":")[0] in UNFOLLOWED for l in s):
                unf.append((b, x, c, op.size, sorted(s)))
        print("F=+0x%02X: covering accesses %d (exact %d, mod60 %d); ROW-REACHING %d" % (
            F, len(acc), sum(1 for a in acc if a[5] == "exact"), sum(1 for a in acc if a[5] == "mod60"), len(rows)))
        print("   leaf classes over all covering accesses: %s" % dict(sorted(leafc.items())))
        for b, x, c, w, s in rows:
            print("   ROW %08X %08X %-5s w%-2d %-44s leaves %s" % (b, x.address, c, w, "%s %s" % (x.mnemonic, x.op_str), s))
        uk = collections.Counter(l.split(":")[0] for r in unf for l in r[4] if l.split(":")[0] in UNFOLLOWED)
        print("   not row-reaching but with an unfollowed leaf: %d accesses in %d functions; by leaf %s"
              % (len(unf), len({r[0] for r in unf}), dict(sorted(uk.items()))))
        if F == 0x0B:
            for b, x, c, w, s in unf:
                print("   UNF %08X %08X %-5s w%-2d %-44s %s" % (b, x.address, c, w, "%s %s" % (x.mnemonic, x.op_str),
                                                              [l for l in s if l.split(":")[0] in UNFOLLOWED]))
    # escapes
    esc = []
    nst = 0
    for b in sorted(allf):
        ins = func(b)[0]
        for j, x in enumerate(ins):
            ops = x.operands
            if x.mnemonic in ("mov", "movq", "movd", "xchg") and len(ops) == 2 and ops[0].type == X86_OP_MEM \
                    and ops[1].type == X86_OP_REG and ops[0].size >= 4:
                db = fam(x, ops[0].mem.base)
                if db in ("rsp", "rbp") and not ops[0].mem.index:
                    continue
                nst += 1
                r = fam(x, ops[1].reg)
                if r and r.startswith(("r", "e")) and "xmm" not in r:
                    s = src(b, j, r)
                    if "ROWBASE" in s:
                        esc.append((b, x, sorted(s)))
    print("escapes: non-stack register stores %d; with a row-reaching value %d" % (nst, len(esc)))
    for b, x, s in esc:
        print("   ESC %08X %08X %-44s leaves %s" % (b, x.address, "%s %s" % (x.mnemonic, x.op_str), s))
    # stack stores and indirect calls: the two routes by which a row could reach code the census types as STACK? or
    # ARG-NOCALLER
    stk, icall, nic = [], [], 0
    for b in sorted(allf):
        ins = func(b)[0]
        for j, x in enumerate(ins):
            ops = x.operands
            if x.mnemonic in ("mov", "movq") and len(ops) == 2 and ops[0].type == X86_OP_MEM \
                    and ops[1].type == X86_OP_REG and ops[0].size >= 4 \
                    and fam(x, ops[0].mem.base) in ("rsp", "rbp") and not ops[0].mem.index:
                r = fam(x, ops[1].reg)
                if r and "xmm" not in r and "ROWBASE" in src(b, j, r):
                    stk.append((b, x))
            if x.mnemonic == "call" and ops and ops[0].type != X86_OP_IMM:
                nic += 1
                t = [r for r in ARGS if "ROWBASE" in src(b, j, r)]
                if t:
                    icall.append((b, x, t))
    print("stack-slot stores of a row-reaching value: %d" % len(stk))
    for b, x in stk:
        print("   STK %08X %08X %s %s" % (b, x.address, x.mnemonic, x.op_str))
    print("indirect calls %d; with a row-reaching rcx/rdx/r8/r9: %d" % (nic, len(icall)))
    for b, x, t in icall:
        print("   ICALL %08X %08X %s %s args %s" % (b, x.address, x.mnemonic, x.op_str, t))


if __name__ == "__main__":
    main()
