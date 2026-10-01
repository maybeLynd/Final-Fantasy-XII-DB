"""S-42: execute CONTRACT-music-control-file-and-bgm-stream.md's bodies - the trampoline 0051EDB0, the rebase 003EAB90, the stream
checker 003EB0D0 and the stream machine 003EADE0 - as shipped code, and the reader 003EAA70 over the SHIPPED musicctrl.bin after
the shipped rebase; test MC-4..MC-8 (OPUS, 2026-09-25, block 325).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session with stack arguments from
block 323) supplies the image, the IAT traps and the named bridges; its world is built once. No application stub.
THE TABLE IS THE SHIPPED FILE: ps2data/image/ff12/in/common/musicctrl.bin (1,615 B, sha256 below) is copied raw (file-relative
page offsets, the state the loader's queued read leaves) to a block below 2 GB, [02B5E0D0] is pointed at it, and the rebase is
reached the way the queue's completion reaches it: through the trampoline 0051EDB0 with the descriptor's +8 word (0x003EAB90).
The progress operand the reader asks 00265270 for is planted (the u16 behind [02098E58], enabled by [02098E20] bit 0).
STOP BOUNDARIES (the run ends there and the arguments are recorded; nothing is substituted): the sound layer 002DF660,
002DEE90, 002DF680, 002DF630, 002DF690. The request queue (0032E400 sizes, 0032E780 / 0032E870 enqueue, 0032E4D0 in-flight)
runs as shipped after its own initialiser 0032EA90; the kind-0x24 size table behind [022C51F0 + 0x24*8] is a planted fixture
(the shipped build has no kind-0x24 files, and the size tables are loaded from FST files at boot).
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
MUSIC = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common\musicctrl.bin"
MUSIC_SHA = None                                        # filled below and recorded
TRAMP, REBASE, READER, CHECKER, MACHINE, QINIT, PLAY, READ = 0x51EDB0, 0x3EAB90, 0x3EAA70, 0x3EB0D0, 0x3EADE0, 0x32EA90, 0x3EB150, 0x3EB100
SETBUF = 0x3EB180
SOUND = {0x2DF660: "002DF660 open", 0x2DEE90: "002DEE90 poll", 0x2DF680: "002DF680 play", 0x2DF630: "002DF630 busy", 0x2DF690: "002DF690 close"}
W.ALLOWED |= {0x16D6A0, TRAMP} | set(SOUND) | set().union(*(W.closure(f) for f in (REBASE, READER, CHECKER, MACHINE, QINIT, PLAY, READ, SETBUF)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc

TABLE_CELL, STREAM, STORY_FLAG, STORY_PTR, SIZE_TABLES = 0x2B5E0D0, 0x2B5E0E0, 0x2098E20, 0x2098E58, 0x22C51F0
T, T2, STORY, SIZES, RING = 0x76100000, 0x76108000, 0x76110000, 0x76111000, 0x76120000
stop = {}


def on_stop(u, a, n, _):
    stop["at"] = SOUND[a]
    stop["args"] = [u.reg_read(r) & 0xFFFFFFFF for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8)]
    u.emu_stop()


for a in SOUND:
    uc.hook_add(UC_HOOK_CODE, on_stop, begin=a, end=a)
entered = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: entered.append(a), begin=REBASE, end=REBASE)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def run(fn, *args, stack=()):
    stop.clear()
    ok = S.call(fn, *args, stack=stack)
    return ok, uc.reg_read(UC_X86_REG_RAX)


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-36s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


raw = open(MUSIC, "rb").read()
MUSIC_SHA = hashlib.sha256(raw).hexdigest()
maxf = struct.unpack_from("<I", raw, 4)[0]
pages = (maxf + 0x7F) >> 7
offs = list(struct.unpack_from("<%dI" % pages, raw, 8))


def model(field, progress):
    """The page's decoding of the RAW file (independent of the image): field -> track or -1."""
    if field > maxf:
        return -1
    o = offs[field >> 7]
    if not o:
        return -1
    p = o
    while True:
        wd = raw[p] | raw[p + 1] << 8
        start, span, cnt = wd & 0x7FF, wd >> 11, raw[p + 2]
        if start > field:
            return -1
        if start + span >= field:
            break
        p += 4 + 3 * cnt
    track, e = raw[p + 3], p + 4
    pr = progress - 0x10000 if progress & 0x8000 else progress
    for _ in range(raw[p + 2]):
        if pr <= (raw[e] | raw[e + 1] << 8):
            break
        track = raw[e + 2]
        e += 3
    return -1 if track == 0 else track


