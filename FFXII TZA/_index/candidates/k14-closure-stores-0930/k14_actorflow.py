"""k14_actorflow.py - K-14: can anything 002E45E0 runs write actor byte +3? OPUS, 2026-09-30. Static. Reads only.

002E5030 checks the actor class at 002E5077 (`movzx eax, byte [rbx + 3]; and al, 0xE0; cmp al, 0x60`), then calls
Movement_UpdateSteeringTowardTarget 002E45E0 with rcx = the actor and rdx = [actor + 0xB8], then 002E4380, which
checks the class again. This follows the actor pointer from 002E45E0's entry through everything it runs:
- registers, the function's own stack (push/pop, spills, reloads), lea/add offsets;
- direct callees, analysed under the argument values they receive (memoised per context), with a summary back
  to the caller: the return value, and any actor-derived value the callee stores into the caller's stack;
- tail jumps (analysed as call + return), switch tables (rc9_channels.jump_table);
- memset/memcpy adapters by their destination and length.

Every memory store is classified by its base:
  ACTOR+3       the base is the actor pointer plus an offset, and the write covers byte +3 (the question);
  ACTOR-other   actor-derived, not covering +3;
  loaded/other  a pointer read from memory (named by where it was read), a call result, a global, the stack;
  UNKNOWN       nothing tracked.
Also reported: stores of the actor pointer into non-stack memory (escapes, since a later load could return it) and
indirect calls that receive it (blind spots).

Controls: (P) seeded at 00380D30 with rcx = actor, the tool must report its `mov dword [rbx], eax` (rbx = rcx) as
ACTOR+3; (O) the seven object-state setter stores (the README's manual finding) must trace to the 0x740-stride slot
table read through global 022C6F28, not to the actor.
"""
import collections, io, os, re, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402  (image access, decoder, switch tables, register naming)

ROOT = 0x002E45E0
MEMFN = {0x00861EC0: "memset", 0x004746F0: "memcpy-adapter"}
GP = R.GP + ["rsp"]
VOLATILE = R.VOLATILE
UNK = None
MAXSET = 12
MAXDEPTH = 10
SETTERS = (0x003E3120, 0x003E31E0, 0x003E33A0, 0x003E33C0, 0x003E33E0, 0x003E3440, 0x003E36C0)
md = R.md
ext = R.ext


def vs(*t):
    return frozenset(t)


def join(a, b):
    """Union; past MAXSET values it widens each base to an unknown offset (a loop cursor keeps its object),
    and only a set of more than MAXSET distinct bases becomes UNKNOWN."""
    if a is UNK or b is UNK:
        return UNK
    u = a | b
    if len(u) <= MAXSET:
        return u
    w = frozenset((b, None) for b, _ in u)
    return w if len(w) <= MAXSET else UNK


def add(v, k):
    if v is UNK:
        return UNK
    return frozenset((base, None if off is None or k is None else off + k) for base, off in v)


def has_actor(v):
    return v is not UNK and any(b == "A" for b, _ in v)


def sp_off(v):
    """The single own-stack offset v denotes, or None."""
    if v is not UNK and len(v) == 1:
        (b, o), = v
        if b == "SP" and o is not None:
            return o
    return None


def desc(v):
    if v is UNK:
        return "UNKNOWN"
    return ",".join(sorted("%s%s" % (b if b is not None else "", "" if o is None and b is not None else
                                     ("+?" if o is None else ("%+#x" % o if b is not None else "%#x" % o))) for b, o in v))


class St:
    __slots__ = ("r", "s")

    def __init__(self, r, s):
        self.r, self.s = r, s

    def copy(self):
        return St(dict(self.r), dict(self.s))

    def merge(self, o):
        r = {k: join(self.r.get(k, UNK), o.r.get(k, UNK)) for k in set(self.r) | set(o.r)}
        s = {k: join(self.s[k], o.s[k]) for k in set(self.s) & set(o.s)}
        return St(r, s)

    def __eq__(self, o):
        return self.r == o.r and self.s == o.s


