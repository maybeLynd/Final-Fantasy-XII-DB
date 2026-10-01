"""S-36: execute CONTRACT-ui-request-router.md's router 00254B50, the post 002E1B10, the drain 002E09A0, the generic scheduler
00280A00 and the request-word setter 00252B40 as shipped code in the built world, and test R-a/R-b/R-c and R-1..R-6
(OPUS, 2026-09-25, block 327).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges; its world is built once. No application stub.
Two more idle singletons are planted as zeroed blocks, the same convention as the world's nine: the HUD object [0209BE80]
(read by 002904B0 inside the policy aggregate's 00360360) and [01F7FFE0] (00198790's object, flagged by a stop callback of the
prelude). STOP BOUNDARIES (the run ends there, arguments recorded, nothing substituted): 001DBA90, the audio call a stop
callback of some requests' prelude makes (the audio registry 01FD36A0 is the sound layer's lazily-built object, S-41's), and
002909F0, the first UI-internal call of the first widget's create message (the UI system's own init 00247AE0 does not build in
this world). Fixtures: the latch / request word 02092730..34 / 020927D8, the aggregate words 0215F1C0..0215F1FF, the mailbox
0215F1A0..A8 and the root's +0xB8 / +0xC0 slots behind [0209AC30].
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ROUTER, POST, DRAIN, SCHED, SETWORD, AGG, MOUNT = 0x254B50, 0x2E1B10, 0x2E09A0, 0x280A00, 0x252B40, 0x2E0FA0, 0x244F50
PROC1, PROC2 = 0x27FB70, 0x280140
STOPS = {0x1DBA90: "001DBA90 audio", 0x2909F0: "002909F0 widget internals"}
W.ALLOWED |= {0x16D6A0, PROC1, PROC2} | set(STOPS) | set().union(*(W.closure(f) for f in (ROUTER, POST, DRAIN, SCHED, SETWORD, PROC1, PROC2, MOUNT)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
WORD, LATCH, WORD_D8, AGG_WORDS, MAIL = 0x2092730, 0x2092734, 0x20927D8, 0x215F1C0, 0x215F1A0
ROOT = struct.unpack("<Q", bytes(uc.mem_read(0x209AC30, 8)))[0]

stop, seen = {}, []


def on_stop(u, a, n, _):
    stop["at"] = STOPS[a]
    u.emu_stop()


for a in STOPS:
    uc.hook_add(UC_HOOK_CODE, on_stop, begin=a, end=a)
for a, nm in ((AGG, "aggregate"), (SCHED, "scheduler"), (SETWORD, "set_word"), (MOUNT, "mount"), (PROC1, "proc_0027FB70"),
              (PROC2, "proc_00280140"), (ROUTER, "router")):
    def on(u, addr, n, _, nm=nm):
        seen.append((nm, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF))
    uc.hook_add(UC_HOOK_CODE, on, begin=a, end=a)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def reset(latch=0, agg=0, b8=0, c0=0):
    uc.mem_write(WORD, bytes(8))
    w(WORD_D8, "<I", 0)
    w(LATCH, "<I", latch)
    uc.mem_write(AGG_WORDS, bytes(0x40))
    w(AGG_WORDS, "<I", agg)
    w(ROOT + 0xB8, "<QQ", b8, c0)
    uc.mem_write(MAIL, bytes(0x10))


def call(fn, *args):
    stop.clear()
    del seen[:]
    ok = S.call(fn, *args)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def word():
    return list(r(WORD, "<II")) + [r(WORD_D8, "<I")[0]]


def names():
    return [s[0] for s in seen]


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- R-a: the latch refuses before the policy is read ----
reset(latch=1)
ok, v = call(ROUTER, 7, 0x11, 0)
record("Ra_latch_before_policy", ok and v == 0 and "aggregate" not in names() and word() == [0, 1, 0], returned=v, entered=names(),
       note="latch 02092734 = 1: the router returns 0 and never enters the policy aggregate 002E0FA0")

# ---- R-b: the policy - every aggregate bit against every id the 22-entry table at 01E0C2C0 gates ----
# the decision is read at the router's own branch after `bt r10d, ebx` (00254BC1): 00254BC7 = passed (the run ends there), 00254C40 = refused
table = [r(0x1E0C2C0 + 4 * i, "<I")[0] for i in range(22)]
decided = {}


def on_pass(u, a, n, _):
    if decided.get("armed"):
        decided["v"] = "passed"
        u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_pass, begin=0x254BC7, end=0x254BC7)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: decided.get("armed") and decided.setdefault("v", "refused"), begin=0x254C40, end=0x254C40)
gated = sorted({i for e in table for i in range(32) if e >> i & 1})
bad_b, refusals = [], 0
for b in range(22):
    for rid in gated + [7]:
        reset(agg=1 << b)
        decided.clear()
        decided["armed"] = True
        call(ROUTER, rid | 0x8000, 0, 0)
        want = "refused" if table[b] >> rid & 1 else "passed"
        refusals += want == "refused"
        if decided.get("v") != want:
            bad_b.append([b, rid, decided.get("v"), want])
record("Rb_policy_bit_table", not bad_b and refusals > 0, gated_ids=gated, table=["%X" % e for e in table], refusals_expected=refusals,
       mismatches=bad_b[:5], note="every aggregate bit alone x ids %s + 7 (bit 15 set): the router refuses exactly when that bit's "
                                  "01E0C2C0 entry holds the MASKED id's bit" % gated)
decided.clear()
reset()

# ---- R-c and R-3: a busy root refuses after dispatch and leaves the request word untouched ----
busy = {}
for label, b8, c0 in (("+0xB8 occupied", 0x1234, 0), ("+0xC0 occupied", 0, 0x1234)):
    reset(b8=b8, c0=c0)
    ok, v = call(ROUTER, 7, 0x11, 0)
    busy[label] = {"returned": v, "scheduler_entered": "scheduler" in names(), "set_word_entered": "set_word" in names(), "word": word()}
record("Rc_R3_busy_root_refuses_after_dispatch", all(x["returned"] == 0 and x["scheduler_entered"] and not x["set_word_entered"]
                                                     and x["word"] == [0, 0, 0] for x in busy.values()), cases=busy,
       note="an occupied root slot: the router passes the request to 00280A00, which returns 0 before 00252B40 - the word stays 0")

# ---- R-3 / R-6: an accepted generic request writes the word, then mounts the first widget with proc 0027FB70 ----
reset()
ok6, v6 = call(ROUTER, 0x8007, 0x11, 0)
order = names()
sched_args = [s for s in seen if s[0] == "scheduler"]
mount_args = [["%X" % s[1], "%X" % s[2]] for s in seen if s[0] == "mount"]
record("R3_R6_accepted_request", word() == [7, 1, 7] and order.index("set_word") < order.index("mount") and "proc_0027FB70" in order
       and mount_args[:1] == [["D8", "%X" % PROC1]] and stop.get("at") == "002909F0 widget internals" and sched_args
       and sched_args[0][1] == 0x8007, word=["%X" % x for x in word()], scheduler_request="%X" % sched_args[0][1], order=order,
       first_mount=mount_args[:1], stopped_at=stop.get("at"),
       note="request 0x8007: the scheduler receives the RAW dword (bit 15 kept); 00252B40 writes the MASKED id 7 to 02092730 and "
            "020927D8 and the latch 1, BEFORE the first mount; the first mount is a 0xD8 widget with proc 0027FB70, whose create "
            "message runs (the run ends at the widget's first UI-internal call)")
reset()

# requests whose prelude reaches the audio layer before any widget
aud = {}
for req in (2, 6, 7, 8, 15, 17):
    reset()
    ok, v = call(ROUTER, req, 0, 0)
    aud[req] = {"word": ["%X" % x for x in word()], "stopped_at": stop.get("at"), "mounted": "mount" in names()}
record("R6_prelude_audio_split", all(aud[q]["stopped_at"] == "001DBA90 audio" and not aud[q]["mounted"] for q in (2, 6, 15, 17))
       and all(aud[q]["stopped_at"] == "002909F0 widget internals" and aud[q]["mounted"] for q in (7, 8)), per_request=aud,
       note="the word is written for every accepted id; for 2, 6, 15, 17 the prelude's stop callbacks reach the audio layer before the "
            "first mount, for 7 and 8 the first widget mounts")

# ---- R-1: one mailbox slot, a second post replaces the first silently ----
reset()
p1 = call(POST, 7, 0x11)[1]
p2 = call(POST, 9, 0x22)[1]
mail = list(r(MAIL, "<BBHII"))
record("R1_single_slot_silent_replace", p1 == 1 and p2 == 1 and mail[0] == 1 and mail[3:] == [9, 0x22], posts=[p1, p2],
       mailbox={"pending": mail[0], "blocked": mail[1], "id": mail[3], "parameter": mail[4]},
       note="two posts before a drain both return 1; the slot holds only the second (id 9, parameter 0x22)")

# ---- R-2: the post's policy test covers id 2 only, and aggregate bit 0 only ----
r2 = {}
for label, agg, pid in (("id 2, bit 0", 1, 2), ("id 7, bit 0", 1, 7), ("id 2, bit 1", 2, 2)):
    reset(agg=agg)
    r2[label] = call(POST, pid, 0)[1]
reset(agg=1)
router_bit0_7 = call(ROUTER, 7, 0, 0)[1]
r2["router id 7, bit 0"] = router_bit0_7
record("R2_post_policy_narrower", r2["id 2, bit 0"] == 0 and r2["id 7, bit 0"] == 1 and r2["id 2, bit 1"] == 1, results=r2,
       note="the post refuses only id 2 under aggregate bit 0; id 7 posts under the same aggregate, and bit 1 does not stop id 2")

# blocked byte
reset()
w(MAIL + 1, "<B", 1)
blocked = call(POST, 7, 0)[1]
record("R1b_blocked_byte_refuses", blocked == 0 and r(MAIL, "<B")[0] == 0, returned=blocked,
       note="0215F1A1 non-zero: the post returns 0 and writes nothing")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
