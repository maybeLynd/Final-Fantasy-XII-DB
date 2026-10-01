"""structflow.py - forward may-taint of a structure-array pointer over each function's control-flow graph, with row offsets
kept (kit tool; generalised by OPUS 2026-09-30 from SWE2-STRUCT's rowflow.py, _index/candidates/gr4-gr5-action-row-readers-0930,
written for GR-4 / GR-5). Static, the certified image, via retool.py.

  Flow(fields, depth, stride=60, slot=0x02EBF138, seed_loads=None, seed_leas=None, seed_calls=None)

Tags a register or stack slot can carry:
  H      the registry slot's header pointer, loaded from `slot` (`mov r64, qword ptr [rip -> slot]`);
  F      the header's +0x0C reference (`mov r32, dword ptr [H + 0xC]`);
  B      the array base: the return of 0020E600 (ImageAddress_ResolveRuntimePointer) called with an F in rcx, or - with
         seed_loads = {(func, disp)} - the result of a qword load `mov r64, qword ptr [X + disp]` inside func, or -
         with seed_leas = {(func, address)} - the result of `lea r64, [rip -> address]` inside func (a static array);
         seed_leas may instead be a dict {(func, address): k} when the lea takes field k of element 0 (e.g. base + 0x14):
         the register then carries ("B", k), a base whose accesses and derived element pointers are shifted by k
         (added by SWE2-STRUCT for GR-8, 2026-09-30; with seed_leas omitted every result is unchanged); or - with
         seed_calls = {(func, callee)} - rax after a direct `call callee` inside func (an allocator's return; added by
         SWE2-STRUCT for GR-13, 2026-09-30; with seed_calls omitted every result is unchanged); seed_loads may also
         hold (func, disp, address) triples, which seed only the load at that address, and such a triple also seeds
         `add r64, qword ptr [X + disp]` at that address as an element pointer at offset 0 (the `index << 5` + list
         form; GR-13, 2026-09-30 - with only (func, disp) pairs, as every earlier caller passes, nothing changes);
  (E,k)  an element pointer at offset k (modulo `stride`), formed by adding any register to a B
         (`add r, B` / `lea r, [B + x]`) and moved by `lea r, [E + d]` / `add r, imm`;
  (E,None) an element pointer plus an unknown register.
Propagation: a worklist over basic blocks, union at joins, strong update on every register write (anything not modelled
kills the register), so a kill on one path never hides a read on another. Direct jump targets and MSVC jump tables are
edges; the blocks of a body with an undecoded indirect jump are entered with the union of the states at those jumps.
Stack slots [rsp + d] / [rbp + d] carry tags; a store of a tagged register (dword or wider) anywhere else is an ESCAPE.
A direct call or tail jump hands its tagged rcx / rdx / r8 / r9 and its tagged outgoing stack slots [rsp + 0x20..0x7F]
to the callee, to `depth` calls; the callee is re-walked when the union of its entry tags grows. A function whose `ret`
holds a tagged rax is element-returning: its callers' rax carries the tags after the call, and every direct caller is
walked. memcpy / memcpy_s with a tagged rdx, `rep movs` from a tagged rsi, and 16-byte accesses through a tag are COPIES.
Every access through a tagged base is classified: a known element offset (reported when its width covers one of
`fields`), or an unknown one (always reported).
It does NOT see: indirect calls' targets (recorded when an argument is tagged), taint through non-stack memory (escapes
are recorded instead), rbp-based outgoing stack arguments, or code outside retool's function extents.
"""
import os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import retool as T  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
RESOLVE = 0x0020E600
COPY = {0x00861EBA: "memcpy", 0x00861FC8: "memcpy_s"}
FAM = {}
for fam in (("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"), ("rcx", "ecx", "cx", "cl", "ch"),
            ("rdx", "edx", "dx", "dl", "dh"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
            ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")):
    for r in fam:
        FAM[r] = fam[0]
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAM["r%d%s" % (n, suf)] = "r%d" % n
ARGS = ("rcx", "rdx", "r8", "r9")
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
ROWTAGS = lambda t: {x for x in t if x not in ("H", "F")}
_cfg = {}


def rn(i, r):
    n = i.reg_name(r) if r else None
    return FAM.get(n, n) if n else None


def cfg(f):
    if f in _cfg:
        return _cfg[f]
    try:
        ins = list(R.md.disasm(R.at(f, SZ[f]), f))
    except Exception:
        ins = []
    end = f + SZ.get(f, 0)
    leaders = {ins[0].address} if ins else set()
    for k, x in enumerate(ins):
        if x.mnemonic.startswith("j") or x.mnemonic in ("ret", "int3"):
            if k + 1 < len(ins):
                leaders.add(ins[k + 1].address)
            if x.operands and x.operands[0].type == 2 and f <= x.operands[0].imm < end:
                leaders.add(x.operands[0].imm)
    blocks, cur = collections.OrderedDict(), None
    for x in ins:
        if x.address in leaders:
            cur = x.address
            blocks[cur] = []
        blocks[cur].append(x)
    succ, indirect = {}, False
    # MSVC jump tables: `lea rB, [rip -> 00120000]` ... `mov eax, dword ptr [rB + rI*4 + D]` ... `add rax, rB; jmp rax`
    tables = {}
    for k, x in enumerate(ins):
        if x.mnemonic == "jmp" and x.operands and x.operands[0].type == 1:
            bound = None
            for y in ins[max(0, k - 12):k]:
                if y.mnemonic == "cmp" and len(y.operands) == 2 and y.operands[1].type == 2:
                    bound = y.operands[1].imm
                for op in y.operands:
                    if op.type == 3 and op.mem.scale == 4 and op.mem.index and op.mem.base and y.mnemonic == "mov":
                        tables[x.address] = (0x120000 + op.mem.disp, bound)
    extra = {}
    for ja, (ta, bound) in tables.items():
        tg = []
        for n in range((bound + 1) if bound is not None and bound < 512 else 512):
            raw = R.at(ta + 4 * n, 4)
            if not raw or len(raw) < 4:
                break
            v = 0x120000 + int.from_bytes(raw, "little")
            if not (f <= v < end):
                break
            tg.append(v)
        extra[ja] = tg
        for v in tg:
            if v not in leaders:
                leaders.add(v)
    if extra:
        blocks, cur = collections.OrderedDict(), None
        for x in ins:
            if x.address in leaders:
                cur = x.address
                blocks[cur] = []
            blocks[cur].append(x)
    addrs = set(blocks)
    keys = list(blocks)
    for n, b in enumerate(keys):
        last = blocks[b][-1]
        s = []
        m = last.mnemonic
        nxt = keys[n + 1] if n + 1 < len(keys) else None
        if m.startswith("j"):
            if last.operands and last.operands[0].type == 2:
                if last.operands[0].imm in addrs:
                    s.append(last.operands[0].imm)
            elif m == "jmp":
                if extra.get(last.address):
                    s.extend(v for v in extra[last.address] if v in addrs)
                else:
                    indirect = True
            if m != "jmp" and nxt:
                s.append(nxt)
        elif m not in ("ret", "int3") and nxt:
            s.append(nxt)
        succ[b] = s
    _cfg[f] = (blocks, succ, indirect, end)
    return _cfg[f]


_frame = {}


def frame(f):
    """bytes the callee's prologue moves rsp by (pushes + sub rsp, imm) - its [rsp + d] then sees the caller's
    [rsp + d - 8 - frame]"""
    if f not in _frame:
        n = 0
        try:
            for x in R.md.disasm(R.at(f, min(SZ.get(f, 64), 64)), f):
                if x.mnemonic == "push":
                    n += 8
                elif x.mnemonic == "sub" and x.op_str.startswith("rsp, "):
                    n += int(x.op_str.split(", ")[1], 0)
                    break
                elif x.mnemonic in ("call", "ret", "jmp") or x.mnemonic.startswith("j"):
                    break
        except Exception:
            pass
        _frame[f] = n
    return _frame[f]


def covers(off, w, fld, stride=60):
    return any((off + j) % stride == fld for j in range(w))


def bk(t):
    """the field offset a base tag stands for: 0 for "B", k for ("B", k), None for any other tag"""
    if t == "B":
        return 0
    if isinstance(t, tuple) and t[0] == "B":
        return t[1]
    return None


def st_key(st):
    return frozenset((k, frozenset(v)) for k, v in st.items() if v)


def join(a, b):
    out = {k: set(v) for k, v in a.items()}
    for k, v in b.items():
        out.setdefault(k, set()).update(v)
    return out


class Flow:
    def __init__(self, fields, depth, follow_returns=True, stride=60, slot=0x02EBF138, seed_loads=None, seed_leas=None,
                 seed_calls=None):
        self.fields, self.depth, self.follow_returns = fields, depth, follow_returns
        self.stride, self.slot, self.seed_loads = stride, slot, set(seed_loads or ())
        self.seed_leas = dict(seed_leas) if isinstance(seed_leas, dict) else {k: 0 for k in (seed_leas or ())}
        self.seed_calls = set(seed_calls or ())
        self.seeded = set()     # (f, addr, reg): a base seeded from a rip-relative lea
        self.hits, self.unk, self.esc, self.copies, self.indirect, self.stackargs = set(), set(), set(), set(), set(), set()
        self.hdr, self.retsum, self.rets = set(), {}, set()
        self.probe = collections.defaultdict(lambda: collections.defaultdict(set))   # addr -> reg -> tags before it
        self.forms = set()      # (f, addr, reg): a row pointer formed from the base (add / lea with the base)
        self.entry, self.q = {}, []
        self.callers_of = collections.defaultdict(set)
        self.handoffs = set()   # (caller, site, callee, argtags)

    def enqueue(self, f, ent, depth):
        old = self.entry.get(f)
        if old is not None:
            od, oe = old
            if all(set(v) <= oe.get(k, set()) for k, v in ent.items()) and od >= depth:
                return
            ent, depth = join(oe, ent), max(od, depth)
        self.entry[f] = (depth, {k: set(v) for k, v in ent.items()})
        self.q.append(f)

    def run(self, roots):
        for f in roots:
            self.enqueue(f, {}, self.depth)
        while self.q:
            f = self.q.pop()
            depth, ent = self.entry[f]
            self.walk(f, ent, depth)

    def walk(self, f, ent, depth):
        blocks, succ, indirect, end = cfg(f)
        if not blocks:
            return
        first = next(iter(blocks))
        IN = {first: {k: set(v) for k, v in ent.items()}}
        wl = [first]
        outs_at_ijmp = {}
        seen_keys = {}
        while True:
            while wl:
                b = wl.pop()
                st = {k: set(v) for k, v in IN[b].items()}
                for x in blocks[b]:
                    for r, v in st.items():
                        if v and not isinstance(r, tuple):
                            self.probe[x.address][r] |= v
                    self.step(f, x, st, depth)
                if blocks[b][-1].mnemonic == "jmp" and not succ[b] and blocks[b][-1].operands[0].type != 2:
                    outs_at_ijmp[b] = st
                for s in succ[b]:
                    new = join(IN.get(s, {}), st)
                    if s not in IN or st_key(new) != st_key(IN[s]):
                        IN[s] = new
                        wl.append(s)
            # blocks never reached: with an indirect jump in the body they may be switch targets - enter them with the
            # union of the states at the indirect jumps (and the entry)
            if not indirect:
                break
            u = {}
            for s in outs_at_ijmp.values():
                u = join(u, s)
            grew = False
            for b in blocks:
                if b == first or b in IN:
                    continue
                new = join(IN.get(b, {}), u)
                if b not in IN or st_key(new) != st_key(IN[b]):
                    IN[b] = new
                    wl.append(b)
                    grew = True
            if not grew:
                break

    def ts(self, st, r):
        return st.get(r, set()) if r else set()

    def step(self, f, x, st, depth):
        m, ops = x.mnemonic, x.operands
        text = "%s %s" % (m, x.op_str)
        # accesses
        for n, op in enumerate(ops):
            if op.type != 3 or m in ("lea", "nop") or m.startswith("prefetch"):
                continue
            b, ix = rn(x, op.mem.base), rn(x, op.mem.index)
            if b == "rip":
                continue
            kind = "w" if (n == 0 and len(ops) > 1 and m not in ("cmp", "test", "bt", "push")) else "r"
            w = op.size
            tags = set(self.ts(st, b))
            if op.mem.scale == 1:
                tags |= {t for t in self.ts(st, ix) if bk(t) is not None}
                if {t for t in ROWTAGS(self.ts(st, ix)) if bk(t) is None}:
                    tags.add(("E", None))
            for t in tags:
                if t == "H":
                    self.hdr.add((f, x.address, op.mem.disp, text))
                    continue
                if t == "F":
                    continue
                if bk(t) is not None:
                    off, form = (bk(t) + op.mem.disp) % self.stride, "B+i" if ix else "B"
                elif t[1] is None or (ix and self.ts(st, b) and t in self.ts(st, b)):
                    off, form = None, "E?"
                else:
                    off, form = (t[1] + op.mem.disp) % self.stride, "E%d" % t[1]
                if w >= 16:
                    self.copies.add((f, x.address, text))
                if off is None:
                    self.unk.add((f, x.address, kind, form, w, text))
                elif any(covers(off, w, fl, self.stride) for fl in self.fields):
                    self.hits.add((f, x.address, kind, form, off, w, text))
        if (m.startswith("rep movs") or m in ("movsb", "movsw", "movsq") or (m == "movsd" and "[rsi]" in x.op_str))                 and ROWTAGS(self.ts(st, "rsi")):
            self.copies.add((f, x.address, text))
        if m == "ret":
            t = ROWTAGS(self.ts(st, "rax")) | ({"F"} & self.ts(st, "rax"))
            if t:
                self.rets.add((f, x.address, frozenset(map(str, t))))
                old = self.retsum.get(f, set())
                if not t <= old:
                    self.retsum[f] = old | t
                    for c in self.callers_of[f]:
                        if c in self.entry:
                            self.q.append(c)
                    for c, _site in SC["calls"].get(f, ()):
                        if c in SZ:
                            self.enqueue(c, {}, self.depth)
            return
        if m in ("call", "jmp") and ops and ops[0].type == 2:
            tgt = ops[0].imm
            if m == "jmp" and f <= tgt < f + SZ[f]:
                return
            if m == "jmp" and tgt not in SZ:
                return
            a = {r: set(st[r]) for r in ARGS if st.get(r)}
            stk = {k: v for k, v in list(st.items()) if isinstance(k, tuple) and k[0] == "rsp" and 0x20 <= k[1] < 0x80 and ROWTAGS(v)}
            if stk and tgt in SZ and tgt not in (RESOLVE,) and tgt not in COPY:
                self.stackargs.add((f, x.address, tgt, repr(sorted((k[1], sorted(map(str, v))) for k, v in stk.items()))))
                fr = frame(tgt)
                for k, v in stk.items():
                    a[("rsp", k[1] + 8 + fr)] = set(v)
            self.callers_of[tgt].add(f)
            if tgt == RESOLVE:
                res = {"B"} if "F" in self.ts(st, "rcx") else set()
            elif tgt in COPY:
                if ROWTAGS(a.get("rdx", set())):
                    self.copies.add((f, x.address, "call %s rdx=%s" % (COPY[tgt], sorted(map(str, a["rdx"])))))
                res = set()
            else:
                if a and depth > 0 and tgt in SZ:
                    self.handoffs.add((f, x.address, tgt, repr(sorted((str(r), sorted(map(str, v))) for r, v in a.items()))))
                    self.enqueue(tgt, a, depth - 1)
                res = set(self.retsum.get(tgt, set())) if self.follow_returns else set()
            if (f, tgt) in self.seed_calls:
                res = set(res) | {"B"}
                self.seeded.add((f, x.address, "rax"))
            for r in VOL:
                st.pop(r, None)
            if res:
                st["rax"] = res
            return
        if m == "call":
            a = {r: sorted(map(str, st[r])) for r in ARGS if st.get(r) and ROWTAGS(st[r]) | ({"F", "H"} & st[r])}
            if a:
                self.indirect.add((f, x.address, text, repr(a)))
            for r in VOL:
                st.pop(r, None)
            return
        if m.startswith("j"):
            return
        # stores of a tagged register
        if len(ops) == 2 and ops[0].type == 3 and ops[1].type == 1 and m in ("mov", "xchg", "movd", "movq"):
            d, s = ops
            t = self.ts(st, rn(x, s.reg))
            db = rn(x, d.mem.base)
            slot = (db, d.mem.disp) if db in ("rsp", "rbp") and not d.mem.index else None
            if slot:
                if t and d.size >= 4:
                    st[slot] = set(t)
                else:
                    st.pop(slot, None)
            elif t and d.size >= 4:
                self.esc.add((f, x.address, frozenset(map(str, t)), text))
            return
        if len(ops) == 2 and ops[0].type == 3:
            d = ops[0]
            db = rn(x, d.mem.base)
            if db in ("rsp", "rbp") and not d.mem.index and m not in ("cmp", "test"):
                st.pop((db, d.mem.disp), None)
            return
        # register writes
        try:
            written = {FAM.get(x.reg_name(r), x.reg_name(r)) for r in x.regs_access()[1]}
        except Exception:
            written = set()
        written.discard("rflags")
        new = None
        if len(ops) == 2 and ops[0].type == 1:
            d, s = ops
            dr = rn(x, d.reg)
            if m in ("mov", "movsxd") or m.startswith("cmov") or (m in ("movzx", "movsx") and s.type == 1 and s.size >= 4):
                if s.type == 1:
                    new = set(self.ts(st, rn(x, s.reg))) if d.size >= 4 and s.size >= 4 else set()
                elif s.type == 3:
                    sb = rn(x, s.mem.base)
                    if sb == "rip" and x.address + x.size + s.mem.disp == self.slot and d.size == 8:
                        new = {"H"}
                    elif sb in ("rsp", "rbp") and not s.mem.index:
                        new = set(st.get((sb, s.mem.disp), set()))
                    elif "H" in self.ts(st, sb) and s.mem.disp == 0xC and not s.mem.index:
                        new = {"F"}
                    elif ((f, s.mem.disp) in self.seed_loads or (f, s.mem.disp, x.address) in self.seed_loads)                             and m == "mov" and d.size == 8 and not s.mem.index:
                        new = {"B"}
                    else:
                        new = set()
                else:
                    new = set()
                if m.startswith("cmov"):
                    new |= self.ts(st, dr)
            elif m in ("movzx", "movsx") and s.type == 3:
                sb = rn(x, s.mem.base)
                new = set()
            elif m == "lea" and s.type == 3:
                sb, si, disp = rn(x, s.mem.base), rn(x, s.mem.index), s.mem.disp
                new = set()
                if sb == "rip" and (f, x.address + x.size + disp) in self.seed_leas and d.size == 8:
                    k = self.seed_leas[(f, x.address + x.size + disp)]
                    new.add("B" if k == 0 else ("B", k))
                    self.seeded.add((f, x.address, dr))
                for t in self.ts(st, sb):
                    if bk(t) is not None:
                        new.add(("E", (bk(t) + disp) % self.stride))
                        self.forms.add((f, x.address, dr))
                    elif t in ("H", "F"):
                        continue
                    elif t[1] is None or si:
                        new.add(("E", None))
                    else:
                        new.add(("E", (t[1] + disp) % self.stride))
                for t in self.ts(st, si):
                    if bk(t) is not None and s.mem.scale == 1:
                        new.add(("E", (bk(t) + disp) % self.stride))
                        self.forms.add((f, x.address, dr))
                    elif t not in ("H", "F") and bk(t) is None:
                        new.add(("E", None))
            elif m in ("add", "sub") and s.type == 2:
                k = s.imm if m == "add" else -s.imm
                new = set()
                for t in self.ts(st, dr):
                    if bk(t) is not None:
                        new.add(("E", (bk(t) + k) % self.stride))
                    elif t not in ("H", "F"):
                        new.add(("E", None) if t[1] is None else ("E", (t[1] + k) % self.stride))
            elif m == "add" and s.type == 1:
                new = set()
                for t in self.ts(st, dr) | self.ts(st, rn(x, s.reg)):
                    if bk(t) is not None:
                        new.add(("E", bk(t)))
                        self.forms.add((f, x.address, dr))
                    elif t not in ("H", "F"):
                        new.add(("E", None))
            elif m == "add" and s.type == 3 and d.size == 8 and not s.mem.index                     and (f, s.mem.disp, x.address) in self.seed_loads:
                new = {("E", 0)}
                self.forms.add((f, x.address, dr))
            elif m == "xchg" and s.type == 1:
                sr = rn(x, s.reg)
                a, b = set(self.ts(st, dr)), set(self.ts(st, sr))
                st[dr], st[sr] = b, a
                return
            if new is not None and dr:
                for r in written - {dr}:
                    st.pop(r, None)
                if new:
                    st[dr] = new
                else:
                    st.pop(dr, None)
                return
        for r in written:
            if r in ("rsp",):
                continue
            st.pop(r, None)


def slot_functions(slot=0x02EBF138):
    return sorted({fn for fn, a, k in SC["refs"].get(slot, ())})
