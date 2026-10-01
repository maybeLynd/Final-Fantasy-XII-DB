"""SWE2-AUDIT-SEM RC-35 check, part 2 (own code).
L  the 15 singleton references with no .pdata entry (leaf routines): decode forward from 64 bytes before each site to
   the first ret, and apply the same three tests (+0xE0 load, byte [x+2] read, a x20 formation).
P  the two .pdata functions that read byte [x+2] and form x20 without a +0xE0 load (003BCAF0, 003BF520): print
   their byte [x+2] and x20 instructions for reading.
N  the three C/D walkers: every memory read with a negative displacement (a reader stepping back from D onto the
   block), printed."""
import struct
import img

LEAF = [0x003BC2C2, 0x003BD860, 0x003BD890, 0x003BE680, 0x003BF8E0, 0x003C0250, 0x003C0340, 0x003C0890, 0x003C0CC0,
        0x003C0CF0, 0x003C20D0, 0x003C2199, 0x003C21B0, 0x003C21C5, 0x003C2202]

def start_of(a):
    # walk back to the int3/ret padding that precedes the routine
    p = a
    while p > a - 0x400:
        b = img.rd(p - 1, 1)[0]
        if b == 0xCC:
            return p
        p -= 1
    return a - 64

def body(a):
    st = start_of(a)
    out = []
    for x in img.md.disasm(img.rd(st, 0x600), st):
        out.append(x)
        if x.mnemonic in ("ret", "int3") and x.address > a:
            break
        if x.mnemonic == "jmp" and x.address > a and x.op_str.startswith("0x"):
            break
    return st, out

def flags(xs):
    e0 = any("+ 0xe0]" in x.op_str for x in xs)
    by2 = [x for x in xs if x.mnemonic.startswith("movzx") and "byte ptr" in x.op_str and "+ 2]" in x.op_str]
    m20 = [x for x in xs if (x.mnemonic == "imul" and x.op_str.endswith("0x14")) or
           (x.mnemonic == "lea" and "*4]" in x.op_str)]
    return e0, by2, m20

for a in LEAF:
    st, xs = body(a)
    e0, by2, m20 = flags(xs)
    print("L site %08X routine %08X..%08X e0=%d byte+2=%d x20=%d %s" % (
        a, st, xs[-1].address, e0, len(by2), len(m20), "CAND" if (e0 and by2 and m20) else ""))

for f in (0x003BCAF0, 0x003BF520):
    st, xs = body(f + 1)
    e0, by2, m20 = flags(xs)
    print("P %08X" % f)
    for x in by2 + m20:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))

for f, e in ((0x003BFF20, 0x003BFFF0), (0x003C1070, 0x003C12B0), (0x003C0740, 0x003C08B0)):
    xs = list(img.md.disasm(img.rd(f, e - f), f))
    neg = [x for x in xs if "- 0x" in x.op_str and "ptr [" in x.op_str and "rsp" not in x.op_str and "rbp" not in x.op_str]
    print("N %08X negative-displacement memory operands: %d" % (f, len(neg)))
    for x in neg:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
