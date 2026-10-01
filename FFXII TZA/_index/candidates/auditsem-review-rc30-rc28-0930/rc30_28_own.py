"""SWE2-AUDIT-SEM own checks for DATA's RC-30 census and RC-28 callback records.
M  every shipped menumap_common*.bin (extract glob): its entry table (the buffer + u16 [+8]; u32 count; 8-byte entries
   from +4, as 003C1F00 indexes them), and the entries whose byte +1 is non-zero.
R  003C26C0's body: every memory read relative to the picture / buffer registers, and whether any read has displacement
   0x22 or 0x23.
Q  RC-28: 0046E030 (the issue wrapper), 0032E330 and 0032E370 (the completion arms), 00364380 (the callback)."""
import glob, struct, re
import img
for f in sorted(set(p.lower() for p in glob.glob("D:/FFXII_TZA_extract/**/menumap_common*.bin", recursive=True))):
    b = open(f, "rb").read()
    tb = struct.unpack_from("<H", b, 8)[0]
    n = struct.unpack_from("<I", b, tb)[0]
    hits = [(i, b[tb + 4 + 8 * i + 1]) for i in range(n) if tb + 4 + 8 * i + 1 < len(b) and b[tb + 4 + 8 * i + 1]]
    print("M %-70s magic %r table +%#x entries %d nonzero byte+1: %s" % (f[-70:], b[:4], tb, n, hits))
def body(a, n=300):
    return [x for x in img.dis(a, n, stop_ret=False)]
PD = []
for n_, rva, vsz, rp, rs in img.secs:
    if n_ == ".pdata":
        for k in range(0, vsz, 12):
            b0, e0, u = struct.unpack_from("<III", img.raw, rp + k)
            if b0:
                PD.append((b0 + img.BASE, e0 + img.BASE))
def frag(f):
    for b0, e0 in PD:
        if b0 == f:
            return list(img.md.disasm(img.rd(b0, e0 - b0), b0))
    return img.dis(f, 200)
xs = frag(0x003C26C0)
reads = [x for x in xs if re.search(r"ptr \[\w+ \+ 0x(8|c|e|6|10|22|23)\]", x.op_str)]
print("R 003C26C0 instructions %d; reads at +6/+8/+0xC/+0xE/+0x10/+0x22/+0x23:" % len(xs))
for x in reads:
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R any +0x22/+0x23 access in 003C26C0:", any(re.search(r"\+ 0x2[23]\]", x.op_str) for x in xs))
for a in (0x0046E030, 0x0032E330, 0x0032E370, 0x00364380):
    print("Q %08X" % a)
    for x in img.dis(a, 30):
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R2 003C2780..003C2830 (the palette arithmetic and the register call, past the first .pdata fragment)")
for x in img.md.disasm(img.rd(0x003C2780, 0xC0), 0x003C2780):
    if x.address > 0x003C2830:
        break
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
