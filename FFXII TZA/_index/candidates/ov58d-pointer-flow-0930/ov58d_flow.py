"""ov58d_flow.py - OV-5/OV-8 (d), the gap FABLE's T3b leaves: the state-pointer flow census. OPUS, 2026-09-30.
Static. Reads only.

Region A (the packed class words of classes 5, 6 and 7) is state + 0x4748 .. + 0x4F0F (021B7054..021B781B with the
state at 021B290C). FABLE's T3b (`../fable-astra-live-facts-0930/t3b_ov58d_region_a.md`) excluded every direct
addressing form and listed the writers; its stated limit is the pointer-flow census over the 318 loads of the state
pointer, the image getters' call sites and the registry storage pointers (T3 gap 1). This runs that census.

Method: the value-flow engine of k14_actorflow.py (registers, the function's own stack, lea/add offsets, switch tables,
callees analysed under the argument values they receive, memoised per context, to depth 10), started at every
function that obtains a root:
  - a load of qword [02EBF190]                         -> state + 0
  - a load of the registry storage cells 01EEBCC8 / 01EEBD20 / 01EEBD78 (the class 5 / 6 / 7 rows' +0x08)
                                                          -> state + 0x4748 / + 0x47C8 / + 0x4B10
  - a load from those three registry rows at an unknown offset (a row walked by index) -> state + unknown
  - the return of the active image getter 002EF640     -> state - 0x4E68C (the image base)
  - any global the census finds a state-derived pointer stored into (an escape to a global) -> its stored value,
    iterated until no new global appears
and every caller of a function whose return value is state-derived (iterated). The capture getter 002EF620 returns
the capture image, not the active one; its stores are reported apart.

Every store (mov/arith to memory, rep stos/movs, memset/memcpy by destination and length) whose base is state-derived
is classified:
  REGION         a known offset whose written bytes overlap region A;
  INDEXED-BELOW  base + index with the base's own offset below region A's end: a non-negative index can reach it;
  INDEXED-ABOVE  base + index starting at or past region A's end;
  STATE-OTHER    a known offset outside region A.
Also listed: escapes (a state-derived pointer stored to non-stack memory), indirect calls receiving one, and depth or
recursion cuts that carry one - the census's blind spots, each read by hand in the README.

Controls (the writers FABLE lists; the census must find each from its own roots):
  C1  the state memset 002370D3 (memset [02EBF190], 0, 0x7410) as REGION;
  C2  the packed handler 002FD150's stores as REGION or INDEXED-BELOW;
  C3  the zeroing loop in 003047F0 (0030482A) as REGION or INDEXED-BELOW;
  C4  the kind-9 packet (built on 00580EB0's stack: 00581113 stores rsi = the image at packet +0x48, and its address goes to
      the enqueue 00582540 by reference) is copied into the queue with movups at 005825A0: that copy is an escape. This
      needs both the by-reference stack read and the xmm halves below; a census without them loses the save-load
      destination without saying so;
  C5  the reference census finds T3's 318 references to [02EBF190] (over the v3 extents and frontier bodies).
"""
import collections, io, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402

R = K.R
STATE_G = 0x02EBF190
# The active image is a STATIC object: 02164280 .. 021BA910 (0x56690 bytes), the state block at 021B290C inside it.
# A rip-relative address into it is the state at a known offset - the root class the first runs lacked (SWE2-AUDIT-SEM's
# REJECT of T3b, 837cdd743, found 002EF4A0 copying 0x6000 bytes from the mirror 02166480 into 021B290C by two leas).
IMG_LO, IMG_HI, STATE_ABS = 0x02164280, 0x021BA910, 0x021B290C
REG_CELLS = {0x01EEBCC8: 0x4748, 0x01EEBD20: 0x47C8, 0x01EEBD78: 0x4B10}
REG_ROWS = (0x01EEBCC0, 0x01EEC1F8)   # the class registry's 15 rows of 0x58 (003047F0 walks 01EEBCD0 .. 01EEC1F8)
IMG_GETTER, CAP_GETTER = 0x002EF640, 0x002EF620
IMG_TO_STATE = -0x4E68C
LO, HI = 0x4748, 0x4F10          # region A, state-relative, [LO, HI)
CTRL = {"C1": {0x002370D3}, "C2": None, "C3": None, "C4": {0x005825A0}}

