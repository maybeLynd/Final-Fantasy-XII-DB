"""Isolated execution of 00227680(id, recA, recB, flag) for ids 0..27, flag 0/1, stub return 0/1.
Method B: shipping .text bytes; callees 00182CD0 / 00182CF0 / 00182D10 / 002DDC30 replaced by `mov eax,R; ret`.
Output: TSV id flag stubret A0 A8 B0 B8 B10 B14 path_calls"""
import struct, hashlib, json, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import *
import os
EXE = os.environ.get("FF12_EXE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/work/exe/FFXII_TZA.exe"))
BASE = 0x120000
d = open(EXE, "rb").read()
print("exe sha256", hashlib.sha256(d).hexdigest(), file=sys.stderr)
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    name = d[o:o+8].rstrip(b"\0").decode()
    secs.append((name, struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 16)[0], struct.unpack_from("<I", d, o + 20)[0]))
text = [s for s in secs if s[0] == ".text"][0]
FUNC, SIZE = 0x227680, 0x634
body = d[text[4] + (FUNC - BASE - text[1]): text[4] + (FUNC - BASE - text[1]) + SIZE]
print("body sha256", hashlib.sha256(body).hexdigest(), file=sys.stderr)
STUBS = [0x182CD0, 0x182CF0, 0x182D10, 0x2DDC30]
REC, STACK, RET = 0x10000000, 0x20000000, 0x30000000
def run(idv, flag, sret):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    tva = BASE + text[1]; tsz = (text[2] + 0xFFF) & ~0xFFF
    mu.mem_map(tva & ~0xFFF, ((tva + tsz) - (tva & ~0xFFF) + 0xFFF) & ~0xFFF)
    mu.mem_write(tva, d[text[4]: text[4] + min(text[3], text[2])])
    calls = []
    for s in STUBS:
        mu.mem_write(s, bytes([0xB8]) + struct.pack("<I", sret) + bytes([0xC3]))
    mu.mem_map(REC, 0x1000); mu.mem_map(STACK, 0x10000); mu.mem_map(RET, 0x1000)
    mu.mem_write(REC, b"\xA5" * 0x100)          # sentinel fill: untouched bytes stay A5
    rsp = STACK + 0x8000
    mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RCX, idv); mu.reg_write(UC_X86_REG_RDX, REC); mu.reg_write(UC_X86_REG_R8, REC + 0x40)
    mu.reg_write(UC_X86_REG_R9, flag)
    def hook(uc, addr, size, ud):
        if addr in STUBS: calls.append("%X" % addr)
        if not (FUNC <= addr < FUNC + SIZE) and not any(x <= addr < x + 6 for x in STUBS) and addr != RET:
            raise RuntimeError("left body at %X" % addr)
    mu.hook_add(UC_HOOK_CODE, hook)
    mu.emu_start(FUNC, RET, count=5000)
    assert mu.reg_read(UC_X86_REG_RIP) == RET and mu.reg_read(UC_X86_REG_RSP) == rsp + 8
    a = mu.mem_read(REC, 0x18); b = mu.mem_read(REC + 0x40, 0x18)
    q = lambda m, o: struct.unpack_from("<Q", m, o)[0]
    return q(a, 0), q(a, 8), q(b, 0), q(b, 8), struct.unpack_from("<I", b, 0x10)[0], b[0x14], ",".join(calls)
print("id\tflag\tstub\tA0\tA8\tB0\tB8\tB10\tB14\tcalls")
for idv in range(28):
    for flag in (0, 1):
        for sret in (0, 1):
            r = run(idv, flag, sret)
            print("%d\t%d\t%d\t%016X\t%016X\t%016X\t%016X\t%08X\t%02X\t%s" % ((idv, flag, sret) + r))
