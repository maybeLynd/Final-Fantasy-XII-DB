"""SWE2-AUDIT-SEM: dump the instruction span behind each of FABLE's 13 MANUAL channel reads (rc9_channels.py) so each
can be read by hand: from the evidence start to the log call site (the call to 005CDAA0 at or after the site), plus
every direct jump in the whole image that lands inside the span (a join the linear read could miss)."""
import struct
import img
SPANS = [(0x0019472D, 0x00194796), (0x001D45F0, 0x001D4636), (0x005CCF2C, 0x005CCF6C), (0x005CCF2C, 0x005CCF8B),
         (0x005CCF2C, 0x005CCF99), (0x006862E1, 0x006865DB), (0x006862E1, 0x006867C7), (0x0079C3E2, 0x0079C42B),
         (0x0062A1EB, 0x0062A22A), (0x0062A281, 0x0062A2C0), (0x0062A31B, 0x0062A362), (0x006391D4, 0x006391F2),
         (0x00677D1A, 0x00677D3E)]
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
# every direct jump / jcc target image-wide (raw, cheap): EB/7x rel8, E9 / 0F 8x rel32
targets = {}
for i in range(len(text) - 6):
    b = text[i]
    if b == 0xE9:
        targets.setdefault(va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0], []).append(va0 + i)
    elif b == 0x0F and 0x80 <= text[i + 1] <= 0x8F:
        targets.setdefault(va0 + i + 6 + struct.unpack_from("<i", text, i + 2)[0], []).append(va0 + i)
    elif b == 0xEB or 0x70 <= b <= 0x7F:
        targets.setdefault(va0 + i + 2 + struct.unpack_from("<b", text, i + 1)[0], []).append(va0 + i)
for lo, site in SPANS:
    print("=== span %08X .. site %08X" % (lo, site))
    for x in img.dis(lo, 400, stop_ret=False):
        if x.address > site + 16:
            break
        mark = ""
        srcs = [s for s in targets.get(x.address, []) if not (lo <= s <= site + 16)]
        if srcs and x.address != lo:
            mark = "   <-- raw jump-in from outside the span: " + " ".join("%08X" % s for s in srcs[:6])
        print("  %08X %-6s %s%s" % (x.address, x.mnemonic, x.op_str, mark))
