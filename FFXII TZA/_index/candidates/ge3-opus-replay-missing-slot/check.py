"""GE-3 (OPUS, 2026-09-25): what 0031C5D0's class-0x1A arm reads at 0031E288 when the registry slot [02EBF118] is missing.
Static claim tested: rsi is 0 from 0031C5EC and only the normal path writes it; the missing-slot conditions are the same ones the
arm tests first (0031E153 / 0031E167), which set rbp = 0 and fault at 0031E22C (byte [rbp + 0x10]) before 0031E24F - so the
GE-3 branches 0031E259 / 0031E266 are never reached in a non-faulting run.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) + shipped_pack.py (battle_pack
bound by shipped code, so [02EBF118] is the shipped table). No application stub. Cases: slot bound (control), slot null, slot's
+0xC dword zeroed (the resolve returns 0). Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ_UNMAPPED
from unicorn.x86_const import UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
FILL, SLOT = 0x31C5D0, 0x2EBF118
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | W.closure(FILL)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
REC = 0x76280000
seen = []
for a in (0x31E14C, 0x31E22C, 0x31E24F, 0x31E288):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: seen.append("%08X" % x), begin=a, end=a)
bad_reads = []
uc.hook_add(UC_HOOK_MEM_READ_UNMAPPED, lambda u, acc, a, n, v, _: bad_reads.append(["%08X" % u.reg_read(UC_X86_REG_RIP), "%X" % a]) or False)

slot_ptr = struct.unpack("<Q", bytes(uc.mem_read(SLOT, 8)))[0]
slot_c = struct.unpack("<I", bytes(uc.mem_read(slot_ptr + 0xC, 4)))[0] if slot_ptr else None


def run(label, index=0, null_slot=False, zero_c=False):
    uc.mem_write(SLOT, struct.pack("<Q", 0 if null_slot else slot_ptr))
    if slot_ptr:
        uc.mem_write(slot_ptr + 0xC, struct.pack("<I", 0 if zero_c else slot_c))
    uc.mem_write(REC, bytes(0x98))
    uc.mem_write(REC, struct.pack("<II", 0x1A, index))
    del seen[:], bad_reads[:]
    ok = S.call(FILL, REC)
    return label, {"returned": ok, "reached": list(seen), "unmapped_reads": list(bad_reads)}


cases = dict([run("slot bound (control)"), run("slot null", null_slot=True), run("slot +0xC zeroed", zero_c=True)])
uc.mem_write(SLOT, struct.pack("<Q", slot_ptr))
ctrl, nul, zc = cases["slot bound (control)"], cases["slot null"], cases["slot +0xC zeroed"]
ok = (bool(slot_ptr) and ctrl["returned"] and "0031E288" in ctrl["reached"]
      and nul["returned"] and nul["reached"] == [] and not nul["unmapped_reads"]
      and not zc["returned"] and zc["reached"] == ["0031E14C", "0031E22C"] and zc["unmapped_reads"] == [["0031E22C", "10"]])
res = {"ok": ok, "slot_02EBF118": "%X" % slot_ptr, "cases": cases,
       "note": "slot null: the validator 00322C50 refuses first (0031E14C never reached) and the arm exits cleanly; slot +0xC "
               "zeroed (the resolve returns 0): validation passes and the arm faults at 0031E22C reading [0x10]. Neither reaches "
               "0031E24F / 0031E288, so GE-3's branches 0031E259 / 0031E266 are never taken in a non-faulting run; the bound "
               "control reaches 0031E288 on the normal path"}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1)
print("ok" if ok else "NOT ok", json.dumps(cases))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
