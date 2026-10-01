"""S-03 probe (OPUS, 2026-09-26): the mode word's setters, reset, getters and save round trip in the S-32 world (world.py +
shipped_pack.py, battle_pack bound by shipped code, which also yields the battle state block [02EBF190]). Exploratory."""
import json, os, struct
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX
import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
LADDER, SET3, SET2, SET1, SET0, RESET = 0x30D9A0, 0x307200, 0x307240, 0x303D90, 0x313550, 0x30DA10
GET3, GET2, GET1, GET0, IS4, IS5, IS2 = 0x3072A0, 0x3072E0, 0x303EE0, 0x3135E0, 0x3072C0, 0x307280, 0x303EC0
CAPTURE, RESTORE = 0x2EF3C0, 0x2EF410
ENTRIES = (LADDER, SET3, SET2, SET1, SET0, RESET, GET3, GET2, GET1, GET0, IS4, IS5, IS2, CAPTURE, RESTORE)
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) | {f} for f in ENTRIES))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
STATE = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


flag_writes = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, ac, a, n, v, _: flag_writes.append(v & 0xFFFFFFFF), begin=STATE + 0x5B04, end=STATE + 0x5B07)
entered = []
for a in (0x35C620, 0x2E73C0, 0x2EB030, 0x3139D0):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, a=a: entered.append(["%08X" % a, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF]), begin=a, end=a)


def call(fn, *args):
    del flag_writes[:]
    del entered[:]
    ok = S.call(fn, *args)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, (S.st["bad"] or S.st["faults"])[:2]


if __name__ == "__main__":
    print("STATE %X" % STATE)
    for fn, nm in ((SET3, "set3"), (SET2, "set2"), (SET0, "set0"), (SET1, "set1")):
        w(STATE + 0x5B04, "<I", 0)
        print(nm, "on", call(fn, 1), "%X" % r(STATE + 0x5B04, "<I")[0], flag_writes, entered)
        print(nm, "again", call(fn, 1), flag_writes, entered)
        print(nm, "off", call(fn, 0), "%X" % r(STATE + 0x5B04, "<I")[0], flag_writes, entered)
