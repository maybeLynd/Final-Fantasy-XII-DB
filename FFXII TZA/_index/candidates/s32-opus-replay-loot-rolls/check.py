"""S-32: execute the loot orchestrator 003180F0 and its four roll bodies (CONTRACT-loot-rolls-and-the-chain.md LC-1..LC-4, LC-6,
LC-7) as shipped code over a foe installed by the shipped installer from a shipped area file, against an independent model of
the shared gameplay LCG (OPUS, 2026-09-25, block 349).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code; grm_e.ard
(shipped extract, ps2data/plan_master/in/plan_map/grm_e/area/grm_e.ard) is bound by the game's binder 003EA710, and its definition
1 - slots 2074 / 202B / 2074 / 2033, the same id in slots 0 and 2 - is installed by 0023A570 class 1. No application stub and no stop
boundary. Fixtures: six idle objects at 0x76300000, the unit pool with the foe (unit 0), the LCG state 022C256C, the chain rank
022C3158 and the profile switch 022C3164 where a case sets them, a 0xAB-filled output buffer of seven 8-byte entries.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ARD_PATH = os.path.join("D:" + os.sep, "FFXII_TZA_extract", "ps2data", "plan_master", "in", "plan_map", "grm_e", "area", "grm_e.ard")
ARD = open(ARD_PATH, "rb").read()
LOOT, INSTALL, BINDER = 0x3180F0, 0x23A570, 0x3EA710
SLOT, QTY, EXTRA, PROFILE = 0x3185D0, 0x3186F0, 0x318510, 0x318820
BODIES = {"slot 003185D0": (0x3185D0, 0x3186F0), "quantity 003186F0": (0x3186F0, 0x318820), "extra 00318510": (0x318510, 0x3185D0),
          "profile 00318820": (0x318820, 0x318900)}
W.ALLOWED |= ({0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (LOOT, INSTALL, BINDER))))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
REGION = 0x76400000
uc.mem_map(REGION, (len(ARD) + 0x1000 + 0xFFFF) & ~0xFFFF)
uc.mem_write(REGION + 0x1000, ARD)
assert S.call(BINDER, REGION + 0x1000), "binder"
POOL, HANDLES, LIST, SPAWNS, OUT, MASTER = 0x76280000, 0x76290000, 0x76290800, 0x762C0000, 0x762D0000, 0x2089300
STATE, RANK, SWITCH = 0x22C256C, 0x22C3158, 0x22C3164
DEF = 1


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def lcg3(s):
    for _ in range(3):
        s = (s * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return s


uc.mem_write(POOL, bytes(0xF50))
uc.mem_write(HANDLES, bytes(0x100))
uc.mem_write(SPAWNS, bytes(0x250))
w(0x208E690, "<Q", SPAWNS)
w(0x208E688, "<Q", POOL)
w(0x208E6A0, "<I", 1)
w(MASTER, "<I", 1)
w(POOL, "<Q", 1 << 26)
w(POOL + 0x10, "<Q", HANDLES)
w(POOL + 0x40, "<Q", LIST)
w(LIST, "<BB", 1, 0)
assert S.call(INSTALL, POOL, 0x0100 | DEF) and uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF == 1, "install"
DEFROW = r(POOL + 0xE60, "<Q")[0]
SLOTS = list(r(DEFROW + 0x28, "<5H"))
EXTRAS = [r(DEFROW + 0x4A, "<H")[0], r(DEFROW + 0x4E, "<H")[0]]

ev = {"writes": [], "slot_calls": [], "buckets": [], "extra_calls": 0, "profile_calls": 0}


def owner(rip):
    for nm, (lo, hi) in BODIES.items():
        if lo <= rip < hi:
            return nm
    return "%08X" % rip


uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev["writes"].append((owner(u.reg_read(UC_X86_REG_RIP)), v & 0xFFFFFFFF)),
            begin=STATE, end=STATE + 3)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev["slot_calls"].append((u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_RDX) & 0xFF)),
            begin=SLOT, end=SLOT)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev["buckets"].append(u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF), begin=0x318225, end=0x318225)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev.__setitem__("extra_calls", ev["extra_calls"] + 1), begin=EXTRA, end=EXTRA)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev.__setitem__("profile_calls", ev["profile_calls"] + 1), begin=PROFILE, end=PROFILE)


def kill(state, rank=0, switch=0):
    w(STATE, "<I", state)
    w(RANK, "<I", rank)
    w(SWITCH, "<I", switch)
    uc.mem_write(OUT, b"\xAB" * 0x38)
    ev.update(writes=[], slot_calls=[], buckets=[], extra_calls=0, profile_calls=0)
    ok = S.call(LOOT, POOL, OUT)
    out = [r(OUT + 8 * i, "<HHI") for i in range(7)]
    return {"ok": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFF, "out": [("%04X" % e[0], e[2]) for e in out],
            "writes": list(ev["writes"]), "slot_calls": list(ev["slot_calls"]), "buckets": list(ev["buckets"]),
            "extra_calls": ev["extra_calls"], "profile_calls": ev["profile_calls"], "state_after": r(STATE, "<I")[0]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


print("definition %d: slots %s extras %s" % (DEF, ["%04X" % x for x in SLOTS], ["%04X" % x for x in EXTRAS]))
kills, s = [], 0x1234567
for n in range(400):
    k = kill(s)
    kills.append(k)
    s = k["state_after"]

# ---- LC-1 / LC-2 / LC-3: one stream - every state write is three LCG steps after the previous one ----
chain_ok, prev, owners = True, 0x1234567, {}
for k in kills:
    for nm, v in k["writes"]:
        chain_ok &= v == lcg3(prev)
        prev = v
        owners[nm] = owners.get(nm, 0) + 1
record("LC1_LC3_one_stream_three_steps", all(k["ok"] for k in kills) and chain_ok and set(owners) <= set(BODIES), writers=owners,
       draws=sum(owners.values()),
       note="400 kills of grm_e def 1: every one of the %d writes to 022C256C is exactly three steps (x*0x41C64E6D + 0x3039) after "
            "the previous write, whichever inlined roll body made it - one stream, three steps per draw; all writes come from the "
            "four roll bodies" % sum(owners.values()))

# ---- LC-4: the draw count is the guarded sum ----
nonempty = sum(1 for x in SLOTS if x != 0xFFFF)
lc4_bad = [k for k in kills if len(k["writes"]) != len(k["slot_calls"]) + len(k["buckets"]) + sum(1 for nm, _ in k["writes"] if nm == "extra 00318510")
           or len(k["slot_calls"]) != nonempty]
counts = sorted({len(k["writes"]) for k in kills})
record("LC4_variable_draws", not lc4_bad and len(counts) > 1 and min(counts) >= 2 and max(counts) <= 13, draws_per_kill=counts,
       slot_rolls_per_kill=nonempty,
       note="each kill draws once per non-empty slot (%d), once more per kept slot, and once per extra that reaches its roll; the "
            "per-kill total varies over %s with the outcomes" % (nonempty, counts))

# ---- LC-7: prefill, and quantity = bucket + 1 (the hook at 00318225 reads eax BEFORE its `inc`) ----
lc7_bad = []
for k in kills:
    if any(e[0] == "FFFF" and e[1] != 0 for e in k["out"]) or any(q < 1 for iid, q in k["out"] if iid != "FFFF"):
        lc7_bad.append(k)
    kept = [i for i in range(5) if SLOTS[i] != 0xFFFF and k["out"][i][0] != "FFFF"]
    merged = SLOTS[0] == SLOTS[2] and k["out"][0][0] != "FFFF" and k["out"][2][0] == "FFFF" and len(k["buckets"]) > len(kept)
    if not merged and [k["out"][i][1] for i in kept] != [b + 1 for b in k["buckets"]]:
        lc7_bad.append(k)
empties = sum(1 for k in kills for e in k["out"] if e == ("FFFF", 0))
record("LC7_prefill_and_bucket_plus_one", not lc7_bad and empties > 0, empty_entries=empties,
       buckets_seen=sorted({b for k in kills for b in k["buckets"]}), bad=lc7_bad[:2],
       note="over a 0xAB-filled buffer every entry ends as a valid item with quantity >= 1 or exactly {FFFF, 0}; each kept slot's "
            "stored quantity is its bucket (read before `inc eax` at 00318225) plus one")

# ---- the merge: two kept slots with the same id are folded into the earlier one ----
both = [k for k in kills if len(k["buckets"]) >= 2 and k["out"][0][0] == "%04X" % SLOTS[0] and k["out"][2][0] == "FFFF"
        and k["slot_calls"] and any(nm == "quantity 003186F0" for nm, _ in k["writes"])]
merged = []
for k in kills:
    qslots = []                                          # which slots drew a quantity: the slot whose roll was followed by one
    last = None
    for nm, _ in k["writes"]:
        if nm == "slot 003185D0":
            last = (last + 1) if last is not None else 0
        elif nm == "quantity 003186F0":
            qslots.append(last)
    if 0 in qslots and 2 in qslots:
        b0, b2 = k["buckets"][qslots.index(0)], k["buckets"][qslots.index(2)]
        merged.append({"out0": k["out"][0], "out2": k["out"][2], "buckets": [b0, b2],
                       "ok": k["out"][0] == ("%04X" % SLOTS[0], b0 + 1 + b2 + 1) and k["out"][2] == ("FFFF", 0)})
record("merge_duplicate_slots", len(merged) > 0 and all(m["ok"] for m in merged), merged_kills=len(merged), examples=merged[:3],
       note="grm_e def 1 holds id %04X in slots 0 and 2: whenever both are kept, entry 2 is cleared to {FFFF, 0} and its quantity "
            "is added to entry 0 (003182A0-003182D5) - a merge pass the contract does not state" % SLOTS[0])
record("extras_not_reached", all(k["extra_calls"] == 2 and not any(nm == "extra 00318510" for nm, _ in k["writes"]) for k in kills),
       extras=["%04X" % x for x in EXTRAS],
       note="both extra-item calls return without drawing in every kill: their condition query 0030B0E0 needs the item-family storage "
            "(descriptor +8), which this world does not build - recorded, not covered")

# ---- LC-6: the rank is the default profile; the switch draws one instead ----
lc6 = {}
for rank in range(4):
    k = kill(0x0BADF00D, rank=rank)
    lc6["rank %d" % rank] = {"profiles_passed": sorted({c[0] for c in k["slot_calls"]}), "profile_calls": k["profile_calls"]}
k = kill(0x0BADF00D, rank=2, switch=1)
lc6["rank 2, switch 1"] = {"profiles_passed": sorted({c[0] for c in k["slot_calls"]}), "profile_calls": k["profile_calls"],
                           "first_write_by": k["writes"][0][0] if k["writes"] else None}
record("LC6_rank_is_the_default_profile", all(lc6["rank %d" % i]["profiles_passed"] == [i] and lc6["rank %d" % i]["profile_calls"] == 0
                                              for i in range(4))
       and lc6["rank 2, switch 1"]["profile_calls"] == 1 and lc6["rank 2, switch 1"]["first_write_by"] == "profile 00318820", cases=lc6,
       note="with 022C3164 = 0 every slot roll receives the chain rank 022C3158 as its profile (0..3); with it > 0 the profile body "
            "00318820 runs first and makes the kill's first draw")

json.dump({"ok": allok, "ard": {"path": ARD_PATH, "sha256": hashlib.sha256(ARD).hexdigest(), "definition": DEF,
                                "slots": ["%04X" % x for x in SLOTS], "extras": ["%04X" % x for x in EXTRAS]},
           "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
