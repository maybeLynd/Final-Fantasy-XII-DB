"""S-41 (OPUS, 2026-09-26): CONTRACT-spatial-source-objects executed for the first time - all five classes' slot 34 and slot 39,
called through their real vtables, stub-free.

The contract (SA-1..SA-7) had no execution record (s41-runtime-per-invariant-exposure.md: coverage, not exposure).
World: block 355's world.py (../s29-opus-replay-inventory-rebase), its real initialisers built, plus three REAL initialiser steps:
  - 00210AF0, the audio object's own lazy initialiser (as in s41-opus-replay-sound-request-stub-free);
  - 007AD620(00210EC0, 00210EB0), the audio library's allocation-callback installer called with EXACTLY the two functions the
    library init 00210760 passes (0021082A lea 00210EC0 / 00210841 lea 00210EB0 -> 007A4D50 -> 007AD620); the rest of that init
    sits under 001DBA40, which needs CreateThread, and is not run;
  - 007BB620, the listener's own initialiser (0xA0 bytes via 007AD460 -> [02EAD0B0], ctor 007EF100, cell 02EADE08).
Source objects are planted DATA: a 0x1000-byte block per object with its class vtable at +0 (Dynamic 01CB99F0, Point 01CB9B40,
Ambient 01CB9C88, Direction 01CB9DD0, Polygon 01CB9F18), the radius +0xE4, a vector at +0x100, and for Polygon a vertex count at
+0x108 with vertices from +0x110. Slot 34 and slot 39 are read from each vtable and called. No application stub.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import importlib.util
import json
import math
import os
import struct
import sys

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX

HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.join(HERE, "..", "s29-opus-replay-inventory-rebase")
sys.path.insert(0, WD)
spec = importlib.util.spec_from_file_location("world355", os.path.join(WD, "world.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
FX = json.load(open(os.path.join(WD, "world.json")))
VT = {"Dynamic": 0x1CB99F0, "Point": 0x1CB9B40, "Ambient": 0x1CB9C88, "Direction": 0x1CB9DD0, "Polygon": 0x1CB9F18}
BASE_VT = 0x1CBAB68
S34 = {"Dynamic": 0x7F1340, "Point": 0x7F1A50, "Ambient": 0x7F1D10, "Direction": 0x7F1F80, "Polygon": 0x7F25E0}
for f in list(S34.values()) + [0x210AF0, 0x7E5800, 0x7E57B0, 0x7BB620, 0x7AD620, 0x210EB0]:
    W.ALLOWED |= W.closure(f) | {f}
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
init = {"audio": S.call(0x210AF0), "callbacks": S.call(0x7AD620, 0x210EC0, 0x210EB0), "listener": S.call(0x7BB620)}
LISTENER = struct.unpack("<Q", bytes(uc.mem_read(0x2EADE08, 8)))[0]
LPOS = struct.unpack("<ffff", bytes(uc.mem_read(LISTENER + 0x30, 16)))
OBJ = 0x72000000
uc.mem_map(OBJ, 0x10000)
cur = {"lo": 0, "hi": 0, "w": set()}


def mw(u, acc, a, n, v, _):
    if cur["lo"] <= a < cur["hi"]:
        cur["w"].update(range(a - cur["lo"], a - cur["lo"] + n))


uc.hook_add(UC_HOOK_MEM_WRITE, mw)
uc.ctl_flush_tb()


def slot(vt, k):
    return struct.unpack("<Q", bytes(uc.mem_read(vt + k * 8, 8)))[0]


def run(cls, radius, vec=(1.0, 2.0, 3.0, 7.0), verts=None, mode=0):
    o = OBJ + list(VT).index(cls) * 0x1000
    uc.mem_write(o, bytes(0x1000))
    uc.mem_write(o, struct.pack("<Q", VT[cls]))
    uc.mem_write(o + 0xE4, struct.pack("<f", radius))
    uc.mem_write(o + 0x100, struct.pack("<ffff", *vec))
    if cls == "Polygon":
        verts = verts or [(1.0, 2.0, 3.0, 1.0), (9.0, 9.0, 9.0, 1.0), (-4.0, 0.0, 0.0, 1.0)]
        uc.mem_write(o + 0x104, bytes([mode]))
        uc.mem_write(o + 0x108, struct.pack("<i", len(verts)))
        for i, v in enumerate(verts):
            uc.mem_write(o + 0x110 + 16 * i, struct.pack("<ffff", *v))
    cur.update(lo=o, hi=o + 0x1000, w=set())
    ok = S.call(slot(VT[cls], 34), o)
    wr = sorted(cur["w"])
    cur.update(lo=0, hi=0)
    d0 = struct.unpack("<ffff", bytes(uc.mem_read(o + 0xD0, 16)))
    return {"ok": ok, "bad": list(S.st["bad"])[:2], "faults": list(S.st["faults"])[:2], "D0": [round(x, 5) for x in d0],
            "E0": uc.mem_read(o + 0xE0, 1)[0], "E4": round(struct.unpack("<f", bytes(uc.mem_read(o + 0xE4, 4)))[0], 5),
            "writes": ["%X" % x for x in wr], "dist": round(math.dist(d0[:3], LPOS[:3]), 5)}


def s39(cls):
    S.call(slot(VT[cls], 39), OBJ)
    return uc.reg_read(UC_X86_REG_RAX) & 0xFF


res = {"live_game": False, "init": init, "listener": "%X" % LISTENER, "listener_pos": LPOS}
runs = {}
for cls in VT:
    runs[cls + "_in"] = run(cls, 10.0)
    runs[cls + "_out"] = run(cls, 2.0)
    runs[cls + "_r0"] = run(cls, 0.0)
runs["Polygon_mode1"] = run("Polygon", 10.0, mode=1)
res["runs"] = runs
res["slot39"] = {cls: s39(cls) for cls in VT}
res["slot34_targets"] = {cls: "%08X" % slot(VT[cls], 34) for cls in VT}
res["base_vtable_slot34"] = "%X" % slot(BASE_VT, 34)
core = set(range(0xD0, 0xE1))
cases = {}
cases["real_initialisers_audio_callbacks_listener"] = all(init.values()) and LISTENER != 0
cases["slot34_targets_are_the_five_contract_bodies"] = res["slot34_targets"] == {c: "%08X" % a for c, a in S34.items()}
std = [k for k in runs if not k.startswith("Polygon_mode1")]
cases["no_fence_no_fault"] = all(runs[k]["ok"] and not runs[k]["bad"] and not runs[k]["faults"] for k in runs)
# SA-1: every class writes the position +0xD0..+0xDF and the byte +0xE0; outside that, only one class writes anything
inr = {c: runs[c + "_in"] for c in VT}
outside = {c: set(int(x, 16) for x in inr[c]["writes"]) - core for c in VT}
res["writes_outside_D0_E0"] = {c: ["%X" % x for x in sorted(v)] for c, v in outside.items()}
cases["SA1_all_five_write_D0_DF_and_E0"] = all(core <= set(int(x, 16) for x in inr[c]["writes"]) for c in VT)
cases["SA1_nothing_outside_D0_E0_written_by_two_classes"] = all(sum(1 for c in VT if x in outside[c]) <= 1 for x in set().union(*outside.values()))
# SA-2: w forced to 1.0 - Ambient explicitly; Direction copies the 16 bytes from +0x100 and then overwrites w
cases["SA2_ambient_w_1_direction_copies_vector_and_forces_w"] = inr["Ambient"]["D0"] == [0.0, 0.0, 0.0, 1.0] \
    and inr["Direction"]["D0"] == [1.0, 2.0, 3.0, 1.0]
# SA-3: +0xE0 always 1 for Ambient/Direction; computed against the radius for Point/Dynamic/Polygon; 0 when the radius <= 0
cases["SA3_ambient_direction_E0_always_1"] = all(runs[c + s]["E0"] == 1 for c in ("Ambient", "Direction") for s in ("_in", "_out", "_r0"))
cases["SA3_point_dynamic_polygon_E0_is_distance_below_radius"] = all(
    runs[c + "_in"]["E0"] == int(runs[c + "_in"]["dist"] < runs[c + "_in"]["E4"]) and runs[c + "_out"]["E0"] == int(runs[c + "_out"]["dist"] < runs[c + "_out"]["E4"])
    and runs[c + "_r0"]["E0"] == 0 for c in ("Point", "Dynamic", "Polygon")) and any(runs[c + "_in"]["E0"] != runs[c + "_out"]["E0"] for c in ("Point", "Polygon"))
# SA-4: +0xE4 written by Dynamic only
e4 = {c: any(int(x, 16) in range(0xE4, 0xE8) for x in inr[c]["writes"]) for c in VT}
res["writes_E4"] = e4
# Dynamic's own store (007F13EC) is gated on +0x140 == 1 (007F1379) and a live audio-library handle at +0x38 (007A8C30 -> registry
# 007B24F0 / 007B2470 under a lock); that emitter registry is not built in this world, so only the other half is executed.
cases["SA4_the_other_four_classes_never_write_the_radius"] = all(not any(int(x, 16) in range(0xE4, 0xE8) for x in runs[k]["writes"])
    for k in runs if not k.startswith("Dynamic"))
cases["SA4_dynamic_mode0_path_leaves_the_radius_unwritten_as_the_gate_predicts"] = not e4["Dynamic"]
# SA-5 (static read): the base vtable's slot 34 is 0
cases["SA5_base_vtable_slot34_is_zero"] = res["base_vtable_slot34"] == "0"
# SA-6: slot 39 true for exactly the three radius-testing classes
cases["SA6_slot39_true_for_point_dynamic_polygon_false_for_ambient_direction"] = res["slot39"] == {"Dynamic": 1, "Point": 1, "Ambient": 0, "Direction": 0, "Polygon": 1}
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-80s %s" % (k, "PASS" if v else "FAIL"))
print("outside D0..E0:", res["writes_outside_D0_E0"])
print({k: (v["D0"], v["E0"], v["E4"], v["dist"]) for k, v in runs.items()})
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
