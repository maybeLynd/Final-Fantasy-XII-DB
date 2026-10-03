"""S-02: the system-stop registry's apply 00226280 executed with NO stub, for invariants SS-1..SS-6 (OPUS, 2026-09-25).

AUDIT-SEM's runtime ruling holds SS-1..SS-6 at MIXED because EXP-191 ran the apply with its effectors stubbed. Here every
callee of the apply runs as shipped code in world.py's built world (the builder of blocks 318-353), with NO application stub:
- the registry is initialised by its own initialiser 00226B30 (boot's order), so the 28 records start inert (all-ones);
- requests are made with the shipped request 00226BE0(slot, 0, 0, 0, fade, -1), as the prelude does at 0025479D;
- the three idle objects of block 331 (zeroed blocks at [0209BE80], [01F7FFE0], [0215E6E0]) are the only planted state.
RECORDED BOUNDARY (not a stub): the sound engine singleton [01FD36A0] is not built by this world. A request that pauses a
sound category reaches it through 002DF370 -> 001DBA90 -> 00210FF0 and faults there. 13 of the 28 request ids never reach it
(4, 6, 7, 16-21, 23-26, measured by probe3.py); every case below uses only those, and each case asserts a clean return.
Hooks are registered before the first call (a unicorn read hook added later misses already-translated code).
Evidence class: NATIVE-REPLAY, live_game false. Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RDX, UC_X86_REG_RIP

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
INIT, REQUEST, APPLY = 0x226B30, 0x226BE0, 0x226280
RECA, RECB, CURSOR_END, DIRTY, BITSET, FADE_EFFECTOR = 0x1FD4160, 0x1FD4400, 0x1FD46B0, 0x1FD46D0, 0x1FD46D4, 0x226640
REG_LO, REG_HI = 0x1FD4160, 0x1FD46D8
QUIET = (4, 6, 7, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26)
W.ALLOWED |= {0x16D6A0} | W.closure(INIT) | W.closure(REQUEST) | W.closure(APPLY)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))

log = {"on": False, "reads": [], "writes": [], "calls": [], "fade_arg": []}
APPLY_LO, APPLY_HI = APPLY, APPLY + 952


def on_read(u, acc, a, n, v, _):
    if log["on"] and REG_LO <= a < REG_HI:
        log["reads"].append((a, n, u.reg_read(UC_X86_REG_RIP)))


def on_write(u, acc, a, n, v, _):
    if log["on"] and REG_LO <= a < REG_HI:
        log["writes"].append((a, n))


def on_code(u, a, n, _):
    if log["on"] and a == FADE_EFFECTOR:
        log["fade_arg"].append(u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)


uc.hook_add(UC_HOOK_MEM_READ, on_read)
uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
uc.hook_add(UC_HOOK_CODE, on_code, begin=FADE_EFFECTOR, end=FADE_EFFECTOR)
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
i32 = lambda a: struct.unpack("<i", bytes(uc.mem_read(a, 4)))[0]


def apply():
    for k in ("reads", "writes", "fade_arg"):
        log[k] = []
    log["on"] = True
    ok = S.call(APPLY)
    log["on"] = False
    return ok and not S.st["bad"] and not S.st["faults"]


def request(slot, fade):
    uc.mem_write(BITSET, struct.pack("<I", struct.unpack("<I", bytes(uc.mem_read(BITSET, 4)))[0] & ~(1 << slot)))
    return S.call(REQUEST, slot, 0, 0, 0, stack=(fade & 0xFFFFFFFF, 0xFFFFFFFF)) and not S.st["faults"]


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-40s %s" % (name, "PASS" if ok else "FAIL"))


okinit = S.call(INIT)
inert = all(q(RECA + s * 0x18) == 0xFFFFFFFFFFFFFFFF and q(RECB + s * 0x18) == 0xFFFFFFFFFFFFFFFF for s in range(28))
init_fades = [i32(RECB + s * 0x18 + 0x10) for s in range(28)]
# the initialiser leaves every fade at 0 (a NON-negative value), so the first apply takes min = 0 and resets all of them to -1:
# consume that through the shipped path (a quiet request, then the apply) before the SS-4 case
first = request(24, -1) and apply()
consumed = [i32(RECB + s * 0x18 + 0x10) for s in range(28)]
record("world_registry_initialised_inert", okinit and inert and first and set(init_fades) == {0} and set(consumed) == {-1},
       note="00226B30 leaves all 28 records all-ones and every fade 0; one shipped request + apply consumes the zeros to -1",
       fade_passed_by_first_apply=list(log["fade_arg"]))

# SS-6: with the dirty byte clear the apply returns at once - no registry write, no effector
uc.mem_write(DIRTY, b"\x00")
ok6 = apply()
record("SS6_clean_registry_apply_is_a_no_op", ok6 and log["writes"] == [] and log["fade_arg"] == [] and
       all(REG_LO <= a < REG_HI and a == DIRTY for a, n, pc in log["reads"]),
       registry_writes=len(log["writes"]), registry_reads=[["%08X" % a, n, "%08X" % pc] for a, n, pc in log["reads"]])

# three requests: fades 7, 3 and -5 (a negative other than -1, so an untouched value is visible)
reqok = request(4, 7) and request(7, 3) and request(16, -5)
dirty_after_requests = uc.mem_read(DIRTY, 1)[0]
pre_a = [q(RECA + s * 0x18) for s in range(28)]
pre_b = [q(RECB + s * 0x18) for s in range(28)]
uc.mem_write(BITSET, struct.pack("<I", 0x0BADF00D))          # garbage bitset: SS-1 says the apply never looks
okA = apply()
reads, writes, fades = list(log["reads"]), list(log["writes"]), list(log["fade_arg"])
comb_a, comb_b = q(0x1FD46A0), q(0x1FD46B8)   # [rsp+0x38] -> 01FD46A0 (00226603), [rsp+0x20] -> 01FD46B8 (00226624)
exp_a, exp_b = 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF
for s in range(28):
    exp_a &= pre_a[s]
    exp_b &= pre_b[s]
record("SS6_request_raises_dirty_and_apply_clears_it", reqok and dirty_after_requests == 1 and okA and uc.mem_read(DIRTY, 1)[0] == 0,
       dirty_after_requests=dirty_after_requests)
record("SS1_bitset_never_read", okA and not any(BITSET <= a < BITSET + 4 for a, n, pc in reads),
       bitset_reads=[["%08X" % pc] for a, n, pc in reads if BITSET <= a < BITSET + 4])
rec_reads = sorted({((a - RECA) % 0x18, n) for a, n, pc in reads if RECA <= a < CURSOR_END})
record("SS3_only_first_qword_and_fade_read", okA and set(rec_reads) <= {(0, 8), (0x10, 4)},
       record_offsets_read=[["%X" % o, n] for o, n in rec_reads])
record("SS2_combine_is_AND_over_28_with_all_ones_identity", okA and (comb_a, comb_b) == (exp_a, exp_b),
       combined=["%016X" % comb_a, "%016X" % comb_b], expected=["%016X" % exp_a, "%016X" % exp_b])
record("SS4_fade_is_min_of_nonnegative_and_consumed", okA and fades == [3] and i32(RECB + 4 * 0x18 + 0x10) == -1
       and i32(RECB + 7 * 0x18 + 0x10) == -1 and i32(RECB + 16 * 0x18 + 0x10) == -5,
       fade_passed_to_00226640=fades, fades_after={4: i32(RECB + 4 * 0x18 + 0x10), 7: i32(RECB + 7 * 0x18 + 0x10), 16: i32(RECB + 16 * 0x18 + 0x10)})
record("SS5_bit41_in_every_record_B_after_apply", okA and all(q(RECB + s * 0x18) >> 41 & 1 for s in range(28)),
       record_B_without_bit41=[s for s in range(28) if not q(RECB + s * 0x18) >> 41 & 1])

# SS-1 control: the same registry state with a different bitset gives the identical outcome
state = bytes(uc.mem_read(REG_LO, REG_HI - REG_LO))
outs = []
for bits in (0, 0xFFFFFFFF):
    uc.mem_write(REG_LO, state)
    request(24, 2)                                # re-dirty through the shipped path
    uc.mem_write(BITSET, struct.pack("<I", bits))
    okc = apply()
    outs.append((okc, q(0x1FD46A0), q(0x1FD46B8), tuple(log["fade_arg"])))
record("SS1_control_bitset_does_not_change_the_outcome", outs[0] == outs[1] and outs[0][0],
       outcomes=[[o[0], "%016X" % o[1], "%016X" % o[2], list(o[3])] for o in outs])

res = {"ok": allok, "quiet_request_ids": list(QUIET), "cases": results,
       "boundary": "sound engine singleton [01FD36A0] not built; requests 0-3, 5, 8-15, 22, 27 reach it via 002DF370 -> 001DBA90 -> 00210FF0 and are not used"}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
print("ALL PASS" if allok else "NOT ALL PASS")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
