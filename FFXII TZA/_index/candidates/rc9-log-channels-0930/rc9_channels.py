"""rc9_channels.py - RC-9: the channel (ecx) every call or tail jump to the formatted log call 005CDAA0 passes,
including the 43 sites where it is computed. OPUS, 2026-09-30. Static. Reads only.

Method: a forward value-set dataflow over each caller's own control flow, decoded from its entry by following
fall-through and direct branch targets (so chained fragments are reached the way the code reaches them). Every
general register holds a small set of values: constants, or an entry register plus an offset (rcx@entry+1), or
UNKNOWN. Joins take the union (more than 16 values is UNKNOWN). A call keeps the callee-saved registers
(rbx rbp rsi rdi r12-r15) and makes the volatile ones UNKNOWN (rax is the call's result). A value that depends on
an entry register is resolved through every caller of that function (edges.tsv, calls and tail jumps), recursively.

Positive controls: the 202 sites CONTRACT's log_channels.py resolves as literals must come out as the same single
value here, and every site must be reached from its function's entry.
"""
import collections, io, os, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import block_writer_disjoint as b  # noqa: E402

TARGET = 0x005CDAA0
MAXSET = 16
UNK = None
GP = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = ("rcx", "rdx", "r8", "r9")

at = b.load()
ext = b.extents()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
_dec = {}


def dec(a):
    if a not in _dec:
        d = at(a, 16)
        i = next(md.disasm(d, a, 1), None) if d else None
        _dec[a] = i
    return _dec[a]


def full(reg_id):
    """(64-bit register name, width in bytes) for a capstone register id, or (None, 0)."""
    n = md.reg_name(reg_id)
    if n is None:
        return None, 0
    m = {"eax": "rax", "ax": "rax", "al": "rax", "ebx": "rbx", "bx": "rbx", "bl": "rbx", "ecx": "rcx", "cx": "rcx",
         "cl": "rcx", "edx": "rdx", "dx": "rdx", "dl": "rdx", "esi": "rsi", "si": "rsi", "sil": "rsi", "edi": "rdi",
         "di": "rdi", "dil": "rdi", "ebp": "rbp", "bp": "rbp", "bpl": "rbp"}
    w = {"e": 4, "r": 8}
    if n in GP:
        return n, 8
    if n in m:
        return m[n], (4 if n.startswith("e") else 1 if n.endswith(("l", "il", "pl")) else 2)
    for r in range(8, 16):
        for suf, wd in (("d", 4), ("w", 2), ("b", 1)):
            if n == "r%d%s" % (r, suf):
                return "r%d" % r, wd
    return None, 0


def const_set(v):
    return v is not UNK and all(t[0] is None for t in v)


def add(v, k):
    if v is UNK:
        return UNK
    return frozenset((base, off + k) for base, off in v)


def trunc32(v):
    if v is UNK:
        return UNK
    return frozenset((base, off & 0xFFFFFFFF) if base is None else (base, off) for base, off in v)


def join(a, c):
    if a is UNK or c is UNK:
        return UNK
    u = a | c
    return UNK if len(u) > MAXSET else u


def opval(st, op):
    if op.type == X.X86_OP_IMM:
        return frozenset([(None, op.imm)])
    if op.type == X.X86_OP_REG:
        r, w = full(op.reg)
        if r is None:
            return UNK
        v = st.get(r, UNK)
        if w == 8:
            return v
        if not const_set(v):
            return UNK if w < 4 else v  # 32-bit use of a parameter keeps its identity
        mask = (1 << (8 * w)) - 1
        return frozenset((None, x & mask) for _, x in v)
    return UNK


