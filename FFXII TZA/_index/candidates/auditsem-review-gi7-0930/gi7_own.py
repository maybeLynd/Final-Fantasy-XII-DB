"""SWE2-AUDIT-SEM GI-7 own checks (function-list independent).
G1 every rip-relative operand into 02CA4600..02CA4900 over the raw .text (longest decode ending on the disp32).
G2 image-base-relative disp32 0x2B84600..0x2B84900 as a [reg (+ reg*s) + disp] operand anywhere.
G3 qwords anywhere in the file holding a VA in 02CA4600..02CA4900; absolute imm32 of the same range.
G4 constant-base inline bulk loops (../lf0930 inline_bulk.tsv, the image-wide census) whose base lies within 64 KB below
   bank B.
G5 raw E8/E9 sites into the registrar 0041D6D0 and the instructions before each."""
import struct, re, csv
import img
LO, HI = 0x02CA4600, 0x02CA4900
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
g1 = {}
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 2, 4):
        tg = va0 + i + 4 + tail + d
        if LO <= tg < HI:
            for back in range(11, 0, -1):
                x = next(img.md.disasm(text[i - back:i - back + 16], va0 + i - back), None)
                if x and x.size == back + 4 + tail and "rip" in x.op_str:
                    g1[x.address] = "%08X %s %s -> %08X" % (x.address, x.mnemonic, x.op_str, tg)
                    break
print("G1 rip-relative operands into 02CA4600..02CA4900: %d" % len(g1))
for a in sorted(g1):
    print("   ", g1[a])
g2 = []
for i in range(len(text) - 4):
    v = struct.unpack_from("<I", text, i)[0]
    if LO - img.BASE <= v < HI - img.BASE:
        for back in range(1, 11):
            x = next(img.md.disasm(text[i - back:i - back + 16], va0 + i - back), None)
            if x and "rip" not in x.op_str and ("0x%x" % v) in x.op_str and "[" in x.op_str:
                g2.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
                break
print("G2 image-base-relative operands:", g2)
q = [o for o in range(0, len(img.raw) - 8, 8) if LO <= struct.unpack_from("<Q", img.raw, o)[0] < HI]
imm = [i for i in range(len(text) - 4) if LO <= struct.unpack_from("<I", text, i)[0] < HI]
print("G3 aligned qwords into the range: %d; raw imm32/disp32 byte hits of the absolute VA: %d" % (len(q), len(imm)))
rows = list(csv.DictReader(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\lf0930\inline_bulk.tsv"), delimiter="\t"))
near = [r for r in rows if r["base_const"] != "-" and LO - 0x10000 <= int(r["base_const"], 16) < HI]
print("G4 constant-base inline loops within 64 KB below / inside bank B:", [(r["head"], r["base_const"], r["stride"], r["extent"]) for r in near])
for i in range(len(text) - 5):
    if text[i] == 0xE8 and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == 0x0041D6D0:
        s = va0 + i
        for back in range(40, 10, -1):
            xs = list(img.md.disasm(img.rd(s - back, back + 5), s - back))
            if any(x.address == s for x in xs):
                break
        print("G5 call 0041D6D0 at %08X:" % s)
        for x in [x for x in xs if x.address <= s][-6:]:
            print("     %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("G6 bank-A slot-5 registrations in the actor-side registrars (instructions before each call site):")
for s in (0x002EA492, 0x002EA5FB):
    for back in range(40, 10, -1):
        xs = list(img.md.disasm(img.rd(s - back, back + 5), s - back))
        if any(x.address == s for x in xs):
            break
    for x in [x for x in xs if x.address <= s][-4:]:
        print("     %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("G6 0016D6A0 body:", ["%s %s" % (x.mnemonic, x.op_str) for x in img.dis(0x0016D6A0, 3)])