# absolute global -> the state offsets of the pointers stored into it (None among them = an unknown offset). An escape
# global carries the offsets the census saw stored: 00253970 stores image+0x8200 into 020927C0, so a later
# `[020927C0] + 0x47B8` is image+0xC9B8 (the image head), not state+0x47B8. The first runs loaded every escape global
# at an unknown offset, which put 33 functions in INDEXED-UNKNOWN.
globals_root = {STATE_G: frozenset([("A", 0)])}   # absolute global -> the state tokens a load from it yields
TABLES = set()     # escape globals stored into at an index: a load anywhere in [g, g + TABLE_SPAN) yields their tokens
TABLE_SPAN = 0x100
# The battle-stats record getter: 00320AB0(i, kind) returns state + 8 + 0x1C8 * k after `cmp al, 0x27` (k <= 39) or 0.
# Its result is the token REC (record base + a known displacement): the 40 records span state +0x8 .. +0x4748 (exclusive),
# exactly where region A begins (corrected 2026-09-30 on SWE2-AUDIT-SPEC's review; REC_END below always computed this), so a store at REC + d with 0 <= d and d + size <= 0x1C8 cannot reach region A.
REC_GETTER, REC_SIZE, REC_END = 0x00320AB0, 0x1C8, 8 + 40 * 0x1C8


def g_token(addr):
    """The state value a load from this absolute global address yields, or None."""
    if addr in globals_root:
        return globals_root[addr]
    for g in TABLES:
        if g <= addr < g + TABLE_SPAN:
            return globals_root[g]
    if addr in REG_CELLS:
        return K.vs(("A", REG_CELLS[addr]))
    return None


_orig_memaddr = K.memaddr


def memaddr(st, m, ins):
    if m.base == X.X86_REG_RIP:
        t = ins.address + ins.size + m.disp
        if IMG_LO <= t < IMG_HI:
            v = K.vs(("A", t - STATE_ABS))
            return frozenset(("A", None) for _ in [0]) if m.index != 0 else v
    return _orig_memaddr(st, m, ins)


K.memaddr = memaddr

_orig_load = K.load_value


CSP_STACK = []     # per running body: {caller-stack offset: value} for caller slots that hold a state-derived value


def load_value(st, addr):
    if addr is not K.UNK and len(addr) == 1 and CSP_STACK:
        (b, off), = addr
        if b == "CSP" and off is not None and off in CSP_STACK[-1]:
            # a callee reading a structure its caller built on the stack and passed by reference (00581113 -> 00582540)
            return CSP_STACK[-1][off]
    if addr is not K.UNK:
        out = set()
        for b, off in addr:
            if isinstance(b, str) and b.startswith("G"):
                g = int(b[1:], 16)
                if off is not None:
                    t = g_token(g + off)
                    if t is not None:
                        out |= t
                        continue
                elif REG_ROWS[0] <= g < REG_ROWS[1]:
                    out.add(("AR", None))      # a class-storage pointer from an unknown registry row
                    continue
                elif g in TABLES:
                    out |= globals_root[g]     # an entry of an escape table at an unknown index
                    continue
            break
        else:
            if out:
                return frozenset(out)
    return _orig_load(st, addr)


K.load_value = load_value