# ---- MC-4 + MC-5: the trampoline reaches the rebase, which rebases the shipped file in place ----
uc.mem_write(T, raw)
w(TABLE_CELL, "<Q", T)
del entered[:]
ok45, _ = run(TRAMP, REBASE)
after = list(r(T + 8, "<%dI" % pages))
record("MC4_MC5_trampoline_then_rebase", ok45 and entered == [REBASE] and after == [o + T for o in offs] and bytes(uc.mem_read(T + 8 + 4 * pages, 32)) == raw[8 + 4 * pages:8 + 4 * pages + 32],
       max_field=maxf, pages=pages, offsets_before=offs, offsets_after=["%08X" % v for v in after],
       note="0051EDB0 with the descriptor's +8 word 0x003EAB90 jumps to the rebase; the %d page words (max field %d) become the block "
            "address + offset, and the bytes after the header are untouched" % (pages, maxf))

# the reader over the rebased shipped file, every field, five progress values
uc.mem_write(STORY, bytes(0x10))
w(STORY_FLAG, "<B", 1)
w(STORY_PTR, "<Q", STORY)
mism, tally = [], {}
for prog in (0, 100, 1580, 5000, 0x8000):
    w(STORY, "<H", prog)
    for f in range(0, maxf + 3):
        ok, v = run(READER, f)
        v = v & 0xFFFFFFFF
        v = v - (1 << 32) if v & 0x80000000 else v
        if not ok or v != model(f, prog):
            mism.append([prog, f, v, model(f, prog)])
        tally.setdefault(prog, {"tracks": 0, "none": 0})["tracks" if v != -1 else "none"] += 1
record("reader_over_rebased_shipped_file", not mism, per_progress=tally, mismatches=mism[:5],
       note="003EAA70 over the file the shipped rebase produced agrees with an independent decode of the raw file for every field "
            "0..%d (+2 past the max) at progress 0, 100, 1580, 5000 and 0x8000" % maxf)

# ---- MC-5: zero stays zero; a second run adds the base again (32-bit) ----
z = bytearray(raw)
struct.pack_into("<I", z, 8 + 4 * 3, 0)
uc.mem_write(T2, bytes(z))
w(TABLE_CELL, "<Q", T2)
run(REBASE)
p3 = r(T2 + 8 + 12, "<I")[0]
w(STORY, "<H", 1580)
f3 = 3 * 128 + 5
ok3, v3 = run(READER, f3)
w(TABLE_CELL, "<Q", T)
run(REBASE)
twice = list(r(T + 8, "<%dI" % pages))
record("MC5_zero_stays_zero_twice_doubles", p3 == 0 and ok3 and v3 & 0xFFFFFFFF == 0xFFFFFFFF and twice == [(o + 2 * T) & 0xFFFFFFFF for o in offs],
       page3_after=p3, reader_on_page3=-1 if v3 & 0xFFFFFFFF == 0xFFFFFFFF else v3, second_run=["%08X" % v for v in twice[:3]],
       note="a zero page word stays 0 and the reader answers -1 for a field on that page; running the rebase again adds the block address "
            "a second time (32-bit wrap)")
uc.mem_write(T, raw)
run(REBASE)

# ---- MC-5: the block must sit below 2 GB for the reader, and below 4 GB for the 32-bit add ----
HI2, HI4 = 0x90000000, 0x200100000
for a in (HI2, HI4):
    uc.mem_map(a, 0x1000)
res = {}
for a in (HI2, HI4):
    uc.mem_write(a, raw)
    w(TABLE_CELL, "<Q", a)
    run(REBASE)
    stored = r(a + 8, "<I")[0]
    okr, v = run(READER, 5)
    res["%X" % a] = {"page0_stored": "%08X" % stored, "reader_returned": okr, "fault": (S.st["faults"] or [None])[0]}
w(TABLE_CELL, "<Q", T)
record("MC5_address_limits", res["90000000"]["page0_stored"] == "%08X" % (HI2 + offs[0]) and not res["90000000"]["reader_returned"]
       and res["200100000"]["page0_stored"] == "%08X" % ((HI4 + offs[0]) & 0xFFFFFFFF) and not res["200100000"]["reader_returned"],
       blocks=res, note="at 0x90000000 the rebase stores 0x9000xxxx and the reader's movsxd sign-extends it to 0xFFFFFFFF9000xxxx and "
                        "faults; at 0x200100000 the 32-bit add keeps only the low half (0x0010xxxx) and the reader faults there")

# ---- MC-4: a callback word >= 0x80000000 is sign-extended into a non-canonical target ----
okn, _ = run(TRAMP, 0x80001000)
record("MC4_sign_extended_target", not okn and bool(S.st["faults"]), fault=(S.st["faults"] or [None])[0],
       note="0051EDB0 with 0x80001000 jumps to 0xFFFFFFFF80001000: the word is a sign-extended 32-bit pointer")

# ---- MC-6: one stream - the checker's loop is bounded to one 0x38-byte slot ----
uc.mem_write(STREAM, bytes(0x70))
w(STREAM + 0x31, "<B", 1)
_, c1 = run(CHECKER)
w(STREAM + 0x31, "<B", 0)
w(STREAM + 0x38 + 0x31, "<B", 1)
_, c2 = run(CHECKER)
w(STREAM + 0x38 + 0x31, "<B", 0)
record("MC6_checker_bounded_to_one", c1 & 0xFF == 1 and c2 & 0xFF == 0, first_active=c1 & 0xFF, second_slot_active=c2 & 0xFF,
       note="active at 02B5E0E0+0x31 -> 1; an active byte in a second 0x38 slot is never reached -> 0")

