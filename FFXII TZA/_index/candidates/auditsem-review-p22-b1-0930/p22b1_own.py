"""SWE2-AUDIT-SEM P22-B1 check (own code): the bodies and edges FRONTIER's six crossing paragraphs cite.
A  0036A190 whole, and the head of its tail-jump target
B  every direct caller of 0036A190 (rel32 call/jmp), with containing .pdata function, so the named Resource / World /
   WorldAreaField bodies can be checked for membership; the 0032E7C0 window 0032E800-0032E80E
E  0053DD10 whole; every direct caller's containing function; the 00341840 window 00341860-00341880
F  00203170 whole; the 16-byte constants it loads (first as floats); the 00356160 call site
G  00247510 whole; its callers' containing functions; the windows 00581D41-00581D52, 00582B0B-00582B19,
   00582A31-00582A37; 001EDEC0 whole."""
import struct, bisect
import img

t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
pd = [s for s in img.secs if s[0].startswith(".pdata")][0]
funcs = []
for i in range(0, pd[2], 12):
    b, e, u = struct.unpack_from("<III", img.raw, pd[3] + i)
    if b:
        funcs.append((img.BASE + b, img.BASE + e, img.BASE + u))
funcs.sort()
fs = [f[0] for f in funcs]
def root(a):
    """the .pdata chain root of the fragment containing a (UNW_FLAG_CHAININFO follows to the parent)"""
    k = bisect.bisect_right(fs, a) - 1
    if k < 0 or not (funcs[k][0] <= a < funcs[k][1]):
        return None
    b, e, u = funcs[k]
    for _ in range(16):
        uo = img.off(u)
        flags = img.raw[uo] >> 3
        if not flags & 4:
            return b
        n = img.raw[uo + 2]
        co = uo + 4 + 2 * (n + (n & 1))
        pb, pe, pu = struct.unpack_from("<III", img.raw, co)
        b, u = img.BASE + pb, img.BASE + pu
    return b
def rel_sites(t):
    return [(va0 + i, "call" if text[i] == 0xE8 else "jmp") for i in range(len(text) - 5)
            if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t]
def d(lo, hi, title):
    print("==", title)
    for back in range(0, 16):
        xs = list(img.md.disasm(img.rd(lo - back, hi - lo + back + 16), lo - back))
        if any(x.address == lo for x in xs):
            break
    for x in xs:
        if lo <= x.address < hi:
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
def callers(t, name):
    s = rel_sites(t)
    by = {}
    for a, k in s:
        r = root(a)
        by.setdefault(r, []).append("%08X%s" % (a, "" if k == "call" else "(jmp)"))
    print("== callers of %s %08X: %d sites in %d functions; qwords %d" % (
        name, t, len(s), len(by), img.raw.count(struct.pack("<Q", t))))
    for r in sorted(by, key=lambda v: v or 0):
        print("   %s  %s" % ("%08X" % r if r else "(no pdata)", " ".join(by[r])))
    return by

d(0x0036A190, 0x0036A1A0, "A 0036A190")
x = list(img.md.disasm(img.rd(0x0036A190, 16), 0x0036A190))
tgt = int([i for i in x if i.mnemonic == "jmp"][0].op_str, 16)
d(tgt, tgt + 0x60, "A tail target %08X (head)" % tgt)
callers(0x0036A190, "0036A190")
d(0x0032E800, 0x0032E812, "B 0032E7C0 window")
d(0x00378580, 0x0037858B, "C 00378540 call")
d(0x002687C0, 0x002687CC, "D 00268750 call")
d(0x0053DD10, 0x0053DD16, "E 0053DD10")
callers(0x0053DD10, "0053DD10")
d(0x00341860, 0x00341880, "E 00341840 gate")
d(0x00203170, 0x002031B0, "F 00203170")
ins = list(img.md.disasm(img.rd(0x00203170, 0x40), 0x00203170))
for i in ins:
    if "rip" in i.op_str:
        disp = int(i.op_str.split("rip + ")[1].split("]")[0], 16)
        a = i.address + i.size + disp
        print("   const %08X: %s" % (a, struct.unpack("<4f", img.rd(a, 16))))
callers(0x00203170, "00203170")
d(0x00247510, 0x00247570, "G 00247510")
callers(0x00247510, "00247510")
d(0x00581D41, 0x00581D57, "G 00581B70 post")
d(0x00582B0B, 0x00582B1E, "G 00582860 post")
d(0x00582A31, 0x00582A3C, "G 00582860 -> 001EDEC0")
d(0x001EDEC0, 0x001EDEE0, "G 001EDEC0")
def dfrom(start, lo, hi, title):
    print("==", title)
    for x in img.md.disasm(img.rd(start, hi - start + 16), start):
        if lo <= x.address < hi:
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
dfrom(0x00341840, 0x00341860, 0x00341890, "E 00341840 gate, decoded from the function entry")
dfrom(0x0036A1A0, 0x0036A1FD, 0x0036A260, "A tail target continued")