class Census(K.Analysis):
    def __init__(self):
        super().__init__()
        self.hits = []          # (class, fn, addr, text, size, base desc)
        self.cap = []
        self.state_returners = set()
        self.esc_vals = collections.defaultdict(set)   # absolute global -> state tokens stored into it
        self.esc_tables = set()                          # globals stored into at an unknown index

    def run(self, f, ctx, depth, stack):
        K.ext.setdefault(f, 0)     # a call target the catalogue lacks (002EB5D0) is still a function start
        CSP_STACK.append(dict(ctx.get("csp") or ()))
        try:
            res = super().run(f, ctx, depth, stack)
        finally:
            CSP_STACK.pop()
        ret = res[0]
        if ret is not K.UNK and any(is_state(b) for b, _ in ret):
            self.state_returners.add(f)
        return res

    def call(self, f, st, i, t, depth, stack, caller_writes):
        if t == IMG_GETTER or t == CAP_GETTER:
            for r in K.VOLATILE:
                st.r[r] = K.UNK
            st.r["rax"] = K.vs(("A", IMG_TO_STATE)) if t == IMG_GETTER else K.vs(("CAP", 0))
            return st
        if t == REC_GETTER:
            for r in K.VOLATILE:
                st.r[r] = K.UNK
            st.r["rax"] = K.vs(("REC", 0))
            return st
        if t in K.MEMFN:
            return super().call(f, st, i, t, depth, stack, caller_writes)
        # K.Analysis.call, plus the caller's stack slots that hold a state-derived value, so a callee that reads a
        # structure passed by reference sees them (the context carries them, so the memo keeps them apart)
        ctx = {}
        for r in ("rcx", "rdx", "r8", "r9"):
            ctx[r] = self.export(st.r.get(r, K.UNK), st)
        rsp = K.sp_off(st.r.get("rsp", K.UNK))
        if rsp is not None:
            for k in range(0x28, 0x68, 8):
                v = st.s.get(rsp + k - 8)
                if K.has_actor(v):
                    ctx[k] = self.export(v, st)
        csp = tuple(sorted((o, self.export(v, st)) for o, v in st.s.items() if K.has_actor(v)))
        if csp:
            ctx["csp"] = csp
        key = tuple(sorted(ctx.items(), key=lambda kv: str(kv[0])))
        rv, cw = self.summary(t, key, depth + 1, stack)
        for off, v in cw:
            st.s[off] = K.join(st.s.get(off, K.UNK), v) if off in st.s else v
        st.r["rax"] = rv if rv is not K.UNK else K.vs(("R%08X" % t, 0))
        for r in K.VOLATILE:
            if r != "rax":
                st.r[r] = K.UNK
        return st

    XMOV = {"movups": 16, "movaps": 16, "movdqu": 16, "movdqa": 16, "lddqu": 16, "movsd": 8, "movq": 8}

    def step(self, f, st, i, depth, stack, caller_writes):
        """SIMD moves carry two 8-byte halves (xmmN.lo / xmmN.hi): a packet copied with movups (00582540 copies the
        kind-9 storage packet into its queue that way) keeps the pointers it holds; any other xmm write drops them."""
        ops = i.operands
        # pointer + index from a known state offset keeps that offset as a lower bound: A@K (index assumed >= 0)
        if i.mnemonic in ("add", "lea") and len(ops) == 2 and ops[0].type == X.X86_OP_REG:
            dn, dw = K.fullname(ops[0].reg)
            k = None
            if dw == 8 and i.mnemonic == "lea" and ops[1].type == X.X86_OP_MEM and ops[1].mem.index != 0                     and ops[1].mem.base not in (0, X.X86_REG_RIP):
                bv = st.r.get(K.fullname(ops[1].mem.base)[0], K.UNK)
                iv = st.r.get(K.fullname(ops[1].mem.index)[0], K.UNK)
                k = self.known_a(bv) if self.known_a(iv) is None else (self.known_a(iv) if ops[1].mem.scale == 1 and self.known_a(bv) is None else None)
                if k is not None:
                    k += ops[1].mem.disp
            elif dw == 8 and i.mnemonic == "add" and ops[1].type == X.X86_OP_REG:
                a1, a2 = self.known_a(st.r.get(dn, K.UNK)), self.known_a(st.r.get(K.fullname(ops[1].reg)[0], K.UNK))
                k = a1 if a2 is None else (a2 if a1 is None else None)
            if k is not None:
                st.r[dn] = K.vs(("A@%X" % k, 0))
                return R.branch_targets(i), st, False
        n = self.XMOV.get(i.mnemonic)
        if n and len(ops) == 2:
            r0 = K.md.reg_name(ops[0].reg) if ops[0].type == X.X86_OP_REG else None
            r1 = K.md.reg_name(ops[1].reg) if ops[1].type == X.X86_OP_REG else None
            x0 = r0 if r0 and r0.startswith("xmm") else None
            x1 = r1 if r1 and r1.startswith("xmm") else None
            if x0 and ops[1].type == X.X86_OP_MEM:
                a = K.memaddr(st, ops[1].mem, i)
                st.r[x0 + ".lo"] = K.load_value(st, a)
                st.r[x0 + ".hi"] = K.load_value(st, K.add(a, 8)) if n == 16 and a is not K.UNK else K.UNK
                return R.branch_targets(i), st, False
            if x1 and ops[0].type == X.X86_OP_MEM:
                a = K.memaddr(st, ops[0].mem, i)
                self.store(f, i, st, a, 8, st.r.get(x1 + ".lo", K.UNK))
                if n == 16:
                    self.store(f, i, st, K.add(a, 8) if a is not K.UNK else K.UNK, 8, st.r.get(x1 + ".hi", K.UNK))
                return R.branch_targets(i), st, False
            if x0 and x1:
                st.r[x0 + ".lo"] = st.r.get(x1 + ".lo", K.UNK)
                st.r[x0 + ".hi"] = st.r.get(x1 + ".hi", K.UNK) if n == 16 else K.UNK
                return R.branch_targets(i), st, False
        res = super().step(f, st, i, depth, stack, caller_writes)
        try:
            _, wr = i.regs_access()
        except capstone.CsError:
            wr = []
        for x in wr:
            nm = K.md.reg_name(x)
            if nm and nm.startswith(("xmm", "ymm")):
                x = "xmm" + nm[3:]
                res[1].r.pop(x + ".lo", None)
                res[1].r.pop(x + ".hi", None)
        return res

    @staticmethod
    def known_a(v):
        """The single known state offset v denotes (A, K) or A@K's lower bound, else None."""
        if v is K.UNK or len(v) != 1:
            return None
        (b, o), = v
        if b == "A" and o is not None:
            return o
        if isinstance(b, str) and b.startswith("A@") and o is not None:
            return int(b[2:], 16) + o
        return None

    def classify(self, b, o, size, st, i):
        if b == "AR":
            return "REGISTRY-STORAGE", None
        if b == "REC":
            if o is None:
                return "RECORD-INDEXED", None
            return ("RECORD" if 0 <= o and o + size <= REC_SIZE else "RECORD-OUTSIDE"), o
        if b == "A":
            if o is not None:
                return ("REGION" if (o < HI and o + size > LO) else "STATE-OTHER"), o
            base = self.pre_index(st, i)
            return ("INDEXED-UNKNOWN" if base is None else "INDEXED-BELOW" if base < HI else "INDEXED-ABOVE"), base
        k = int(b[2:], 16)
        lo = k + (o or 0)
        if o is None:
            return ("INDEXED-BELOW" if k < HI else "INDEXED-ABOVE"), k
        return ("INDEXED-BELOW" if lo < HI else "INDEXED-ABOVE"), lo

    def store(self, f, i, st, addr, size, val):
        text = "%s %s" % (i.mnemonic, i.op_str)
        op = i.operands[0] if i.operands and i.operands[0].type == X.X86_OP_MEM else None
        if op is not None and op.mem.index != 0 and op.mem.scale == 1:
            # `[counter + pointer + d]`: the pointer rides in the index register (003047F0's zeroing loop)
            iv = st.r.get(K.fullname(op.mem.index)[0], K.UNK)
            if iv is not K.UNK:
                for b, o in iv:
                    if not is_state(b):
                        continue
                    # the address is counter (>= 0) + this pointer + disp; the pointer's own lower bound + disp
                    if b == "AR":
                        cls, lo = "REGISTRY-STORAGE", None
                    elif b == "REC":
                        cls, lo = "RECORD-INDEXED", None if o is None else o + op.mem.disp
                    else:
                        pk = Census.known_a(K.vs((b, o)))
                        if pk is None and b.startswith("A@"):
                            pk = int(b[2:], 16)
                        lo = None if pk is None else pk + op.mem.disp
                        cls = "INDEXED-UNKNOWN" if lo is None else "INDEXED-BELOW" if lo < HI else "INDEXED-ABOVE"
                    self.hits.append((cls, f, i.address, text, size, "index " + K.desc(iv) + ("" if lo is None else " lo=%#x" % lo)))
        if addr is not K.UNK:
            for b, o in addr:
                if b == "CAP" and o is not None and o + IMG_TO_STATE < HI and o + IMG_TO_STATE + size > LO:
                    self.cap.append((f, i.address, text, size))
                if not is_state(b):
                    continue
                cls, lo = self.classify(b, o, size, st, i)
                self.hits.append((cls, f, i.address, text, size, K.desc(addr) + ("" if lo is None else " lo=%#x" % lo)))
        if (val is not K.UNK and addr is not K.UNK and len(addr) == 1 and size == 8
                and any(is_state(vb) for vb, _ in val)):
            (b, o), = addr
            if isinstance(b, str) and b.startswith("G") and int(b[1:], 16) != 0x00120000:
                ga = int(b[1:], 16) + (o or 0)
                if o is None:
                    self.esc_tables.add(ga)
                for vb, vo in val:
                    if is_state(vb):
                        self.esc_vals[ga].add((vb, vo))
        super().store(f, i, st, addr, size, val)

    @staticmethod
    def pre_index(st, i):
        """The state offset of a memory operand's base register plus displacement, before the index is added."""
        op = i.operands[0] if i.operands and i.operands[0].type == X.X86_OP_MEM else None
        if op is None or op.mem.base == 0 or op.mem.base == X.X86_REG_RIP:
            return None
        bn, _ = K.fullname(op.mem.base)
        bv = st.r.get(bn, K.UNK)
        if bv is K.UNK:
            return None
        offs = [Census.known_a(K.vs((b, o))) for b, o in bv if is_state(b)]
        if not offs or any(o is None for o in offs):
            return None
        return min(offs) + op.mem.disp


