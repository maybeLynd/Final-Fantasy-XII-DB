"""S-32: execute the defeat-rewards body 00312280 (CONTRACT-defeat-rewards-sequence.md DR-1..DR-6) over foes installed by the
shipped installer 0023A570 from shipped area files, with shipped party rows as recipients (OPUS, 2026-09-25, block 344).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code; the area files
(shipped extract, ps2data/plan_master/in/plan_map/...) are bound by the game's own binder 003EA710 (block 342), each rewritten
fresh before every bind because the binder relocates the file's tables in place. No application stub.
ONE STOP BOUNDARY: the message poster 0046AB10, which the gil notifier 00469E80 calls with event 0x26 for a positive gil delta and
which leads into the font/painter surface (001B5FA0 = the text singleton [01F811F8]) this world does not build. The run ENDS
there and its arguments are recorded; the zero-gil runs never reach it and run 00312280 to its return.
Fixtures: six idle objects (the world's convention; 02092758 holds gil at +8, 020927C0 the game-state block), the unit pool with
the foe (unit 0, installed by 0023A570 class 1: flag bit 26, +0x10 handle, +0x40 spawn list {1, 0}) and three party units owning
battle-state rows 0..2 (+4 type, +0x1C2 level, +0x18C EXP, +0x190 LP), slot map 0 = {0, 1, 2} with maps 1-4 built by the real
refresher 003266C0, a zeroed spawn pool, the master flag.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
AREAS = {n: r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\%s\area\%s.ard" % (n, n) for n in ("bds_a", "rsn_b")}
DATA = {n: open(p, "rb").read() for n, p in AREAS.items()}
REWARDS, INSTALL, BINDER, REFRESH, POSTER = 0x312280, 0x23A570, 0x3EA710, 0x3266C0, 0x46AB10
TAILS = {0x315820}                                     # 00253750 is `jmp 00315820` (a game-state flag-array reader)
W.ALLOWED |= ({0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(t) | {t} for t in TAILS)) | W.closure(REWARDS)
              | W.closure(INSTALL) | W.closure(BINDER) | W.closure(REFRESH))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76300000                                      # clear of the unit pool (0x76280000) and handles
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
GIL = IDLE + 4 * 0x20000 + 8                           # [02092758] + 8, read by 00253690
REGIONS = {"bds_a": 0x76400000, "rsn_b": 0x76500000}
for n, reg in REGIONS.items():
    uc.mem_map(reg, (len(DATA[n]) + 0x1000 + 0xFFFF) & ~0xFFFF)
POOL, HANDLES, LIST, SPAWNS, MASTER = 0x76280000, 0x76290000, 0x76290800, 0x762C0000, 0x2089300
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
MAP0 = BLOCK + 0x5A48


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def row(i):
    return BLOCK + 8 + i * 0x1C8


def bind(area):
    buf = REGIONS[area] + 0x1000
    uc.mem_write(buf, DATA[area])                       # fresh bytes: the binder relocates the tables in place
    assert S.call(BINDER, buf), ("binder", area)


SITES = {0x3122CD: "317ED0", 0x3122D5: "3171C0", 0x312367: "320AB0 recipients", 0x3123D1: "2F8BB0 EXP", 0x3123DE: "2F90C0 LP",
         0x312453: "2F8F20 threshold", 0x31246C: "2F8F20 threshold", 0x312496: "316A50", 0x3124A3: "30C650 advance", 0x3124BE: "2F8BB0 EXP(NULL)",
         0x3124CA: "2F90C0 LP(NULL)", 0x312518: "28FB80 presentation", 0x31254C: "253690 gil read", 0x31255D: "254EE0 gil set",
         0x312566: "469E80 notify", 0x31257E: "265020", 0x312588: "319490 item placement", 0x3125A1: "3180F0", 0x3125B4: "319CA0",
         0x3125BC: "317090 retire"}
ev = {"sites": [], "args": {}, "rets": {}, "boundary": []}


def on_site(u, x, n, _):
    ev["sites"].append(SITES[x])
    ev["args"].setdefault(SITES[x], []).append([u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                                                u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF])


for a in SITES:
    uc.hook_add(UC_HOOK_CODE, on_site, begin=a, end=a)
for a, nm in ((0x3124C3, "EXP(NULL)"), (0x3124CF, "LP(NULL)")):   # the instruction after each NULL call: eax = the result
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev["rets"].setdefault(nm, []).append(
        struct.unpack("<i", struct.pack("<I", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF))[0]), begin=a, end=a)


def _boundary(u, x, n, _):
    ev["boundary"].append({"at": "%08X" % x, "rcx": u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, "edx": "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)})
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, _boundary, begin=POSTER, end=POSTER)


def world(area, foe_def, levels=(10, 10, 10), exps=(0, 0, 0), lps=(0, 0, 0), foe_span=None, layers=None, gil=0):
    bind(area)
    uc.mem_write(POOL, bytes(0xF50 * 4))
    uc.mem_write(HANDLES, bytes(0x400))
    uc.mem_write(SPAWNS, bytes(0x250 * 4))
    w(0x208E690, "<Q", SPAWNS)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 4)
    w(MASTER, "<I", 1)
    w(GIL, "<I", gil)
    for i in range(3):
        rec = row(i)
        uc.mem_write(rec, bytes(0x1C8))
        w(rec + 4, "<BB", i, 0)
        w(rec + 0x1C2, "<B", levels[i])
        w(rec + 0x18C, "<ii", exps[i], lps[i])
        for off, v in (layers or {}).get(i, {}).items():
            w(rec + off, "<16s", v.to_bytes(16, "little"))
        u = POOL + (i + 1) * 0xF50
        w(u + 0x10, "<Q", HANDLES + (i + 1) * 0x100)
        w(u + 0x698, "<Q", rec)
    uc.mem_write(MAP0, struct.pack("<9H", 0, 1, 2, *[0xFFFF] * 6))
    assert S.call(REFRESH, 0), "refresh"
    foe = POOL
    w(foe, "<Q", 1 << 26)
    w(foe + 0x10, "<Q", HANDLES)
    w(foe + 0x40, "<Q", LIST)
    w(LIST, "<BB", 1, 0)
    assert S.call(INSTALL, foe, 0x0100 | foe_def) and uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF == 1, "install"
    fs = r(foe + 0x698, "<Q")[0]
    if foe_span is not None:
        w(fs + 0x88, "<B", 0)
        w(fs + 0x1C2, "<B", foe_span)
    return foe


def kill(foe, killer=0):
    for k in ("sites", "boundary"):
        ev[k] = []
    ev["args"], ev["rets"] = {}, {}
    ok = S.call(REWARDS, row(killer), foe)
    at_boundary = uc.reg_read(UC_X86_REG_RIP) == POSTER and not S.st["faults"] and not S.st["bad"] and len(ev["boundary"]) == 1
    return {"returned": ok, "at_boundary": at_boundary, "faults": S.st["faults"][:2], "bad": S.st["bad"][:2],
            "sites": list(ev["sites"]), "args": ev["args"], "rets": ev["rets"], "boundary": list(ev["boundary"]),
            "party": [{"level": r(row(i) + 0x1C2, "<B")[0], "exp": r(row(i) + 0x18C, "<i")[0], "lp": r(row(i) + 0x190, "<i")[0]}
                      for i in range(3)], "gil": r(GIL, "<I")[0]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


def first_order(sites):
    seen = []
    for s in sites:
        if s not in seen:
            seen.append(s)
    return seen


# ---- DR-1: the whole body, in order, over a zero-gil shipped foe (bds_a def 0) ----
k1 = kill(world("bds_a", 0))
order = first_order(k1["sites"])
WANT = ["3171C0", "320AB0 recipients", "2F8BB0 EXP", "2F90C0 LP", "2F8F20 threshold", "316A50", "30C650 advance", "2F8BB0 EXP(NULL)",
        "2F90C0 LP(NULL)", "28FB80 presentation", "253690 gil read", "254EE0 gil set", "469E80 notify", "265020",
        "319490 item placement", "317090 retire"]
record("DR1_order_to_the_return", k1["returned"] and [s for s in order if s in WANT] == WANT and k1["sites"].count("30C650 advance") == 3,
       order=order, party=k1["party"], gil=k1["gil"], faults=k1["faults"], bad=k1["bad"],
       note="bds_a def 0 (gil terms 0): 00312280 runs to its return with no stub - recipients (9 slot lookups), per recipient "
            "EXP / LP / threshold walk / 00316A50 / advance, then the NULL-recipient EXP and LP, presentation 0028FB80, gil read / "
            "set / notify, item placement, retirement - in the order DR-1 states")

# ---- DR-2: the NULL calls and the shared division ----
exp_null = k1["rets"].get("EXP(NULL)", [None])[0]
lp_null = k1["rets"].get("LP(NULL)", [None])[0]
pres = k1["args"].get("28FB80 presentation", [[0, 0, 0]])[0]
record("DR2_null_recipient_calls", k1["returned"] and [a[0] for a in k1["args"].get("2F8BB0 EXP(NULL)", [[1]])] == [0]
       and [a[0] for a in k1["args"].get("2F90C0 LP(NULL)", [[1]])] == [0] and all(p["exp"] == k1["party"][0]["exp"] for p in k1["party"])
       and exp_null is not None and pres[1] == exp_null and pres[2] == max(0, min(lp_null, 999)),
       gains=[p["exp"] for p in k1["party"]], exp_null=exp_null, lp_null=lp_null, presentation_edx_r8=pres[1:],
       note="after the loop the body calls 002F8BB0 and 002F90C0 with rcx = 0 (003124BC / 003124C6); each of the three recipients "
            "gains %d EXP and the NULL result %s goes to the presentation call 0028FB80 (edx = EXP, r8 = LP)" % (k1["party"][0]["exp"], exp_null))

# ---- DR-3: levelling is a search - one advance call carrying the searched target ----
# A level change makes the advance 0030C650 post through the same poster 0046AB10, so these runs END at the boundary inside
# the advance, after the walk and after the level store; the other recipients are not reached.
d3 = {}
for label, lv, xp in (("level 10, 250,000 EXP", 10, 250000), ("level 98, the EXP cap", 98, 99999999)):
    k = kill(world("bds_a", 0, levels=(lv, 10, 10), exps=(xp, 0, 0)))
    adv = k["args"].get("30C650 advance", [])
    d3[label] = {"at_boundary": k["at_boundary"], "boundary": k["boundary"], "advance_calls": [a[1] for a in adv],
                 "threshold_calls": k["sites"].count("2F8F20 threshold"), "level_after": k["party"][0]["level"], "exp_after": k["party"][0]["exp"]}
a, b = d3["level 10, 250,000 EXP"], d3["level 98, the EXP cap"]
record("DR3_level_walk_is_a_search", a["at_boundary"] and len(a["advance_calls"]) == 1 and a["advance_calls"][0] > 11
       and a["level_after"] == a["advance_calls"][0] and a["threshold_calls"] == a["advance_calls"][0] - 10 + 1
       and b["at_boundary"] and b["advance_calls"] == [99] and b["level_after"] == 99, cases=d3,
       note="level 10 with 250,000 EXP: the walk calls the threshold %d times and ONE advance call carries target %d (a %d-level "
            "rise from one kill); level 98 at the EXP cap stops at 99. Each run ends at the poster boundary inside the advance"
            % (a["threshold_calls"], a["advance_calls"][0] if a["advance_calls"] else -1,
               (a["advance_calls"][0] - 10) if a["advance_calls"] else -1))

# ---- DR-4: the gil term reads the DEFEATED unit's span and +0x30 of its two rows (rsn_b def 0: 8 flat, 3 per level) ----
d4 = {}
for label, span, lv in (("foe span 0, party 10", 0, 10), ("foe span 5, party 10", 5, 10), ("foe span 5, party 50", 5, 50)):
    k = kill(world("rsn_b", 0, levels=(lv, lv, lv), foe_span=span))
    d4[label] = {"at_boundary": k["at_boundary"], "boundary": k["boundary"], "gil_after_set": k["gil"],
                 "notify_arg": k["args"].get("469E80 notify", [[None]])[0][0], "faults": k["faults"], "bad": k["bad"]}
record("DR4_gil_reads_the_defeated_units_span", all(v["at_boundary"] for v in d4.values())
       and d4["foe span 0, party 10"]["gil_after_set"] == 8 and d4["foe span 5, party 10"]["gil_after_set"] == 23
       and d4["foe span 5, party 50"]["gil_after_set"] == 23 and all(v["boundary"][0]["edx"] == "26" for v in d4.values()),
       cases=d4,
       note="gil = (foe +0x1C2 - foe +0x88) x [unit+0xE78]+0x30 + [unit+0xE70]+0x30 = 8 + 3 x span: 8 at span 0, 23 at span 5, and "
            "23 again with the recipients at level 50 - the recipients' level does not enter the gil term. Each run ends at the "
            "boundary 0046AB10 with event 0x26")

# ---- DR-5: status id 12 converts LP into gil, in either layer, with the RECIPIENT's level ----
d5 = {}
for label, off in (("id 12 in the mutable layer", 0x68), ("id 12 in the derived layer", 0x78)):
    k = kill(world("bds_a", 0, levels=(20, 10, 10), layers={0: {off: 1 << 12}}))
    d5[label] = {"at_boundary": k["at_boundary"], "gil": k["gil"], "lp": [p["lp"] for p in k["party"]], "faults": k["faults"]}
k0 = kill(world("bds_a", 0, levels=(20, 10, 10)))
lp_plain = k0["party"][0]["lp"]
record("DR5_status12_converts_lp_to_gil", k0["returned"] and lp_plain > 0 and all(
    v["at_boundary"] and v["lp"][0] == 0 and v["lp"][1] == lp_plain and v["gil"] == 5 * 20 * lp_plain for v in d5.values()),
       cases=d5, lp_without_status=lp_plain,
       note="a zero-gil foe; recipient 0 at level 20 with id 12 (either layer) receives NO LP and the gil accumulator gains "
            "5 x 20 x LP (x + 4x), so the zero-gil kill now pays gil and ends at the poster boundary; without id 12 the same "
            "recipient gains the LP and the run returns")

# ---- DR-6: the reported delta can exceed the stored gain ----
k6 = kill(world("rsn_b", 0, foe_span=0, gil=99999995))
setter = k6["args"].get("254EE0 gil set", [[0]])[0][0] & 0xFFFFFFFF
notify = k6["args"].get("469E80 notify", [[0]])[0][0] & 0xFFFFFFFF
record("DR6_report_exceeds_stored_gain", k6["at_boundary"] and k6["gil"] == 99999999 and setter == 100000003 and notify == 8,
       gil_after=k6["gil"], setter_arg=setter, notify_arg=notify,
       note="old gil 99,999,995 and award 8: the setter 00254EE0 receives 100,000,003 and stores 99,999,999 (gain 4); the notifier "
            "receives requested - old = 8 and posts event 0x26 (the boundary)")

json.dump({"ok": allok, "areas": {n: {"path": AREAS[n], "sha256": hashlib.sha256(DATA[n]).hexdigest()} for n in AREAS},
           "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
