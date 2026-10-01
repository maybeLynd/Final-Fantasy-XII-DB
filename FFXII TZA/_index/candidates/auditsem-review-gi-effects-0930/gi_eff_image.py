"""SWE2-AUDIT-SEM GI-8..11 image checks (own code).
E1 (correction 2, 'step 002F3BC0 is the birth'): every direct call/jmp to 002F3BC0 and 002F3910 (the update) with the
   owning .pdata function, so the call sites can be read (birth vs per-frame).
E2 (correction 3): is 00454890 a .pdata function start, and is it an instruction boundary in its containing fragment?
   Is 00452C70 a .pdata function start? Every rel32 reference / qword pointing at either.
E3 (corrections 4): 0054C6B0 / 0054E040 / 0054C440 / 0054DD30 - their direct callers.
E4 (correction 5): 0045F600 - direct callers."""
import struct, bisect
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
PD = []
for n, rva, vsz, rpp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rpp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE))
PD.sort()
S = [p[0] for p in PD]
def frag(a):
    k = bisect.bisect_right(S, a) - 1
    return PD[k] if k >= 0 and PD[k][0] <= a < PD[k][1] else None
IDX = {}
for i in range(len(text) - 6):
    b = text[i]
    if b in (0xE8, 0xE9):
        IDX.setdefault(va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0], []).append((va0 + i, "call" if b == 0xE8 else "jmp"))
def sites(t):
    return ["%08X %s in %s" % (a, k, "%08X" % frag(a)[0] if frag(a) else "?") for a, k in IDX.get(t, [])]
print("E1 002F3BC0 sites:", sites(0x002F3BC0))
print("E1 002F3910 sites:", sites(0x002F3910))
for a in (0x00454890, 0x00452C70):
    f = frag(a)
    inb = None
    if f:
        inb = any(x.address == a for x in img.md.disasm(img.rd(f[0], a - f[0] + 16), f[0]))
    qw = img.raw.count(struct.pack("<Q", a))
    print("E2 %08X: .pdata start %s, containing fragment %s, instruction boundary %s, rel32 sites %s, qwords %d" % (
        a, a in S, "%08X-%08X" % f if f else None, inb, sites(a), qw))
for a in (0x0054C6B0, 0x0054E040, 0x0054C440, 0x0054DD30, 0x0045F600, 0x0052E270, 0x0052F400):
    print("E3/E4 %08X sites: %s" % (a, sites(a)))
print("E1b the one 002F3BC0 caller, 00441DE0..00441E80 (from its chunk start), and who reaches it")
import re
for x in img.md.disasm(img.rd(0x00441E5D, 0x30), 0x00441E5D):
    if x.address > 0x00441E80:
        break
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
f = frag(0x00441E5D)
print("   fragment", "%08X-%08X" % f if f else None, "sites into fragment start:", sites(f[0]) if f else None)
