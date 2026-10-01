"""SWE2-AUDIT-SEM UQ-218 check of the op 0x09 index base: every store covering word +0x2A in the motion-command module
(0x00400000..0x00430000, .pdata fragments decoded), and the two arms of 00417F40 (index arm vs @FMN-tag lookup arm)."""
import struct, re
import img
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b and 0x00400000 <= b + img.BASE < 0x00430000:
                PD.append((b + img.BASE, e + img.BASE))
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
hits = []
for b, e in PD:
    for x in img.md.disasm(img.rd(b, e - b), b):
        o = [s.strip() for s in x.op_str.split(",")]
        m = re.match(r"(byte|word|dword|qword|xmmword) ptr \[(\w+) \+ (0x[0-9a-f]+|\d+)\]$", o[0]) if o else None
        if not m or x.mnemonic in ("cmp", "test") or len(o) < 2:
            continue
        d, w = int(m.group(3), 0), W[m.group(1)]
        if d <= 0x2A < d + w and m.group(2) not in ("rsp", "rbp"):
            hits.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("stores covering +0x2A in 0x00400000..0x00430000:", len(hits))
for h in hits:
    print("  ", h)
print("00417F40 arms: 00417FE3 test byte [r12+4], 3 (r12 = [ctx+0x368]); jne -> 0041805C index arm "
      "(word[cmd+2]>>1 + s16[ctx+0x2A]); else 00417FF6 edx = 0x4E4D4640 ('@FMN' tag) -> 00409930 lookup arm")
