"""S-36 (OPUS, 2026-09-26): R-4's arbiter half - where the input the arbiter 00253C70 would test against the latch at 00253FE3
comes from, executed from a shipped-code input stack, and the point where it stops.

World: block 332's (s21-opus-replay-applier-stub-free/check.py, imported; its cases run first, unchanged). Built by shipped code:
 - the CRT's stdio-options pre-C initialiser 00808D4C (entry of the pre-C table at 008C5690; block 332 runs only 00809124 of it),
   which sets the legacy wide-specifier bit the wide printf path needs;
 - the application object 01F7E350 by its C++ static initialiser 0015BC40 (C++ initialiser table entry 008C31F0) - it builds the
   input backend: [02EA5368] = the object, +0xDF8 = its device table (+0xE00). Block 332 plants [02EA5368] as a zero block; the
   cell is reset to its image value 0 first;
 - the mode object [01F81268] by its ensure-singleton 001C1940; the input manager [01F7FFE0] by its ensure-singleton 00198750
   (block 332's zero block reset to 0 first): keymap path built, keymap.ini absent, default bindings; the channel layer by
   003692D0 (boot 0022A3AD);
 - an XInput controller built exactly as the per-device body 00797690 builds one: 00584740(0x470), then 00792CB0(obj, descriptor,
   [02EA9500]); its base constructor registers it on the device list 01F401E8. The DirectInput descriptor is a model (0x244 bytes,
   dwSize, type 0x15 gamepad); DirectInput enumeration itself is not run.
Models (disclosed): os_model.py (a fresh install: folders, files, platform answers, Steam present but empty) and msvcp_wide.py
(msvcp140's wide stream members, fail-closed). THE PAD: XInputGetState(0) answers ERROR_SUCCESS with wButtons = 0x0010 (START)
and packet numbers 1, 2, ...; other user indices are not connected.
Each simulated frame runs, in this order: the backend's device update 007A3110 (the vtable method at 01CB2468/01CB2480), the
application frame 0079C140 on the application object, then the input frame InputControl_UpdateFrame 0035EC90; after the frames the
gameplay snapshot 002498B0 and then the arbiter 00253C70.
Cases:
 W1  the world is built: every builder above returns; [02EA5368] = 01F7E350 with +0xDF8 = +0xE00; the manager and the controller
     exist; the controller's vtable is 01CB2678 (XInputController_PollState at slot 5).
 I1  the stack runs every frame without a stop: the backend puts the controller in device-table slot 0 (0079AF20), the input
     frame polls it (InputManager -> InputSystem_UpdateRegisteredDevices -> 007A2140 -> XInputGetState(0)), and START is decoded
     into the controller's byte +0x445 (bit 4 at 007A2371).
 G1  the gate: every application frame calls its first-frame initialiser (vtable +0x48 = the game's override 0017D0C0, which
     stores the window size at 00189120()+0xAD8/+0xADC and tail-jumps to the framework's 007A05D0; call at 0079C1F1), which returns
     0x15 from 006278B0 - the renderer's back-buffer resize - so 0079C140 leaves at 0079C1F6 before counting the frame (+0x64 stays
     0) and before its per-code device update 0079D010 (never entered). The controller's per-code state (+0x30.., which the
     binding query 0079E650 reads) stays 0.
 G2  downstream it stays 0: the control state's pressure bytes are 0, channel 0's history marks all sixteen buttons present
     (0xFFFF) with pressure 0, and the snapshot leaves the arbiter's words 02F97368 / 02F9736A at 0.
 G3  the arbiter never reaches the latch test: run with the latch 02092734 = 0 and = 1, it returns 0 both times and 00253FE3 is not
     executed. (In this world it leaves even earlier, at 00253D19: 00265680, "every manager slot ready", is 0 without a field -
     disclosed; the input words would stop it at the button test 00253FB3 regardless.)
 S1  static, byte-verified: 0079D010's only caller is 0079C140 (0079C260), after the first-frame gate 0079C1E2..0079C1F6; the
     per-code writers of the input backend (00790000-007A4000) are 0079D010, the clears 0079AE40 / 0079AE90, the bank copy 007A0B50
     (from +0x130, which 0079D010's first loop writes), 0079A120 (from 00796490, the input script's "Frames" command) and
     00797EE0 / 00797F20 / 00797F60 (the input script's "KeyDown" / "KeyUp" / "Keypress"); the input-script commands are
     registered only on the runner 0079F150 creates when [02EA5220] is non-null, and [02EA5220] has exactly one reference image-wide
     (its read at 0079F1D0) - no writer, so the script facility is dead in this build. The snapshot's words have one producer,
     002498B0 (002284F0 only wipes the band).
Evidence class NATIVE-REPLAY (unicorn) with disclosed OS / pad / descriptor models, live_game false. Writes result.json.
"""
import collections
import contextlib
import io
import json
import os
import struct
import sys

