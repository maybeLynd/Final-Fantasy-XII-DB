"""S-45 I-1 (OPUS, 2026-09-26): CONTRACT-steam-integration-subsystem's I-1 failure half - "if SteamAPI_Init fails, [01F83450]
stays null and every by-index award returns at the null check" - executed through the shipped start-up 007980A0 under a
disclosed FAILING Steam-library model.

World: block 332's (s21-opus-replay-applier-stub-free/check.py, imported; its cases run first, unchanged). The start-up 007980A0
runs from its entry as a PREFIX that stops at 00798152, the first instruction after the Steam block (00798116-0079814B).
Models (disclosed, by name at each import's trap): SetUnhandledExceptionFilter -> 0 (no previous filter); ImmDisableIME -> TRUE;
CoInitializeEx -> S_OK; THE STEAM LIBRARY, as it answers when the Steam client is not running: SteamInternal_ContextInit returns
a context whose interfaces are all null, SteamAPI_Init returns false; SteamAPI_RestartAppIfNecessary(595520) returns the case's
value; exit is recorded and stops the run. The by-index award thunk 008632B0 is then called for every entry.
Cases:
 F1  SteamAPI_Init false, RestartAppIfNecessary false: the manager builder 0020CD30 is not entered, [01F83450] stays 0, and the
     prefix reaches 00798152 - start-up continues with achievements off.
 F2  every by-index award 008632B0(0..40) in that world returns at 0020CE00's null manager: 0020CE60 is never entered and no
     Steam import is called.
 F3  SteamAPI_Init false, RestartAppIfNecessary true: exit(1) is called at 0079814B (the process ends before any manager).
 C1  control: SteamAPI_Init true (context still empty): the builder 0020CD30 is entered from 0079812D (stopped at its entry).
 S1  static: 0079811C tests the context's +0x18 before SteamAPI_Init; 0079812B `je 00798137` skips the builder on false; the
     award thunk's null test.
Evidence class NATIVE-REPLAY (unicorn) against a failing Steam-library model, live_game false. Writes i1_result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

import capstone
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C                                     # block 332 (its cases run first, unchanged)
os.chdir(cwd)
W, uc, S = C.W, C.uc, C.S
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
START, END, BUILDER, AWARD, AWARD_BODY, MGRCELL = 0x7980A0, 0x798152, 0x20CD30, 0x8632B0, 0x20CE60, 0x1F83450
for f in (START, BUILDER, AWARD):
    W.ALLOWED |= W.closure(f) | {f}
IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
CTX = 0x7B500000
uc.mem_map(CTX, 0x1000)
uc.mem_write(CTX, bytes(0x1000))
case = {"init": 0, "restart": 0}
calls = []


def model(nm):
    def on(u, a, n, _):
        calls.append(nm)
        if nm == "SteamInternal_ContextInit":
            r = CTX
        elif nm == "SteamAPI_Init":
            r = case["init"]
        elif nm == "SteamAPI_RestartAppIfNecessary":
            calls[-1] = (nm, "%X" % (u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
            r = case["restart"]
        elif nm == "exit":
            calls[-1] = (nm, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF)
            u.emu_stop()
            return
        elif nm == "SetUnhandledExceptionFilter":
            r = 0
        else:                                             # ImmDisableIME -> TRUE, CoInitializeEx -> S_OK
            r = 1 if nm == "ImmDisableIME" else 0
        u.reg_write(UC_X86_REG_RAX, r)
    return on


for nm in ("SetUnhandledExceptionFilter", "ImmDisableIME", "CoInitializeEx", "SteamInternal_ContextInit", "SteamAPI_Init",
           "SteamAPI_RestartAppIfNecessary", "exit"):
    W.OSRET[nm] = 0
    W.BRIDGED.add(nm)
    uc.hook_add(UC_HOOK_CODE, model(nm), begin=q(IAT[nm]), end=q(IAT[nm]))
entered = []
for a, nm in ((BUILDER, "builder_0020CD30"), (AWARD_BODY, "award_body_0020CE60"), (END, "after_steam_block_00798152")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, x, n, _: entered.append(nm))(nm), begin=a, end=a)
stops = {}


def stop_at(a):
    stops[a] = uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: u.emu_stop(), begin=a, end=a)


uc.ctl_flush_tb()


def run(init, restart, stop):
    case.update(init=init, restart=restart)
    del calls[:], entered[:]
    uc.mem_write(MGRCELL, bytes(8))
    stop_at(stop)
    S.call(START)
    uc.hook_del(stops.pop(stop))
    return {"stopped_at": "%X" % uc.reg_read(UC_X86_REG_RIP), "calls": [c if isinstance(c, str) else list(c) for c in calls],
            "entered": list(entered), "manager": "%X" % q(MGRCELL)}


R = {}
R["F1"] = run(0, 0, END)
awards = []
for k in range(41):
    del calls[:], entered[:]
    ok = S.call(AWARD, k)
    awards.append({"k": k, "ok": ok, "entered": list(entered), "steam_calls": list(calls)})
R["F2"] = {"all_return": all(a["ok"] for a in awards), "body_entered": [a["k"] for a in awards if a["entered"]],
           "steam_calls": sum(len(a["steam_calls"]) for a in awards), "manager": "%X" % q(MGRCELL)}
R["F3"] = run(0, 1, END)
R["C1"] = run(1, 0, BUILDER)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
ins = lambda a: (lambda i: "%s %s" % (i.mnemonic, i.op_str))(next(md.disasm(bytes(uc.mem_read(a, 16)), a, count=1)))
R["S1"] = [ins(a) for a in (0x79811C, 0x798121, 0x798123, 0x798129, 0x79812B, 0x79812D, 0x20CE00, 0x8632B0)]
cases = {
    "F1_init_fails_no_manager_startup_continues": R["F1"]["stopped_at"] == "798152" and R["F1"]["manager"] == "0"
        and "builder_0020CD30" not in R["F1"]["entered"] and "after_steam_block_00798152" in R["F1"]["entered"]
        and [c if isinstance(c, str) else c[0] for c in R["F1"]["calls"]] == ["SetUnhandledExceptionFilter", "ImmDisableIME",
            "CoInitializeEx", "SteamInternal_ContextInit", "SteamAPI_Init", "SteamAPI_RestartAppIfNecessary"]
        and R["F1"]["calls"][-1] == ["SteamAPI_RestartAppIfNecessary", "91640"],
    "F2_every_award_returns_at_the_null_manager": R["F2"]["all_return"] and R["F2"]["body_entered"] == [] and R["F2"]["steam_calls"] == 0
        and R["F2"]["manager"] == "0",
    "F3_restart_true_exits_1_before_any_manager": R["F3"]["calls"][-1] == ["exit", 1] and R["F3"]["manager"] == "0"
        and "builder_0020CD30" not in R["F3"]["entered"],
    "C1_control_init_true_enters_the_builder": R["C1"]["stopped_at"] == "20CD30" and "builder_0020CD30" in R["C1"]["entered"]
        and [c if isinstance(c, str) else c[0] for c in R["C1"]["calls"]][-1] == "SteamAPI_Init",
    "S1_the_branches": R["S1"][0] == "cmp qword ptr [rax + 0x18], 0" and R["S1"][4] == "je 0x798137" and R["S1"][5] == "call 0x20cd30",
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "i1_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-58s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("F1", "F3", "C1", "S1")}, default=str)[:1800])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
