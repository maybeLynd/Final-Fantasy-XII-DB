"""S-18: execute BattleLocomotion_ApplyHeadingTurnLimiter (003364D0), CONTRACT-battle-locomotion-turn-limiter.md's one
entry, as shipped code and test BL-1..BL-6 and the section-14 committed-direction latch as PROPERTIES of each call and of
multi-call histories (OPUS, 2026-09-25, block 307).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NOTHING substituted: the body
calls only its angle-wrap leaf 0033CB70 (real) and no import; entering any other function fails the case.
Fixtures (planted data only): ctx +0x100 -> flag block (+0x21 direction pair, +0x38 bit 3 turning, +0x3C bit 0 fast
latch), ctx +0x108 -> motion state (+0xE0 current heading, +0xEC slow rate, +0xF0 fast rate, +0x170 locomotion flags).
The properties are stated from the contract, not transcribed from the body: the error is the shortest signed angle
(desired - current) computed here in double precision, and every case keeps |error| at least 0.5 degree away from the
20 / 45 / 120 degree thresholds and from 180 degrees, so the property's own rounding cannot decide a case.
Writes result.json next to this file.
"""
import hashlib
import json
import math
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RIP, UC_X86_REG_XMM0, UC_X86_REG_XMM1

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD = 0x70000000, 0x100000, 0x71000000, 0x72000000
CTX, FL, ST = WORLD, WORLD + 0x1000, WORLD + 0x2000
LIM = 0x3364D0
ALLOWED = {LIM, 0x33CB70}
D = math.pi / 180


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def bits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")

uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x4000)
uc.mem_write(RET, bytes([0xF4]))
state = {"bad": [], "faults": []}


def on_code(u, a, n, _):
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)

# the three constants the contract names (BL-1), read from the image at the compare operands
CONST = {}
for name, va in (("45", 0x915614), ("120", 0x915FE0), ("20", 0xD10AD8)):
    CONST[name] = struct.unpack("<f", bytes(uc.mem_read(va, 4)))[0]


def setup(cur, slow, fast, flags170, fl21, fl38, fl3c):
    uc.mem_write(WORLD, bytes(0x4000))
    uc.mem_write(CTX + 0x100, struct.pack("<Q", FL))
    uc.mem_write(CTX + 0x108, struct.pack("<Q", ST))
    uc.mem_write(ST + 0xE0, struct.pack("<f", cur))
    uc.mem_write(ST + 0xEC, struct.pack("<ff", slow, fast))
    uc.mem_write(ST + 0x170, struct.pack("<I", flags170))
    uc.mem_write(FL + 0x21, bytes([fl21]))
    uc.mem_write(FL + 0x38, struct.pack("<II", fl38, fl3c))


def flags():
    return uc.mem_read(FL + 0x21, 1)[0], struct.unpack("<I", bytes(uc.mem_read(FL + 0x38, 4)))[0], \
        struct.unpack("<I", bytes(uc.mem_read(FL + 0x3C, 4)))[0]


