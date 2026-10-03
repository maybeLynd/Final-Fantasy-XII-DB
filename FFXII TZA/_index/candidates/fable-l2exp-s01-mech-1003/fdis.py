"""dis.py - FABLE scratch: print a .pdata function (or [start,end)) with rip targets resolved and .rdata strings peeked."""
import sys
from rawref import Img, sec
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

img = Img.load()
rd = sec(img, ".rdata")
dt = sec(img, ".data")


def peek(t):
    try:
        if rd[0] <= t < rd[0] + rd[1]:
            s = img.read(t, 48)
            z = s.split(b"\0")[0]
            if len(z) >= 3 and all(32 <= c < 127 for c in z):
                return "'%s'" % z.decode()
            return "u64=%X" % img.u64(t)
        if dt[0] <= t < dt[0] + dt[1]:
            if t - dt[0] < dt[3]:
                return "data u32=%X" % img.u32(t)
            return "data (zero-init)"
    except Exception:
        pass
    return ""


def dump(s, e):
    for ci in img.cs.disasm(img.read(s, e - s), s):
        extra = ""
        for op in ci.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = ci.address + ci.size + op.mem.disp
                extra = "  ; -> %08X %s" % (t, peek(t))
        print("%08X  %-24s %s %s%s" % (ci.address, ci.bytes.hex(), ci.mnemonic, ci.op_str, extra))


for a in sys.argv[1:]:
    if ":" in a:
        s, e = [int(x, 16) for x in a.split(":")]
    else:
        s, e = img.pdata(int(a, 16))
    print("==== %08X..%08X (%d B)" % (s, e, e - s))
    dump(s, e)
