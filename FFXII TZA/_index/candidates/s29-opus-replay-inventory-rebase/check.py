"""Regression for the structural consequence of ORACLE's EXP-189 correction (OPUS, 2026-09-25, repair 4): run
InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState 0030B6A0 over a 0xA5-poisoned 0x7410-byte BattleSystemState block.

Rejects: (a) any reading that the rebase clears more or less than +0x57C8..+0x59C7, or zeroes the 128 bytes at +0x59C8 instead
of masking them with 0xF8; (b) the store's former 'no censused access' reading of +0x57C0 - the rebase binds it into
descriptor 0's +0x30 (and +0x57C8 into descriptor 2's +0x20), so both regions are reached through the descriptor table 01EEBCC0.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges. No application stub and no stop boundary. Fixture: the block, filled 0xA5. The descriptor table is
the image's own .data (01EEBCC0), modified by the body as shipped. Writes result.json next to this file.
"""
import json
import os
import struct

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
REBASE, TABLE = 0x30B6A0, 0x1EEBCC0
W.ALLOWED |= {0x16D6A0} | W.closure(REBASE)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
BLOCK, SIZE = 0x76280000, 0x7410
uc.mem_write(BLOCK, b"\xA5" * SIZE)
ok = S.call(REBASE, BLOCK)
b = bytes(uc.mem_read(BLOCK, SIZE))
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
res = {
    "returned": bool(ok),
    "zeroed_57C8_59C7": b[0x57C8:0x59C8] == bytes(0x200),
    "masked_59C8_5A47_to_A0": b[0x59C8:0x5A48] == b"\xA0" * 0x80,
    "untouched_57C0_57C7": b[0x57C0:0x57C8] == b"\xA5" * 8,
    "untouched_5A48_next": b[0x5A48:0x5A50] == b"\xA5" * 8,
    "untouched_57B8_57BF": b[0x57B8:0x57C0] == b"\xA5" * 8,
    "descriptor0_plus30": "%X" % (q(TABLE + 0x30) - BLOCK),
    "descriptor2_plus20": "%X" % (q(TABLE + 0x58 * 2 + 0x20) - BLOCK),
    "descriptor0_plus8": "%X" % (q(TABLE + 0x8) - BLOCK),
}
res["ok"] = (res["returned"] and res["zeroed_57C8_59C7"] and res["masked_59C8_5A47_to_A0"] and res["untouched_57C0_57C7"]
             and res["untouched_5A48_next"] and res["untouched_57B8_57BF"] and res["descriptor0_plus30"] == "57C0"
             and res["descriptor2_plus20"] == "57C8")
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1)
print("ok" if res["ok"] else "NOT ok", res)
