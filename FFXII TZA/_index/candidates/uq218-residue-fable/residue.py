"""residue.py - UQ-218 residue items 1, 2, 4 and 5 (FABLE, Claude Opus 5.5, 2026-09-29): the claims two read-only subagent
readings made, each pinned here to the image. STATIC, certified image.

  E  the effect ticket at resource-entry +0x44: written by 00409FE0 (0040A17C) and reset to -1 (00409757); READ by
     0040A1B3 (-> 003B3B10), 00409CFD and 00409EB8 (-> 003B37E0, stop/release), 0041F6FB (-> 003B3550, which builds the
     character's render object) and 005049B3 (-> the ret-0 stub 0016D6A0)
  C  0041E580's four call sites 002E4DB4, 002E4EFA, 003DC371, 003DD8AB; each lies in a load-completion callback whose
     address is taken by lea at 002EADA2 (002E4D20), 002E6FB3 (002E4E50), 003DC650 (003DC340), 003DDA83 (003DD850)
  S  the bone scale at +0x100: the final-pose composer 00373860 (single E8 caller 003705BA) takes lea r9, [rbx + 0x100]
     (00373B58) into 00372610, which scales the pose's rows by four calls to 00202FE0; the branch at 003739DD tests
     byte [bone + 0x280] bit 0x10
  W  the @FMW literal codec reads s16 LITTLE-endian: high byte from p + 2 + 2i, low byte from p + 1 + 2i - in the arm-0
     reader (0041B412 / 0041B41F) and the arm-1 reader (0041B7C6 / 0041B7D3). The page's "s16 big-endian" is rejected
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def after(a, want, span=0x30):
    """the first call at or after a within span bytes, as its target text"""
    return any(x.mnemonic in ("call", "jmp") and x.op_str == want for x in cs.disasm(d[off(a):off(a) + span], a))
def lea_target(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a))
    if x.mnemonic != "lea" or "rip" not in x.op_str: return None
    sgn = -1 if "rip - " in x.op_str else 1
    return a + x.size + sgn * int(x.op_str.split("rip ")[1][2:].rstrip("]"), 16)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
has = lambda a, *subs: all(s in ins(a) for s in subs)
e = [has(0x40A17C, "mov", "+ 0x44]"), (ins(0x40974F) == "or ecx, 0xffffffff" and ins(0x409757) == "mov dword ptr [rdi + 0x44], ecx"),
     has(0x40A1B3, "+ 0x44]") and after(0x40A1B3, "0x3b3b10", 0x20),
     has(0x409CFD, "+ 0x44]") and after(0x409CFD, "0x3b37e0", 0x40), has(0x409EB8, "+ 0x44]") and after(0x409EB8, "0x3b37e0", 0x40),
     has(0x41F6FB, "+ 0x44]") and after(0x41F6FB, "0x3b3550", 0x40), has(0x5049B3, "+ 0x44]") and after(0x5049B3, "0x16d6a0", 0x20)]
check("E", all(e), "ticket +0x44: write 0040A17C, reset 00409757, readers 0040A1B3 / 00409CFD / 00409EB8 / 0041F6FB / 005049B3 -> %s" % e)
sites = [ins(a) for a in (0x2E4DB4, 0x2E4EFA, 0x3DC371, 0x3DD8AB)]
leas = [(a, ins(a)) for a in (0x2EADA2, 0x2E6FB3, 0x3DC650, 0x3DDA83)]
tg = ["0x2e4d20", "0x2e4e50", "0x3dc340", "0x3dd850"]
lea_ok = [lea_target(a) == int(t, 16) for (a, s), t in zip(leas, tg)]
check("C", all(s.split(" ")[-1] == "0x41e580" for s in sites) and sites[2].startswith("jmp") and all(lea_ok),
      "call sites %s; callbacks taken by lea %s" % (sites, lea_ok))
e8 = []
for vs, va, rs, ro in SECS:
    blob = d[ro:ro + rs]
    for i in range(len(blob) - 5):
        if blob[i] == 0xE8 and B + va + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == 0x373860: e8.append(B + va + i)
s_ok = [has(0x373B58, "lea r9", "+ 0x100]"), after(0x373B58, "0x372610", 0x40), has(0x3739DD, "0x280]", "0x10"), e8 == [0x3705BA]]
sc = sum(1 for x in cs.disasm(d[off(0x372610):off(0x372610) + 0x100], 0x372610) if x.mnemonic == "call" and x.op_str == "0x202fe0")
check("S", all(s_ok) and sc == 4, "lea r9,[rbx+0x100] -> 00372610 %s; 00373860 callers %s; 00202FE0 calls in the compose %d"
      % (s_ok, ["%08X" % a for a in e8], sc))
w = [ins(a) for a in (0x41B412, 0x41B418, 0x41B41F, 0x41B7C6, 0x41B7CC, 0x41B7D3)]
check("W", "+ 2]" in w[0] and "shl ax, 8" == w[1] and "+ 1]" in w[2] and "+ 2]" in w[3] and "shl ax, 8" == w[4] and "+ 1]" in w[5],
      "s16 high byte at p+2+2i, low at p+1+2i (little-endian), arm 0 and arm 1: %s" % w)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
