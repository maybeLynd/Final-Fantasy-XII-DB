#!/usr/bin/env python3
"""fn_audit.py - check two kinds of claim about a function body MECHANICALLY.

The two claims this exists for
------------------------------
Documents in this database repeatedly assert things of the form

    "these two functions are identical apart from one instruction"
    "this function never touches <register>"

Both are checkable, and both have already been wrong once: the input name registry's two inserts
were called *byte-identical* and differ in four bytes. Asserting either by eye is exactly the
habit the evidence standard exists to replace.

    --compare A:LEN B:LEN     normalised instruction diff of two bodies
    --touches REG             every instruction that reads or writes a register, implicit included

**Normalisation, and what it deliberately keeps.** Two bodies at different addresses cannot be
compared byte for byte: every RIP-relative displacement and every relative branch differs by
construction. So each instruction is reduced to `mnemonic` plus its operand text with

  * RIP-relative operands replaced by their **resolved absolute target** -- so two functions that
    reference *different* globals still differ, which is the whole point;
  * relative branch targets replaced by their **offset from the function's own entry** -- so the
    same control flow at a different address compares equal.

Nothing else is normalised. Register names, immediates and operand sizes are all significant.

**Register touching uses capstone's `regs_access`**, which reports implicit reads and writes as
well as explicit operands -- so `xor r8d, r8d`, `push r8`, and a `div` that implicitly writes
`rdx` are all caught. Reading the operand text with a regular expression would miss the implicit
ones, and that is the failure this tool is written to avoid.
"""
import argparse
import sys

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP
except ImportError:
    sys.stderr.write("fn_audit: needs capstone (pip install capstone)\n")
    raise SystemExit(2)

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from disasm_fn import Image, DEFAULT_EXE

BRANCH = set("jmp je jne jz jnz jl jle jg jge jb jbe ja jae js jns jo jno jp jnp "
             "loop loope loopne call".split())


def normalise(img, va, length):
    """-> list of (offset, text). See the docstring for what is and is not normalised."""
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    code = img.read(va, length)
    if code is None or len(code) < length:
        raise SystemExit("cannot read %d bytes at %08X" % (length, va))
    out = []
    for ins in md.disasm(code, va):
        text = ins.op_str
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.value.mem.base == X86_REG_RIP:
                tgt = ins.address + ins.size + op.value.mem.disp
                # the resolved target, so two bodies touching DIFFERENT globals differ
                text = text.replace("rip + 0x%x" % op.value.mem.disp, "ABS:%08X" % tgt)
                text = text.replace("rip - 0x%x" % (-op.value.mem.disp), "ABS:%08X" % tgt)
        if ins.mnemonic in BRANCH and ins.op_str.startswith("0x"):
            tgt = int(ins.op_str, 16)
            text = "+%d" % (tgt - va) if va <= tgt < va + length else "OUT:%08X" % tgt
        out.append((ins.address - va, "%s %s" % (ins.mnemonic, text)))
    return out


def cmd_compare(img, a, alen, b, blen):
    x, y = normalise(img, a, alen), normalise(img, b, blen)
    print("%08X : %d instruction(s), %d bytes" % (a, len(x), alen))
    print("%08X : %d instruction(s), %d bytes" % (b, len(y), blen))
    if len(x) != len(y):
        print()
        print("**DIFFERENT INSTRUCTION COUNTS** - they are not the same shape, and a"
              " position-by-position diff below would be misleading")
    n = min(len(x), len(y))
    diff = [i for i in range(n) if x[i][1] != y[i][1]]
    print("positions compared        : %d" % n)
    print("positions differing       : %d" % len(diff))
    for i in diff:
        print("  [%2d]  +%-3d %-40s |  +%-3d %s" % (i, x[i][0], x[i][1], y[i][0], y[i][1]))
    if len(x) != len(y):
        longer, name = (x, "%08X" % a) if len(x) > len(y) else (y, "%08X" % b)
        print("  ...%s has %d more instruction(s):" % (name, abs(len(x) - len(y))))
        for off, t in longer[n:]:
            print("        +%-3d %s" % (off, t))
    return 0 if (len(x) == len(y)) else 1


def cmd_touches(img, va, length, reg):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    code = img.read(va, length)
    if code is None or len(code) < length:
        raise SystemExit("cannot read %d bytes at %08X" % (length, va))
    want = reg.lower()
    # every width of the same architectural register counts as touching it
    fam = {want}
    if want.startswith("r") and want[1:].isdigit():
        fam |= {want + s for s in ("d", "w", "b")}
    elif want in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"):
        base = want[1:]
        fam |= {"e" + base, base, base[0] + "l" if len(base) == 2 else base}
    hits = []
    total = 0
    for ins in md.disasm(code, va):
        total += 1
        try:
            regs_read, regs_write = ins.regs_access()
        except Exception:
            regs_read, regs_write = (), ()
        names = {ins.reg_name(r).lower() for r in tuple(regs_read) + tuple(regs_write)
                 if ins.reg_name(r)}
        if names & fam:
            hits.append((ins.address - va, "%s %s" % (ins.mnemonic, ins.op_str),
                         sorted(names & fam)))
    print("%08X : %d instruction(s) over %d bytes" % (va, total, length))
    print("register family checked   : %s" % ", ".join(sorted(fam)))
    print("instructions touching it  : %d" % len(hits))
    for off, text, which in hits:
        print("  +%-3d %-42s %s" % (off, text, ",".join(which)))
    if not hits:
        print()
        print("NOT TOUCHED - and this is capstone's regs_access, which reports IMPLICIT reads and")
        print("writes too, so a `push`, an `xor r8d,r8d` or a `div`'s implicit rdx would all show.")
    return 0


def addr_len(s):
    a, _, l = s.partition(":")
    if not l:
        raise SystemExit("give ADDR:LENGTH, e.g. 0026B5A0:117")
    return int(a, 16), int(l, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--compare", nargs=2, metavar="ADDR:LEN")
    ap.add_argument("--fn", metavar="ADDR:LEN")
    ap.add_argument("--touches", metavar="REG")
    a = ap.parse_args()
    img = Image(a.exe)
    if a.compare:
        (x, xl), (y, yl) = addr_len(a.compare[0]), addr_len(a.compare[1])
        return cmd_compare(img, x, xl, y, yl)
    if a.fn and a.touches:
        va, ln = addr_len(a.fn)
        return cmd_touches(img, va, ln, a.touches)
    ap.error("give --compare A:LEN B:LEN, or --fn A:LEN --touches REG")


if __name__ == "__main__":
    sys.exit(main())
