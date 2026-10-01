"""SWE2-AUDIT-SEM DEFEAT-CROSSING check (own code): the two edges FRONTIER's pass-22 section cites.
A  0030C650 around 0030C820-0030C860 (003A1180 with ecx = 7, the -1 test, 002DF220(id, 0x40, 0x7F)); 003A1180 whole;
   whether 0030C650 uses 002DF220's return; the recipient walk's call 003124A3
S  00236780 whole; 00583D60's call to it and 00583F50-00583F78; DR-2's test 00312500-00312520
C  direct callers of 003A1180, 002DF220 and 00236780"""
import struct
import img

t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
def rel_sites(t):
    return ["%08X" % (va0 + i) for i in range(len(text) - 5)
            if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t]
def dfrom(start, lo, hi, title):
    print("==", title)
    for x in img.md.disasm(img.rd(start, hi - start + 16), start):
        if lo <= x.address < hi:
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
        if x.address >= hi:
            break
dfrom(0x0030C650, 0x0030C810, 0x0030C870, "A 0030C650 (decoded from entry)")
dfrom(0x003A1180, 0x003A1180, 0x003A1200, "A 003A1180")
dfrom(0x00312280, 0x00312498, 0x003124AA, "A the walk's call (00312280 decoded from entry)")
dfrom(0x00236780, 0x00236780, 0x002367A0, "S 00236780")
dfrom(0x00583D60, 0x00583D60, 0x00583F80, "S 00583D60 (entry to the header write)")
dfrom(0x00312280, 0x003124F8, 0x00312520, "S DR-2 test")
for f in (0x003A1180, 0x002DF220, 0x00236780):
    s = rel_sites(f)
    print("C callers of %08X: %d %s" % (f, len(s), s[:40]))
dfrom(0x00329210, 0x00329210, 0x00329260, "A 00329210 (takes 002DF220's return at 0030C850-0030C857)")
# the global array 00329210 writes: every rip reference to [ARR, ARR+0x40), with its containing .pdata function
ARR = 0x0032921A + 0x1d6410e
print("== rip references to the 00329210 array %08X..+0x40" % ARR)
pd = [s for s in img.secs if s[0].startswith(".pdata")][0]
fl = sorted((img.BASE + struct.unpack_from("<III", img.raw, pd[3] + i)[0], img.BASE + struct.unpack_from("<III", img.raw, pd[3] + i)[1])
            for i in range(0, pd[2], 12) if struct.unpack_from("<I", img.raw, pd[3] + i)[0])
import bisect
fsb = [f[0] for f in fl]
def fn(a):
    k = bisect.bisect_right(fsb, a) - 1
    return "%08X" % fl[k][0] if k >= 0 and fl[k][0] <= a < fl[k][1] else "(no pdata)"
seen = set()
for i in range(len(text) - 4):
    dd = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 4):
        tgt = va0 + i + 4 + tail + dd
        if ARR <= tgt < ARR + 0x40:
            for L in range(15, 4, -1):
                st = i + 4 + tail - L
                xs = list(img.md.disasm(text[st:st + L], va0 + st, 1))
                if xs and xs[0].size == L and "rip" in xs[0].op_str and xs[0].address not in seen:
                    seen.add(xs[0].address)
                    print("   %08X %s %s  in %s" % (xs[0].address, xs[0].mnemonic, xs[0].op_str, fn(xs[0].address)))
                    break
