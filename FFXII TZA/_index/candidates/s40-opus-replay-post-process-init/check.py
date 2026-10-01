"""S-40 (OPUS, 2026-09-26): CONTRACT-post-processing-subsystem executed - the game-owned frame function 00193DA0 and its lazy
creation route run as shipped, with the licensed library's own code (licence check, CPostEffect construction, Initialize) real up
to the Direct3D device.

World: block 332's (s21-opus-replay-applier-stub-free/check.py, imported; its cases run first, unchanged).
Built, not planted:
 - the library allocator object 02E5BDE0 is built by its shipped C++ static initialiser 00167990 (an entry of the CRT initialiser
   table, pointer at 008C44D8), which block 332's CRT start does not run;
 - the wrapper [02D38540], its adapter object and the library handle are built by the frame itself (0065E5D0, 0065E530/006CBAA0,
   006DA990), CPostEffect by 006DAA70's own allocation and constructor 006FF5D0;
 - the licence is the shipped string 00D86C00, validated by the library's own reader (006DFF40 -> 0071CD10: parse 0071D170, check
   0071D9E0).
Fence: the frame's closure plus the targets edges.tsv does not list because they are reached indirectly: the allocator's vtable
00D86BD8 (read from the image to its null slot), the handle vtable slot 006DAF50 (pointer at 00D8F908), 006DA990 (behind the
tail-jump thunk 006DEF20) and the `free` thunk 0019C590 (pointer cell 01F44CE8).
Bridges (crt_bridge.py, by name, fail-closed): the C runtime's strtok_s / sscanf / memcmp / strncmp and msvcp140's
basic_streambuf / basic_istream members the licence reader uses.
THE DEVICE IS NOT EMULATED. The render command is {+0 render context, +0x10 cfg}; the render context is a zero block whose only
populated field is +0x110, the D3D11 device context Initialize takes. That context is a ONE-METHOD MODEL, disclosed: slot 112
(+0x380, ID3D11DeviceContext::GetType) returns 1 (D3D11_DEVICE_CONTEXT_DEFERRED); every other slot points into a non-executable
page, so any further device use faults. In the shipped game the context is the immediate one; the model exists to take
Initialize's own refusal branch instead of the device-creation work behind it.
Cases:
 P1  cfg+0x99 set, no library object: the teardown 0065E6C0 -> 006CC2F0 runs and null-guards both members; the frame returns at
     00193DFC. No creation route, no setter forwarder and no run forwarder is entered (I-1: nothing runs without a library object).
 P2  cfg+0x99 clear: the lazy creation route runs once at every link - 0065E5A0 -> 006CBD20 -> 006DAA70 -> Initialize 006FF900 -
     with 006DAA70's arguments (3, 5, flags 0x20001); the shipped licence validates (0071CD10 returns 0); CPostEffect (0xD40) is
     allocated at [02EA0B70]; Initialize stores the flags 0x20001 at +0x208 and +0x20C (I-2), none of 0x800, 0x40000, 0x4000000,
     0x8000000 set.
 P3  the failure half of I-5, executed: the model context is refused by the library ("CPostEffect::Initialize(): Device context
     must be immediate context.", 0x80070057), 006DAA70 returns it, and 006CBD20 logs "Failed to initialize PPFX context."
     through 005CDAA0(2, ...) and continues - into 006DB4C0 -> 00708110, which faults at 00708186 reading +0x68 of CPostEffect's
     null +0x108. Creation continues, but not past its next library call.
 S1  static, byte-verified: +0x147 is written in Initialize only at 00700083 and only when the flags hold 0x800 (00700077), after
     00700056 zeroes it; +0x108 is zeroed by the constructor (006FF68E) and written in Initialize only at 007009BB; 00708110 returns
     early only on +0x147, else reads [+0x108]. Both writes follow the context-type refusal at 006FFC50-006FFC5E. With the build's
     constant 0x20001, therefore, creation survives only an Initialize that passed 007009BB, which needs an immediate device context;
     and the frame's setters and run (after 00193DFC) are reached only once creation has returned.
Evidence class NATIVE-REPLAY (unicorn) against a one-method device-context model, live_game false. Writes result.json.
"""
import collections
import contextlib
import io
import json
import os
import struct
import sys

import capstone
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP, \
    UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C                                     # block 332 (its cases run first, unchanged)
os.chdir(cwd)
sys.path.insert(0, HERE)
import crt_bridge

W, uc, S = C.W, C.uc, C.S
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
img = lambda a, n: bytes(uc.mem_read(a, n))                # the SHA-asserted image block 332 maps

FRAME, STATIC_INIT, WRAPPER, LIB = 0x193DA0, 0x167990, 0x2D38540, 0x2EA0B70
ALLOC_VT, HANDLE_VT_SLOT = 0xD86BD8, 0xD8F908
indirect = []
k = 0
while q(ALLOC_VT + 8 * k):
    indirect.append(q(ALLOC_VT + 8 * k)); k += 1
