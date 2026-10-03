"""k54flow.py - FABLE 2026-10-03. A small reaching-definition / affine-value analysis over one function body of the
certified image (rvlib decode, capstone operands), used by k54_residue.py.

Values are affine: (sym, a, c) = sym + a*P + c, where sym is None or a base name ('PARAM', 'REC', 'SP0') and P is the
iteration count of ONE loop (the header given to `loop_proof`). An absent key is TOP (unknown). Locations are the 16
GPR families and stack slots, keyed by their offset from the entry rsp ('SP0'), so rsp-, rbp- and r11-relative
addresses alias correctly.

Calls: rax rcx rdx r8-r11 become TOP; the callee's home area [rsp, rsp+0x20) and a 0x100-byte window above every
stack address passed in rcx/rdx/r8/r9 (or held in an outgoing stack argument) are invalidated. __chkstk (00808F10)
preserves everything except rsp handling, so it is modelled as a no-op. Writes through non-stack pointers are assumed
not to alias the frame (MSVC code; every frame address that escapes is a lea we see).

The loop proof is inductive: entry state E at the header (dataflow from the function entry, the header a sink);
hypothesis h[L] = (s, A, c0) with E[L] = (s, 0, c0); the body is run from the header with h and every back edge must
deliver h[L] with P -> P+1, i.e. (s, A, c0 + A). Locations that fail are dropped and the body re-run until stable.
"""
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
from rvlib import Body, fam

VOLATILE = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
CHKSTK = 0x808F10
FLAGSET = set("cmp test sub add and or xor inc dec shl shr sar neg bt".split())


def vadd(x, y):
    if x is None or y is None:
        return None
    if x[0] is not None and y[0] is not None:
        return None
    return (x[0] if x[0] is not None else y[0], x[1] + y[1], x[2] + y[2])


def vscale(x, k):
    if x is None or (x[0] is not None and k != 1):
        return None
    return (x[0], x[1] * k, x[2] * k)


def const(c):
    return (None, 0, c)


class State(object):
    __slots__ = ("r", "s")

    def __init__(self, r=None, s=None):
        self.r = dict(r or {})
        self.s = dict(s or {})   # off -> (value, size)

    def copy(self):
        return State(self.r, self.s)

    def join(self, o):
        r = {k: v for k, v in self.r.items() if o.r.get(k) == v}
        s = {k: v for k, v in self.s.items() if o.s.get(k) == v}
        return State(r, s)

    def __eq__(self, o):
        return self.r == o.r and self.s == o.s

    def get(self, loc):
        if isinstance(loc, int):
            e = self.s.get(loc)
            return e[0] if e else None
        return self.r.get(loc)