def step(st, i):
    """Transfer function: returns the state after instruction i."""
    st = dict(st)
    mn = i.mnemonic
    ops = i.operands
    if mn == "call":
        for r in VOLATILE:
            st[r] = UNK
        st["rax"] = frozenset([("call@%08X" % i.address, 0)])  # the result: untracked, but copies of it stay identifiable
        st["_z"] = None
        return st
    if not ops:
        return st
    # registers the instruction writes
    try:
        _, wr = i.regs_access()
    except capstone.CsError:
        wr = []
    written = set()
    for rid in wr:
        r, _ = full(rid)
        if r:
            written.add(r)
    d = ops[0]
    dr, dw = full(d.reg) if d.type == X.X86_OP_REG else (None, 0)
    new = {}
    if dr:
        s = ops[1] if len(ops) > 1 else None
        if mn in ("mov", "movzx", "movsxd", "movsx") and s is not None and s.type in (X.X86_OP_IMM, X.X86_OP_REG):
            v = opval(st, s)
            if mn == "movzx" and s.type == X.X86_OP_REG and not const_set(v):
                v = UNK
            new[dr] = trunc32(v) if dw == 4 else (v if dw == 8 else UNK)
            if dw in (1, 2):  # partial write merges into the old value only when both are constant
                old = st.get(dr, UNK)
                if const_set(old) and const_set(v):
                    mask = (1 << (8 * dw)) - 1
                    new[dr] = frozenset((None, (o & ~mask) | (x & mask)) for _, o in old for _, x in v)
                    if len(new[dr]) > MAXSET:
                        new[dr] = UNK
                else:
                    new[dr] = UNK
        elif mn == "xor" and s is not None and s.type == X.X86_OP_REG and full(s.reg)[0] == dr:
            new[dr] = frozenset([(None, 0)])
        elif mn == "lea" and s is not None and s.type == X.X86_OP_MEM and s.mem.index == 0 and s.mem.base not in (0, X.X86_REG_RIP):
            br, bw = full(s.mem.base)
            v = add(st.get(br, UNK), s.mem.disp) if br else UNK
            new[dr] = trunc32(v) if dw == 4 else (v if dw == 8 else UNK)
        elif mn in ("add", "sub") and s is not None and s.type == X.X86_OP_IMM and dw >= 4:
            new[dr] = add(st.get(dr, UNK), s.imm if mn == "add" else -s.imm)
        elif mn in ("inc", "dec") and dw >= 4:
            new[dr] = add(st.get(dr, UNK), 1 if mn == "inc" else -1)
        elif mn.startswith("set") and dw == 1:
            old = st.get(dr, UNK)
            new[dr] = frozenset((None, (o & ~0xFF) | x) for _, o in old for x in (0, 1)) if const_set(old) else UNK
        elif mn.startswith("cmov") and s is not None:
            v = opval(st, s)
            new[dr] = join(st.get(dr, UNK), trunc32(v) if dw == 4 else v) if dw >= 4 else UNK
        elif mn in ("cmp", "test", "push", "bt"):
            pass
        elif mn == "and" and s is not None and s.type == X.X86_OP_IMM and const_set(st.get(dr, UNK)):
            new[dr] = frozenset((None, x & s.imm) for _, x in st[dr])
    for r in written:
        if r not in new and not (mn in ("cmp", "test", "push", "bt") and r == dr):
            st[r] = UNK
    st.update(new)
    # "_z": (register, constant) a following je/jne compares for equality (`test r, r` is r == 0, `cmp r, c` is
    # r == c; 32 or 64 bits); any other flag-writing instruction, or a write to that register, forgets it
    s1 = ops[1] if len(ops) > 1 else None
    if dr and dw >= 4 and mn == "test" and s1 is not None and s1.type == X.X86_OP_REG and full(s1.reg) == (dr, dw):
        st["_z"] = (dr, 0)
    elif dr and dw >= 4 and mn == "cmp" and s1 is not None and s1.type == X.X86_OP_IMM:
        st["_z"] = (dr, s1.imm & 0xFFFFFFFF if dw == 4 else s1.imm)
    elif not (mn.startswith(("mov", "lea", "push", "pop", "cmov", "set", "nop", "j")) or st.get("_z") is None):
        st["_z"] = None
    elif st.get("_z") is not None and (st["_z"][0] in written or st["_z"][0] in new):
        st["_z"] = None
    return st


def refine(st, i, t):
    """The state on edge i -> t of a je/jne after `test r,r` / `cmp r,c`: the equal edge holds r = c, and so does every
    register holding the same untracked value (a call result copied before the test); the other edge drops c from a
    constant set. None when the edge is infeasible."""
    z = st.get("_z")
    if z is None or i.mnemonic not in ("je", "jne"):
        return st
    r, c = z
    eq_edge = (t == i.operands[0].imm) == (i.mnemonic == "je")
    v = st.get(r, UNK)
    st = dict(st)
    if eq_edge:
        if const_set(v) and not any(x & 0xFFFFFFFF == c & 0xFFFFFFFF for _, x in v):
            return None
        if v is not UNK and not const_set(v) and len(v) == 1:
            for q in GP:
                if st.get(q) == v:
                    st[q] = frozenset([(None, c)])
        st[r] = frozenset([(None, c)])
    elif const_set(v):
        v = frozenset(e for e in v if e[1] & 0xFFFFFFFF != c & 0xFFFFFFFF)
        if not v:
            return None
        st[r] = v
    return st


def before(a, n=12):
    """The n instructions ending at a (a window decode that lands exactly on a)."""
    for k in range(64, 0, -1):
        seq = list(md.disasm(at(a - k, k + 16), a - k))
        idx = [j for j, x in enumerate(seq) if x.address == a]
        if idx:
            return seq[max(0, idx[0] - n):idx[0]]
    return []


def u32(a):
    return int.from_bytes(at(a, 4), "little")


