"""classifier.py - UQ-218: @FMC 0x0B selector kinds 0, 0xA and 0xB, the locomotion classifier 004256E0 (FABLE, Claude Opus 5.5,
2026-09-29; read with a subagent's full reading, every claim below re-checked here from the certified image).

  B  THE BANDS (the band value lands in ebx; each anchor is the instruction that sets it):
     0xE  when 003E7D10(rec+0x6A4, 4) is non-zero (004257E9 call, 004257F8 lea ebx, [r15 + 0xd]);
     below the speed threshold T = 003E58B0(rec) compared with rec+0x23C:
       0  when the last turn D = wrap(+0x124 - +0x254) (facing minus previous facing, both yaw lanes) is 0 or inside +-C1,
          C1 = float [01DFE0BC] (the boot fixups' 1.0 at 30 fps, 0.5 at 60);
       6  otherwise (0042584E), 7 when 003E5EA0(rec) is set and |D| x C2 ([01DFE0B8]) reaches the model's turn angle
          003E5C90(rec) (00425867 / 00425887 cmovae); esi = D >= 0;
     between T and rec+0x420: the movement heading +0x244 against the facing: within +-45 -> 1, (45, 135] -> 3,
       [-135, -45) -> 4, else 5 (004258B1 / 00425919 / 00425931 / 0042593B);
     at or above +0x420: 2 (0042594C); when the view query 0x1000 answers flag 0x20 (00425974 / 00425979), the bearing to
       the resolved target record splits it: +-45 -> 2, (45, 135] -> 0xA, [-135, -45) -> 9, else 0xB.
  F  THE MODEL CHECK: each band is tested against a model (FCP) property read by 004FE2F0 with ids 0x63070F30, 0x62070E30,
     0x61070D30, 0x60070C30 and 0x63070B2D (00425A28, 00425A4E, 00425A94, 00425AE6, 00425BA9), falling back to a
     simpler band when the model lacks the motion (fallback table in criteria.md)
  R  THE RESULT: rec+0x2A0 = band (00425C6A); argument 0 and 2 lower bands 9-0xB by one (00425D0A dec ebx), 0xE becomes
     0xB / 0xC / 0xD for argument 0 / 1 / 2 (lea ebx, [r12 + 0xb]); eax = index + ((1 - esi) << 16) (00425D0C..00425D11),
     so the selector never returns -1: it always chooses
  Not claimed: which yaw sign is left; what +0x23C (typed animPhaseFloat) measures; the names of the bands beyond the
  geometry above (idle / walk / run / turn are inference).
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
ins = {x.address: x for x in cs.disasm(d[off(0x4256E0):off(0x425D5E)], 0x4256E0)}
txt = {a: ("%s %s" % (x.mnemonic, x.op_str)).strip() for a, x in ins.items()}
def rip(a):
    x = ins[a]; s = x.op_str
    return a + x.size + int(s.split("rip + ")[1].split("]")[0], 16)
f32 = lambda a: struct.unpack_from("<f", d, off(a))[0]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda w: all(txt.get(a) == s for a, s in w.items())

bands = at({0x4257E4: "mov edx, 4", 0x4257E9: "call 0x3e7d10", 0x4257F8: "lea ebx, [r15 + 0xd]", 0x4257EE: "mov r15d, 1",
            0x425751: "movss xmm1, dword ptr [rdi + 0x254]", 0x425759: "movss xmm6, dword ptr [rdi + 0x124]",
            0x42573F: "call 0x3e58b0", 0x425804: "movss xmm1, dword ptr [rdi + 0x23c]", 0x42584E: "mov ebx, 6",
            0x425867: "mov eax, 7", 0x425887: "cmovae ebx, eax", 0x425898: "movss xmm0, dword ptr [rdi + 0x420]",
            0x4258A9: "movss xmm1, dword ptr [rdi + 0x244]", 0x4258B1: "mov ebx, r15d", 0x425919: "mov ebx, 3",
            0x425931: "mov ebx, 4", 0x42593B: "mov ebx, 5", 0x42594C: "mov ebx, 2", 0x42596F: "mov edx, 0x1000",
            0x425979: "test byte ptr [rsp + 0x5c], 0x20", 0x4259DA: "mov ebx, 0xa", 0x4259ED: "mov ebx, 9", 0x4259F4: "mov ebx, 0xb"})
c1, c2 = rip(0x425827), rip(0x42587C)
ang = [f32(rip(a)) for a in (0x4258E9, 0x4258F4, 0x42590C, 0x425928)]
check("B", bands and c1 == 0x1DFE0BC and c2 == 0x1DFE0B8 and ang == [-45.0, 45.0, 135.0, -135.0],
      "band sites %s; C1 at %08X, C2 at %08X; heading windows %s" % (bands, c1, c2, ang))
fcp = at({0x425A28: "mov edx, 0x63070f30", 0x425A4E: "mov edx, 0x62070e30", 0x425A94: "mov edx, 0x61070d30",
          0x425AE6: "mov edx, 0x60070c30", 0x425BA9: "mov edx, 0x63070b2d", 0x425A30: "call 0x4fe2f0"})
check("F", fcp, "five FCP property ids passed to 004FE2F0 before each band is accepted: %s" % fcp)
res = at({0x425C6A: "mov dword ptr [rdi + 0x2a0], ebx", 0x425C8A: "lea ebx, [r12 + 0xb]", 0x425D0A: "dec ebx",
          0x425D0C: "shl esi, 0x10", 0x425D0F: "sub ebx, esi", 0x425D11: "lea eax, [rbx + 0x10000]", 0x425D5D: "ret"})
minus_one = [a for a, s in txt.items() if s in ("or eax, 0xffffffff", "mov eax, 0xffffffff")]
check("R", res and not minus_one, "result = index + ((1 - esi) << 16); no -1 in the body: %s" % (not minus_one))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
