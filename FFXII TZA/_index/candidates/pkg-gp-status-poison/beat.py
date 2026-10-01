"""beat.py - PKG-GP-STATUS-POISON Q1: how often Poison hits (FABLE, Claude Opus 5.5, 2026-09-29). STATIC + DATA.

  S  STAGE 2's beat (00386C70): each run subtracts 10 from the status's beat +0x13C[s] (00386CEB-00386CF5); when it
     runs out the beat reloads to status row byte +9 x [01DFE0B4] x 30 (00386E76-00386E84), the same value the
     infliction's default gives (BattleStatus_ComputeDefaultShortTimer 003876D0, 00387714-0038771F)
  D  DATA (status_data.bin): Poison +9 = 120, Sap +9 = 1, Regen +9 = 15
  M  MODEL, on two premises the model does not re-derive: the periodic tick runs once per unit per frame (the per-unit
     frame, the world-tick page), and [01DFE0B4] is 1 at 30 fps and 2 at 60 (the boot-fixups contract). Then a beat lasts
     byte9 x fb x 30 / 10 runs = byte9 x 3 x fb frames = byte9 / 10 seconds at either frame rate: Poison 12 s, Sap 0.1 s,
     Regen 1.5 s. The "third of a second" the tick contract gave Poison is the stage-4 drain's interval (frame base x 10
     runs), not Poison's
  Not claimed: a live timing (none exists); the beat during a skip, when the tick runs up to sixteen times a frame.
"""
import glob, hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
EXT = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"
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
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
lin = {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(0x386C70):off(0x387017)], 0x386C70)}
dflt = {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(0x3876D0):off(0x387728)], 0x3876D0)}
check("S", at(lin, {0x386CEB: "movsx eax, word ptr [rcx + r15]", 0x386CF0: "sub eax, 0xa", 0x386CF5: "jg 0x386e84",
                    0x386E76: "movzx eax, byte ptr [rcx + 9]", 0x386E7A: "imul eax, dword ptr [rip + 0x1a77233]",
                    0x386E81: "imul eax, eax, 0x1e", 0x386E84: "mov word ptr [r15], ax"})
      and 0x386E81 + 0x1A77233 == 0x1DFE0B4
      and at(dflt, {0x387714: "movzx eax, byte ptr [rcx + 9]", 0x387718: "imul eax, dword ptr [rip + 0x1a76995]",
                    0x38771F: "imul eax, eax, 0x1e"}) and 0x38771F + 0x1A76995 == 0x1DFE0B4,
      "beat -10 per run; reload = byte9 x [01DFE0B4] x 30 (and the same default at infliction)")
sd = open(sorted(glob.glob(os.path.join(EXT, "*", "binaryfile", "status_data.bin")))[0], "rb").read()
cn, st, rp = struct.unpack_from("<III", sd, 4)
b9 = lambda k: sd[rp + k * st + 9]
check("D", (b9(8), b9(10), b9(25)) == (120, 1, 15), "Poison / Sap / Regen byte +9 = %d / %d / %d" % (b9(8), b9(10), b9(25)))
def beat_seconds(byte9, fps):
    fb = 1 if fps == 30 else 2
    runs = byte9 * fb * 30 / 10
    return runs / fps
drain = lambda fps: (1 if fps == 30 else 2) * 10 / fps
check("M", all(abs(beat_seconds(120, f) - 12.0) < 1e-9 and abs(beat_seconds(1, f) - 0.1) < 1e-9
               and abs(beat_seconds(15, f) - 1.5) < 1e-9 and abs(drain(f) - 1 / 3) < 1e-9 for f in (30, 60)),
      "Poison 12 s, Sap 0.1 s, Regen 1.5 s at 30 and 60 fps; the drain interval is 1/3 s - a different timer")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
