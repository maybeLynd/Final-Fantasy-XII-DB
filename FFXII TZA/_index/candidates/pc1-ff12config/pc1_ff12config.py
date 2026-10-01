"""pc1_ff12config.py - PC-1 narrowed: three of the FF12CONFIG clauses answered and one getter's name corrected (FABLE,
Claude Opus 5.5, 2026-09-26; read by a delegated read-only pass, re-checked here).

  C1 the two option getters are plain byte reads of the loaded FF12CONFIG copy, not device queries:
     00408B80 = movzx eax, byte [02B62DAC]; ret (file byte +0x06) and 00408B40 = movzx eax, byte [02B62DB6] (+0x10).
     Each has one caller, in 002DDA30 (002DDA3B, 002DDA66).
  C2 002DDA30 forces options-word bit 13 from the first (value 1 sets, 002DDA60; value 2 clears, 002DDA51) and bit 14
     from the second (002DDA8B / 002DDA7C). The settings command table names those bits Vibration (command 9) and
     Screen Shake (command 10).
  C3 who enters 002DDA30 with 1: its two entries are the defaults installer's tail jump 002DE035, with ecx = ebx
     (002DE029) and ebx = 1 set at 002DDF9F and not written again before, and the thunk 002DE050, which passes 0.
  C4 field id 236 resolves, through the PLMN name table's u16 offsets at +0x10 + id*2, to "Throne Road" in the shipped
     us planmapname.bin. Control: ids 233 and 243 decode to "Outpost" and "Nomad Village", as the navimap page names
     them.
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
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def at(a): x = ins(a, 16)[0]; return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def rip(a):
    x = ins(a, 16)[0]; s = x.op_str
    return x.address + x.size + int(s.split("rip + ")[1].split("]")[0], 16) if "rip + " in s else None
def e8e9(t):
    out = []; vs, va, rs, ro = secs[0]
    for op in (b"\xE8", b"\xE9"):
        k = d.find(op, ro)
        while 0 <= k < ro + rs - 5:
            a = BASE + va + k - ro
            if a + 5 + struct.unpack_from("<i", d, k + 1)[0] == t: out.append(a)
            k = d.find(op, k + 1)
    return sorted(out)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("C1 00408B80 / 00408B40 are byte getters of FF12CONFIG +0x06 / +0x10, each called once from 002DDA30",
      at(0x408B80).startswith("movzx eax, byte ptr [rip") and rip(0x408B80) == 0x2B62DAC and at(0x408B87) == "ret"
      and rip(0x408B40) == 0x2B62DB6 and e8e9(0x408B80) == [0x2DDA3B] and e8e9(0x408B40) == [0x2DDA66])
check("C2 002DDA30 forces options bit 13 and bit 14 from them",
      at(0x2DDA60) == "or dword ptr [rax], 0x2000" and at(0x2DDA51) == "and dword ptr [rax], 0xffffdfff"
      and at(0x2DDA8B) == "or dword ptr [rax], 0x4000" and at(0x2DDA7C) == "and dword ptr [rax], 0xffffbfff")
W = [x for x in ins(0x2DDF9F, 0x2DE035 - 0x2DDF9F) if 0x2DDF9F < x.address < 0x2DE029 and x.op_str.split(",")[0].strip() in ("ebx", "rbx", "bx", "bl")
     and x.mnemonic not in ("cmp", "test", "push")]
J = [x.address for x in ins(0x2DDE60, 0x2DE040 - 0x2DDE60) if x.mnemonic.startswith("j") and x.op_str.startswith("0x")
     and 0x2DDF9F < int(x.op_str, 16) <= 0x2DE035 and not (0x2DDF9F <= x.address < 0x2DE035)]
check("C3 the defaults installer enters 002DDA30 with 1 (ebx = 1 unchanged, no jump in from outside); the thunk 002DE050 enters with 0",
      e8e9(0x2DDA30) == [0x2DE035, 0x2DE052] and at(0x2DDF9F) == "mov ebx, 1" and at(0x2DE029) == "mov ecx, ebx"
      and at(0x2DE050) == "xor ecx, ecx" and not W and not J,
      "ebx writes between %s; jumps in %s" % (["%08X" % x.address for x in W], ["%08X" % a for a in J]))
P = (Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract") / "ps2data/image/ff12/us/bin/planmapname.bin").read_bytes()
def name(fid):
    o = struct.unpack_from("<H", P, 0x10 + fid * 2)[0]; e = P.index(b"\0", o); s = ""
    for c in P[o:e]:
        s += " " if c == 4 else chr(c + 0x21) if 0x20 <= c <= 0x39 else chr(c + 0x27) if 0x3A <= c <= 0x53 else "?"
    return s
check("C4 field id 236 is 'Throne Road'; control: 233 'Outpost', 243 'Nomad Village'",
      P[:4] == b"PLMN" and name(236) == "Throne Road" and name(233) == "Outpost" and name(243) == "Nomad Village",
      "%r %r %r" % (name(236), name(233), name(243)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
