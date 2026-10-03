"""S-20: execute the native command seam 00311CF0 and the commit funnel 0030F760 (CONTRACT-native-command-seam.md CS-1, CS-2,
CS-5), and follow a commit into the handler-table dispatch 00305080 (OPUS, 2026-09-25, block 351) - probe draft.

Evidence class: NATIVE-REPLAY (unicorn), live_game false.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
SEAM, COMMIT, DISPATCH = 0x311CF0, 0x30F760, 0x305080
W.ALLOWED |= ({0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (SEAM, COMMIT, DISPATCH))))
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
POOL, HANDLES, CTX = 0x76280000, 0x76290000, 0x762D0000
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
REC = BLOCK + 8


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def world():
    uc.mem_write(POOL, bytes(0xF50 * 2))
    uc.mem_write(HANDLES, bytes(0x400))
    uc.mem_write(CTX, bytes(0x100))
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 1)
    w(POOL + 0x10, "<Q", HANDLES)
    w(POOL + 0x698, "<Q", REC)
    w(POOL + 8, "<I", 0x100001)
    uc.mem_write(REC, bytes(0x1C8))



import pefile

pe = pefile.PE(W.EXE, fast_load=True)
TABLE = 0x1EEC460
ENTRY5 = struct.unpack_from("<Q", pe.get_data(TABLE - 0x120000 + 8 * 5, 8))[0]
W.ALLOWED |= {ENTRY5}                                  # the dispatcher's `jmp rdx` target (block 350)
COMMIT_FIELDS = (0x708, 0x71F)
ev = {"field_writes": [], "calls": [], "stop": None}
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev["field_writes"].append(["+%X" % (a - POOL), "%08X" % u.reg_read(UC_X86_REG_RIP)]),
            begin=POOL + COMMIT_FIELDS[0], end=POOL + COMMIT_FIELDS[1])
for a, nm in ((0x317E60, "00317E60"), (0x3105D0, "reset 003105D0"), (0x377C20, "00377C20")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev["calls"].append(nm), begin=a, end=a)


def _stop(u, x, n, _):
    ev["stop"] = "%08X" % x
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, _stop, begin=ENTRY5, end=ENTRY5)


def call(fn, *args, stack=(0,)):
    ev["field_writes"], ev["calls"], ev["stop"] = [], [], None
    ok = S.call(fn, *args, stack=stack)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def fields():
    return {"708": "%X" % r(POOL + 0x708, "<Q")[0], "710": "%X" % r(POOL + 0x710, "<I")[0], "714": "%X" % r(POOL + 0x714, "<H")[0],
            "BA0": "%X" % r(POOL + 0xBA0, "<H")[0], "BB8": "%X" % r(POOL + 0xBB8, "<I")[0]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- CS-1: the seam records a PENDING command and does not commit ----
cs1 = {}
for label, target in (("target 0 (self)", 0), ("target 0x200002", 0x200002)):
    world()
    ok, ret = call(SEAM, POOL, target, 1, 0x4005)
    cs1[label] = {"ok": ok, "ret": ret, "fields": fields(), "commit_field_writes": list(ev["field_writes"]), "calls": list(ev["calls"])}
record("CS1_seam_records_pending_not_commit", all(v["ok"] and v["ret"] == 0 and v["fields"]["BA0"] == "4005" and not v["commit_field_writes"]
                                                  and v["fields"]["714"] == "0" and "00317E60" in v["calls"] for v in cs1.values())
       and cs1["target 0 (self)"]["fields"]["BB8"] == "100001" and cs1["target 0x200002"]["fields"]["BB8"] == "200002", cases=cs1,
       note="00311CF0(unit, target, r8b, command 0x4005) returns 0 and records the command as PENDING: +0xBA0 = 0x4005, +0xBB8 = the "
            "target (the unit's own id +8 when the target is 0), then calls 00317E60 - and writes NOTHING in +0x708..+0x71F")

gates = {}
for label, status, cmd, pre714 in (("status bit 3 (0x8800203B only)", 0x8, 0x4005, 0), ("status bit 0 (0x80000003)", 0x1, 0x4005, 0),
                                   ("command 0x113 while +0x714 = 0x113", 0, 0x113, 0x113)):
    world()
    w(REC + 0x64, "<I", status)
    w(POOL + 0x714, "<H", pre714)
    ok, ret = call(SEAM, POOL, 0, 1, cmd)
    gates[label] = {"ok": ok, "ret": "%X" % ret, "BA0": fields()["BA0"], "calls": list(ev["calls"])}
world()
w(POOL + 0x698, "<Q", 0)
ok, ret = call(SEAM, POOL, 0, 1, 0x4005)
gates["null stats"] = {"ok": ok, "ret": "%X" % ret, "BA0": fields()["BA0"]}
record("CS1_seam_refusals", all(v["ok"] and v["BA0"] == "0" for v in gates.values())
       and gates["status bit 3 (0x8800203B only)"]["ret"] == "0" and gates["status bit 0 (0x80000003)"]["ret"] == "FFFFFFFE"
       and gates["command 0x113 while +0x714 = 0x113"]["ret"] == "FFFFFFFE" and gates["null stats"]["ret"] == "FFFFFFFE", cases=gates,
       note="three refusals, two return values: a status bit only in 0x8800203B returns 0 (indistinguishable from success) with nothing "
            "recorded; bit 0 (0x80000003 with 00377C20 false), command 0x113 over a current 0x113, or a null stats pointer return -2")

# ---- CS-2: the commit funnel writes the three fields ----
cs2 = {}
for label, reset in (("no reset", 0), ("reset first", 1)):
    world()
    w(POOL + 0x6B4, "<B", 7)
    ok, ret = call(COMMIT, POOL, CTX, 0x4005, 0x100001, stack=(reset,))
    cs2[label] = {"ok": ok, "ret": ret, "fields": fields(), "phase_6B4": r(POOL + 0x6B4, "<B")[0], "calls": list(ev["calls"]),
                  "writers": sorted({x[1] for x in ev["field_writes"]})}
record("CS2_commit_writes_the_three_fields", all(v["ok"] and v["fields"]["708"] == "%X" % CTX and v["fields"]["710"] == "100001"
                                                 and v["fields"]["714"] == "4005" and v["phase_6B4"] == 0 for v in cs2.values())
       and "reset 003105D0" in cs2["reset first"]["calls"] and "reset 003105D0" not in cs2["no reset"]["calls"], cases=cs2,
       note="0030F760(unit, ctx, id 0x4005, focus 0x100001, reset) stores +0x708 = ctx, +0x710 = focus, +0x714 = id and phase +0x6B4 = 0 "
            "(from 7); its fifth argument runs the reset 003105D0 first")

# ---- CS-5: the dispatch trusts +0x714, which only the commit writes ----
world()
call(SEAM, POOL, 0, 1, 0x4005)
ok_a, ret_a = call(DISPATCH, POOL, stack=())
seam_only = {"ok": ok_a, "ret": "%X" % ret_a, "stop": ev["stop"]}
call(COMMIT, POOL, CTX, 0x4005, 0x100001)
call(DISPATCH, POOL, stack=())
committed = {"stop": ev["stop"]}
record("CS5_dispatch_reads_the_committed_id", seam_only["ok"] and seam_only["ret"] == "FFFFFFFF" and seam_only["stop"] is None
       and committed["stop"] == "%08X" % ENTRY5, seam_only=seam_only, after_commit=committed, handler_for_4005="%08X" % ENTRY5,
       note="after the seam alone (+0xBA0 = 0x4005, +0x714 = 0) the dispatcher 00305080 returns -1; after the commit it reaches "
            "table[5] = %08X (a recorded stop at the handler entry) - the dispatch reads +0x714, not the pending +0xBA0" % ENTRY5)

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
