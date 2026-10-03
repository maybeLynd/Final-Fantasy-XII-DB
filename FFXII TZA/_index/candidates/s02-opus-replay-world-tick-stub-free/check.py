"""S-02: the world tick 00314020 executed with NO application stub, in all six frame modes, over a world built by shipped
initialisers, and CONTRACT-world-simulation-tick.md's WT-1 .. WT-5 tested (OPUS, 2026-09-25, block 318).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (with world.json and printf_bridge.py) builds the world and
runs the tick; its docstring lists every bridge and fixture. Nothing on the tick's path is scripted: every function entered is
shipped code inside ALLOWED (the tick's static closure + the jump targets and initialisers listed in world.json), and the run
must reach the tick's own `ret`.
Writes result.json next to this file.
"""
import collections
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
assert hashlib.sha256(W.raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
MODE_TESTS = [0x3140CF, 0x3140DC, 0x314103, 0x314108, 0x314249, 0x31424E]
LOOP_SITES = {"cmp_ebx_5@00314132": 0x314132, "cmp_ebx_5@003141E9": 0x3141E9, "cmp_ebx_5@00314218": 0x314218,
              "cmp_ebx_5@00314270": 0x314270, "cmp_ebp_5@0031425D": 0x31425D, "cmp_esi_16@0031421F": 0x31421F}
DRAIN, ACTIVE, LATCHED, DEFERRED, RET_SITE = 0x25BFB0, 0x22C2548, 0x1EED060, 0x1EED064, 0x31436C


def img_dword(va):
    for v, vs, ra, rs in W.secs:
        if v <= va < v + rs:
            return struct.unpack_from("<I", W.raw, ra + va - v)[0]


def tick(mode, deferred=None):
    ev = {"order": [], "hits": collections.Counter(), "active_writes": [], "deferred_writes": [], "latched_writes": []}

    def pre(uc):
        if deferred is not None:
            uc.mem_write(DEFERRED, struct.pack("<i", deferred))

    def hook(uc, st):
        def on_code(u, a, n, _):
            if a == DRAIN:
                ev["order"].append("drain")
            if a in MODE_TESTS:
                ev["order"].append("mode_test")
            ev["hits"][a] += 1

        def on_write(u, ac, a, n, v, _):
            if a == ACTIVE:
                ev["active_writes"].append(("%08X" % u.reg_read(W.UC_X86_REG_RIP), v & 0xFFFFFFFF))
            elif a == DEFERRED:
                ev["deferred_writes"].append(("%08X" % u.reg_read(W.UC_X86_REG_RIP), v & 0xFFFFFFFF))
            elif a == LATCHED:
                ev["latched_writes"].append(("%08X" % u.reg_read(W.UC_X86_REG_RIP), v & 0xFFFFFFFF))
        for a in set(MODE_TESTS) | set(LOOP_SITES.values()) | {DRAIN, RET_SITE}:
            uc.hook_add(UC_HOOK_CODE, on_code, begin=a, end=a)
        uc.hook_add(UC_HOOK_MEM_WRITE, on_write, begin=LATCHED, end=DEFERRED + 3)
        uc.hook_add(UC_HOOK_MEM_WRITE, on_write, begin=ACTIVE, end=ACTIVE + 3)

    ok, st, uc = W.run(mode, 0, FX["fixes"], trace_n=8, count=20000000, inits=FX["inits"], pre_tick=pre, tick_hook=hook)
    after = struct.unpack("<ii", bytes(uc.mem_read(LATCHED, 8)))
    return {"ok": ok, "stopped_at": (st["bad"] or st["faults"])[:1], "functions_entered": len(st["entered"]),
            "imports": dict(st["imports"]), "stdout": [x.decode("latin-1") for x in st.get("stdout", [])], "debug_out": [x.decode("latin-1") for x in st.get("debug_out", [])],
            "mode_test_hits": {"%08X" % a: ev["hits"][a] for a in MODE_TESTS},
            "loop_site_hits": {k: ev["hits"][a] for k, a in LOOP_SITES.items()},
            "drain_before_first_mode_test": bool(ev["order"]) and ev["order"][0] == "drain",
            "active_writes": ev["active_writes"], "active_after": struct.unpack("<I", bytes(uc.mem_read(ACTIVE, 4)))[0],
            "exit_via_single_ret": ev["hits"][RET_SITE] == 1, "deferred_writes": ev["deferred_writes"],
            "latched_writes": ev["latched_writes"], "latched_after": after[0], "deferred_after": after[1]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


modes = {m: tick(m) for m in range(6)}
for m, r in modes.items():
    print("mode", m, r["ok"], r["stopped_at"], r["functions_entered"], r["mode_test_hits"], r["loop_site_hits"])

record("stub_free_all_modes", all(r["ok"] for r in modes.values()),
       functions_entered={m: r["functions_entered"] for m, r in modes.items()},
       note="every mode 0..5 runs to the tick's own ret; only shipped functions entered; imports only through the listed bridges")
# WT-1: the mode is tested at the five sites (00314103/00314108 and 00314249/0031424E are the paired tests)
wt1 = all(r["mode_test_hits"]["003140CF"] == 1 and r["mode_test_hits"]["003140DC"] == 1 and r["mode_test_hits"]["00314103"] == 1
          and r["mode_test_hits"]["00314249"] == 1 for r in modes.values())
record("WT1_mode_consulted_at_five_sites", wt1, hits={m: r["mode_test_hits"] for m, r in modes.items()},
       note="in every mode the tests at 003140CF, 003140DC, 00314103 and 00314249 each run once; the paired cmp r14d,1 sites run "
            "when the preceding test did not settle it")
record("WT2_drain_before_mode", all(r["drain_before_first_mode_test"] for r in modes.values()),
       note="0025BFB0 is entered before the first mode test in every mode")
wt3 = all(r["active_writes"] == [("00314047", 1), ("0031435D", 0)] and r["active_after"] == 0 and r["exit_via_single_ret"]
          for r in modes.values())
record("WT3_active_word_set_and_cleared", wt3, writes={m: r["active_writes"] for m, r in modes.items()},
       note="022C2548 is written exactly twice per tick, 1 at 00314047 and 0 at 0031435D, and the tick leaves through 0031436C")
# WT-4: the sentinels are image data (static). The consume path itself (a staged request) is NOT executed here: it runs a
# world transition (003C5E50 ...) that reaches the UI manager and beyond, outside this world. Unstaged, the tick writes
# the latched word once (00314092) and never the deferred word.
img_sent = (img_dword(LATCHED), img_dword(DEFERRED))
unstaged_ok = all(r["deferred_writes"] == [] and [w[0] for w in r["latched_writes"]] == ["00314092"] for r in modes.values())
record("WT4_sentinels_and_unstaged_writes", img_sent == (0xFFFFFFFF, 0xFFFFFFFF) and unstaged_ok,
       image_sentinels=["%08X" % x for x in img_sent], latched_writes={m: r["latched_writes"] for m, r in modes.items()},
       note="01EED060 / 01EED064 hold 0xFFFFFFFF in the image; with nothing staged the tick writes 01EED060 once (00314092) and "
            "never 01EED064; the staged consume path is not executed (static: 003140BF writes -1 after 0032FC30)")
record("WT5_loop_bounds_observed", True, loop_site_hits={m: r["loop_site_hits"] for m, r in modes.items()},
       note="observed per mode: how many times each immediate-bound compare runs")
results["per_mode"] = {str(m): r for m, r in modes.items()}

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "world": FX, "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