def reg(st, rid):
    if md.reg_name(rid) == "rsp":
        return st.r.get("rsp", UNK), "rsp", 8
    r, w = R.full(rid)
    if r is None:
        return UNK, None, 0
    return st.r.get(r, UNK), r, w


def fullname(rid):
    n = md.reg_name(rid)
    if n == "rsp":
        return "rsp", 8
    return R.full(rid)


def memaddr(st, m, ins):
    """Value set of a memory operand's address (index registers make the offset unknown)."""
    if m.base == X.X86_REG_RIP:
        return vs(("G%08X" % (ins.address + ins.size + m.disp), 0))
    if m.base == 0:
        return UNK
    bn, _ = fullname(m.base)
    bv = st.r.get(bn, UNK)
    if bv is UNK:
        return UNK
    v = add(bv, m.disp)
    if m.index != 0:
        v = frozenset((b, None) for b, _ in v)
    return v


def load_value(st, addr):
    o = sp_off(addr)
    if o is not None:
        return st.s.get(o, UNK)
    if addr is UNK:
        return UNK
    out = set()
    for b, off in addr:
        if b is None:
            return UNK
        name = "L(%s%s)" % (b, "+?" if off is None else "%+#x" % off)
        if len(name) > 60:
            name = "L(deep)"
        out.add((name, 0))
    return frozenset(out)


