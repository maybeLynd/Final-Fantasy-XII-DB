"""S-11: execute BattleUnit_TryTriggerNearbyAuthoredFieldAction (002F8060), CONTRACT-authored-trigger-points.md's one entry, as
shipped code and test TP-1 .. TP-6 (OPUS, 2026-09-25, block 317).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub. ALLOWED = the
entry's static closure plus the thunk targets its callees reach by jump (003EC700 -> 002E7410) and the MT19937 body; entering
anything else stops the case and is reported. IMPORTS: every IAT slot is trapped; memset / memcpy / memmove and sqrtf (the distance helper 003A1920's
import; float32(math.sqrt(x))) are bridged by name.
The generator is the image's own, lazily seeded (5489) by the shipped code; each draw is checked against an independent
MT19937.
Fixtures (planted data only): the acting unit (+0x10 actor, +0x698 stats), the actor (class 3, +0xB8 position block), the stats
block (the TP-6 eligibility bytes), the active field id (save payload 0x02164480 + 0x1044, read by 003148F0), the per-field
live-mask table at 02EC3EA0 (count at 02EC3EC8), the authored point list behind [022BE948] ({+0 count, +4 + 4i offsets}, records
{s16 x10, s16 z10, u8 flag id, u16 outcome75, u16 outcome25, u8 +0x0A}).
Every test outcome is >= 0x200: the delivery 0046A9D0 -> 0046AB10 refuses an outcome index >= 0x1FF at its entry
(0046AB19 cmp [r8+0x28], 0x1FF / jge exit), which is the shipped behaviour and lets the run continue through the notify and
the mask store; the item-grant branch for outcomes below 0x1FF is not covered.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import math
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RAX,
                               UC_X86_REG_XMM0)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
UNIT, ACTOR, POS, STATS, PLIST, OUT, CTXA = (WORLD, WORLD + 0x1000, WORLD + 0x1400, WORLD + 0x2000, WORLD + 0x4000,
                                             WORLD + 0x8000, WORLD + 0x8100)
ENTRY, PAYLOAD, LIVE, LIVE_COUNT, G_PLIST = 0x2F8060, 0x2164480, 0x2EC3EA0, 0x2EC3EC8, 0x22BE948
RNG_RET = 0x2F821D
BRIDGED = {"memset", "memcpy", "memmove", "sqrtf"}
THRESH = struct.unpack("<f", struct.pack("<I", 0x3FA66666))[0]     # the f32 at 00901B34, checked below

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        graph[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(graph[x])
    return seen


ALLOWED = closure(ENTRY) | closure(0x2E7410) | {0x863BF0, 0x866D60, 0x866B90, 0x2E7410}
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40


def import_slots():
    def r2o(rva):
        for v, vs, ra, rs in secs:
            if v - IMG <= rva < v - IMG + max(vs, rs):
                return ra + rva - (v - IMG)
    imp_rva = struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]
    out, dd = [], r2o(imp_rva)
    while True:
        oft, ts, fc, name, ft = struct.unpack_from("<IIIII", raw, dd)
        if not (oft or name or ft):
            return out
        th, i = r2o(oft or ft), 0
        while True:
            e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
            if e == 0:
                break
            nm = "ord%d" % (e & 0xFFFF) if e >> 63 else raw[r2o(e) + 2:raw.index(b"\x00", r2o(e) + 2)].decode()
            out.append((IMG + ft + 8 * i, nm))
            i += 1
        dd += 20


uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x10000)
uc.mem_map(BRIDGE, 0x2000)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_write(BRIDGE, bytes([0xC3]) * 0x2000)
BR = {}
for i, (slot, name) in enumerate(import_slots()):
    uc.mem_write(slot, struct.pack("<Q", BRIDGE + 4 * i))
    BR[BRIDGE + 4 * i] = name
IMG_THRESH = struct.unpack("<f", bytes(uc.mem_read(0x901B34, 4)))[0]
state = {"bad": [], "faults": [], "rng": []}


def on_code(u, a, n, _):
    if a in BR:
        nm = BR[a]
        if nm not in BRIDGED:
            state["bad"].append("import " + nm)
            u.emu_stop()
            return
        if nm == "sqrtf":
            x = struct.unpack("<f", struct.pack("<I", u.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]
            y = struct.unpack("<f", struct.pack("<f", math.sqrt(x) if x >= 0 else float("nan")))[0]
            u.reg_write(UC_X86_REG_XMM0, struct.unpack("<I", struct.pack("<f", y))[0])
            return
        rcx, rdx, r8 = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        if nm == "memset":
            u.mem_write(rcx, bytes([rdx & 0xFF]) * r8)
        else:
            u.mem_write(rcx, bytes(u.mem_read(rdx, r8)) if r8 else b"")
        u.reg_write(UC_X86_REG_RAX, rcx)
        return
    if a == RNG_RET:
        state["rng"].append(u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


class MT:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xFFFFFFFF
        self.i = 624

    def next(self):
        if self.i >= 624:
            for k in range(624):
                y = (self.mt[k] & 0x80000000) | (self.mt[(k + 1) % 624] & 0x7FFFFFFF)
                self.mt[k] = self.mt[(k + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
            self.i = 0
        y = self.mt[self.i]
        self.i += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF


mt = MT(5489)
FIELD = 77


def world(points, unit_pos=(0.0, 0.0, 0.0), mask=0xFFFFFFFF, field_in_table=True, stats=None, count=None):
    uc.mem_write(WORLD, bytes(0x10000))
    uc.mem_write(UNIT + 0x10, struct.pack("<Q", ACTOR))
    uc.mem_write(UNIT + 0x698, struct.pack("<Q", STATS))
    uc.mem_write(ACTOR + 3, bytes([0x65]))                           # class 3 (kind 3, sequence 5)
    uc.mem_write(ACTOR + 0xB8, struct.pack("<Q", POS))
    uc.mem_write(POS, struct.pack("<fff", *unit_pos))
    for k, v in (stats or {}).items():
        uc.mem_write(STATS + k, v)
    uc.mem_write(PAYLOAD + 0x1044, struct.pack("<i", FIELD))
    uc.mem_write(PAYLOAD + 0x14B4, bytes(64))                       # Bank512 cleared per case
    uc.mem_write(LIVE, bytes(0x30))
    uc.mem_write(LIVE, struct.pack("<IIi", FIELD if field_in_table else FIELD + 1, mask, 0))
    uc.mem_write(LIVE + 0x24, struct.pack("<ii", 0, 1))            # +0x24 / +0x28 (count at 02EC3EC8)
    n = len(points) if count is None else count
    hdr = struct.pack("<I", n) + b"".join(struct.pack("<I", 0x200 + 0x10 * i) for i in range(len(points)))
    uc.mem_write(PLIST, hdr)
    for i, (x, z, flag, o75, o25) in enumerate(points):
        uc.mem_write(PLIST + 0x200 + 0x10 * i, struct.pack("<hhBBHHB", x, z, flag, 0, o75, o25, 0))
    uc.mem_write(G_PLIST, struct.pack("<Q", PLIST))


def run():
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, UNIT)
    uc.reg_write(UC_X86_REG_RDX, CTXA)
    uc.reg_write(UC_X86_REG_R8, OUT)
    uc.mem_write(OUT, struct.pack("<Q", 0x5555555555555555))
    state.update(bad=[], faults=[], rng=[])
    try:
        uc.emu_start(ENTRY, RET, count=3000000)
    except UcError as e:
        state["faults"].append(str(e))
    ok = uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]
    ret16 = uc.reg_read(UC_X86_REG_RAX) & 0xFFFF
    mask = struct.unpack("<I", bytes(uc.mem_read(LIVE + 4, 4)))[0]
    b512 = bytes(uc.mem_read(PAYLOAD + 0x14B4, 64))
    mt_match = all(d == mt.next() for d in state["rng"])            # every shipped draw checked against MT19937(5489)
    return {"ok": ok, "ret": ret16, "mask": mask, "flags512": [i for i in range(512) if (b512[i >> 3] >> (i & 7)) & 1],
            "draws": list(state["rng"]), "mt_match": mt_match, "stopped_at": (state["bad"] or state["faults"])[:1]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


def expect_outcome(draw, o75, o25):
    return o75 if draw % 100 < 75 else o25


# TP-1: the threshold is the f32 at 00901B34; a point at that distance fires, the next float above does not
nxt = struct.unpack("<f", struct.pack("<I", struct.unpack("<I", struct.pack("<f", IMG_THRESH))[0] + 1))[0]
tp1 = {}
for name, d in (("below", 1.25), ("at_f32_threshold", IMG_THRESH), ("next_f32_above", nxt), ("1.4", 1.4)):
    world([(0, 0, 0xFF, 0x211, 0x222)], unit_pos=(d, 0.0, 0.0))
    r = run()
    fired = r["ok"] and r["ret"] != 0xFFFF
    tp1[name] = {"distance": d, "fired": fired, "ok": r["ok"], "stopped_at": r["stopped_at"]}
tp1_ok = (IMG_THRESH == THRESH and tp1["below"]["fired"] and tp1["at_f32_threshold"]["fired"] and not tp1["next_f32_above"]["fired"]
          and not tp1["1.4"]["fired"] and all(v["ok"] for v in tp1.values()))
record("TP1_threshold", tp1_ok, constant=repr(IMG_THRESH), cases=tp1,
       note="fires at d <= the f32 nearest 1.3 (1.2999999523), not at the next float (1.3000000715)")

# TP-2: the point has no height: a unit 1.0 above a point 1.0 away horizontally is sqrt(2) away and does not fire
world([(10, 0, 0xFF, 0x211, 0x222)], unit_pos=(0.0, 1.0, 0.0))
r_hi = run()
world([(10, 0, 0xFF, 0x211, 0x222)], unit_pos=(0.0, 0.0, 0.0))
r_lo = run()
record("TP2_height_is_ignored", r_hi["ok"] and r_hi["ret"] != 0xFFFF and r_lo["ok"] and r_lo["ret"] != 0xFFFF,
       raised=r_hi, level=r_lo, note="CONTRADICTS TP-2: a unit 1.0 above a point 1.0 away still fires - 002F8150 zeroes the unit's "
       "height after 00265020 returns, so both heights are 0 and the distance is horizontal")

# TP-3 / TP-4: firing - the draw (independent MT19937), 75/25 outcome, the flag bit, one point only, its mask bit cleared
fires = []
for k in range(12):
    world([(0, 0, 40 + k, 0x200 + k, 0x300 + k), (5, 0, 0xFF, 0x999, 0x999)], unit_pos=(0.0, 0.0, 0.0), mask=0b11)
    r = run()
    want_draw = r["draws"][0] if r["draws"] else None
    fires.append({"ok": r["ok"], "ret": hex(r["ret"]), "draws": r["draws"], "mt": want_draw, "mt_match": r["mt_match"],
                  "want": hex(expect_outcome(want_draw, 0x200 + k, 0x300 + k)) if want_draw is not None else None, "mask": bin(r["mask"]), "flags512": r["flags512"],
                  "out": hex(struct.unpack("<Q", bytes(uc.mem_read(OUT, 8)))[0])})
tp3 = all(f["ok"] and len(f["draws"]) == 1 and f["mt_match"] and f["ret"] == f["want"] for f in fires)
tp4 = all(f["mask"] == "0b10" and f["flags512"] == [40 + k] for k, f in enumerate(fires))
record("TP3_75_25_from_the_draw", tp3, n=len(fires), note="each fire draws once; outcome +0x06 when draw % 100 < 75, else +0x08")
record("TP4_one_point_flag_and_bit", tp4, fires=fires,
       note="two points in range: only the first fires; its flag id is set in Bank512 (payload +0x14B4); its live bit is cleared")

# flag id 0xFF sets nothing
world([(0, 0, 0xFF, 0x277, 0x277)])
r = run()
record("TP4_flag_FF_sets_none", r["ok"] and r["flags512"] == [] and r["ret"] == 0x277, result=r, note="flag id 0xFF: no Bank512 bit")

# TP-5: 40 listed points, only index 35 in range, full mask: nothing fires (the walk stops at 32)
pts = [(300, 300, 0xFF, 1, 1)] * 40
pts[35] = (0, 0, 0xFF, 0x255, 0x255)
world(pts)
r35 = run()
pts[35], pts[31] = (300, 300, 0xFF, 1, 1), (0, 0, 0xFF, 0x266, 0x266)
world(pts)
r31 = run()
record("TP5_32_point_ceiling", r35["ok"] and r35["ret"] == 0xFFFF and r31["ok"] and r31["ret"] == 0x266, index35=r35, index31=r31,
       note="of 40 listed points, index 35 is unreachable; index 31 fires")

# TP-6: eligibility
elig = {}
for name, st in (("bit26", {0x3C: struct.pack("<I", 1 << 26)}), ("layer6C", {0x6C: b"\x20"}), ("layer7C", {0x7C: b"\x20"}),
                 ("sel5_is_1", {5: b"\x01"}), ("esper_band", {5: b"\x00", 4: b"\x1B"}), ("eligible", {5: b"\x00", 4: b"\x05"})):
    world([(0, 0, 0xFF, 0x244, 0x244)], stats=st)
    r = run()
    elig[name] = {"fired": r["ret"] != 0xFFFF, "ok": r["ok"]}
tp6 = all(v["ok"] for v in elig.values()) and [elig[k]["fired"] for k in ("bit26", "layer6C", "layer7C", "sel5_is_1", "esper_band", "eligible")] \
    == [False, False, False, False, False, True]
record("TP6_eligibility", tp6, cases=elig, note="status bit 26, either layer's 0x20, rec+5 == 1, or the 0x1B..0x27 band: no fire")

# not in the contract: a field absent from the live-mask table has no live points
world([(0, 0, 0xFF, 0x244, 0x244)], field_in_table=False)
r = run()
record("field_not_in_live_table", r["ok"] and r["ret"] == 0xFFFF, result=r,
       note="the active field has no row at 02EC3EA0: the live mask is 0 and nothing fires")

json.dump({"ok": allok, "allowed_functions": len(ALLOWED), "threshold_f32_at_00901B34": repr(IMG_THRESH), "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok", "allowed", len(ALLOWED))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
