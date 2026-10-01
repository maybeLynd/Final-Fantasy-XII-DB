"""TA-1 (OPUS, 2026-09-25): the clock behind the texture-animation frame that 002F4520 reads at [[entry+0x50]+0x90].

Static chain under test (each link is an instruction in the shipping image):
  - 002F57A3..002F57CE (the per-frame map pass 002F5550) stores into runtime entry +0x50 the tag-23 slot record that
    00466CB0 matches (a 0x130-byte record of the 02EBB6E0 slot family built by 00466E70);
  - 004677A0 walks every slot's tracks and calls 00466420(record, channel, &track+0xC); channel 9 is the jump-table arm
    00466488 `mov [rcx+0x90], r8`, so record+0x90 points at a TRACK's sampled float;
  - 004678E0(dt): for every active slot (+0x4C bit 0) delta +0x48 += dt * rate +0x38;
  - 004668C0: time +0x44 += delta; loop (+0x4C bit 1, span +0x40 - +0x3C >= 1.0) wraps once by the span, otherwise the
    time clamps to [+0x3C, +0x40] and bit 2 (finished) is set; then every track is sampled (00466240).
Evidence class: NATIVE-REPLAY (unicorn), live_game false, world.py Session, no application stub. Input: the shipped
tag-23 chunk of dst0101.mpk's YM00 section, read from the extracted game data (sha256 recorded). The chunk is placed
below 4 GiB; the shipped setters 00467620 (active), 00467700 (rate), 004676C0 (loop) drive the state.
"""
import hashlib
import json
import os
import struct
import sys

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
MPK = r"D:/FFXII_TZA_extract/ps2data/plan_master/map_ctrl/dst01/dst0101/bin/dst0101.mpk"
BUILD, BIND, ACCUM, ADVANCE = 0x466E70, 0x4677A0, 0x4678E0, 0x4668C0
SET_ACTIVE, SET_RATE, SET_LOOP = 0x467620, 0x467700, 0x4676C0
for f in (BUILD, BIND, ACCUM, ADVANCE):
    W.ALLOWED |= W.closure(f)
W.ALLOWED |= {SET_ACTIVE, SET_RATE, SET_LOOP} | W.closure(0x217150)   # 00217150: matrix multiply behind 00202D70 (thunk tail jmp)
BLOCK, ARENA = 0x36D240, 0x369D30          # boot's arena creation, 0022A309..0022A321 for arena 6
W.ALLOWED |= W.closure(BLOCK) | W.closure(ARENA)


def mpk_slot(d, s):                     # the map-ctrl container walk of gen_ym00_census.py (slot 8 = YM00)
    cnt = struct.unpack_from("<I", d, 0)[0]
    sz = struct.unpack_from("<32I", d, 4)
    off = ((cnt + 1) * 4 + 0x3F) & ~0x3F
    for i in range(32):
        if sz[i]:
            off += 0x40
            if i == s:
                return d[off:off + sz[i]]
            off += sz[i]


raw = open(MPK, "rb").read()
ym = mpk_slot(raw, 8)
n = struct.unpack_from("<I", ym, 0x10)[0]
ents = [struct.unpack_from("<I", ym, 0x14 + 4 * i)[0] for i in range(n + 1)]
chunk = None
for i, e in enumerate(ents[:-1]):
    if e >> 24 == 23:
        chunk = ym[0x10 + (e & 0xFFFFFF) * 16: 0x10 + (ents[i + 1] & 0xFFFFFF) * 16]
assert chunk is not None

S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
# World state by shipped code: register arena 6 the way the boot frame 0022A0B0 does (0022A219: 0036D240(0x6C00400);
# 0022A309..0022A321: 00369D30(6, block, 0x6C00000, 0x400)) so the tag-23 builder's 003EC8D0(6, ...) allocations are
# served. DECLARED DEVIATION: capacity 4 MiB (block 0x400400, size 0x400000) instead of boot's 108 MiB, because the
# harness heap is 16 MiB; the granularity argument 0x400 is boot's. Capacity only - the builder allocates < 16 KiB.
from unicorn.x86_const import UC_X86_REG_RAX
arena_mask_before = struct.unpack("<I", bytes(uc.mem_read(0x22D89B8, 4)))[0]
okBlk = S.call(BLOCK, 0x400400)
blk = uc.reg_read(UC_X86_REG_RAX)
okAr = S.call(ARENA, 6, blk, 0x400000, 0x400)
arena_mask_after = struct.unpack("<I", bytes(uc.mem_read(0x22D89B8, 4)))[0]
CH = 0x76280000
uc.mem_write(CH, chunk + bytes(0x100))
rd = lambda a, f, n: struct.unpack(f, bytes(uc.mem_read(a, n)))[0]
q = lambda a: rd(a, "<Q", 8)
dw = lambda a: rd(a, "<I", 4)
fl = lambda a: rd(a, "<f", 4)
w16 = lambda a: rd(a, "<h", 2)

okB = S.call(BUILD, CH)
count, table = dw(0x2EBB6E0), q(0x2EBB6F0)
if not okB:
    sys.exit(1)


