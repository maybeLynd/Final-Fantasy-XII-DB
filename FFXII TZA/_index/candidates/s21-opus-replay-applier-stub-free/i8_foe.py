"""S-21 I8, the foe paths (OPUS, 2026-09-26): "foe stat adjustments check targetStats+5 == 1; steal and effect-byte paths require
an owning unit whose unit->stats exists and has kind 1; steal IDs are words at unit->p_E60 + 0x32 + 2*i; availability clears at
unit->spawn + 0x14; effect bytes modify spawn +0x7B/+0x79/+0x78/+0x7A and OR 0x80 into its leading dword"
(CONTRACT-apply-result-to-target.md I8) - executed with the whole applier 003112F0 and its REAL callees over block 332's world
(check.py, imported: its cases run first, unchanged).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub; block 332's recorded display boundary 002B4090
stays (no case here writes HP/MP). Planted data only: the target unit (pool slot 1) gets +0x6A0 = a spawn block and +0xE60 = a
definition block whose words at +0x32 are the steal ids; the target stats' kind byte +5.
Cases (flags 0x10, source = the other unit):
 M   member adds: with target stats +5 = 1, record +0x11E/+0x120/+0x122/+0x124 add (word - base byte +0x2A/+0x2B/+0x2F/+0x30)
     to stats +0x08/+0x0A/+0x12/+0x14 (003118A1..00311915); with +5 = 0 nothing changes.
 E   effect bytes: with the owning unit's stats kind 1, record +0x128..+0x12B OR into spawn +0x7B/+0x79/+0x78/+0x7A,
     +0x12C..+0x12F AND-NOT the same bytes, and each touched byte ORs 0x80 into the spawn's leading dword; kind 0: untouched.
 S   steal: with kind 1 and record +0x32..+0x34 set, the ids 0x3001 / 0x4002 at p_E60 + 0x32 / +0x36 go to the item write
     003008A0, each followed by the tail 00253770(3, 1); the 0xFFFF id at slot 1 is skipped although +0x33 is set; kind 0:
     no item write.
 G   NOT IN I8'S WORDING: the availability bits at spawn +0x14 are cleared by the gate 00385BA0 (00385C17 / 00385C41 /
     00385C6B, one bit per steal byte +0x34 / +0x33 / +0x32), BEFORE the steal loop and for EITHER kind - so a steal byte
     on a non-foe target uses up the availability with no item. The steal loop's own btr (0031146F) then finds it clear.
Recorded stop boundary (disclosed, S-26's): 002FEF30, the foe arm the kind-1 tail reaches; every write asserted lands
before it. Planted: a fifth idle object behind [020927C0] (read by the steal tail through 002536A0).
Writes i8_foe_result.json.
"""
import json
import os
import struct

from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc, w, r = C.uc, C.w, C.r
UNIT1 = C.POOL + 0xF50
SPAWN, DEFB = 0x77000000, 0x77001000
try:
    uc.mem_map(SPAWN, 0x2000)
except Exception:                                         # already inside the world's mapped fixture region
    pass
IDLE5 = 0x77010000                                        # a fifth idle object: [020927C0], read by the steal tail through 002536A0
uc.mem_map(IDLE5, 0x10000)
uc.mem_write(0x20927C0, struct.pack("<Q", IDLE5))
FOE_ARM = 0x2FEF30                                        # recorded stop boundary (S-26's): the foe arm the kind-1 tail reaches


def on_foe_arm(u, a, n, _):
    C.ev["stopped_at"] = "002FEF30 foe arm"
    u.emu_stop()


from unicorn import UC_HOOK_CODE
uc.hook_add(UC_HOOK_CODE, on_foe_arm, begin=FOE_ARM, end=FOE_ARM)
C.hook(0x3008A0, "item_write", (UC_X86_REG_RCX, UC_X86_REG_RDX))
C.hook(0x253770, "steal_tail", (UC_X86_REG_RCX, UC_X86_REG_RDX))
uc.ctl_flush_tb()


def setup(kind):
    C.reset()
    uc.mem_write(IDLE5, bytes(0x10000))
    w(C.TGT + 5, "<B", kind)
    uc.mem_write(SPAWN, bytes(0x2000))
    w(UNIT1 + 0x6A0, "<Q", SPAWN)
    w(UNIT1 + 0xE60, "<Q", DEFB)
    w(DEFB + 0x32, "<HHH", 0x3001, 0xFFFF, 0x4002)
    w(SPAWN + 0x14, "<B", 0x07)


def stats_fields():
    return {"08": r(C.TGT + 8, "<h")[0], "0A": r(C.TGT + 0xA, "<h")[0], "12": r(C.TGT + 0x12, "<h")[0], "14": r(C.TGT + 0x14, "<h")[0]}


