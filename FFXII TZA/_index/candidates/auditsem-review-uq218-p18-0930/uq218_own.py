"""SWE2-AUDIT-SEM own UQ-218 pass-18 checks (image only).
Y  yaw sign: 004258B0..00425930 (heading - facing and the band 3 / band 4 tests) and 00425760..004258A0 (the turn sign
   setting esi).
L  @FOR list decoding: 0053C160..0053C240 (list base / count / packing kind) and 0053CDE0..0053CE10 (cursor steps).
F  @FEF seeding: in 0019FFD0, count the stores into [+0x228 + ...] of a rip-relative .rdata string, and print the
   distinct string prefixes (all 'PS2Data\\effect_finish\\jp\\chara\\h....efx'?).
A  op 0x09's lookup arm: 00409780 (called through 00409930 with the '@FMN' tag) - its first 40 instructions, to see
   whether the operand at cmd+2 is used as an index or as a key compared against entries."""
import re, struct, collections
import img
def show(lo, hi, filt=None):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        if filt is None or re.search(filt, x.op_str + " " + x.mnemonic):
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("Y heading - facing, band tests"); show(0x004258B0, 0x00425930)
print("Y turn sign"); show(0x00425760, 0x004258A0, r"0x124|0x254|esi|subss|comiss|seta|setae|setb|jb|ja|jae")
print("L list decoding"); show(0x0053C160, 0x0053C240)
print("L cursor steps"); show(0x0053CDE0, 0x0053CE10)
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE, u + img.BASE))
def chain_root(b, u):
    uo = img.off(u)
    while uo is not None and (img.raw[uo] >> 3) & 4:
        cnt = img.raw[uo + 2]
        co = uo + 4 + ((cnt + 1) & ~1) * 2
        cb, ce, cu = struct.unpack_from("<III", img.raw, co)
        b = cb + img.BASE
        uo = img.off(cu + img.BASE)
    return b
frs = [(b, e) for b, e, u in PD if chain_root(b, u) == 0x0019FFD0]
strings = []
for b, e in sorted(frs):
    xs = list(img.md.disasm(img.rd(b, e - b), b))
    for i, x in enumerate(xs):
        m = re.search(r"rip \+ (0x[0-9a-f]+)", x.op_str)
        if x.mnemonic == "lea" and m:
            t = x.address + x.size + int(m.group(1), 16)
            s = img.rd(t, 64)
            if s and s[:3] in (b"PS2", b"ps2"):
                strings.append(s.split(b"\0")[0].decode("latin-1"))
pref = collections.Counter(re.sub(r"h\d{4}\.efx$", "hNNNN.efx", s) for s in strings)
print("F 0019FFD0 fragments", len(frs), "rip-lea'd PS2Data strings:", len(strings), "distinct", len(set(strings)), dict(pref))
print("A 00409780 (lookup behind 00409930)"); show(0x00409780, 0x00409840)
