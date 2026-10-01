"""lmap_field_reads.py - RC-35 / RC-36: which code reads a menumap_location.bin point's +0x0C (RC-36: a marker's
destination-label id) and whether anything reads the 8-byte block between arrays C and D (RC-35). OPUS, 2026-09-30.
Static, the certified image. Reads only.

The location table is `[[02B457E0] + 0xE0]`; its only point accessor is 003BF430(n, i, &kind), which returns the point
and writes kind 0 (array A), 1 (array B) or 3 (out of range) (lmap page section 10.2).

Census R36: for every call to 003BF430, the value-flow engine of k14_actorflow.py follows the returned pointer (token P)
through registers, the stack and callees, and records every memory READ whose address is P + d. The kind the call wrote
is read back from its out-slot (token K on the stack) and each P + 0x0C read is listed with the instruction; the README
reads the kind test on each path by hand.
Census R35: every function that loads the table (`mov r, [r' + 0xE0]` after a load of [02B457E0]) is listed, and every
instruction in them that multiplies a count by 20 (the array-C stride) is shown; a reader of the 8-byte block must form
C + 20*countC and read at that address + 0..7 before adding the 8 that 003BFF20 / 003C1070 add.
Controls: R36 must find the known kind-0 read 003C17E0's caller 003C1680 (its +0x0C read at 003C17A4 region, P5 of
CONTRACT's record) - that function does not call 003BF430, so the control is instead 003BCDE0 (C2: `+0xC` compared at
003BCE94..003BCEA3 on the point 003BF430 returned); and 003C0740's walker, which calls 003BF430 at 003C0760/003C0798.
"""
import collections, os, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402

R = K.R
ACC = 0x003BF430
G = 0x02B457E0


class Reads(K.Analysis):
    def __init__(self):
        super().__init__()
        self.reads = []

    def call(self, f, st, i, t, depth, stack, caller_writes):
        if t == ACC:
            for r in K.VOLATILE:
                st.r[r] = K.UNK
            st.r["rax"] = K.vs(("P%08X" % i.address, 0))
            return st
        return super().call(f, st, i, t, depth, stack, caller_writes)

    def step(self, f, st, i, depth, stack, caller_writes):
        for n, op in enumerate(i.operands):
            if op.type == X.X86_OP_MEM and not (n == 0 and op.access & capstone.CS_AC_WRITE and not op.access & capstone.CS_AC_READ) \
                    and i.mnemonic not in ("lea", "nop") and not i.mnemonic.startswith("prefetch"):
                a = K.memaddr(st, op.mem, i)
                if a is not K.UNK:
                    for b, o in a:
                        if isinstance(b, str) and b.startswith("P") and not b.startswith("PS"):
                            self.reads.append((b[1:], f, i.address, "%s %s" % (i.mnemonic, i.op_str), o))
        return super().step(f, st, i, depth, stack, caller_writes)


def callers():
    out = collections.defaultdict(list)
    for f, n in R.ext.items():
        d = R.at(f, n)
        if not d:
            continue
        for i in R.md.disasm(d, f):
            if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == ACC:
                out[f].append(i.address)
    return out


def main():
    cs = callers()
    an = Reads()
    for f in sorted(cs):
        an.summary(f, (), 0, ())
    rd = sorted(set(an.reads))
    by = collections.defaultdict(list)
    for site, f, a, text, o in rd:
        by[(site, f)].append((a, text, o))
    print("callers of 003BF430: %d functions, %d call sites" % (len(cs), sum(len(v) for v in cs.values())))
    c0c = [(s, f, a, t) for (s, f), v in by.items() for a, t, o in v if o == 0x0C]
    print("reads of P+0x0C: %d" % len(c0c))
    for s, f, a, t in c0c:
        print("  +0x0C  call %s in %08X: read at %08X  %s" % (s, f, a, t))
    print("all P reads by offset:", dict(collections.Counter(o for *_, o in rd)))
    for (s, f), v in sorted(by.items()):
        print("  call %s in %08X: %s" % (s, f, "; ".join("%08X +%s" % (a, "?" if o is None else hex(o)) for a, t, o in v)))
    ok1 = any(f == 0x003BCDE0 for s, f, a, t in c0c)
    print("%s  control: 003BCDE0's +0x0C comparison is found" % ("PASS" if ok1 else "FAIL"))
    ok2 = 0x003C0740 in cs
    print("%s  control: 003C0740 is a caller" % ("PASS" if ok2 else "FAIL"))
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    sys.exit(main())
