"""check_sd197.py - FABLE verification record, 2026-10-03.

Re-derives from the shipping image every load-bearing claim of the cloud draft for SD-197 (the planar-scalar track
evaluators 004309C0 / 00430540 / 004307C0), then evaluates the shipped kind-0x54 pass slots' planar-scalar tracks.

Sections
  S  static anchors: the instruction each claim rests on (rvlib Body decode of the listed extents)
  E  execution: the original bytes of 004309C0 (and everything it reaches) run under Unicorn against a float32
     reference model of the decoded semantics, over seeded random records; bit-exact comparison
  C  controls: deliberately wrong readings / patched images that MUST be rejected
  D  shipped data: every active type-0x05 mode-2 pass slot's planar-scalar track (the 16-byte record 0x10 bytes
     before the slot), resolved through the setup rebase and evaluated by the original bytes

Stubs (the only non-original code executed): 00861F14 (an import thunk to CRT sqrtf; replaced by a correctly rounded
float32 sqrt), 00808C40 (the stack-cookie check; replaced by `ret`), and in section E the random scaler 003D8E50
(replaced by a deterministic recorder F(x) = x * 0.6171875 so each combine arm's formula can be checked exactly;
section E8 runs the real 003D8E50).

Run: python check_sd197.py > check_sd197.out   (exit 1 when any non-control check fails)
"""
import collections
import os
import random
import struct
import sys

import numpy as np

RV = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\fable-review-astra-ov42-caller-quotient-bound-1002"
sys.path.insert(0, RV)
from rvlib import Img, Report, Body, expect  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP,  # noqa: E402
                               UC_X86_REG_RIP, UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_XMM2,
                               UC_X86_REG_R8)

HERE = os.path.dirname(os.path.abspath(__file__))
f32 = np.float32
np.seterr(all="ignore")

EXT = {0x4309C0: 155, 0x430540: 634, 0x4307C0: 238, 0x20E600: 10, 0x39B6E0: 147, 0x39B630: 170, 0x3D8E50: 418}


def fbits(x):
    return struct.unpack("<I", struct.pack("<f", float(x)))[0]


def bitsf(u):
    return f32(struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0])


def i32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x & 0x80000000 else x


def same(a, b):
    a, b = f32(a), f32(b)
    if np.isnan(a) and np.isnan(b):
        return True
    return fbits(a) == fbits(b)