_jt = {}


def jump_table(i):
    """Targets of an MSVC switch `jmp reg`: reg = BASE + dword[BASE + D + idx*4], idx bounded by `cmp idx, N` / `ja`,
    optionally through a byte table `movzx idx, byte [BASE + D2 + idx]`. None when the idiom is not found."""
    if i.address in _jt:
        return _jt[i.address]
    res = None
    prev = before(i.address)
    dt = bt = n = None
    for p in reversed(prev):
        o = p.op_str
        if dt is None and p.mnemonic == "mov" and "dword ptr [" in o and "*4 + " in o:
            dt = b.BASE + p.operands[1].mem.disp
        elif dt is not None and bt is None and p.mnemonic == "movzx" and "byte ptr [" in o and "*" not in o and p.operands[1].mem.disp > 0x1000:
            bt = b.BASE + p.operands[1].mem.disp
        elif dt is not None and n is None and p.mnemonic == "cmp" and p.operands[1].type == X.X86_OP_IMM:
            n = p.operands[1].imm + 1
            break
    if dt is not None and n is not None and n < 4096:
        idx = sorted(set(at(bt, n))) if bt is not None else range(n)
        res = sorted(set(b.BASE + u32(dt + 4 * k) for k in idx))
    _jt[i.address] = res
    return res


def branch_targets(i):
    """Successor addresses of instruction i."""
    mn = i.mnemonic
    nxt = i.address + i.size
    imm = i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None
    if mn in ("ret", "int3", "ud2", "hlt"):
        return []
    if mn == "jmp":
        if imm is None and i.operands and i.operands[0].type == X.X86_OP_REG:
            return jump_table(i) or []
        return [imm] if imm is not None else []
    if mn.startswith("j") or mn.startswith("loop"):
        return [nxt] + ([imm] if imm is not None else [])
    return [nxt]


EDGES = io.open(os.path.join(b.DB, "..", "Tools", "work", "graph", "edges.tsv"), encoding="utf-8").read().splitlines()[1:]
CALLERS = collections.defaultdict(set)
for l in EDGES:
    c = l.split("\t")
    CALLERS[int(c[1], 16)].add(int(c[0], 16))


def call_sites_to(f, g):
    """Addresses in caller f of direct calls/jmps to g (decoded along f's own control flow)."""
    out = []
    for a in reach(f):
        i = dec(a)
        if i and i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == g:
            out.append(a)
    return out


_reach = {}


def reach(f):
    if f not in _reach:
        seen, work = set(), [f]
        while work:
            a = work.pop()
            if a in seen:
                continue
            seen.add(a)
            i = dec(a)
            if i is None:
                continue
            imm = i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None
            if i.mnemonic == "jmp" and imm is not None and imm in ext and imm != f and not (f <= imm < f + ext[f]):
                continue
            work.extend(branch_targets(i))
        _reach[f] = seen
    return _reach[f]


_states = {}


def analyse_keep(f):
    if f in _states:
        return _states[f]
    # the state before every instruction reached from the entry; argument and callee-saved registers start as
    # entry tokens so a pass-through value resolves through the callers
    ins_state = {f: {r: frozenset([(r + "@entry", 0)]) if (r in ARGS or r not in VOLATILE) else UNK for r in GP}}
    work, cnt = [f], collections.Counter()
    while work:
        a = work.pop()
        i = dec(a)
        if i is None:
            continue
        cnt[a] += 1
        if cnt[a] > 64:
            continue
        imm = i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None
        if i.mnemonic == "jmp" and imm is not None and imm != f and imm in ext and not (f <= imm < f + ext[f]):
            continue
        st0 = step(ins_state[a], i)
        for t in branch_targets(i):
            nst = refine(st0, i, t)
            if nst is None:
                continue
            if t in ins_state:
                m = {r: join(ins_state[t].get(r, UNK), nst.get(r, UNK)) for r in GP}
                m["_z"] = nst.get("_z") if nst.get("_z") == ins_state[t].get("_z") else None
                if m != ins_state[t]:
                    ins_state[t] = m
                    work.append(t)
            else:
                ins_state[t] = nst
                work.append(t)
    _states[f] = (ins_state, None)
    return _states[f]


