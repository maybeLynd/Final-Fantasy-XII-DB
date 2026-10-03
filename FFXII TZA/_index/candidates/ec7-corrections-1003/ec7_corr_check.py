"""ec7_corr_check.py - byte control for SWE2-EC7's corrections of 2026-10-03 (R1/R2 of FABLE's title record, X1/X2 of
FABLE's kind-0x54 record, OPUS-REQ-EC7-PREFETCH-CLOSE-CONDITIONAL-1002). Reads the shipping image directly; each check
names the instruction the corrected sentence rests on, and each has a planted wrong expectation that must be rejected.
Prints FAILS 0 when every positive holds and every planted negative is refused."""
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


def call_target(va):
    b = rd(va, 5)
    if b[0] not in (0xE8, 0xE9):
        return None
    return va + 5 + struct.unpack("<i", b[1:5])[0]


def rip_target(va, disp_off, ilen):
    return va + ilen + struct.unpack("<i", rd(va + disp_off, 4))[0]


fails = 0


def check(name, got, want, planted):
    global fails
    ok = got == want and got != planted
    print(("ok   " if ok else "FAIL ") + name, hex(got) if isinstance(got, int) else got)
    if not ok:
        fails += 1


# R1: 00189120 is `mov rax, [rip+d]` / `ret` reading 01F7F598 - no argument register is read.
b = rd(0x00189120, 8)
check("R1 00189120 is mov rax,[rip] ; ret", (b[:3] == b"\x48\x8b\x05" and b[7] == 0xC3), True, False)
check("R1 00189120 reads 01F7F598", rip_target(0x00189120, 3, 7), 0x01F7F598, 0x01F7F590)
# R2: the anchor 0062BCBE calls 0062B100; the 0062EC70 call is at 0062BD75.
check("R2 0062BCBE call target", call_target(0x0062BCBE), 0x0062B100, 0x0062EC70)
check("R2 0062BD75 call target", call_target(0x0062BD75), 0x0062EC70, 0x0062B100)
# PREFETCH: 0059BD40 frees +0x30 only when nonzero (je), releases +0x40 only when > 0 (jle), returns al = 1.
check("P 0059BD50 je over the +0x30 free", rd(0x0059BD50, 1)[0], 0x74, 0x75)
check("P 0059BD52 frees through 002150D0", call_target(0x0059BD52), 0x002150D0, 0)
check("P 0059BD66 jle over the +0x40 release", rd(0x0059BD66, 1)[0], 0x7E, 0x7C)
check("P 0059BD78 mov al, 1", rd(0x0059BD78, 2), b"\xb0\x01", b"\xb0\x00")
# X2: 00521450 is not call-free - it calls 00521BB0 at 00521B26.
check("X2 00521B26 call target", call_target(0x00521B26), 0x00521BB0, None)
# X1: the swap's two stores (low dword to [r8-4], high to [r8-8]) and its scratch cell 022D8F90.
check("X1 0043E7F4 mov [r8-4], eax", rd(0x0043E7F4, 4), b"\x41\x89\x40\xfc", b"\x41\x89\x50\xf8")
check("X1 0043E826 mov [r8-8], edx", rd(0x0043E826, 4), b"\x41\x89\x50\xf8", b"\x41\x89\x40\xfc")
check("X1 0043E7D7 stages into 022D8F90", rip_target(0x0043E7D7, 3, 7), 0x022D8F90, 0x02EB8738)
# X1: 00434760 stores x at [r8-4] and y at [r8-8] (the swap after the affine map).
check("X1 004348D0 mov [r8-8], edx", rd(0x004348D0, 4), b"\x41\x89\x50\xf8", b"\x41\x89\x40\xfc")
# X1: 0043E840's immediate puts -0.5 (BF000000) in the low dword.
check("X1 0043E84D low dword is -0.5", struct.unpack("<I", rd(0x0043E84D + 7, 4))[0], 0xBF000000, 0x3F000000)
# X1: 00396F20's loop bound is the cell 022D8F10.
check("X1 00396FB0 reads 022D8F10", rip_target(0x00396FB0, 3, 7), 0x022D8F10, 0x022D94A0)

print("FAILS", fails)
sys.exit(1 if fails else 0)
