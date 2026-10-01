"""rc15_flow.py - RC-15: every native read or write of the script VM register file (ActorStorageRecord +0x64..+0x83),
found by following the record pointer itself, not by the functions a hop count reaches. ORACLE, 2026-09-30. Static.

Engine: k14_actorflow.Analysis (../k14-closure-stores-0930), token "A" = an ActorStorageRecord. What yields A:
- the manager array 02098E10 (5 slots, stride 0x288): a load from a slot's +0x08 is the pool ("POOL"), and a load
  from POOL + 8 + k*8 (any k) is a record (ActorManager_GetRecordByOrdinal 00358940 is exactly that). Offsets into
  the array are kept modulo 0x288, because code adds idx*0x288 to the array address;
- a verb callback's first two arguments (rcx = issuer, rdx = owner; verb-dispatch ABI section 2.5), for every
  handler address in scriptvm-verb-table.tsv (begin, poll, result, arg_handler);
- any function whose return value is A (found to a fixpoint), which makes its callers roots;
- any global the flow sees A stored into (an escape); a load from that global then yields A. Iterated.
Roots: every function that references the manager array (rip-relative, or a disp32 off the image base), the verb
handlers, and the callers of every A-returning function. A is followed through registers, stack, offsets,
direct callees with context, tail jumps and switch tables.

Reported: every memory READ and every WRITE whose bytes can overlap A + 0x64..0x83 (known offset in range, or unknown
offset "A+?"), bulk calls (memcpy / memcpy_s / memset / memcmp / 004746F0) with A in rcx or rdx, rep string ops
on A, escapes of A into non-global memory (object fields: listed for typing), and indirect calls receiving A.
Controls: (C1) the interpreter's eight register loads 002616AF..0026172C and (C2) its eight register stores
00261624..002616A1 must be found through the flow (roots -> 0025D9E0 -> 0025DF00 -> 0025E4C0), not seeded.
Output: rc15_flow.out (stdout), rc15_flow.tsv (every range access).
"""
import collections, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402
import capstone  # noqa: E402
from capstone import x86 as X  # noqa: E402

R = K.R
K.MAXDEPTH = 14
MGR_LO, MGR_N, MGR_STRIDE = 0x02098E10, 5, 0x288
MGR_HI = MGR_LO + MGR_N * MGR_STRIDE
LO, HI = 0x64, 0x84
BULK = {0x00861EBA: "memcpy", 0x00861FC8: "memcpy_s", 0x00861EC0: "memset", 0x00861ED2: "memcmp",
        0x004746F0: "memcpy-adapter"}
K.MEMFN = {}  # bulk calls are handled here, by both pointers
C1 = {0x002616AF, 0x002616C0, 0x002616D1, 0x002616E2, 0x002616F3, 0x00261706, 0x00261719, 0x0026172C}
C2 = {0x00261624, 0x00261635, 0x00261646, 0x00261657, 0x00261668, 0x0026167B, 0x0026168E, 0x002616A1}
A = K.vs(("A", 0))
REC_GLOBALS = set()


def norm(v):
    """Rename any global token whose absolute address lies in the manager array to GMGR + (offset mod stride)."""
    if v is K.UNK:
        return v
    out = set()
    for b, o in v:
        if isinstance(b, str) and b.startswith("G") and len(b) == 9 and o is not None:
            a = int(b[1:], 16) + o
            if MGR_LO <= a < MGR_HI:
                out.add(("GMGR", (a - MGR_LO) % MGR_STRIDE))
                continue
        out.add((b, o))
    return frozenset(out)


_memaddr = K.memaddr


def _gmgr(v):
    return v is not K.UNK and len(v) > 0 and all(b == "GMGR" and o is not None for b, o in v)


def _nonptr(v):
    return v is K.UNK or all(b is None for b, _ in v)


def memaddr(st, m, ins):
    """As the engine, plus: an index register added to a manager-array address keeps the offset (mod stride),
    because the index is idx*0x288 (code computes the slot address as array + idx*0x288)."""
    if m.index != 0 and m.base not in (0, X.X86_REG_RIP):
        bv = st.r.get(K.fullname(m.base)[0], K.UNK)
        iv = st.r.get(K.fullname(m.index)[0], K.UNK)
        if _gmgr(bv) and _nonptr(iv):
            return frozenset(("GMGR", (o + m.disp) % MGR_STRIDE) for _, o in bv)
        if _gmgr(iv) and m.scale == 1 and _nonptr(bv):
            return frozenset(("GMGR", (o + m.disp) % MGR_STRIDE) for _, o in iv)
    return norm(_memaddr(st, m, ins))


K.memaddr = memaddr
_load = K.load_value


