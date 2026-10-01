"""sd_header_reads.py - who reads save-header dwords 0x12/0x13 (+0x48/+0x4C) and the stamp copies (+0x58/+0x60) of the
active image and the capture image (OPUS, 2026-09-30). Registers: SD-40, SD-42.

Engine: the OV-5/8 (d) value-flow census (../ov58d-pointer-flow-0930/ov58d_flow.py) with its roots, escape globals
(02092758 = image, 020927C0 = image+0x8200, the 022C1740 record table) and callees analysed under their argument
values. The active image 02164280 is the state (021B290C) at -0x4E68C, so header byte h is token (A, -0x4E68C + h); the
capture image 021BA940 (getter 002EF620) is token (CAP, h). Every memory operand the engine resolves is recorded by
K.memaddr: a READ is any instruction whose source operand is that memory (mov/movzx/movsx/cmp/test/and/or/add/sub/xor
reading it, movups/movsd loads), a WRITE a store.

Control H1: SaveRuntime_InitializeHeaderAndImageBackedState 00253A80 writes +0x58 at 00253AB8 (the stamp's writer).
Control H2: the load-side reader T3b names for dword 0x12's neighbour group must be reached: every header access the
census finds is printed, so a reader of +0x48 / +0x4C / +0x58 / +0x60 would appear by function.

Limit: this follows the two static images only. A header copy in a heap buffer (a slot file read for the save list)
is outside its roots; the literal-displacement scan in part 2 covers the save controller's own functions.
"""
import collections, io, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ov58d-pointer-flow-0930"))
import ov58d_flow as F  # noqa: E402
K, X = F.K, F.X

HDR = {0x48: "dword 0x12 (+0x48)", 0x4C: "dword 0x13 (+0x4C)", 0x58: "stamp copy +0x58", 0x60: "stamp copy +0x60"}
WINDOW = 0x200
READ_MN = {"mov", "movzx", "movsx", "movsxd", "cmp", "test", "and", "or", "add", "sub", "xor", "movups", "movaps", "movdqu",
           "movsd", "movq", "movd", "lea"}
acc = collections.defaultdict(set)   # (image, header offset) -> {(fn, addr, R/W, text)}
CUR = []


# The two other whole-image copies: 02211000 (getter 002EF630; 0057E310 copies it into the capture image) and
# 022676C0 (002EF570 backs the active image up into it). A rip address in either header window, or 002EF630's
# result, is that image's header.
EXTRA = {"third": 0x02211000, "backup": 0x022676C0}
THIRD_GETTER = 0x002EF630


def hdr_off(b, o):
    if o is None:
        return None
    if b in EXTRA and 0 <= o < WINDOW:
        return b, o
    if b == "A" and F.IMG_TO_STATE <= o < F.IMG_TO_STATE + WINDOW:
        return "active", o - F.IMG_TO_STATE
    if b == "CAP" and 0 <= o < WINDOW:
        return "capture", o
    return None


_orig_memaddr = K.memaddr


def memaddr(st, m, ins):
    if m.base == X.X86_REG_RIP:
        t = ins.address + ins.size + m.disp
        for name, base in EXTRA.items():
            if base <= t < base + WINDOW:
                a = K.vs((name, t - base))
                break
        else:
            a = _orig_memaddr(st, m, ins)
    else:
        a = _orig_memaddr(st, m, ins)
    if a is not K.UNK and CUR:
        ops = ins.operands

        def same(q):
            return (q.base, q.index, q.scale, q.disp, q.segment) == (m.base, m.index, m.scale, m.disp, m.segment)
        is_dst = bool(ops) and ops[0].type == X.X86_OP_MEM and same(ops[0].mem)
        for b, o in a:
            h = hdr_off(b, o)
            if h is None:
                continue
            img, off = h
            size = ops[0].size if is_dst else (ops[1].size if len(ops) > 1 else 4)
            for want in HDR:
                if off < want + 4 and off + max(size, 1) > want:
                    kind = "W" if (is_dst and ins.mnemonic not in ("cmp", "test")) else ("LEA" if ins.mnemonic == "lea" else "R")
                    acc[(img, want)].add((CUR[-1], ins.address, kind, "%s %s" % (ins.mnemonic, ins.op_str)))
    return a


