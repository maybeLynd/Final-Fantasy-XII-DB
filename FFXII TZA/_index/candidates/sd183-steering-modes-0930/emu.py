"""emu.py - a small isolated-execution harness over the certified image (SWE2-ORACLE, 2026-09-30).

The image's sections are mapped at their VAs from FFXII_TZA.exe (img.py). A call starts at a function entry with a
return address RET on a fresh stack; it ends when RET is fetched. Floats go in xmm0..xmm3 and come back in xmm0.
Every instruction fetched outside the allowed code ranges raises, so an unexpected call is never silently skipped.
IAT thunks the caller names (cosf, sinf, sqrtf, atan2f, acosf) are answered in Python with float32 rounding; each is
listed by the caller as a stub. No other stub exists unless a caller passes one.
"""
import math, struct
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                               UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_XMM2,
                               UC_X86_REG_XMM3)
import img

STACK, RET, HEAP = 0x71000000, 0x72000000, 0x73000000
f2b = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]
b2f = lambda u: struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0]
r32 = lambda x: b2f(f2b(x))                      # round a Python float to float32

# the jmp [IAT] thunks this harness may answer (7-byte region starts; each is `jmp qword ptr [rip+..]`)
THUNKS = {0x00861F08: ("cosf", lambda a: math.cos(a[0])), 0x00861F0E: ("sinf", lambda a: math.sin(a[0])),
          0x00861F14: ("sqrtf", lambda a: math.sqrt(a[0]) if a[0] >= 0 else float("nan")),
          0x00861F02: ("atan2f", lambda a: math.atan2(a[0], a[1])),
          0x00861EFC: ("asinf", lambda a: math.asin(max(-1.0, min(1.0, a[0]))))}
XMM = [UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_XMM2, UC_X86_REG_XMM3]


class Emu:
    def __init__(self, code_ranges, thunks=(), stubs=None):
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_64)
        for _n, va, vsz, raw, rawsz in img.SECS:
            lo, hi = va & ~0xFFF, (va + vsz + 0xFFF) & ~0xFFF
            mu.mem_map(lo, hi - lo)
            mu.mem_write(va, img.blob[raw:raw + min(rawsz, vsz)])
        mu.mem_map(STACK, 0x20000)
        mu.mem_map(RET, 0x1000)
        mu.mem_map(HEAP, 0x100000)
        self.code = list(code_ranges)
        self.thunks = {a: THUNKS[a] for a in thunks}
        self.stubs = dict(stubs or {})           # addr -> callable(emu) returning (rax or None, xmm0 float or None)
        self.calls = []
        mu.hook_add(UC_HOOK_CODE, self._code)

    def _ret(self, uc, rax=None, xmm0=None):
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        if rax is not None:
            uc.reg_write(UC_X86_REG_RAX, rax & 0xFFFFFFFFFFFFFFFF)
        if xmm0 is not None:
            uc.reg_write(UC_X86_REG_XMM0, f2b(r32(xmm0)))
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)

    def _code(self, uc, addr, size, _):
        if addr == RET:
            return
        if addr in self.thunks:
            name, fn = self.thunks[addr]
            a = [b2f(uc.reg_read(r) & 0xFFFFFFFF) for r in XMM[:2]]
            self.calls.append(name)
            self._ret(uc, xmm0=fn(a))
            return
        if addr in self.stubs:
            self.calls.append("%08X" % addr)
            rax, x0 = self.stubs[addr](self)
            self._ret(uc, rax, x0)
            return
        if not any(lo <= addr < hi for lo, hi in self.code):
            raise RuntimeError("fetch outside the allowed code at %08X" % addr)

    def f32(self, a):
        return b2f(struct.unpack("<I", self.mu.mem_read(a, 4))[0])

    def put_f32(self, a, x):
        self.mu.mem_write(a, struct.pack("<f", x))

    def call(self, fn, floats=(), rcx=0, rdx=0, r8=0, r9=0, stack_args=(), count=2000000):
        mu = self.mu
        sp = STACK + 0x10000 - 8                 # RSP % 16 == 8 at entry, as after a real call
        frame = struct.pack("<Q", RET) + b"\0" * 0x20 + b"".join(struct.pack("<Q", v) for v in stack_args)
        mu.mem_write(sp, frame)
        mu.reg_write(UC_X86_REG_RSP, sp)
        for r, v in zip((UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9), (rcx, rdx, r8, r9)):
            mu.reg_write(r, v)
        for r, x in zip(XMM, floats):
            mu.reg_write(r, f2b(r32(x)))
        mu.emu_start(fn, RET, count=count)
        return b2f(mu.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF), mu.reg_read(UC_X86_REG_RAX)
