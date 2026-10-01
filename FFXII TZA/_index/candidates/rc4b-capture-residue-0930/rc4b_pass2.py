"""rc4b_pass2.py - RC-4 residue, pass 2 (ORACLE, 2026-09-30). Static.

OPUS's interprocedural flow (../rc4-capture-machine-0930/rc4_flow.py, on k14_actorflow.py) re-run with its four blind
spots closed:

1. SELF-POINTER FIELDS. A load from A+K where the object stores a pointer into itself returns that pointer. The map is
   pass 1's exact-offset self stores (rc4b_selffields.tsv), plus the four stores 001897C0 makes at an index the flow
   could not resolve. The index is a view-pair number k in {0, 1}, fixed by `setne al` at 00189817 (checked below):
     A+0xD8  <- A+0xF8    A+0x410 <- A+0x430    (view k, [rbx+0xB8] = rcx, 00189A55)
     A+0x268 <- A+0x288   A+0x5A0 <- A+0x5C0    (second view of pair k, 00189B63)
2. VIRTUAL CALLS. `call [reg + slot]` whose reg holds the vtable loaded from A+K is resolved through the vtable the
   constructors store there (checked below against the bytes):
     views     A + {0x20, 0x1B0, 0x358, 0x4E8, 0x690, 0x820}                       -> 008C5D68 (00184CE0 stores it)
     Phyre     A + {0x128, 0x2B8, 0x460, 0x5F0, 0x798, 0x928, 0x9C8, 0xA50}         -> 00D562A8 (0062DD10 stores it
               after the base constructor 006CB5F0 stored 00D86B80; both are resolved, to be conservative)
     allocators A + 0xC50 + 0x20k, k < 4 (vector triples at 0xC38, 00184CB0 -> 001EDF00) -> 00902720
   Resolved targets are analysed like direct calls under the receiver.
3. CONSTRUCTORS RUN THROUGH THE EH VECTOR ITERATOR 00808FE4 (`call rsi`), seeded directly: 00184CE0 at A+0x20 and
   A+0x358 (00184F74: stride 0x338, count 2), 00184CB0 at A+0xC38 + 0x20k (count 4); and the matching destructors
   001850B0 / 00185070.
4. ESCAPE INTO CLASS 00902F90. 001F1E80 stores A at [obj + 0x18]. A token B is seeded as rcx into every code slot of
   vtable 00902F90, and a load from B+0x18 yields A.

Output: every store that can cover A+0xDAC, beyond pass 1's (rc4b_pass2.out). Control: the five known stores are
found again. Blind spots this pass does not close are listed: the escape of view pointers into the external object
[A+8] (0060CE50 -> +0xA8, 001F0AD0 -> slot 2 with r8 = a view pair). rc4b_scan.py bounds those.
"""
import contextlib, io, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc4-capture-machine-0930"))
import rc4_flow as F  # noqa: E402
K = F.K
R = K.R
from capstone import x86 as X  # noqa: E402

FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def u64(a):
    return struct.unpack("<Q", R.at(a, 8))[0]


def dis(a, n=0x20):
    return {i.address: (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(a, n), a)}


# ---- the facts the models rest on ----
d = dis(0x00189812, 0x10)
check(d.get(0x00189812) == ("xor", "eax, eax") and d.get(0x00189817) == ("setne", "al"), "M1 001897C0's pair index is setne al: 0 or 1")
c = dis(0x00184F5D, 0x30)
check(c.get(0x00184F74) == ("mov", "edx, 0x338") and c.get(0x00184F79) == ("lea", "r8d, [rsi + 2]")
      and c.get(0x00184F6D, ("", ""))[0] == "lea", "M2 00184F20 builds 2 view pairs of 0x338 at A+0x20 with 00184CE0 through 00808FE4")
v = dis(0x00184D18, 0x10)
check(v.get(0x00184D1F) == ("mov", "qword ptr [rdi], rsi") and u64(0x008C5D68 + 8) == 0x00189C20,
      "M3 00184CE0 stores view vtable 008C5D68 (slot 1 = 00189C20)")
