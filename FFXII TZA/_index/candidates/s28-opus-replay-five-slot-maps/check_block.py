"""S-28: execute CONTRACT-battle-state-block.md - the binder 00233C10 in all three arms and the reset 002370C0 - as shipped code,
and test BS-1, BS-2, BS-3 and BS-5 with the resolver 0031B9F0 reading the result (OPUS, 2026-09-25, block 338).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges; shipped_pack.py binds battle_pack by shipped code. No application stub and no stop boundary.
Fixtures: the cell [02EBF190] set to null (the unbound arm) or to a block with a wrong or right magic; six idle objects.
Writes result_block.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
BINDER, RESET, RESOLVE, RUNTIME_RESET, PRECHECK = 0x233C10, 0x2370C0, 0x31B9F0, 0x237DF0, 0x235AF0
CELL, ACTIVE, MAGIC, SIZE = 0x2EBF190, 0x2164280, 0x05071901, 0x7410
W.ALLOWED |= {0x16D6A0, RESET, RUNTIME_RESET} | SP.allowed(W) | set().union(*(W.closure(f) for f in (BINDER, RESET, RESOLVE)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
calls = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: calls.append("00237DF0 runtime reset"), begin=RUNTIME_RESET, end=RUNTIME_RESET)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: calls.append("002370C0 block reset"), begin=RESET, end=RESET)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: calls.append("00233C5E body"), begin=0x233C5E, end=0x233C5E)


def q(a):
    return struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]


def d(a):
    return struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


REF = ACTIVE + 0x2200                                          # 00235AF0 compares the block with this image first


def binder():
    del calls[:]
    ok = S.call(BINDER)
    return ok, list(calls)


arms = {}
uc.mem_write(CELL, bytes(8))                                   # unbound
ok_u, c_u = binder()
blk = q(CELL)
arms["unbound"] = {"ok": ok_u, "cell_after": "%X" % blk, "calls": c_u}
uc.mem_write(blk, b"\xAA" * 4)                                 # bound, magic wrong
ok_w, c_w = binder()
arms["bound, magic wrong"] = {"ok": ok_w, "calls": c_w, "magic_after": "%X" % d(blk)}
for label, ref_matches in (("bound, magic right, reference matching", True), ("bound, magic right, reference differing", False)):
    uc.mem_write(blk, struct.pack("<II", MAGIC, 0))
    uc.mem_write(REF, struct.pack("<II", MAGIC if ref_matches else 0x11111111, 0))
    uc.mem_write(REF + 0x5B42, bytes([blk and uc.mem_read(blk + 0x5B42, 1)[0]]))
    uc.mem_write(REF + 0x5B12, bytes(uc.mem_read(blk + 0x5B12, 2)))
    ok_r, c_r = binder()
    arms[label] = {"ok": ok_r, "calls": c_r, "fault": (S.st["faults"] or S.st["bad"] or [None])[0]}
um, ud = arms["bound, magic right, reference matching"], arms["bound, magic right, reference differing"]
record("BS1_BS2_binder_arms", blk == ACTIVE + 0x4E68C and c_u.count("00237DF0 runtime reset") == 2
       and c_w.count("00237DF0 runtime reset") == 1 and "00233C5E body" not in c_w
       and "00233C5E body" in um["calls"] and "00237DF0 runtime reset" not in um["calls"]
       and "00237DF0 runtime reset" in ud["calls"] and "00233C5E body" not in ud["calls"], arms=arms,
       note="unbound: the cell becomes the active save buffer + 0x4E68C and 00237DF0 runs twice; bound with a wrong magic: once, no "
            "body; bound with the right magic: the body and no reset - but ONLY when the block agrees with the reference image at "
            "active + 0x2200: otherwise the first call 00235AF0 rebuilds the block and the magic test then sends it to the reset")

# BS-3 / BS-5: what one reset leaves
uc.mem_write(blk, b"\x5A" * SIZE)
uc.mem_write(blk + SIZE, b"\x5A" * 0x10)
assert S.call(RESET)
after = bytes(uc.mem_read(blk, SIZE + 0x10))
maps = [list(struct.unpack("<9H", after[0x5A48 + 0x12 * k:0x5A48 + 0x12 * k + 18])) for k in range(5)]
nonzero_outside = [i for i in range(4, SIZE) if after[i] and not (0x5A48 <= i < 0x5A5A)]
lookups = {}
for cls in range(5):
    S.call(RESOLVE, 0, cls)
    lookups[cls] = "%02X" % (uc.reg_read(UC_X86_REG_RAX) & 0xFF)
record("BS3_BS5_reset_leaves", d(blk) == MAGIC and maps[0] == [0xFFFF] * 9 and all(m == [0] * 9 for m in maps[1:]) and not nonzero_outside
       and after[SIZE:] == b"\x5A" * 0x10 and lookups == {0: "FF", 1: "00", 2: "00", 3: "00", 4: "00"},
       magic="%X" % d(blk), maps=[["%04X" % x for x in m] for m in maps], other_nonzero_bytes=len(nonzero_outside), resolver_after_reset=lookups,
       note="the reset zeroes exactly 0x7410 bytes, rewrites the magic 05071901, and fills ONLY map 0 with FFFF; maps 1-4 stay 0, so the "
            "resolver answers FF for class 0 and 00 - a slot-zero reading - for classes 1-4")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result_block.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
