"""S-21 (OPUS, 2026-09-26): where the applier's lethal chain stops in this world, measured - a boundary record, not a closer.

The lethal chain (CONTRACT-apply-result-to-target section 13, EXP-149: 0030E360(bit 0, mode 3), killer id, kill counter, the credit
chain) was listed as blocked on [02AEE870], which 0039BA00 indexes. [02AEE870] is fontpack_it's directory entry 2, the
special-character table, bound only by the pack's load callback 0039C150 (loader-bound-bin-families.md). Here the SHIPPED
us/fontpack_it.bin is bound by that callback: the pack is copied raw and its pointer stored at [02AEE868] (what the registrar
0039C3F0 does at 0039C467 once the file is read), then 0039C150 runs as shipped up to 0039C277 (the directory slots and the TIM2
relocator 0039BF50; the texture upload 0017FBC0 at 0039C27C needs the graphics context, below).
Loads block 332's check.py (its cases run first, unchanged) and lifts the display boundary 002B4090 as i4_numeric.py does.
Measured: a lethal target-HP result runs 0028F1F0 -> 00469BB0 -> 0032A150 -> the battle-message display 002B4090 (message 0x180)
-> the glyph emitter 002AC5F0, which reads the font table through 0039BA00 (now bound) and then calls the graphics context [01F811F8] (001B5FA0) - nothing in this
world constructs it. Control: with a zeroed cell there, the fault only moves deeper into the graphics layer (001B51C0). Every
contract step of the lethal chain comes after that display, so none is executed; HP 0 is the only write that lands.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes lethal_boundary_result.json.
"""
import bisect
import contextlib
import hashlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
cwd = os.getcwd(); os.chdir(HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
os.chdir(cwd)
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RIP

W, uc, S = C.W, C.uc, C.S
FP = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data", "image", "ff12", "myoshiok", "us",
                  "packfiles", "fontpack_it.bin")
FP_SHA = "21a324236f4463873ae01be70f622095531fdc4be9490c0f4e8bd8e8fa3f03a9"
C.on_display.__code__ = (lambda u, a, n, _: None).__code__
W.ALLOWED |= W.closure(C.DISPLAY) | {C.DISPLAY} | W.closure(0x39C150) | {0x39C150}
FONT, GCTX, FONT_STOP = 0x76500000, 0x76520000, 0x39C277
uc.mem_map(FONT, 0x20000)
uc.mem_map(GCTX, 0x20000)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=FONT_STOP, end=FONT_STOP)
order = []
NAMES = {0x377C20: "00377C20 can-die", 0x30E360: "0030E360 status", 0x312280: "00312280 arm", 0x32A150: "0032A150 credit",
         0x306F00: "00306F00 credit", 0x3299B0: "003299B0 post", 0x469BB0: "00469BB0 death credit", 0x2B4090: "002B4090 display",
         0x28F1F0: "0028F1F0 display", 0x39BA00: "0039BA00 font table", 0x2AC5F0: "002AC5F0 glyph emitter", 0x1B5FA0: "001B5FA0 graphics context"}
for a, nm in NAMES.items():
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: (not order or order[-1] != nm) and order.append(nm))(nm), begin=a, end=a)
uc.ctl_flush_tb()
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
rows = {}
for l in open(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    c = l.split("\t")
    try:
        rows[int(c[0], 16)] = c[1]
    except (ValueError, IndexError):
        pass
starts = sorted(rows)
func = lambda a: "%08X" % starts[bisect.bisect_right(starts, a) - 1]


def run(zero_gctx):
    C.reset()
    pack = open(FP, "rb").read()
    assert hashlib.sha256(pack).hexdigest() == FP_SHA
    for a in range(0x2AEE800, 0x2AEE8A0, 8):
        uc.mem_write(a, bytes(8))
    uc.mem_write(FONT, pack)
    uc.mem_write(0x2AEE868, struct.pack("<Q", FONT))
    uc.mem_write(0x1F811F8, struct.pack("<Q", GCTX if zero_gctx else 0))
    uc.mem_write(GCTX, bytes(0x20000))
    S.call(0x39C150)
    bound = uc.reg_read(UC_X86_REG_RIP) == FONT_STOP and not S.st["faults"]
    slots = {"%08X" % a: "%X" % (q(a) - FONT if q(a) else 0) for a in (0x2AEE810, 0x2AEE850, 0x2AEE870, 0x2AEE878, 0x2AEE880, 0x2AEE888)}
    C.w(C.TGT + 0x48, "<i", 500); C.w(C.TGT + 0x24, "<i", 1000); C.w(C.SRC + 8, "<I", 0x1234ABCD)
    C.w(C.REC + 0x2C, "<I", 1 << 8); C.w(C.REC + 0x24, "<i", -600)
    del order[:]
    ok = C.apply()
    return {"font_bound": bound, "font_slots_rel": slots, "apply_ok": ok, "fault": S.st["faults"][:1], "fault_function": func(list(S.st["trace"])[-1]),
            "order": list(order), "hp": C.r(C.TGT + 0x48, "<i")[0], "d64": "%X" % C.r(C.TGT + 0x64, "<I")[0],
            "killer": "%X" % C.r(C.TGT + 0x30, "<I")[0]}


R = {"graphics_context_null": run(False), "graphics_context_zeroed_cell": run(True)}
g, z = R["graphics_context_null"], R["graphics_context_zeroed_cell"]
PATH = ["0028F1F0 display", "00469BB0 death credit", "0032A150 credit", "002B4090 display", "002AC5F0 glyph emitter", "0039BA00 font table"]
cases = {
    "font_pack_binds_by_its_shipped_callback": g["font_bound"] and g["font_slots_rel"]["02AEE870"] != "0",
    "lethal_path_reaches_the_message_display_through_the_death_credit": g["order"][:len(PATH)] == PATH,
    "font_table_read_now_succeeds_and_the_glyph_emitter_calls_the_graphics_context":
        "002AC5F0 glyph emitter" in g["order"] and g["order"][-1] == "001B5FA0 graphics context" and g["fault_function"] == "005C52D0",
    "zeroed_context_cell_only_moves_the_fault_into_the_graphics_layer": not z["apply_ok"] and z["fault_function"] == "001B51C0",
    "no_contract_step_of_the_lethal_chain_is_reached": all(n not in x["order"] for x in (g, z) for n in ("0030E360 status", "00312280 arm", "003299B0 post"))
        and g["d64"] == "0" and g["killer"] == "0" and g["hp"] == 0,
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "lethal_boundary_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-82s %s" % (k, "PASS" if v else "FAIL"))
print({k: (v["order"], v["fault_function"], v["fault"]) for k, v in R.items()})
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
