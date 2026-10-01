"""S-41 (OPUS, 2026-09-26): the sound request's POSITIVE dispatch over a bank LOADED from the shipped se000.seb - the Seb bank built
by the game's own load chain, the dispatch matching it, the receipt, the play entry and the loading fence.

S-41's residual (AUDIT-SEM): "the loaded-bank positive dispatch arm (EXP-105's fork ran under stubs)". Runs the sound-request
closer's world (../s41-opus-replay-sound-request-stub-free/check.py, executed first from its own source with its cases unchanged;
its result.json is not rewritten), then:
  - the audio driver manager [01FD4138] built by its own lazy initialiser 002216B0(0x400, 0x400) - the constants its only caller
    00210760 passes - which runs operator new and the constructor 0021E570;
  - the audio file loader [01FD36A8] built by its own lazy initialiser 002125A0 (operator new(0x158), constructor 00211840).
    Its worker thread is NOT run: CreateThread and the thread-attribute calls are bridged by name and return handles; the thread
    body never executes. That is the recorded boundary - the loader's file I/O;
  - the shipped ps2data/sound/se/block/se000.seb (sha256 40d50fc1...) copied to memory - the bytes the kind-32 load delivers - and
    handed to 002DEF00(0, blob), the registration's own call (003A1650 -> 002DEF00(slot & 0x3F, blob)), which runs 001DBD20 ->
    the Seb controller's load 0021B430 -> SebAudioBank's initialiser 00223AD0: the slot map is filled from the file and the .sab
    load is queued (strcpy_s bridged by name with library semantics, copying the path into the request).
No application stub. Functions reached through vtables/indirect calls and admitted: 00218920, 0021B150, 00212810 (the controller's
slots), 0019C590 (free).
Cases:
 L1  the load: a SebAudioBank (vtable 00907D80) is spliced into the controller's list; its map root +0x70 is set (slots from the
     file); +0x3C = 0 (block 0's bucket); +0x30 = 1 (loading); the queued path is PS2Data/sound/se/sead_data_win/se000/se000.win.sab.
 D1  positive dispatch: 0021B5B0(controller, id 1, pan 0x40, vol 0x7F) mints the receipt at 0021B5E2 BEFORE the walk (the
     contract's "Seb calls RCAL 00212950 at 0021B5E2, before it walks the list"), matches the loaded bank on id / 512 = 0 at +0x3C,
     and calls the Seb play 00224540 with it.
 D2  the fence: with +0x30 == 1 the play enters the spin fence (0022459E cmp / 005CCB80) and keeps yielding (Sleep, bridged by
     name, returns) - +0x30 never changes, because only the unrun loader thread completes the load. Stopped by the instruction
     budget. Recorded boundary: the .sab file I/O.
 D3  control: id 0x201 (bucket 1) matches no bank - no play call - and a receipt is still minted.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import contextlib
import hashlib
import io
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s41-opus-replay-sound-request-stub-free"))
SEB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data", "sound", "se", "block", "se000.seb"))
SEB_SHA = "40d50fc1e11f91c34a8780dacd0bcf20fee6c0919951063c5fe67f08eafa65f6"
src = open(os.path.join(BASE, "check.py"), encoding="utf-8").read()
src = re.sub(r"sys\.exit\([^\n]*\)", "pass", src)
src = src.replace('open(os.path.join(HERE, "result.json"), "w")', "io.StringIO()")
g = {"__file__": os.path.join(BASE, "check.py"), "__name__": "s41sr", "io": io}
cwd = os.getcwd(); os.chdir(BASE); sys.path.insert(0, BASE)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "check.py", "exec"), g)
os.chdir(cwd)
base_ok = g["allok"] if "allok" in g else g.get("res", {}).get("ok")
uc, S, W = g["uc"], g["S"], g["W"]
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8

q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
pe = pefile.PE(W.EXE)
IAT = {(imp.name or b"").decode(): imp.address for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
for nm, v in (("CreateThread", 0x1234), ("SetThreadPriority", 1), ("ResumeThread", 1), ("SetThreadAffinityMask", 1),
              ("SetThreadIdealProcessor", 0), ("strcpy_s", 0), ("Sleep", 0)):
    W.OSRET[nm] = v
    W.BRIDGED.add(nm)
paths = []


def strcpy_s(u, a, n, _):
    d, s_ = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_R8)
    raw = bytes(u.mem_read(s_, 512))
    txt = raw[:raw.find(b"\0")]
    u.mem_write(d, txt + b"\0")
    paths.append(txt.decode("latin1"))


uc.hook_add(UC_HOOK_CODE, strcpy_s, begin=q(IAT["strcpy_s"]), end=q(IAT["strcpy_s"]))
ADMIT = (0x218920, 0x21B150, 0x212810, 0x19C590)
for f in (0x2216B0, 0x2125A0, 0x2DEF00, 0x21B5B0, 0x224540) + ADMIT:
    W.ALLOWED |= W.closure(f) | {f}
ev, ctl = [], []
for a, nm in ((0x212950, "receipt"), (0x224540, "play"), (0x5CCB80, "fence"), (q(IAT["Sleep"]), "Sleep")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: ev.append(nm))(nm), begin=a, end=a)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ctl.append(u.reg_read(UC_X86_REG_RCX)), begin=0x21B430, end=0x21B430)
walk = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: walk.append("walk"), begin=0x21B5E7, end=0x21B5E7)
uc.ctl_flush_tb()
okm = S.call(0x2216B0, 0x400, 0x400)
okl = S.call(0x2125A0)
BLOB = 0x79000000
uc.mem_map(BLOB, 0x10000)
data = open(SEB, "rb").read()
assert hashlib.sha256(data).hexdigest() == SEB_SHA
uc.mem_write(BLOB, data)
okb = S.call(0x2DEF00, 0, BLOB)
c = ctl[-1] if ctl else 0
banks = []
n = q(c + 8) if c else 0
while c and n and n != c + 8 and len(banks) < 8:
    b = q(n + 0x10)
    banks.append({"bank": "%X" % b, "vt": "%X" % q(b), "+30": d4(b + 0x30), "+3C": d4(b + 0x3C), "root_70": "%X" % q(b + 0x70)})
    n = q(n)


def dispatch(sid, budget):
    del ev[:], walk[:]
    S.count = budget
    ok = S.call(0x21B5B0, c, sid, 0x40, 0x7F, stack=(0, 0, 0))
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:1], "receipt": d4g(), "events": list(ev), "walk_after_receipt": list(walk)}


def d4g():
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


d1 = dispatch(1, 400000)
bank30_after = d4(int(banks[0]["bank"], 16) + 0x30) if banks else None
d3 = dispatch(0x201, 400000)
R = {"base_ok": base_ok, "manager": {"ok": okm, "cell": "%X" % q(0x1FD4138)}, "loader": {"ok": okl, "cell": "%X" % q(0x1FD36A8)},
     "load": {"ok": okb, "banks": banks, "queued_paths": paths[:2]}, "D1_D2": dict(d1, bank30_after=bank30_after), "D3": d3}
first = lambda evs, nm: evs.index(nm) if nm in evs else None
cases = {
    "L1_seb_bank_loaded_from_the_shipped_file": okm and okl and okb and len(banks) == 1 and banks[0]["vt"] == "907D80" and banks[0]["root_70"] != "0"
        and banks[0]["+3C"] == 0 and banks[0]["+30"] == 1 and paths[:1] == ["PS2Data/sound/se/sead_data_win/se000/se000.win.sab"],
    "D1_receipt_before_walk_match_and_play": d1["events"][:2] == ["receipt", "play"] and first(d1["events"], "receipt") < first(d1["events"], "play"),
    "D2_play_waits_on_the_loading_fence_forever": not d1["ok"] and not d1["halt"] and d1["events"].count("fence") > 100 and d1["events"].count("Sleep") > 100
        and bank30_after == 1,
    "D3_no_matching_bank_no_play_receipt_still_minted": d3["ok"] and d3["events"] == ["receipt"] and d3["receipt"] != 0,
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
summ = dict(R)
summ["D1_D2"] = dict(d1, events=d1["events"][:4] + ["...x%d" % len(d1["events"])], bank30_after=bank30_after)
json.dump(dict(res, results=summ), open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps(summ, default=str)[:1800])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
