"""gr1315_q2.py - SWE2-AUDIT-SPEC, GR-13/14/15 review: replacement for gr1315_indep.py's blind Q sweep (2026-09-30).

Defect of the old Q: a 24-instruction linear window after each holder load, intraprocedural. It found 1 of the 14
known +0x10 price reads (the callbacks read +0x10 far after the load; 0056E700 / 0056D870 / 0056DA80 get the row as an
argument).

This sweep:
  * seeds every qword load `mov|add r64, [base + 0xC8 | 0xD0 | 0xE0]` (base not rip/rsp) in every .pdata function of
    the image (whole-function extent: every .pdata chunk whose unwind chain roots at the function);
  * runs a forward MAY-taint dataflow over the function's CFG (union at joins; direct jcc/jmp edges; an indirect jmp
    feeds every instruction that follows an unconditional jmp/ret, i.e. every possible jump-table arm);
    taint moves through mov/cmov/xchg/lea/add/sub/or register forms and 8-byte rsp/rbp stack slots;
  * is interprocedural: a tainted rcx/rdx/r8/r9 at a direct call or tail jmp taints that register at the callee's
    entry (fixpoint, callee depth <= 4);
  * records every non-lea memory operand at displacement +0x10 whose base or index is tainted, with its width.
Positive control: the 14 package sites (A4a) must all be found. Everything else found is listed by root for
classification (the question is whether any of them reads a SHOP list row).
"""
import os, struct, sys, bisect, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_RSP, X86_REG_RBP, X86_REG_INVALID

