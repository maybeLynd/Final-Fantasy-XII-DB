"""S-28: execute PF-3..PF-8 of CONTRACT-party-focus-and-control-suppression.md - the request 003594B0, the summon upgrade 003594C0,
the commit 00358BB0 -> 00358BC0 with its real teardown 0025A6A0 and push 002681D0, and the suppression recompute 0023B040 through
the real leader derivation 003272A0 (003590D0 -> 003588B0 -> 00263E30) - as shipped code (OPUS, 2026-09-25, block 338).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges. No application stub and no stop boundary.
Fixtures (the leader chain EXP-145 disclosed, planted here the same way): the focus handle d[022C7FE0]; the enable bit
b[02089340] & 0x10; the manager 00263FF0 returns for table 0 (+0 non-null, +8 the object array, +0x10 enable, +0x20 count); the
object (w +0x16 generation, q +0x30 the leader, q +0xC0 a context naming motion entry 0); motion entry 0 of the 0x740 table
behind [022C6F28] (+0x284 set, +0xC8 = -1, +0xCC = 0x2001: the leader's current motion, which 00322920 / 00322600 test);
the leader record (byte 0 bit 3, +8 id, +0x5C = 0x2001, +0x698 stats) and its stats status words +0x64 / +0x3C; six idle objects (the world's convention).
Writes result_focus.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
RECOMPUTE, LEADER, MGR = 0x23B040, 0x3272A0, 0x263FF0
OUT1, OUT2 = 0x3592C0, 0x359200
REQUEST, UPGRADE, COMMIT_THUNK, TEARDOWN = 0x3594B0, 0x3594C0, 0x358BB0, 0x25A6A0
W.ALLOWED |= {0x16D6A0, UPGRADE, 0x25A680, 0x25A690, TEARDOWN} | W.closure(RECOMPUTE) | W.closure(REQUEST) | W.closure(UPGRADE) \
    | W.closure(COMMIT_THUNK) | W.closure(0x358BC0) | W.closure(TEARDOWN)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
OBJ, ARR, UNIT, STATS = 0x76300000, 0x76301000, 0x76302000, 0x76304000
FOCUS, ENABLE = 0x22C7FE0, 0x2089340
GEN, SLOT = 5, 3


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


from unicorn.x86_const import UC_X86_REG_RAX
assert S.call(MGR, 0)
MANAGER = uc.reg_read(UC_X86_REG_RAX)
MOTION = struct.unpack("<Q", bytes(uc.mem_read(0x22C6F28, 8)))[0]      # the 0x740-stride table 002E8100 indexes (a world cell)
CTX = 0x76305000
outs = []
# 003592C0(1, bit 2) carries the value in edx; 00359200(bit 0, 1) carries it in ecx
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: outs.append(["003592C0", u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF]), begin=OUT1, end=OUT1)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: outs.append(["00359200", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF]), begin=OUT2, end=OUT2)
tail = []
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: tail.append(u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF), begin=0x23B1EA, end=0x23B1EA)


def leader(status=0, stats=True):
    uc.mem_write(MANAGER, bytes(0x28))
    w(MANAGER, "<Q", 1)
    w(MANAGER + 8, "<Q", ARR)
    w(MANAGER + 0x10, "<B", 1)
    w(MANAGER + 0x20, "<I", 16)
    uc.mem_write(ARR, bytes(0x100))
    w(ARR, "<I", 16)
    w(ARR + 8 + 8 * SLOT, "<Q", OBJ)
    uc.mem_write(OBJ, bytes(0x100))
    w(OBJ + 0x16, "<H", GEN)
    w(OBJ + 0x30, "<Q", UNIT)
    w(OBJ + 0xC0, "<Q", CTX)                               # 002E8100: the object's context -> motion index 0
    uc.mem_write(CTX, bytes(0x10))
    uc.mem_write(MOTION, bytes(0x740))
    w(MOTION + 0x284, "<I", 1)
    w(MOTION + 0xC8, "<i", -1)
    w(MOTION + 0xCC, "<H", 0x2001)                          # 0041FCA0 returns this word: a value 00322920 / 00322600 accept
    uc.mem_write(UNIT, bytes(0x1000))
    w(UNIT, "<B", 8)
    w(UNIT + 8, "<I", (GEN << 20) | SLOT)
    w(UNIT + 0x5C, "<I", 0x2001)
    uc.mem_write(STATS, bytes(0x200))
    if stats:
        w(UNIT + 0x698, "<Q", STATS)
        w(STATS + 0x64, "<I", status)
    w(FOCUS, "<I", (GEN << 20) | SLOT)
    w(ENABLE, "<B", r(ENABLE, "<B")[0] | 0x10)


def recompute():
    del outs[:]
    del tail[:]
    ok = S.call(RECOMPUTE)
    return ok


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


leader()
okl = S.call(LEADER)
got_leader = uc.reg_read(UC_X86_REG_RAX)
record("leader_derived", okl and got_leader == UNIT, leader="%X" % got_leader,
       note="003272A0 resolves the focus handle through 003588B0 (generation, table, slot) and 00263E30 to the planted leader")

pf7 = {}
for label, st in (("status 0", 0), ("bit 14 only (0x4000)", 1 << 14), ("bit 3 (0x8, in both masks)", 1 << 3),
                  ("bit 27 (0x08000000, in both masks)", 1 << 27), ("bit 1 (in the gate 0x80000003)", 1 << 1)):
    leader(status=st)
    ok = recompute()
    bits = {"bit0 (00359200)": [o for o in outs if o[0] == "00359200"][0][1] if any(o[0] == "00359200" for o in outs) else None,
            "bit2 (003592C0)": [o for o in outs if o[0] == "003592C0"][0][1] if any(o[0] == "003592C0" for o in outs) else None,
            "not bit1 (tail)": tail[0] if tail else None}
    pf7[label] = dict(ok=ok, **bits)
z, b14, b3 = pf7["status 0"], pf7["bit 14 only (0x4000)"], pf7["bit 3 (0x8, in both masks)"]
pf7_ok = (all(v["ok"] for v in pf7.values())
          and (z["bit0 (00359200)"], z["bit2 (003592C0)"], z["not bit1 (tail)"]) == (0, 0, 1)
          and (b14["bit0 (00359200)"], b14["bit2 (003592C0)"], b14["not bit1 (tail)"]) == (1, 1, 1)
          and (b3["bit0 (00359200)"], b3["bit2 (003592C0)"], b3["not bit1 (tail)"]) == (1, 1, 0))
record("PF7_bit14_raises_0_and_2_only", pf7_ok, cases=pf7,
       note="status 0 suppresses nothing; a status whose only bit is 14 raises suppression bits 0 and 2 and leaves bit 1 clear "
            "(0x8800403B hits, 0x8800003B misses); bit 3, in both masks, raises all three")

leader(status=0, stats=False)
okn = recompute()
fault = (S.st["faults"] or [None])[0]
trace = ["%08X" % a for a in list(S.st["trace"])[-3:]]
record("PF8_null_stats_faults_mid_function", not okn and fault == "00000064", fault=fault, last_instructions=trace,
       note="a leader whose +0x698 is null passes the first check (0023B0AB sends it on), then 0023B15E dereferences the unguarded "
            "second load: the recompute faults reading address 0x64")

# ---- PF-3..PF-6: request, commit, teardown ----
OBJ2, UNIT2, H1, H2 = 0x76306000, 0x76307000, (GEN << 20) | SLOT, (GEN << 20) | 4
order = []
for a_, nm in ((0x3272A0, "leader getter"), (0x358C24, "re-read pending 00358C24"), (0x358C2F, "store current 00358C2F"),
               (0x358C35, "clear kind 00358C35"), (0x358C3C, "resolve 00358C3C"), (0x358C52, "tail push 00358C52"),
               (0x25A680, "teardown thunk 0025A680 (flag 1)"), (0x25A690, "teardown thunk 0025A690 (flag 0)"),
               (0x3D9B80, "003D9B80 (the summon-only call)"), (0x2681D0, "push 002681D0"),
               (0x358B40, "release outgoing 00358B40"), (0x259800, "00259800")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: order.append(nm), begin=a_, end=a_)


def two_leaders():
    leader()
    uc.mem_write(OBJ2, bytes(0x100))
    w(OBJ2 + 0x16, "<H", GEN)
    w(OBJ2 + 0x30, "<Q", UNIT2)
    uc.mem_write(UNIT2, bytes(0x1000))
    w(UNIT2, "<B", 8)
    w(UNIT2 + 8, "<I", H2)
    w(ARR + 8 + 8 * 4, "<Q", OBJ2)


def focus():
    return {"current": "%X" % r(FOCUS, "<I")[0], "pending": "%X" % r(FOCUS + 4, "<I")[0], "kind": r(FOCUS + 0x18, "<B")[0]}


pf = {}
for label, target, upgrade in (("redundant (pending = current)", H1, False), ("change, kind 1", H2, False), ("change, kind 2 (summon)", H2, True)):
    two_leaders()
    assert S.call(REQUEST, target)
    if upgrade:
        assert S.call(UPGRADE, 2)
    after_request = focus()
    assert S.call(LEADER)
    leader_between = uc.reg_read(UC_X86_REG_RAX)
    del order[:]
    okc = S.call(COMMIT_THUNK)
    pf[label] = {"after_request": after_request, "leader_between": "%X" % leader_between, "commit_ok": okc,
                 "order": [o for o in order if o != "leader getter"], "after_commit": focus()}
red, k1, k2 = pf["redundant (pending = current)"], pf["change, kind 1"], pf["change, kind 2 (summon)"]
tail_body = ["store current 00358C2F", "clear kind 00358C35", "resolve 00358C3C", "tail push 00358C52", "push 002681D0"]


def subseq(want, got):
    it = iter(got)
    return all(x in it for x in want)
record("PF3_deferred_until_commit", k1["after_request"]["current"] == "%X" % H1 and k1["after_request"]["pending"] == "%X" % H2
       and k1["after_request"]["kind"] == 1 and k1["leader_between"] == "%X" % UNIT and k1["after_commit"]["current"] == "%X" % H2,
       case=k1, note="the request writes pending and kind 1 and moves nothing: the leader getter still returns the old leader; the commit "
                     "installs the new handle")
record("PF4_redundant_commit_still_pushes", red["commit_ok"] and red["order"] == tail_body and red["after_commit"]["kind"] == 0, case=red,
       note="pending = current: 00358BE4 jumps straight to the store - no release, no teardown, no re-read - but the store, the kind "
            "clear, the resolve and the push all run")
record("PF5_PF6_order_and_the_summon_call", k1["commit_ok"] and k2["commit_ok"]
       and subseq(["release outgoing 00358B40", "00259800", "teardown thunk 0025A680 (flag 1)", "re-read pending 00358C24"] + tail_body,
                  k1["order"]) and "003D9B80 (the summon-only call)" not in k1["order"] and "teardown thunk 0025A690 (flag 0)" not in k1["order"]
       and subseq(["release outgoing 00358B40", "00259800", "teardown thunk 0025A690 (flag 0)", "003D9B80 (the summon-only call)",
                   "re-read pending 00358C24"] + tail_body, k2["order"]) and "teardown thunk 0025A680 (flag 1)" not in k2["order"]
       and k1["after_commit"] == {"current": "%X" % H2, "pending": "%X" % H2, "kind": 0}
       and k2["after_request"]["kind"] == 2, kind1=k1, kind2=k2,
       note="a real change releases the outgoing leader (00358B40), calls 00259800, runs the teardown, and only then re-reads pending, "
            "stores it, clears the kind, resolves and pushes; kind 1 "
            "takes thunk 0025A680 (flag 1), kind 2 - set by the summon upgrade 003594C0 - takes 0025A690 (flag 0), and only that path "
            "calls 003D9B80. The pending handle is not cleared by the commit")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result_focus.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
