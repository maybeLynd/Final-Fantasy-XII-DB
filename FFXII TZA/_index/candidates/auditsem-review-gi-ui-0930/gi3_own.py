"""SWE2-AUDIT-SEM GI-3 spot check: every instruction in .text carrying the immediate 0x11D (message 285) in a
mov/cmp/sub form, with its .pdata owner, to see who posts 285 (the shared boxes) and who compares it (openers);
plus 00566F4E (GI-1's create-record +0x14 read)."""
import struct, re, bisect
import img
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE))
PD.sort(); S = [p[0] for p in PD]
def own(a):
    k = bisect.bisect_right(S, a) - 1
    return PD[k][0] if k >= 0 and PD[k][0] <= a < PD[k][1] else None
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
hits = {}
pat = struct.pack("<I", 0x11D)
p = text.find(pat)
while p >= 0:
    for back in range(1, 11):
        x = next(img.md.disasm(text[p - back:p - back + 16], va0 + p - back), None)
        if x and x.address + x.size == va0 + p + 4 and re.search(r", 0x11d$", x.op_str):
            f = own(x.address)
            if f:
                hits.setdefault(f, []).append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
            break
    p = text.find(pat, p + 1)
for f in sorted(hits):
    print("%08X: %s" % (f, " | ".join(hits[f][:4])))
print("functions:", len(hits))
x = next(img.md.disasm(img.rd(0x00566F4E, 16), 0x00566F4E))
print("00566F4E:", x.mnemonic, x.op_str, "owner", "%08X" % own(0x00566F4E))