import capstone
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
sys.path.insert(0, HERE)
import os_model
import msvcp_wide

W, uc, S = C.W, C.uc, C.S
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
w2 = lambda a: struct.unpack("<H", bytes(uc.mem_read(a, 2)))[0]

CRT_OPTS, APP_INIT, MODE_OBJ, IMGR, CHAN_INIT = 0x808D4C, 0x15BC40, 0x1C1940, 0x198750, 0x3692D0
ALLOC, XCTOR, BACKEND, APPFRAME, INFRAME, SNAP, ARB = 0x584740, 0x792CB0, 0x7A3110, 0x79C140, 0x35EC90, 0x2498B0, 0x253C70
APPCELL, IMGRCELL, OPTS, LATCH, W_HELD, W_EDGE = 0x2EA5368, 0x1F7FFE0, 0x2EBA3D0, 0x2092734, 0x2F97368, 0x2F9736A
# reached only indirectly (edges.tsv lacks them): the free thunk 0019C590; 00792D90 and 005DC1B0, passed by lea to constructor
# iterators (00792940, 005DC2F0); the controller vtable slots 00799F40 / 0079D670 / 007A2140; the thunk tail 001E09E0 (00862680);
# 0017D0C0 (a function pointer at 008C57A8)
INDIRECT = [0x19C590, 0x792D90, 0x5DC1B0, 0x799F40, 0x79D670, 0x7A2140, 0x1E09E0, 0x17D0C0]
for f in [CRT_OPTS, 0x809C50, APP_INIT, MODE_OBJ, IMGR, CHAN_INIT, ALLOC, XCTOR, BACKEND, APPFRAME, INFRAME, SNAP, ARB] + INDIRECT:
    W.ALLOWED |= W.closure(f) | {f}
LOG = []
IAT = os_model.install(W, uc, LOG)
msvcp_wide.install(W, uc, LOG)
pad = {"calls": 0}
W.OSRET["XInputGetState"] = 0
W.BRIDGED.add("XInputGetState")


def xinput(u, a, n, _):                                   # the pad model: user 0 connected, START held
    idx, p = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_RDX)
    if idx == 0:
        pad["calls"] += 1
        u.mem_write(p, struct.pack("<IHBBhhhh", pad["calls"], 0x0010, 0, 0, 0, 0, 0, 0))
        u.reg_write(UC_X86_REG_RAX, 0)
    else:
        u.reg_write(UC_X86_REG_RAX, 1167)                  # ERROR_DEVICE_NOT_CONNECTED


uc.hook_add(UC_HOOK_CODE, xinput, begin=q(IAT["XInputGetState"]), end=q(IAT["XInputGetState"]))
WATCH = {0x79D010: "percode_update", 0x7A05D0: "app_first_frame_init", 0x6278B0: "renderer_resize", 0x7A2140: "xinput_poll",
         0x79AF20: "table_resolve", 0x253FE3: "arbiter_latch_test", 0x254166: "arbiter_exit_00253D19", 0x253FB3: "arbiter_button_test"}
seen = []
for a in WATCH:
    uc.hook_add(UC_HOOK_CODE, (lambda a: lambda u, x, n, _: seen.append(WATCH[a]))(a), begin=a, end=a)
init_ret = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: init_ret.append("%X" % (u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)), begin=0x79C1F4, end=0x79C1F4)
resize_ret = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: resize_ret.append("%X" % (u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)), begin=0x7A0668, end=0x7A0668)
uc.ctl_flush_tb()


def halt():
    tr = list(S.st["trace"])
    return {"halt": (S.st["bad"] or S.st["faults"])[:2], "last_pc": "%X" % tr[-1] if tr else None}


