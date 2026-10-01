"""SWE2-AUDIT-SEM BIT46 counterexample hunt, part 3 (own code): composite masks.
The producer's movabs test matched only the two single-bit masks (0x400000000000 / 0xFFFFBFFFFFFFFFFF). A clear can
also come from a wider mask that clears bit 46 together with other bits. This sweeps every `movabs r64, imm64` in
.text (REX.W B8+r, decoded at each candidate and kept only if it decodes to a movabs there), and keeps
  CLEAR-MASK  imm bit 63 set (an and-mask) and bit 46 clear
  SET-MASK    imm bit 46 set and imm bit 63 clear (an or/test mask)
then prints, for each, the first use of the register in the next 12 instructions (the and/or/test that applies it).
Control: the producer's three sites 00304F9F (clear), 00304EF3 (set) and 0023B0D4 (test) must be listed."""
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
    return "%08X" % funcs[k][0] if k >= 0 and funcs[k][0] <= a < funcs[k][1] else "(no pdata)"

hits = []
for i in range(len(text) - 10):
    if text[i] in (0x48, 0x49) and 0xB8 <= text[i + 1] <= 0xBF:
        imm = struct.unpack_from("<Q", text, i + 2)[0]
        b46 = (imm >> 46) & 1
        b63 = imm >> 63
        kind = None
        if b63 and not b46:
            kind = "CLEAR-MASK"
        elif b46 and not b63:
            kind = "SET-MASK"
        if not kind:
            continue
        a = va0 + i
        xs = list(img.md.disasm(img.rd(a, 80), a))
        if not xs or xs[0].mnemonic != "movabs":
            continue
        reg = xs[0].op_str.split(",")[0].strip()
        use = "(no use in 12)"
        for x in xs[1:13]:
            ops = [o.strip() for o in x.op_str.split(",")]
            if reg in ops[1:] or (reg in ops[:1] and x.mnemonic not in ("mov", "movabs", "lea")):
                use = "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
                break
            if ops and ops[0] == reg:
                use = "(overwritten at %08X)" % x.address
                break
        hits.append((a, kind, imm, use))
for a, kind, imm, use in hits:
    print("M %08X %-10s 0x%016X  in %-10s use: %s" % (a, kind, imm, fn(a), use))
print("TOTAL", len(hits), "CLEAR-MASK", sum(1 for h in hits if h[1] == "CLEAR-MASK"),
      "SET-MASK", sum(1 for h in hits if h[1] == "SET-MASK"))
got = {h[0] for h in hits}
print("CONTROL producer sites found:", all(a in got for a in (0x00304F9F, 0x00304EF3, 0x0023B0D4)))