class Flow(object):
    def __init__(self, img, start, end):
        self.B = Body(img, start, end)
        assert self.B.exact, "decode not exact"
        self.start = start
        self.preds = {}
        for a in self.B.order:
            for t in self.B.succ(a):
                self.preds.setdefault(t, []).append(a)

    # ------------------------------------------------------------------ operand evaluation
    def addr(self, st, m):
        if m["base"] == "rip":
            return None
        v = const(m["disp"])
        if m["base"]:
            v = vadd(v, st.r.get(fam(m["base"])))
        if m["index"]:
            v = vadd(v, vscale(st.r.get(fam(m["index"])), m["scale"]))
        return v

    def slot(self, st, m):
        a = self.addr(st, m)
        if a is not None and a[0] == "SP0" and a[1] == 0:
            return a[2]
        return None

    def kill_slots(self, st, lo, hi):
        for k in list(st.s):
            sz = st.s[k][1]
            if k < hi and k + sz > lo:
                del st.s[k]

    def store(self, st, off, size, val):
        self.kill_slots(st, off, off + size)
        if val is not None and not (size < 8 and val[0] is not None) and size >= 4:
            st.s[off] = (val, size)

    def load(self, st, off, size):
        e = st.s.get(off)
        if not e:
            return None
        v, sz = e
        if sz == size or (size == 4 and sz == 8 and v[0] is None):
            return v
        return None

    def setreg(self, st, name, size, val):
        f = fam(name)
        if val is not None and size < 8 and val[0] is not None:
            val = None
        if size < 4:
            val = None
        if val is None:
            st.r.pop(f, None)
        else:
            st.r[f] = val

    # ------------------------------------------------------------------ transfer
    def step(self, a, st):
        I = self.B[a]
        ci = I.ci
        m = I.mnemonic
        ops = ci.operands
        st = st.copy()
        if m == "call":
            t = I.direct_target()
            if t == CHKSTK:
                return st
            rsp = st.r.get("rsp")
            esc = []
            for r in ("rcx", "rdx", "r8", "r9"):
                v = st.r.get(r)
                if v is not None and v[0] == "SP0" and v[1] == 0:
                    esc.append(v[2])
            if rsp is not None and rsp[0] == "SP0":
                self.kill_slots(st, rsp[2], rsp[2] + 0x20)
                for off, (v, sz) in list(st.s.items()):
                    if rsp[2] + 0x20 <= off < rsp[2] + 0x80 and v[0] == "SP0" and v[1] == 0:
                        esc.append(v[2])
            else:
                st.s.clear()
            for e in esc:
                self.kill_slots(st, e, e + 0x100)
            for r in VOLATILE:
                st.r.pop(r, None)
            return st
        if m == "push":
            rsp = vadd(st.r.get("rsp"), const(-8))
            self.setreg(st, "rsp", 8, rsp)
            if rsp is not None and rsp[0] == "SP0":
                v = st.r.get(fam(ci.reg_name(ops[0].reg))) if ops[0].type == X86_OP_REG else None
                self.store(st, rsp[2], 8, v)
            return st
        if m == "pop":
            rsp = st.r.get("rsp")
            v = self.load(st, rsp[2], 8) if rsp is not None and rsp[0] == "SP0" else None
            self.setreg(st, "rsp", 8, vadd(rsp, const(8)))
            if ops[0].type == X86_OP_REG:
                self.setreg(st, ci.reg_name(ops[0].reg), 8, v)
            return st

        handled = set()
        if ops and ops[0].type == X86_OP_REG:
            dn = ci.reg_name(ops[0].reg)
            df = fam(dn)
            ds = ops[0].size
            val = None
            src = ops[1] if len(ops) > 1 else None
            cur = st.r.get(df)

            def srcval():
                if src is None:
                    return None
                if src.type == X86_OP_IMM:
                    return const(src.imm)
                if src.type == X86_OP_REG:
                    v = st.r.get(fam(ci.reg_name(src.reg)))
                    if v is not None and src.size < 8 and v[0] is not None:
                        return None
                    if src.size < 4:
                        return None
                    return v
                if src.type == X86_OP_MEM:
                    mm = I.mems[0]
                    off = self.slot(st, mm)
                    if off is None:
                        return None
                    return self.load(st, off, src.size)
                return None

            if m in ("mov", "movsxd"):
                val = srcval()
            elif m == "movzx":
                val = None
            elif m == "lea":
                val = self.addr(st, I.mems[0])
            elif m in ("add", "sub"):
                sv = srcval()
                if m == "sub":
                    sv = vscale(sv, -1) if sv is not None and sv[0] is None else None
                val = vadd(cur, sv)
            elif m == "inc":
                val = vadd(cur, const(1))
            elif m == "dec":
                val = vadd(cur, const(-1))
            elif m == "shl" and src is not None and src.type == X86_OP_IMM:
                val = vscale(cur, 1 << src.imm) if cur is not None and cur[0] is None else None
            elif m == "xor" and src is not None and src.type == X86_OP_REG and fam(ci.reg_name(src.reg)) == df:
                val = const(0)
            elif m in ("cmp", "test", "bt"):
                return st
            else:
                val = None
            self.setreg(st, dn, ds, val)
            handled.add(df)
        elif ops and ops[0].type == X86_OP_MEM and m not in ("cmp", "test", "bt", "prefetch", "nop"):
            mm = I.mems[0]
            off = self.slot(st, mm)
            if off is not None:
                sz = ops[0].size
                src = ops[1] if len(ops) > 1 else None
                if m == "mov":
                    if src.type == X86_OP_REG:
                        v = st.r.get(fam(ci.reg_name(src.reg)))
                        if v is not None and src.size < 8 and v[0] is not None:
                            v = None
                    elif src.type == X86_OP_IMM:
                        v = const(src.imm)
                    else:
                        v = None
                    self.store(st, off, sz, v)
                elif m in ("add", "sub", "inc", "dec") and sz >= 4:
                    cur = self.load(st, off, sz)
                    if m == "inc":
                        v = vadd(cur, const(1))
                    elif m == "dec":
                        v = vadd(cur, const(-1))
                    elif src.type == X86_OP_IMM:
                        v = vadd(cur, const(src.imm if m == "add" else -src.imm))
                    else:
                        v = None
                    self.store(st, off, sz, v)
                else:
                    self.kill_slots(st, off, off + max(sz, 1))
        # any other register the instruction writes (implicit operands, xchg, cdq, div ...)
        for r in I.reg_writes:
            if r in handled or r.startswith("xmm") or r in ("rflags", "rip"):
                continue
            if r == "rsp" and m in ("push", "pop", "call", "ret"):
                continue
            st.r.pop(r, None)
        return st

    # ------------------------------------------------------------------ dataflow
    def run(self, entry, st0, sink=None):
        """Forward dataflow from `entry`. Returns (in_states, arrivals at sink [(pred, state)])."""
        ins = {entry: st0}
        arrivals = []
        work = [entry]
        while work:
            a = work.pop()
            st = self.step(a, ins[a])
            for t in self.B.succ(a):
                if t == sink and not (t == entry):
                    arrivals.append((a, st))
                    continue
                if t == entry and sink == entry:
                    arrivals.append((a, st))
                    continue
                old = ins.get(t)
                new = st if old is None else old.join(st)
                if old is None or not (new == old):
                    ins[t] = new
                    work.append(t)
        # de-duplicate arrivals: keep the last state per predecessor after the fixpoint by recomputing
        last = {}
        for a in self.B.order:
            if a in ins:
                for t in self.B.succ(a):
                    if t == sink:
                        last[a] = self.step(a, ins[a])
        return ins, sorted(last.items())

    def entry_state(self, param_reg, rec_reg):
        st = State()
        st.r["rsp"] = ("SP0", 0, 0)
        st.r[param_reg] = ("PARAM", 0, 0)
        if rec_reg:
            st.r[rec_reg] = ("REC", 0, 0)
        return st

    def loop_proof(self, header, param_reg, rec_reg, max_iter=40):
        """Returns (ok, hyp, body_in_states, log)."""
        _, ent = self.run(self.start, self.entry_state(param_reg, rec_reg), sink=header)
        if not ent:
            return False, {}, {}, ["header not reached from entry"]
        E = ent[0][1]
        for _, s in ent[1:]:
            E = E.join(s)
        hyp = {}
        for L, v in list(E.r.items()) + [(k, e[0]) for k, e in E.s.items()]:
            hyp[L] = (v[0], 1 if v[0] is None else 0, v[2])
        sizes = {k: e[1] for k, e in E.s.items()}
        log = []
        for it in range(max_iter):
            H = State()
            for L, v in hyp.items():
                if isinstance(L, int):
                    H.s[L] = (v, sizes[L])
                else:
                    H.r[L] = v
            ins, backs = self.run(header, H, sink=header)
            new = {}
            for L, (s, A, c0) in hyp.items():
                bv = [b.get(L) for _, b in backs]
                if all(x == (s, A, c0 + A) for x in bv):
                    new[L] = (s, A, c0)
                elif all(x == (s, A, c0) for x in bv):          # unchanged on every back edge: invariant
                    new[L] = (s, 0, c0)
                elif bv and all(x is not None and x[0] == s and x[1] == A for x in bv) and len(set(x[2] for x in bv)) == 1 \
                        and A == 1:
                    d = bv[0][2] - c0                            # constant stride d: value = c0 + d*P
                    new[L] = (s, d, c0)
                # else dropped (TOP)
            if new == hyp:
                return True, hyp, ins, log + ["stable after %d iterations, %d back edges" % (it + 1, len(backs))]
            hyp = new
        return False, hyp, {}, log + ["no fixpoint"]
