"""rc18_modes_emu.py - RC-18: what BattleGroup_RefreshFourActorDefinitions 003266C0 leaves in the four battle maps
(block +0x5A5A map 1 ... +0x5A90 map 4) for each battle runtime mode 0..5. ORACLE, 2026-09-30. Isolated execution of
the shipped bytes (unicorn), not a live run.

Setup: the image's sections are mapped at their VAs; a 0x7410-byte block is allocated and its address written to the
global 02EBF190. Map 0 (+0x5A48) = [0, 1, 2, 9, 3, 4, 5, FFFF, FFFF] (three playables, a guest-band row 9 in slot 3, three
reserve playables); maps 1..4 are pre-filled with 0xEEEE so an untouched word is visible; the leader +0x5AA4 = 1.
Every call 003266C0 makes is answered by a stub (the value each returns is printed):
  0030D9A0 the mode ladder -> MODE;  003272F0 focus roster slot -> 1;  00377C20 field bit 15 -> 0 (mode 3 run: 1);
  00377C70 the field record's character -> 4;  00304650 the rider's index -> 0;  00313800 the summoner's index -> 1;
  003137E0 +0x5AD4 (the summoned Esper's row) -> 0x1B;  00311E20, 00326500 -> return;  00263750 roster -> 0 (no actor,
  so the re-bind tail loop does nothing);  00322C50 -> 0.
Positive control: mode 0 must leave map 1 = map 0's slots 0..3 followed by five 0xFFFF (the five-maps page's
correction, 00326714..00326730).
"""
import os, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RCX

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import img  # noqa: E402

FN = 0x003266C0
BLOCK = 0x70000000
STACK = 0x71000000
RET = 0x72000000
MAP0 = [0, 1, 2, 9, 3, 4, 5, 0xFFFF, 0xFFFF]


def run(mode, bit15):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    for name, va, vsz, raw, rawsz in img.SECS:
        lo, hi = va & ~0xFFF, (va + vsz + 0xFFF) & ~0xFFF
        mu.mem_map(lo, hi - lo)
        mu.mem_write(va, img.blob[raw:raw + min(rawsz, vsz)])
    mu.mem_map(BLOCK, 0x8000)
    mu.mem_map(STACK, 0x10000)
    mu.mem_map(RET, 0x1000)
    mu.mem_write(0x02EBF190, struct.pack("<Q", BLOCK))
    blk = bytearray(0x7410)
    struct.pack_into("<9H", blk, 0x5A48, *MAP0)
    for m in range(1, 5):
        struct.pack_into("<9H", blk, 0x5A48 + 0x12 * m, *([0xEEEE] * 9))
    struct.pack_into("<I", blk, 0x5AA4, 1)
    mu.mem_write(BLOCK, bytes(blk))
    stubs = {0x0030D9A0: mode, 0x003272F0: 1, 0x00377C20: bit15, 0x00377C70: 4, 0x00304650: 0, 0x00313800: 1,
             0x003137E0: 0x1B, 0x00311E20: 0, 0x00326500: 0, 0x00263750: 0, 0x00322C50: 0, 0x00313F60: bit15}

    def code(uc, addr, size, _):
        if addr in stubs:
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
            uc.reg_write(UC_X86_REG_RAX, stubs[addr])
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RIP, ret)
        elif not (0x00326000 <= addr < 0x00327000) and addr != RET:
            raise RuntimeError("unstubbed call to %08X" % addr)

    mu.hook_add(UC_HOOK_CODE, code)
    sp = STACK + 0x8000
    mu.mem_write(sp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, sp)
    mu.emu_start(FN, RET, count=200000)
    out = mu.mem_read(BLOCK + 0x5A48, 0x12 * 5)
    return [list(struct.unpack_from("<9H", out, 0x12 * m)) for m in range(5)]


def fmt(ws):
    return " ".join("----" if w == 0xFFFF else ("%04X" % w) for w in ws)


def main():
    names = {0: "mode 0 (none of the four bits)", 1: "mode 1 (summon)", 2: "mode 2 (chocobo)",
             3: "mode 3 (field record bit 15)", 4: "mode 4 (event party)", 5: "mode 5 (event party 2)"}
    ok = True
    for mode in range(6):
        maps = run(mode, 1 if mode == 3 else 0)
        if mode == 0:
            c = maps[1] == MAP0[:4] + [0xFFFF] * 5
            print("%s  control: mode 0 leaves map 1 = map 0 slots 0..3 then five 0xFFFF" % ("PASS" if c else "FAIL"))
            ok &= c
        print("%s" % names[mode])
        for m in range(5):
            print("   map %d  %s" % (m, fmt(maps[m])))
    print("(---- = 0xFFFF, the empty slot; EEEE would be a word the refresh left untouched)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