def is_state(b):
    """A state-derived base: A (state + a known offset or unknown), A@K (state + K + a non-negative index, then the
    token's own offset), AR (a class-storage pointer read from an unknown registry row)."""
    return isinstance(b, str) and (b == "A" or b == "AR" or b == "REC" or b.startswith("A@"))


K.has_actor = lambda v: v is not K.UNK and any(is_state(b) for b, _ in v)


def scan():
    """Linear decode of every catalogued function: rip-relative references and direct calls."""
    refs = collections.defaultdict(set)     # absolute global -> {(fn, addr, is_load)}
    calls = collections.defaultdict(set)    # callee -> {caller fn}
    import uc1_band
    sizes, _ = uc1_band.apply_extents(dict(R.ext))        # executable definition v3: chained tails included
    for st_, sz in uc1_band.load()["frontier"].items():  # and the UC-1 frontier bodies
        sizes.setdefault(st_, sz)
    for f, n in sizes.items():
        d = R.at(f, n) if hasattr(R, "at") else None
        if not d:
            continue
        for i in R.md.disasm(d, f):
            if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM:
                calls[i.operands[0].imm].add(f)
            for op in i.operands:
                if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                    g = i.address + i.size + op.mem.disp
                    refs[g].add((f, i.address, i.mnemonic == "mov" and i.operands[0].type == X.X86_OP_REG and op is i.operands[1]))
    return refs, calls


