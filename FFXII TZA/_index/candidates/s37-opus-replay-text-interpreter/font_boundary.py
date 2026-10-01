"""S-37 (OPUS, 2026-09-26): why 002A9F00's re-entry stays unexecuted, measured - a boundary record, not a closer.

I-4's remaining half was recorded as "needs the font object 0039C4A0 returns (not planted)". Here the SHIPPED us/fontpack_it.bin
is bound by its own load callback 0039C150 (the pack copied raw, its pointer at [02AEE868] as the registrar 0039C3F0 stores it at
0039C467), over block 313's harness (check.py, imported: its cases run first, unchanged) with i4.py's planted [01F81200].
Measured:
 F1  the callback binds the directory slots (02AEE810 glyph sheet, 02AEE870 special characters, ...) and relocates the TIM2
     (0039BF50), then queues the glyph sheet's render commands: 0017FBC0 -> 001B6510 -> 001BA860, which takes a slot from the
     render-state manager's command pool. The planted manager has no pool, so no slot comes back and the write faults.
 F2  0039C4A0(0) returns [02AEE800], which the callback caches at 0039C2AA - after that render enqueue. It stays 0.
 F3  the glyph measure 002AC2F0, reached by `02 41 00` (interpreter -> 002B2150 -> measure), calls 0039C4A0 and faults reading
     the null font object (+0xC), with or without the pack.
 S   static: right after the getter, the measure calls 0017FD30 (render state; its dl != 0 arm calls 001B5FA0, the graphics
     context [01F811F8]) at 002AC34E / 002AC363.
So the font object sits behind the render layer twice over: its cache is written after a render enqueue, and its first user
calls render state. Binding the pack does not reach 002A9F00.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes font_boundary_result.json.
"""
import collections
import contextlib
import hashlib
import io
import json
import os
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import UC_HOOK_CODE

HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
uc = C.uc
FP = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data", "image", "ff12", "myoshiok", "us",
                  "packfiles", "fontpack_it.bin")
FP_SHA = "21a324236f4463873ae01be70f622095531fdc4be9490c0f4e8bd8e8fa3f03a9"
G_MGR, MGR, FONT = 0x1F81200, C.WORLD + 0x38000, 0x76500000
uc.mem_map(FONT, 0x20000)
C.ALLOWED |= C.closure(0x39C150) | {0x39C150}
seen = []
for a, k in ((0x2AC5F0, "interpreter"), (0x2B2150, "002B2150"), (0x2AC2F0, "measure 002AC2F0"), (0x39C4A0, "getter 0039C4A0"),
             (0x39BF50, "relocator 0039BF50"), (0x17FBC0, "enqueue 0017FBC0"), (0x1BA860, "command slot 001BA860"),
             (0x2A9F00, "002A9F00")):
    uc.hook_add(UC_HOOK_CODE, (lambda k: lambda u, a, n, _: (not seen or seen[-1] != k) and seen.append(k))(k), begin=a, end=a)
tail = collections.deque(maxlen=64)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: tail.append(a))
uc.ctl_flush_tb()


def last():
    return "%08X" % tail[-1] if tail else None


def bind():
    pack = open(FP, "rb").read()
    assert hashlib.sha256(pack).hexdigest() == FP_SHA
    for a in range(0x2AEE800, 0x2AEE8A0, 8):
        uc.mem_write(a, bytes(8))
    uc.mem_write(FONT, pack)
    uc.mem_write(0x2AEE868, struct.pack("<Q", FONT))
    del seen[:]; tail.clear()
    ok = C.call(0x39C150)
    rel = lambda a: "%X" % (C.q(a) - FONT) if C.q(a) else "0"
    return {"ok": ok, "faults": C.state["faults"][:1], "last": last(), "calls": list(seen),
            "slots_rel": {"%08X" % a: rel(a) for a in (0x2AEE810, 0x2AEE850, 0x2AEE870, 0x2AEE888)}, "cache_02AEE800": "%X" % C.q(0x2AEE800)}


def measure(font):
    C.world()
    uc.mem_write(G_MGR, struct.pack("<Q", MGR))
    b = bind() if font else None
    del seen[:]; tail.clear()
    ok = C.interp(bytes([0x02, 0x41, 0x00]))[0]
    return {"bind": b, "ok": ok, "faults": C.state["faults"][:1], "last": last(), "calls": list(seen)}


with_font, without = measure(True), measure(False)
b = with_font["bind"]
code = C.raw[[ra + 0x2AC2F0 - v for v, vs, ra, rs in C.secs if v <= 0x2AC2F0 < v + rs][0]:][:0x80]
ins = list(Cs(CS_ARCH_X86, CS_MODE_64).disasm(code, 0x2AC2F0))
getter_at = [i.address for i in ins if i.mnemonic == "call" and i.op_str == "0x39c4a0"]
state_at = [i.address for i in ins if i.mnemonic == "call" and i.op_str == "0x17fd30"]
cases = {
    "F1_callback_binds_the_slots_then_the_render_enqueue_gets_no_command_slot":
        b["slots_rel"]["02AEE870"] != "0" and b["slots_rel"]["02AEE810"] != "0" and b["calls"][-3:] == ["relocator 0039BF50", "enqueue 0017FBC0", "command slot 001BA860"]
        and not b["ok"] and b["faults"] != [],
    "F2_the_font_object_cache_stays_null": b["cache_02AEE800"] == "0",
    "F3_measure_faults_on_the_null_font_object_with_or_without_the_pack": all(
        not r["ok"] and r["calls"][-2:] == ["measure 002AC2F0", "getter 0039C4A0"] and "002A9F00" not in r["calls"] for r in (with_font, without)),
    "S_measure_calls_render_state_right_after_the_getter": getter_at == [0x2AC330] and state_at == [0x2AC34E, 0x2AC363],
}
res = {"live_game": False, "with_font": with_font, "without_font": without, "static": {"getter": ["%08X" % a for a in getter_at],
       "render_state": ["%08X" % a for a in state_at]}, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "font_boundary_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-78s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({"bind": b, "measure_with_font": with_font["calls"], "measure_without": without["calls"]}))
print("ALL PASS" if res["ok"] else "FAILED")
raise SystemExit(0 if res["ok"] else 1)
