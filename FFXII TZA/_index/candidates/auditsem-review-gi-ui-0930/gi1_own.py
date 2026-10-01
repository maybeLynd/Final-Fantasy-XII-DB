"""SWE2-AUDIT-SEM GI-1 spot check: the tab-strip marker 00566C10 - its calls (a sine for the pulsing alpha, not an icon
load) and every test of the create record's +0x14; and the two picker builders' menu kinds (0056AE80 -> 0x22,
0056B100 -> 0x23) with their grid addresses."""
import struct, re
import img
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE))
def body(f):
    out = []
    for b, e in PD:
        if b == f:
            out = list(img.md.disasm(img.rd(b, e - b), b))
    return out
xs = body(0x00566C10)
print("00566C10 size", (xs[-1].address + xs[-1].size - 0x00566C10) if xs else None)
calls = sorted(set(x.op_str for x in xs if x.mnemonic == "call"))
print("calls:", calls)
for x in xs:
    if "0x14]" in x.op_str or "sin" in x.op_str:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for f in (0x0056AE80, 0x0056B100):
    ys = body(f)
    hits = []
    for y in ys:
        m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", y.op_str)
        if m:
            t = y.address + y.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
            if 0x0208D000 <= t < 0x0208E000:
                hits.append("%08X %s -> %08X" % (y.address, y.mnemonic, t))
        if re.search(r", 0x2[23]$", y.op_str):
            hits.append("%08X %s %s" % (y.address, y.mnemonic, y.op_str))
    print("%08X:" % f, hits)
