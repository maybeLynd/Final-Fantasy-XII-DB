"""S-08: execute the four invariants of CONTRACT-resource-request-queue.md that stand as STATIC in its owner verdicts - I1 (the
constructor's field list over a dirty pool), I4's counter wrap and signed compare, I6 (offset truncation toward zero) and I7
(recycling does not sanitize) - on the shipped constructor 0032E450, requester 0032E870 and recycler 0032EC40 (OPUS,
2026-09-25, block 330).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session with stack arguments)
supplies the image, the IAT traps and the named bridges; its world is built once. No application stub and no stop boundary:
no case lets the free list run dry, so the requester never enters its pump / pacer stall (I3 is replay-confirmed elsewhere).
Fixtures: the pool bytes before construction (two dirty patterns), the counter 01EED498 where a case sets it, and the request
descriptors.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
CTOR, REQ, RECYCLE, PUMP = 0x32E450, 0x32E870, 0x32EC40, 0x32E070
POOL, COUNTER, FREE = 0x22C31C0, 0x1EED498, 0x22C51D0
W.ALLOWED |= {0x16D6A0} | set().union(*(W.closure(f) for f in (CTOR, REQ, RECYCLE)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
DESC, DEST = 0x76300000, 0x76310000
pumped = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: pumped.append(1), begin=PUMP, end=PUMP)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def run(fn, *args, stack=()):
    ok = S.call(fn, *args, stack=stack)
    assert ok, (hex(fn), (S.st["bad"] or S.st["faults"])[:2])
    return uc.reg_read(UC_X86_REG_RAX)


def slot_of(rid):
    return POOL + (rid & 0x3F) * 0x80


def request(offset, kind=0x24, index=3, nbytes=0x1000, arg=0x55, cb=0x1111, cancel=0x2222):
    w(DESC, "<iIIIQQ", offset, 0, arg, 0, cb, cancel)      # {+0 offset, +8 argument, +0x10 completion, +0x18 cancellation}
    return run(REQ, kind, index, DEST, nbytes, stack=(DESC, 0)) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- I1: the constructor over a dirty pool writes exactly the listed fields ----
changed = set()
for fill in (0xAA, 0x55):
    uc.mem_write(POOL, bytes([fill]) * 0x2000)
    run(CTOR)
    after = bytes(uc.mem_read(POOL, 0x2000))
    for s in range(64):
        for o in range(0x80):
            if after[s * 0x80 + o] != fill:
                changed.add(o)
spans = []
for o in sorted(changed):
    if spans and spans[-1][1] == o:
        spans[-1][1] = o + 1
    else:
        spans.append([o, o + 1])
listed = [[0x10, 0x20], [0x20, 0x22], [0x28, 0x2C], [0x58, 0x5C], [0x64, 0x68]]
idx_ok = all(r(POOL + s * 0x80 + 0x58, "<I")[0] == s and r(POOL + s * 0x80 + 0x64, "<i")[0] == -1 for s in range(64))
record("I1_constructor_field_list", spans == [[0x10, 0x22], [0x28, 0x2C], [0x58, 0x5C], [0x64, 0x68]] and idx_ok,
       bytes_written_per_slot=["+%02X..+%02X" % (a, b - 1) for a, b in spans], counter_after=r(COUNTER, "<I")[0],
       note="over pools filled 0xAA and 0x55, 0032E450 changes only +0x10..+0x21 (links, state, kind), +0x28..+0x2B, +0x58..+0x5B "
            "(= slot index) and +0x64..+0x67 (= -1) in every slot; every other byte survives")

# ---- I4: the id and the counter wrap ----
run(CTOR)
w(COUNTER, "<I", 0xFFFFFF)
id1 = request(0)
c1 = r(COUNTER, "<I")[0]
id2 = request(0)
c2 = r(COUNTER, "<I")[0]
w(COUNTER, "<I", 0x7FFFFFFF)
id3 = request(0)
c3 = r(COUNTER, "<I")[0]
w(COUNTER, "<I", 0x80000005)
id4 = request(0)
c4 = r(COUNTER, "<I")[0]
i4 = (id1 == ((0xFFFFFF << 6) + (id1 & 0x3F)) & 0xFFFFFFFF and c1 == 1 and id2 == (1 << 6) + (id2 & 0x3F) and c2 == 2
      and c3 == 0x80000000 and c4 == 0x80000006)
record("I4_counter_wrap_signed", i4 and not pumped, ids=["%08X" % x for x in (id1, id2, id3, id4)],
       counter_after=["%X" % x for x in (c1, c2, c3, c4)],
       note="counter 0xFFFFFF: id = (0xFFFFFF << 6) + slot in 32 bits, then the counter resets to 1 (next id (1 << 6) + slot). A "
            "corrupted 0x7FFFFFFF increments to 0x80000000 and 0x80000005 to 0x80000006: the compare is signed (cmovg), not a clamp")

# ---- I6: the file offset truncates toward zero to a 0x800 multiple ----
run(CTOR)
trunc = {}
for off in (0x1234, 0x7FF, 0x800, -1, -0x7FF, -0x800, -0x801, -0x1234, 0x7FFFFFFF, -0x80000000):
    rid = request(off)
    trunc["%X" % (off & 0xFFFFFFFF)] = "%X" % r(slot_of(rid) + 0x2C, "<I")[0]
    run(RECYCLE, slot_of(rid))
model = {"%X" % (o & 0xFFFFFFFF): "%X" % ((abs(o) // 0x800 * 0x800 * (1 if o >= 0 else -1)) & 0xFFFFFFFF)
         for o in (0x1234, 0x7FF, 0x800, -1, -0x7FF, -0x800, -0x801, -0x1234, 0x7FFFFFFF, -0x80000000)}
record("I6_offset_truncates_toward_zero", trunc == model, stored=trunc,
       note="the slot's +0x2C is the descriptor offset truncated TOWARD ZERO to a 0x800 multiple: 0x1234 -> 0x1000, -1 -> 0, "
            "-0x801 -> -0x800; the extremes do not overflow")

# ---- I7: recycling writes the links and the id, nothing else ----
run(CTOR)
rid = request(0x3000, kind=0x09, index=0x20, nbytes=0x647, arg=0x77, cb=0xAAAA, cancel=0xBBBB)
sl = slot_of(rid)
w(sl + 0x68, "<Q", 0x1122334455667788)                  # an unobserved byte range, planted
before = bytes(uc.mem_read(POOL, 0x2000))
run(RECYCLE, sl)
after = bytes(uc.mem_read(POOL, 0x2000))
diff = {}
for i in range(0x2000):
    if before[i] != after[i]:
        diff.setdefault(i // 0x80, set()).add(i % 0x80)
mine = sorted(diff.get((sl - POOL) // 0x80, set()))
kept = {"arg": r(sl + 0x60, "<I")[0], "kind": r(sl + 0x21, "<B")[0], "index": r(sl + 0x24, "<I")[0], "bytes": r(sl + 0x28, "<I")[0], "offset": r(sl + 0x2C, "<I")[0],
        "cb": r(sl + 0x40, "<Q")[0], "cancel": r(sl + 0x48, "<Q")[0], "dest": r(sl + 0x70, "<Q")[0], "planted_68": r(sl + 0x68, "<Q")[0]}
others = {s: sorted(v) for s, v in diff.items() if s != (sl - POOL) // 0x80}
record("I7_recycle_does_not_sanitize", r(sl + 0x64, "<i")[0] == -1 and set(mine) <= set(range(0x10, 0x20)) | set(range(0x64, 0x68))
       and kept == {"arg": 0x77, "kind": 9, "index": 0x20, "bytes": 0x647, "offset": 0x3000, "cb": 0xAAAA, "cancel": 0xBBBB, "dest": DEST,
                    "planted_68": 0x1122334455667788} and all(set(v) <= set(range(0x10, 0x20)) for v in others.values()),
       recycled_slot_bytes_changed=["+%02X" % x for x in mine], other_slots_changed={"%d" % s: ["+%02X" % x for x in v] for s, v in others.items()},
       retained=({k: "%X" % v for k, v in kept.items()}),
       note="0032EC40 changes only the recycled slot's links (+0x10..+0x1F) and id (+0x64 = -1), plus neighbours' links; kind, index, "
            "byte count, offset, callbacks, destination and an unobserved planted qword at +0x68 all survive")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
