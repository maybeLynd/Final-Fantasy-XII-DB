"""cs3_mist_charges.py - CS-3: the authored source of the secondary pool's multiplier (stats +0x37), and the pool's name
(FABLE, Claude Opus 5.5, 2026-09-26; readings first made by a delegated read-only pass and re-checked here).

  M1 +0x37 is min(stats +0x20, 3) for a party record and 0 otherwise. The rebuild 002FEF30 defaults it to 0
     (002FEFF1), reaches the load only when the kind byte is 0 (002FF026), loads byte +0x20 (002FF0AA), clamps it at 3
     (002FF892-002FF89B), and stores it at [rsi+0x13] (002FF89F). rsi is the record plus 0x24, set at 002FEFAB.
  M2 +0x20 is the larger of chr_data +0x46 and a licence-derived rank. The grower 0030C470 stores row byte +0x46
     (0030C54B/0030C54F), then keeps the larger of that and 00324100's result (0030C552-0030C55F).
  M3 00324100 returns the larger of two things: the count of owned licences 0..17 (00324020, bits at stats +0x194),
     and, over owned licences 0x12..0x1E, the value 00308FF0(0, licence word +8). 00308FF0 returns action +0x0A, but
     only for actions whose kind +0x1E is 5 or 6.
  M4 the shipped data, all nine language packs:
     - chr_data +0x46 is 0 in all 40 rows;
     - licence rows 0x12..0x1E name actions 0x106..0x112 (the Esper summons);
     - those actions have kind 5, and their +0x0A costs are 1,1,1,2,2,3,1,2,3,2,2,3,3.
  M5 the pool's shipped name is "Mist Charges": help_menu.bin in the us pack, in the game's shifted text encoding.
     Control: the same encoder finds "Zodiark" in word.bin.
So +0x37 is not an authored per-unit value. It is derived from the licence board: min(3, max(owned Quickening licences,
the highest charge cost among owned Esper licences, chr_data +0x46 = 0)), and the pool is the Mist Charges.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
R = dis(0x2FEF30, 0x1000)
check("M1 +0x37 = min(+0x20, 3), party only, default 0",
      R.get(0x2FEFF1) == "mov dword ptr [rsp + 0x60], r12d" and R.get(0x2FEFFB) == "movzx ecx, byte ptr [rdi + 5]"
      and R.get(0x2FF0AA) == "movzx eax, byte ptr [rdi + 0x20]" and R.get(0x2FF89F) == "mov byte ptr [rsi + 0x13], r8b"
      and any(v.startswith("cmova") for a, v in R.items() if 0x2FF892 <= a <= 0x2FF89B))
G = dis(0x30C470, 0x200)
check("M2 +0x20 = max(chr_data +0x46, 00324100())",
      G.get(0x30C54B) == "movzx eax, byte ptr [rbp + 0x46]" and G.get(0x30C54F) == "mov byte ptr [rbx + 0x20], al"
      and G.get(0x30C552) == "call 0x324100")
L = dis(0x324100, 198); A = dis(0x308FF0, 110)
check("M3 00324100 takes the licence popcount (00324020) and the Esper licences' 00308FF0 cost; 00308FF0 gates on kind 5/6",
      L.get(0x32412A) == "call 0x324020" and any(v.startswith("test byte ptr [rcx + rbp + 0x194]") for v in L.values())
      and "call 0x308ff0" in L.values() and any("0x1e]" in v for v in A.values()) and any("+ 0xa]" in v for v in A.values()))
EX = Path("D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle")
packs = sorted(EX.glob("*/binaryfile/battle_pack.bin"))
def table(b, k):
    o = struct.unpack_from("<I", b, 4 + 4 * k)[0]
    cnt, stride, ro = struct.unpack_from("<I", b, o + 4)[0], struct.unpack_from("<H", b, o + 8)[0], struct.unpack_from("<I", b, o + 12)[0]
    return lambda i: b[o + ro + stride * i:o + ro + stride * (i + 1)], cnt
ok = []
for p in packs:
    b = p.read_bytes()
    chr_, nc = table(b, 16); lic, nl = table(b, 12); act, na = table(b, 14)
    c46 = all(chr_(i)[0x46] == 0 for i in range(nc))
    w8 = [struct.unpack_from("<H", lic(i), 8)[0] for i in range(0x12, 0x1F)]
    kinds = [act(w)[0x1E] for w in w8]; costs = [act(w)[0x0A] for w in w8]
    ok.append(c46 and w8 == list(range(0x106, 0x113)) and set(kinds) == {5} and costs == [1, 1, 1, 2, 2, 3, 1, 2, 3, 2, 2, 3, 3])
check("M4 the shipped data agree in every pack", len(packs) == 9 and all(ok), "%d packs, %s" % (len(packs), ok))
def enc(s, sp): return bytes((0x20 + ord(c) - 65) if c.isupper() else (0x3A + ord(c) - 97) if c.islower() else sp for c in s)
hm = (EX / "us/binaryfile/help_menu.bin").read_bytes(); wb = (EX / "us/binaryfile/word.bin").read_bytes()
# the word separator in this help text is 0x04 (read at +0xDB8); the letters are the shifted charset A=0x20, a=0x3A
at = hm.find(enc("Mist Charges", 0x04))
check("M5 'Mist Charges' is in the us help_menu.bin; control: 'Zodiark' in word.bin",
      at != -1 and wb.find(enc("Zodiark", 0x04)) != -1, "help_menu +0x%X" % at)
print("FAILS", fails)
sys.exit(1 if fails else 0)
