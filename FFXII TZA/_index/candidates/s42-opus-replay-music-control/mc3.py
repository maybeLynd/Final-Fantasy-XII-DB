"""S-42 MC-3 (OPUS, 2026-09-26): 'The loader returns the block BEFORE the bytes arrive. It sizes the file, allocates from heap 5,
queues the read and hands the pointer back immediately.' (CONTRACT-music-control-file-and-bgm-stream.md MC-3), executed over
block 325's world (check.py, imported: its cases run first, unchanged).

What block 325 lacked was engine heap 5. It is registered here the way the boot frame does it, at boot's own sizes
(0022A2EC..0022A304: 00369D30(5, 0036D240(0x1C0100), 0x1C0000, 0x100)). The kind-9 size table entry for id 0x20 is planted
with the shipped musicctrl.bin's size (the size tables are FST-loaded at boot; the same kind of fixture block 325 plants for
kind 0x24). Then the boot music loader 003EAB60 runs as shipped: 0051ED10 -> 0032E400 (size), 0036C1D0/0036A190/0036C140
(heap 5 allocation), 0032E620 (queue the read).
Asserted: the loader returns; [02B5E0D0] (MC-1's one writer, 003EAB78) holds the returned block, which lies inside arena 5;
the read queued through 0032E620 names kind 9, id 0x20, that block and the file's size; and NO byte of the block is written
during the call - the pointer comes back before any data does.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes mc3_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
LOADER, BLOCKNEW, ARENA, ENQUEUE = 0x3EAB60, 0x36D240, 0x369D30, 0x32E620
W.ALLOWED |= set().union(*(W.closure(f) | {f} for f in (LOADER, BLOCKNEW, ARENA)))
FILE_SIZE = len(open(C.MUSIC, "rb").read())

okb = S.call(BLOCKNEW, 0x1C0100)
blk = uc.reg_read(UC_X86_REG_RAX)
oka = S.call(ARENA, 5, blk, 0x1C0000, 0x100)

SIZES9 = C.SIZES + 0x2000
uc.mem_write(SIZES9, bytes(0x200))
C.w(C.SIZE_TABLES + 9 * 8, "<Q", SIZES9)
C.w(SIZES9 + 4 * 0x20, "<I", FILE_SIZE)
C.w(C.TABLE_CELL, "<Q", 0)

ev = {"enqueue": None, "block_writes": 0, "watch": None}


def on_enq(u, a, n, _):
    ev["enqueue"] = {"kind": u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, "id": u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                     "block": "%X" % u.reg_read(UC_X86_REG_R8), "size": u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF}


def on_w(u, ac, a, n, v, _):
    lo = ev["watch"]
    if lo is not None and lo <= a < lo + FILE_SIZE:
        ev["block_writes"] += 1


uc.hook_add(UC_HOOK_CODE, on_enq, begin=ENQUEUE, end=ENQUEUE)
uc.hook_add(UC_HOOK_MEM_WRITE, on_w, begin=blk, end=blk + 0x1C0000)
uc.ctl_flush_tb()
# the allocator is deterministic here, so watch the whole arena and attribute writes after the block is known: arm the
# watch on the first allocation's return by re-running once to learn the address, then run the measured call
ok0 = S.call(LOADER)
first = C.r(C.TABLE_CELL, "<Q")[0]
C.w(C.TABLE_CELL, "<Q", 0)
ev.update(enqueue=None, block_writes=0, watch=None)
# measured run: a fresh arena so the block lands at the same place as the first run
okb2 = S.call(BLOCKNEW, 0x1C0100); blk2 = uc.reg_read(UC_X86_REG_RAX)
oka2 = S.call(ARENA, 5, blk2, 0x1C0000, 0x100)
uc.hook_add(UC_HOOK_MEM_WRITE, on_w, begin=blk2, end=blk2 + 0x1C0000)
uc.ctl_flush_tb()
ev["watch"] = None
ok = S.call(LOADER)
ret = uc.reg_read(UC_X86_REG_RAX)
cell = C.r(C.TABLE_CELL, "<Q")[0]
# count writes into the returned block during the call: re-run the measured call with the watch armed at the known address
C.w(C.TABLE_CELL, "<Q", 0)
okb3 = S.call(BLOCKNEW, 0x1C0100); blk3 = uc.reg_read(UC_X86_REG_RAX)
oka3 = S.call(ARENA, 5, blk3, 0x1C0000, 0x100)
uc.hook_add(UC_HOOK_MEM_WRITE, on_w, begin=blk3, end=blk3 + 0x1C0000)
uc.ctl_flush_tb()
predicted = cell - blk2 + blk3
ev.update(enqueue=None, block_writes=0, watch=predicted)
ok3 = S.call(LOADER)
cell3 = C.r(C.TABLE_CELL, "<Q")[0]
head = bytes(uc.mem_read(cell3, 16))
filehead = open(C.MUSIC, "rb").read()[:16]

cases = {
    "heap5_registered_by_boots_own_calls": okb and oka and okb2 and oka2 and okb3 and oka3,
    "loader_returns_and_publishes_the_block": ok and ok3 and cell == ret and cell3 == predicted and blk2 <= cell < blk2 + 0x1C0000,
    "the_read_is_queued_with_kind_9_id_0x20_the_block_and_the_file_size": ev["enqueue"] is not None
        and ev["enqueue"]["kind"] == 9 and ev["enqueue"]["id"] == 0x20 and int(ev["enqueue"]["block"], 16) == cell3
        and ev["enqueue"]["size"] == FILE_SIZE,
    "no_byte_of_the_block_is_written_before_the_pointer_returns": ev["block_writes"] == 0 and head != filehead,
}
res = {"ok": all(cases.values()), "cases": cases, "file_size": FILE_SIZE, "arena5_block": "%X" % blk3, "returned": "%X" % cell3,
       "enqueue": ev["enqueue"], "block_writes_during_call": ev["block_writes"], "block_head": head.hex(), "file_head": filehead.hex()}
json.dump(res, open(os.path.join(HERE, "mc3_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