# ---- MC-7 / MC-8: the stream machine, queue initialised by its own initialiser ----
okq, _ = run(QINIT)
init = {"requestId": r(STREAM, "<i")[0], "pan_vol": list(r(STREAM + 0x32, "<BB")), "kind": r(STREAM + 0x1C, "<i")[0]}
uc.mem_write(SIZES, bytes(0x1000))
w(SIZE_TABLES + 0x24 * 8, "<Q", SIZES)
w(SIZES + 4 * 3, "<I", 0x12345)                        # kind 0x24 index 3: smaller than the ring
w(SIZES + 4 * 4, "<I", 0x45000)                        # kind 0x24 index 4: larger than the ring


def state():
    v = r(STREAM, "<iIQiiiiiiiiBB")                     # +0 requestId, +8 buffer, +0x10 bufferBytes ... +0x30 state, +0x31 active
    return {"requestId": v[0], "bufferBytes": v[3], "fileBytes": v[8], "bytesRead": v[9], "ringCursor": v[10], "state": v[11], "active": v[12]}


def stream_read(index, ring):
    run(SETBUF, RING, ring)
    run(READ, index)
    return run(MACHINE, STREAM)


# state 1 with a file smaller than the ring: the ring is clamped, the whole file is submitted
okA, tickA = stream_read(3, 0x30000)
sA = state()
# state 2 waits while the request is in flight
okA2, tickA2 = run(MACHINE, STREAM)
sA2 = state()
# state 1 with a larger file: the ring stays
okB, tickB = stream_read(4, 0x30000)
sB = state()
mc7a = (okq and okA and tickA & 0xFF == 1 and sA["fileBytes"] == 0x12345 and sA["bufferBytes"] == 0x12345 and sA["bytesRead"] == 0x12345
        and sA["ringCursor"] == 0 and sA["state"] == 2 and sA["requestId"] > 0 and okA2 and tickA2 & 0xFF == 0 and sA2["state"] == 2
        and okB and sB["bufferBytes"] == 0x30000 and sB["fileBytes"] == 0x45000 and sB["bytesRead"] == 0x30000)
record("MC7_ring_clamped_to_file", mc7a, init=init, small_file=sA, still_in_flight=sA2, large_file=sB,
       note="file 0x12345 under a 0x30000 ring: the ring becomes 0x12345 (0032E400 returns the table entry as is - only its fallback "
            "path rounds to 64) and the first read is the whole file; a 0x45000 file keeps the 0x30000 ring and reads 0x30000 first; state 2 waits while 0032E4D0 reports the read in flight")

# state 7: the next piece is min(0x10000, ring - cursor, file - read); cursor = read mod ring
pieces = []
w(STREAM + 0x30, "<B", 7)
for _ in range(3):
    b = state()
    okp, _ = run(MACHINE, STREAM)
    a = state()
    pieces.append({"read_before": "%X" % b["bytesRead"], "read_after": "%X" % a["bytesRead"], "cursor_after": "%X" % a["ringCursor"],
                   "state": a["state"], "stopped_at": stop.get("at")})
    w(STREAM + 0x30, "<B", 7)
want = [{"read_before": "30000", "read_after": "40000", "cursor_after": "10000", "state": 8, "stopped_at": None},
        {"read_before": "40000", "read_after": "45000", "cursor_after": "15000", "state": 8, "stopped_at": None},
        {"read_before": "45000", "read_after": "45000", "cursor_after": "15000", "state": 7, "stopped_at": "002DF630 busy"}]
record("MC7_pieces_and_ring_cursor", pieces == want, pieces=pieces,
       note="0x45000 file, 0x30000 ring: 0x10000 (the 002DF600 piece), then 0x5000 (what is left of the file); the cursor is bytesRead "
            "mod ring; with everything read the machine asks the sound layer whether the stream is still busy")

# state 6: play hands 0x40 / 0x7F to the sound layer
w(STREAM + 0x30, "<B", 5)
w(STREAM + 0x18, "<i", 0x77)
okp5, _ = run(PLAY)
st6 = state()["state"]
run(MACHINE, STREAM)
record("MC8_play_pair", okp5 and st6 == 6 and stop.get("at") == "002DF680 play" and stop["args"] == [0x77, 0x40, 0x7F], play_state=st6,
       sound_call=stop, note="bgmstreamplay moves state 5 to 6; the next tick calls 002DF680(streamId, 0x40, 0x7F) from the descriptor's "
                             "+0x32 / +0x33 (initialised by 003EB050)")

json.dump({"ok": allok, "musicctrl_sha256": MUSIC_SHA, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