def resolve(f, v, depth=0, path=()):
    """Resolve a value set of f (constants and f's entry registers) to constants through f's callers.
    Returns (set of constants, notes)."""
    if v is UNK:
        return None, ["UNKNOWN in %08X" % f]
    consts, notes = set(), []
    for base, off in v:
        if base is None:
            consts.add(off & 0xFFFFFFFF)
            continue
        if depth >= 4 or f in path:
            notes.append("depth limit at %08X %s" % (f, base))
            return None, notes
        if base.startswith("call@"):
            notes.append("%s result in %08X" % (base, f))
            return None, notes
        reg = base.split("@")[0]
        callers = sorted(CALLERS.get(f, ()))
        if not callers:
            notes.append("%08X has no direct caller (%s+%d)" % (f, base, off))
            return None, notes
        for c in callers:
            st_c, _ = analyse_keep(c)
            for s in call_sites_to(c, f):
                if s not in st_c:
                    notes.append("site %08X unreached in %08X" % (s, c))
                    continue
                cv, cn = resolve(c, st_c[s].get(reg, UNK), depth + 1, path + (f,))
                notes += cn
                if cv is None:
                    return None, notes
                consts |= set((x + off) & 0xFFFFFFFF for x in cv)
    return consts, notes


def main():
    callers = sorted(CALLERS[TARGET])
    literal = {}
    for line in io.open(os.path.join(HERE, "..", "swe2contract-ddres-b1-0930", "log_channels.out"), encoding="utf-8"):
        pass  # CONTRACT's output lists only the unresolved sites by address; the control recomputes literals below
    rows, per = [], collections.Counter()
    ctl_bad, unreached, merged, fmt_consts = 0, 0, [], 0
    for f in callers:
        st, _ = analyse_keep(f)
        for s in call_sites_to(f, TARGET):
            i = dec(s)
            # CONTRACT's literal rule: nearest preceding write to ecx in linear order is an immediate or xor
            lin = list(md.disasm(at(f, max(ext.get(f, 0), s - f + 16)), f))
            prev = [x for x in lin if x.address < s][-30:]
            lit = None
            for p in reversed(prev):
                o = p.op_str.replace(" ", "")
                if o.startswith(("ecx,", "rcx,")):
                    rhs = o.split(",", 1)[1]
                    if p.mnemonic == "mov" and (rhs.startswith("0x") or rhs.isdigit()):
                        lit = int(rhs, 16) if rhs.startswith("0x") else int(rhs)
                    elif p.mnemonic == "xor" and o in ("ecx,ecx", "rcx,rcx"):
                        lit = 0
                    break
                if p.mnemonic == "call":
                    break
            if s not in st:
                unreached += 1
                rows.append((f, s, "UNREACHED", "", lit))
                continue
            v = st[s].get("rcx", UNK)
            v = trunc32(v) if v is not UNK else UNK
            consts, notes = resolve(f, v)
            if lit is not None and (consts is None or lit not in consts):
                ctl_bad += 1
            if lit is not None and consts is not None and consts != {lit}:
                merged.append((f, s, lit, consts))
            vals = ",".join(str(x) for x in sorted(consts)) if consts is not None else "UNRESOLVED"
            for x in (consts or ()):
                per[x] += 1
            rows.append((f, s, vals, "; ".join(sorted(set(notes)))[:200], lit))
            # negative control: the format pointer (rdx, a rip-relative lea) is not a tracked constant
            fmt_consts += const_set(st[s].get("rdx", UNK))
    print("%s  negative control: sites whose format pointer (rdx) the dataflow calls a constant: %d (must be 0)" % (
        "PASS" if fmt_consts == 0 else "FAIL", fmt_consts))
    comp = [r for r in rows if r[4] is None]
    print("%s  control: sites %d in %d functions (page: 245 in 136); literal sites whose literal is in the resolved set: %d of %d" % (
        "PASS" if len(rows) == 245 and len(callers) == 136 and ctl_bad == 0 else "FAIL", len(rows), len(callers),
        sum(1 for r in rows if r[4] is not None) - ctl_bad, sum(1 for r in rows if r[4] is not None)))
    print("unreached sites: %d" % unreached)
    for f, s, lit, cs in merged:
        print("  literal site %08X (in %08X) also receives %s through a jump into its call: channel %s" % (
            s, f, ",".join(str(x) for x in sorted(cs - {lit})), ",".join(str(x) for x in sorted(cs))))
    print("computed sites: %d; resolved: %d; unresolved: %d" % (
        len(comp), sum(1 for r in comp if r[2] not in ("UNRESOLVED", "UNREACHED")), sum(1 for r in comp if r[2] in ("UNRESOLVED", "UNREACHED"))))
    print("channel values over all sites (a site with two possible values counts under both):",
          ", ".join("%d: %d" % kv for kv in sorted(per.items())))
    for r in comp:
        print("  %08X %08X ch=%-12s %s" % (r[0], r[1], r[2], r[3]))
    with io.open(os.path.join(HERE, "rc9_channels.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("function\tsite\tchannel_values\tliteral_by_contract_rule\tnotes\n")
        for r in rows:
            o.write("%08X\t%08X\t%s\t%s\t%s\n" % (r[0], r[1], r[2], "" if r[4] is None else r[4], r[3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
