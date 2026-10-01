"""SWE2-AUDIT-SEM GI-2 / GI-4 own checks.
D1 (C1 framing): the 0x48 bytes at 00D23688 read as 12 records {u16 label, u16 help, u8 key, u8 flag} and, for
   contrast, as FABLE's retired framing {u8 paneKind, u8 flag, u16, u16} from 00D2368C; every instruction that uses the
   image-base-relative displacements 0xC0368C / 0xC036A4 (raw disp32 search, decoded in place); what lies at 00D236D0.
D2 (C2 hcom): menuhandbook.bin in all locales under myoshiok/*/handbook: magic, then the chain p = 8; p += u16[p]
   until the end; the number of sections and whether the chain ends exactly at the file size.
D3 (C4): the direct installers of 0056F810 and 00556F90 (every rel32 reference and every rip lea / qword naming them)."""
import struct, glob, re
import img
b = img.rd(0x00D23688, 0x50)
print("D1 reader framing {u16 label, u16 help, u8 key, u8 flag} from 00D23688:")
for k in range(12):
    lab, hlp, key, fl = struct.unpack_from("<HHBB", b, 6 * k)
    print("   rec %2d  label %04X  help %04X  key %d  flag %d" % (k, lab, hlp, key, fl))
print("D1 dword at 00D236D0: %08X" % struct.unpack_from("<I", img.rd(0x00D236D0, 4))[0])
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
for disp in (0xC0368C, 0xC036A4):
    pat = struct.pack("<I", disp)
    p = text.find(pat)
    while p >= 0:
        for back in range(1, 11):
            x = next(img.md.disasm(text[p - back:p - back + 16], va0 + p - back), None)
            if x and x.address + x.size >= va0 + p + 4 and ("0x%x" % disp) in x.op_str:
                print("   disp %#x at %08X %s %s" % (disp, x.address, x.mnemonic, x.op_str))
                break
        p = text.find(pat, p + 1)
FF = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
for f in sorted(glob.glob(FF + "/*/handbook/menuhandbook.bin")):
    d = open(f, "rb").read()
    p, secs = 8, []
    while p + 2 <= len(d):
        ln = struct.unpack_from("<H", d, p)[0]
        if ln == 0:
            break
        secs.append(ln)
        p += ln
    print("D2 %s: magic %r, size %d, sections %d %s, chain end %d (== size: %s)" % (
        f[-40:], d[:4], len(d), len(secs), secs, p, p == len(d)))
for target in (0x0056F810, 0x00556F90):
    refs = []
    for i in range(len(text) - 4):
        d32 = struct.unpack_from("<i", text, i)[0]
        if va0 + i + 4 + d32 == target:
            for back in range(11, 0, -1):
                x = next(img.md.disasm(text[i - back:i - back + 16], va0 + i - back), None)
                if x and x.size == back + 4 and ("rip" in x.op_str or x.mnemonic in ("call", "jmp")):
                    refs.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
                    break
        if text[i] in (0xE8, 0xE9) and i + 5 <= len(text) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == target:
            refs.append("%08X %s rel32" % (va0 + i, "call" if text[i] == 0xE8 else "jmp"))
    print("D3 %08X referenced by: %s ; qwords %d" % (target, sorted(set(refs)), img.raw.count(struct.pack("<Q", target))))
