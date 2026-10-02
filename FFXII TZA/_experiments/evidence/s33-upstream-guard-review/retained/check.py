"""S-33 (OPUS, 2026-09-26): CONTRACT-world-loot-pickup-pool's create executed with presentation op 1 (003FA160) REAL - the one
leaf EXP-141 scripted - over the pickup visual sub-object and the HUD sprite records built by shipped code.

World: block 332's (s21-opus-replay-applier-stub-free/check.py, imported; its cases run first, unchanged). Its HUD manager
[0209BE80] is a zero block (the world's convention for idle objects), which is what the HUD constructor 00291750 leaves after its
own memset (00291765); on it:
 - the pickup visual sub-object mgr+0x57E0 is initialised by its shipped initialiser 003FA760, the call 00291750 makes at 002917C9;
 - the ten HUD sprite records of the registry 0208F580 are registered by the shipped registrar 00280750, run as a PREFIX that stops
   at 0028083B, before its file request 00249180 (the loader's I/O is not emulated);
 - the two records op 1 looks up, partytop_8_c and partytop_4_c (00280750's records 6 and 5), are bound by the shipped binder
   0024A1D0 from the SHIPPED bundle the request names - file (7, 0xD7), which the path installer 002DF9A0 resolves to
   PS2Data/image/FF12/myoshiok/in_sdver/PackFiles/tex2pack_ys.bin - with the offsets the completion 00280670 uses
   ([bundle + 4k]). Each binder run is a PREFIX that stops at 0024A25E, its first render-layer call (00181520, the texture
   manager on [01F811E8]); the record's sprite header (+0x18 / +0x20) and format bits are stored before it. The GS TEX0 word
   (+0x30) is laid out later by 0024A710 through the GS command buffers, so it is 0 here: op 1's UV floats (sub-object +0x25F4..,
   +0x2654..) are computed with a 1x1 texture. Those are presentation values; no case reads them.
The pool is initialised by its shipped INIT 00319B10; every create is the shipped CREATE 00319CA0 with a 56-byte drop buffer
(item 0x0101 x1, the rest 0xFFFF) and position (5, 6, 7); the dispatcher 0028F000 and op 1 run as shipped. No application stub.
Cases:
 R1  the world: 003FA760 leaves +0x249A = 0xFFFF on the zeroed sub-object; the ten names are registered in 00280750's order;
     partytop_4_c / partytop_8_c get +0x18 = bundle + offset, +0x20 = +0x18 + 0x10.
 R2  the first create runs op 1 for real: 0028F000(0, 1, payload) -> 003FA160(mgr+0x57E0, payload, tier, table value); op 1 fills
     its sprite cache once (+0x2690 = partytop_8_c's record, +0x2698 = partytop_4_c's), takes visual slot 0 (sub+0x270), sets its
     flag +0x272 bit 0, phase +0x260 = 1, +0x264 = -0.25f, +0x268 = the tier, +0x26C = the table value, makes it the list head
     (+0x2490) and requests sound 0x50 (00249C60). It returns the slot's address, and CREATE stores its LOW 32 BITS at node +0x58
     (00319E05 `mov [rbx+0x58], eax`) - the handle is a truncated pointer to the visual slot.
 R3  later creates take slots 1, 2, ... in order, appended at the list tail (+0x278 / +0x280 links); the record lookups do not recur.
 R4  the handle resolves: the shipped TICK 00319600 looks each state-1 node up through 0028EFE0 -> 003FA730(mgr+0x57E0, handle),
     which finds the slot on the list and returns its phase (1); no node changes state.
 R5  an eviction retires the head's visual through 003FA820(handle, 0), which sets its flag bit 1 and keeps bit 0: the slot stays
     occupied. With ten nodes and thirteen slots, the 14th create (the 4th eviction) finds every slot occupied and op 1 returns
     0; CREATE stores handle 0 - the case EXP-141 had to script (c-op1ret0), here reached by shipped code.
 R6  bounded finding: TICK then looks up handle 0, and 003FA730 reads +0x272 of a null object (`test byte [rdx+0x272],1` at
     003FA730, no null test) - a fault at address 0x272. Whether thirteen visuals can be occupied at once in the game depends on
     how fast a retired visual is freed, which runs in the per-frame visual update and is not run here (live question, routed).
 R7  how long a retired visual holds its slot: the per-frame visual update 003FA790 (called by the HUD update 0028E290) frees
     the five retired slots together on its 51st call here (visuals retired without any update since creation), and no live
     slot. The C runtime's _isnan / _finite are bridged by name for it.
 S1  static, byte-verified: 00319E05 stores eax (32 bits) at +0x58; 003FA730's first instruction is the unguarded +0x272 test;
     the manager is allocated by 0028F8B0 through 00271420(0x10FD0), which selects arena 3 (0036C1D0 with ecx = 0xF - 0xC) -
     the arena boot backs with 0036D240(0xD20100) = the CRT malloc (0022A1E6 / 0022A2C0..0022A2CB). So the < 4 GB requirement
     of UQ-137 is a requirement on where the CRT places that 13 MiB boot block.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

import capstone
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
# THE UPSTREAM'S VERDICT GATES THIS REPLAY (2026-10-01, OPUS, on ASTRA-REQ-OPUS-S33-UPSTREAM-VERDICT-GUARD-1001):
# the import used to be trusted, so an upstream that printed FAIL still let every case below run and pass.
# An import exception or any verdict other than allok True with every case passing refuses, exit 2, no result.
# The retained result.json predates this guard (its upstream was ok, four rows); see test_upstream_guard.py.
sys.path.append(HERE)                                     # appended: BASE must stay first, or `import check` finds this file
import upstream_guard                                     # noqa: E402
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import check as C                                 # block 332 (its cases run first, unchanged)
except Exception as e:                                    # noqa: BLE001 - any failure of the upstream refuses
    print("REFUSED: upstream check raised %s: %s" % (e.__class__.__name__, e))
    sys.exit(2)
finally:
    os.chdir(cwd)
_ok, _why = upstream_guard.verdict(C)
if not _ok:
    print("REFUSED: %s" % _why)
    sys.exit(2)

W, uc, S = C.W, C.uc, C.S
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
w2 = lambda a: struct.unpack("<H", bytes(uc.mem_read(a, 2)))[0]
f4 = lambda a: struct.unpack("<f", bytes(uc.mem_read(a, 4)))[0]
BUNDLE_PATH = os.path.join("D:" + os.sep, "FFXII_TZA_extract", "ps2data", "image", "ff12", "myoshiok", "in_sdver", "packfiles", "tex2pack_ys.bin")

SUBINIT, REGISTER, BINDER, CREATE, INIT, TICK = 0x3FA760, 0x280750, 0x24A1D0, 0x319CA0, 0x319B10, 0x319600
for f in (SUBINIT, REGISTER, BINDER, CREATE, INIT, TICK):
    W.ALLOWED |= W.closure(f) | {f}
POOL, TAIL, CLOCK, HUDCELL, MGRCELL, REG = 0x2EC0FA0, 0x2EC1368, 0x208D45C, 0x209AC30, 0x209BE80, 0x208F580
ev = []
WATCH = {0x3FA160: "op1", 0x249C60: "sound", 0x3FA730: "lookup", 0x3FA820: "retire", 0x24A5A0: "record_lookup", 0x181520: "render"}


def on_watch(u, a, n, _):
    ev.append([WATCH[a], "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % u.reg_read(UC_X86_REG_RDX), "%X" % (u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF),
               "%X" % (u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF)])


for a in WATCH:
    uc.hook_add(UC_HOOK_CODE, on_watch, begin=a, end=a)
op1_ret = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: op1_ret.append("%X" % u.reg_read(UC_X86_REG_RAX)), begin=0x319E05, end=0x319E05)
lookup_ret = []
for a in (0x3FA756, 0x3FA759):                             # the lookup's two returns (0 / the phase)
    uc.hook_add(UC_HOOK_CODE, (lambda a: lambda u, x, n, _: lookup_ret.append(["miss" if a == 0x3FA756 else "hit", "%X" % u.reg_read(UC_X86_REG_RDX)]))(a),
                begin=a, end=a)
uc.ctl_flush_tb()


def halt():
    tr = list(S.st["trace"])
    return {"halt": (S.st["bad"] or S.st["faults"])[:2], "last_pc": "%X" % tr[-1] if tr else None}


R = {}
# ---- world ----
MGR = q(MGRCELL)
SUB = MGR + 0x57E0
zero_before = not any(bytes(uc.mem_read(MGR, 0x10FD0)))
ok_sub = S.call(SUBINIT, SUB)
R["R1"] = {"mgr": "%X" % MGR, "mgr_zero_block": zero_before, "subinit_ok": ok_sub, "plus_249A": "%X" % w2(SUB + 0x249A)}
stop = uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=0x28083B, end=0x28083B)
S.call(REGISTER, 0)
R["R1"]["register_stopped_at"] = "%X" % uc.reg_read(UC_X86_REG_RIP)
uc.hook_del(stop)
HUD = q(HUDCELL)
recs = [q(HUD + 0x338 + 8 * k) for k in range(10)]
names = [bytes(uc.mem_read(r, 16)).split(b"\0")[0].decode() for r in recs]
R["R1"]["records"] = names
R["R1"]["records_in_registry"] = all(r == REG + 0x48 * k for k, r in enumerate(recs))
data = open(BUNDLE_PATH, "rb").read()
import hashlib
R["R1"]["bundle_sha256"] = hashlib.sha256(data).hexdigest()
BUF = 0x7D000000
uc.mem_map(BUF, (len(data) + 0xFFFF) & ~0xFFFF)
uc.mem_write(BUF, data)
stopb = uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=0x24A25E, end=0x24A25E)
binds = {}
for k in (5, 6):
    off = struct.unpack_from("<I", data, 4 * k)[0]
    del ev[:]
    S.call(BINDER, recs[k], BUF + off)
    r = recs[k]
    binds[names[k]] = {"stopped_at": "%X" % uc.reg_read(UC_X86_REG_RIP), "offset": "%X" % off, "plus_18": "%X" % (q(r + 0x18) - BUF),
                       "plus_20": "%X" % (q(r + 0x20) - BUF), "plus_30": "%X" % q(r + 0x30), "flags": "%X" % d4(r + 0x38),
                       "render_entered": any(e[0] == "render" for e in ev)}
uc.hook_del(stopb)
R["R1"]["binds"] = binds
ok_init = S.call(INIT)
R["R1"]["pool_init_ok"] = ok_init
DROP, POS = 0x7C100000, 0x7C100100
uc.mem_map(0x7C100000, 0x1000)
uc.mem_write(DROP, (struct.pack("<HH", 0x0101, 1) + struct.pack("<HH", 0xFFFF, 0) * 6).ljust(56, b"\0"))
uc.mem_write(POS, struct.pack("<3f", 5.0, 6.0, 7.0))


def slot(k):
    return SUB + 0x270 + 0x2A0 * k


def occupied():
    return [k for k in range(13) if w2(slot(k) + 0x272) & 1]


def create():
    del ev[:], op1_ret[:]
    ok = S.call(CREATE, DROP, POS)
    return {"ok": ok, "events": [e for e in ev], "op1_return": op1_ret[-1] if op1_ret else None, "occupied": occupied(),
            "handles": ["%X" % d4(POOL + 0x60 * j + 0x58) for j in range(10)]}


creates = [create() for _ in range(3)]
s0 = slot(0)
R["R2"] = {"create": creates[0], "cache_2690": "%X" % q(SUB + 0x2690), "cache_2698": "%X" % q(SUB + 0x2698),
           "slot0": {"flag": "%X" % w2(s0 + 0x272), "phase": d4(s0 + 0x260), "f264": f4(s0 + 0x264), "tier": d4(s0 + 0x268), "table": d4(s0 + 0x26C)},
           "list_head": "%X" % q(SUB + 0x2490), "node0_handle": "%X" % d4(POOL + 0x58)}
R["R3"] = {"creates": creates[1:], "links": [["%X" % q(slot(k) + 0x278), "%X" % q(slot(k) + 0x280)] for k in range(3)]}
# R4: the handles resolve through the shipped tick
del ev[:], lookup_ret[:]
uc.mem_write(CLOCK, struct.pack("<I", 100))
ok_tick = S.call(TICK)
R["R4"] = {"ok": ok_tick, "lookups": list(lookup_ret), "states": [d4(POOL + 0x60 * j + 4) & 0xFF for j in range(3)]}
# R5: fill the pool, then evict until op 1 runs out of visual slots
more = [create() for _ in range(12)]                      # creates 4..15
R["R5"] = {"creates": [{"n": i + 4, "op1_return": c["op1_return"], "occupied": len(c["occupied"]),
                        "retired": [e[1] for e in c["events"] if e[0] == "retire"]} for i, c in enumerate(more)]}
first_zero = next((i + 4 for i, c in enumerate(more) if c["op1_return"] == "0"), None)
R["R5"]["first_zero_handle_create"] = first_zero
R["R5"]["retired_slots_flags"] = ["%X" % w2(slot(k) + 0x272) for k in range(4)]
# R6: the tick after a zero handle
del ev[:], lookup_ret[:]
ok6 = S.call(TICK)
R["R6"] = {"ok": ok6, **halt(), "zero_handle_nodes": [j for j in range(10) if d4(POOL + 0x60 * j + 0x58) == 0 and d4(POOL + 0x60 * j + 4) & 0xFF == 1],
           "last_lookup": ev[-1] if ev else None}

# R7: how long a retired visual keeps its slot - the per-frame visual update 003FA790 (the HUD update 0028E290's call), run
# until the retired slots free. It needs the C runtime's _isnan / _finite, bridged by name with their library semantics.
import math
import pefile
from unicorn.x86_const import UC_X86_REG_XMM0
_IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
for _nm, _f in (("_isnan", math.isnan), ("_finite", math.isfinite)):
    W.OSRET[_nm] = 0
    W.BRIDGED.add(_nm)
    uc.hook_add(UC_HOOK_CODE, (lambda f: lambda u, a, n, _: u.reg_write(UC_X86_REG_RAX, 1 if f(struct.unpack("<d", struct.pack(
        "<Q", u.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFFFFFFFFFF))[0]) else 0))(_f), begin=q(_IAT[_nm]), end=q(_IAT[_nm]))
UPDATE = 0x3FA790
W.ALLOWED |= W.closure(UPDATE) | {UPDATE}
uc.ctl_flush_tb()
retired = [k for k in range(13) if w2(slot(k) + 0x272) & 3 == 3]
live = [k for k in range(13) if w2(slot(k) + 0x272) & 3 == 1]
freed_at = {}
ok7 = True
for frame in range(1, 201):
    ok7 = S.call(UPDATE, SUB)
    if not ok7:
        break
    for k in range(13):
        if k not in freed_at and not w2(slot(k) + 0x272) & 1:
            freed_at[k] = frame
    if all(k in freed_at for k in retired):
        break
R["R7"] = {"ok": ok7, **halt(), "retired_slots": retired, "live_slots": live, "freed_at_update": {str(k): v for k, v in sorted(freed_at.items())},
           "list_after": "%X" % q(SUB + 0x2490)}

# ---- S1 static ----
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
ins = lambda a: (lambda i: "%s %s" % (i.mnemonic, i.op_str))(next(md.disasm(bytes(uc.mem_read(a, 16)), a, count=1)))
R["S1"] = {"store_58": ins(0x319E05), "lookup_first": ins(0x3FA730), "mgr_alloc": [ins(0x28F8CA), ins(0x28F8CF), ins(0x28F8D4)],
           "arena_select": [ins(0x271426), ins(0x27142D), ins(0x271430)], "boot_block": [ins(0x22A1E6), ins(0x22A1F2)],
           "boot_arena3": [ins(0x22A2C0), ins(0x22A2C6), ins(0x22A2CB)], "block_is_malloc": [ins(0x36D240), ins(0x36D249)]}

A = lambda k: slot(k)
c0 = creates[0]
cases = {
    "R1_world_built_by_shipped_code": R["R1"]["mgr_zero_block"] and ok_sub and R["R1"]["plus_249A"] == "FFFF"
        and R["R1"]["register_stopped_at"] == "28083B" and R["R1"]["records_in_registry"]
        and names[5] == "partytop_4_c" and names[6] == "partytop_8_c"
        and all(b["stopped_at"] == "24A25E" and int(b["plus_18"], 16) == int(b["offset"], 16) and int(b["plus_20"], 16) == int(b["offset"], 16) + 0x10
                and b["plus_30"] == "0" and not b["render_entered"] for b in binds.values()) and ok_init,
    "R2_op1_real_fills_slot0_and_the_handle_is_its_truncated_address": c0["ok"]
        and [e[0] for e in c0["events"]][:4] == ["op1", "record_lookup", "record_lookup", "sound"]
        and c0["events"][0][1] == "%X" % SUB and c0["op1_return"] == "%X" % A(0) and R["R2"]["node0_handle"] == "%X" % (A(0) & 0xFFFFFFFF)
        and R["R2"]["cache_2690"] == "%X" % recs[6] and R["R2"]["cache_2698"] == "%X" % recs[5]
        and R["R2"]["slot0"]["flag"] == "1" and R["R2"]["slot0"]["phase"] == 1 and R["R2"]["slot0"]["f264"] == -0.25
        and R["R2"]["list_head"] == "%X" % A(0) and c0["events"][3][1] == "50",
    "R3_later_creates_take_the_next_slot_at_the_list_tail": [c["op1_return"] for c in creates] == ["%X" % A(k) for k in range(3)]
        and all("record_lookup" not in [e[0] for e in c["events"]] for c in creates[1:])
        and R["R3"]["links"] == [["%X" % A(1), "0"], ["%X" % A(2), "%X" % A(0)], ["0", "%X" % A(1)]],
    "R4_tick_resolves_each_handle_to_its_slot": ok_tick and [l[0] for l in R["R4"]["lookups"]] == ["hit"] * 3
        and [l[1] for l in R["R4"]["lookups"]] == ["%X" % (A(k) & 0xFFFFFFFF) for k in range(3)] and R["R4"]["states"] == [1, 1, 1],
    "R5_retired_visuals_keep_their_slot_and_op1_runs_out_at_the_14th_create": first_zero == 14
        and [c["op1_return"] for c in more[:10]] == ["%X" % A(k) for k in range(3, 13)]
        and more[10]["op1_return"] == "0" and R["R5"]["creates"][10]["retired"] and all(int(f, 16) & 3 == 3 for f in R["R5"]["retired_slots_flags"]),
    "R6_zero_handle_faults_the_tick_lookup_bounded": not ok6 and R["R6"]["last_pc"] == "3FA730" and R["R6"]["halt"][:1] == ["00000272"]
        and R["R6"]["zero_handle_nodes"] != [],
    "R7_a_retired_visual_holds_its_slot_for_51_updates": ok7 and len(R["R7"]["retired_slots"]) >= 4
        and all(freed_at.get(k) == 51 for k in R["R7"]["retired_slots"]) and not any(k in freed_at for k in R["R7"]["live_slots"]),
    "S1_truncating_store_unguarded_lookup_and_the_managers_arena": R["S1"]["store_58"] == "mov dword ptr [rbx + 0x58], eax"
        and R["S1"]["lookup_first"] == "test byte ptr [rdx + 0x272], 1"
        and R["S1"]["mgr_alloc"] == ["mov ecx, 0x10fd0", "call 0x271420", "mov qword ptr [rip + 0x1e0c5a5], rax"]
        and R["S1"]["arena_select"] == ["mov edx, 0xf", "lea ecx, [rdx - 0xc]", "call 0x36c1d0"]
        and R["S1"]["boot_block"][0] == "mov ecx, 0xd20100" and R["S1"]["boot_arena3"] == ["mov r8d, 0xd20000", "mov ecx, 3", "call 0x369d30"]
        and R["S1"]["block_is_malloc"][1] == "jmp 0x85e730",
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("R1", "R2", "R4", "R6", "S1")}, default=str)[:2500])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
