"""Run the shipped 003DAB50 (separation visit walk) under unicorn and record, for each resolver call, which body
pointer it received and which remembered bit it tested/cleared/set. Question: are the body pointer and the
remembered-bit index the ABSOLUTE candidate index, or a count of visited positions?
Control: candidates only in byte 0 (where the two readings agree) must map candidate i -> body i, bit i."""
import struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import *

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
b = open(EXE, "rb").read()
pe = struct.unpack_from("<I", b, 0x3C)[0]
nsec = struct.unpack_from("<H", b, pe + 6)[0]
so = struct.unpack_from("<H", b, pe + 20)[0]
sec = pe + 24 + so
BASE = 0x120000
size_img = struct.unpack_from("<I", b, pe + 24 + 56)[0]
mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(BASE, (size_img + 0xFFF) & ~0xFFF)
for i in range(nsec):
    s = sec + 40 * i
    vs, va, rs, ro = struct.unpack_from("<IIII", b, s + 8)
    mu.mem_write(BASE + va, b[ro:ro + min(rs, vs if vs else rs)])

FN = 0x003DAB50
CAND = 0x02B57EE0          # u64[2] candidate set (walked 02B57EE0..02B57EF0)
POOL = 0x02B4E4C0          # bodies, stride 0x130
STRIDE = 0x130
STACK = 0x70000000; mu.mem_map(STACK, 0x100000)
SELF = 0x71000000; mu.mem_map(SELF, 0x1000)        # the visiting body; +0x18 = u64[2] remembered bits
CB = 0x72000000; mu.mem_map(CB, 0x1000); mu.mem_write(CB, b"\xC3")   # callback = ret; hook sets eax
RET = 0x73000000; mu.mem_map(RET, 0x1000); mu.mem_write(RET, b"\xF4")

def run(cands, remembered, cb_result=1):
    mu.mem_write(CAND, struct.pack("<QQ", *cands))
    mu.mem_write(SELF, b"\0" * 0x40)
    mu.mem_write(SELF + 0x18, struct.pack("<QQ", *remembered))
    calls = []
    def hook(uc, addr, size, ud):
        if addr == CB:
            rdx = uc.reg_read(UC_X86_REG_RDX)
            rem = struct.unpack("<QQ", uc.mem_read(SELF + 0x18, 16))
            calls.append(((rdx - POOL) // STRIDE if (rdx - POOL) % STRIDE == 0 else hex(rdx), rem))
            uc.reg_write(UC_X86_REG_RAX, cb_result)
    h = mu.hook_add(UC_HOOK_CODE, hook, begin=CB, end=CB)
    rsp = STACK + 0x80000
    mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RCX, 0); mu.reg_write(UC_X86_REG_RDX, 0)
    mu.reg_write(UC_X86_REG_R8, SELF); mu.reg_write(UC_X86_REG_R9, CB)
    mu.emu_start(FN, RET, count=200000)
    mu.hook_del(h)
    after = struct.unpack("<QQ", mu.mem_read(SELF + 0x18, 16))
    return calls, after

def bits(q):
    return [i for i in range(128) if (q[i // 64] >> (i % 64)) & 1]

CASES = [
    ("control: candidates {1,3} in byte 0", (0b1010, 0), (0, 0)),
    ("candidate {9} only (byte 1)", (1 << 9, 0), (0, 0)),
    ("candidates {1,9}", ((1 << 1) | (1 << 9), 0), (0, 0)),
    ("candidate {64} only (qword 1)", (0, 1), (0, 0)),
    ("candidate {2} + {64}", (1 << 2, 1), (0, 0)),
    ("no candidate, remembered {2}", (0, 0), (1 << 2, 0)),
    ("candidate {9}, remembered {2}", (1 << 9, 0), (1 << 2, 0)),
]
for name, c, r in CASES:
    calls, after = run(c, r)
    print("%-34s cand=%s rem=%s -> resolver bodies %s ; remembered after %s" % (
        name, bits(c), bits(r), [x[0] for x in calls], bits(after)))