# ================================================================================================ S: static
def static_checks(img, R):
    B = {a: Body(img, a, a + n) for a, n in EXT.items()}
    for a, b in B.items():
        R.check("S0 %08X decodes exactly over its %d-byte extent" % (a, EXT[a]), b.exact)
    X = lambda a, t: expect(R, B[[f for f in B if f <= a < f + EXT[f]][0]], a, t)  # noqa: E731
    R.note("-- record fields read by 004309C0 (rcx = record, edx = time)")
    for a, t in [(0x4309CA, "movzx eax, byte ptr [rcx + 0xc]"), (0x4309CE, "mov edi, edx"),
                 (0x4309D5, "mov rbx, rcx"), (0x4309DC, "xorps xmm6, xmm6"),
                 (0x4309E1, "cmp eax, 1"), (0x4309E6, "mov ecx, dword ptr [rcx]"), (0x4309E8, "call 0x20e600"),
                 (0x4309ED, "movss xmm6, dword ptr [rax + 4]"), (0x4309F4, "xor r8d, r8d"),
                 (0x4309F7, "call 0x430540"), (0x4309FF, "movzx eax, byte ptr [rbx + 0xd]"),
                 (0x430A05, "jne 0x430a1a"), (0x430A07, "movaps xmm0, xmm6"), (0x430A19, "ret"),
                 (0x430A1F, "mov ecx, dword ptr [rbx + 4]"), (0x430A27, "movss xmm0, dword ptr [rax + 4]"),
                 (0x430A2E, "mov r8d, 1"), (0x430A34, "mov edx, edi"), (0x430A3E, "movaps xmm2, xmm0"),
                 (0x430A41, "movaps xmm1, xmm6"), (0x430A44, "mov rcx, rbx"), (0x430A56, "jmp 0x4307c0")]:
        X(a, t)
    rets, tails, outs = B[0x4309C0].exits()
    R.check("S1 004309C0 has exactly one ret (00430A19) and one tail jump (00430A56 -> 004307C0)",
            rets == [0x430A19] and tails == [(0x430A56, 0x4307C0)] and not outs, "%s %s %s" % (rets, tails, outs))
    R.note("-- 00430540 (rcx = record, edx = time, r8d = channel)")
    for a, t in [(0x43055F, "movsxd rsi, r8d"), (0x430562, "mov ebx, edx"), (0x430564, "mov rdi, rcx"),
                 (0x430567, "test r8d, r8d"), (0x43056A, "jne 0x430579"), (0x43056C, "mov ecx, dword ptr [rcx]"),
                 (0x43056E, "call 0x20e600"), (0x430573, "movzx ecx, word ptr [rdi + 0xe]"),
                 (0x430579, "mov ecx, dword ptr [rcx + 4]"), (0x43057C, "call 0x20e600"),
                 (0x430581, "movzx ecx, word ptr [rdi + 0xe]"), (0x430585, "shr ecx, 2"),
                 (0x430588, "mov r8, rax"), (0x43058B, "and ecx, 3"),
                 (0x43058E, "movzx eax, word ptr [rdi + rsi*2 + 8]"), (0x430596, "test ax, ax"),
                 (0x430599, "je 0x4305ac"), (0x43059F, "cmp ebx, r9d"), (0x4305A2, "jle 0x4305ac"),
                 (0x4305A6, "cdq"), (0x4305A7, "idiv r9d"), (0x4305AA, "mov ebx, edx"),
                 (0x4305B4, "test ecx, ecx"), (0x4305B6, "je 0x43073b"), (0x4305BC, "cmp ecx, 1"),
                 (0x4305BF, "je 0x4305c9"), (0x4305C1, "xorps xmm0, xmm0"), (0x4305C4, "jmp 0x43079a"),
                 (0x4305C9, "movzx eax, byte ptr [rsi + rdi + 0xc]"), (0x4305CE, "cmp al, 2"),
                 (0x4305D0, "jbe 0x43073b"),
                 (0x4305E7, "movss xmm1, dword ptr [rbp - 0x21]"), (0x4305EC, "movss xmm3, dword ptr [rbp - 0x25]"),
                 (0x430600, "mov ecx, dword ptr [r8]"), (0x430603, "movss xmm2, dword ptr [r8 + 4]"),
                 (0x430609, "add r8, 8"), (0x43060D, "cmp ecx, ebx"), (0x43060F, "jge 0x43062a"),
                 (0x430625, "jmp 0x430797"), (0x43062A, "test r9d, r9d"), (0x43062D, "je 0x430797"),
                 (0x430633, "mov eax, ecx"), (0x430635, "sub eax, r10d"), (0x430638, "cdq"),
                 (0x430639, "sub eax, edx"), (0x43063B, "sar eax, 1"), (0x43063D, "add eax, r10d"),
                 (0x430640, "cmp r9d, 1"), (0x430644, "jne 0x43064f"), (0x430646, "cmp ebx, eax"),
                 (0x430648, "jg 0x430696"), (0x43064A, "jmp 0x430762"), (0x43064F, "cmp ebx, eax"),
                 (0x430651, "jg 0x43068a"), (0x43068A, "lea eax, [rsi - 1]"), (0x43068D, "cmp r9d, eax"),
                 (0x430690, "je 0x430762"), (0x4306B9, "movd xmm0, dword ptr [r8]"),
                 (0x4306C6, "movss xmm1, dword ptr [r8 + 4]"), (0x4306E5, "cvtdq2ps xmm6, xmm6"),
                 (0x4306EB, "call 0x39b6e0"), (0x4306F0, "movss xmm0, dword ptr [rbp - 0x39]"),
                 (0x4306F5, "ucomiss xmm0, dword ptr [rip + 0x18bb50c]"), (0x430727, "call 0x39b630"),
                 (0x43072C, "movss xmm2, dword ptr [rbp - 0x25]"),
                 (0x43073B, "movss xmm3, dword ptr [rbp - 0x25]"), (0x430740, "xorps xmm2, xmm2"),
                 (0x430743, "mov r10d, dword ptr [rbp - 0x25]"), (0x43074A, "movzx eax, byte ptr [r11 + rdi + 0xc]"),
                 (0x430750, "cmp r9d, eax"), (0x430753, "jge 0x430797"), (0x430762, "cmp ecx, ebx"),
                 (0x430764, "je 0x430797"), (0x430766, "jg 0x430773"), (0x430773, "subss xmm2, xmm3"),
                 (0x430777, "sub ebx, r10d"), (0x43077A, "sub ecx, r10d"), (0x43078F, "divss xmm2, xmm1"),
                 (0x430793, "addss xmm2, xmm3"), (0x430797, "movaps xmm0, xmm2"),
                 (0x4307A9, "call 0x808c40"), (0x4307B9, "ret")]:
        X(a, t)
    R.check("S2 the curve's degenerate sentinel 01CEBC08 is the float 2.0 (the ucomiss at 004306F5 reads it)",
            0x4306F5 + 7 + 0x18BB50C == 0x1CEBC08 and img.read(0x1CEBC08, 4) == struct.pack("<f", 2.0))
    R.note("-- 0039B6E0 (solve x(t) = v) and 0039B630 (the quadratic B-spline), read whole")
    for a, t in [(0x39B6E6, "movss xmm2, dword ptr [rdx + 0x10]"), (0x39B6EF, "movss xmm3, dword ptr [rdx]"),
                 (0x39B720, "addss xmm6, dword ptr [rdx + 0x20]"), (0x39B72C, "mov dword ptr [r8], 0x40000000"),
                 (0x39B752, "call 0x861f14"), (0x39B769, "movss dword ptr [rbx], xmm0"),
                 (0x39B665, "mulss xmm0, dword ptr [rdx]"), (0x39B697, "mulss xmm3, dword ptr [rdx + 0x14]"),
                 (0x39B69C, "mulss xmm0, dword ptr [rdx + 4]"), (0x39B6A1, "mulss xmm1, dword ptr [rdx + 0x24]"),
                 (0x39B6AE, "movss dword ptr [r8 + 4], xmm3")]:
        X(a, t)
    rd = sorted(set((m["disp"]) for a in B[0x39B6E0].order for m in B[0x39B6E0][a].mems
                    if m["base"] == "rdx"))
    rd2 = sorted(set((m["disp"]) for a in B[0x39B630].order for m in B[0x39B630][a].mems
                     if m["base"] == "rdx"))
    R.check("S3 0039B6E0 reads only lane 0 of the three points (rdx + 0x0 / 0x10 / 0x20)", rd == [0, 0x10, 0x20],
            str([hex(x) for x in rd]))
    R.check("S3b 0039B630 reads lanes 0-2 of each point, never lane 3 (rdx + 0xC / 0x1C / 0x2C)",
            rd2 == [0, 4, 8, 0x10, 0x14, 0x18, 0x20, 0x24, 0x28], str([hex(x) for x in rd2]))
    R.check("S3c 0039B630 constants: [01CEBBA8] = 1.0, [01CEBB70] = 0.5",
            0x39B63C + 0x195056C == 0x1CEBBA8 and 0x39B644 + 0x195052C == 0x1CEBB70 and
            img.read(0x1CEBBA8, 4) == struct.pack("<f", 1.0) and img.read(0x1CEBB70, 4) == struct.pack("<f", 0.5))
    R.check("S3d 00861F14 is an import thunk to sqrtf (the one stub on the curve path)",
            img.import_name_of_thunk(0x861F14) == "sqrtf", str(img.import_name_of_thunk(0x861F14)))
    R.note("-- 004307C0 (rcx = record, xmm1 = a, xmm2 = b)")
    for a, t in [(0x4307D1, "movaps xmm6, xmm1"), (0x4307D4, "movaps xmm7, xmm2"), (0x4307D7, "ucomiss xmm7, xmm0"),
                 (0x4307DA, "jp 0x43080f"), (0x4307DC, "jne 0x43080f"),
                 (0x4307DE, "movzx ecx, word ptr [rcx + 0xe]"), (0x4307E2, "shr ecx, 4"),
                 (0x4307E5, "and ecx, 0xf"), (0x4307E8, "sub ecx, 4"), (0x4307EB, "je 0x4307fd"),
                 (0x4307ED, "cmp ecx, 1"), (0x4307F0, "jne 0x4307fd"), (0x4307F2, "subss xmm7, xmm6"),
                 (0x4307F9, "jp 0x430833"), (0x4307FB, "jne 0x430833"), (0x4307FD, "movaps xmm0, xmm6"),
                 (0x43080F, "movzx eax, word ptr [rcx + 0xe]"), (0x430813, "shr eax, 4"), (0x430816, "and eax, 0xf"),
                 (0x430819, "cmp eax, 5"), (0x43081C, "ja 0x4307fd"), (0x43081E, "lea rdx, [rip - 0x310825]"),
                 (0x430827, "mov ecx, dword ptr [rdx + rax*4 + 0x3108b0]"), (0x43082E, "add rcx, rdx"),
                 (0x430831, "jmp rcx"), (0x430833, "movaps xmm0, xmm7"), (0x430836, "call 0x3d8e50"),
                 (0x43083B, "addss xmm0, xmm6"), (0x43084E, "movaps xmm0, xmm7"), (0x430851, "call 0x3d8e50"),
                 (0x430856, "subss xmm6, xmm0"), (0x43086C, "movaps xmm0, xmm7"), (0x43086F, "addss xmm0, xmm7"),
                 (0x430873, "call 0x3d8e50"), (0x430878, "addss xmm0, xmm6"), (0x43087C, "subss xmm0, xmm7"),
                 (0x43088F, "movaps xmm0, xmm7"), (0x430892, "call 0x3d8e50"), (0x43089C, "mulss xmm0, xmm6"),
                 (0x4308A0, "addss xmm0, xmm6")]:
        X(a, t)
    R.check("S4 004307C0's table base: lea at 0043081E forms 00120000 (the image base), table at 004308B0",
            0x430825 - 0x310825 == img.base == 0x120000 and img.base + 0x3108B0 == 0x4308B0)
    tab = check_table(img)
    R.check("S5 jump table 004308B0, m = 0..5 -> 004307FD (a), 00430833 (a+F(b)), 0043084E (a-F(b)), "
            "0043086C (F(2b)+a-b), 0043088F (F(b)*a+a), 004307F2 (b-a == 0 ? a : F(b-a)+a)",
            tab == [0x4307FD, 0x430833, 0x43084E, 0x43086C, 0x43088F, 0x4307F2], str(["%08X" % x for x in tab]))
    R.note("-- 0020E600 (the handle resolver), read whole")
    for a, t in [(0x20E600, "mov eax, ecx"), (0x20E602, "add rax, qword ptr [rip + 0x1d74f27]"), (0x20E609, "ret")]:
        X(a, t)
    R.check("S6 0020E600 adds the qword at 01F83530 to the zero-extended ecx", 0x20E609 + 0x1D74F27 == 0x1F83530)
    R.note("-- caller context: the planar scalar of pass p (00449AB0, the type-0x05 walk)")
    W = Body(img, 0x449F80, 0x44A03F)
    for a, t in [(0x449FE8, "mov edx, dword ptr [r15 + 0x44]"), (0x449FEC, "lea rcx, [rsi + 0x90]"),
                 (0x449FF3, "call 0x4309c0"), (0x44A017, "movss dword ptr [rcx + 0xa0], xmm0")]:
        expect(R, W, a, t)
    S = Body(img, 0x538DB0, 0x538EAE)
    for a, t in [(0x538E22, "lea rbx, [rbp + 0x1b0]"), (0x538E35, "call 0x431770"), (0x538E3A, "add rbx, 0xf0")]:
        expect(R, S, a, t)
    RB = Body(img, 0x431770, 0x431821)
    for a, t in [(0x43178F, "mov ecx, dword ptr [rdi + 0x90]"), (0x43179A, "lea rcx, [rbx + rax]"),
                 (0x43179E, "call 0x20e620"), (0x4317A9, "mov dword ptr [rdi + 0x90], eax"),
                 (0x4317A3, "mov ecx, dword ptr [rdi + 0x94]"), (0x4317BD, "mov dword ptr [rdi + 0x94], eax")]:
        expect(R, RB, a, t)
    H = Body(img, 0x3A9A70, 0x3A9AC4)
    for a, t in [(0x3A9A81, "add rcx, 4"), (0x3A9AA5, "mov edx, dword ptr [rip + 0x2b11c8d]"),
                 (0x3A9AAB, "add edx, ecx"), (0x3A9AAD, "call 0x5004c0")]:
        expect(R, H, a, t)
    R.check("S7 the setup's rebase delta is low32(record) + [02EBB738] (the chunk's +0x08 i32, stored by the loader)",
            0x3A9AAB + 0x2B11C8D == 0x2EBB738)