indirect += [q(HANDLE_VT_SLOT), 0x6DA990, q(0x1F44CE8)]
assert indirect[-2:] == [0x6DA990, 0x19C590] and q(HANDLE_VT_SLOT) == 0x6DAF50, indirect
for f in [FRAME, STATIC_INIT] + indirect:
    W.ALLOWED |= W.closure(f) | {f}
BR = []
crt_bridge.install(W, uc, BR)

# the built world: the library allocator's static initialiser, as the CRT would run it
assert q(0x8C44D8) == STATIC_INIT
static_ok = S.call(STATIC_INIT)
alloc_vt = q(0x2E5BDE0)

# instrumentation (records only)
WATCH = {0x65E6C0: "teardown_fwd", 0x6CC2F0: "teardown", 0x65E5A0: "create_fwd", 0x6CBD20: "create", 0x6DAA70: "ctx_init",
         0x6FF900: "Initialize", 0x6FF5D0: "CPostEffect_ctor", 0x71CD10: "licence_check", 0x6DB4C0: "set_6DB4C0",
         0x708110: "lib_708110", 0x65E6A0: "fwd_6A0", 0x65E6B0: "fwd_6B0", 0x65E670: "glare_fwd", 0x65E630: "fwd_630",
         0x65E610: "dof_fwd", 0x65E5C0: "run_fwd", 0x6CBEA0: "run", 0x6DB660: "apply_fwd", 0x70BA00: "ApplyEffects",
         0x5CDAA0: "game_log", 0x6DF480: "lib_log"}
entries = []
logs = []
args = {}


def on_entry(u, a, n, _):
    entries.append(WATCH[a])
    if a == 0x6DAA70:
        args["ctx_init"] = {"r8": u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF, "r9": u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF,
                            "arg5": "%X" % d4(u.reg_read(UC_X86_REG_RSP) + 0x28)}
    elif a == 0x6DF480:
        logs.append(("lib", crt_bridge.cstr(u, u.reg_read(UC_X86_REG_RCX), 200).decode("latin1")))
    elif a == 0x5CDAA0:
        logs.append(("game", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, crt_bridge.cstr(u, u.reg_read(UC_X86_REG_RDX), 200).decode("latin1")))


for a in WATCH:
    uc.hook_add(UC_HOOK_CODE, on_entry, begin=a, end=a)
rets = {}
for site, nm in ((0x6CBE0F, "ctx_init"), (0x6E012E, "licence_check")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: rets.__setitem__(nm, "%X" % (u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)))(nm),
                begin=site, end=site)

# the device context: a one-method model (disclosed)
D3D = 0x7B400000
uc.mem_map(D3D, 0x3000)
uc.mem_write(D3D, bytes(0x3000))
uc.mem_map(D3D + 0x3000, 0x1000, 1)                       # readable, NOT executable: any other method faults
CTXM, CTXVT, GETTYPE = D3D, D3D + 0x1000, D3D + 0x2000
uc.mem_write(GETTYPE, bytes([0xC3]))
uc.mem_write(CTXM, struct.pack("<Q", CTXVT))
for k in range(0x100):
    uc.mem_write(CTXVT + 8 * k, struct.pack("<Q", D3D + 0x3000 + 8 * k))
uc.mem_write(CTXVT + 0x380, struct.pack("<Q", GETTYPE))
d3d_calls = []


def gettype(u, a, n, _):
    d3d_calls.append("GetType")
    u.reg_write(UC_X86_REG_RAX, 1)                       # D3D11_DEVICE_CONTEXT_DEFERRED


uc.hook_add(UC_HOOK_CODE, gettype, begin=GETTYPE, end=GETTYPE)
uc.ctl_flush_tb()

BUF = 0x7C000000
uc.mem_map(BUF, 0x10000)
uc.mem_write(BUF, bytes(0x10000))
CMD, RC, CFG = BUF, BUF + 0x1000, BUF + 0x2000
uc.mem_write(CMD, struct.pack("<Q", RC))
uc.mem_write(CMD + 0x10, struct.pack("<Q", CFG))
uc.mem_write(RC + 0x110, struct.pack("<Q", CTXM))


def frame(x99):
    del entries[:], logs[:], d3d_calls[:]
    rets.clear(); args.clear()
    uc.mem_write(CFG + 0x99, bytes([x99]))
    ok = S.call(FRAME, CMD)
    tr = list(S.st["trace"])
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:2], "last_pc": "%X" % tr[-1] if tr else None,
            "entries": list(entries), "logs": list(logs), "d3d": list(d3d_calls), "rets": dict(rets), "args": dict(args)}


R = {"static_init": {"ok": static_ok, "allocator_vtable": "%X" % alloc_vt, "fence_indirect": ["%08X" % x for x in indirect]}}
R["P1"] = p1 = frame(1)
p1["wrapper"] = "%X" % q(WRAPPER)
p1["adapter"] = "%X" % q(q(WRAPPER))
p1["handle"] = "%X" % q(q(q(WRAPPER)))
R["P2"] = p2 = frame(0)
lib = q(LIB)
p2["lib"] = "%X" % lib
p2["handle"] = "%X" % q(q(q(WRAPPER)))
if lib:
    p2["flags_208"], p2["flags_20C"] = "%X" % d4(lib + 0x208), "%X" % d4(lib + 0x20C)
    p2["plus_108"], p2["plus_147"] = "%X" % q(lib + 0x108), uc.mem_read(lib + 0x147, 1)[0]