def member(kind):
    setup(kind)
    w(C.TGT + 8, "<h", 5); w(C.TGT + 0xA, "<h", 7); w(C.TGT + 0x12, "<h", 9); w(C.TGT + 0x14, "<h", 11)
    w(C.TGT + 0x2A, "<BB", 1, 2); w(C.TGT + 0x2F, "<BB", 3, 4)
    w(C.REC + 0x11E, "<hhhh", 20, 30, 40, 50)
    ok = C.apply()
    return {"ok": ok, "stop": C.ev.get("stopped_at"), "halt": (C.S.st["bad"] or C.S.st["faults"])[:2], "fields": stats_fields()}


def effect(kind):
    setup(kind)
    w(SPAWN + 0x78, "<BBBB", 0x55, 0x55, 0x55, 0x55)
    w(C.REC + 0x128, "<BBBBBBBB", 0x0F, 0x30, 0x01, 0x00, 0xF0, 0x0C, 0x00, 0x08)
    ok = C.apply()
    return {"ok": ok, "stop": C.ev.get("stopped_at"), "halt": (C.S.st["bad"] or C.S.st["faults"])[:2], "bytes_78_79_7A_7B": ["%02X" % b for b in r(SPAWN + 0x78, "<BBBB")],
            "lead": "%X" % r(SPAWN, "<I")[0]}


def steal(kind):
    setup(kind)
    w(C.REC + 0x32, "<BBB", 1, 1, 1)
    ok = C.apply()
    return {"ok": ok, "stop": C.ev.get("stopped_at"), "halt": (C.S.st["bad"] or C.S.st["faults"])[:2], "item_writes": [["%X" % a, b] for a, b in C.ev.get("item_write", [])],
            "steal_tail": C.ev.get("steal_tail", []), "avail_14": "%02X" % r(SPAWN + 0x14, "<B")[0]}


m1, m0 = member(1), member(0)
e1, e0 = effect(1), effect(0)
gate_writes = []
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RIP
_gw = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: _gw.append(["%08X" % u.reg_read(UC_X86_REG_RIP), "+%X" % (a - SPAWN), v]),
            begin=SPAWN + 0x14, end=SPAWN + 0x14)
uc.ctl_flush_tb()
del _gw[:]
s0 = steal(0)
gate_writes.append([x for x in _gw if x[0].startswith("00385C")])
del _gw[:]
s1 = steal(1)
gate_writes.insert(1, [x for x in _gw if x[0].startswith("00385C")])
gate_writes = [gate_writes[1], gate_writes[0]]            # [kind 1, kind 0]
steal_loop_btr = [x for x in _gw if x[0] == "0031146F"]
want_m = {"08": 5 + 20 - 1, "0A": 7 + 30 - 2, "12": 9 + 40 - 3, "14": 11 + 50 - 4}
b = 0x55
want_e = ["%02X" % ((b | 0x01) & ~0x00 & 0xFF), "%02X" % ((b | 0x30) & ~0x0C & 0xFF), "%02X" % ((b | 0x00) & ~0x08 & 0xFF),
          "%02X" % ((b | 0x0F) & ~0xF0 & 0xFF)]
done = lambda x: x["ok"] or (x["stop"] == "002FEF30 foe arm" and not x["halt"])
cases = {
    "M_member_adds_only_on_foe_stats": done(m1) and m1["fields"] == want_m and m0["ok"] and m0["fields"] == {"08": 5, "0A": 7, "12": 9, "14": 11},
    "E_effect_bytes_or_and_not_and_flag_only_for_kind1": done(e1) and e1["bytes_78_79_7A_7B"] == want_e and int(e1["lead"], 16) & 0x80
        and e0["ok"] and e0["bytes_78_79_7A_7B"] == ["55"] * 4 and e0["lead"] == "0",
    "S_steal_ids_from_p_E60_skip_FFFF_kind1_only": done(s1) and [x[0] for x in s1["item_writes"]] == ["3001", "4002"]
        and len(s1["steal_tail"]) == 2 and s0["ok"] and s0["item_writes"] == [],
    "G_the_gate_clears_availability_for_every_steal_byte_either_kind": s1["avail_14"] == "00" and s0["avail_14"] == "00"
        and [x[1:] for x in gate_writes[0]] == [["+14", 3], ["+14", 1], ["+14", 0]] and [x[1:] for x in gate_writes[1]][:3] == [["+14", 3], ["+14", 1], ["+14", 0]],
}
res = {"ok": all(cases.values()), "cases": cases, "member": {"kind1": m1, "kind0": m0, "want": want_m},
       "effect": {"kind1": e1, "kind0": e0, "want": want_e}, "steal": {"kind1": s1, "kind0": s0, "gate_writes_kind1_kind0": gate_writes, "steal_loop_btr_kind1": steal_loop_btr}}
json.dump(res, open(os.path.join(HERE, "i8_foe_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps(res)[:1500])
