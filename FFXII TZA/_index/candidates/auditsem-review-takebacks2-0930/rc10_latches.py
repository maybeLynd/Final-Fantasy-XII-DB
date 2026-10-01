"""SWE2-AUDIT-SEM RC-10 re-read (own code): for each of FABLE's nine warn-once latches, the guard compares a global
byte and, between the guard and the log call, the SAME byte is set to 1 (a latch). For the screen-mode flag 02EA5247,
every rip-relative instruction referencing it (reads and writes) image-wide. For the three "linear-window artefacts",
the span from guard to site is printed for reading."""
import struct, re
import img
LATCH = [(0x00601E09, 0x00601E24, 0x02CE9D9D), (0x00603382, 0x006033A2, 0x02CE9D9C), (0x0061C1FD, 0x0061C219, 0x02CF6C3C),
         (0x0062A1F3, 0x0062A22A, 0x02CF6ABC), (0x0062A289, 0x0062A2C0, 0x02CF6ABD), (0x0062A327, 0x0062A362, 0x02CF6ABE),
         (0x0067C28B, 0x0067C2A7, 0x02E3F804), (0x0079A158, 0x0079A178, 0x02EAC278), (0x0079FDAF, 0x0079FDCB, 0x02EAC279)]
def rip_target(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    if not m:
        return None
    return x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
ok = 0
for g, site, cell in LATCH:
    sets = []
    for x in img.dis(g, 60, stop_ret=False):
        if x.address > site:
            break
        if x.mnemonic == "mov" and x.op_str.startswith("byte ptr [rip") and rip_target(x) == cell:
            sets.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
    good = bool(sets) and all(s.endswith(", 1") for s in sets)
    ok += good
    print("%s latch %08X guard %08X site %08X: sets %s" % ("PASS" if good else "FAIL", cell, g, site, sets))
print("latches confirmed: %d / %d" % (ok, len(LATCH)))
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
refs = {}
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 2, 4):
        if va0 + i + 4 + tail + d == 0x02EA5247:
            for back in range(11, 0, -1):
                s = i - back
                x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
                if x and x.size == back + 4 + tail and "rip" in x.op_str:
                    refs[x.address] = "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
                    break
print("02EA5247 rip references:", list(refs.values()))
for lo, hi in ((0x001DDBA0, 0x001DDC22), (0x0079A158, 0x0079A1A6), (0x007994B4, 0x007994DD)):
    print("== span %08X..%08X" % (lo, hi))
    for x in img.dis(lo, 80, stop_ret=False):
        if x.address > hi:
            break
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