R = {}
# ---- W1: the world ----
w1 = {}
w1["crt_options"] = S.call(CRT_OPTS)
w1["options_word"] = "%X" % q(OPTS)
w1["app_cell_planted"] = "%X" % q(APPCELL)
uc.mem_write(APPCELL, bytes(8))
w1["app_init"] = S.call(APP_INIT)
APP = q(APPCELL)
w1["app"], w1["app_df8"] = "%X" % APP, "%X" % q(APP + 0xDF8) if APP else None
w1["mode_obj"] = S.call(MODE_OBJ)
w1["imgr_cell_planted"] = "%X" % q(IMGRCELL)
uc.mem_write(IMGRCELL, bytes(8))
w1["imgr"] = S.call(IMGR)
w1["imgr_obj"] = "%X" % q(IMGRCELL)
w1["chan_init"] = S.call(CHAN_INIT)
w1["alloc"] = S.call(ALLOC, 0x470)
CTRL = uc.reg_read(UC_X86_REG_RAX)
DESC = 0x7C200000
uc.mem_map(DESC, 0x1000)
desc = bytearray(0x244); struct.pack_into("<I", desc, 0, 0x244); struct.pack_into("<I", desc, 0x24, 0x15)
uc.mem_write(DESC, bytes(desc))
w1["xctor"] = S.call(XCTOR, CTRL, DESC, d4(0x2EA9500))
w1["ctrl"], w1["ctrl_vtable"], w1["device_list_first"] = "%X" % CTRL, "%X" % q(CTRL), "%X" % (q(0x1F401E8) - 8)
w1["os_log"] = [x if isinstance(x, str) else list(x) for x in LOG]
R["W1"] = w1

# ---- the frames ----
CH0 = 0x22CAE90
frames = []
for k in range(4):
    del seen[:], init_ret[:], resize_ret[:]
    ok_b = S.call(BACKEND); hb = halt()
    ok_a = S.call(APPFRAME, APP); ha = halt()
    ok_f = S.call(INFRAME); hf = halt()
    frames.append({"backend_ok": ok_b, "app_ok": ok_a, "input_ok": ok_f, "halts": [hb, ha, hf], "seen": sorted(set(seen)),
                   "init_ret": list(init_ret), "resize_ret": list(resize_ret), "app_frame_counter": d4(APP + 0x64),
                   "slot0": "%X" % q(q(APP + 0xDF8) + 0x88), "decoded_445": uc.mem_read(CTRL + 0x445, 1)[0],
                   "percode": bytes(uc.mem_read(CTRL + 0x30, 0x11)).hex(), "xinput_calls": pad["calls"]})
R["frames"] = frames
R["control_state"] = bytes(uc.mem_read(0x22CB680, 0x30)).hex()
hist_idx = uc.mem_read(CH0, 1)[0] & 0xF
ent = CH0 + hist_idx * 0x24
R["history"] = {"index": hist_idx, "present_mask": "%X" % w2(ent + 0x46), "pressure": bytes(uc.mem_read(ent + 0x58, 0x10)).hex()}
ok_s = S.call(SNAP)
R["snapshot"] = {"ok": ok_s, "held": "%X" % w2(W_HELD), "edge": "%X" % w2(W_EDGE)}
arb = {}
for latch in (0, 1):
    uc.mem_write(LATCH, struct.pack("<I", latch))
    del seen[:]
    ok = S.call(ARB)
    arb[str(latch)] = {"ok": ok, "ret": "%X" % (uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF), "seen": sorted(set(seen))}
uc.mem_write(LATCH, bytes(4))
R["arbiter"] = arb

# ---- S1: static ----
EXE_IMG = pefile.PE(W.EXE, fast_load=True).get_memory_mapped_image()
IB = 0x120000
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
ins = lambda a: (lambda i: "%s %s" % (i.mnemonic, i.op_str))(next(md.disasm(EXE_IMG[a - IB:a - IB + 16], a, count=1)))
graph_callers = collections.defaultdict(set)
for line in open(os.path.join(W.GRAPH, "edges.tsv"), encoding="utf-8"):
    c = line.split("\t")
    if len(c) > 2 and c[2] == "false":
        graph_callers[c[1]].add(c[0])


def rip_refs(target):                                     # every rip-relative reference to target, image-wide (.text)
    out = []
    text = EXE_IMG[0x1000:0x1000 + 0x7A0635]
    for off in range(len(text) - 4):
        d = struct.unpack_from("<i", text, off)[0]
        for tail in (0, 1, 4):
            if IB + 0x1000 + off + 4 + tail + d == target:
                for back in range(2, 11):
                    s = off - back
                    i = next(md.disasm(text[s:s + 16], IB + 0x1000 + s, count=1), None)
                    if i and i.size == back + 4 + tail:
                        out.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
                        break
    return out


percode_writers = {}
import re
rx = re.compile(r"^mov byte ptr \[[a-z0-9]+ \+ [a-z0-9]+ \+ 0x30\]")
for line in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace"):
    c = line.rstrip("\n").split("\t")
    try:
        a = int(c[0], 16); sz = int(c[2])
    except (ValueError, IndexError):
        continue
    if not 0x790000 <= a < 0x7A4000:
        continue
    hits = ["%08X" % i.address for i in md.disasm(EXE_IMG[a - IB:a - IB + sz], a) if rx.search("%s %s" % (i.mnemonic, i.op_str))]
    if hits:
        percode_writers["%08X" % a] = {"stores": hits, "graph_callers": sorted(graph_callers.get("%08X" % a, []))}