K.memaddr = memaddr
F.K.memaddr = memaddr
_has = K.has_actor
K.has_actor = lambda v: _has(v) or (v is not K.UNK and any(b in EXTRA for b, _ in v))


def _touch_all_mem(st, i):
    """The engine resolves a memory operand only for a load into a register or a store; a read-only use (cmp, test,
    a flag-setting and/or/add into a register from memory is covered, a compare against memory is not) never reaches
    memaddr. Resolve every memory operand once before the step, so the recording hook sees every access."""
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base not in (0, X.X86_REG_RIP):
            memaddr(st, op.mem, i)


class HdrCensus(F.Census):
    def step(self, f, st, i, depth, stack, caller_writes):
        if CUR:
            _touch_all_mem(st, i)
        return super().step(f, st, i, depth, stack, caller_writes)

    def call(self, f, st, i, t, depth, stack, caller_writes):
        if t == THIRD_GETTER:
            for r in K.VOLATILE:
                st.r[r] = K.UNK
            st.r["rax"] = K.vs(("third", 0))
            return st
        return super().call(f, st, i, t, depth, stack, caller_writes)

    def run(self, f, ctx, depth, stack):
        CUR.append(f)
        try:
            return super().run(f, ctx, depth, stack)
        finally:
            CUR.pop()


def main():
    t0 = time.time()
    refs, calls = F.scan()
    # the escape globals the OV-5/8 (d) census found stable
    F.globals_root[0x02092758] = frozenset([("A", F.IMG_TO_STATE)])
    F.globals_root[0x020927C0] = frozenset([("A", 0x8200 + F.IMG_TO_STATE)])
    F.globals_root[0x022C1740] = frozenset([("REC", 0)])
    F.TABLES.add(0x022C1740)
    an = HdrCensus()
    roots = set(f for g in F.globals_root for f, _, _ in refs.get(g, ()))
    roots |= set(f for g, xs in refs.items() if F.IMG_LO <= g < F.IMG_HI for f, _, _ in xs)
    roots |= set(f for g, xs in refs.items() if 0x021BA940 <= g < 0x021BA940 + WINDOW for f, _, _ in xs)
    roots |= calls.get(F.IMG_GETTER, set()) | calls.get(F.CAP_GETTER, set()) | calls.get(THIRD_GETTER, set())
    for base in EXTRA.values():
        roots |= set(f for g, xs in refs.items() if base <= g < base + WINDOW for f, _, _ in xs)
    done = set()
    while True:
        new = sorted(roots - done)
        if not new:
            break
        for f in new:
            try:
                an.summary(f, (), 0, ())
            except Exception as e:  # noqa: BLE001
                print("  error in %08X: %s %r (a blind spot)" % (f, type(e).__name__, e))
        done |= set(new)
        roots |= set(c for f in an.state_returners for c in calls.get(f, ()))
    print("roots analysed %d, bodies reached %d (%.0f s)" % (len(done), len(an.fns), time.time() - t0))
    h1 = any(x[1] == 0x00253AB8 and x[2] == "W" for x in acc[("active", 0x58)])
    print("%s  H1 00253A80 writes the active header's +0x58 at 00253AB8" % ("PASS" if h1 else "FAIL"))
    with io.open(os.path.join(HERE, "sd_header_reads.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("image\theader\tfunction\taddress\tkind\tinstruction\n")
        for (img, want), xs in sorted(acc.items()):
            for fn, a, kind, text in sorted(xs):
                o.write("%s\t+0x%X\t%08X\t%08X\t%s\t%s\n" % (img, want, fn, a, kind, text))
    for img in ("active", "capture", "third", "backup"):
        for want, name in HDR.items():
            xs = acc.get((img, want), set())
            rd = sorted(x for x in xs if x[2] == "R")
            wr = sorted(x for x in xs if x[2] == "W")
            print("%-8s %-20s reads %2d in %s | writes %2d in %s" % (
                img, name, len(rd), " ".join(sorted(set("%08X@%08X" % (x[0], x[1]) for x in rd))) or "-",
                len(wr), " ".join(sorted(set("%08X" % x[0] for x in wr))) or "-"))
    print("elapsed %.0f s" % (time.time() - t0))
    return 0 if h1 else 1


if __name__ == "__main__":
    sys.exit(main())