p2["bridged"] = dict(collections.Counter(x if isinstance(x, str) else x[0] for x in BR))

# S1: static, over the shipped bytes
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def ins(a):
    i = next(md.disasm(img(a, 16), a, count=1))
    return "%s %s" % (i.mnemonic, i.op_str)


def stores(fn, size, disp):                               # object-field stores: frame-based ([rbp+..] / [rsp+..]) locals excluded
    out = []
    for i in md.disasm(img(fn, size), fn):
        dst = i.op_str.split(",")[0]
        if i.mnemonic == "mov" and dst.endswith("+ 0x%x]" % disp) and "ptr [" in dst and not dst.split("[")[1].startswith(("rbp", "rsp")):
            out.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
    return out


S1 = {"init_147": stores(0x6FF900, 23568, 0x147), "init_108": stores(0x6FF900, 23568, 0x108),
      "ctor_108": stores(0x6FF5D0, 608, 0x108), "ctor_147": stores(0x6FF5D0, 608, 0x147),
      "flag_test_0x800": ins(0x700077), "set_147": ins(0x700083), "zero_146_147": ins(0x700056),
      "ctx_type_call": [ins(0x6FFC50), ins(0x6FFC53), ins(0x6FFC56), ins(0x6FFC5C), ins(0x6FFC5E)],
      "flags_store": [ins(0x6FFB86), ins(0x6FFB8C)],
      "f708110": [ins(0x708152), ins(0x70815F), ins(0x708173), ins(0x708186)],
      "frame_gate": [ins(0x193DF5), ins(0x193DFA), ins(0x193DFC)]}
R["S1"] = S1

create_route = ["create_fwd", "create", "ctx_init", "Initialize"]
after_gate = {"fwd_6A0", "fwd_6B0", "glare_fwd", "fwd_630", "dof_fwd", "run_fwd", "run", "apply_fwd", "ApplyEffects"}
p2_route = [e for e in p2["entries"] if e in create_route]
cases = {
    "static_initialiser_builds_the_library_allocator": static_ok and alloc_vt == ALLOC_VT,
    "P1_teardown_without_object_runs_nothing_behind_the_gate": p1["ok"] and p1["entries"][:2] == ["teardown_fwd", "teardown"]
        and not set(p1["entries"]) & (set(create_route) | after_gate) and p1["handle"] == "0" and p1["adapter"] != "0",
    "P2_creation_route_once_per_link_with_constant_flags": p2_route == create_route
        and p2["args"].get("ctx_init") == {"r8": 3, "r9": 5, "arg5": "20001"},
    "P2_shipped_licence_validates": p2["rets"].get("licence_check") == "0" and "licence_check" in p2["entries"],
    "P2_Initialize_stores_0x20001_at_208_and_20C": lib != 0 and p2.get("flags_208") == "20001" and p2.get("flags_20C") == "20001"
        and int(p2["flags_20C"], 16) & (0x800 | 0x40000 | 0x4000000 | 0x8000000) == 0 and p2["entries"].count("CPostEffect_ctor") == 1,
    "P3_refused_init_is_logged_and_creation_continues": p2["d3d"] == ["GetType"] and p2["rets"].get("ctx_init") == "80070057"
        and any("Device context must be immediate context" in l[1] for l in p2["logs"] if l[0] == "lib")
        and ("game", 2, "Failed to initialize PPFX context. \n") in p2["logs"]
        and p2["entries"][-2:] == ["set_6DB4C0", "lib_708110"],
    "P3_continuation_faults_on_the_unbuilt_plus_108": not p2["ok"] and p2["last_pc"] == "708186" and p2["halt"][:1] == ["00000068"]
        and p2.get("plus_108") == "0" and p2.get("plus_147") == 0 and not set(p2["entries"]) & after_gate,
    "S1_plus_147_and_plus_108_written_only_past_the_device_check": S1["init_147"] == ["00700083 mov byte ptr [rsi + 0x147], r12b"]
        and S1["init_108"] == ["007009BB mov qword ptr [rsi + 0x108], rax"] and S1["ctor_108"] == ["006FF68E mov qword ptr [rdi + 0x108], rsi"]
        and S1["ctor_147"] == [] and S1["flag_test_0x800"] == "test dword ptr [rsi + 0x20c], 0x800"
        and S1["zero_146_147"] == "mov word ptr [rsi + 0x146], r14w"
        and S1["ctx_type_call"][2] == "call qword ptr [rax + 0x380]" and S1["flags_store"][1] == "mov dword ptr [rsi + 0x20c], eax"
        and S1["f708110"] == ["cmp byte ptr [rsi + 0x147], 0".replace("rsi", "rcx"), "je 0x708173", "mov r10, qword ptr [rcx + 0x108]",
                              "cmp qword ptr [r10 + 0x68], rax"]
        and S1["frame_gate"][2] == "je 0x193f5d",
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("P1", "P2")}, default=str)[:2500])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
