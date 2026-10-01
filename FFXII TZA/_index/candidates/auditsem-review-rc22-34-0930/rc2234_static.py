"""SWE2-AUDIT-SEM independent static checks for the RC-22..RC-34 record (own code: img.py mapper, raw sweeps).
S1 RC-24: every direct rel32 call/jmp/jcc into the walker 0024AA00 and the codec 00248500 (+ qword / rip refs).
S2 RC-29: every reference to the .rdata block 008FCE00..008FD2D0 by (a) rip-relative operand (longest decode),
   (b) image-base-relative disp32 (RVA 0x7DCE00..0x7DD2D0 appearing as a [reg + reg*s + disp] operand), (c) a qword
   holding a VA in the block anywhere in the file. The producer claims 3 rip + 1 base-relative (001CD186).
S3 RC-27: the u32 table 00D10C98 and every reference to it; the caller loop of 00365810.
S4 RC-26: 003A1F20's dispatch for psm 0x14 / 0x13 / 0.
S5 RC-31: the threshold compare in 00577C30 (00577C9D..00577CB3) and the +0x04 read claim (no read of lst+4 in
   0037EFC0 / 0037E5B0).
"""
import struct, re
import img

t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0

def direct(target):
    out = []
    for i in range(len(text) - 6):
        b = text[i]
        if b in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == target:
            out.append("%08X %s" % (va0 + i, "call" if b == 0xE8 else "jmp"))
        if b == 0x0F and 0x80 <= text[i + 1] <= 0x8F and va0 + i + 6 + struct.unpack_from("<i", text, i + 2)[0] == target:
            out.append("%08X jcc" % (va0 + i))
    return out

def riprefs(lo, hi):
    hits = set()
    for i in range(len(text) - 4):
        d = struct.unpack_from("<i", text, i)[0]
        for tail in (0, 1, 2, 4):
            tgt = va0 + i + 4 + tail + d
            if lo <= tgt < hi:
                hits.add((i, tail, tgt))
    found = {}
    for i, tail, tgt in sorted(hits):
        for back in range(11, 0, -1):
            s = i - back
            if s < 0:
                continue
            x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
            if x and x.size == back + 4 + tail and "rip" in x.op_str:
                found[x.address] = "%08X %s %s -> %08X" % (x.address, x.mnemonic, x.op_str, tgt)
                break
    return found

def qwords(lo, hi):
    out = []
    raw = img.raw
    for o in range(0, len(raw) - 8, 8):
        v = struct.unpack_from("<Q", raw, o)[0]
        if lo <= v < hi:
            out.append("file+%X = %X" % (o, v))
    return out

def based(lo_rva, hi_rva):
    """[reg + reg*s + disp32] with disp32 in the RVA range (image-base-relative addressing)"""
    out = {}
    for i in range(len(text) - 4):
        d = struct.unpack_from("<I", text, i)[0]
        if lo_rva <= d < hi_rva:
            for back in range(1, 12):
                s = i - back
                x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
                if x and s + back + 4 <= x.address - va0 + x.size and "rip" not in x.op_str and re.search(r"\[\w+( \+ \w+(\*\d)?)? \+ 0x%x\]" % d, x.op_str):
                    out[x.address] = "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
                    break
    return out

print("S1 walker 0024AA00 direct sites:", direct(0x0024AA00))
print("S1 codec 00248500 direct sites:", direct(0x00248500))
print("S1 qword refs walker/codec:", qwords(0x0024AA00, 0x0024AA01), qwords(0x00248500, 0x00248501))
r = riprefs(0x008FCE00, 0x008FD2D0)
print("S2a rip refs into 008FCE00..008FD2D0: %d" % len(r))
for a in sorted(r):
    print("   ", r[a])
bb = based(0x008FCE00 - img.BASE, 0x008FD2D0 - img.BASE)
print("S2b image-base-relative [r + r*s + disp] with disp in the block's RVA range: %d" % len(bb))
for a in sorted(bb):
    print("   ", bb[a])
q = qwords(0x008FCE00, 0x008FD2D0)
print("S2c qwords holding a VA inside the block: %d %s" % (len(q), q[:10]))
tb = [struct.unpack_from("<I", img.rd(0x00D10C98, 48), 4 * k)[0] for k in range(12)]
print("S3 00D10C98 u32[12]:", tb)
print("S3 rip refs to 00D10C98..00D10CC8:", list(riprefs(0x00D10C98, 0x00D10CC8).values()))
print("S3 direct sites into 00365810:", direct(0x00365810))
for x in img.dis(0x0053EC80, 24, stop_ret=False):
    if 0x0053EC80 <= x.address <= 0x0053ECB0:
        print("    %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("S4 003A1F20:")
for x in img.dis(0x003A1F20, 30, stop_ret=False):
    if x.address < 0x003A1F60:
        print("    %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("S5 00577C90..00577CB8:")
for x in img.dis(0x00577C90, 20, stop_ret=False):
    if x.address <= 0x00577CB8:
        print("    %08X %s %s" % (x.address, x.mnemonic, x.op_str))
