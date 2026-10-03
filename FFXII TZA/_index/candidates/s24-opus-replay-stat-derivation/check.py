"""S-24: execute the stat derivation 002FEF30 (CONTRACT-stat-derivation.md, D-1..D-5, D-7 and section 12) as shipped code on
BOTH paths - the party path over the shipped battle_pack tables, the foe path over a shipped area .ard bound by the game's own
binder 003EA710 - with the reset 003105D0 and the sink 00307D10 real (OPUS, 2026-09-25, block 342).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code; the area file is
ps2data/plan_master/in/plan_map/rsn_b/area/rsn_b.ard from the shipped extract (sha256 below), bound by 003EA710. No application
stub and no stop boundary. Fixtures: four idle objects, the unit pool [0208E688] / [0208E6A0] with owning units (+0x698 -> the
record, +0x10 a zeroed actor), party / foe records.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RAX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ARD_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard"
ARD = open(ARD_PATH, "rb").read()
ARD_SHA = hashlib.sha256(ARD).hexdigest()
DERIVE, BINDER, RESET, SINK = 0x2FEF30, 0x3EA710, 0x3105D0, 0x307D10
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | W.closure(DERIVE) | W.closure(BINDER)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
ARD2_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rwf_d\area\rwf_d.ard"   # holds a definition above 9,999
ARD2 = open(ARD2_PATH, "rb").read()
ARD2_SHA = hashlib.sha256(ARD2).hexdigest()


def bind_ard(data, region):
    """copy a shipped .ard below 4 GB (the binder keeps the buffer in ebp, 003EA732) and bind it with 003EA710. The file sits
    0x1000 into its own zeroed mapping: 0036C660 (called first by the binder) tests a heap-block header at buf - 0x40 for the
    magic 0xFF12 and tags the block when present; here the header is zero, so that branch is not taken (the buffer is not a
    heap block in this world)."""
    uc.mem_map(region, (len(data) + 0x1000 + 0xFFFF) & ~0xFFFF)
    buf = region + 0x1000
    uc.mem_write(buf, data)
    assert S.call(BINDER, buf), ("binder", S.st["faults"][:2], S.st["bad"][:2], "%X" % uc.reg_read(UC_X86_REG_RIP))
    return buf


def ard_model(data, d, span, cap=1000000000):
    """independent parse of the file: main = clamp(base[+0x20] + perLevel[+0x20] * span, 1, cap), rows chosen by def +0x22 / +0x24"""
    s = struct.unpack_from("<8I", data, 0x10)
    tabs = []
    for off in (s[2], s[5], s[6]):                     # categories 2 / 3 / 4 -> 02EBF120 / 02EBF148 / 02EBF140 (003EA751-003EA7FA)
        n, st, ro = struct.unpack_from("<III", data, off + 4)
        tabs.append((off + ro, n, st))
    (D, _, dst), (B, _, bst), (L, _, lst) = tabs
    bi, li = struct.unpack_from("<HH", data, D + d * dst + 0x22)
    v = struct.unpack_from("<i", data, B + bi * bst + 0x20)[0] + struct.unpack_from("<i", data, L + li * lst + 0x20)[0] * span
    return min(max(v, 1), cap)


BUF, BUF2 = 0x76400000, 0x76500000
bind_ard(ARD, BUF)
POOL, PARTY, FOE, ACTORS = 0x76280000, 0x76290000, 0x76291000, 0x762A0000
SLOTS = {0x2EBF038 + 8 * k: "%08X" % (0x2EBF038 + 8 * k) for k in range(0x1A)}   # registry slot cells 02EBF038..02EBF100
LIST3 = [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85]                           # .rdata 00D102B0, the main-value list


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


ev = {"slot_reads": set(), "main_stores": [], "entered": [], "unit_writes": []}
uc.hook_add(UC_HOOK_MEM_READ, lambda u, acc, a, n, v, _: ev["slot_reads"].add("%08X" % (a & ~7)), begin=0x2EBF038, end=0x2EBF1FF)
for rec in (PARTY, FOE):
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev["main_stores"].append(["%08X" % u.reg_read(UC_X86_REG_RIP), v & 0xFFFFFFFF]),
                begin=rec + 0x24, end=rec + 0x27)
for a, nm in ((RESET, "reset 003105D0"), (SINK, "sink 00307D10")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev["entered"].append(nm), begin=a, end=a)
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev["unit_writes"].append("%08X" % u.reg_read(UC_X86_REG_RIP)),
            begin=POOL + 4, end=POOL + 7)


def world():
    uc.mem_write(POOL, bytes(0xF50 * 2))
    for i, rec in enumerate((PARTY, FOE)):
        uc.mem_write(rec, bytes(0x400))
        w(rec + 0x50, "<5H", *[0xFFFF] * 5)
        uc.mem_write(ACTORS + i * 0x1000, bytes(0x1000))
        w(POOL + i * 0xF50 + 0x10, "<Q", ACTORS + i * 0x1000)
        w(POOL + i * 0xF50 + 0x698, "<Q", rec)
    w(PARTY + 5, "<B", 0)
    w(FOE + 5, "<B", 1)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 2)


def derive(rec, out=0):
    for k in ev:
        ev[k] = set() if k == "slot_reads" else []
    ok = S.call(DERIVE, rec, out, 0)
    o = out or rec + 0x24
    return ok, {"main": r(o, "<i")[0], "word4": r(o + 4, "<H")[0], "bytes6_13": list(bytes(uc.mem_read(o + 6, 14))),
                "status_word": "%08X" % r(o + 0x18, "<I")[0], "stores": [s[0] for s in ev["main_stores"]],
                "entered": sorted(set(ev["entered"])), "unit_plus4": "%08X" % r(POOL + 4, "<I")[0]}


def party(t, growth, **kw):
    world()
    w(PARTY + 4, "<B", t)
    w(PARTY + 8, "<i", growth)
    for off, v in kw.get("layers", {}).items():
        w(PARTY + off, "<16s", v.to_bytes(16, "little"))
    if "status" in kw:
        w(PARTY + 0x3C, "<I", kw["status"])
    return derive(PARTY, kw.get("out", 0))


def foe(d, lo, hi, **kw):
    world()
    w(FOE + 4, "<B", d)
    w(FOE + 0x88, "<B", lo)
    w(FOE + 0x1C2, "<B", hi)
    if "status" in kw:
        w(FOE + 0x3C, "<I", kw["status"])
    return derive(FOE, kw.get("out", 0))


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


NDEF = r(r(0x2EBF120, "<Q")[0] + 4, "<I")[0]
NPARTY = r(r(0x2EBF130, "<Q")[0] + 4, "<I")[0]
print("ard", ARD_SHA, "defs", NDEF, "party rows", NPARTY)

# ---- D-1: one byte selects the source; each path reads only its own registry slots ----
okp, p = party(0, 1000)
rp = sorted(ev["slot_reads"])
okf, f = foe(0, 0, 50)
rf = sorted(ev["slot_reads"])
ARD_SLOTS, PARTY_SLOT = {"02EBF120", "02EBF140", "02EBF148", "02EBF150"}, "02EBF130"
record("D1_two_disjoint_sources", okp and okf and PARTY_SLOT in rp and not ARD_SLOTS & set(rp) and ARD_SLOTS <= set(rf)
       and PARTY_SLOT not in rf, party_slots_read=rp, foe_slots_read=rf,
       note="rec+5 = 0 reads registry slot 02EBF130 (battle_pack growth rows) and none of the four .ard slots; rec+5 = 1 reads "
            "02EBF120 / 140 / 148 / 150 and never 02EBF130")

# ---- D-2 / D-3: every output inside its cap; the main-value cap is 9,999 for rec+5 = 0 and 1e9 otherwise ----
sweep, bad, model_miss = [], [], []


def foe_sweep(tag, data, ndef):
    for d in range(ndef):
        for lo, hi in ((0, 0), (0, 50), (0, 255)):
            ok, x = foe(d, lo, hi)
            sweep.append((tag, d, hi - lo, ok, x["main"]))
            if not ok or not (1 <= x["main"] <= 1000000000 and x["word4"] <= 999 and all(b <= 0xFF for b in x["bytes6_13"])):
                bad.append((tag, d, lo, hi, ok, x))
            if x["main"] != ard_model(data, d, hi - lo):
                model_miss.append((tag, d, hi - lo, x["main"], ard_model(data, d, hi - lo)))


foe_sweep("rsn_b", ARD, NDEF)
bind_ard(ARD2, BUF2)
NDEF2 = r(r(0x2EBF120, "<Q")[0] + 4, "<I")[0]
foe_sweep("rwf_d", ARD2, NDEF2)
for t in range(min(NPARTY, 0x28)):
    for g in (0, 1000000, 0x7FFFFFFF):
        ok, x = party(t, g)
        sweep.append(("party", t, g, ok, x["main"]))
        cap = 32767 if 0x1B <= t <= 0x27 else 9999
        if not ok or not (1 <= x["main"] <= cap and x["word4"] <= 999):
            bad.append(("party", t, g, ok, x))
foe_max = max(s[4] for s in sweep if s[0] != "party")
party_max = max(s[4] for s in sweep if s[0] == "party" and not 0x1B <= s[1] <= 0x27)
nfoe = (NDEF + NDEF2) * 3
record("D2_every_output_inside_its_cap", not bad and not model_miss and len(sweep) == nfoe + min(NPARTY, 0x28) * 3,
       runs=len(sweep), outside=bad[:5], model_mismatches=model_miss[:5],
       note="all %d + %d foe definitions of the shipped rsn_b.ard / rwf_d.ard at level spans 0 / 50 / 255 (main value equal to an "
            "independent parse of the file in every run) and party types 0..0x27 at growth inputs 0 / 1e6 / 0x7FFFFFFF: every main "
            "value lies in [1, cap], every word and byte field inside its cap" % (NDEF, NDEF2))
record("D3_one_cmove_picks_the_cap", party_max == 9999 and foe_max > 9999, party_max=party_max, foe_max=foe_max,
       note="the party path saturates at exactly 9,999; the same writeback on the foe path passes %d through (cap 1e9)" % foe_max)

# ---- D-4: the 32,767 band is a second store to the same slot, for party types 0x1B..0x27 only ----
d4 = {}
for t in (0x00, 0x1A, 0x1B, 0x1E, 0x27):
    ok, x = party(t, 100000)
    d4["%02X" % t] = {"ok": ok, "main": x["main"], "stores": [s for s in ev["main_stores"] if s[0] != "002FEFB9"]}
inband = [v for k, v in d4.items() if 0x1B <= int(k, 16) <= 0x27]
outband = [v for k, v in d4.items() if not 0x1B <= int(k, 16) <= 0x27]
record("D4_second_write_of_the_same_slot",
       len(inband) == 3 and all(v["ok"] and v["stores"] == [["002FF7E2", 9999], ["002FF805", 32767]] and v["main"] == 32767 for v in inband)
       and len(outband) == 2 and all(v["ok"] and v["stores"] == [["002FF7E2", 9999]] and v["main"] == 9999 for v in outband), types=d4,
       note="growth input 100,000: party types 0x1B / 0x1E / 0x27 store rec+0x24 = 9,999 at 002FF7E2 and AGAIN = 32,767 at 002FF805, "
            "and the second survives; types 0x00 / 0x1A store 9,999 once. The band is decided at 002FF007-002FF011 "
            "(rec+5 == 0 and rec+4 - 0x1B <= 0xC)")
growth_ret = []
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: growth_ret.append(struct.unpack("<i", struct.pack("<I", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF))[0]),
            begin=0x2FF080, end=0x2FF080)                  # the return of 002F8E50 (called at 002FF07B)
wrap = {}
for t, g in ((0x06, 0x7FFFFFFF), (0x0C, 100000000), (0x1B, 10000000), (0x00, 0x7FFFFFFF), (0x1B, 1000000)):
    del growth_ret[:]
    ok, x = party(t, g)
    wrap["%02X at %d" % (t, g)] = {"ok": ok, "main": x["main"], "002F8E50_returned": growth_ret[:]}
k = list(wrap.values())
record("growth_input_wraps_to_the_floor", all(v["ok"] and len(v["002F8E50_returned"]) == 1 for v in k)
       and all(v["main"] == 1 and v["002F8E50_returned"][0] <= 0 for v in k[:3])
       and k[3]["main"] == 9999 and k[3]["002F8E50_returned"][0] > 9999 and k[4]["main"] == 32767 and k[4]["002F8E50_returned"][0] > 32767,
       cases=wrap,
       note="for some types a large rec+8 input makes 002F8E50 return a non-positive value, so the party main value lands on the "
            "floor 1 (types 0x06 / 0x0C / 0x1B at 0x7FFFFFFF / 1e8 / 1e7); type 0x00 at 0x7FFFFFFF and 0x1B at 1e6 return above "
            "their caps and are capped. The threshold is type-dependent; D-2's floor holds. Observed only - what rec+8 counts, "
            "and its shipped range, is not claimed")

# ---- D-5 / section 12: a status in the derived layer alone still pays its bonus ----
d5 = {}
for n in LIST3:
    _, none = party(0, 1000)
    _, mut = party(0, 1000, layers={0x68: 1 << n})
    _, der = party(0, 1000, layers={0x78: 1 << n})
    d5[n] = {"none": none["main"], "mutable": mut["main"], "derived": der["main"]}
paying = {n: v for n, v in d5.items() if v["mutable"] != v["none"]}
record("D5_either_layer_pays_the_bonus", paying and all(v["mutable"] == v["derived"] for v in d5.values()), ids=d5,
       paying_ids=sorted(paying),
       note="each of the twelve main-value list ids (.rdata 00D102B0) set in the mutable layer only or the derived layer only "
            "gives the SAME main value; %d of them change it from the no-status value" % len(paying))

# ---- D-7: the tail runs only when rec+5 == 0, the output is the record's own block with an owner, and bits 0x8000020 change ----
_, base = party(0, 1000)
settled = int(base["status_word"], 16)
d7 = {}
for label, kw, fn in (("party, own block, bit 5 flips", {"status": settled ^ 0x20}, party),
                      ("party, own block, no change", {"status": settled}, party),
                      ("party, explicit output block, bit 5 flips", {"status": settled ^ 0x20, "out": 0x762C0000}, party),
                      ("foe, own block, bit 5 flips", {"status": 0x20}, foe)):
    args = (0, 1000) if fn is party else (0, 0, 50)
    ok, x = fn(*args, **kw)
    d7[label] = {"ok": ok, "entered": x["entered"], "unit_plus4": x["unit_plus4"], "unit_writes": ev["unit_writes"][:]}
t = d7
record("D7_tail_behind_three_guards",
       all(v["ok"] for v in t.values()) and t["party, own block, bit 5 flips"]["entered"] == ["reset 003105D0", "sink 00307D10"]
       and t["party, own block, bit 5 flips"]["unit_plus4"] == "00200000"
       and all(not t[k]["entered"] and t[k]["unit_plus4"] == "00000000" for k in list(t)[1:]),
       cases=d7, settled_status_word="%08X" % settled,
       note="with the record's own output block, an owning unit and a flip of bit 5 of +0x3C, the tail runs: the reset 003105D0 "
            "and the sink 00307D10 execute real and unit+4 gains 0x200000 (002FFA38); no change, an explicit output block, or a "
            "foe record each return at 002FFA45 with no unit write")

json.dump({"ok": allok, "ard": [{"path": ARD_PATH, "sha256": ARD_SHA, "defs": NDEF}, {"path": ARD2_PATH, "sha256": ARD2_SHA, "defs": NDEF2}],
           "bound": made,
           "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
