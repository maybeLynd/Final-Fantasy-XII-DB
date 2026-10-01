"""sd120_emu.py - SWE2-ORACLE, 2026-09-30. Unicorn harness for SD-120: runs one 0050xxxx binding operation on the certified image in controlled memory.
The image is mapped at its own ImageBase 0x120000; the three 0x1000 working buffers are the image's own BSS
02B477A0 / 02B487A0 / 02B497A0; the operation record lives in a mapped scratch page. The bridged calls are the
VCRUNTIME140 memcpy thunk 00861EBA (performed in Python, then ret) and the stack probe __chkstk 00808F10 (returned;
it only touches guard pages below rsp). Everything else runs natively.
"""
import os, struct
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import *

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
BASE = 0x120000
A, B, C = 0x02B477A0, 0x02B487A0, 0x02B497A0
REC = 0x10000000
STACK = 0x20000000
RET = 0x30000000
CHKSTK = 0x00808F10
MEMCPY = 0x00861EBA

_pe = pefile.PE(EXE)
_size = (_pe.OPTIONAL_HEADER.SizeOfImage + 0xFFF) & ~0xFFF
_secs = [(BASE + s.VirtualAddress, s.get_data()) for s in _pe.sections]
_hdr = _pe.get_memory_mapped_image()[:0x1000]


class Emu:
    def __init__(self):
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        mu.mem_map(BASE, _size)
        mu.mem_write(BASE, _hdr)
        for va, data in _secs:
            mu.mem_write(va, data)
        mu.mem_map(REC, 0x10000)
        mu.mem_map(STACK, 0x100000)
        mu.mem_map(RET, 0x1000)
        mu.mem_write(RET, b"\xf4")
        self.mu = mu
        self.calls = []
        self.fault = None
        mu.hook_add(UC_HOOK_CODE, self._code, begin=MEMCPY, end=MEMCPY)
        mu.hook_add(UC_HOOK_CODE, self._chkstk, begin=CHKSTK, end=CHKSTK)
        mu.hook_add(UC_HOOK_MEM_UNMAPPED, self._unmapped)

    def _code(self, mu, addr, size, ud):
        dst, src, n = (mu.reg_read(UC_X86_REG_RCX), mu.reg_read(UC_X86_REG_RDX), mu.reg_read(UC_X86_REG_R8))
        self.calls.append(("memcpy", dst, src, n))
        mu.mem_write(dst, bytes(mu.mem_read(src, n)))
        rsp = mu.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", mu.mem_read(rsp, 8))[0]
        mu.reg_write(UC_X86_REG_RAX, dst)
        mu.reg_write(UC_X86_REG_RSP, rsp + 8)
        mu.reg_write(UC_X86_REG_RIP, ret)

    def _chkstk(self, mu, addr, size, ud):
        # __chkstk only probes guard pages (gs:[0x10] StackLimit); the harness stack is fully committed, so return
        rsp = mu.reg_read(UC_X86_REG_RSP)
        self.calls.append(("chkstk", mu.reg_read(UC_X86_REG_RAX)))
        mu.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", mu.mem_read(rsp, 8))[0])
        mu.reg_write(UC_X86_REG_RSP, rsp + 8)

    def _unmapped(self, mu, access, addr, size, value, ud):
        self.fault = (access, addr)
        return False

    def put_buf(self, va, rows):
        self.mu.mem_write(va, b"".join(struct.pack("<4i", *r) for r in rows))

    def get_buf(self, va, n=256):
        d = bytes(self.mu.mem_read(va, 16 * n))
        return [list(struct.unpack_from("<4i", d, 16 * i)) for i in range(n)]

    def put_rec(self, raw):
        self.mu.mem_write(REC, bytes(raw))

    def call(self, fn, rcx, rdx, r8=0, r9=0):
        mu = self.mu
        rsp = STACK + 0xF0000
        mu.mem_write(rsp, struct.pack("<Q", RET))
        mu.reg_write(UC_X86_REG_RSP, rsp)
        for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
            mu.reg_write(r, v)
        self.calls = []
        mu.emu_start(fn, RET, count=20_000_000)
        return mu.reg_read(UC_X86_REG_RIP)