class Analysis:
    def __init__(self):
        self.memo = {}
        self.stores = []        # (fn, addr, text, size, base desc, class)
        self.escapes = []       # (fn, addr, text, where)
        self.indirect = []      # (fn, addr, text, which args carry the actor)
        self.dispatch = set()   # every indirect call/jump reached: (fn, addr, text, import name or why not)
        self.recursive = []
        self.fns = set()

    def summary(self, f, ctx, depth, stack):
        key = (f, ctx)
        if key in self.memo:
            return self.memo[key]
        if f in stack or depth > MAXDEPTH:
            self.recursive.append((f, depth, any(has_actor(v) for _, v in ctx)))
            return (UNK, ())
        self.memo[key] = (UNK, ())  # provisional for recursion through the memo
        res = self.run(f, dict(ctx), depth, stack + (f,))
        self.memo[key] = res
        return res

    def run(self, f, ctx, depth, stack):
        self.fns.add(f)
        r0 = {r: UNK for r in GP}
        for r in ("rcx", "rdx", "r8", "r9"):
            r0[r] = ctx.get(r, UNK)
        r0["rsp"] = vs(("SP", 0))
        s0 = {}
        for k, v in ctx.items():
            if isinstance(k, int):
                s0[k] = v          # stack arguments, at the callee's own entry offsets (+0x28 ...)
        states = {f: St(r0, s0)}
        work, cnt = [f], collections.Counter()
        ret = UNK
        seen_ret = False
        caller_writes = {}
        while work:
            a = work.pop()
            i = R.dec(a)
            if i is None:
                continue
            cnt[a] += 1
            if cnt[a] > 40:
                continue
            st = states[a].copy()
            succ, st2, is_ret = self.step(f, st, i, depth, stack, caller_writes)
            if is_ret:
                rv = st2.r.get("rax", UNK) if st2 is not None else UNK
                ret = rv if not seen_ret else join(ret, rv)
                seen_ret = True
            for t in succ:
                if t in states:
                    m = states[t].merge(st2)
                    if not (m == states[t]):
                        states[t] = m
                        work.append(t)
                else:
                    states[t] = st2.copy()
                    work.append(t)
        if ret is not UNK:
            ret = frozenset(x for x in ret if x[0] != "SP" and not str(x[0]).startswith("CSP")) or UNK
        return (ret, tuple(sorted(caller_writes.items())))

    def store(self, f, i, st, addr, size, val):
        a3 = False
        if addr is not UNK:
            for b, o in addr:
                if b == "A" and (o is None or o <= 3 < o + size):
                    a3 = True
        cls = ("ACTOR+3" if a3 else "ACTOR-other" if has_actor(addr) else
               "UNKNOWN" if addr is UNK else "stack" if all(b in ("SP", "CSP") for b, _ in addr) else "loaded/other")
        self.stores.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), size, desc(addr), cls))
        o = sp_off(addr)
        if o is not None:
            for k in [k for k in st.s if k < o + size and o < k + 8 and k != o]:
                del st.s[k]
            if size == 8:
                st.s[o] = val
            else:
                st.s.pop(o, None)
        else:
            if addr is UNK or any(b == "SP" for b, _ in addr):
                st.s.clear()
            if has_actor(val):
                self.escapes.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), desc(addr)))

    def call(self, f, st, i, t, depth, stack, caller_writes):
        """Apply a direct call to t; returns the state after it."""
        if t in MEMFN:
            dst, n = st.r.get("rcx", UNK), st.r.get("r8", UNK)
            size = max(o for _, o in n) if n is not UNK and all(b is None for b, _ in n) else 1 << 20
            self.store(f, i, st, dst, size, UNK)
        else:
            ctx = {}
            for r in ("rcx", "rdx", "r8", "r9"):
                v = st.r.get(r, UNK)
                ctx[r] = self.export(v, st)
            rsp = sp_off(st.r.get("rsp", UNK))
            if rsp is not None:
                for k in range(0x28, 0x68, 8):
                    v = st.s.get(rsp + k - 8)
                    if has_actor(v):
                        ctx[k] = self.export(v, st)
            key = tuple(sorted(ctx.items(), key=lambda kv: str(kv[0])))
            rv, cw = self.summary(t, key, depth + 1, stack)
            for off, v in cw:  # the callee stored an actor-derived value into this function's stack
                st.s[off] = join(st.s.get(off, UNK), v) if off in st.s else v
            st.r["rax"] = rv if rv is not UNK else vs(("R%08X" % t, 0))
        for r in VOLATILE:
            if r != "rax":
                st.r[r] = UNK
        if t in MEMFN:
            st.r["rax"] = UNK
        return st

    def export(self, v, st):
        """A caller value as the callee sees it: own-stack offsets become caller-stack tokens CSP+off."""
        if v is UNK:
            return UNK
        return frozenset((("CSP", o) if b == "SP" else (b, o)) for b, o in v)

    def step(self, f, st, i, depth, stack, caller_writes):
        mn, ops = i.mnemonic, i.operands
        nxt = i.address + i.size
        imm = ops[0].imm if ops and ops[0].type == X.X86_OP_IMM else None
        if mn == "call":
            if imm is not None:
                return [nxt], self.call(f, st, i, imm, depth, stack, caller_writes), False
            carried = [r for r in ("rcx", "rdx", "r8", "r9") if has_actor(st.r.get(r, UNK))]
            if carried:
                self.indirect.append((f, i.address, "%s %s" % (mn, i.op_str), ",".join(carried)))
            self.dispatch.add((f, i.address, "%s %s" % (mn, i.op_str), import_name(i)))
            for r in VOLATILE:
                st.r[r] = UNK
            return [nxt], st, False
        if mn == "jmp" and imm is not None and imm != f and imm in ext and not (f <= imm < f + ext[f]):
            st = self.call(f, st, i, imm, depth, stack, caller_writes)  # tail jump = call + return
            return [], st, True
        if mn == "jmp" and imm is None and ops and ops[0].type == X.X86_OP_MEM:
            carried = [r for r in ("rcx", "rdx", "r8", "r9") if has_actor(st.r.get(r, UNK))]
            if carried:
                self.indirect.append((f, i.address, "%s %s" % (mn, i.op_str), ",".join(carried)))
            self.dispatch.add((f, i.address, "%s %s" % (mn, i.op_str), import_name(i)))
            return [], st, True
        if mn in ("ret", "retn"):
            return [], st, True
        if mn.startswith(("rep", "stos", "movs")) and ("stos" in mn or "movs" in mn and "movsx" not in mn and "movss" not in mn and "movsd" != mn):
            self.store(f, i, st, st.r.get("rdi", UNK), 1 << 20, UNK)
            st.r["rdi"] = UNK
            st.r["rcx"] = UNK
            st.r["rsi"] = UNK
            return R.branch_targets(i), st, False
        if mn == "push":
            v = UNK
            if ops[0].type == X.X86_OP_REG:
                v, _, _ = reg(st, ops[0].reg)
            elif ops[0].type == X.X86_OP_IMM:
                v = vs((None, ops[0].imm))
            st.r["rsp"] = add(st.r.get("rsp", UNK), -8)
            o = sp_off(st.r["rsp"])
            if o is not None:
                st.s[o] = v
            return [nxt], st, False
        if mn == "pop":
            o = sp_off(st.r.get("rsp", UNK))
            v = st.s.get(o, UNK) if o is not None else UNK
            if ops[0].type == X.X86_OP_REG:
                n, _ = fullname(ops[0].reg)
                if n:
                    st.r[n] = v
            st.r["rsp"] = add(st.r.get("rsp", UNK), 8)
            return [nxt], st, False
        # memory destination: a store
        if ops and ops[0].type == X.X86_OP_MEM and ops[0].access & capstone.CS_AC_WRITE and not mn.startswith(("cmp", "test", "prefetch", "lea", "nop")):
            addr = memaddr(st, ops[0].mem, i)
            val = UNK
            if len(ops) > 1 and ops[1].type == X.X86_OP_REG and mn == "mov":
                val, _, w = reg(st, ops[1].reg)
                if w != 8:
                    val = UNK
            elif len(ops) > 1 and ops[1].type == X.X86_OP_IMM and mn == "mov":
                val = vs((None, ops[1].imm))
            elif len(ops) > 1 and ops[1].type == X.X86_OP_IMM and mn in ("add", "sub") and ops[0].size == 8 \
                    and sp_off(addr) is not None:
                # a cursor kept in a stack slot and advanced in place (`add qword [rsp + 0x30], 0x10`)
                val = add(st.s.get(sp_off(addr), UNK), ops[1].imm if mn == "add" else -ops[1].imm)
            self.store(f, i, st, addr, ops[0].size, val)
            return R.branch_targets(i), st, False
        # register destination
        try:
            _, wr = i.regs_access()
        except capstone.CsError:
            wr = []
        written = set(n for n, _ in (fullname(x) for x in wr) if n)
        new = {}
        if ops and ops[0].type == X.X86_OP_REG:
            dn, dw = fullname(ops[0].reg)
            s = ops[1] if len(ops) > 1 else None
            if dn:
                if mn == "mov" and s is not None and s.type == X.X86_OP_REG:
                    v, _, w = reg(st, s.reg)
                    new[dn] = v if (dw == 8 and w == 8) else (UNK if not (v and all(b is None for b, _ in v)) else v)
                elif mn == "mov" and s is not None and s.type == X.X86_OP_IMM:
                    new[dn] = vs((None, s.imm))
                elif mn == "mov" and s is not None and s.type == X.X86_OP_MEM:
                    new[dn] = load_value(st, memaddr(st, s.mem, i)) if dw == 8 else UNK
                elif mn == "lea" and s is not None:
                    new[dn] = memaddr(st, s.mem, i) if dw == 8 else UNK
                elif mn == "xor" and s is not None and s.type == X.X86_OP_REG and fullname(s.reg)[0] == dn:
                    new[dn] = vs((None, 0))
                elif mn in ("add", "sub") and s is not None and s.type == X.X86_OP_IMM and dw == 8:
                    new[dn] = add(st.r.get(dn, UNK), s.imm if mn == "add" else -s.imm)
                elif mn == "add" and s is not None and s.type in (X.X86_OP_REG, X.X86_OP_MEM) and dw == 8:
                    # pointer + index: the pointer side keeps its identity with an unknown offset
                    a1 = st.r.get(dn, UNK)
                    a2 = reg(st, s.reg)[0] if s.type == X.X86_OP_REG else load_value(st, memaddr(st, s.mem, i))
                    ptr = set()
                    for v in (a1, a2):
                        if v is not UNK:
                            ptr |= set((b, None) for b, _ in v if b is not None)
                    new[dn] = frozenset(ptr) if ptr else UNK
                elif mn == "imul" and len(ops) == 3:
                    new[dn] = UNK  # three-operand imul overwrites the destination with src * imm (an index)
                elif mn.startswith("cmov") and s is not None and dw == 8:
                    v = reg(st, s.reg)[0] if s.type == X.X86_OP_REG else (load_value(st, memaddr(st, s.mem, i)) if s.type == X.X86_OP_MEM else UNK)
                    new[dn] = join(st.r.get(dn, UNK), v)
                elif mn == "xchg" and s is not None and s.type == X.X86_OP_REG:
                    sn, _ = fullname(s.reg)
                    new[dn], new[sn] = st.r.get(sn, UNK), st.r.get(dn, UNK)
                elif mn in ("cmp", "test", "bt"):
                    written.discard(dn)
                elif has_actor(st.r.get(dn, UNK)) and dw == 8 and mn in ("and", "or", "sub", "add", "imul", "shl", "shr"):
                    new[dn] = vs(("A", None))  # arithmetic on the actor pointer: offset unknown, kept conservatively
        for r in written:
            if r not in new:
                st.r[r] = UNK
        st.r.update(new)
        return R.branch_targets(i), st, False