def load_value(st, addr):
    if addr is not K.UNK:
        out = set()
        rest = []
        for b, o in addr:
            if b == "GMGR":
                if o is None or o == 8:
                    out.add(("POOL", 0))
                if o != 8:
                    rest.append((b, o))
            elif b == "POOL":
                if o is None or o >= 8:
                    out.add(("A", 0))
                else:
                    rest.append((b, o))
            elif isinstance(b, str) and b.startswith("G") and len(b) == 9 and o is not None and \
                    int(b[1:], 16) + o in REC_GLOBALS:
                out.add(("A", 0))
            else:
                rest.append((b, o))
        if out:
            r = _load(st, frozenset(rest)) if rest else frozenset()
            return frozenset(out) | (r if r is not K.UNK else frozenset())
    return _load(st, addr)


K.load_value = load_value


def overlaps(addr, size):
    if addr is K.UNK:
        return None
    for b, o in addr:
        if b == "A":
            if o is None:
                return "A+?"
            if o < HI and o + max(size, 1) > LO:
                return "A%+#x" % o
    return None


class Flow(K.Analysis):
    def __init__(self):
        super().__init__()
        self.hits = set()   # (fn, addr, kind, text, where)
        self.bulk = set()
        self.objesc = set()
        self.globesc = set()

    def store(self, f, i, st, addr, size, val):
        w = overlaps(addr, size)
        if w:
            kind = "BULK-WRITE" if size >= 1 << 20 else "WRITE"
            self.hits.add((f, i.address, kind, "%s %s" % (i.mnemonic, i.op_str), w))
        if K.has_actor(val) and addr is not K.UNK and K.sp_off(addr) is None:
            for b, o in addr:
                if isinstance(b, str) and b.startswith("G") and len(b) == 9 and o is not None:
                    self.globesc.add(int(b[1:], 16) + o)
                elif b not in ("SP", "CSP"):
                    self.objesc.add((f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr)))
        # stack bookkeeping as the base engine, without its escape list
        o = K.sp_off(addr)
        if o is not None:
            for k in [k for k in st.s if k < o + size and o < k + 8 and k != o]:
                del st.s[k]
            if size == 8:
                st.s[o] = val
            else:
                st.s.pop(o, None)
        elif addr is K.UNK or any(b == "SP" for b, _ in addr):
            st.s.clear()

    def call(self, f, st, i, t, depth, stack, caller_writes):
        if t in BULK:
            for r, role in (("rcx", "dst"), ("rdx", "src")):
                v = st.r.get(r, K.UNK)
                if K.has_actor(v):
                    self.bulk.add((f, i.address, BULK[t], role, K.desc(v)))
            for r in K.VOLATILE:
                st.r[r] = K.UNK
            return st
        return super().call(f, st, i, t, depth, stack, caller_writes)

    def step(self, f, st, i, depth, stack, caller_writes):
        mn = i.mnemonic
        if mn not in ("lea", "nop") and not mn.startswith("prefetch"):
            for op in i.operands:
                if op.type == X.X86_OP_MEM and op.access & capstone.CS_AC_READ:
                    w = overlaps(memaddr(st, op.mem, i), op.size)
                    if w:
                        self.hits.add((f, i.address, "READ", "%s %s" % (mn, i.op_str), w))
            if ("movs" in mn or "cmps" in mn or "lods" in mn or "scas" in mn) and \
                    mn not in ("movss", "movsd", "movsx", "movsxd", "movshdup", "movsldup") and \
                    K.has_actor(st.r.get("rsi", K.UNK)):
                self.hits.add((f, i.address, "BULK-READ", mn, "rsi=" + K.desc(st.r.get("rsi"))))
        ops = i.operands
        if mn == "add" and len(ops) == 2 and ops[0].type == X.X86_OP_REG and ops[1].type == X.X86_OP_REG:
            dn, dw = K.fullname(ops[0].reg)
            sn, _ = K.fullname(ops[1].reg)
            if dn and sn and dw == 8:
                dv, sv = st.r.get(dn, K.UNK), st.r.get(sn, K.UNK)
                keep = dv if (_gmgr(dv) and _nonptr(sv)) else sv if (_gmgr(sv) and _nonptr(dv)) else None
                if keep is not None:
                    st.r[dn] = keep
                    return R.branch_targets(i), st, False
        return super().step(f, st, i, depth, stack, caller_writes)


