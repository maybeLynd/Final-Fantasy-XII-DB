"""ec7_corr_b_check.py - byte control for SWE2-EC7's corrections set B of 2026-10-03 (00297C10 matched row, the
004309C0 combiner tail, 00399B80 / 0039A150 return and pack sites). Reads the shipping image directly; every positive
has a planted wrong expectation that must be refused. Prints FAILS 0 when all hold."""
import struct
import sys

EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
img = open(EXE, "rb").read()
pe = struct.unpack_from("<I", img, 0x3C)[0]
nsec = struct.unpack_from("<H", img, pe + 6)[0]
optsz = struct.unpack_from("<H", img, pe + 20)[0]
BASE = struct.unpack_from("<Q", img, pe + 24 + 24)[0]
SECS = []
o = pe + 24 + optsz
for i in range(nsec):
    vs, va, rs, rp = struct.unpack_from("<IIII", img, o + 8)
    SECS.append((BASE + va, vs, rp, rs))
    o += 40


def rd(va, n):
    for v, vs, rp, rs in SECS:
        if v <= va < v + max(vs, rs):
            return img[rp + va - v: rp + va - v + n]
    raise ValueError(hex(va))


def branch_target(va):
    b = rd(va, 6)
    if b[0] in (0xE8, 0xE9):
        return va + 5 + struct.unpack("<i", b[1:5])[0]
    if b[0] == 0x0F and 0x80 <= b[1] <= 0x8F:
        return va + 6 + struct.unpack("<i", b[2:6])[0]
    if 0x70 <= b[0] <= 0x7F or b[0] == 0xEB:
        return va + 2 + struct.unpack("<b", b[1:2])[0]
    return None


def rip(va, disp_off, ilen):
    return va + ilen + struct.unpack("<i", rd(va + disp_off, 4))[0]


fails = 0


def check(name, got, want, planted):
    global fails
    ok = got == want and got != planted
    print(("ok   " if ok else "FAIL ") + name, hex(got) if isinstance(got, int) else got)
    if not ok:
        fails += 1


# 00297C10: scan base and bound, the matched row's je into the tail, the free path's two initializer calls.
check("W 00297C1A lea 0209BFBE", rip(0x00297C1A, 3, 7), 0x0209BFBE, 0x0209BF40)
check("W 00297C27 bound 0209C2BE", rip(0x00297C27, 3, 7), 0x0209C2BE, 0x0209C1FE)
check("W four rows", (0x0209C2BE - 0x0209BFBE) // 0xC0, 4, 3)
check("W 00297C45 je -> tail 00297CE2", branch_target(0x00297C45), 0x00297CE2, 0x00297C7E)
check("W 00297C9A free path calls 003F89C0", branch_target(0x00297C9A), 0x003F89C0, 0x00297CE2)
check("W 00297CB7 second half calls 003F89C0", branch_target(0x00297CB7), 0x003F89C0, 0)
check("W tail 00297CE2 above both init calls", 0x00297CE2 > 0x00297CB7, True, False)
# 004309C0: tail-jump to 004307C0 at 00430A56; 00430540 is called, not tailed.
check("R 00430A56 jmp 004307C0", branch_target(0x00430A56), 0x004307C0, 0x00430540)
check("R 00430A56 is jmp (E9)", rd(0x00430A56, 1)[0], 0xE9, 0xE8)
check("R 004309F7 call 00430540", branch_target(0x004309F7), 0x00430540, 0x004307C0)
check("R 00430A39 call 00430540", branch_target(0x00430A39), 0x00430540, 0x004307C0)
# 00399B80: 1 into 022D8F30 at 00399E37/00399E45, jne to the exit that returns it, normal exit returns $zero.
check("T 00399E37 or r10, 1", rd(0x00399E37, 4), b"\x49\x83\xca\x01", b"\x49\x83\xca\x00")
check("T 00399E45 stores 022D8F30", rip(0x00399E45, 3, 7), 0x022D8F30, 0x022D8F10)
check("T 0039A0C9 jne -> 0039A122", branch_target(0x0039A0C9), 0x0039A122, 0x0039A116)
check("T 0039A122 reads 022D8F30", rip(0x0039A122, 2, 6), 0x022D8F30, 0x022D8F10)
check("T 0039A0F9 reads $zero 022D8F10", rip(0x0039A0F9, 3, 7), 0x022D8F10, 0x022D8F30)
# 0039A150: the two entry stores, and the $zero read before the failing one.
check("P 0039A6CB je 0039A6F0 (pass arm)", branch_target(0x0039A6CB), 0x0039A6F0, 0x0039A6CD)
check("P 0039A6CD mov [r11], rcx", rd(0x0039A6CD, 3), b"\x49\x89\x0b", b"\x49\x89\x03")
check("P 0039A712 mov [r11], rcx", rd(0x0039A712, 3), b"\x49\x89\x0b", b"\x49\x89\x03")
check("P 0039A51A loads $zero 022D8F10", rip(0x0039A51A, 3, 7), 0x022D8F10, 0x022D8F30)

print("FAILS", fails)
sys.exit(1 if fails else 0)