def check_table(img):
    return [img.u32(0x4308B0 + 4 * i) + img.base for i in range(6)]


# ================================================================================================ E: execution
BASE = 0x120000
KEYS = 0x10000000
RECPG = 0x11000000
REC = RECPG + 0xFF0          # the 16-byte record ends exactly at the end of its mapped page
STACK = 0x20000000
RET = 0x30000000
FK = f32(0.6171875)


class Emu(object):
    def __init__(self, img, stub_f=True):
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pe = struct.unpack_from("<I", img.d, 0x3C)[0]
        size_img = (struct.unpack_from("<I", img.d, pe + 24 + 56)[0] + 0xFFF) & ~0xFFF
        mu.mem_map(BASE, size_img)
        mu.mem_write(BASE, img.d[:0x1000])
        for name, va, vs, ra, rs in img.secs:
            mu.mem_write(BASE + va, img.d[ra:ra + min(rs, vs if vs else rs)])
        mu.mem_map(KEYS, 0x100000)
        mu.mem_map(RECPG, 0x1000)
        mu.mem_map(STACK, 0x100000)
        mu.mem_map(RET, 0x1000)
        mu.mem_write(RET, b"\xf4")
        self.mu = mu
        self.fault = None
        self.fcalls = []
        self.fmode = "k"
        mu.hook_add(UC_HOOK_MEM_UNMAPPED, self._unm)
        self.stub(0x861F14, self._sqrtf)
        self.stub(0x808C40, lambda: None)
        if stub_f:
            self.stub(0x3D8E50, self._F)

    def _unm(self, mu, access, addr, size, value, ud):
        self.fault = ("unmapped", access, hex(addr), hex(mu.reg_read(UC_X86_REG_RIP)))
        return False

    def stub(self, addr, fn):
        def hit(mu, a, size, ud):
            fn()
            rsp = mu.reg_read(UC_X86_REG_RSP)
            mu.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", bytes(mu.mem_read(rsp, 8)))[0])
            mu.reg_write(UC_X86_REG_RSP, rsp + 8)
        self.mu.hook_add(UC_HOOK_CODE, hit, begin=addr, end=addr)

    def xin(self, reg=UC_X86_REG_XMM0):
        return bitsf(self.mu.reg_read(reg) & 0xFFFFFFFF)

    def xout(self, v):
        self.mu.reg_write(UC_X86_REG_XMM0, fbits(v))

    def _sqrtf(self):
        self.xout(np.sqrt(self.xin()))

    def _F(self):
        x = self.xin()
        self.fcalls.append(x)
        if self.fmode == "k":
            self.xout(f32(x * FK))
        elif self.fmode == "zero":
            self.xout(f32(0.0))
        else:                       # "id": the bound itself
            self.xout(x)

    def w(self, a, b):
        self.mu.mem_write(a, bytes(b))

    def run(self, fn, rcx, edx=0, xmm1=None, xmm2=None, fill=b"\0"):
        mu = self.mu
        rsp = STACK + 0xF0000
        mu.mem_write(rsp - 0x3000, (fill * (0x3000 // len(fill) + 1))[:0x3000])
        mu.mem_write(rsp, struct.pack("<Q", RET) + b"\0" * 0x40)
        mu.reg_write(UC_X86_REG_RSP, rsp)
        mu.reg_write(UC_X86_REG_RCX, rcx)
        mu.reg_write(UC_X86_REG_RDX, edx & 0xFFFFFFFF)
        if xmm1 is not None:
            mu.reg_write(UC_X86_REG_XMM1, fbits(xmm1))
        if xmm2 is not None:
            mu.reg_write(UC_X86_REG_XMM2, fbits(xmm2))
        self.fault = None
        self.fcalls = []
        try:
            mu.emu_start(fn, RET, count=2_000_000)
        except Exception as e:  # noqa: BLE001
            self.fault = self.fault or ("exception", str(e))
        ok = self.fault is None and mu.reg_read(UC_X86_REG_RIP) == RET
        return ok


# ------------------------------------------------------------------ the reference model (the draft's reading, as decoded)
class Ref(object):
    """Float32 model of 004309C0 / 00430540 / 004307C0 / 0039B6E0 / 0039B630, operation order copied from the bytes.
    Variant switches implement the deliberately WRONG readings the controls must reject."""

    def __init__(self, period_off=8, wrap_ge=False, swap12=False, fmode="k"):
        self.period_off, self.wrap_ge, self.swap12, self.fmode = period_off, wrap_ge, swap12, fmode
        self.paths = collections.Counter()
        self.fcalls = []

    def F(self, x):
        x = f32(x)
        self.fcalls.append(x)
        return f32(x * FK) if self.fmode == "k" else (f32(0.0) if self.fmode == "zero" else x)

    @staticmethod
    def b6e0(v, X):
        x0, x1, x2 = X
        xmm0 = f32(v + v)
        xmm1 = f32(x1 + x1)
        xmm7 = f32(x1 - x0)
        xmm3 = f32(x0 + x1)
        xmm6 = f32(x0 - xmm1)
        xmm3 = f32(xmm3 - xmm0)
        xmm6 = f32(xmm6 + x2)
        if xmm6 == f32(0.0):
            return f32(2.0)
        xmm3 = f32(xmm3 * xmm6)
        xmm0 = f32(xmm7 * xmm7)
        xmm0 = f32(xmm0 - xmm3)
        xmm0 = f32(np.sqrt(xmm0))
        xmm0 = f32(xmm0 - xmm7)
        return f32(xmm0 / xmm6)

    @staticmethod
    def b630_y(t, Y):
        y0, y1, y2 = Y
        xmm5 = f32(f32(1.0) - t)
        xmm4 = f32(f32(xmm5 * f32(0.5)) * xmm5)       # w0 = 0.5 (1-t)^2
        xmm5 = f32(xmm5 * t)
        xmm6 = f32(t * t)
        xmm5 = f32(xmm5 + f32(0.5))                    # w1 = (1-t) t + 0.5
        xmm6 = f32(xmm6 * f32(0.5))                    # w2 = 0.5 t^2
        return f32(f32(f32(xmm5 * y1) + f32(xmm4 * y0)) + f32(xmm6 * y2))

    def lin(self, K, cnt, t, res):
        pf, pv = res
        v = f32(0.0)
        for i in range(cnt):
            f, v = K[i]
            if f == t:
                self.paths["linear: exact key frame"] += 1
                return v
            if f > t:
                self.paths["linear: interpolate" + (" (BEFORE the first key: stack residue)" if i == 0 else "")] += 1
                return self.tail_interp((pf, pv), (f, v), t)
            pf, pv = f, v
        self.paths["linear: " + ("count 0 -> 0.0" if cnt == 0 else "after the last key -> last value")] += 1
        return v

    @staticmethod
    def tail_interp(P, Q, t):
        pf, pv = P
        f, v = Q
        x = f32(v - pv)
        x = f32(x * f32(i32(t - pf)))
        x = f32(x / f32(i32(f - pf)))
        return f32(x + pv)

    def tail(self, P, Q, t):
        if Q[0] == t:
            self.paths["curve->linear tail: exact"] += 1
            return Q[1]
        self.paths["curve->linear tail: interpolate"] += 1
        return self.tail_interp(P, Q, t)

    def curve(self, K, cnt, t, st):
        i = 0
        while i < cnt and not (K[i][0] >= t):
            i += 1
        if i == cnt:
            self.paths["curve: after the last key -> last value"] += 1
            return K[cnt - 1][1]
        if i == 0:
            self.paths["curve: at/before the first key -> key 0 value"] += 1
            return K[0][1]
        fp, f = K[i - 1][0], K[i][0]
        d = i32(f - fp)
        half = d // 2 if d >= 0 else -((-d) // 2)
        mid = i32(fp + half)
        if i == 1:
            if t > mid:
                W, tag = (K[0], K[1], K[2]), "curve: window keys 0,1,2"
            else:
                return self.tail(K[0], K[1], t)
        else:
            if t <= mid:
                W, tag = (K[i - 2], K[i - 1], K[i]), "curve: window i-2,i-1,i"
            elif i == cnt - 1:
                return self.tail(K[i - 1], K[i], t)
            else:
                W, tag = (K[i - 1], K[i], K[i + 1]), "curve: window i-1,i,i+1"
        X = [f32(p[0]) for p in W]
        Y = [p[1] for p in W]
        T = f32(t)
        u = self.b6e0(T, X)
        if u == f32(2.0):
            tag += " (2.0 sentinel -> linear parameter)"
            u = f32(f32(f32(f32(T + T) - X[0]) - X[1]) / f32(X[2] - X[0]))
        self.paths[tag] += 1
        y = self.b630_y(u, Y)
        st["res"] = (i32(fbits(y)), y)          # B630's output lane 1 lands on [rbp-0x25]
        return y

    def channel(self, rec, K, c, t, st):
        cnt = rec[0xC + c]
        flags = struct.unpack_from("<H", rec, 0xE)[0]
        sel = (flags >> (2 * c)) & 3
        period = struct.unpack_from("<H", rec, self.period_off + 2 * c)[0]
        if period and (t >= period if self.wrap_ge else t > period):
            t = t % period
            self.paths["period wrap"] += 1
        if sel == 0 or (sel == 1 and cnt <= 2):
            return self.lin(K, cnt, t, st["res"])
        if sel == 1:
            return self.curve(K, cnt, t, st)
        self.paths["selector %d -> 0.0" % sel] += 1
        return f32(0.0)

    def combine(self, rec, a, b):
        m = (struct.unpack_from("<H", rec, 0xE)[0] >> 4) & 0xF
        if b == f32(0.0):
            if m == 5:
                d = f32(b - a)
                if d == f32(0.0):
                    self.paths["combine b=0 m=5, a=0 -> a"] += 1
                    return a
                self.paths["combine b=0 m=5 -> F(-a)+a"] += 1
                return f32(self.F(d) + a)
            self.paths["combine b=0 m=%s -> a" % ("4" if m == 4 else "other")] += 1
            return a
        if m == 0 or m > 5:
            self.paths["combine m=0/>5 -> a"] += 1
            return a
        if self.swap12 and m in (1, 2):
            m = 3 - m
        self.paths["combine m=%d" % m] += 1
        if m == 1:
            return f32(self.F(b) + a)
        if m == 2:
            return f32(a - self.F(b))
        if m == 3:
            return f32(f32(self.F(f32(b + b)) + a) - b)
        if m == 4:
            return f32(f32(self.F(b) * a) + a)
        d = f32(b - a)
        if d == f32(0.0):
            return a
        return f32(self.F(d) + a)

    def top(self, rec, KS, t, res0=(0, f32(0.0))):
        st = {"res": res0}
        self.fcalls = []
        k0, k1 = rec[0xC], rec[0xD]
        if k0 == 0:
            a = f32(0.0)
        elif k0 == 1:
            a = KS[0][0][1]
        else:
            a = self.channel(rec, KS[0], 0, t, st)
        if k1 == 0:
            self.paths["channel 1 count 0 -> return a (no combine)"] += 1
            return a
        b = KS[1][0][1] if k1 == 1 else self.channel(rec, KS[1], 1, t, st)
        return self.combine(rec, a, b)


def gen_case(rng):
    """One random record + key arrays + time. Returns (rec bytes with emulator handles, KS, t)."""
    KS = []
    rec = bytearray(16)
    addr = KEYS
    for c in (0, 1):
        cnt = rng.choice([0, 1, 1, 2, 3, 3, 4, 5, 6, 8])
        start = rng.randint(-5, 30)
        eq = rng.random() < 0.25                       # equally spaced frames reach the 2.0 sentinel
        step = rng.randint(1, 12)
        fr, x = [], start
        for _ in range(max(cnt, 1)):
            fr.append(x)
            x += step if eq else rng.randint(1, 15)
        vals = []
        for _ in fr:
            r = rng.random()
            vals.append(f32(0.0) if r < 0.08 else (f32(-0.0) if r < 0.12 else
                        f32(rng.randint(-40, 40)) if r < 0.4 else f32(rng.uniform(-60, 60))))
        K = list(zip(fr, vals))
        KS.append(K)
        struct.pack_into("<I", rec, 4 * c, addr)
        rec[0xC + c] = cnt
        struct.pack_into("<H", rec, 8 + 2 * c, 0 if rng.random() < 0.55 else rng.randint(1, 80))
        addr += 0x100
    flags = rng.randint(0, 0xFFFF)
    if rng.random() < 0.5:                             # favour selectors 0/1 so the key paths dominate
        flags = (flags & ~0xF) | rng.choice([0, 1, 4, 5, 0, 5])
    struct.pack_into("<H", rec, 0xE, flags)
    allf = [f for K in KS for f, _ in K]
    r = rng.random()
    if r < 0.25:
        t = rng.choice(allf)
    elif r < 0.35:
        p = struct.unpack_from("<H", rec, 8)[0] or struct.unpack_from("<H", rec, 0xA)[0]
        t = p if p else rng.randint(-10, 150)
    else:
        t = rng.randint(-10, 150)
    return bytes(rec), KS, t


def load_case(E, rec, KS):
    for c, K in enumerate(KS):
        h = struct.unpack_from("<I", rec, 4 * c)[0]
        E.w(h, b"".join(struct.pack("<iI", f, fbits(v)) for f, v in K))
    E.w(REC, rec)


def exec_top(E, rec, KS, t, fill=b"\0"):
    load_case(E, rec, KS)
    ok = E.run(0x4309C0, REC, t, fill=fill)
    return ok, (E.xin() if ok else None)


def exec_checks(img, R):
    E = Emu(img)
    rng = random.Random(197)
    ref = Ref()
    N = 6000
    cases = [gen_case(rng) for _ in range(N)]
    bad, faults, fbad = [], 0, 0
    for rec, KS, t in cases:
        ok, got = exec_top(E, rec, KS, t)
        if not ok:
            faults += 1
            continue
        want = ref.top(rec, KS, t)
        if not same(got, want):
            bad.append((rec.hex(), t, got, want))
        if len(E.fcalls) != len(ref.fcalls) or not all(same(x, y) for x, y in zip(E.fcalls, ref.fcalls)):
            fbad += 1
    R.check("E1 %d seeded random records: 004309C0 executed on the original bytes equals the float32 reference "
            "bit for bit (no fault)" % N, not bad and faults == 0, "mismatch %d fault %d first %s" % (
                len(bad), faults, bad[:2]))
    R.check("E1b the scaler 003D8E50 is called with exactly the reference's arguments, in order (b, 2b, b-a, -a)",
            fbad == 0, "%d cases differ" % fbad)
    for k, v in sorted(ref.paths.items()):
        R.note("   path covered %6d  %s" % (v, k))
    need = ["linear: exact key frame", "linear: interpolate", "linear: after the last key -> last value",
            "linear: interpolate (BEFORE the first key: stack residue)",
            "curve: after the last key -> last value", "curve: at/before the first key -> key 0 value",
            "curve: window keys 0,1,2", "curve: window i-2,i-1,i", "curve: window i-1,i,i+1",
            "curve->linear tail: exact", "curve->linear tail: interpolate", "selector 2 -> 0.0", "selector 3 -> 0.0",
            "period wrap", "combine m=1", "combine m=2", "combine m=3", "combine m=4", "combine m=5",
            "combine m=0/>5 -> a", "combine b=0 m=4 -> a", "combine b=0 m=5 -> F(-a)+a", "combine b=0 m=other -> a",
            "channel 1 count 0 -> return a (no combine)"]
    miss = [k for k in need if ref.paths[k] == 0]
    sent = sum(v for k, v in ref.paths.items() if "2.0 sentinel" in k)
    R.check("E1c every decoded path was exercised at least once (incl. the 2.0 sentinel: %d)" % sent,
            not miss and sent > 0, str(miss))
    R.check("E1d 00430540's own count-0 exit (0043074A..00430753 -> 0.0) is never reached from 004309C0: counts 0 and 1 "
            "are taken by 004309C0 before the call", ref.paths["linear: count 0 -> 0.0"] == 0)

    # E2 flag bits 8-15 are never read: flip the high byte of +0xE
    diff = 0
    for rec, KS, t in cases[:800]:
        r2 = bytearray(rec)
        r2[0xF] ^= 0xA5
        a = exec_top(E, rec, KS, t)[1]
        b = exec_top(E, bytes(r2), KS, t)[1]
        diff += not same(a, b)
    R.check("E2 flag bits 8-15 (+0xF) change nothing (800 records, high byte flipped)", diff == 0, "%d differ" % diff)

    # E3 the record is at most 16 bytes: it ends exactly at the end of its mapped page and no run faulted (E1)
    R.check("E3 no read at or above record +0x10: all %d runs had the record's last byte on the page end, 0 faults" % N,
            faults == 0)

    # E4 the before-first-key residue
    res_cases, inv_cases = [], []
    for rec, KS, t in cases:
        r = Ref()
        r.top(rec, KS, t)
        if r.paths["linear: interpolate (BEFORE the first key: stack residue)"]:
            res_cases.append((rec, KS, t))
        elif any(k.startswith("curve") for k in r.paths):
            inv_cases.append((rec, KS, t))
    pat = struct.pack("<I", 0x41200007)          # int 0x41200007, float 10.000007
    changed, model_ok = 0, 0
    for rec, KS, t in res_cases:
        a = exec_top(E, rec, KS, t)[1]
        b = exec_top(E, rec, KS, t, fill=pat)[1]
        changed += not same(a, b)
        model_ok += same(b, Ref().top(rec, KS, t, res0=(0x41200007, bitsf(0x41200007))))
    R.check("E4 linear path, time before the first key: the result follows the stack slot [rbp-0x25] "
            "(%d cases; %d change under a filled stack; the model with that slot as (frame, value) matches %d)" % (
                len(res_cases), changed, model_ok),
            len(res_cases) > 0 and changed > 0 and model_ok == len(res_cases))
    same_n = sum(same(exec_top(E, rec, KS, t)[1], exec_top(E, rec, KS, t, fill=pat)[1]) for rec, KS, t in inv_cases)
    R.check("E4b curve path (selector 1, >= 3 keys): result independent of stack residue, incl. the unwritten "
            "lanes 2-3 of the three points (%d cases)" % len(inv_cases), same_n == len(inv_cases) and inv_cases,
            "%d of %d same" % (same_n, len(inv_cases)))

    # E5 0020E600 zero-extends ecx and adds the full qword base
    E.w(0x1F83530, struct.pack("<Q", 0x100000000))
    E.mu.reg_write(UC_X86_REG_RCX, 0xFFFFFFFF80000010)
    E.run(0x20E600, 0xFFFFFFFF80000010)
    rax = E.mu.reg_read(UC_X86_REG_RAX)
    E.w(0x1F83530, struct.pack("<Q", 0))
    R.check("E5 0020E600(ecx = 80000010) with [01F83530] = 1_00000000 returns 1_80000010 (zero-extended, not signed)",
            rax == 0x180000010, hex(rax))

    # E6 count 1 reads the float at +4 of the resolved handle and ignores the time
    rec = bytearray(16)
    struct.pack_into("<I", rec, 0, KEYS)
    rec[0xC] = 1
    E.w(KEYS, struct.pack("<iI", 12345, fbits(3.25)))
    E.w(REC, rec)
    vals = set()
    for t in (-50, 0, 7, 12345, 99999):
        E.run(0x4309C0, REC, t)
        vals.add(fbits(E.xin()))
    R.check("E6 count 1: value = float at handle+4 (3.25) for every time", vals == {fbits(3.25)}, str(vals))

    # E7 the period boundary: t == period is NOT wrapped, t = period + k wraps to k
    rec = bytearray(16)
    struct.pack_into("<I", rec, 0, KEYS)
    rec[0xC] = 2
    struct.pack_into("<H", rec, 8, 10)
    E.w(KEYS, struct.pack("<iIiI", 0, fbits(0.0), 20, fbits(20.0)))
    E.w(REC, rec)
    got = {}
    for t in (10, 11, 15, 21, -3):
        E.run(0x4309C0, REC, t)
        got[t] = float(E.xin())
    R.check("E7 keys (0,0),(20,20), period 10: t=10 -> 10 (not wrapped), 11 -> 1, 15 -> 5, 21 -> 1; t=-3 (not "
            "wrapped, before the first key) uses the residue", got[10] == 10.0 and got[11] == 1.0 and got[15] == 5.0
            and got[21] == 1.0, str(got))

    # E8 the real 003D8E50 behind 004307C0 (gate 022D9138 = 1, documented seed 458DC800)
    ER = Emu(img, stub_f=False)
    ER.w(0x22D9138, struct.pack("<I", 1))
    ER.w(0x1EF93E8, struct.pack("<I", 0x458DC800))
    rec = bytearray(16)
    outs = {1: [], 3: [], 5: []}
    okall = True
    for m in (1, 3, 5):
        struct.pack_into("<H", rec, 0xE, m << 4)
        ER.w(REC, rec)
        for _ in range(200):
            okall &= ER.run(0x4307C0, REC, 0, xmm1=10.0, xmm2=5.0)
            outs[m].append(float(ER.xin()))
    R.check("E8 real 003D8E50, 200 draws each, a = 10, b = 5: m=1 in [10, 15), m=3 in [5, 15), m=5 in (5, 10]",
            okall and all(10 <= x < 15 for x in outs[1]) and all(5 <= x < 15 for x in outs[3]) and
            all(5 < x <= 10 for x in outs[5]) and len(set(outs[1])) > 100,
            "m1 %.3f..%.3f m3 %.3f..%.3f m5 %.3f..%.3f" % (min(outs[1]), max(outs[1]), min(outs[3]), max(outs[3]),
                                                       min(outs[5]), max(outs[5])))
    st0 = bytes(ER.mu.mem_read(0x1EF93E8, 4))
    struct.pack_into("<H", rec, 0xE, 1 << 4)
    ER.w(REC, rec)
    ER.run(0x4307C0, REC, 0, xmm1=10.0, xmm2=0.0)
    r0 = float(ER.xin())
    R.check("E8b b = 0.0, m = 1: returns a (10.0) and draws nothing (state 01EF93E8 unchanged)",
            r0 == 10.0 and bytes(ER.mu.mem_read(0x1EF93E8, 4)) == st0)
    return E, cases


# ================================================================================================ C: controls
def controls(img, R, E, cases):
    def mism(ref):
        n = 0
        for rec, KS, t in cases[:2500]:
            got = exec_top(E, rec, KS, t)[1]
            n += not same(got, ref.top(rec, KS, t))
        return n
    n1 = mism(Ref(period_off=0xA))
    R.check("C1 control: the WRONG reading 'channel c's period is the u16 at +0xA + 2c' is rejected by execution "
            "(%d mismatches)" % n1, n1 > 0)
    n2 = mism(Ref(wrap_ge=True))
    R.check("C2 control: the WRONG reading 'a time equal to the period wraps' is rejected (%d mismatches)" % n2, n2 > 0)
    n3 = mism(Ref(swap12=True))
    R.check("C3 control: the WRONG reading 'm=1 is a-F(b), m=2 is a+F(b)' is rejected (%d mismatches)" % n3, n3 > 0)
    P = img.patched(0x4308B0 + 4, struct.pack("<I", 0x43084E - img.base))
    R.check("C4 control: on a patched image (table slot 1 -> 0043084E) the S5 table check would fail",
            check_table(P) != [0x4307FD, 0x430833, 0x43084E, 0x43086C, 0x43088F, 0x4307F2])
    # C5 the record-bound instrument is sensitive: map only 0xE bytes of the record (record at page end - 0xE)
    E2 = Emu(img)
    rec, KS, t = next((r, k, tt) for r, k, tt in cases if r[0xC] >= 2 and r[0xD] >= 1)
    load_case(E2, rec, KS)
    E2.w(RECPG + 0x1000 - 0xE, rec[:0xE])
    ok = E2.run(0x4309C0, RECPG + 0x1000 - 0xE, t)
    R.check("C5 control: with only 14 record bytes mapped the run faults (the E3 instrument can see a read past "
            "the record)", not ok and E2.fault and E2.fault[0] == "unmapped", str(E2.fault))


# ================================================================================================ D: shipped data
def shipped(img, R):
    MEM = os.path.abspath(os.path.join(HERE, "..", "..", "..", "17-Presentation-Rendering", "Effect-File-Formats",
                                       "members"))
    sys.path.insert(0, MEM)
    import type_census as TC
    std = []
    for dp, dn, fn in os.walk(os.path.join(TC.ROOT, "ps2data")):
        std += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
    std.sort()
    emb = [os.path.join(TC.ROOT, l.strip()) for l in open(TC.EMB) if l.strip()]
    E = Emu(img)
    rows = []
    n_el = 0
    oob = []
    for src, paths in (("std", std), ("emb", emb)):
        for p in paths:
            b = open(p, "rb").read()
            rel = os.path.relpath(p, TC.ROOT).replace("\\", "/")
            for ch, exact in TC.streams(b):
                for ty, o in ch:
                    if ty != 0xA00 or b[o + 0xE] != 0x05:
                        continue
                    n_el += 1
                    ln = struct.unpack_from("<I", b, o)[0]
                    bias = struct.unpack_from("<i", b, o + 8)[0]
                    rec0 = o + 0x10
                    pb = b[rec0 + 0x590]
                    f1 = (((pb >> 5) & 1) << 7) | ((((pb >> 0) | (pb >> 5)) & 1) << 3)
                    path = "00438860" if f1 >= 0x80 else ("00437130" if f1 & 8 else "inline")
                    p_idx = 0
                    for i in range(4):
                        so = rec0 + 0x250 + 0xF0 * i
                        if b[so] == 0:
                            continue
                        mode = b[so + 7]
                        if mode == 2:
                            trk = b[so - 0x10:so]
                            KS, offs = [], []
                            for c in (0, 1):
                                cnt = trk[0xC + c]
                                if cnt == 0:
                                    KS.append([])
                                    offs.append(None)
                                    continue
                                st = struct.unpack_from("<I", trk, 4 * c)[0]
                                fo = rec0 + i32(st + bias)
                                if not (rec0 <= fo and fo + 8 * cnt <= o + ln):
                                    oob.append((rel, hex(o), i, c, hex(st), bias))
                                    KS.append([])
                                    offs.append(None)
                                    continue
                                K = [(struct.unpack_from("<i", b, fo + 8 * k)[0], bitsf(struct.unpack_from(
                                    "<I", b, fo + 8 * k + 4)[0])) for k in range(cnt)]
                                KS.append(K)
                                offs.append(fo - rec0)
                            rows.append(dict(file=rel, src=src, chunk="0x%X" % o, path=path, slot=i, p=p_idx, trk=trk,
                                             KS=KS, offs=offs, bias=bias))
                        p_idx += 1
    R.check("D0 type-0x05 element chunks walked = 5,204 (the census population)", n_el == 5204, str(n_el))
    R.check("D1 every authored handle of a used channel, rebased as stored + low32(record) + bias with "
            "[01F83530] = 0, lands inside its own chunk with room for its keys", not oob, str(oob[:3]))
    R.check("D2 type-0x05 mode-2 slots = 152 (the census)", len(rows) == 152, str(len(rows)))
    kinds = collections.Counter((r["trk"][0xC], r["trk"][0xD]) for r in rows)
    R.note("   (count+0xC, count+0xD) over the 152 slots: %s" % sorted(kinds.items()))
    asc = all(all(K[k][0] < K[k + 1][0] for k in range(len(K) - 1)) for r in rows for K in r["KS"])
    R.check("D3 every shipped key array has strictly ascending frames", asc)

    out = []
    tracks = [r for r in rows if r["trk"][0xC] >= 2 or r["trk"][0xD] >= 2]
    combos = [r for r in rows if r["trk"][0xD] >= 1]
    const1 = [r for r in rows if r["trk"][0xC] == 1 and r["trk"][0xD] == 0]
    R.note("   slots: constant 0.0 (0,0) %d; one resource float (1,0) %d; keyed curve on a channel (count >= 2) %d; "
           "channel 1 present (combine runs) %d" % (kinds[(0, 0)], len(const1), len(tracks), len(combos)))
    cv = collections.Counter(float(r["KS"][0][0][1]) for r in const1)
    R.note("   (1,0) constant values: %s" % sorted(cv.items()))
    resid = 0
    for r in rows:
        trk = r["trk"]
        flags = struct.unpack_from("<H", trk, 0xE)[0]
        sel = [flags & 3, (flags >> 2) & 3]
        m = (flags >> 4) & 0xF
        per = [struct.unpack_from("<H", trk, 8)[0], struct.unpack_from("<H", trk, 0xA)[0]]
        # evaluate by the original bytes: copy the keys to the emulator, point the handles at them
        rec = bytearray(trk)
        for c in (0, 1):
            if r["KS"][c]:
                h = KEYS + 0x1000 * c
                struct.pack_into("<I", rec, 4 * c, h)
                E.w(h, b"".join(struct.pack("<iI", f, fbits(v)) for f, v in r["KS"][c]))
        E.w(REC, bytes(rec))
        lastf = max([K[-1][0] for K in r["KS"] if K] + [0])
        firstf = [K[0][0] if K else None for K in r["KS"]]
        tmax = max([lastf] + per) + 2
        lo, hi = None, None
        flag_res = False
        for c in (0, 1):
            cnt = trk[0xC + c]
            if cnt >= 2 and (sel[c] == 0 or (sel[c] == 1 and cnt <= 2)) and firstf[c] > 0:
                flag_res = True
        resid += flag_res
        for fm in ("zero", "id"):
            E.fmode = fm
            for t in range(0, tmax + 1):
                if flag_res and any(firstf[c] is not None and t < firstf[c] for c in (0, 1)):
                    continue
                E.run(0x4309C0, REC, t)
                v = float(E.xin())
                lo = v if lo is None or v < lo else lo
                hi = v if hi is None or v > hi else hi
        E.fmode = "k"
        keyv = [sorted(set(float(v) for f, v in K)) for K in r["KS"]]
        out.append([r["file"], r["src"], r["chunk"], r["path"], r["slot"], r["p"], trk[0xC], trk[0xD],
                    sel[0], sel[1], m, per[0], per[1], "0x%02X" % trk[0xF],
                    ";".join("%d:%g" % (f, float(v)) for f, v in r["KS"][0]),
                    ";".join("%d:%g" % (f, float(v)) for f, v in r["KS"][1]),
                    "%g" % lo, "%g" % hi, int(flag_res)])
    with open(os.path.join(HERE, "sd197_planar_tracks.tsv"), "w", newline="\n") as fo:
        fo.write("file\tsource\tchunk_off\tpath\tslot\tpass\tcount0\tcount1\tsel0\tsel1\tcombine_m\tperiod0\tperiod1\t"
                 "flags_hi\tkeys0(frame:value)\tkeys1\tmin_over_t\tmax_over_t\tresidue_reachable\n")
        for o in out:
            fo.write("\t".join(str(x) for x in o) + "\n")
    T = [o for o in out if o[6] >= 2 or o[7] >= 2]
    R.note("   keyed-curve slots: %d; channel-0 selector %s; channel-1 selector (when count1 >= 2) %s; "
           "combine modes (count1 >= 1) %s; periods used %s" % (
               len(T), sorted(collections.Counter(o[8] for o in T if o[6] >= 2).items()),
               sorted(collections.Counter(o[9] for o in out if o[7] >= 2).items()),
               sorted(collections.Counter(o[10] for o in out if o[7] >= 1).items()),
               sorted(collections.Counter((o[11], o[12]) for o in T).items())))
    R.note("   flags high byte (+0xF) over the 152: %s" % sorted(collections.Counter(o[13] for o in out).items()))
    for o in sorted(out, key=lambda o: (-(o[6] + o[7]), o[0])):
        if o[6] >= 2 or o[7] >= 1:
            R.note("   %s %s %s p%d k=(%d,%d) sel=(%d,%d) m=%d per=(%d,%d) keys0=[%s] keys1=[%s] -> [%s, %s]%s" % (
                o[0], o[2], o[3], o[5], o[6], o[7], o[8], o[9], o[10], o[11], o[12], o[14], o[15], o[16], o[17],
                " RESIDUE-REACHABLE before the first key" if o[18] else ""))
    R.note("   slots whose linear channel's first key frame is > 0 (time 0..first-1 would read the residue): %d" % resid)
    return out


def main():
    img = Img.load()
    img.cs.detail = True
    R = Report("sd197")
    print("== S: static")
    static_checks(img, R)
    print("== E: execution (original bytes under Unicorn vs the float32 reference)")
    E, cases = exec_checks(img, R)
    print("== C: controls (each must reject a wrong reading)")
    controls(img, R, E, cases)
    print("== D: shipped data (all EFX streams of D:/FFXII_TZA_extract)")
    shipped(img, R)
    print("FAILS %d" % R.fails)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