def slot(i):
    s = table + i * 0x50
    return {"authored": "%X" % q(s + 8), "tracks": w16(s + 0x30), "records": w16(s + 0x32), "rate+38": fl(s + 0x38),
            "start+3C": fl(s + 0x3C), "end+40": fl(s + 0x40), "time+44": fl(s + 0x44), "flags+4C": "%X" % dw(s + 0x4C)}


built = [slot(i) for i in range(count)]
okBind = S.call(BIND)
# every (slot, track) whose authored channel is 9, and whether its record's +0x90 now points at the track's +0xC
ch9 = []
for i in range(count):
    s = table + i * 0x50
    if not q(s + 8):
        continue
    tr, recs = q(s + 0x20), q(s + 0x28)
    for t in range(w16(s + 0x30)):
        te = tr + t * 0x18
        auth = q(te)
        chan, recidx = dw(auth + 4), rd(auth + 0xC, "<i", 4)
        if chan == 9 and 0 <= recidx < w16(s + 0x32):
            rec = recs + recidx * 0x130
            ch9.append({"slot": i, "track": t, "record": recidx, "+0x90 points at track+0xC": q(rec + 0x90) == te + 0xC,
                        "track entry": te, "record addr": rec})
res = {"arena6": {"block_ok": okBlk, "create_ok": okAr, "mask_before": "%X" % arena_mask_before, "mask_after": "%X" % arena_mask_after},
       "mpk": os.path.basename(MPK), "chunk_sha256": hashlib.sha256(chunk).hexdigest(), "chunk_bytes": len(chunk),
       "build_returned": okB, "slot_count": count, "slots_after_build": built, "bind_returned": okBind,
       "channel9_bindings": [{k: v for k, v in c.items() if k not in ("track entry", "record addr")} for c in ch9]}

# drive one channel-9 slot through the clock: active, rate 1.0, loop on / off, dt = 1.0 per call
runs = {}
if ch9:
    c = ch9[0]
    si, te = c["slot"], c["track entry"]
    sb = table + si * 0x50
    for label, loop in (("loop on", 1), ("loop off", 0)):
        uc.mem_write(sb + 0x44, struct.pack("<f", fl(sb + 0x3C)))          # start of range (state, not code)
        S.call(SET_ACTIVE, si, 1); S.call(SET_LOOP, si, loop)
        S.call(SET_RATE, si, 0, xmm={1: 1.0})
        span = fl(sb + 0x40) - fl(sb + 0x3C)
        seq = []
        for k in range(int(span) + 6):
            a = S.call(ACCUM, xmm={0: 1.0}); b = S.call(ADVANCE)
            seq.append({"ok": a and b, "time": round(fl(sb + 0x44), 4), "delta+48": fl(sb + 0x48),
                        "flags": "%X" % dw(sb + 0x4C), "value@track+0xC": round(fl(te + 0xC), 4)})
        runs[label] = {"slot": si, "range": [fl(sb + 0x3C), fl(sb + 0x40)], "frames": seq}
    # rate 2.0, loop on: two time units per call
    uc.mem_write(sb + 0x44, struct.pack("<f", fl(sb + 0x3C)))
    S.call(SET_LOOP, si, 1); S.call(SET_RATE, si, 0, xmm={1: 2.0})
    seq = []
    for k in range(4):
        S.call(ACCUM, xmm={0: 1.0}); S.call(ADVANCE)
        seq.append(round(fl(sb + 0x44), 4))
    runs["rate 2.0"] = seq
res["clock_runs"] = runs
on, off = runs["loop on"]["frames"], runs["loop off"]["frames"]
end = runs["loop on"]["range"][1]
t_on, v_on = [f["time"] for f in on], [f["value@track+0xC"] for f in on]
t_off, v_off = [f["time"] for f in off], [f["value@track+0xC"] for f in off]
checks = {
    "build and bind return": okB and okBind,
    "every channel-9 record +0x90 points at its track +0xC": bool(ch9) and all(c["+0x90 points at track+0xC"] for c in ch9),
    "loop on: slot time wraps once by the span at the end": t_on[:int(end) - 1] == [float(i) for i in range(1, int(end))]
        and t_on[int(end) - 1] == 0.0 and all(f["flags"] == "13" for f in on),
    "loop on: the channel-9 value cycles (falls back while time rises)": any(v_on[i + 1] < v_on[i] and t_on[i + 1] > t_on[i] for i in range(len(v_on) - 1)),
    "loop off: slot time clamps at the end and sets bit 2": t_off[-3:] == [end] * 3 and off[-1]["flags"] == "15",
    "loop off: the channel-9 value holds": len(set(v_off[-10:])) == 1,
    "rate 2.0 doubles the step": runs["rate 2.0"] == [2.0, 4.0, 6.0, 8.0],
}
res["checks"] = checks
res["ok"] = all(checks.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
print("ok" if res["ok"] else "NOT ok", json.dumps(res["checks"]))
print(json.dumps({k: res[k] for k in ("build_returned", "slot_count", "bind_returned")}), len(ch9), "channel-9 bindings")
print(json.dumps(res["channel9_bindings"][:6]))
for k, v in runs.items():
    print(k, json.dumps(v)[:900])
