"""S-15 (OPUS, 2026-09-26): the field pass's other arms - the +0x12 == 0 branch (audio 00261F90, then the init core 002620E0 from
a SECOND call site), and the slot-0 deferred request 0032FC30 up to its resource boundary.

Runs check.py's world and cases (executed first from its own source, unchanged; its result.json is not rewritten - the source's
final dump is redirected), then:
STATIC (from the image):
 T1  the pass 0025D9E0 calls 002620E0 at TWO sites: 0025DB7D (exit A, after 0025DB79 publishes +0x12) and 0025DC27. The second is
     on the branch 0025DB25 cmp byte [rbx+0x12], dil / 0025DB29 je 0025DB87, i.e. +0x12 == 0: 0025DB8E calls 00261F90, and
     0025DC10..0025DC27 call the init core when +0x17 < 0x80 and +0x10 bit 5 is clear. 00261F90 has one call site, 0025DB8E.
NATIVE-REPLAY (the S-13 world's five real records, as check.py):
 F1  slot 1, +0x10 = 0x81, +0x12 = 0: 00261F90 runs as shipped, then the init core runs, called from 0025DC27 (return address
     0025DC2C), then the resolver drives all five records, the counters go to 1 and the pass returns.
 F2  control, +0x12 = 1 (check.py's drive case): neither 00261F90 nor the init core runs; one record is driven.
 F3  the deferred arm, measured to its boundary: slot 0, +0x10 = 0x81 with bits 3/4 clear, and the ready word [02ADD0D8] = 1
     (planted; its writers are the map binder 003775D0 and 00377CC0 / 00378230). WorldSimulation_ProcessDeferredModeRequest
     0032FC30 is entered with (1, 0xD4) and does not return: after the resource-path lookup (002DF960, reached through a tail jump
     and admitted) and the main-thread check (00368ED0's own store of GetCurrentThread() at 00368EE1, run as its prefix; the import
     bridged by name to the pseudo-handle -2), the area-resource loop 003E9780 is entered and the run ends on the instruction
     budget (the last function recorded varies with where the budget falls inside the loop's callees). +0x10 bit 3
     (0025DAF2, after the call) is not set. Recorded boundary: the resource pipeline.
Evidence classes STATIC (T1) and NATIVE-REPLAY (F1-F3), live_game false. Writes arms_result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "check.py"), encoding="utf-8").read()
src = src.replace('sys.exit(0 if res["ok"] else 1)', "pass")
src = src.replace('open(os.path.join(HERE, "result.json"), "w")', "io.StringIO()")   # check.py's own result stays as published
g = {"__file__": os.path.join(HERE, "check.py"), "__name__": "s15check", "io": io}
cwd = os.getcwd(); os.chdir(HERE); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "check.py", "exec"), g)
os.chdir(cwd)
base_ok = g["res"]["ok"]
run, uc, S, W = g["run"], g["uc"], g["S"], g["W"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP

md = Cs(CS_ARCH_X86, CS_MODE_64)
body = list(md.disasm(bytes(uc.mem_read(0x25D9E0, 1297)), 0x25D9E0))
T = {"init_core_sites": ["%08X" % i.address for i in body if i.mnemonic == "call" and i.op_str == "0x2620e0"],
     "audio_sites": ["%08X" % i.address for i in body if i.mnemonic == "call" and i.op_str == "0x261f90"],
     "branch": ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in body if i.address in (0x25DB25, 0x25DB29, 0x25DB79, 0x25DC10, 0x25DC14, 0x25DC1A, 0x25DC1E)]}
ev = []
for a, nm in ((0x261F90, "audio"), (0x2620E0, "init_core"), (0x32FC30, "deferred"), (0x3E9780, "area_resource_loop")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: ev.append([nm, "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF),
                                                                        "%08X" % struct.unpack("<Q", bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP), 8)))[0]]))(nm),
                begin=a, end=a)
uc.ctl_flush_tb()


def names(x):
    return [e[0] for e in x]


del ev[:]
f1 = run(1, b10=0x81, b13=1, b12=0)
f1_ev = list(ev)
del ev[:]
f2 = run(1, b10=0x81, b13=1, b12=1)
f2_ev = list(ev)
# F3: the deferred arm, to its boundary
W.ALLOWED |= W.closure(0x32FC30) | {0x32FC30, 0x2DF960} | W.closure(0x2DF960) | {0x368ED0, 0x862090}
W.OSRET["GetCurrentThread"] = 0xFFFFFFFFFFFFFFFE
W.BRIDGED.add("GetCurrentThread")
h = uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=0x368EE7, end=0x368EE7)
uc.ctl_flush_tb()
S.call(0x368ED0)
uc.hook_del(h)
main_thread = struct.unpack("<I", bytes(uc.mem_read(0x22D7FB0, 4)))[0]
uc.mem_write(0x2ADD0D8, struct.pack("<I", 1))
uc.ctl_flush_tb()
del ev[:]
f3 = run(0, count=3000000, b10=0x81, b13=1, b12=1)
f3_ev = list(ev)
trace = list(S.st["trace"])
f3_last = "%08X" % max(f for f in W.FSTARTS if f <= trace[-1]) if trace else None
R = {"static": T, "base_check_ok": base_ok, "F1": dict(f1, events=f1_ev), "F2": dict(f2, events=f2_ev),
     "F3": dict(f3, events=f3_ev, last_function=f3_last, main_thread_store="%X" % main_thread)}
cases = {
    "T1_two_init_core_call_sites_one_audio_site": T["init_core_sites"] == ["0025DB7D", "0025DC27"] and T["audio_sites"] == ["0025DB8E"],
    "F1_plus12_zero_audio_then_init_core_from_0025DC27_no_drive_loop": base_ok and f1["ok"] and names(f1_ev) == ["audio", "init_core"]
        and f1_ev[1][3] == "0025DC2C" and f1["drives"] == 5 and f1["d24"] == 1 and f1["d38"] == 1,
    "F2_control_plus12_one_no_audio_no_init_core": f2["ok"] and names(f2_ev) == [] and f2["drives"] == 1,
    "F3_deferred_arm_entered_1_D4_boundary_resource_pipeline": names(f3_ev)[:2] == ["deferred", "area_resource_loop"] and f3_ev[0][1:3] == ["1", "D4"]
        and not f3["ok"] and not f3["bad"] and not f3["faults"] and (f3["b10"] & 8) == 0 and main_thread == 0xFFFFFFFE,
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "arms_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-70s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({"T": T, "F1": f1_ev, "F2": f2_ev, "F3": f3_ev, "F3_last": f3_last}))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
