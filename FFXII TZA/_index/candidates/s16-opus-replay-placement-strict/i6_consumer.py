"""S-16 I6, the consumer half (OPUS, 2026-09-26): "area mode does not publish out_observed, and the automatic caller reads its slot
anyway ... a value below the threshold [02F973B8] accepts the candidate; otherwise the attempt counts as a miss and is retried, up
to [0208D457] times" (CONTRACT-spawn-placement.md I6) - executed: Spawn_SelectAndPrepareAutomaticEntry 00235720 run as shipped
over EXP-145's world, with the placement 00234AF0 in AREA mode inside it.

Imports EXP-145's module (_experiments/evidence/spawn-placement-exec/check.py) for its World, image loading and fixture builders
(plant_fmt0 / plant_leader / plant_units, the area-box-hit fixture: one mode-1 record whose box admits every draw). Strict as in
check.py next to this file: 00861F02 is bridged as the named import atan2f (asserted), any other import fails, and entering a
function outside the static closure of 00235720 (+ the tail targets the graph lacks) fails. No application stub.
Planted data only, besides EXP-145's fixtures: an actor object whose +0x30 is a unit; the unit's +0x38 candidate list
{count 2, entry 1 = start 4 / end 5, candidate word 0 at index 4} and +0x40 spawn index list {2, _, 0}; a spawn pool [0208E690]
with record 0 marked bit 0 (no timing gate); the unit-count cap byte [0208D458] = 4; the attempts byte [0208D457] = 3; the
threshold [02F973B8] = 100.0; the max radius [02089364] = 15.0.
THE STALE SLOT (disclosed): at 00235720's entry a hook writes a float into the caller's own out_observed stack slot
(entry rsp - 0xB4, i.e. [rsp+0x34] after the prologue) - standing for whatever an earlier call left there. Nothing else writes it.
Cases:
 A  stale slot 0.0 (below 100.0): the area placement returns 1 WITHOUT writing the slot, the caller accepts - the spawn record's
    +0x50 / +0x60 receive the position and the unit gains 0x4000000 - and returns the entry index 1; one placement call.
 R  stale slot 1000.0 (not below): the same successful area placements are all refused - three placement calls (the attempts
    byte), no spawn write, no unit flag, return -1.
Writes i6_consumer_result.json.
"""
import collections
import csv
import json
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence", "spawn-placement-exec"))
sys.path.insert(0, EXP)
import check as E                                          # EXP-145 (its __main__ guard keeps it from running)
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RIP

GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
AUTO, PLACE = 0x235720, 0x234AF0
TAILS = {0x3DFD00, 0x328370, 0x31AC90, 0x861F02, 0x3A1960, 0x263E30, 0x182E80, 0x182EB0}
graph = collections.defaultdict(set)
for row in csv.DictReader(open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8"), delimiter="\t"):
    if row["callee_external"] != "true":
        graph[int(row["caller"], 16)].add(int(row["callee"], 16))
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(os.path.join(GRAPH, "functions.tsv"), encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")


def closure(starts):
    seen, st = set(), list(starts)
    while st:
        x = st.pop()
        if x not in seen:
            seen.add(x)
            st.extend(graph[x])
    return seen


ALLOWED = closure({AUTO} | TAILS) | TAILS
BaseWorld = E.World


class StrictWorld(BaseWorld):
    def on_code(self, uc, addr, size, _):
        if addr == 0x861F02:
            if not self.imports.get(0x8C2BD0, "").endswith("!atan2f"):
                self.faults.append(("0x861F02 is not atan2f",))
                uc.emu_stop()
                return
            y, x = E.fx(uc.reg_read(UC_X86_REG_XMM0)), E.fx(uc.reg_read(UC_X86_REG_XMM1))
            uc.reg_write(UC_X86_REG_XMM0, E.xf(math.atan2(y, x)))
            self._ret(uc)
            return
        if addr in FSTARTS and addr not in ALLOWED:
            self.faults.append(("outside closure", "%08X" % addr))
            uc.emu_stop()
            return
        return BaseWorld.on_code(self, uc, addr, size, _)

    def _iat_stub(self, uc, addr):
        insn = self.gm.r(addr, 8)
        off = 1 if insn[0] in (0x48, 0x4C) else 0
        if insn[off:off + 2] in (b"\xff\x25", b"\xff\x15"):
            cell = addr + off + 6 + struct.unpack("<i", insn[off + 2:off + 6])[0]
            name = self.imports.get(cell)
            if name is not None:
                self.faults.append(("unbridged import", name))
                uc.emu_stop()
                return True
        return False


raw, secs = E.load_image()
imports = E.import_map(raw, secs)


def run(stale):
    w = StrictWorld({}, raw, secs, imports)
    w.gm.w(E.LCG_STATE, E.dw(E.LCG_PLANT))
    w.gm.w(E.ARC_DEG, E.dw(90))
    E.plant_fmt0(w, [{"mode": 1, "hx": 1e6, "hz": 1e6, "x": 0, "y": 7.5, "z": 0}])
    E.plant_leader(w)
    E.plant_units(w, E.LEAD)
    unit = w.alloc(0xF50)
    actor = w.alloc(0x100)
    w.gm.w(actor + 0x30, E.qw(unit))
    cand = w.alloc(0x40)
    w.gm.w(cand, struct.pack("<HHHHh", 2, 0, 4, 5, 0))  # count 2; entry 1 at +4: start 4, end 5; candidate word [4] = 0
    sidx = w.alloc(0x10)
    w.gm.w(sidx, bytes([2, 0xFF, 0]))                   # count 2; entry 1 -> spawn record 0
    w.gm.w(unit + 0x38, E.qw(cand))
    w.gm.w(unit + 0x40, E.qw(sidx))
    spawns = w.alloc(0x250 * 2)
    w.gm.w(spawns, E.dw(1))                             # record 0: bit 0 set - the timing gate is skipped
    w.gm.w(0x208E690, E.qw(spawns))
    w.gm.w(0x208D458, bytes([4]))
    w.gm.w(0x208D457, bytes([3]))
    w.gm.w(0x2F973B8, E.f32(100.0))
    w.gm.w(0x2089364, E.f32(15.0))
    places = []
    slot_writes = []

    def at_entry(u, a, n, _):
        sp = u.reg_read(UC_X86_REG_RSP)
        slot = sp - 0xB4
        u.mem_write(slot, E.f32(stale))
        u.hook_add(UC_HOOK_MEM_WRITE, lambda uu, acc, aa, nn, vv, __: slot_writes.append("%08X" % uu.reg_read(UC_X86_REG_RIP)),
                   begin=slot, end=slot + 3)

    w.uc.hook_add(UC_HOOK_CODE, at_entry, begin=AUTO, end=AUTO)
    w.uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: places.append(u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF), begin=PLACE, end=PLACE)
    ret = w.run(AUTO, regs={UC_X86_REG_RCX: actor})
    return {"ret": ret if ret < 0x80000000 else ret - 0x100000000, "faults": w.faults, "placement_calls": places,
            "slot_writes": slot_writes, "spawn_50": [w.gm.f(spawns + 0x50 + 4 * k) for k in range(4)],
            "spawn_60": [w.gm.f(spawns + 0x60 + 4 * k) for k in range(4)],
            "unit_flag_4000000": bool(struct.unpack("<Q", w.gm.r(unit, 8))[0] & 0x4000000), "lcg": hex(w.gm.dw(E.LCG_STATE))}


a, r = run(0.0), run(1000.0)
cases = {
    "A_stale_slot_below_threshold_accepts_the_area_candidate": not a["faults"] and a["ret"] == 1 and a["placement_calls"] == [0]
        and a["slot_writes"] == [] and a["unit_flag_4000000"] and a["spawn_50"] != [0.0] * 4,
    "R_stale_slot_not_below_refuses_every_successful_candidate": not r["faults"] and r["ret"] == -1 and r["placement_calls"] == [0, 0, 0]
        and r["slot_writes"] == [] and not r["unit_flag_4000000"] and r["spawn_50"] == [0.0] * 4,
}
res = {"ok": all(cases.values()), "cases": cases, "accept": a, "refuse": r, "allowed_functions": len(ALLOWED)}
json.dump(res, open(os.path.join(HERE, "i6_consumer_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps(res, default=str)[:1500])
