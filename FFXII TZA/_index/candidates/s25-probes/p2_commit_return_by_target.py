"""P2 (original-code replay) - what the shipped commit 0030F760 returns, as a function of the
target word the walk passes in r8w.

Why: EXP-095 scripts 0030F760 and, in cases commit-fail-cont / commit-never, makes it return 0 for
target 0x4086. This probe measures whether the shipped commit can return 0 for that target.

Method: 0030F760 (570 B) runs as shipped bytes. Its callees are replaced by `ret` with rax = 0, and
every call is logged: 003105D0, 0031B7E0, 00316CF0, 00316CD0, 0030AB40, 00236850, 00236820,
00377C20 and 00313B30. 0031B7E0 returning 0 makes r15 = 0, which skips the 0030AB40 block. The
return register is set only by `mov eax,1` at 0030F97A and `xor eax,eax` at 0030F981, and the
latter is reached only from `ja` at 0030F7EC. So the callee stubs cannot change WHICH of the two
is returned; they only shorten the path. Every run records the final RIP, whether the return
sentinel was reached, the instruction count, and the stores to unit+0x708/+0x710/+0x714.
"""
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, read
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, \
    UC_X86_REG_R9, UC_X86_REG_RAX, UC_X86_REG_RIP

COMMIT, SIZE = 0x30F760, 570
CALLEES = [0x3105D0, 0x31B7E0, 0x316CF0, 0x316CD0, 0x30AB40, 0x236850, 0x236820, 0x377C20, 0x313B30]
UNIT, REC, STACK, SENT = 0x40000000, 0x40010000, 0x61000000, 0x62000000
raw, secs = load()


def run(target, param=0, arg5=1):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    pages = {COMMIT & ~0xFFF, (COMMIT + SIZE) & ~0xFFF, 0x22C1000}
    pages |= {c & ~0xFFF for c in CALLEES}
    for p in sorted(pages):
        uc.mem_map(p, 0x1000)
    uc.mem_write(COMMIT, read(raw, secs, COMMIT, SIZE))
    for c in CALLEES:
        uc.mem_write(c, b"\xc3")
    uc.mem_map(UNIT, 0x20000); uc.mem_map(STACK, 0x10000); uc.mem_map(SENT, 0x1000)
    uc.mem_write(SENT, b"\xc3")
    stats = UNIT + 0x8000
    uc.mem_write(UNIT + 0x698, struct.pack("<Q", stats))
    sp = STACK + 0x8000
    uc.mem_write(sp, struct.pack("<Q", SENT))
    uc.mem_write(sp + 0x28, struct.pack("<Q", arg5))
    for r, v in ((UC_X86_REG_RSP, sp), (UC_X86_REG_RCX, UNIT), (UC_X86_REG_RDX, REC),
                 (UC_X86_REG_R8, target), (UC_X86_REG_R9, param)):
        uc.reg_write(r, v)
    calls, stores, n = [], {}, [0]

    def code(u, addr, size, _):
        n[0] += 1
        if addr in CALLEES:
            calls.append("%08X" % addr)
            rsp = u.reg_read(UC_X86_REG_RSP)
            back = struct.unpack("<Q", u.mem_read(rsp, 8))[0]
            u.reg_write(UC_X86_REG_RSP, rsp + 8); u.reg_write(UC_X86_REG_RAX, 0)
            u.reg_write(UC_X86_REG_RIP, back)

    def wr(u, access, addr, size, value, _):
        off = addr - UNIT
        if off in (0x708, 0x710, 0x714):
            stores["+0x%X" % off] = hex(value)

    uc.hook_add(UC_HOOK_CODE, code)
    uc.hook_add(UC_HOOK_MEM_WRITE, wr)
    err = None
    try:
        uc.emu_start(COMMIT, SENT, count=100000)
    except UcError as e:
        err = str(e)
    rip = uc.reg_read(UC_X86_REG_RIP)
    rax = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    return dict(target="0x%04X" % target, rax=rax, final_rip="%08X" % rip,
                reached_sentinel=(rip == SENT), fault=err, insns=n[0],
                unit_stores=stores, callees=calls)


print("0030F760 return by target word (arg5=1, r9=0, callees ret 0)")
for t in (0x0000, 0x0100, 0x021E, 0x021F, 0x3FFF, 0x4000, 0x4086, 0x4166, 0x4167, 0x4168, 0xFFFF):
    r = run(t)
    print("  target=%(target)s  rax=%(rax)d  final_rip=%(final_rip)s  reached_sentinel=%(reached_sentinel)s"
          "  fault=%(fault)s  insns=%(insns)d  stores=%(unit_stores)s  callees=%(callees)s" % r)
