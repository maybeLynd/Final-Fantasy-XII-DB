"""closure.py - direct call/tail-jump closure of the EFX parse 003EDAD0, and which bodies in it store 02F97340
(ORACLE, 2026-09-30, RC-11). Direct rel32 E8/E9 targets only; indirect calls are listed as the blind spot.
Bodies without a .pdata entry (leaf functions) are decoded linearly to their first ret/int3 run."""
import img
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
WRITERS = {0x0024B3A0, 0x0024D050, 0x0024D540, 0x0024ED80, 0x0024F410, 0x0026FB90, 0x003B3480, 0x003B3550, 0x003B3CA0,
           0x003B8260, 0x003B8670, 0x003BA1F0}


def body(f):
    r = img.owner(f)
    if r == f:
        return img.fn_ins(f)
    out = []
    for x in img.dis(f, 0x400):
        out.append(x)
        if x.mnemonic in ("ret", "int3"):
            break
    return out


def closure(root):
    seen, todo, ind, stores = set(), [root], [], []
    while todo:
        f = todo.pop()
        if f in seen:
            continue
        seen.add(f)
        for x in body(f):
            if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == X86_OP_IMM:
                t = x.operands[0].imm
                if x.mnemonic == "jmp" and img.owner(t) == img.owner(f) and img.owner(f) is not None:
                    continue
                if x.mnemonic == "jmp" and img.owner(t) is None and f <= t < f + 0x400:
                    continue
                todo.append(t)
            elif x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type != X86_OP_IMM:
                ind.append((f, x.address, x.op_str))
            m = img.ripmem(x)
            if m == 0x02F97340 and x.operands[0].type == X86_OP_MEM and x.mnemonic == "mov":
                stores.append((f, x.address, x.op_str))
    return seen, ind, stores


if __name__ == "__main__":
    s, ind, st = closure(0x003EDAD0)
    print("closure of 003EDAD0: %d bodies" % len(s))
    print("control: 00504350 in closure: %s" % ("PASS" if 0x00504350 in s else "FAIL"))
    print("known 02F97340 writer bodies in closure: %s" % sorted("%08X" % w for w in WRITERS & s))
    print("stores to 02F97340 inside closure bodies: %d" % len(st))
    for f, a, o in st:
        print("  %08X %08X %s" % (f, a, o))
    print("indirect calls/jumps in closure: %d" % len(ind))
    for f, a, o in ind:
        print("  %08X %08X %s" % (f, a, o))
