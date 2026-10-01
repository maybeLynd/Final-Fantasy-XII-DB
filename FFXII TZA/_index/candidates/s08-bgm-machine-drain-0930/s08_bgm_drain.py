"""S-08 I3 same-call drain with the BGM stream machine 003EADE0 REAL (SWE2-ORACLE, 2026-09-30).

Request: OPUS-REQ-ORACLE-S08-BGM-MACHINE-REAL. candidates/s08-runtime-per-invariant-exposure.md names 003EADE0 as the one
exposure of I3's same-call drain: the pump's state-1 arm (0032E0BD) calls 003EADD0 -> 003EADE0 before it services the head
request and ends the pass on a non-zero return (0032E0C4), and the machine can itself submit through 0032E780 -> 0032E870.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Harness: OPUS block 318/330's world
(_index/candidates/s08-opus-replay-queue-static-invariants/world.py + world.json + printf_bridge.py), imported read-only (no
bytecode written, its check.py is NOT imported so its result files are untouched). The constructor 0032E450, requester
0032E870, head-insert wrapper 0032E780, pump 0032E070, in-flight getter 0032E4D0, recycler 0032EC40, size getter 0032E400,
piece size 002DF600, 003EADD0 and 003EADE0 all run as shipped. No application stub.

Declared fixtures (each also listed in README.md):
  F1 pool: rebuilt by the shipped constructor, then 64 zero-byte requests through the shipped requester (as i2i3.py).
  F2 BgmStream 02B5E0E0 (0x38 B): planted per case (active, state, counters, buffer pointer). The shipped build never
     activates it (music-control page 3.4: no script issues the verbs), so every active != 0 case is a modded-script domain.
  F3 C_STATE1 only: the kind-0x24 size-table slot 022C51F0+0x24*8 -> a fixture array with entry[3] = 0x40000 (the shipped
     build has no kind-36 sizes).
  F4 pacer OS bridges and the frame-counter tick at 0035EBB0 (the other thread's effect) - identical to i2i3.py.
  F5 PLANNED STOP (recursion cases only): the run is stopped when the requester 0032E870 has been entered 1 + DEPTH times
     without returning; the stop is an instrument boundary, not an effect of the code.
Writes s08_bgm_drain.out-style lines to stdout and s08_bgm_drain_result.json next to this file.
"""
import hashlib
import json
import os
import struct
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OPUS_DIR = os.path.join(DB, "_index", "candidates", "s08-opus-replay-queue-static-invariants")
if not os.path.isdir(OPUS_DIR):
    OPUS_DIR = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\s08-opus-replay-queue-static-invariants"
sys.path.insert(0, OPUS_DIR)

from unicorn import UC_HOOK_CODE                              # noqa: E402
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RSP   # noqa: E402

import world as W                                             # noqa: E402

AUTH = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
assert hashlib.sha256(W.raw).hexdigest() == AUTH, "image is not the authority EXE"
HARNESS = {n: hashlib.sha256(open(os.path.join(OPUS_DIR, n), "rb").read()).hexdigest()[:16]
           for n in ("world.py", "world.json", "printf_bridge.py")}

CTOR, REQ, RECYCLE, PUMP, HEADREQ = 0x32E450, 0x32E870, 0x32EC40, 0x32E070, 0x32E780
MACH_WRAP, MACH = 0x3EADD0, 0x3EADE0
POOL, FREE, PEND_H = 0x22C31C0, 0x22C51D0, 0x22C51C0
BGM = 0x2B5E0E0
SIZETAB = 0x22C51F0
FRAME = 0x22CA5E0
DEPTH = 6

W.ALLOWED |= {0x16D6A0} | set().union(*(W.closure(f) for f in (CTOR, REQ, RECYCLE, PUMP, MACH_WRAP)))
for _k, _v in {"GetCurrentThread": 0xFFFFFFFFFFFFFFFE, "GetThreadPriority": 0, "SetThreadPriority": 1,
               "SwitchToThread": 0, "Sleep": 0, "SleepEx": 0}.items():
    W.OSRET[_k] = _v
    W.BRIDGED.add(_k)
FX = json.load(open(os.path.join(OPUS_DIR, "world.json")))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
DESC, DEST, BUF, SZFIX = 0x76300000, 0x76310000, 0x76400000, 0x76380000

# ---- instrumentation (observers only; none writes guest state except the declared pacer tick) ----
ev = {"mach": [], "arm_ret": [], "req_live": 0, "req_max": 0, "req_entries": 0, "headreq": 0, "stopped": None, "polls": 0}


def _mach(u, a, n, _):
    b = bytes(u.mem_read(BGM, 0x38))
    ev["mach"].append({"state": b[0x30], "active": b[0x31], "rsp": u.reg_read(UC_X86_REG_RSP)})


def _arm_ret(u, a, n, _):                                   # 0032E0C2: eax = 003EADD0's return in the state-1 arm
    ev["arm_ret"].append(u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)


