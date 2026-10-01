"""S-45 (OPUS, 2026-09-26): CONTRACT-achievement-counters' unexecuted items run as shipped code over the REAL image-backed
state block - the read and store bounds, kind 4's saturation on every kind-4 id, the widths and offsets, the evaluate-before-store
order, and the award tail with the Steam manager absent.

EXP-089 planted the save image and the manager. Here the block pointer [020927C0] is bound by its own binder, 00253970's prefix
up to 00253997 (00249840, then 002EF640() + 0x8200 stored at 00253990), as in s21-opus-replay-applier-stub-free/item38.py; the
counters live at *(020927C0) + 0x384C + descriptor +1, the award bitmap at + 0x3844 (fields.tsv AchievementDescriptor, corrected
2026-09-13). The manager cell [01F83450] is left as the image leaves it: its one writer 0020CD30 is not run, which is the state
the Steam contract's I-1 describes after a failed Init. Loads block 332's check.py (its cases run first, unchanged). No
application stub; no import is reached by the cases.
Boundary record (B): the manager builder 0020CD30 runs 0020C730, which registers three callbacks through
SteamAPI_RegisterCallback (bridged by name here, recording its arguments) and then needs SteamInternal_ContextInit, the Steam
library's interface object - not bridged, so the manager is not built.
Cases:
 K1  kind 4 saturates at 0x7FFFFFFF on every kind-4 id (6, 7, 11, 17): stored 0x7FFFFFF0, +0x100 -> 0x7FFFFFFF; below the
     limit the add is exact (100 + 5 -> 105).
 K2  kind 2 saturates at 0x7FFF (id 0: 0x7FF0 + 0x100 -> 0x7FFF), and the word write leaves the neighbouring counter alone.
 K3  the store writes exactly `kind` bytes at block + 0x384C + the descriptor's offset (id 0: 2 bytes at +0x384C; id 6: 4 bytes at
     +0x3860).
 K4  the bound: ids 30, 31 and 255 - the read returns -1, the store writes nothing, and the update enters neither evaluate nor
     store and writes nothing.
 K5  the update calls evaluate (00316BC1) before the store (00316BCC).
 K6  the award tail with no manager: a completed achievement sets its bit in the award bitmap (00316061 bts, 00316069 store) and
     then calls 008632B0, which reads the null manager through 0020CE00 and returns - no Steam import is reached. The award is
     recorded in the save even though Steam is never told.
 B   the manager builder's boundary, measured: callbacks 1101, 1102 and 1103 registered, then SteamInternal_ContextInit.
Note: 003165C0 returns 0 for every id in this world (its inputs are runtime tables left zero), so mode 0's threshold falls back
to the descriptor's +4, which is 0; any counter completes. K6 uses that; no case claims a real threshold.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

import pefile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C                                     # block 332 (its cases run first, unchanged)
os.chdir(cwd)
W, uc, S = C.W, C.uc, C.S
UPD, READ, EVAL, STORE, FIRE, AWARD, MGR, BUILD = 0x316A50, 0x3166F0, 0x315E90, 0x316BF0, 0x3165C0, 0x8632B0, 0x20CE00, 0x20CD30
for f in (UPD, READ, EVAL, STORE, FIRE, AWARD, BUILD):
    W.ALLOWED |= W.closure(f) | {f}
W.ALLOWED |= {0x253970, 0x249840, 0x2EF640}
BIND_STOP = 0x253997
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=BIND_STOP, end=BIND_STOP)
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
pe = pefile.PE(W.EXE if hasattr(W, "EXE") else os.path.join(W.GRAPH, "..", "exe", "FFXII_TZA.exe"))
IAT = {(imp.name or b"").decode(): imp.address for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
STEAM = [n for n in IAT if n.startswith("Steam")]
order, steam, regs, writes = [], [], [], []
for a, nm in ((EVAL, "evaluate"), (STORE, "store"), (AWARD, "award"), (MGR, "manager getter"), (0x20CE60, "send")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: order.append(nm))(nm), begin=a, end=a)
for nm in STEAM:
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: steam.append(nm))(nm), begin=q(IAT[nm]), end=q(IAT[nm]))
W.OSRET["SteamAPI_RegisterCallback"] = 0                   # case B only: the registration is recorded and returns (void)
W.BRIDGED.add("SteamAPI_RegisterCallback")
reg_trap = q(IAT["SteamAPI_RegisterCallback"])
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: regs.append(u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF), begin=reg_trap, end=reg_trap)
uc.ctl_flush_tb()

C.reset()
S.call(0x253970)
bound = uc.reg_read(UC_X86_REG_RIP) == BIND_STOP and not S.st["faults"]
IB = q(0x20927C0)
STATE = IB + 0x3844
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: writes.append(["+%X" % (a - IB), n, "%08X" % u.reg_read(UC_X86_REG_RIP)]),
            begin=STATE, end=STATE + 0x27)
uc.ctl_flush_tb()
desc = {i: bytes(uc.mem_read(0xD10460 + 8 * i, 8)) for i in range(30)}
counter = lambda i: struct.unpack("<i" if desc[i][0] == 4 else "<h", bytes(uc.mem_read(IB + 0x384C + desc[i][1], desc[i][0])))[0]


def run(fnc, *a):
    del order[:], writes[:], steam[:]
    ok = S.call(fnc, *a)
    return ok and not S.st["bad"] and not S.st["faults"], uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def reset_state():
    uc.mem_write(STATE, bytes(0x28))


R = {"bound": bound, "image_block": "%X" % IB, "manager_cell": "%X" % q(0x1F83450)}
k1 = {}
for i in (6, 7, 11, 17):
    reset_state()
    a = run(STORE, i, 0x7FFFFFF0)[0]
    b = run(UPD, i, 0x100)[0]
    sat = counter(i)
    reset_state()
    run(STORE, i, 100)
    run(UPD, i, 5)
    k1[i] = {"ok": a and b, "kind": desc[i][0], "saturated": "%X" % (sat & 0xFFFFFFFF), "exact": counter(i)}
R["K1"] = k1
reset_state()
run(STORE, 1, 0x1234)
run(STORE, 0, 0x7FF0)
ok2 = run(UPD, 0, 0x100)[0]
R["K2"] = {"ok": ok2, "id0": "%X" % (counter(0) & 0xFFFF), "id1_neighbour": "%X" % (counter(1) & 0xFFFF)}
reset_state()
run(STORE, 0, 0x55)
w0 = list(writes)
run(STORE, 6, 0x66)
w6 = list(writes)
R["K3"] = {"store_id0": w0, "store_id6": w6}
k4 = {}
for bad in (30, 31, 255):
    reset_state()
    before = bytes(uc.mem_read(STATE, 0x28))
    rd = run(READ, bad)
    sw = run(STORE, bad, 0x1234)
    sww = list(writes)
    up = run(UPD, bad, 5)
    k4[bad] = {"read": "%X" % rd[1], "read_ok": rd[0], "store_writes": sww, "update_calls": list(order), "update_writes": list(writes),
               "unchanged": bytes(uc.mem_read(STATE, 0x28)) == before, "ok": sw[0] and up[0]}
R["K4"] = k4
reset_state()
ok5 = run(UPD, 1, 1)[0]
R["K5_K6"] = {"ok": ok5, "calls": list(order), "writes": list(writes), "steam_imports": list(steam),
              "bitmap": bytes(uc.mem_read(STATE, 4)).hex(), "manager_cell": "%X" % q(0x1F83450)}
del regs[:]
okb = run(BUILD)[0]
R["B"] = {"completed": okb, "halt": S.st["bad"][:1], "registered_callback_ids": list(regs), "manager_cell": "%X" % q(0x1F83450)}

k56 = R["K5_K6"]
cases = {
    "K1_kind4_saturates_on_every_kind4_id": all(v["ok"] and v["kind"] == 4 and v["saturated"] == "7FFFFFFF" and v["exact"] == 105 for v in k1.values()),
    "K2_kind2_saturates_and_leaves_the_neighbour": ok2 and R["K2"]["id0"] == "7FFF" and R["K2"]["id1_neighbour"] == "1234",
    "K3_store_writes_kind_bytes_at_block_plus_384C_plus_offset": [x[:2] for x in w0] == [["+384C", 2]] and [x[:2] for x in w6] == [["+3860", 4]],
    "K4_ids_30_31_255_rejected_by_read_store_and_update": all(v["ok"] and v["read_ok"] and v["read"] == "FFFFFFFF" and v["store_writes"] == []
                                                               and v["update_calls"] == [] and v["update_writes"] == [] and v["unchanged"] for v in k4.values()),
    "K5_update_evaluates_before_it_stores": ok5 and k56["calls"].index("evaluate") < k56["calls"].index("store"),
    "K6_award_bit_set_then_null_manager_returns_no_steam_call": ok5 and k56["bitmap"] == "02000000"
        and [w[2] for w in k56["writes"]][:1] == ["00316069"] and k56["calls"][:4] == ["evaluate", "award", "manager getter", "store"]
        and "send" not in k56["calls"] and k56["steam_imports"] == [] and k56["manager_cell"] == "0",
    "B_manager_builder_registers_1101_1102_1103_then_needs_the_steam_interface": not okb and R["B"]["registered_callback_ids"] == [1101, 1102, 1103]
        and R["B"]["halt"] == ["import SteamInternal_ContextInit"] and R["B"]["manager_cell"] == "0",
    "world_bound_by_the_shipped_binder": bound and IB == 0x2164280 + 0x8200,
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-74s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("K1", "K2", "K3", "K5_K6", "B")})[:2500])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