def main():
    t0 = time.time()
    refs, calls = scan()
    loads = [x for x in refs.get(STATE_G, ()) if x[2]]
    allrefs = refs.get(STATE_G, ())
    print("%s  C5: rip-relative references to qword [02EBF190]: %d (T3's census: 318), of them `mov reg, [..]` loads %d; "
          "every referencing function is a root" % ("PASS" if len(allrefs) == 318 else "FAIL", len(allrefs), len(loads)))
    for attempt in range(1, 4):
        before = dict(globals_root)     # a global first learnt mid-pass was loaded as non-state by earlier bodies
        before_t = set(TABLES)
        an, done = fixpoint(refs, calls, t0)
        # the offsets each escape global carries; rerun from scratch until they stop moving (memoised summaries from a
        # pass that loaded a global at the wrong offset cannot be patched in place)
        seen = {}
        for fn, a, text, where in set(an.escapes):
            w = where.strip("{}").split(",")[0].strip()
            if w.startswith("G") and "?" not in w:
                g, _, off = w[1:].partition("+")
                ga = int(g, 16) + (int(off, 0) if off else 0)
                if ga != STATE_G:
                    seen[ga] = frozenset(an.esc_vals.get(ga) or {("A", None)})
        moved = {g: v for g, v in seen.items() if before.get(g) != v}
        tables = set(an.esc_tables) & set(seen)
        print("pass %d: escape globals %s%s" % (attempt, ", ".join("%08X%s:%s" % (g, "[table]" if g in tables else "", "/".join(
            sorted(K.desc(K.vs(t)) for t in v))) for g, v in sorted(seen.items())),
            "" if (not moved and tables == before_t) else " (moved: rerun)"))
        if not moved and tables == before_t:
            break
        globals_root.update(moved)
        TABLES.clear()
        TABLES.update(tables)
    c7 = globals_root.get(0x020927C0) == frozenset([("A", 0x8200 + IMG_TO_STATE)])
    return report(an, done, c7, t0)