check(u64(0x00902720 + 0x10) == 0x001EDF80 and u64(0x00902720 + 0x18) == 0x001EDFE0 and u64(0x00D562A8 + 0x50) == 0x0062E1C0,
      "M4 allocator vtable 00902720 slots 2/3 = 001EDF80/001EDFE0; Phyre vtable 00D562A8 slot 10 = 0062E1C0")

SELF = {}
for line in io.open(os.path.join(HERE, "rc4b_selffields.tsv"), encoding="utf-8").read().splitlines()[1:]:
    kind, _f, _a, off, val = line.split("\t")
    if kind == "SELF":
        vals = set()
        for part in val.split(","):
            if part.startswith("A+"):
                vals.add(("A", int(part[2:], 16)))
        SELF.setdefault(int(off, 16), set()).update(vals)
for off, val in ((0xD8, 0xF8), (0x410, 0x430), (0x268, 0x288), (0x5A0, 0x5C0)):
    SELF.setdefault(off, set()).add(("A", val))
PAIRS = (0x20, 0x358, 0x690)
VIEWS = sorted({p for p in PAIRS} | {p + 0x190 for p in PAIRS})
PHYRE = sorted({p + 0x108 for p in PAIRS} | {p + 0x298 for p in PAIRS} | {0x9C8, 0xA50})
ALLOC = [0xC50 + 0x20 * k for k in range(4)]
VT = {}
for k in VIEWS:
    VT[k] = [0x008C5D68]
for k in PHYRE:
    VT[k] = [0x00D562A8, 0x00D86B80]
for k in ALLOC:
    VT[k] = [0x00902720]
print("self fields modelled: %d; vtable receivers: %d" % (len(SELF), len(VT)))

_prev_load = K.load_value


def load_value(st, addr):
    if addr is not K.UNK and len(addr) == 1:
        (b, o), = addr
        if b == "A" and o in SELF:
            return frozenset(SELF[o])
        if b == "B" and o == 0x18:
            return K.vs(("A", 0))
    return _prev_load(st, addr)


K.load_value = load_value
RESOLVED = []
BaseFlow = F.Flow


NEWSELF = {}


class Flow2(BaseFlow):
    def store(self, f, i, st, addr, size, val):
        if addr is not K.UNK and len(addr) == 1 and size == 8 and K.has_actor(val) and val is not K.UNK:
            (b, o), = addr
            if b == "A" and o is not None:
                NEWSELF.setdefault(o, set()).update((bb, oo) for bb, oo in val if bb == "A" and oo is not None)
        return BaseFlow.store(self, f, i, st, addr, size, val)

    def step(self, f, st, i, depth, stack, caller_writes):
        if i.mnemonic == "call" and i.operands and i.operands[0].type == X.X86_OP_MEM and i.operands[0].mem.base not in (0, X.X86_REG_RIP):
            addr = K.memaddr(st, i.operands[0].mem, i)
            targets = set()
            if addr is not K.UNK:
                for b, o in addr:
                    m = re.match(r"L\(A\+0x([0-9a-f]+)\)$", str(b))
                    if m and o is not None and int(m.group(1), 16) in VT:
                        for vt in VT[int(m.group(1), 16)]:
                            t = u64(vt + o)
                            if t in K.ext:
                                targets.add(t)
            if targets:
                out = None
                for t in sorted(targets):
                    RESOLVED.append((f, i.address, t))
                    s2 = self.call(f, st.copy(), i, t, depth, stack, caller_writes)
                    out = s2 if out is None else out.merge(s2)
                return [i.address + i.size], out, False
        return BaseFlow.step(self, f, st, i, depth, stack, caller_writes)


holder = {}
_init = Flow2.__init__


def init(self):
    _init(self)
    holder["an"] = self


Flow2.__init__ = init
F.Flow = Flow2


def _A(o):
    return K.vs(("A", o))