def limit(desired):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, CTX)
    uc.reg_write(UC_X86_REG_XMM1, bits(desired))
    state["bad"], state["faults"] = [], []
    try:
        uc.emu_start(LIM, RET, count=200000)
    except UcError as e:
        state["faults"].append(str(e))
    ok = uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]
    return struct.unpack("<f", struct.pack("<I", uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0], ok


def sdiff(a, b):
    """shortest signed angle a - b, in (-pi, pi]"""
    d = math.fmod(a - b, 2 * math.pi)
    if d > math.pi:
        d -= 2 * math.pi
    if d <= -math.pi:
        d += 2 * math.pi
    return d


def far(deg):
    return all(abs(abs(deg) - t) >= 0.5 for t in (20, 45, 120, 180))


# ---------------- 1. single-call property grid ----------------
viol, n = {k: [] for k in ("returned", "BL1_BL2_entry", "BL2_idle_unchanged", "BL3_latch", "BL4_band_keeps", "release_below_20",
                            "rate_and_direction", "S14_committed_direction", "BL5_pair", "BL6_snap")}, 0
exercised = {k: 0 for k in ("idle", "turning", "snap", "committed_direction", "rate_step", "latch_set_by_BL3",
                             "latch_blocked_by_BL3", "band_kept_latch_1", "release_below_20_from_1")}
curs = [-2.9, -1.0, 0.0, 0.4, 2.5]
deltas = [5, 15, 30, 44, 46, 60, 100, 119, 121, 150, 175]
for cur in curs:
    for dd in deltas:
        for sign in (1, -1):
            desired = f32(cur + sign * dd * D)
            err = sdiff(desired, f32(cur))
            if not far(err / D):
                continue
            for fl38 in (0, 8):
                for fl3c in (0, 1):
                    for fl21 in (0x00, 0x02, 0x04, 0x81, 0x83, 0x85):
                        for f170 in (0x00, 0x0C, 0x1C, 0xFF):
                            for slow, fast in ((0.05, 0.2), (1.2, 2.5)):
                                cur32 = f32(cur)
                                setup(cur32, slow, fast, f170, fl21, fl38, fl3c)
                                res, ok = limit(desired)
                                n += 1
                                a21, a38, a3c = flags()
                                key = [cur, dd * sign, fl38, fl3c, fl21, f170, slow]
                                if not ok:
                                    viol["returned"].append(key)
                                    continue
                                e = abs(err) / D
                                turning = bool(fl38 & 8) or e > 45
                                exercised["turning" if turning else "idle"] += 1
                                if not turning:
                                    # BL-2: flag clear and error <= 45 -> the current heading, nothing written
                                    if bits(res) != bits(cur32) or (a21, a38, a3c) != (fl21, fl38, fl3c):
                                        viol["BL2_idle_unchanged"].append(key + [res])
                                    continue
                                # BL-1: > 45 raises bit 3 (unless the same call arrives and clears it)
                                snapped = bits(res) == bits(desired)
                                if not snapped and not (a38 & 8):
                                    viol["BL1_BL2_entry"].append(key)
                                # expected latch after the band logic
                                if e > 120:
                                    latch = (fl3c & 1) | (1 if (f170 & 0x1C) == 0x1C else 0)
                                elif e > 20:
                                    latch = fl3c & 1
                                else:
                                    latch = 0
                                rate = f32(fast if latch else slow)
                                if e > 120 and not (fl3c & 1):
                                    exercised["latch_set_by_BL3" if latch else "latch_blocked_by_BL3"] += 1
                                if 20 < e <= 120 and fl3c & 1:
                                    exercised["band_kept_latch_1"] += 1
                                if e <= 20 and fl3c & 1:
                                    exercised["release_below_20_from_1"] += 1
                                if snapped:
                                    if a38 & 8 or a3c & 1:
                                        viol["BL6_snap"].append(key + ["flags not cleared"])
                                else:
                                    if (a3c & 1) != latch:
                                        viol["BL3_latch" if e > 120 else ("BL4_band_keeps" if e > 20 else "release_below_20")].append(key + [a3c])
                                step = sdiff(res, cur32)
                                pair = fl21 & 6
                                if e > 120 and pair in (2, 4):
                                    # section 14: a committed direction is continued, +rate for pair 2, -rate for pair 4
                                    exercised["committed_direction"] += 1
                                    want = f32(cur32 + rate) if pair == 2 else f32(cur32 - rate)
                                    if bits(res) != bits(want):
                                        viol["S14_committed_direction"].append(key + [res, want])
                                elif abs(err) <= rate + 1e-6:
                                    exercised["snap"] += 1
                                    if not snapped:                      # BL-6: within the rate -> exactly desired
                                        viol["BL6_snap"].append(key + [res, desired])
                                else:
                                    exercised["rate_step"] += 1
                                    if abs(abs(step) - rate) > 1e-5 or (step > 0) != (err > 0):
                                        viol["rate_and_direction"].append(key + [res, step, rate, err])
                                # BL-5: exactly one of bits 1 / 2, matching the sign of the step; other bits kept
                                wantpair = 2 if sdiff(res, cur32) > 0 else 4
                                if (a21 & 6) != wantpair or (a21 & ~6 & 0xFF) != (fl21 & ~6 & 0xFF):
                                    viol["BL5_pair"].append(key + [a21, wantpair])
grid_ok = all(not v for v in viol.values()) and all(exercised.values())
results = {"constants_read": {k: v for k, v in CONST.items()},
           "single_call_grid": {"pass_": grid_ok, "n": n, "violations": {k: v[:8] for k, v in viol.items()},
                                "violation_counts": {k: len(v) for k, v in viol.items()}, "branches_exercised": exercised}}
print("constants", CONST)
print("single_call_grid  %s  n=%d  %s  exercised=%s" % ("PASS" if grid_ok else "FAIL", n, {k: len(v) for k, v in viol.items() if v}, exercised))


# ---------------- 2. histories ----------------
def run(cur, desired, steps, slow=0.1, fast=0.3, f170=0, fl38=0, fl3c=0, fl21=0):
    setup(f32(cur), slow, fast, f170, fl21, fl38, fl3c)
    trace = []
    for _ in range(steps):
        before = struct.unpack("<f", bytes(uc.mem_read(ST + 0xE0, 4)))[0]
        res, ok = limit(f32(desired))
        a21, a38, a3c = flags()
        trace.append({"heading": before, "result": res, "err_deg": round(sdiff(f32(desired), before) / D, 3),
                      "turning": bool(a38 & 8), "latch": a3c & 1, "pair": a21 & 6, "ok": ok})
        uc.mem_write(ST + 0xE0, struct.pack("<f", res))                  # the caller commits the limited heading
        if bits(res) == bits(f32(desired)) and not (a38 & 8):
            break
    return trace


# BL-2 hysteresis: 50 degrees off turns and keeps turning through 40; a fresh 40-degrees-off actor never turns
h1 = run(0.0, 50 * D, 40)
h1_ok = h1[0]["turning"] and any(t["turning"] and 20 < abs(t["err_deg"]) < 45 for t in h1) and bits(h1[-1]["result"]) == bits(f32(50 * D))
h2 = run(0.0, 40 * D, 5)
h2_ok = all(not t["turning"] and bits(t["result"]) == bits(f32(0.0)) for t in h2)
# BL-4 path dependence: from 150 degrees with the three locomotion bits the latch sets and is KEPT through 60 degrees;
# a fresh turning actor at 60 degrees with the latch clear steps at the slow rate
h3 = run(0.0, 150 * D, 60, f170=0x1C)
at60 = [t for t in h3 if 50 < abs(t["err_deg"]) < 70]
h3_ok = bool(at60) and all(t["latch"] == 1 for t in at60) and any(t["latch"] == 0 and abs(t["err_deg"]) <= 20 for t in h3)
h4 = run(0.0, 60 * D, 1, fl38=8)
h4_ok = abs(abs(sdiff(h4[0]["result"], 0.0)) - f32(0.1)) < 1e-6 and h4[0]["latch"] == 0
# BL-6: arrival snaps and ends the loop - the history terminates with result == desired and both flags clear
h5_ok = all(bits(h[-1]["result"]) == bits(f32(d)) and not h[-1]["turning"] and h[-1]["latch"] == 0
            for h, d in ((h1, 50 * D), (h3, 150 * D)))
all_ok = all(t["ok"] for h in (h1, h2, h3, h4) for t in h)
hist_ok = h1_ok and h2_ok and h3_ok and h4_ok and h5_ok and all_ok
results["histories"] = {"pass_": hist_ok, "BL2_hysteresis_50_through_40": h1_ok, "BL2_fresh_40_never_turns": h2_ok,
                        "BL4_latch_kept_through_60": h3_ok, "BL4_fresh_60_slow": h4_ok, "BL6_snap_ends_loop": h5_ok,
                        "all_returned": all_ok, "trace_50": h1, "trace_150_fast": h3}
print("histories         %s  %s" % ("PASS" if hist_ok else "FAIL", {k: results["histories"][k] for k in
                                                                      ("BL2_hysteresis_50_through_40", "BL2_fresh_40_never_turns", "BL4_latch_kept_through_60", "BL4_fresh_60_slow", "BL6_snap_ends_loop")}))

ok = grid_ok and hist_ok
json.dump({"pass": int(grid_ok) + int(hist_ok), "total": 2, "ok": ok, "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
print("%d/2 pass" % (int(grid_ok) + int(hist_ok)))
