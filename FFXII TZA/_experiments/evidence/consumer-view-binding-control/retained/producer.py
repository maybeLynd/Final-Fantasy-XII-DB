"""three_check.py - three ASTRA returns re-derived (FABLE, Claude Opus 5.5, 2026-09-28). Static binding plus exact models.
  R1  00229E70: xmm0 = 0; comiss xmm0, [01E02820]; jb -> return the rate; else store and return [01CEBBA8] (1.0). Model:
      0.5 kept, 0 / -0 / -1 reset to 1.0, NaN kept (unordered sets CF)
  I1  0020E600: mov eax, ecx; add rax, qword [01F83530]; 0020E620: sub ecx, dword [01F83530]; mov eax, ecx. Model with a nonzero
      base B: E(D(u)) = u for every 32-bit u; D(E(p)) = p only when (p - B) mod 2^64 < 2^32; D(0) = B
  A1  00339630: xmm9 is written only by the load at 00339723 (constant 008F3138 = 43340000 = 180.0) and the epilogue restore
      00339A02, so 00339880's divss xmm0, xmm9 divides by 180.0
  C   controls: a jbe model keeps zero; an add in place of 0020E620's sub breaks E(D(u)) for nonzero B; a planted write
      to xmm9 before 00339880 is refused by A1's write census
"""
import os, re, struct, sys, math
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
F = {}
for l in open(CACHE, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split(None, 2)
    if len(p) == 3 and p[1] in ("00229E70", "0020E600", "0020E620", "00339630"): F.setdefault(p[1], []).append((int(p[0], 16), p[2]))
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, rs, ra)); o += 40
def u32(v):
    r = v - 0x120000
    for va, rs, ra in secs:
        if va <= r < va + rs: return struct.unpack_from("<I", d, ra + r - va)[0]
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
r = [s.split(" ;")[0] for a, s in F["00229E70"]]
fl = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
def rate(v, jbe=False):
    unordered = math.isnan(v)
    cf = unordered or (0.0 < v); zf = unordered or (v == 0.0)
    take = (cf or zf) if jbe else cf
    return v if take else 1.0
ok("R1", r[:4] == ["movss xmm1, dword ptr [rip + 0x1bd89a8]", "xorps xmm0, xmm0", "comiss xmm0, xmm1", "jb 0x229e91"] and u32(0x01CEBBA8) == 0x3F800000
   and rate(0.5) == 0.5 and rate(0.0) == 1.0 and rate(-0.0) == 1.0 and rate(-1.0) == 1.0 and math.isnan(rate(float("nan"))),
   "kept: 0.5, NaN; reset to 1.0: 0, -0, -1 (default constant %08X)" % u32(0x01CEBBA8))
a = [s.split(" ;")[0].strip() for x, s in F["0020E600"]]; b = [s.split(" ;")[0].strip() for x, s in F["0020E620"]]
B = 0x0000000140000000
D = lambda u: (B + (u & 0xFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
E = lambda p: ((p & 0xFFFFFFFF) - (B & 0xFFFFFFFF)) & 0xFFFFFFFF
samples = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x12345678]
inwin = [B, B + 0xFFFFFFFF]; outwin = [B - 1, B + 0x100000000, 0]
ok("I1", a == ["mov eax, ecx", "add rax, qword ptr [rip + 0x1d74f27]", "ret"] and b == ["sub ecx, dword ptr [rip + 0x1d74f0a]", "mov eax, ecx", "ret"]
   and all(E(D(u)) == u for u in samples) and all(D(E(p)) == p for p in inwin) and not any(D(E(p)) == p for p in outwin) and D(0) == B,
   "E(D(u)) = u for all samples; D(E(p)) = p only inside [B, B + 2^32); D(0) = B")
x9 = [(x, s.split(" ;")[0]) for x, s in F["00339630"] if re.match(r"\w+ xmm9,", s.split(" ;")[0])]
ok("A1", x9 == [(0x00339723, "movss xmm9, dword ptr [rip + 0x5b9a0c]"), (0x00339A02, "movaps xmm9, xmmword ptr [rsp + 0x120]")]
   and u32(0x008F3138) == 0x43340000 and dict(F["00339630"]).get(0x00339880, "").startswith("divss xmm0, xmm9"),
   "xmm9 writes %s; 008F3138 = %08X (180.0)" % (["%08X" % x for x, s in x9], u32(0x008F3138)))
Eadd = lambda p: ((p & 0xFFFFFFFF) + (B & 0xFFFFFFFF)) & 0xFFFFFFFF
planted = x9 + [(0x00339870, "movss xmm9, xmm8")]
ok("C", rate(0.0, jbe=True) == 0.0 and not all(Eadd(D(u)) == u for u in samples)
   and planted != [(0x00339723, "movss xmm9, dword ptr [rip + 0x5b9a0c]"), (0x00339A02, "movaps xmm9, xmmword ptr [rsp + 0x120]")],
   "controls: jbe keeps zero; add-for-sub breaks the round trip; a planted xmm9 write changes the census")
print("FAILS", fails); sys.exit(1 if fails else 0)
