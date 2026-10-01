"""adump.py - SWE2-AUDIT-SPEC: resolving linear dump over the certified image via arena_ix (2026-09-30).
    python adump.py START END [START END ...]     (START alone: the .pdata range containing START)
rip targets resolved; a disp32 in [0x100000, 0x2A00000) on a non-rip base is annotated as IB+disp (image-base form)."""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arena_ix as X  # noqa: E402
from capstone import CS_OP_MEM
from capstone.x86 import X86_REG_RIP


def peek(va):
    b = X.rd(va, 8)
    if not b or len(b) < 8:
        return "(virtual tail: zero-init)" if b is None else ""
    return "q=%016X" % struct.unpack("<Q", b)[0]


def dump(a, b):
    for i in X.dis(a, b):
        s = "%08X  %-9s %s" % (i.address, i.mnemonic, i.op_str)
        for op in i.operands:
            if op.type == CS_OP_MEM:
                m = op.mem
                if m.base == X86_REG_RIP:
                    t = i.address + i.size + m.disp
                    s += "   ; -> %08X %s" % (t, peek(t))
                elif 0x100000 <= m.disp < 0x2A00000:
                    s += "   ; IB+disp = %08X" % (X.IB + m.disp)
        if i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j"):
            pass
        print(s)


if __name__ == "__main__":
    a = sys.argv[1:]
    k = 0
    while k < len(a):
        s = int(a[k], 16)
        if k + 1 < len(a) and int(a[k + 1], 16) > s and int(a[k + 1], 16) - s < 0x10000:
            e = int(a[k + 1], 16); k += 2
        else:
            e = X.pend(s) or s + 0x200; k += 1
        print("=== %08X..%08X root %s" % (s, e, "%08X" % X.root(s) if X.root(s) else "-"))
        dump(s, e)