_IAT = None


def import_name(i):
    """The DLL!name an indirect `call/jmp [rip + d]` dispatches through, or why it is not an import slot."""
    global _IAT
    if _IAT is None:
        import pefile
        pe = pefile.PE(R.b.EXE, fast_load=True)
        pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
        _IAT = {imp.address: "%s!%s" % (e.dll.decode(), (imp.name or b"#%d" % imp.ordinal).decode())
                for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    op = i.operands[0] if i.operands else None
    if op is None or op.type != X.X86_OP_MEM or op.mem.base != X.X86_REG_RIP:
        return "NOT-RIP (register or table dispatch)"
    return _IAT.get(i.address + i.size + op.mem.disp, "NOT-AN-IMPORT-SLOT")


def own_disp_covers3(text, size):
    """Whether the store's own displacement from its base register covers byte +3 of that base."""
    m = re.search(r"\[(\w+)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]", text)
    if not m or "*" in text.split(",")[0]:
        return True
    d = 0 if m.group(2) is None else int(m.group(3), 0) * (1 if m.group(2) == "+" else -1)
    return d <= 3 < d + size


def linear(f):
    return list(md.disasm(R.at(f, ext[f]), f))


def last_def(ins, a, regname):
    """The last instruction before a (linear order) whose first operand is regname or a sub-register of it."""
    for x in reversed([x for x in ins if x.address < a]):
        if x.operands and x.operands[0].type == X.X86_OP_REG and fullname(x.operands[0].reg)[0] == regname \
                and x.mnemonic not in ("cmp", "test", "push"):
            return x
    return None


def explain(f, a):
    """For an untracked store: its base register's linear definition, and when that is a stack-slot reload, every
    instruction in the function that writes the slot, each with its source's own definition."""
    out, ins = [], linear(f)
    i = next(x for x in ins if x.address == a)
    base = fullname(i.operands[0].mem.base)[0]
    d = last_def(ins, a, base)
    out.append("base %s <- %s" % (base, "%08X %s %s" % (d.address, d.mnemonic, d.op_str) if d else "entry"))
    if d is not None and d.mnemonic == "mov" and d.operands[1].type == X.X86_OP_MEM and md.reg_name(d.operands[1].mem.base) == "rsp":
        disp = d.operands[1].mem.disp
        for x in ins:
            o0 = x.operands[0] if x.operands else None
            if o0 is not None and o0.type == X.X86_OP_MEM and md.reg_name(o0.mem.base) == "rsp" and o0.mem.disp == disp \
                    and o0.access & capstone.CS_AC_WRITE:
                src = ""
                if len(x.operands) > 1 and x.operands[1].type == X.X86_OP_REG:
                    sd = last_def(ins, x.address, fullname(x.operands[1].reg)[0])
                    src = " ; source %s" % ("%08X %s %s" % (sd.address, sd.mnemonic, sd.op_str) if sd else "the entry register")
                out.append("slot [rsp%+#x] writer %08X %s %s%s" % (disp, x.address, x.mnemonic, x.op_str, src))
    return out


def analyse(root, ctx):
    an = Analysis()
    an.summary(root, tuple(sorted(ctx.items())), 0, ())
    return an


def main():
    A = vs(("A", 0))
    # (P) positive control: a direct seed on a body that stores through rcx at +0
    pc = analyse(0x00380D30, {"rcx": A})
    p_ok = any(s[5] == "ACTOR+3" and s[1] == 0x00380DA6 for s in pc.stores)
    print("%s  control P: seeded at 00380D30 with rcx = actor, 00380DA6 `mov dword [rbx], eax` is ACTOR+3" % ("PASS" if p_ok else "FAIL"))
    # the question
    an = analyse(ROOT, {"rcx": A, "rdx": vs(("L(A+0xb8)", 0))})
    # (O) the seven setters' stores trace to the slot table, not the actor
    ss = [s for s in an.stores if s[0] in SETTERS]
    o_ok = bool(ss) and all(s[5] == "loaded/other" and "G022C6F28" in s[4] for s in ss if "+0x580" in s[4] or True)
    print("%s  control O: object-state setter stores (%d) all loaded/other through the slot table read at 022C6F28: %s" % (
        "PASS" if o_ok else "FAIL", len(ss), sorted(set(s[4] for s in ss))[:4]))
    cut_actor = [c for c in an.recursive if c[2]]
    print("%s  bodies analysed: %d (contexts %d); recursion or depth cuts: %d, of which carry the actor: %d" % (
        "PASS" if not cut_actor else "FAIL", len(an.fns), len(an.memo), len(an.recursive), len(cut_actor)))
    cls = collections.Counter(s[5] for s in an.stores)
    print("stores by class:", dict(sorted(cls.items())))
    for s in an.stores:
        if s[5] == "ACTOR+3":
            print("  ACTOR+3   %08X %08X %-44s size %d base %s" % s[:5])
    for s in sorted(set(an.stores)):
        if s[5] == "ACTOR-other":
            print("  ACTOR-oth %08X %08X %-44s size %d base %s" % s[:5])
    print("actor pointer stored to non-stack memory (escapes): %d" % len(an.escapes))
    for e in sorted(set(an.escapes)):
        print("  ESCAPE    %08X %08X %-44s to %s" % e)
    engine = [d for d in an.dispatch if "!" not in d[3]]
    print("%s  indirect calls/jumps reached: %d, through an import slot: %d, into engine code: %d" % (
        "PASS" if not engine else "OPEN", len(an.dispatch), len(an.dispatch) - len(engine), len(engine)))
    for d in sorted(an.dispatch):
        print("  DISPATCH  %08X %08X %-36s %s" % d)
    print("indirect calls/jumps receiving the actor: %d" % len(set(an.indirect)))
    for e in sorted(set(an.indirect)):
        print("  INDIRECT  %08X %08X %-44s args %s" % e)
    unk = sorted(set(s for s in an.stores if s[5] == "UNKNOWN"))
    unk3 = [s for s in unk if own_disp_covers3(s[2], s[3])]
    print("stores with an untracked base: %d; of them able to reach byte +3 of their own base: %d" % (len(unk), len(unk3)))
    for s in unk3:
        print("  RESIDUE   %08X %08X %-44s" % s[:3])
        for line in explain(s[0], s[1]):
            print("            " + line)
    with io.open(os.path.join(HERE, "k14_actorflow.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("function\taddress\tinstruction\tsize\tbase\tclass\n")
        for s in sorted(set(an.stores)):
            o.write("%08X\t%08X\t%s\t%d\t%s\t%s\n" % s)
    return 0 if p_ok and o_ok else 1


if __name__ == "__main__":
    sys.exit(main())
