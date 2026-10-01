"""SWE2-AUDIT-SEM RC-36 check (own code).
K  every rel32 route into the draw-row emitter 003C2320 (and qwords naming it), with each call site's r8 (the kind the
   emitter tests at 003C23C2) and rdx, read back to the producer of the kind.
W  in 003C2320: every write to r15 (the point register read at 003C25BD); it must be only 003C2354 (mov r15, rdx) and
   the epilogue restore.
B  every write into the kind out-slot of 003BF430 (all immediate stores of 0/1/2 into memory through an argument
   register or an out-pointer in 003BF430's body), to see which kinds reach the emitter's non-zero arm.
D  the label pass 004044D0: the instructions from its kind test to the draw call at 004046AB, printed.
C  the copy 00402C30: the lines that read the row's +0x10 / +2 fields."""
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
        funcs.append((img.BASE + b, img.BASE + e))
funcs.sort()
fs = [f[0] for f in funcs]
def fn(a):
    k = bisect.bisect_right(fs, a) - 1
    return funcs[k] if k >= 0 and funcs[k][0] <= a < funcs[k][1] else (None, None)
def rel_sites(t):
    out = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t:
            out.append((va0 + i, "call" if text[i] == 0xE8 else "jmp"))
    return out
def ctx(a, before, after):
    for back in range(0, 16):
        xs = list(img.md.disasm(img.rd(a - before - back, before + after + back), a - before - back))
        if any(x.address == a for x in xs):
            return [x for x in xs if x.address >= a - before]
    return []
def body(f):
    s, e = fn(f)
    if s is None:
        s, e = f, f + 0x400
    return list(img.md.disasm(img.rd(s, e - s), s))

E = 0x003C2320
print("K qwords naming 003C2320:", img.raw.count(struct.pack("<Q", E)))
for a, k in rel_sites(E):
    print("K site %08X %s in %08X" % (a, k, fn(a)[0] or 0))
    for x in ctx(a, 0x50, 6):
        if any(r in x.op_str.split(",")[0] for r in ("r8", "rdx", "edx")) or x.address == a:
            print("     %08X %s %s" % (x.address, x.mnemonic, x.op_str))

print("W writes to r15 in 003C2320:")
for x in list(img.md.disasm(img.rd(E, 0x3A0), E)):
    if x.op_str.split(",")[0].strip() in ("r15", "r15d", "r15w") and x.mnemonic not in ("cmp", "test", "push"):
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    if x.mnemonic == "ret":
        break

print("B immediate stores in 003BF430 (kind out-slot candidates):")
for x in body(0x003BF430):
    if x.mnemonic == "mov" and "dword ptr [" in x.op_str and x.op_str.split(",")[-1].strip() in ("0", "1", "2", "3") \
            and "rsp" not in x.op_str:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    if x.mnemonic == "mov" and "dword ptr [" in x.op_str.split(",")[0] and "rsp" not in x.op_str:
        pass

print("D 004044D0 around the kind test and the draw at 004046AB:")
for x in body(0x004044D0):
    if 0x00404600 <= x.address <= 0x004046B0:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))

print("C 00402C30 reads of +0x10 / +2:")
for x in body(0x00402C30):
    if "+ 0x10]" in x.op_str or "+ 2]" in x.op_str or x.mnemonic == "call":
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
