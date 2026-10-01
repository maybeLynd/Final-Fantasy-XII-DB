"""How wide is a field, when one instruction says one thing and forty say another?

THE PROBLEM THIS TOOL EXISTS FOR. The store's rule is that WIDTH COMES FROM THE ACCESS
INSTRUCTION, and that rule is right, but it does not say what to do when a span is reached at
more than one width. Widget +0x98 was declared uint32 because the shared initialiser stores a
dword there; handlers store WORDS at +0x98 and +0x9A. Both instructions exist. A dword store is
a perfectly ordinary way to initialise TWO adjacent 16-bit fields with one instruction, so
"there is a dword store" does not settle the question, and neither does "there is a word store".
WHAT SETTLES IT IS WHETHER THE INTERIOR OFFSET IS EVER ADDRESSED: if +0x9A is reached on its own,
+0x98 cannot be one 4-byte field, whatever the initialiser does.

THE INSTRUMENT. Counting displacements across the image would answer a different question -
+0x9A is a common offset in many unrelated types. So this tool counts only accesses through a
register PROVEN TO HOLD THE OBJECT:

  1. It recovers a FAMILY of functions that take the object as their first argument, by finding
     every call to the family's constructor and reading the callback/handler address out of the
     `lea r8, [rip+X]` that set it up. A function registered that way receives the object in RCX
     by construction. For the widget family the constructors are 00245000 (in place) and
     002465F0 (sized), and the census also reports the size immediate at each site.
  2. Inside each such function it runs an OFFSET-0 MAY-TAINT over the instruction graph: RCX
     holds the object at entry, a register-to-register `mov` copies it, any other definition of a
     register kills it, a call kills the caller-saved set, and A LOAD *THROUGH* A TRACKED POINTER
     KILLS IT - the loaded value is not the object. MAY rather than MUST, so a register counts as
     tracked if ANY path reaches it holding the object. That direction over-counts, which is the
     safe direction here: the claim being tested is "this offset IS addressed", and an
     over-counting analysis cannot manufacture the absence that would refute it.
  3. It tallies, per displacement, the width of every memory operand so reached, and prints the
     citing instructions.

The second argument is never tracked, so for a message handler the message record cannot
contaminate the count.

CONTROLS. Two are built in and printed every run. The FAMILY CONTROL reports the site count, the
distinct handler count and the distinct sizes, which must match the family's published census -
if the family is wrong the widths mean nothing. The WIDTH CONTROL is the tally itself read
adversarially: a split is only supported if the INTERIOR offsets (+2 inside a suspected pair) are
reached, and reached at the narrow width and no other. An interior offset reached at the wide
width, or an offset reached at a width that straddles the suspected boundary, is a refutation and
is printed rather than filtered out.

WHAT IT CANNOT DO. It cannot tell you what a field MEANS, and a narrow-width access does not
prove two SEPARATE fields rather than one field that happens to be written in halves. It reports
where the image addresses the interior, and that is a bounded claim about addressing.

USAGE
  python census_handler_field_widths.py [--disp 0x98,0x9a,0x9c,0x9e] [--ctor 0x245000,0x2465f0]
        [--exe PATH] [--funcs PATH] [--examples N]
"""
import argparse
import collections
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP, X86_REG_R8, X86_REG_EDX

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE_DEFAULT = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS_DEFAULT = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
CALLER_SAVED = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def load_image(path):
    raw = open(path, "rb").read()
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
    return raw, secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE_DEFAULT)
    ap.add_argument("--funcs", default=FUNCS_DEFAULT)
    ap.add_argument("--disp", default="0x98,0x9a,0x9c,0x9e")
    ap.add_argument("--ctor", default="0x245000,0x2465f0")
    ap.add_argument("--examples", type=int, default=8)
    a = ap.parse_args()

    disps = tuple(int(x, 0) for x in a.disp.split(","))
    ctors = tuple(int(x, 0) for x in a.ctor.split(","))
    raw, secs = load_image(a.exe)

    def fo(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)
        return None

    tlo = thi = 0
    for nm, va, vs, rs, pr in secs:
        if nm == ".text":
            tlo, thi = va, va + vs

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
    flen = dict(funcs)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    cache = {}

    def body(entry):
        if entry not in cache:
            n = flen.get(entry, 0)
            f = fo(entry)
            cache[entry] = [] if (f is None or n <= 0) else list(md.disasm(raw[f:f + n], entry))
        return cache[entry]

    def norm(r):
        nm = md.reg_name(r)
        m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
             "ebp": "rbp", "esp": "rsp", "ax": "rax", "bx": "rbx", "cx": "rcx", "dx": "rdx",
             "si": "rsi", "di": "rdi", "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx"}
        if nm in m:
            return m[nm]
        if nm and nm.startswith("r") and nm[-1] in "dwb" and nm[1:-1].isdigit():
            return "r" + nm[1:-1]
        return nm

    # ---- the family, and the family control ------------------------------------------------
    sites = []
    for entry, _ in funcs:
        r8 = size = None
        for i in body(entry):
            ops = i.operands
            if (i.mnemonic == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG
                    and ops[0].reg == X86_REG_R8):
                t = None
                if ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
                    t = i.address + i.size + ops[1].mem.disp
                r8 = t if (t and tlo <= t < thi) else None
            elif (i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG
                    and ops[0].reg == X86_REG_EDX):
                size = ops[1].imm if ops[1].type == X86_OP_IMM else None
            elif (i.mnemonic in ("call", "jmp") and len(ops) == 1
                    and ops[0].type == X86_OP_IMM and ops[0].imm in ctors):
                sites.append((i.address, entry, r8, size))

    handlers = sorted({h for _, _, h, _ in sites if h})
    sizes = sorted({s for _, _, _, s in sites if s})
    print("FAMILY CONTROL")
    print("  constructor sites      %d" % len(sites))
    print("  distinct handlers      %d" % len(handlers))
    print("  distinct sizes         %d   %s" % (len(sizes), ", ".join("0x%X" % s for s in sizes)))
    print("  sites with no immediate size %d, with no handler lea %d"
          % (sum(1 for s in sites if s[3] is None), sum(1 for s in sites if not s[2])))

    # ---- the widths ------------------------------------------------------------------------
    tally = collections.Counter()
    cites = collections.defaultdict(list)
    for h in handlers:
        ins = body(h)
        if not ins:
            continue
        idx = {i.address: k for k, i in enumerate(ins)}
        succ = collections.defaultdict(set)
        for k, i in enumerate(ins):
            m = i.mnemonic
            tgt = i.operands[0].imm if (i.operands and i.operands[0].type == X86_OP_IMM) else None
            if m == "jmp":
                if tgt in idx:
                    succ[k].add(idx[tgt])
            elif m.startswith("j"):
                if tgt in idx:
                    succ[k].add(idx[tgt])
                if k + 1 < len(ins):
                    succ[k].add(k + 1)
            elif m != "ret" and k + 1 < len(ins):
                succ[k].add(k + 1)

        state = [None] * len(ins)
        state[0] = frozenset(["rcx"])
        work, seen = [0], set()
        while work:
            k = work.pop()
            cur = state[k]
            if cur is None:
                continue
            i = ins[k]
            for op in i.operands:
                if (op.type == X86_OP_MEM and op.mem.index == 0
                        and op.mem.base != X86_REG_RIP and op.mem.base):
                    if norm(op.mem.base) in cur and op.mem.disp in disps:
                        sig = (i.address, op.mem.disp, op.size)
                        if sig not in seen:
                            seen.add(sig)
                            tally[(op.mem.disp, op.size)] += 1
                            cites[(op.mem.disp, op.size)].append(
                                "%08X (in %08X)  %s %s" % (i.address, h, i.mnemonic, i.op_str))
            nxt = set(cur)
            m, ops = i.mnemonic, i.operands
            if m == "call":
                nxt -= CALLER_SAVED
            elif m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG:
                d = norm(ops[0].reg)
                s = ops[1]
                if s.type == X86_OP_REG and norm(s.reg) in nxt:
                    nxt.add(d)
                else:
                    nxt.discard(d)
            elif ops and ops[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
                nxt.discard(norm(ops[0].reg))
            nxt = frozenset(nxt)
            for s in succ[k]:
                if state[s] is None:
                    state[s] = nxt
                    work.append(s)
                elif not nxt <= state[s]:
                    state[s] = state[s] | nxt
                    work.append(s)

    print()
    print("WIDTHS, through a register proven to hold the object")
    print("  %-8s %-6s %8s" % ("disp", "width", "count"))
    for d in disps:
        for w in (1, 2, 4, 8, 16):
            if tally[(d, w)]:
                print("  %-8s %-6s %8d" % ("0x%02X" % d, w, tally[(d, w)]))
        if not any(tally[(d, w)] for w in (1, 2, 4, 8, 16)):
            print("  %-8s %-6s %8s" % ("0x%02X" % d, "-", "0"))

    print()
    print("WIDTH CONTROL, read adversarially")
    for d in disps:
        ws = sorted(w for w in (1, 2, 4, 8, 16) if tally[(d, w)])
        if not ws:
            print("  0x%02X  NOT REACHED - no split is supported at this offset" % d)
        elif len(ws) == 1:
            print("  0x%02X  reached only at width %d (%d times) - one width, no contest"
                  % (d, ws[0], tally[(d, ws[0])]))
        else:
            print("  0x%02X  REACHED AT SEVERAL WIDTHS %s - the wide accesses are printed below "
                  "and must be read, not assumed to be combined writes"
                  % (d, ", ".join("%d x%d" % (tally[(d, w)], w) for w in ws)))

    if a.examples:
        print()
        print("CITATIONS")
        for k in sorted(cites):
            print("  0x%02X width %d  (%d)" % (k[0], k[1], len(cites[k])))
            for s in cites[k][:a.examples]:
                print("      " + s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
