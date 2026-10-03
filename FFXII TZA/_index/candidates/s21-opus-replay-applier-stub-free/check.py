"""S-21: execute the whole result applier 003112F0 (CONTRACT-apply-result-to-target.md) with its REAL callees - the status
operation 0030E360, the recompute 0030FED0, the item/owner paths and the numeric setters - over the shipped battle_pack tables,
and test I1..I3 and I5..I7 (OPUS, 2026-09-25, block 332).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The gap this answers: "the setters are stubbed" (EXP-060 stubbed five
setters; EXP-149 scripted callees). world.py (block 318/319's builder, Session with stack arguments; block 332 adds a faithful
UCRT rand/srand bridge, seed 1) supplies the image, the IAT traps and the named bridges. No application stub.
The battle_pack tables are bound by shipped code (shipped_pack.py: the directory relocation 003846F0 and 00236C30's own binding
calls, the two heap-6 ones skipped). Four idle objects are zeroed blocks, the convention of the world's nine: [0209BE80] (HUD),
[01F7FFE0], [0215E6E0] and [0209CC40] (the battle-text object). The unit pool [0208E688] (count [0208E6A0], stride 0xF50) holds
two planted units whose +0x698 are the two planted stats records: 0031B860 maps stats to unit by walking it.
STOP BOUNDARY (recorded, nothing substituted): 002B4090, where a numeric HP/MP write posts its damage display into the
battle-text layer (S-37/S-38's presentation); the setter's call and its arguments are recorded before it.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R12,
                                UC_X86_REG_R15, UC_X86_REG_RSP)

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
APPLY, STATUS, RECOMP = 0x3112F0, 0x30E360, 0x30FED0
DISPLAY = 0x2B4090
W.ALLOWED |= {0x16D6A0, DISPLAY} | W.closure(APPLY) | SP.allowed(W)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
handlers = set()
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            handlers.add(h)
for h in handlers:                                         # the inventory handlers 0030xxxx reach by `jmp rax`
    W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
POOL, SRC, TGT, REC = 0x76280000, 0x76290000, 0x76291000, 0x76292000

ev = {}


def hook(addr, name, regs=(), stack=0):
    def on(u, a, n, _):
        sp = u.reg_read(UC_X86_REG_RSP)
        v = [u.reg_read(x) & 0xFFFFFFFFFFFFFFFF for x in regs] + [struct.unpack("<Q", bytes(u.mem_read(sp + 0x28 + 8 * i, 8)))[0]
                                                                   for i in range(stack)]
        ev.setdefault(name, []).append(v)
    uc.hook_add(UC_HOOK_CODE, on, begin=addr, end=addr)


def on_display(u, a, n, _):
    ev["stopped_at"] = "002B4090 display"
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_display, begin=DISPLAY, end=DISPLAY)
hook(STATUS, "status", (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9), stack=3)
hook(0x311AC5, "outer_recompute", (UC_X86_REG_RCX, UC_X86_REG_RDX))
for site, nm, target_reg in ((0x311668, "target_hp", UC_X86_REG_RAX), (0x3116A4, "target_mp", UC_X86_REG_RAX),
                              (0x311739, "source_hp", UC_X86_REG_R12), (0x311775, "source_mp", UC_X86_REG_R15)):
    hook(site, nm, (target_reg, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def reset():
    uc.mem_write(POOL, bytes(0xF50 * 2))
    for i, st in enumerate((SRC, TGT)):
        uc.mem_write(st, bytes(0x400))
        w(st + 4, "<BB", i, 0)
        w(POOL + i * 0xF50 + 0x698, "<Q", st)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 2)
    uc.mem_write(REC, bytes(0x148))
    uc.mem_write(REC + 0x5C, b"\xff" * 0x80)                 # every per-bit dword parameter absent (negative)
    uc.mem_write(REC + 0xDC, b"\xff" * 0x40)                 # every per-bit word parameter absent
    uc.mem_write(REC + 0x38, b"\xff" * 4)                    # no item
    uc.mem_write(REC + 0x3C, b"\xff" * 6)                    # layer bytes absent: +0x3C..3D (00311788 loop, 2) and +0x3E..41
                                                             # (003117E4 loop, 4); 0xFF is absent, 0 is layer 0 - section 3
    uc.mem_write(REC + 0x11E, b"\xff" * 8)                   # foe stat words absent (-1)


def apply(source=SRC, target=TGT, flags=0):
    ev.clear()
    ok = S.call(APPLY, REC, source, target, 0x10, stack=(flags,))
    return ok


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- I2: direct copy-through, masks zero ----
reset()
uc.mem_write(TGT + 0xBC, b"\x77" * 0x80)
uc.mem_write(TGT + 0x13C, b"\x77" * 0x40)
w(REC + 0x5C, "<iii", 5, -1, 0)
w(REC + 0xDC, "<hhh", 7, -3, 0)
ok = apply()
bc = list(r(TGT + 0xBC, "<III"))
w13c = list(r(TGT + 0x13C, "<HHH"))
i2_ev = {k: len(v) if isinstance(v, list) else v for k, v in ev.items()}
record("I2_copy_through_without_masks", ok and bc == [5, 0x77777777, 0] and w13c == [7, 0x7777, 0] and "outer_recompute" not in ev
       and "status" not in ev, events=i2_ev, dwords=["%X" % x for x in bc], words=["%X" % x for x in w13c],
       note="both masks zero: the applier copies each non-negative +0x5C dword to target +0xBC and each non-negative +0xDC word to "
            "+0x13C (negative preserves, zero is present); no status call and no outer recompute")

# ---- I1 + I3: +0x54 bit 5 forwards its parameters to 0030E360 mode 3, and the outer recompute follows (flag 0x200 blocks it) ----
st1 = {}
for label, flags in (("callerFlags 0", 0), ("callerFlags 0x200", 0x200)):
    reset()
    w(REC + 0x54, "<I", 1 << 5)
    w(REC + 0x5C + 4 * 5, "<i", 100)
    w(REC + 0xDC + 2 * 5, "<h", 3)
    before = bytes(uc.mem_read(TGT, 0x200))
    ok = apply(flags=flags)
    after = bytes(uc.mem_read(TGT, 0x200))
    calls = [["%X" % x for x in c] for c in ev.get("status", [])]
    st1[label] = {"ok": ok, "status_calls": calls, "outer_recompute": ["%X" % x for x in (ev.get("outer_recompute") or [[]])[0]],
                  "status_words_after": {"+38": "%X" % r(TGT + 0x38, "<I")[0], "+3C": "%X" % r(TGT + 0x3C, "<I")[0],
                                         "+64": "%X" % r(TGT + 0x64, "<I")[0]}}
first = st1["callerFlags 0"]["status_calls"][:1]
i1_ok = (first == [["%X" % TGT, "%X" % SRC, "5", "64", "3", "200", "3"]] and st1["callerFlags 0"]["outer_recompute"] == ["%X" % TGT, "0"]
         and st1["callerFlags 0x200"]["outer_recompute"] == [] and all(v["ok"] for v in st1.values())
        and st1["callerFlags 0"]["status_words_after"]["+64"] == "20")
record("I1_I3_apply_bit_mode3_and_outer_recompute", i1_ok, cases=st1,
       note="+0x54 bit 5 calls 0030E360(target, source, 5, 100, 3, 0x200, mode 3) with the bit's +0x5C / +0xDC parameters - the flags "
            "argument is 0x200 whatever the caller passed - and target +0x64 bit 5 is set; the outer "
            "0030FED0(target, 0) at 00311AC5 follows with caller flags 0 and is skipped with 0x200")

# ---- I1: +0x58 bit 5 is the same operation with zero parameters, mode 0 ----
reset()
w(REC + 0x58, "<I", 1 << 5)
ok = apply()
calls = [["%X" % x for x in c] for c in ev.get("status", [])]
record("I1_remove_bit_mode0", ok and calls[:1] == [["%X" % TGT, "%X" % SRC, "5", "0", "0", "200", "0"]], status_calls=calls[:3],
       note="+0x58 bit 5 calls 0030E360(target, source, 5, 0, 0, 0x200, mode 0)")

# ---- I5 / I6 / I7: the numeric dispatch - which setter, with which outgoing flags ----
num = {}
for label, A, src in (("target HP", 1 << 8, SRC), ("target HP absolute (bit 3)", (1 << 8) | (1 << 3), SRC),
                      ("target HP, A19 A10 A18 A6", (1 << 8) | (1 << 19) | (1 << 10) | (1 << 18) | (1 << 6), SRC),
                      ("target MP", 1 << 14, SRC), ("target MP absolute (bit 4)", (1 << 14) | (1 << 4), SRC),
                      ("source HP", 1 << 7, SRC), ("source HP, null source", 1 << 7, 0), ("source HP absolute (bit 1)", (1 << 7) | 2, SRC)):
    reset()
    w(REC + 0x2C, "<I", A)
    w(REC + 0x24, "<i", 40)
    ok = apply(source=src)
    seen = {k: [["%X" % x for x in c] for c in v] for k, v in ev.items() if k in ("target_hp", "target_mp", "source_hp", "source_mp")}
    num[label] = {"calls": seen, "stopped_at": ev.get("stopped_at")}


def setter(label, site):
    c = num[label]["calls"].get(site)
    return (c[0][0], c[0][4]) if c else None


i67 = (setter("target HP", "target_hp") == ("300530", "50") and setter("target HP absolute (bit 3)", "target_hp") == ("300520", "50")
       and setter("target HP, A19 A10 A18 A6", "target_hp") == ("300530", "120")
       and setter("target MP", "target_mp")[0] == "300CE0" and setter("target MP absolute (bit 4)", "target_mp")[0] == "300C90"
       and setter("source HP", "source_hp")[0] == "300530" and setter("source HP absolute (bit 1)", "source_hp")[0] == "300520"
       and num["source HP, null source"]["calls"] == {})
record("I5_I6_I7_numeric_dispatch", i67, cases=num,
       note="target HP alone -> 00300530 with flags 0x50; bit 3 -> 00300520; A19/A10 set and A18/A6 set -> flags 0x120 (8 and 5 on, 6 and 4 "
            "off); target MP -> 00300CE0, bit 4 -> 00300C90; source HP (A7) -> 00300530, bit 1 -> 00300520; a null source calls no "
            "setter for it. Each write then posts its damage display (the recorded boundary)")

json.dump({"ok": allok, "bound": made, "not_bound": skipped, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