R["S1"] = {"gate": [ins(a) for a in (0x79C1E2, 0x79C1E5, 0x79C1EB, 0x79C1F1, 0x79C1F4, 0x79C1F6, 0x79C21B, 0x79C260)],
           "percode_update_callers": sorted(graph_callers.get("0079D010", [])),
           "percode_writers_backend_range": percode_writers,
           "script_path_refs": rip_refs(0x2EA5220),
           "script_runner": [ins(a) for a in (0x79F1CF, 0x79F1DD, 0x79F1E0, 0x79F211, 0x79F21B)],
           "script_commands": {"796490": "Frames", "797EE0": "KeyDown", "797F20": "KeyUp", "797F60": "Keypress"},
           "renderer_call": [ins(a) for a in (0x7A0663, 0x7A0668, 0x7A066A, 0x7A066C)]}

# the snapshot band 02F97360..02F97398 (the arbiter's words 02F97368 / 02F9736A inside it): every instruction image-wide, decoded
# from its function's start, that stores to the band rip-relatively or takes its address with lea
mdd = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
mdd.detail = True
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
band = []
for line in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace"):
    c = line.rstrip("\n").split("\t")
    try:
        a = int(c[0], 16); sz = int(c[2])
    except (ValueError, IndexError):
        continue
    for i in mdd.disasm(EXE_IMG[a - IB:a - IB + sz], a):
        if not i.operands or i.operands[0].type != X86_OP_MEM and i.mnemonic != "lea":
            continue
        for k, op in enumerate(i.operands):
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = i.address + i.size + op.mem.disp
                if 0x2F97360 <= t < 0x2F97398 and (i.mnemonic == "lea" or (k == 0 and i.mnemonic not in ("cmp", "test"))):
                    band.append("%08X %s %s  (fn %08X)" % (i.address, i.mnemonic, i.op_str, a))
R["S1"]["band_stores_and_addresses"] = band

last = frames[-1]
cases = {
    "W1_world_built_by_shipped_code": all(w1[k] for k in ("crt_options", "app_init", "mode_obj", "imgr", "chan_init", "alloc", "xctor"))
        and w1["options_word"] == "4" and APP == 0x1F7E350 and q(APP + 0xDF8) == APP + 0xE00 and w1["ctrl_vtable"] == "1CB2678"
        and w1["imgr_obj"] != "0",
    "I1_stack_runs_and_start_is_decoded": all(f["backend_ok"] and f["app_ok"] and f["input_ok"] for f in frames)
        and last["slot0"] == "%X" % CTRL and last["decoded_445"] == 1 and last["xinput_calls"] >= 3
        and "xinput_poll" in last["seen"] and "table_resolve" in last["seen"],
    "G1_first_frame_init_fails_at_the_renderer_and_percode_never_updates": all(f["init_ret"] == ["15"] and f["resize_ret"] == ["15"]
        and "percode_update" not in f["seen"] and "renderer_resize" in f["seen"] and f["app_frame_counter"] == 0 for f in frames)
        and last["percode"] == "00" * 0x11,
    "G2_nothing_reaches_the_snapshot": ok_s and R["snapshot"]["held"] == "0" and R["snapshot"]["edge"] == "0"
        and R["history"]["present_mask"] == "FFFF" and R["history"]["pressure"][8:] == "00" * 12,
    "G3_the_arbiter_never_reaches_its_latch_test": all(v["ok"] and v["ret"] == "0" and "arbiter_latch_test" not in v["seen"]
        and "arbiter_button_test" not in v["seen"] for v in arb.values()),
    "S1_single_live_writer_behind_the_gate_and_a_dead_script_path": R["S1"]["percode_update_callers"] == ["0079C140"]
        and R["S1"]["gate"][0] == "cmp dword ptr [rdi + 0x64], ebx" and R["S1"]["gate"][3] == "call qword ptr [rax + 0x48]"
        and R["S1"]["gate"][7] == "call 0x79d010" and len(R["S1"]["script_path_refs"]) == 1 and "0079F1D0" in R["S1"]["script_path_refs"][0]
        and set(percode_writers) <= {"0079A120", "0079AE40", "0079AE90", "0079D010", "007A0B50", "00797EE0", "00797F20", "00797F60"}
        and "0079D010" in percode_writers,
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("snapshot", "arbiter", "history")}, default=str)[:1500])
print(json.dumps(frames[-1], default=str)[:800])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
