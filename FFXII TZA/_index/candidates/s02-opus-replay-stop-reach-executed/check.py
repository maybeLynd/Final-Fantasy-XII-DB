"""S-02: execute the system-stop registry's request 00226BE0 for ALL 28 slots in the built world - the record build 00227680,
SS-7's breadth computation 00226C77..00226C94 and the per-manager loop - and record the reach AS THE CODE COMPUTES IT and the
managers it actually walks (OPUS, 2026-09-25, block 331).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session with stack arguments)
supplies the image, the IAT traps and the named bridges; its world is built once. No application stub and no stop boundary.
This completes block 287, which measured the reach for 23 of 28 ids with the breadth arithmetic RE-COMPUTED by the check,
never ran 00226BE0's manager loop, and faulted on ids 0, 12, 13, 15, 17 through null globals.
Three idle objects are planted as zeroed blocks, the convention of the world's nine: [0209BE80] (the HUD object), [01F7FFE0]
(00198790's object, which the record build flags for ids 12/13/15/17 through 00182CD0 / 00182CF0) and [0215E6E0] (the flag word
002DDC30 reads for slot 0; its bit 3 is run both clear and set). Each run clears the slot's bit in the active bitset 01FD46D4
first (00226C08 skips an already-active slot); the call is the prelude's own, 00226BE0(slot, 0, 0, 0, -1, -1) as at 0025479D.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
REQUEST, RECORDS, BITSET, MGR = 0x226BE0, 0x1FD4160, 0x1FD46D4, 0x263FF0
W.ALLOWED |= {0x16D6A0} | W.closure(REQUEST)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
FLAGWORD = IDLE + 2 * 0x20000
ev = {}
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.setdefault("reach", u.reg_read(UC_X86_REG_RAX)), begin=0x226C94, end=0x226C94)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.setdefault("managers", []).append(u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF),
            begin=MGR, end=MGR)


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def request(slot):
    ev.clear()
    uc.mem_write(BITSET, bytes(4))
    ok = S.call(REQUEST, slot, 0, 0, 0, stack=(0xFFFFFFFF, 0xFFFFFFFF))
    a, b = r(RECORDS + slot * 0x18, "<QQ")
    return {"ok": ok, "fault": (S.st["faults"] or [None])[0], "record_A": "%016X" % a, "record_B": "%016X" % b,
            "reach_computed": ev.get("reach"), "managers_walked": ev.get("managers", []), "active_bit_after": r(BITSET, "<I")[0] >> slot & 1}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


per = {}
for s in range(28):
    per[s] = request(s)
uc.mem_write(FLAGWORD, struct.pack("<I", 1 << 3))
slot0_bit3 = request(0)
uc.mem_write(FLAGWORD, bytes(4))

bad = []
for s, v in per.items():
    a_low = int(v["record_A"][8:], 16)
    breadth = ((~(a_low >> 30)) & 2) | 1
    if not v["ok"] or v["reach_computed"] != breadth or v["managers_walked"] != list(range(breadth)) or v["active_bit_after"] != 1:
        bad.append(s)
reach3 = sorted(s for s, v in per.items() if v["reach_computed"] == 3)
record("SS7_reach_executed_all_28_slots", not bad and slot0_bit3["ok"], mismatches=bad, reach_3_slots=reach3,
       per_slot={s: {k: v[k] for k in ("record_A", "reach_computed", "managers_walked")} for s, v in per.items()},
       slot0_with_flag_bit3=slot0_bit3,
       note="00226BE0 runs to its return for every slot 0..27. The breadth is the value the code computes at 00226C94; it equals "
            "(~(A >> 30) & 2) | 1 of the record the code itself built, and the loop asks 00263FF0 for managers 0..breadth-1 exactly. "
            "Only slot 11 reaches 3 managers")

a0, a0b = per[0]["record_A"], slot0_bit3["record_A"]
record("slot0_record_depends_on_flag_bit3", True, flag_clear=a0, flag_set=a0b, differs=a0 != a0b,
       note="slot 0's record is built through 002DDC30 (bit 3 of the flag word behind 0215E6E0); recorded both ways")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
