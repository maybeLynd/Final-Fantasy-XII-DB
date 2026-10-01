"""sd140_emu.py - SWE2-ORACLE, 2026-09-30. Unicorn harness for SD-140: runs shipped vertex-prep and emit bodies of the
certified image in controlled memory.

The image is mapped at its own ImageBase 0x120000 (all sections, so the PS2 register bank 022D8F10.. and the globals
02AEED50 / 02F8F2F8 / 02AEE900 are the image's own BSS). Caller data lives in a scratch region SCR. Calls leave the
shipped code only through explicit stubs (Emu.stub), each of which returns a disclosed value and is logged; a call
into an address that is neither shipped code under test nor a stub still runs natively. Nothing is patched.
"""
import os, struct
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_HOOK_MEM_READ
from unicorn.x86_const import *

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
BASE = 0x120000
SCR = 0x10000000            # 4 MB caller scratch
STACK = 0x20000000
RET = 0x30000000

_pe = pefile.PE(EXE)
_size = (_pe.OPTIONAL_HEADER.SizeOfImage + 0xFFF) & ~0xFFF
_secs = [(BASE + s.VirtualAddress, s.get_data()) for s in _pe.sections]
_hdr = _pe.get_memory_mapped_image()[:0x1000]

REGS = {"rcx": UC_X86_REG_RCX, "rdx": UC_X86_REG_RDX, "r8": UC_X86_REG_R8, "r9": UC_X86_REG_R9}


class Emu:
    def __init__(self):
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        mu.mem_map(BASE, _size)
        mu.mem_write(BASE, _hdr)
        for va, data in _secs:
            mu.mem_write(va, data)
        mu.mem_map(SCR, 0x400000)
        mu.mem_map(STACK, 0x100000)
        mu.mem_map(RET, 0x1000)
        mu.mem_write(RET, b"\xf4")
        self.mu = mu
        self.stubs = {}
        self.calls = []
        self.fault = None
        self.reads = []
        self.watch = None
        mu.hook_add(UC_HOOK_MEM_UNMAPPED, self._unmapped)
        mu.hook_add(UC_HOOK_MEM_READ, self._read)

    # a stub: at addr, record the call, set rax = fn(emu) (or leave it), and return to the caller (ret semantics; a
    # tail-jump into a stubbed address returns to the tail-caller's caller, exactly as the real callee would)
    def stub(self, addr, name, fn=None):
        def _hit(mu, a, size, ud):
            self.calls.append((name, {k: mu.reg_read(r) for k, r in REGS.items()}))
            if fn is not None:
                v = fn(self)
                if v is not None:
                    mu.reg_write(UC_X86_REG_RAX, v)
            rsp = mu.reg_read(UC_X86_REG_RSP)
            mu.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", mu.mem_read(rsp, 8))[0])
            mu.reg_write(UC_X86_REG_RSP, rsp + 8)
        self.stubs[addr] = name
        self.mu.hook_add(UC_HOOK_CODE, _hit, begin=addr, end=addr)

    def _unmapped(self, mu, access, addr, size, value, ud):
        self.fault = (access, addr)
        return False

    def _read(self, mu, access, addr, size, value, ud):
        if self.watch and self.watch[0] <= addr < self.watch[1]:
            self.reads.append((addr, size))

    def w(self, va, b):
        self.mu.mem_write(va, bytes(b))

    def r(self, va, n):
        return bytes(self.mu.mem_read(va, n))

    def q(self, va, v):
        self.w(va, struct.pack("<Q", v))

    def call(self, fn, rcx=0, rdx=0, r8=0, r9=0, stack_args=(), xmm=None, count=50_000_000):
        mu = self.mu
        rsp = STACK + 0xF0000
        frame = struct.pack("<Q", RET) + b"\0" * 32 + b"".join(struct.pack("<Q", a) for a in stack_args)
        mu.mem_write(rsp, frame)
        mu.reg_write(UC_X86_REG_RSP, rsp)
        for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
            mu.reg_write(r, v)
        for reg, v in (xmm or {}).items():
            mu.reg_write(reg, v)
        self.calls = []
        self.reads = []
        self.fault = None
        try:
            mu.emu_start(fn, RET, count=count)
        except Exception as e:  # noqa: BLE001 - reported to the caller as a fault
            self.fault = self.fault or ("exception", str(e))
        return mu.reg_read(UC_X86_REG_RIP)
