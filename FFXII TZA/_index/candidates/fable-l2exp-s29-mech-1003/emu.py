"""emu.py - FABLE, 2026-10-03: a lean Unicorn 2.1.4 world for the S-29 reserve -> consume-or-refund bodies.

Original code runs at its own virtual addresses over the SHA-checked image (rvlib).  Planted state (disclosed):
  - class 0's storage pointer: descriptor 01EEBCC0 row 0 +0x08 -> a zeroed 64-word array (the image has NULL there; the
    shipped rebase 0030B6A0 binds it at runtime - s29-opus-replay-inventory-storage runs that rebase);
  - the action table: registry slot 02EBF138 -> a header {+4 count, +8 stride 60, +0xC handle}, resolver base
    01F83530 = 0, so 0020E600(handle) is the row block itself;
  - the gil block: 02092758 -> a block whose +8 is the gil;
  - one battle unit (0x1000 bytes) whose +0x698 is a stats record; stats +5 is the kind byte, +0x6C bit 0 effect 32.
Native: 0030EF20, 00305640, 00300280, 003008A0, 00309F30, 002FD150, 002FD8D0, 00325F40, 00322C50, 00309440, 0020E600,
00309060, 002F9820, 002F95D0, 00253690, 00254EE0, 003037A0, 003093D0, 0030B0E0, 00309110, 00308FF0 and whatever they call
that is not listed in STUBS.  STUBS answer by a recording hook (their own bodies are executed elsewhere: EXP-065/066):
  00300CE0 (MP), 00300BC0 (secondary pool), 00316440 / 00253770 (category accounting), 00316A50 (achievement counter
  reached from GameState_SetGil when the gil changes).
Any other function entry that is a .pdata root and not in NATIVE is recorded as UNEXPECTED and stops the run.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,  # noqa: E402
                               UC_X86_REG_RSP, UC_X86_REG_RIP)

PREPARE, CONSUME, REFUND, AVAIL, IDOP = 0x0030EF20, 0x00305640, 0x00300280, 0x003037A0, 0x003008A0
TABLE, REG_ACTIONS, RESOLVE_BASE, GILCELL = 0x01EEBCC0, 0x02EBF138, 0x01F83530, 0x02092758
STACK, HEAP, RET = 0x70000000, 0x72000000, 0x71000000
UNIT, STATS, KIND1STATS, WORDS, HDR, ROWS, GIL = (HEAP + 0x0000, HEAP + 0x2000, HEAP + 0x3000, HEAP + 0x4000, HEAP + 0x5000,
                                                   HEAP + 0x6000, HEAP + 0x9000)
STRIDE = 60
STUBS = {0x00300CE0: 0, 0x00300BC0: 0, 0x00316440: 0, 0x00253770: 0, 0x00316A50: 0}
NATIVE = {0x0030EF20, 0x00305640, 0x00300280, 0x003008A0, 0x00309F30, 0x002FD150, 0x002FD8D0, 0x00325F40, 0x00322C50,
          0x00309440, 0x0020E600, 0x00309060, 0x002F9820, 0x002F95D0, 0x00253690, 0x00254EE0, 0x003037A0, 0x003093D0,
          0x0030B0E0, 0x00309110, 0x00308FF0, 0x00808C40}

ITEM = 0x0005                  # class 0, index 5
ROW_ITEM, ROW_PLAIN, ROW_GIL = 1, 2, 3


def _roots(img):
    po = img.off(img.base + img.exc_rva)
    out = set()
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u)
        if not ((img.d[ui] >> 3) & 4):
            out.add(b + img.base)
    return out


class World(object):
    def __init__(self, img):
        self.img = img
        self.roots = _roots(img)
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        hi = max(img.base + va + max(vs, rs) for n, va, vs, ra, rs in img.secs)
        uc.mem_map(img.base, ((hi + 0xFFFF) & ~0xFFFF) - img.base)
        uc.mem_write(img.base, img.d[:0x1000])
        for n, va, vs, ra, rs in img.secs:
            uc.mem_write(img.base + va, img.d[ra:ra + min(rs, vs if vs else rs)])
        uc.mem_map(STACK, 0x100000)
        uc.mem_map(RET, 0x1000)
        uc.mem_write(RET, b"\xF4")
        uc.mem_map(HEAP, 0x100000)
        uc.mem_map(0x7FF00000, 0x2000)                     # a TEB for gs: (the GS-cookie helper reads nothing from it)
        uc.msr_write(0xC0000101, 0x7FF00000)
        self.uc = uc
        self.log, self.unexpected, self.faults, self.idop = [], [], [], []
        uc.hook_add(UC_HOOK_CODE, self._code)
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._bad)
        self.plant()

    # ------------------------------------------------------------- planted state
    def w(self, a, f, v):
        self.uc.mem_write(a, struct.pack(f, v))

    def r(self, a, f):
        return struct.unpack(f, bytes(self.uc.mem_read(a, struct.calcsize(f))))[0]

    def plant(self):
        self.uc.mem_write(HEAP, bytes(0x10000))
        self.w(TABLE + 0x08, "<Q", WORDS)                   # class 0 storage bound (64 uint16 words)
        self.w(REG_ACTIONS, "<Q", HDR)
        self.w(HDR + 4, "<I", 16)                           # row count seen by the 0x14 validator
        self.w(HDR + 8, "<H", STRIDE)
        self.w(HDR + 0xC, "<I", ROWS)
        self.w(RESOLVE_BASE, "<Q", 0)
        self.w(GILCELL, "<Q", GIL)
        self.w(GIL + 8, "<i", 1000)
        for i in range(16):
            row = ROWS + i * STRIDE
            self.w(row + 0x1E, "<B", 0)
            self.w(row + 0x22, "<H", 0xFFFF)
        self.w(ROWS + ROW_ITEM * STRIDE + 0x1E, "<B", 3)
        self.w(ROWS + ROW_ITEM * STRIDE + 0x22, "<H", ITEM)
        self.w(ROWS + ROW_GIL * STRIDE + 0x0A, "<B", 31)    # base 31 -> 390 gil with effect 32 (the page's own example)
        self.w(UNIT + 0x698, "<Q", STATS)
        self.w(UNIT + 0xDC8, "<H", 0xFFFF)
        self.w(STATS + 5, "<B", 0)
        self.w(KIND1STATS + 5, "<B", 1)

    def owned(self, item=ITEM):
        return self.r(WORDS + 2 * (item & 0xFFF), "<H") & 0x3FF

    def set_owned(self, n, item=ITEM, equipped=0):
        self.w(WORDS + 2 * (item & 0xFFF), "<H", (equipped << 10) | n)

    def row(self, i):
        return ROWS + i * STRIDE

    def gil(self):
        return self.r(GIL + 8, "<i")

    def res(self):
        return self.r(UNIT + 0xDC8, "<H"), self.r(UNIT + 0xE58, "<i")

    # ------------------------------------------------------------- hooks
    def _code(self, uc, a, n, _):
        if a in STUBS:
            self.log.append(("%08X" % a, uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF))
            sp = uc.reg_read(UC_X86_REG_RSP)
            uc.reg_write(UC_X86_REG_RAX, STUBS[a])
            uc.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", bytes(uc.mem_read(sp, 8)))[0])
            uc.reg_write(UC_X86_REG_RSP, sp + 8)
            return
        if a == IDOP:
            sp = uc.reg_read(UC_X86_REG_RSP)
            self.idop.append((uc.reg_read(UC_X86_REG_RCX) & 0xFFFF, struct.unpack("<i", struct.pack("<I", uc.reg_read(
                UC_X86_REG_RDX) & 0xFFFFFFFF))[0], uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF, self.r(sp + 0x28, "<I")))
        if a in self.roots and a not in NATIVE and a not in STUBS:
            self.unexpected.append("%08X" % a)
            uc.emu_stop()

    def _bad(self, uc, acc, a, n, v, _):
        self.faults.append("%08X" % a)
        return False

    def call(self, fn, rcx=0, rdx=0, r8=0, r9=0):
        uc = self.uc
        self.log, self.unexpected, self.faults, self.idop = [], [], [], []
        sp = STACK + 0x80000
        uc.mem_write(sp, struct.pack("<Q", RET))
        uc.reg_write(UC_X86_REG_RSP, sp)
        for reg, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
            uc.reg_write(reg, v & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(fn, RET, count=2000000)
        except UcError as e:
            self.faults.append(str(e))
        ok = uc.reg_read(UC_X86_REG_RIP) == RET and not self.unexpected and not self.faults
        return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF

    # ------------------------------------------------------------- the three operations
    def prepare(self, row):
        return self.call(PREPARE, UNIT, self.row(row))

    def consume(self, row, flag=1):
        return self.call(CONSUME, UNIT, self.row(row), flag)

    def refund(self):
        return self.call(REFUND, UNIT)

    def avail(self, row):
        return self.call(AVAIL, UNIT, row)


if __name__ == "__main__":
    W = World(Img.load())
    W.set_owned(3)
    print("prepare", W.prepare(ROW_ITEM), W.owned(), W.res(), W.idop, W.unexpected, W.faults, W.log)
    print("consume", W.consume(ROW_ITEM), W.owned(), W.res(), W.idop, W.unexpected, W.faults, W.log)
    print("refund", W.refund(), W.owned(), W.res(), W.idop, W.unexpected, W.faults)
    W.set_owned(3)
    print("prepare", W.prepare(ROW_ITEM), W.owned(), W.res())
    print("refund", W.refund(), W.owned(), W.res(), W.idop)
    W.set_owned(0)
    print("prepare@0", W.prepare(ROW_ITEM), W.owned(), W.res(), W.idop)
    print("refund", W.refund(), W.owned(), W.res(), W.idop)
    W.w(0x02EBF138, "<Q", HDR)
    print("avail owned1", W.avail(ROW_ITEM), W.unexpected, W.faults)