def fixpoint(refs, calls, t0):
    an = Census()
    done, rounds = set(), 0
    while True:
        rounds += 1
        roots = set(f for g in list(globals_root) + list(REG_CELLS) for f, _, _ in refs.get(g, ()))
        roots |= set(f for g, xs in refs.items() for t in TABLES if t <= g < t + TABLE_SPAN for f, _, _ in xs)
        roots |= set(f for g, xs in refs.items() if REG_ROWS[0] <= g < REG_ROWS[1] for f, _, _ in xs)
        roots |= set(f for g, xs in refs.items() if IMG_LO <= g < IMG_HI for f, _, _ in xs)   # the static image itself
        roots |= calls.get(IMG_GETTER, set()) | calls.get(CAP_GETTER, set())
        roots |= set(c for f in an.state_returners for c in calls.get(f, ()))
        new = sorted(roots - done)
        if not new:
            break
        for f in new:
            try:
                an.summary(f, (), 0, ())
            except Exception as e:  # noqa: BLE001
                print("  error in %08X: %s %r (its stores are a blind spot)" % (f, type(e).__name__, e))
        done |= set(new)
        added = 0
        for fn, a, text, where in set(an.escapes):
            if where.startswith("G") and "+" in where:
                pass
        # escapes into globals become roots
        for fn, a, text, where in set(an.escapes):
            w = where.strip("{}").split(",")[0].strip()
            if w.startswith("G") and "?" not in w:
                g, _, off = w[1:].partition("+")
                ga = int(g, 16) + (int(off, 0) if off else 0)
                if ga not in globals_root:
                    globals_root[ga] = frozenset(an.esc_vals.get(ga) or {("A", None)})
                    if ga in an.esc_tables:
                        TABLES.add(ga)
                    added += 1
        print("round %d: %d new root functions, %d new escape globals (%.0f s)" % (rounds, len(new), added, time.time() - t0))
    return an, done


