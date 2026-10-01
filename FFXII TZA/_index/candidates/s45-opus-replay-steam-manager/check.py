"""S-45 (OPUS, 2026-09-26): CONTRACT-steam-integration-subsystem's I-2, I-3 and I-4 executed with the achievement manager BUILT by
its own builder 0020CD30, against a disclosed model of the Steam library.

World: block 332's (s21-opus-replay-applier-stub-free/check.py, imported; its cases run first, unchanged), with the image-backed
block bound by 00253970's own prefix as in s45-opus-replay-counters. No application stub.
THE STEAM LIBRARY IS MODELLED, disclosed (steam_api64.dll is external to the image, and AUDIT-SEM named this route on
AUDITSEM-REQ-OPUS-412): SteamAPI_RegisterCallback records its (object, id) and returns; SteamInternal_ContextInit returns a
context whose +0x08 / +0x18 / +0x28 hold three interface objects. Their methods are addresses on a `ret` page, each hooked with
library semantics: ISteamUser +0x08 BLoggedOn -> 1; ISteamUtils +0x48 GetAppID -> 595520 (0x91640, the id the contract's
RestartAppIfNecessary check uses); ISteamUserStats +0x00 RequestCurrentStats -> 1, +0x30 GetAchievement(name, bool *) -> the
model's state, +0x38 SetAchievement(name) -> sets it, +0x50 StoreStats -> 1, +0x60 GetAchievementDisplayAttribute(name, key) ->
a fixed model string (the 1101 handler formats it into the entry's +0x10 / +0x90). Every method call is recorded.
Receipts are delivered by calling the game's own handlers with a callback struct {u64 game id, u32 result}: 1101 = 0020C940,
1103 = 0020C8C0 (their registrations are recorded in M0).
Cases:
 M0  0020CD30 builds the manager: callbacks 1101, 1102, 1103 registered in that order; GetAppID read once into +0x00;
     0020CCC0 asks BLoggedOn and then RequestCurrentStats; [01F83450] = the manager; +0x10 = 41 entries; +0x18 = 0.
 I2  an award by index (008632B0(k)) before 1101 marks the entry's +0x190 and makes NO Steam call; 1101 with the right game id
     and result 1 sets +0x18 and overwrites every entry's +0x190 from GetAchievement - the pre-receipt award is lost (model: not
     achieved). Control: a 1101 for another game id changes nothing.
 I3  after 1101 the same award calls SetAchievement(entry name) then StoreStats once; awarding it again makes no Steam call.
 I4  1103 receipts count into +0x14; only the receipt that brings it to count - 1 (40) looks at entry 0, and with entry 0 not
     achieved it awards it (SetAchievement("ACH_...") through 0020CE10) - one award for forty receipts. Static half: the
     by-index route's payload table 00D10550 (the evaluate path's [r15 + r14*4 + 0xBF0550]) holds no 0 for ids 0..29, so no
     authored condition awards entry 0.
Evidence class NATIVE-REPLAY (unicorn) against a disclosed library model, live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C                                     # block 332 (its cases run first, unchanged)
os.chdir(cwd)
W, uc, S = C.W, C.uc, C.S
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
cstr = lambda a: bytes(uc.mem_read(a, 64)).split(b"\0")[0].decode("latin1")
BUILD, AWARD, H1101, H1103, SEND = 0x20CD30, 0x8632B0, 0x20C940, 0x20C8C0, 0x20CE60
for f in (BUILD, AWARD, H1101, H1103, 0x20CE10, 0x20CCC0):
    W.ALLOWED |= W.closure(f) | {f}
W.ALLOWED |= {0x253970, 0x249840, 0x2EF640}
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=0x253997, end=0x253997)
pe = pefile.PE(W.EXE)
IAT = {(imp.name or b"").decode(): imp.address for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
APPID = 0x91640
STEAM = 0x7B000000
uc.mem_map(STEAM, 0x10000)
uc.mem_write(STEAM, bytes(0x10000))
METH = STEAM + 0x8000
uc.mem_write(METH, b"\xC3" * 0x100)
CTX, USER, UTILS, STATS = STEAM, STEAM + 0x100, STEAM + 0x200, STEAM + 0x300
VT = {USER: STEAM + 0x1000, UTILS: STEAM + 0x1100, STATS: STEAM + 0x1200}
for obj, vt in VT.items():
    uc.mem_write(obj, struct.pack("<Q", vt))
uc.mem_write(CTX + 0x08, struct.pack("<Q", USER))
uc.mem_write(CTX + 0x18, struct.pack("<Q", UTILS))
uc.mem_write(CTX + 0x28, struct.pack("<Q", STATS))
achieved = {}
calls = []
METHODS = {(USER, 0x08): "BLoggedOn", (UTILS, 0x48): "GetAppID", (STATS, 0x00): "RequestCurrentStats", (STATS, 0x30): "GetAchievement",
           (STATS, 0x38): "SetAchievement", (STATS, 0x50): "StoreStats", (STATS, 0x60): "GetAchievementDisplayAttribute"}
ATTR = STEAM + 0x5000                                      # the display attribute string the model returns


def method(name):
    def on(u, a, n, _):
        if name == "BLoggedOn":
            r = 1
        elif name == "GetAppID":
            r = APPID
        elif name == "GetAchievement":
            nm = cstr(u.reg_read(UC_X86_REG_RDX))
            u.mem_write(u.reg_read(UC_X86_REG_R8), bytes([1 if achieved.get(nm) else 0]))
            calls.append([name, nm]); r = 1
        elif name == "GetAchievementDisplayAttribute":
            u.mem_write(ATTR, b"model attribute\0")
            r = ATTR
            calls.append([name])
            u.reg_write(UC_X86_REG_RAX, r)
            return
        elif name == "SetAchievement":
            nm = cstr(u.reg_read(UC_X86_REG_RDX))
            achieved[nm] = True
            calls.append([name, nm]); r = 1
        else:
            calls.append([name]); r = 1
        if name in ("BLoggedOn", "GetAppID"):
            calls.append([name])
        u.reg_write(UC_X86_REG_RAX, r)
    return on


for i, ((obj, off), name) in enumerate(METHODS.items()):
    addr = METH + 4 * i
    uc.mem_write(VT[obj] + off, struct.pack("<Q", addr))
    uc.hook_add(UC_HOOK_CODE, method(name), begin=addr, end=addr)
regs = []
for nm, v in (("SteamAPI_RegisterCallback", 0), ("SteamInternal_ContextInit", CTX)):
    W.OSRET[nm] = v
    W.BRIDGED.add(nm)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: regs.append(u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF),
            begin=q(IAT["SteamAPI_RegisterCallback"]), end=q(IAT["SteamAPI_RegisterCallback"]))
uc.ctl_flush_tb()
C.reset()
S.call(0x253970)
okb = S.call(BUILD)
M = q(0x1F83450)
entry = lambda k: q(M + 8) + k * 0x198
M0 = {"ok": okb, "registered": list(regs), "calls": [c[0] for c in calls], "manager": "%X" % M, "appid": "%X" % d4(M) if M else None,
      "count": d4(M + 0x10) if M else None, "stats_received": uc.mem_read(M + 0x18, 1)[0] if M else None}
CB = STEAM + 0x4000


def receipt(handler, game=APPID, result=1):
    uc.mem_write(CB, struct.pack("<QI", game, result))
    del calls[:]
    ok = S.call(handler, M, CB)
    return ok, list(calls)


def award(k):
    del calls[:]
    ok = S.call(AWARD, k)
    return ok, list(calls)


K = 5
name5 = cstr(q(entry(K) + 8))
a_pre = award(K)
pre_mark = uc.mem_read(entry(K) + 0x190, 1)[0]
wrong = receipt(H1101, game=APPID + 1)
wrong_flag = uc.mem_read(M + 0x18, 1)[0]
r1101 = receipt(H1101)
after_1101 = {"flag18": uc.mem_read(M + 0x18, 1)[0], "entry5_190": uc.mem_read(entry(K) + 0x190, 1)[0],
              "getachievement_calls": sum(1 for c in r1101[1] if c[0] == "GetAchievement")}
a_post = award(K)
a_again = award(K)
# I-4: forty 1103 receipts
uc.mem_write(M + 0x14, struct.pack("<I", 0))
name0 = cstr(q(entry(0) + 8))
per = []
for i in range(41):
    ok, cl = receipt(H1103)
    per.append({"i": i, "ok": ok, "count": d4(M + 0x14), "calls": cl})
entry0_awards = [p["i"] for p in per if any(c[0] == "SetAchievement" and c[1] == name0 for c in p["calls"])]
payload = [d4(0xD10550 + 4 * i) for i in range(30)]
R = {"M0": M0, "I2": {"award_before": a_pre, "entry_marked": pre_mark, "wrong_game": {"ok": wrong[0], "calls": wrong[1], "flag18": wrong_flag},
                       "receipt_1101": {"ok": r1101[0]}, "after_1101": after_1101},
     "I3": {"entry5_name": name5, "award_after": a_post, "award_again": a_again},
     "I4": {"entry0_name": name0, "awarded_at_receipt": entry0_awards, "counts": [p["count"] for p in per][:3] + ["..."] + [p["count"] for p in per][-3:],
            "payload_ids_0_29": payload}}
cases = {
    "M0_manager_built_registers_1101_1102_1103_reads_appid_requests_stats": okb and regs == [1101, 1102, 1103] and M0["appid"] == "%X" % APPID
        and M0["count"] == 41 and M0["stats_received"] == 0 and M0["calls"][:3] == ["GetAppID", "BLoggedOn", "RequestCurrentStats"],
    "I2_award_before_1101_marks_locally_no_steam_call": a_pre[0] and a_pre[1] == [] and pre_mark == 1,
    "I2_control_1101_for_another_game_changes_nothing": wrong[0] and wrong[1] == [] and wrong_flag == 0,
    "I2_1101_sets_flag_and_overwrites_entries_the_early_award_is_lost": r1101[0] and after_1101["flag18"] == 1 and after_1101["entry5_190"] == 0
        and after_1101["getachievement_calls"] >= 40,
    "I3_award_after_1101_sends_once_then_is_idempotent": a_post[0] and a_post[1] == [["SetAchievement", name5], ["StoreStats"]] and a_again[0] and a_again[1] == [],
    "I4_entry0_awarded_once_on_the_receipt_that_reaches_count_minus_1": entry0_awards == [39] and all(p["ok"] for p in per),
    "I4_static_no_by_index_payload_is_0": all(p != 0 for p in payload),
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({"M0": M0, "I2": R["I2"]["after_1101"], "I3": [a_post, a_again], "I4": R["I4"]["awarded_at_receipt"], "payload": payload[:8]}, default=str)[:1500])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