SEEDS = [(0x00184CE0, _A(p)) for p in (0x20, 0x358)] + [(0x001850B0, _A(p)) for p in (0x20, 0x358, 0x690)]
SEEDS += [(0x00184CB0, _A(0xC38 + 0x20 * k)) for k in range(4)] + [(0x00185070, _A(0xC38 + 0x20 * k)) for k in range(4)]
SEEDS += [(t, _A(k)) for k in VIEWS for t in (u64(0x008C5D68), u64(0x008C5D68 + 8))]
SEEDS += [(t, _A(k)) for k in ALLOC for t in (0x001EDF80, 0x001EDFE0)]
SEEDS += [(u64(vt + 8 * s), _A(k)) for k in PHYRE for vt in (0x00D562A8, 0x00D86B80) for s in range(11)
          if u64(vt + 8 * s) in K.ext]
B_SLOTS = [u64(0x00902F90 + 8 * s) for s in range(12) if u64(0x00902F90 + 8 * s) in K.ext]
SEEDS += [(t, K.vs(("B", 0))) for t in B_SLOTS]


def run_once():
    RESOLVED.clear()
    NEWSELF.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        F.main()
    an = holder["an"]
    for t, rcx in SEEDS:
        an.summary(t, (("rcx", rcx),), 0, ())
    return an


def main():
    for it in range(1, 6):
        an = run_once()
        grow = {o: v for o, v in NEWSELF.items() if not v <= SELF.get(o, set())}
        print("iteration %d: self fields %d, new or grown this pass %d" % (it, len(SELF), len(grow)))
        if not grow:
            break
        for o, v in grow.items():
            SELF.setdefault(o, set()).update(v)
    print("self fields at the fixpoint: %s" % " ".join("A%+#x<-%s" % (o, "/".join("%#x" % x for _, x in sorted(v))) for o, v in sorted(SELF.items())))
    hits = sorted(set(an.hits))
    known = [h for h in hits if h[1] in F.MACHINE]
    check(set(h[1] for h in known) == F.MACHINE, "C the five known stores are found again")
    p1 = set()
    for line in io.open(os.path.join(HERE, "..", "rc4-capture-machine-0930", "rc4_flow.out"), encoding="utf-8"):
        m = re.match(r"\s+(KNOWN|OTHER) ([0-9A-F]{8}) ([0-9A-F]{8})", line)
        if m:
            p1.add(int(m.group(3), 16))
    new = [h for h in hits if h[1] not in F.MACHINE and h[1] not in p1]
    print("seeds: %d (class 00902F90 code slots %d); bodies analysed %d; virtual calls resolved %d at %d sites" % (
        len(SEEDS), len(B_SLOTS), len(an.fns), len(set(RESOLVED)), len(set((a, b) for a, b, _ in RESOLVED))))
    print("stores that can cover A+0xDAC: %d distinct; in pass 1's list: %d; NEW: %d" % (
        len(set(h[1] for h in hits)), len(set(h[1] for h in hits) & (p1 | F.MACHINE)), len(set(h[1] for h in new))))
    for h in new:
        print("  NEW %08X %08X %-40s base %-24s value %s" % h)
    esc = sorted(set(an.escapes))
    ind = sorted(set(an.indirect))
    res_sites = set((a, b) for a, b, _ in RESOLVED)
    unres = [e for e in ind if (e[0], e[1]) not in res_sites]
    print("indirect calls receiving the object that stay unresolved: %d" % len(unres))
    for e in unres:
        print("  UNRESOLVED %08X %08X %-40s args %s" % e)
    print("escapes: %d" % len(esc))
    for e in esc:
        print("  ESCAPE %08X %08X %-40s to %s" % e)
    carrying = [f for (f, k) in an.memo if f == 0x006FF5D0 and any(K.has_actor(v) for _r, v in k)]
    check(not carrying, "N the foreign +0xCB8 writer 006FF5D0 is never analysed with the object in any argument")
    print("\nFAILS %d" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
