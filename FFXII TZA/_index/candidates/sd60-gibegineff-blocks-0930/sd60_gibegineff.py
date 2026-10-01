"""sd60_gibegineff.py - what the GiBeginEff command's two 64-byte blocks and two floats are (OPUS, 2026-09-30; SD-60).
Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c = T.R, T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# F1 - block 1 (command +0x08..+0x47): 64 bytes copied from 0039D1D0(), which returns the global 02AEEB20
check("F1", txt(0x00864F57) == "call 0x39d1d0" and txt(0x00864F5F) == "movups xmmword ptr [rbx + 8], xmm0"
      and txt(0x00864F77) == "movups xmmword ptr [rbx + 0x38], xmm1" and txt(0x0039D1D0).startswith("lea rax, [rip")
      and T.fmt(next(R.md.disasm(R.at(0x0039D1D0, 8), 0x0039D1D0, 1))).endswith("02AEEB20"),
      "block 1 = the 64-byte global 02AEEB20")
# F2 - block 2 (command +0x48..+0x87): the source record's 4 x 4 at +0x30..+0x6F (xmm2 / xmm3 / xmm6 / xmm7), then
#      00678B50(block, near = [src+0xB8], far = [src+0xBC]) rewrites +0x28 / +0x38
check("F2", txt(0x00864FB2) == "movups xmm2, xmmword ptr [rdx + 0x30]" and txt(0x00864FBB) == "movups xmm3, xmmword ptr [rdx + 0x40]"
      and txt(0x00864FC4) == "movups xmm6, xmmword ptr [rdx + 0x50]" and txt(0x00864FCC) == "movups xmm7, xmmword ptr [rdx + 0x60]"
      and txt(0x00865008) == "movss xmm5, dword ptr [rdx + 0xb8]" and txt(0x00865015) == "movss xmm4, dword ptr [rdx + 0xbc]"
      and txt(0x00865055) == "lea rcx, [rbx + 0x48]" and txt(0x008650F0) == "movaps xmm2, xmm4" and txt(0x008650F3) == "movaps xmm1, xmm5"
      and txt(0x008650F6) == "call 0x678b50",
      "block 2 = source +0x30..+0x6F, depth terms recomputed from source +0xB8 / +0xBC")
# F3 - 00678B50: with m33 (+0x3C) == 0 (perspective) m22 = f / (n - f), m32 = n f / (n - f); otherwise (orthographic)
#      m22 = 1 / (n - f), m32 = n / (n - f) - the Direct3D right-handed projection depth terms (n = xmm1, f = xmm2)
one = struct.unpack("<f", R.at(0x01CEBBA8, 4))[0]
seq = [txt(a) for a in (0x00678B50, 0x00678B62, 0x00678B65, 0x00678B69, 0x00678B70, 0x00678B74, 0x00678B78, 0x00678B7D,
                        0x00678B8B, 0x00678B8F, 0x00678B93)]
check("F3", seq == ["movss xmm3, dword ptr [rcx + 0x3c]", "movaps xmm3, xmm1", "mulss xmm4, xmm2", "subss xmm3, xmm2",
                    "divss xmm0, xmm3", "divss xmm4, xmm3", "movss dword ptr [rcx + 0x28], xmm0", "movss dword ptr [rcx + 0x38], xmm4",
                    "subss xmm1, xmm2", "divss xmm0, xmm1", "divss xmm4, xmm1"] and one == 1.0,
      "perspective: m22 = f/(n-f), m32 = n*f/(n-f); orthographic: m22 = 1/(n-f), m32 = n/(n-f)")
# F4 - the two floats: command +0x88 = 0039D1F0() = [02AEEBA0], +0x8C = 0039D1E0() = [02AEEBA4], both written as a
#      pair by 0024FF60
w = sorted((f, a) for g in (0x02AEEBA0, 0x02AEEBA4) for f, a, k in c["refs"].get(g, ()) if k == "W")
check("F4", txt(0x008650FB) == "call 0x39d1f0" and txt(0x00865100) == "movss dword ptr [rbx + 0x88], xmm0"
      and txt(0x00865108) == "call 0x39d1e0" and txt(0x0086510D) == "movss dword ptr [rbx + 0x8c], xmm0"
      and all(f == 0x0024FF60 for f, _ in w) and len(w) == 4,
      "floats from 02AEEBA0 / 02AEEBA4, written only by 0024FF60 (%d stores)" % len(w))
# F5 - where 02AEEB20 and the floats come from: 003820C0 calls 0024E180(02AEDD30), which stores the mat4 inverse
#      (00202D60 -> 00216720) of that matrix at 02AEEB20 - substituting 00915518 / 0091551C for m00 / m11 when both are 0;
#      002F5550 calls 0024FF60, whose pair is a = g([cam+0xCC0]) + 3.0, b = g([cam+0xCBC]) - 3.0, both (a + b) * 0.5 when
#      a > b; g = 003B40F0 maps a distance d through the matrix 02B40470 (set by 003B4150 just before each publish):
#      (m[+0x38] - d m[+0x28]) / (m[+0x3C] - d m[+0x2C])
check("F5", txt(0x003828D4).endswith("0x276b455]") and txt(0x003828DB) == "call 0x24e180" and txt(0x0024E1F5) == "call 0x202d60"
      and txt(0x00202D60) == "jmp 0x216720" and txt(0x002F58B8) == "call 0x3b4150" and txt(0x002F58BD) == "call 0x24ff60"
      and txt(0x003828CF) == "call 0x3b4150" and txt(0x001867D0) == "movss xmm0, dword ptr [rcx + 0xcc0]"
      and txt(0x00186970) == "movss xmm0, dword ptr [rcx + 0xcbc]" and struct.unpack("<d", R.at(0x00915510, 8))[0] == 3.0
      and struct.unpack("<d", R.at(0x01CEBBD8, 8))[0] == 0.5 and txt(0x003B4153).endswith("0x278c316]")
      and txt(0x003B4133) == "divsd xmm3, xmm0",
      "block 1 = inverse of 02AEDD30; floats = the camera's two distances mapped through 02B40470, +3 / -3, midpoint if crossed")
# F6 - execute (slot 1, 00864E90): 00210520(+0x08 block, +0x88, +0x8C) stores them at 01FD3620..01FD365F / 01FD3660 /
#      01FD3664; the +0x48 block goes to the device's +0x30 - PrimitiveRendererD3D11 (00D86960) slot 006CAF40 copies its
#      16 dwords to renderer +0x10..+0x4F and sets byte +0x208F3 = 1
vt = struct.unpack("<3Q", R.at(0x01CCFB78, 24))
check("F6", vt[:2] == (0x00864F30, 0x00864E90) and txt(0x00864ECA) == "lea rcx, [rbx + 8]" and txt(0x00864ED6) == "call 0x210520"
      and txt(0x00864EDE) == "lea rdx, [rbx + 0x48]" and txt(0x00864EE5) == "call qword ptr [rax + 0x30]"
      and T.rtti_class(0x00D86960) == "PrimitiveRendererD3D11" and struct.unpack("<Q", R.at(0x00D86990, 8))[0] == 0x006CAF40
      and txt(0x006CAF42) == "mov dword ptr [rcx + 0x10], eax" and txt(0x006CAF9C) == "mov dword ptr [rcx + 0x4c], eax"
      and txt(0x006CAFA1) == "mov byte ptr [rcx + 0x208f3], 1" and txt(0x0021052B) == "movaps xmmword ptr [rip + 0x1dc30ee], xmm0",
      "execute: block 1 + floats -> 01FD3620..01FD3664; block 2 -> PrimitiveRendererD3D11 +0x10..+0x4F, dirty byte +0x208F3")
print("FAILS %d" % fails)
