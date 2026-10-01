"""dof_setter_sites.py - the static facts under the post-processing contract's 2026-09-27 live-scope note (FABLE, Claude
Opus 5.5; on ASTRA-RETURN-FABLE-S40-DISCRIMINATOR).

  S1 the DOF setter 00194250 stores its enable argument (dl) at +0x110.
  S2 it has exactly five direct E8 call sites image-wide (raw sweep, each on a decoded boundary), one of them the
     cutscene loader's 001C42A1 - so a 0 at +0x110 does not by itself name its writer.
  S3 the glare setter 00194310 writes +0xF4 / +0xF8 (the values every cutscene authors equal to the constructor's).
Planted negative: the raw sweep must find the known call 001C42A1 (a sweep that finds nothing would pass S2's "not one").
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
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
s = dis(0x194250, 0x194283)
check("S1 the DOF setter stores the enable byte at +0x110", s.get(0x19427C) == "mov byte ptr [rcx + 0x110], dl" and s.get(0x194282) == "ret")
text = [x for x in secs if x[1] == 0x1000][0]
hits = []
for i in range(text[3], text[3] + text[2] - 5):
    if d[i] == 0xE8:
        va = i - text[3] + text[1] + BASE
        if va + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x194250: hits.append(va)
real = [h for h in hits if dis(h, h + 5).get(h) == "call 0x194250"]
check("S2 five direct call sites, the cutscene loader's among them", len(real) == 5 and 0x1C42A1 in real,
      str(["%08X" % h for h in real]))
g = dis(0x194310, 0x194321)
check("S3 the glare setter writes +0xF4 / +0xF8",
      any(t.endswith("[rcx + 0xf4], xmm1") for t in g.values()) and any(t.endswith("[rcx + 0xf8], xmm2") for t in g.values()),
      str(sorted(g.values())))
print("FAILS", fails)
sys.exit(1 if fails else 0)