IB, raw = T.IB, T.raw
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def root(va):
    rva = va - IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    e = PD[j]
    for _ in range(16):
        uo = T.off(IB + e[2]); fl = raw[uo] >> 3; cnt = raw[uo + 2]
        if not (fl & 4):
            return IB + e[0]
        e = struct.unpack_from("<III", raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return IB + e[0]


CHUNKS = collections.defaultdict(list)
for b, e, u in PD:
    r = root(IB + b)
    if r:
        CHUNKS[r].append((IB + b, IB + e))

FAMN = {}
for a, b, c, d in (("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"),
                   ("rdx", "edx", "dx", "dl"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
                   ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")):
    for x in (a, b, c, d):
        FAMN[x] = a
for q in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAMN["r%d%s" % (q, suf)] = "r%d" % q


def fam(i, reg):
    if reg in (0, X86_REG_INVALID):
        return None
    return FAMN.get(i.reg_name(reg), i.reg_name(reg))


DECODED = {}


def decode(f):
    if f in DECODED:
        return DECODED[f]
    ins = {}
    for a, b in CHUNKS.get(f, [(f, f + 0x800)]):
        for i in T.md.disasm(T.rd(a, b - a), a):
            ins[i.address] = i
    order = sorted(ins)
    DECODED[f] = (ins, order)
    return DECODED[f]


ARGS = ("rcx", "rdx", "r8", "r9")
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
HOLD = (0xC8, 0xD0, 0xE0)
hits = collections.defaultdict(set)   # site -> {(width, mnemonic op, func)}
seeds_by_func = collections.defaultdict(set)
callee_in = collections.defaultdict(set)
prov = collections.defaultdict(set)   # callee -> {(caller site, caller root)}
escapes = collections.defaultdict(set)
nseed = 0


def is_holder_load(i):
    if i.mnemonic not in ("mov", "add") or len(i.operands) != 2:
        return False
    d, s = i.operands
    return (d.type == CS_OP_REG and s.type == CS_OP_MEM and s.size == 8 and s.mem.disp in HOLD
            and s.mem.base not in (X86_REG_RIP, X86_REG_RSP, 0) and fam(i, d.reg) not in (None,))


def stack_key(i, m):
    if m.base in (X86_REG_RSP, X86_REG_RBP) and m.index in (0, X86_REG_INVALID):
        return ("stk", i.reg_name(m.base), m.disp)
    return None


def analyse(f, entry_regs, depth):
    ins, order = decode(f)
    if not order:
        return
    pos = {a: k for k, a in enumerate(order)}
    after_uncond = set()
    for k, a in enumerate(order[:-1]):
        i = ins[a]
        if i.mnemonic in ("ret", "jmp", "int3"):
            after_uncond.add(order[k + 1])
    state = collections.defaultdict(frozenset)
    work = []
    start = f if f in ins else order[0]
    state[start] = frozenset(entry_regs)
    # every seed-load site is a source regardless of path: start the walk at the function entry and at every seed
    work = [start] + [a for a in order if is_holder_load(ins[a])]
    for a in work[1:]:
        seeds_by_func[f].add(a)
    inq = set(work)
    ind_state = frozenset()
    steps = 0
    while work:
        a = work.pop()
        inq.discard(a)
        steps += 1
        if steps > 400000:
            print("  !! step budget hit in %08X" % f)
            break
        i = ins[a]
        S = set(state[a])
        mn = i.mnemonic
        ops = i.operands
        # hits
        if mn != "lea":
            for op in ops:
                if op.type == CS_OP_MEM and op.mem.disp == 0x10:
                    b = fam(i, op.mem.base); x = fam(i, op.mem.index)
                    if (b in S) or (x in S):
                        hits[a].add((op.size, "%s %s" % (mn, i.op_str), f))
        # transfer
        wr = set()
        try:
            _, w = i.regs_access()
            wr = {fam(i, r) for r in w} - {None, "rsp", "rip"}
            wr = {r for r in wr if r in FAMN.values()}
        except Exception:
            pass
        N = set(S)
        tainted_dst = None
        if is_holder_load(i):
            tainted_dst = fam(i, ops[0].reg)
        elif len(ops) == 2 and ops[0].type == CS_OP_REG:
            d = fam(i, ops[0].reg); s_ = ops[1]
            dsz = ops[0].size
            if mn in ("mov",) and s_.type == CS_OP_REG and dsz == 8:
                tainted_dst = d if fam(i, s_.reg) in S else None
            elif mn.startswith("cmov") and s_.type == CS_OP_REG and dsz == 8:
                tainted_dst = d if (fam(i, s_.reg) in S or d in S) else None
            elif mn == "lea" and dsz == 8:
                tainted_dst = d if (fam(i, s_.mem.base) in S or fam(i, s_.mem.index) in S) else None
            elif mn in ("add", "sub", "or") and dsz == 8:
                tainted_dst = d if (d in S or (s_.type == CS_OP_REG and fam(i, s_.reg) in S)) else None
            elif mn == "mov" and s_.type == CS_OP_MEM and dsz == 8:
                k = stack_key(i, s_.mem)
                tainted_dst = d if (k and k in S) else None
            elif mn == "xchg" and s_.type == CS_OP_REG:
                e_ = fam(i, s_.reg)
                ta, tb = d in S, e_ in S
                N.discard(d); N.discard(e_)
                if ta: N.add(e_)
                if tb: N.add(d)
                wr = set()
        # stores
        if mn == "mov" and len(ops) == 2 and ops[0].type == CS_OP_MEM and ops[1].type == CS_OP_REG and ops[1].size == 8:
            k = stack_key(i, ops[0].mem)
            src_t = fam(i, ops[1].reg) in S
            if k:
                N.discard(k)
                if src_t:
                    N.add(k)
            elif src_t:
                escapes[f].add((a, ops[0].mem.disp, "%s %s" % (mn, i.op_str)))
        if mn != "xchg":
            for r in wr:
                N.discard(r)
            if tainted_dst:
                N.add(tainted_dst)
        # calls / successors
        succ = []
        if mn == "call":
            targs = [r for r in ARGS if r in S]
            if targs and ops and ops[0].type == CS_OP_IMM:
                callee_in[ops[0].imm] |= {(r, depth + 1) for r in targs}
                prov[ops[0].imm].add((a, f))
            elif targs:
                escapes[f].add((a, None, "indirect call %s with tainted %s" % (i.op_str, targs)))
            for r in VOL:
                N.discard(r)
            succ = [order[pos[a] + 1]] if pos[a] + 1 < len(order) else []
        elif mn == "ret" or mn == "int3":
            succ = []
        elif mn == "jmp":
            if ops and ops[0].type == CS_OP_IMM:
                t = ops[0].imm
                if t in ins:
                    succ = [t]
                else:
                    targs = [r for r in ARGS if r in S]
                    if targs:
                        callee_in[t] |= {(r, depth + 1) for r in targs}
                        prov[t].add((a, f))
            else:
                ind_state = ind_state | frozenset(N)
                succ = list(after_uncond)
        elif i.group(7) or mn.startswith("j") or mn.startswith("loop"):
            succ = [order[pos[a] + 1]] if pos[a] + 1 < len(order) else []
            if ops and ops[0].type == CS_OP_IMM and ops[0].imm in ins:
                succ.append(ops[0].imm)
        else:
            succ = [order[pos[a] + 1]] if pos[a] + 1 < len(order) else []
        NF = frozenset(N)
        for t in succ:
            new = state[t] | NF
            if new != state[t] or t not in state:
                state[t] = new
                if t not in inq:
                    inq.add(t); work.append(t)


# pass 1: every .pdata function that contains a holder load
funcs = set()
for r, ch in CHUNKS.items():
    ins, order = decode(r)
    for a in order:
        if is_holder_load(ins[a]):
            funcs.add(r)
            nseed += 1
print("== Q2. holder loads (mov|add r64, qword [base + 0xC8|0xD0|0xE0]) image-wide: %d in %d functions" % (nseed, len(funcs)))
for f in sorted(funcs):
    analyse(f, (), 0)
# interprocedural fixpoint
done = {}
for rnd in range(6):
    todo = []
    for t, s in list(callee_in.items()):
        regs = frozenset(r for (r, dep) in s if dep <= 4)
        if not regs:
            continue
        if done.get(t, frozenset()) >= regs:
            continue
        done[t] = done.get(t, frozenset()) | regs
        todo.append((t, done[t], min(dep for (r, dep) in s)))
    if not todo:
        break
    print("  round %d: %d callees with tainted argument registers" % (rnd, len(todo)))
    for t, regs, dep in todo:
        f = root(t) or t
        if t not in CHUNKS and root(t) is None:
            CHUNKS[t] = [(t, t + 0x400)]
        analyse(t if t in CHUNKS else f, regs, dep)

P14 = [0x0056CC7E, 0x0056CCA2, 0x0056CE07, 0x0056CE31, 0x0056CFF3, 0x0056D023, 0x0056D0C8, 0x0056D267, 0x0056D291,
       0x0056D461, 0x0056D8F1, 0x0056DBCA, 0x0056E71A, 0x0056E797]
print("== positive control: the package's 14 +0x10 price reads found: %d of 14 (missing %s)"
      % (sum(1 for a in P14 if a in hits), ["%08X" % a for a in P14 if a not in hits]))
UI = lambda a: 0x00560000 <= a < 0x00580000 or 0x003FC000 <= a < 0x00400000
dw = {a: v for a, v in hits.items() if any(w == 4 for (w, _, _) in v)}
print("  total +0x10 accesses through a holder-derived register: %d (dword: %d)" % (len(hits), len(dw)))
print("== every hit inside the UI windows 00560000-0057FFFF / 003FC000-003FFFFF (any width), by root")
byr = collections.defaultdict(list)
for a in sorted(hits):
    if UI(a):
        byr[root(a)].append(a)
for r in sorted(byr, key=lambda z: z or 0):
    print("  root %s:" % ("%08X" % r if r else "--------"))
    for a in byr[r]:
        w, txt, f = sorted(hits[a])[0]
        print("    %08X %dB %-45s %s" % (a, w, txt, "P14" if a in P14 else "NEW"))
out_ui = sorted(a for a in dw if not UI(a))
print("== dword +0x10 hits OUTSIDE the UI windows: %d, in %d roots" % (len(out_ui), len({root(a) for a in out_ui})))
rc = collections.Counter(root(a) for a in out_ui)
print("  roots: %s" % ", ".join("%s(%d)" % ("%08X" % r if r else "-", n) for r, n in sorted(rc.items(), key=lambda z: z[0] or 0)))
print("== provenance of every hit root outside the UI windows: own holder loads, or tainted arguments from which call sites")
for r in sorted({root(a) for a in out_ui}, key=lambda z: z or 0):
    ins, order = decode(r)
    own = [a for a in order if is_holder_load(ins[a])]
    print("  %08X own holder loads %s ; tainted-arg entries from %s" % (r, ["%08X" % a for a in own],
          sorted("%08X(in %08X)" % (s_, f_) for (s_, f_) in prov.get(r, ()))))
    for a in out_ui:
        if root(a) == r:
            print("      hit %08X %s" % (a, sorted(hits[a])[0][1]))
SHOPF = [0x0056E140, 0x0056E410, 0x005655F0, 0x0056D370, 0x0056CBC0, 0x0056CD50, 0x0056CF10, 0x0056D1B0, 0x0056E700,
         0x0056D870, 0x0056DA80, 0x0056C490, 0x0056CA60, 0x0056D9D0, 0x00565A00]
print("== escapes (a tainted register stored to non-stack memory, or an indirect call with a tainted argument) in the shop family")
for f in SHOPF:
    print("  %08X %s" % (f, sorted(("%08X" % a, ("+0x%X" % d) if d is not None else "-", t) for (a, d, t) in escapes.get(f, ()))))
print("== interprocedural edges out of the shop family (callee <- call site)")
for t, ss in sorted(prov.items()):
    for (s_, f_) in sorted(ss):
        if f_ in SHOPF:
            print("  %08X <- %08X (in %08X) regs %s" % (t, s_, f_, sorted(r for (r, d) in callee_in[t])))