def report(an, done, c7, t0):
    hits = sorted(set(an.hits))
    by = collections.Counter(h[0] for h in hits)
    print("root functions analysed: %d; bodies reached %d (contexts %d); stores on state-derived bases: %s" % (
        len(done), len(an.fns), len(an.memo), dict(sorted(by.items()))))
    region_fns = set(h[1] for h in hits if h[0] in ("REGION", "INDEXED-BELOW", "INDEXED-UNKNOWN", "REGISTRY-STORAGE",
                                                        "RECORD-INDEXED", "RECORD-OUTSIDE"))
    c8 = any(h[2] == 0x00305927 and h[0] == "RECORD" for h in hits)
    c1 = any(h[2] in CTRL["C1"] and h[0] == "REGION" for h in hits)
    c2 = 0x002FD150 in region_fns
    c3 = 0x003047F0 in region_fns
    c4 = any(e[1] in CTRL["C4"] for e in an.escapes)
    c6 = any(h[1] == 0x002EF4A0 for h in hits)
    for n, ok in (("C1 the state memset 002370D3 is REGION", c1), ("C2 the packed handler 002FD150 writes region A", c2),
                  ("C3 the zeroing loop's function 003047F0 writes region A", c3),
                  ("C4 the enqueue's movups copy 005825A0 of the kind-9 packet (image at +0x48) is an escape", c4),
                  ("C6 the mirror copy 002EF4A0 (lea 021B290C / lea 02166480) is a state writer", c6),
                  ("C7 the escape global 020927C0 carries image+0x8200 (state-0x4648C) from 00253970", c7),
                  ("C8 00305927 `mov [rax+0x18c]` through a 022C1740 entry (a 00320AB0 record) is RECORD", c8)):
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("functions that may write region A (REGION, INDEXED-*, REGISTRY-STORAGE, RECORD-INDEXED/OUTSIDE): %d" % len(region_fns))
    for f in sorted(region_fns):
        hs = [h for h in hits if h[1] == f and h[0] not in ("STATE-OTHER", "INDEXED-ABOVE", "RECORD")]
        print("  %08X  %d stores: %s" % (f, len(hs), "; ".join("%s %08X %s" % (h[0][:6], h[2], h[3]) for h in hs[:4])))
    esc = sorted(set(an.escapes))
    print("escapes (state-derived pointer stored to non-stack memory): %d" % len(esc))
    for e in esc:
        print("  ESCAPE   %08X %08X %-46s to %s" % e)
    ind = sorted(set(an.indirect))
    print("indirect calls receiving a state-derived pointer: %d" % len(ind))
    for e in ind:
        print("  INDIRECT %08X %08X %-46s args %s" % e)
    cuts = [c for c in an.recursive if c[2]]
    print("depth/recursion cuts carrying a state-derived value: %d" % len(cuts))
    for c in sorted(set(cuts)):
        print("  CUT      %08X depth %d" % c[:2])
    print("capture-image stores at region A's offsets: %d" % len(set(an.cap)))
    with io.open(os.path.join(HERE, "ov58d_flow.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("class\tfunction\taddress\tinstruction\tsize\tbase\n")
        for h in hits:
            o.write("%s\t%08X\t%08X\t%s\t%d\t%s\n" % h)
    print("elapsed %.0f s" % (time.time() - t0))
    return 0 if (c1 and c2 and c3 and c4 and c6 and c7 and c8) else 1


if __name__ == "__main__":
    sys.exit(main())
