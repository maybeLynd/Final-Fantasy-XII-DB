"""SWE2-AUDIT-SEM RC-35 check (own code).
R  003BE680 read to its returns (122 B).
X  every route into 003BE680 image-wide: rel32 call/jmp, qword, and jmp-thunks; each site's context.
G  image-wide: every rip-relative reference to the widget singleton 02B457E0 (longest decode ending on the disp32),
   grouped by .pdata function; for each function, whether it also loads [reg+0xE0] (the location file) and whether it
   forms the C end (a byte [x+2] read multiplied by 20 / 0x14). This widens the producer's 3-hop reach to the whole
   image for the one handle every reader must start from.
C  control: the three known walkers 003BFF20 / 003C1070 / 003C0740 must be among the functions G reaches (directly or
   via their callers' singleton load)."""
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

def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address >= hi:
            break
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))

print("R 003BE680")
show(0x003BE680, 0x003BE680 + 122)

def rel_sites(t):
    out = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t:
            out.append(va0 + i)
    return out
T = 0x003BE680
s = rel_sites(T)
print("X rel32 sites:", ["%08X" % a for a in s])
print("X qwords naming it:", img.raw.count(struct.pack("<Q", T)))
for a in s:
    f = fn(a)
    print("X site %08X in %s" % (a, "%08X" % f[0] if f[0] else "?"))
    lo = a - 0x30
    for back in range(0, 16):
        xs = list(img.md.disasm(img.rd(lo - back, 0x70 + back), lo - back))
        if any(x.address == a for x in xs):
            break
    for x in xs:
        if a - 0x30 <= x.address <= a + 0x38:
            print("     %08X %s %s" % (x.address, x.mnemonic, x.op_str))

G = 0x02B457E0
refs = []
for i in range(len(text) - 4):
    va_end = va0 + i + 4
    d = struct.unpack_from("<i", text, i)[0]
    if not (0 <= G - (va0 + i + 4 + d) <= 4):
        continue
    for L in range(11, 3, -1):
        st = i + 4 - L
        if st < 0:
            continue
        xs = list(img.md.disasm(text[st:st + L], va0 + st, 1))
        if not xs or xs[0].size != L:
            continue
        x = xs[0]
        if "rip" in x.op_str:
            # the disp32 must be at i: check target
            tail = x.size - (va0 + i - x.address) - 4
            if va0 + i + 4 + tail + d == G:
                refs.append(x.address)
            break
refs = sorted(set(refs))
byf = {}
for a in refs:
    f = fn(a)[0]
    byf.setdefault(f, []).append(a)
print("G rip references to 02B457E0:", len(refs), "in", len(byf), "functions")
cands = []
for f, sites in sorted(byf.items(), key=lambda kv: kv[0] or 0):
    if f is None:
        print("G  (no pdata)", ["%08X" % a for a in sites])
        continue
    e = fn(f)[1]
    xs = list(img.md.disasm(img.rd(f, e - f), f))
    e0 = any("+ 0xe0]" in x.op_str for x in xs)
    by2 = any(x.mnemonic.startswith("movzx") and "byte ptr" in x.op_str and "+ 2]" in x.op_str for x in xs)
    m20 = any((x.mnemonic == "imul" and x.op_str.endswith("0x14")) or
              (x.mnemonic == "lea" and "*4]" in x.op_str) for x in xs)
    flag = e0 and by2 and m20
    if flag:
        cands.append(f)
    print("G  %08X sites=%d e0=%d byte+2=%d x20=%d %s" % (f, len(sites), e0, by2, m20, "CAND" if flag else ""))
print("G candidates (e0 & byte+2 & x20):", ["%08X" % c for c in cands])
