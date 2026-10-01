"""For one flags field: which bits are set, which are cleared, which are only tested.

WHY A BIT NEEDS THE SAME TREATMENT AS A FIELD. This kit already insists that a write with no
reader and a read with no writer look identical to an instrument that measures only one side.
The same is true one level down. A bit that is SET and never CLEARED is a one-way latch and the
contract says so; a bit that is TESTED and never set is a dead branch or a sign that the setter
was missed; a bit that is cleared and never set is the same mistake seen from the other end.
None of those is visible to anyone reading one function.

WHAT IT MEASURES. Every instruction in the image whose destination is `[reg + disp]` and whose
source is an IMMEDIATE, for `or`, `and`, `xor`, `test`, `bt`, `bts`, `btr`, plus `bt`-family
reads. From those it builds, per bit: the instructions that SET it (`or` with the bit, `bts`),
that CLEAR it (`and` with the bit zero, `btr`), and that TEST it (`test` with the bit, `bt`).

AND WHAT IT CANNOT SEE, WHICH IS STATED IN THE OUTPUT AND NOT ONLY HERE. A full-word store -
`mov dword ptr [reg + disp], eax` - can set or clear every bit at once and carries no immediate
to read. The scan counts those separately and prints the count as a BLIND SPOT, because a
"never cleared" verdict is only as good as the reader's willingness to go and read them. It
also cannot tell one type from another: a displacement is not a type, so the instructions it
returns are the candidate population and the caller decides which belong to the field in
question.

THE CONTROL is built in and printed: a displacement whose bits are ordinary state should show
bits with BOTH setters and clearers. If every bit at a displacement looks like a latch, the
scan has most likely collected several unrelated types at one offset rather than found a
remarkable structure.

    scan_flag_bit_lifecycle.py --disp 0x80 [--only 0x...] [--exe PATH] [--funcs PATH]
"""
import argparse
import collections
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE_DEFAULT = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS_DEFAULT = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
SET_OPS = ("or", "bts")
CLEAR_OPS = ("and", "btr")
TEST_OPS = ("test", "bt")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE_DEFAULT)
    ap.add_argument("--funcs", default=FUNCS_DEFAULT)
    ap.add_argument("--disp", type=lambda x: int(x, 0), required=True)
    ap.add_argument("--only", type=lambda x: int(x, 0), default=None,
                    help="report only this bit mask's bits")
    a = ap.parse_args()

    raw = open(a.exe, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off, secs = pe + 24 + opt, []
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((nm, ib + va, vs, rs, pr))
        off += 40

    def fo(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)
        return None

    funcs = []
    with open(a.funcs, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 3:
                try:
                    funcs.append((int(c[0], 16), int(c[2])))
                except ValueError:
                    pass

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    sets = collections.defaultdict(list)
    clears = collections.defaultdict(list)
    tests = collections.defaultdict(list)
    opaque = []

    for entry, n in funcs:
        f = fo(entry)
        if f is None or n <= 0:
            continue
        for i in md.disasm(raw[f:f + n], entry):
            o = i.operands
            if (len(o) != 2 or o[0].type != X86_OP_MEM or not o[0].mem.base
                    or o[0].mem.base == X86_REG_RIP or o[0].mem.index != 0
                    or o[0].mem.disp != a.disp):
                continue
            base = md.reg_name(o[0].mem.base)
            if base in ("rsp", "esp", "rbp", "ebp"):
                continue
            cite = (entry, i.address, "%s %s" % (i.mnemonic, i.op_str))
            if o[1].type != X86_OP_IMM:
                if i.mnemonic in ("mov", "or", "and", "xor"):
                    opaque.append(cite)
                continue
            imm = o[1].imm & ((1 << (8 * max(o[0].size, 1))) - 1)
            width = 8 * max(o[0].size, 1)
            if i.mnemonic in SET_OPS:
                bits = [imm] if i.mnemonic == "bts" else \
                    [b for b in range(width) if imm >> b & 1]
                if i.mnemonic == "bts":
                    bits = [o[1].imm]
                for b in bits:
                    sets[b].append(cite)
            elif i.mnemonic in CLEAR_OPS:
                if i.mnemonic == "btr":
                    clears[o[1].imm].append(cite)
                else:
                    for b in range(width):
                        if not (imm >> b & 1):
                            clears[b].append(cite)
            elif i.mnemonic in TEST_OPS:
                if i.mnemonic == "bt":
                    tests[o[1].imm].append(cite)
                else:
                    for b in range(width):
                        if imm >> b & 1:
                            tests[b].append(cite)

    allbits = sorted(set(sets) | set(clears) | set(tests))
    if a.only is not None:
        allbits = [b for b in allbits if a.only >> b & 1]

    print("DISPLACEMENT +0x%X, bits reached by an immediate operation" % a.disp)
    print("  %-5s %-6s %-8s %-7s %s" % ("bit", "sets", "clears", "tests", "verdict"))
    latch, dead, phantom, ordinary = [], [], [], []
    for b in allbits:
        s, c, t = len(sets[b]), len(clears[b]), len(tests[b])
        if s and not c:
            v = "SET AND NEVER CLEARED - a one-way latch, if these are one type"
            latch.append(b)
        elif c and not s:
            v = "CLEARED AND NEVER SET"
            phantom.append(b)
        elif t and not s and not c:
            v = "TESTED ONLY - no immediate ever writes it"
            dead.append(b)
        else:
            v = "ordinary"
            ordinary.append(b)
        print("  %-5s %-6d %-8d %-7d %s" % (b, s, c, t, v))

    print()
    print("CONTROL  bits with BOTH a setter and a clearer: %d of %d"
          % (len(ordinary), len(allbits)))
    if allbits and not ordinary:
        print("  EVERY bit looks like a latch or a phantom. That is far more likely to mean this "
              "displacement collects several unrelated types than to be a real structure.")

    print()
    print("BLIND SPOT  full-word or register-sourced writes at this displacement, which carry no")
    print("            immediate and can set or clear every bit at once: %d" % len(opaque))
    print("            A 'never cleared' verdict is only as good as a reading of these.")
    for b in latch:
        print()
        print("  bit %d SETTERS:" % b)
        for e, ad, t in sets[b][:8]:
            print("      %08X (in %08X)  %s" % (ad, e, t))
        print("  bit %d TESTERS:" % b)
        for e, ad, t in tests[b][:8]:
            print("      %08X (in %08X)  %s" % (ad, e, t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
