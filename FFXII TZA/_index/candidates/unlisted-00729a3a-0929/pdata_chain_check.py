"""00729A3A is a chained .pdata fragment of 00729920 (FABLE 2026-09-29, on OPUS-NOTICE-FABLE-00729A3A-RESOLVED).

P1  the exception directory holds 00729920-007299F5 (primary), 007299F5-00729A3A and 00729A3A-00729A9C; both later
    records carry UNW_FLAG_CHAININFO (flags 4) whose chained RUNTIME_FUNCTION is 00729920-007299F5.
P2  00729920 dispatches through a jump table (`jmp rcx` at 007299D3) and its range check `ja` at 007299B9 goes to
    00729A58, inside the 00729A3A fragment.
Control: the primary record 00729920 itself carries flags 0 (not chained) - the flag test can tell the two apart.
Exit 1 on any failure.
"""
import struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, ro, rs))


def off(va):
    rva = va - BASE
    for a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


exc_rva, exc_sz = struct.unpack_from("<II", d, pe + 24 + 112 + 3 * 8)
o = off(BASE + exc_rva)
recs = {}
for i in range(exc_sz // 12):
    b, e, u = struct.unpack_from("<III", d, o + i * 12)
    if 0x00729900 <= b + BASE < 0x00729AA0:
        uo = off(BASE + u)
        flags, cnt = d[uo] >> 3, d[uo + 2]
        chain = None
        if flags & 4:
            cb, ce, _cu = struct.unpack_from("<III", d, uo + 4 + ((cnt + 1) & ~1) * 2)
            chain = (cb + BASE, ce + BASE)
        recs[b + BASE] = (e + BASE, flags, chain)
        print("%08X-%08X flags %d chain %s" % (b + BASE, e + BASE, flags, "%08X-%08X" % chain if chain else "-"))
fails = []
p1 = (recs.get(0x00729920, (0, None, None))[1] == 0
      and recs.get(0x007299F5, (0, 0, None))[2] == (0x00729920, 0x007299F5)
      and recs.get(0x00729A3A) == (0x00729A9C, 4, (0x00729920, 0x007299F5)))
print("P1", "OK" if p1 else "FAIL")
if not p1:
    fails.append("P1")
md = Cs(CS_ARCH_X86, CS_MODE_64)
ins = {x.address: x for x in md.disasm(d[off(0x007299B3):off(0x007299B3) + 0x30], 0x007299B3)}
p2 = (0x007299B9 in ins and ins[0x007299B9].mnemonic == "ja" and ins[0x007299B9].op_str == "0x729a58"
      and 0x007299D3 in ins and ins[0x007299D3].op_str == "rcx" and 0x00729A3A <= 0x00729A58 < 0x00729A9C)
print("P2", "OK" if p2 else "FAIL")
if not p2:
    fails.append("P2")
print("FAILS", len(fails), fails)
sys.exit(1 if fails else 0)
