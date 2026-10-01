"""wrap_check.py - 0026C090's re-wrap is a two-cycle at exactly +/-pi, not idempotent (FABLE, Claude Opus 5.5, 2026-09-28).
Static: binds the instruction sequence from the listing and the three constants from the image, then computes the
sequence in binary32 (round to nearest, no FTZ/DAZ).
  W1  sequence: comiss h, 0 / jb -> bias = [00915620] (h < 0) else [01CEBC50]; t = h + bias; q = cvttss2si(t / [01CEBC78]);
      t - float(q) * [01CEBC78] - bias; kind 3 stores it at 0026C0F9
  W2  constants: 01CEBC50 = 40490FDB (+pi), 00915620 = C0490FDB (-pi), 01CEBC78 = 40C90FDB (2pi)
  W3  +pi -> -pi -> +pi and -pi -> +pi -> -pi (a two-cycle); +0 -> +0 (fixed; control)
  C   detector: with the negative bias replaced by +pi (ASTRA's private changed-bias case), -pi becomes a fixed point,
      so the check sees the bias choice
"""
import os, re, struct, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
ins = sorted((int(p[0], 16), p[2].split(" ;")[0]) for p in (l.rstrip("\n").split(None, 2) for l in open(CACHE, encoding="utf-8", errors="replace")) if len(p) == 3 and p[1] == "0026C090")
B = dict(ins)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, rs, ra)); o += 40
def u32(v):
    r = v - 0x120000
    for va, rs, ra in secs:
        if va <= r < va + rs: return struct.unpack_from("<I", d, ra + r - va)[0]
want = {0x0026C096: "comiss xmm3, xmm0", 0x0026C09C: "jb 0x26c0a8", 0x0026C0B4: "addss xmm3, xmm4", 0x0026C0BE: "divss xmm0, dword ptr [rip + 0x1a7fbb2]",
        0x0026C0C6: "cvttss2si eax, xmm0", 0x0026C0CE: "cvtdq2ps xmm1, xmm1", 0x0026C0D1: "mulss xmm1, dword ptr [rip + 0x1a7fb9f]",
        0x0026C0D9: "subss xmm3, xmm1", 0x0026C0DD: "subss xmm3, xmm4", 0x0026C0F9: "movss dword ptr [rcx + 0x34], xmm3"}
ok("W1", all(B.get(a) == s for a, s in want.items()) and B.get(0x0026C09E, "").startswith("movss xmm4") and B.get(0x0026C0A8, "").startswith("movss xmm4"),
   "sequence bound at %d instructions (sign branch 0026C09C, bias loads 0026C09E / 0026C0A8, store 0026C0F9)" % len(want))
PP, NP, TP = u32(0x01CEBC50), u32(0x00915620), u32(0x01CEBC78)
ok("W2", (PP, NP, TP) == (0x40490FDB, 0xC0490FDB, 0x40C90FDB), "constants %08X %08X %08X" % (PP, NP, TP))
f = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
bits = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]
fl = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
def wrap(h, neg=NP):
    bias = fl(PP) if not (h < 0.0) else fl(neg)          # comiss / jb: unordered or below takes the negative bias
    t = f(h + bias); q = int(f(t / fl(TP)))                # cvttss2si truncates toward zero
    return f(f(t - f(float(q) * fl(TP))) - bias)
pi, npi = fl(0x40490FDB), fl(0xC0490FDB)
c1 = [bits(x) for x in (pi, wrap(pi), wrap(wrap(pi)))]; c2 = [bits(x) for x in (npi, wrap(npi), wrap(wrap(npi)))]
ok("W3", c1 == [0x40490FDB, 0xC0490FDB, 0x40490FDB] and c2 == [0xC0490FDB, 0x40490FDB, 0xC0490FDB] and bits(wrap(0.0)) == 0,
   "+pi -> %08X -> %08X; -pi -> %08X -> %08X; +0 -> %08X" % (c1[1], c1[2], c2[1], c2[2], bits(wrap(0.0))))
ok("C", bits(wrap(npi, neg=PP)) == 0xC0490FDB, "detector: with the negative bias set to +pi, -pi maps to %08X (fixed)" % bits(wrap(npi, neg=PP)))
print("FAILS", fails); sys.exit(1 if fails else 0)
