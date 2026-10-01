"""SWE2-AUDIT-SEM RC-8 attack, part 2 (own code): 0015CC00 stores the singleton pointer (001F0850's return) into a
second global, 01F812C8. List every rip-relative reference to 01F812C8 (longest decode) with its owning function
(.pdata chain root), then intersect those functions (and their direct callees) with the image-wide covering-store
sweep for +0x13C (cover_13C.out, any width, own sweep)."""
import struct, re
import img
ALIAS = 0x01F812C8
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
PD = []
for n, rva, vsz, rpp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rpp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE, u))
def root(a):
    for b, e, u in PD:
        if b <= a < e:
            uo = img.off(u + img.BASE)
            while uo is not None and (img.raw[uo] >> 3) & 4:
                cnt = img.raw[uo + 2]
                co = uo + 4 + ((cnt + 1) & ~1) * 2
                cb, ce, cu = struct.unpack_from("<III", img.raw, co)
                b = cb + img.BASE
                uo = img.off(cu + img.BASE)
            return b
    return None
def frags(r):
    return [(b, e) for b, e, u in PD if root(b) == r]
refs = {}
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 2, 4):
        if va0 + i + 4 + tail + d == ALIAS:
            for back in range(11, 0, -1):
                s = i - back
                x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
                if x and x.size == back + 4 + tail and "rip" in x.op_str:
                    refs[x.address] = x
                    break
fns = {}
for a, x in sorted(refs.items()):
    r = root(a)
    fns.setdefault(r, []).append("%08X %s %s" % (a, x.mnemonic, x.op_str))
print("rip refs to 01F812C8: %d in %d functions" % (len(refs), len(fns)))
for r in sorted(fns, key=lambda v: v or 0):
    print("  %s: %s" % ("%08X" % r if r else "?", " | ".join(fns[r])))
stores = []
for line in open("cover_13C.out"):
    m = re.match(r"([0-9A-F]{8}) ", line)
    if m:
        stores.append((int(m.group(1), 16), line.strip()))
print("covering +0x13C stores image-wide:", len(stores))
hit = [(a, l) for a, l in stores if root(a) in fns]
print("covering stores inside the alias-referencing functions:", hit or "none")
# one hop: direct callees of the alias functions
callees = set()
for r in fns:
    for b, e in frags(r):
        for x in img.md.disasm(img.rd(b, e - b), b):
            if x.mnemonic in ("call", "jmp") and re.fullmatch(r"0x[0-9a-f]+", x.op_str):
                callees.add(int(x.op_str, 16))
hit1 = [(a, l) for a, l in stores if root(a) in callees]
print("direct callees of those functions: %d; covering stores inside them:" % len(callees))
for a, l in hit1:
    print("   ", l, " in %08X" % root(a))
