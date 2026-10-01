"""S-23 (OPUS, 2026-09-26): the HP write's event variants (EY-4, knockback), the Bubble cap (EY-1) and the presentation calls
executed with no stub, over block 334's world (check.py, imported: its three cases run first, unchanged).

EY-4 (CONTRACT-hp-write-and-lethal-transition.md section 9 / section 14 item 3): the variant r13 is the SOURCE unit's
target-buffer entryFlags bit 8 for the target (00300700 key = target unit +0x10, 0030070B call 00316D70 on source +0x778,
0030071A entryFlags at +0x788 + idx*16), 'knockback rolled'. Alive posts 0x2005 + variant (0030087A); dead posts 0x2008 for
variant 0 and 0x2007 for variant 1 (00300854 neg / sbb / add 0x2008); 0x200E instead when the call's flags carry bit 8
(00300846). EY-1: status bit 28 (Bubble) doubles the cap.
Planted data: block 334's units and stats records, plus a source target-buffer entry {key = target unit +0x10, flags}. The
flags word 0x02 (bit 1 set: no death credit; bits 4 / 6 / 7 clear) lets the display 0028F1F0 and 003283D0 run as shipped.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes ey_result.json.
"""
import contextlib
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
from unicorn.x86_const import UC_X86_REG_RDX

uc, S, w, r = C.uc, C.S, C.w, C.r
evs = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: evs.append("%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)), begin=0x3299B0, end=0x3299B0)
uc.ctl_flush_tb()
SRCU, TGTU = C.POOL, C.POOL + 0xF50


def run(delta, hp=100, kb=None, flags=0x02, maxhp=500, status=0):
    C.world_units(hp, maxhp=maxhp, status=status)
    if kb is not None:
        w(SRCU + 0x778, "<BBHI", 0, 0, 0, 1)
        w(SRCU + 0x780, "<QI", r(TGTU + 0x10, "<Q")[0], (1 << 8) if kb else 0)
    del evs[:]
    ok, d = C.hp_write(delta, flags=flags)
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:1], "events": list(evs), "hp": d["hp_after"], "stores": d["stores"],
            "entered": d["entered"]}


R = {
    "alive_kb0": run(-30, kb=0), "alive_kb1": run(-30, kb=1),
    "dead_kb0": run(-150, kb=0), "dead_kb1": run(-150, kb=1),
    "alive_no_entry": run(-30), "dead_no_entry": run(-150),
    "dead_flag_bit8": run(-150, kb=1, flags=0x102),
    "heal_no_bubble": run(400, hp=480), "heal_bubble": run(400, hp=480, status=1 << 28),
    "heal_bubble_over": run(900, hp=480, status=1 << 28),
}
cases = {
    "EY4_alive_variant_is_entryFlags_bit8": R["alive_kb0"]["events"] == ["2005"] and R["alive_kb1"]["events"] == ["2006"],
    "EY4_dead_variant_inverted_2008_2007": R["dead_kb0"]["events"] == ["2008"] and R["dead_kb1"]["events"] == ["2007"],
    "EY4_no_entry_is_variant_0": R["alive_no_entry"]["events"] == ["2005"] and R["dead_no_entry"]["events"] == ["2008"],
    "flag_bit8_death_posts_200E": R["dead_flag_bit8"]["events"] == ["200E"],
    "EY1_bubble_doubles_the_cap": R["heal_no_bubble"]["hp"] == 500 and R["heal_bubble"]["hp"] == 880 and R["heal_bubble_over"]["hp"] == 1000,
    "presentation_calls_run_as_shipped": all(n in R["alive_kb0"]["entered"] for n in ("display 0028F1F0", "003283D0")),
    "no_fault": all(x["ok"] and not x["halt"] for x in R.values()),
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "ey_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print({k: (v["events"], v["hp"]) for k, v in R.items()}, R["alive_kb0"]["entered"])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