def verb_handlers():
    p = os.path.join(HERE, "..", "..", "..", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
    rows = io.open(p, encoding="utf-8").read().splitlines()
    head = rows[0].split("\t")
    cols = [head.index(c) for c in ("begin", "poll", "result", "arg_handler")]
    out = set()
    for l in rows[1:]:
        c = l.split("\t")
        for k in cols:
            if k < len(c) and c[k].strip():
                try:
                    out.add(int(c[k], 16))
                except ValueError:
                    pass
    return sorted(a for a in out if a in K.ext)


_REFS = None


def referrers(lo, hi):
    """Functions with an instruction whose rip target or (non-rip) disp32 + image base lies in [lo, hi).
    One decode of the whole image, kept as target -> functions."""
    global _REFS
    if _REFS is None:
        base = 0x00120000
        _REFS = collections.defaultdict(set)
        for f in sorted(K.ext):
            for i in R.md.disasm(R.at(f, K.ext[f]), f):
                for op in i.operands:
                    if op.type != X.X86_OP_MEM:
                        continue
                    if op.mem.base == X.X86_REG_RIP:
                        a = i.address + i.size + op.mem.disp
                    elif (op.mem.base != 0 or op.mem.index != 0) and op.mem.disp >= 0x01000000:
                        a = base + (op.mem.disp & 0xFFFFFFFF)
                    else:
                        continue
                    _REFS[a].add(f)
    out = set()
    for a, fs in _REFS.items():
        if lo <= a < hi:
            out |= fs
    return out


def main():
    an = Flow()
    handlers = verb_handlers()
    roots = referrers(MGR_LO, MGR_HI)
    print("manager-array referrers: %d" % len(roots), flush=True)
    done, returners = set(), set()
    rounds = 0
    while True:
        rounds += 1
        for h in handlers:
            an.summary(h, (("rcx", A), ("rdx", A)), 0, ())
        print("round %d: handlers done, bodies %d" % (rounds, len(an.fns)), flush=True)
        work = sorted(roots - done)
        while work:
            f = work.pop()
            if f in done:
                continue
            done.add(f)
            an.summary(f, (), 0, ())
            for (g, ctx), (rv, _) in list(an.memo.items()):
                if K.has_actor(rv) and g not in returners:
                    returners.add(g)
                    work.extend(sorted(c for c in R.CALLERS.get(g, ()) if c not in done))
        new = set(a for a in an.globesc if a not in REC_GLOBALS)
        if not new:
            break
        REC_GLOBALS.update(new)
        for a in new:
            roots |= referrers(a, a + 8)
        roots = set(f for f in roots if f in K.ext)
        print("round %d: new record globals %s" % (rounds, " ".join("%08X" % a for a in sorted(new))), flush=True)
        done.clear()  # re-run everything with the new global rule (memo is per context; clear it)
        an.memo.clear()
        if rounds > 6:
            break
    hits = sorted(an.hits)
    c1 = C1 <= set(h[1] for h in hits if h[2] == "READ")
    c2 = C2 <= set(h[1] for h in hits if h[2] == "WRITE")
    print("%s  C1 interpreter PUSHI/PUSHF register loads found through the flow: %d of 8" % (
        "PASS" if c1 else "FAIL", len(C1 & set(h[1] for h in hits))))
    print("%s  C2 interpreter POPI/POPF register stores found through the flow: %d of 8" % (
        "PASS" if c2 else "FAIL", len(C2 & set(h[1] for h in hits))))
    print("verb handlers seeded: %d; manager-array referrer roots + returner callers: %d; rounds %d" % (
        len(handlers), len(done), rounds))
    print("functions returning a record: %s" % " ".join("%08X" % g for g in sorted(returners)))
    print("globals holding a record (escapes to globals): %s" % " ".join("%08X" % g for g in sorted(REC_GLOBALS)))
    print("bodies analysed %d, contexts %d; depth/recursion cuts %d, of which carry a record %d" % (
        len(an.fns), len(an.memo), len(an.recursive), sum(1 for c in an.recursive if c[2])))
    for c in sorted(set(c for c in an.recursive if c[2])):
        print("  CUT %08X depth %d" % (c[0], c[1]))
    print()
    byfn = collections.defaultdict(list)
    for h in hits:
        byfn[h[0]].append(h)
    print("accesses that can overlap record +0x64..+0x83: %d in %d functions" % (len(hits), len(byfn)))
    for fn in sorted(byfn):
        tag = "INTERPRETER" if fn == 0x0025E4C0 else "OTHER"
        print("  %s %08X" % (tag, fn))
        for h in byfn[fn]:
            print("      %08X %-10s %-48s at %s" % (h[1], h[2], h[3], h[4]))
    print("bulk calls with a record pointer: %d" % len(an.bulk))
    for b in sorted(an.bulk):
        print("  BULK %08X %08X %s %s=%s" % b)
    print("record pointer stored into object fields (not globals): %d" % len(an.objesc))
    for e in sorted(an.objesc):
        print("  OBJESC %08X %08X %-44s to %s" % e)
    ind = sorted(set(an.indirect))
    print("indirect calls/jumps receiving a record: %d" % len(ind))
    for e in ind:
        print("  INDIRECT %08X %08X %-40s args %s" % e)
    with io.open(os.path.join(HERE, "rc15_flow.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("function\taddress\tkind\tinstruction\trecord_offset\n")
        for h in hits:
            o.write("%08X\t%08X\t%s\t%s\t%s\n" % h)
    return 0 if c1 and c2 else 1


if __name__ == "__main__":
    sys.exit(main())
