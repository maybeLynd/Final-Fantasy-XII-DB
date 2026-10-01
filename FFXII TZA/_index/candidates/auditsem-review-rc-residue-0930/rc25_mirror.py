"""SWE2-AUDIT-SEM RC-25 attack, part 3 (own code): the party block is static - 002EF640 returns 02164280 and 00233C2A
adds 0x4E68C, so *(02EBF190) = 021B290C. 002EF4A0 copies 0xC0 x 0x80 = 0x6000 bytes from 02166480 over 021B290C..
(covering all 0x28 pages, so every page's byte +4). This script lists:
  1. every direct call/jmp to 002EF4A0 (who restores the block from the mirror) and the reverse copier if any;
  2. every rip-relative reference into the mirror 02166480..0216C480 and into the live block 021B290C..021B8904;
  3. the mirror's byte +4 of each page in the file image (zero-fill BSS if not file-backed).
Rip decoding takes the LONGEST instruction ending at the displacement (a REX-prefixed op must not be shadowed by its
prefix-less tail).
"""
import struct
import img

t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0

def direct(target):
    out = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == target:
            out.append((va0 + i, "call" if text[i] == 0xE8 else "jmp"))
    return out

def riprefs(ranges):
    hits = set()
    for i in range(len(text) - 4):
        d = struct.unpack_from("<i", text, i)[0]
        for tail in (0, 1, 2, 4):
            tgt = va0 + i + 4 + tail + d
            for lo, hi, tag in ranges:
                if lo <= tgt < hi:
                    hits.add((i, tail, tgt, tag))
    found = {}
    for i, tail, tgt, tag in sorted(hits):
        for back in range(11, 0, -1):
            s = i - back
            if s < 0:
                continue
            x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
            if x and x.size == back + 4 + tail and "rip" in x.op_str:
                found[x.address] = (x.mnemonic, x.op_str, tgt, tag)
                break
    return found

def owner(a):
    for n, rva, vsz, rpp, rs in img.secs:
        if n == ".pdata":
            for k in range(0, vsz, 12):
                b, e, u = struct.unpack_from("<III", img.raw, rpp + k)
                if b + img.BASE <= a < e + img.BASE:
                    return b + img.BASE
    return None

print("direct sites into 002EF4A0:", ["%08X %s in %s" % (a, m, "%08X" % owner(a) if owner(a) else "?") for a, m in direct(0x002EF4A0)])
R = riprefs([(0x02166480, 0x0216C480, "MIRROR"), (0x021B290C, 0x021B290C + 0x6000, "LIVE")])
for a in sorted(R):
    m, o, t, tag = R[a]
    fn = owner(a)
    print("  %-6s %08X %s %s  -> %08X (+%#x)  in %s" % (tag, a, m, o, t, t - (0x02166480 if tag == "MIRROR" else 0x021B290C),
                                                   "%08X" % fn if fn else "?"))
print("refs:", len(R))
o = img.off(0x02166480)
print("mirror file-backed:", o is not None)
if o is not None:
    vals = [img.raw[o + 8 + k * 0x1C8 + 4] for k in range(0x28)]
    print("mirror page byte +4 in the file image:", vals)