def _req(u, a, n, _):
    ev["req_entries"] += 1
    ev["req_live"] += 1
    ev["req_max"] = max(ev["req_max"], ev["req_live"])
    if LIMIT["on"] and ev["req_live"] > 1 + DEPTH:
        ev["stopped"] = "planned stop: 0032E870 entered %d times without returning" % ev["req_live"]
        u.emu_stop()


def _req_ret(u, a, n, _):                                   # the requester's single ret (0032E98C)
    ev["req_live"] -= 1


def _headreq(u, a, n, _):
    ev["headreq"] += 1


def _tick(u, a, n, _):
    ev["polls"] += 1
    u.mem_write(FRAME, (int.from_bytes(bytes(u.mem_read(FRAME, 8)), "little") + 1).to_bytes(8, "little"))


LIMIT = {"on": False}
for addr, fn in ((MACH, _mach), (0x32E0C2, _arm_ret), (REQ, _req), (0x32E98C, _req_ret), (HEADREQ, _headreq),
                 (0x35EBB0, _tick)):
    uc.hook_add(UC_HOOK_CODE, fn, begin=addr, end=addr)
uc.ctl_flush_tb()


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def walk(head):
    out, p, g = [], r(head, "<Q")[0], 0
    while p and g < 200:
        out.append((p - POOL) // 0x80)
        p = r(p + 0x10, "<Q")[0]
        g += 1
    return out


def lists():
    f, pn = walk(FREE), walk(PEND_H)
    return {"free": len(f), "pending": len(pn), "cover": sorted(f + pn) == list(range(64)) and not (set(f) & set(pn))}


def req(nbytes=0):
    w(DESC, "<iIIIQQ", 0x1000, 0, 0x55, 0, 0, 0)
    ok = S.call(REQ, 0x24, 3, DEST, nbytes, stack=(DESC, 0))
    assert ok, (S.st["bad"] or S.st["faults"])[:2]


def plant_bgm(active, state, file_bytes=0x40000, bytes_read=0x10000, buf_bytes=0x30000, request_id=-1):
    blk = bytearray(0x38)
    struct.pack_into("<iIQiiiiiiii", blk, 0, request_id, 0, BUF, buf_bytes, 0, 0, 0x24, 3, file_bytes, bytes_read,
                     bytes_read % buf_bytes)
    blk[0x30], blk[0x31], blk[0x32], blk[0x33] = state, active, 0x40, 0x7F
    uc.mem_write(BGM, bytes(blk))


def run_case(name, active, state, size_fixture=False, recursion=False, **kw):
    for k in ("mach", "arm_ret"):
        ev[k] = []
    ev.update(req_live=0, req_max=0, req_entries=0, headreq=0, stopped=None, polls=0)
    LIMIT["on"] = False
    uc.mem_write(POOL, bytes(0x2000))
    w(SIZETAB + 0x24 * 8, "<Q", SZFIX if size_fixture else 0)
    if size_fixture:
        uc.mem_write(SZFIX, bytes(0x1000))
        w(SZFIX + 3 * 4, "<i", 0x40000)
    w(BGM, "<Q", 0)
    uc.mem_write(BGM, bytes(0x38))                        # stream idle while the pool is filled
    assert S.call(CTOR)
    for _ in range(64):
        req(0)
    full = lists()
    plant_bgm(active, state, **kw)
    before = bytes(uc.mem_read(BGM, 0x38))
    for k in ("mach", "arm_ret"):
        ev[k] = []
    ev.update(req_live=0, req_max=0, req_entries=0, headreq=0, stopped=None, polls=0)
    LIMIT["on"] = recursion
    ok = S.call(REQ, 0x24, 3, DEST, 0, stack=(DESC, 0))
    LIMIT["on"] = False
    rid = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    after = bytes(uc.mem_read(BGM, 0x38))
    rsps = [m["rsp"] for m in ev["mach"]]
    return {"case": name, "returned": ok, "id": "%X" % rid if ok else None,
            "stop": ev["stopped"] or ((S.st["bad"] or S.st["faults"])[:2] if not ok else None),
            "full_before": full, "after": lists(), "mach_calls": len(ev["mach"]),
            "mach_states": sorted({m["state"] for m in ev["mach"]}),
            "arm_returns": sorted(set(ev["arm_ret"])), "arm_calls": len(ev["arm_ret"]),
            "req_entries": ev["req_entries"], "req_max_live": ev["req_max"], "headreq_calls": ev["headreq"],
            "mach_rsp_strictly_falling": all(b < a for a, b in zip(rsps, rsps[1:])) if len(rsps) > 1 else None,
            "mach_rsp_step": (rsps[0] - rsps[1]) if len(rsps) > 1 else None,
            "pacer_polls": ev["polls"], "bgm_before": before.hex(), "bgm_after": after.hex(),
            "bgm_state_after": after[0x30], "bgm_active_after": after[0x31]}


CASES = []
CHECKS = []


def check(name, cond, detail):
    CHECKS.append((name, bool(cond), detail))


# C0 control - the shipped reality: stream inactive (active = 0).
c0 = run_case("C0_inactive", 0, 0)
CASES.append(c0)
check("C0 returns with a valid id", c0["returned"] and c0["id"] not in (None, "0"), c0["id"])
check("C0 drains all 64 in the same call", c0["full_before"]["pending"] == 64 and c0["after"]["pending"] == 1
      and c0["after"]["free"] == 63 and c0["after"]["cover"], c0["after"])
check("C0 machine entered once per state-1 arm visit and returns 0", c0["mach_calls"] >= 64 and c0["arm_returns"] == [0]
      and c0["arm_calls"] == 64, (c0["mach_calls"], c0["arm_calls"], c0["arm_returns"]))
check("C0 stream bytes unchanged", c0["bgm_before"] == c0["bgm_after"], "")

# C1 active, state 5 ('ready', waiting for bgmstreamplay): no arm for 5 in the machine's table -> returns 0.
c1 = run_case("C1_active_state5_ready", 1, 5)
CASES.append(c1)
check("C1 drains all 64 in the same call", c1["returned"] and c1["after"]["pending"] == 1 and c1["after"]["free"] == 63,
      c1["after"])
check("C1 machine returns 0 at every arm visit", c1["arm_returns"] == [0] and c1["arm_calls"] == 64, c1["arm_returns"])
check("C1 stream bytes unchanged", c1["bgm_before"] == c1["bgm_after"], "")

# C2 active, state 8 with its read done (requestId -1 -> 0032E4D0 'not in flight'), all bytes read: -> state 7, returns 0.
#     Next arm visit, state 7 with bytesRead == fileBytes, calls the sound layer 002DF630 - a stop boundary of this world,
#     so the case is sized to observe only the first transition and is NOT a drain case.
# (omitted by design: every path out of 4/6/7-all-read enters the sound layer, which this world does not build.)

# C3 active, state 7 with bytes left: the machine submits the next piece through 0032E780 BEFORE it writes state 8.
c3 = run_case("C3_active_state7_piece_pending", 1, 7, recursion=True, file_bytes=0x40000, bytes_read=0x10000)
CASES.append(c3)
check("C3 does not return (planned stop)", not c3["returned"] and c3["stop"] and "planned stop" in str(c3["stop"]),
      c3["stop"])
check("C3 nothing drained: 64 pending, 0 free at the stop", c3["after"]["pending"] == 64 and c3["after"]["free"] == 0,
      c3["after"])
check("C3 re-entry chain: requester nested 1+DEPTH deep via 0032E780, machine re-entered in state 7 each level",
      c3["req_max_live"] == 1 + DEPTH + 1 and c3["headreq_calls"] == DEPTH + 1 and c3["mach_states"] == [7]
      and c3["mach_rsp_strictly_falling"], (c3["req_max_live"], c3["headreq_calls"], c3["mach_states"],
                                            c3["mach_rsp_step"]))
check("C3 state never advances to 8 (the write follows the submission)", c3["bgm_state_after"] == 7, c3["bgm_state_after"])

# C4 active, state 1 (fresh bgmstreamread) with a planted kind-0x24 size (F3): same order - submit, then state 2.
c4 = run_case("C4_active_state1_fresh_read", 1, 1, size_fixture=True, recursion=True, file_bytes=0, bytes_read=0)
CASES.append(c4)
check("C4 does not return (planned stop)", not c4["returned"] and c4["stop"] and "planned stop" in str(c4["stop"]),
      c4["stop"])
check("C4 nothing drained: 64 pending, 0 free at the stop", c4["after"]["pending"] == 64 and c4["after"]["free"] == 0,
      c4["after"])
check("C4 re-entry chain in state 1", c4["req_max_live"] == 1 + DEPTH + 1 and c4["headreq_calls"] == DEPTH + 1
      and c4["mach_states"] == [1] and c4["mach_rsp_strictly_falling"],
      (c4["req_max_live"], c4["headreq_calls"], c4["mach_states"], c4["mach_rsp_step"]))
check("C4 fileBytes taken from the size table (0x40000) and state still 1", struct.unpack_from("<i", bytes.fromhex(
      c4["bgm_after"]), 0x24)[0] == 0x40000 and c4["bgm_state_after"] == 1, c4["bgm_after"][0x48:0x50])

# Negative control on the checker itself: a corrupted C0 record must fail the C0 drain predicate.
bad = dict(c0, after={"free": 62, "pending": 2, "cover": True})
check("NEG corrupted C0 record is rejected by the drain predicate",
      not (bad["after"]["pending"] == 1 and bad["after"]["free"] == 63), bad["after"])

fails = [c for c in CHECKS if not c[1]]
for n, ok, d in CHECKS:
    print("%-4s %s  %s" % ("PASS" if ok else "FAIL", n, json.dumps(d, default=str)[:160]))
print("harness sha16:", json.dumps(HARNESS, sort_keys=True))
print("checks %d FAILS %d" % (len(CHECKS), len(fails)))
json.dump({"cases": CASES, "checks": [{"name": n, "pass": ok} for n, ok, _ in CHECKS], "harness": HARNESS,
           "image_sha256": AUTH, "depth": DEPTH}, open(os.path.join(HERE, "s08_bgm_drain_result.json"), "w"),
          indent=1, sort_keys=True)
