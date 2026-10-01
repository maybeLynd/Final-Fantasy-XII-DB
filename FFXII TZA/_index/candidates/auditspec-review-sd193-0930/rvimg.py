"""rvimg.py - SWE2-AUDIT-SPEC reviewer's own image loader, disassembler and unicorn harness (2026-09-30).

Written for the SD-184 / SD-193 reviews without the packages' img.py / emu.py / retool.py. pefile + capstone + unicorn.
The certified image's sha256 is asserted. Addresses are canonical VAs (image base 0x120000 included).
A .data cell past SizeOfRawData reads as zero (mapped, no file bytes).

Emulation: sections are mapped at their VAs; a call starts at the function entry with RSP % 16 == 8 and a sentinel return
address; any fetch outside the caller-supplied code ranges raises (no silent skipping); stubs are explicit and listed.
"""
import hashlib, math, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    if o is None:
        return b"\0" * n
    return raw[o:o + n]


def f32(va):
    return struct.unpack("<f", rd(va, 4))[0]


def dis(start, end):
    return list(md.disasm(rd(start, end - start), start))


def show(start, end):
    for i in dis(start, end):
        print("  %08X  %-8s %s" % (i.address, i.mnemonic, i.op_str))


f2b = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]
b2f = lambda u: struct.unpack("<f", struct.pack("<I", u & 0xFFFFFFFF))[0]
r32 = lambda x: b2f(f2b(x))

STACK, RET, HEAP = 0x71000000, 0x72000000, 0x73000000


class Emu:
    def __init__(self, code_ranges, stubs=None):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_64)
        for n, v, vs, p, rs, x in SECS:
            lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
            mu.mem_map(lo, hi - lo)
            mu.mem_write(v, raw[p:p + min(vs, rs)])
        mu.mem_map(STACK, 0x20000)
        mu.mem_map(RET, 0x1000)
        mu.mem_map(HEAP, 0x100000)
        self.code = list(code_ranges)
        self.stubs = dict(stubs or {})
        self.hits = []
        mu.hook_add(UC_HOOK_CODE, self._code)

    def _code(self, uc, addr, size, _):
        from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX, UC_X86_REG_XMM0
        if addr == RET:
            return
        if addr in self.stubs:
            self.hits.append(addr)
            rax, x0 = self.stubs[addr](self)
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
            if rax is not None:
                uc.reg_write(UC_X86_REG_RAX, rax & 0xFFFFFFFFFFFFFFFF)
            if x0 is not None:
                uc.reg_write(UC_X86_REG_XMM0, f2b(r32(x0)))
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RIP, ret)
            return
        if not any(lo <= addr < hi for lo, hi in self.code):
            raise RuntimeError("fetch outside the allowed code at %08X" % addr)

    def reg(self, name):
        import unicorn.x86_const as K
        return self.mu.reg_read(getattr(K, "UC_X86_REG_" + name.upper()))

    def call(self, fn, floats=(), ints=(), count=1000000):
        import unicorn.x86_const as K
        mu = self.mu
        sp = STACK + 0x10000 - 8
        mu.mem_write(sp, struct.pack("<Q", RET) + b"\0" * 0x40)
        mu.reg_write(K.UC_X86_REG_RSP, sp)
        for r, v in zip(("RCX", "RDX", "R8", "R9"), ints):
            mu.reg_write(getattr(K, "UC_X86_REG_" + r), v & 0xFFFFFFFFFFFFFFFF)
        for k, x in enumerate(floats):
            if x is not None:
                mu.reg_write(getattr(K, "UC_X86_REG_XMM%d" % k), f2b(r32(x)))
        mu.emu_start(fn, RET, count=count)
        return b2f(mu.reg_read(K.UC_X86_REG_XMM0) & 0xFFFFFFFF), mu.reg_read(K.UC_X86_REG_RAX)

    def w32f(self, a, x):
        self.mu.mem_write(a, struct.pack("<f", x))

    def w(self, a, b):
        self.mu.mem_write(a, b)
