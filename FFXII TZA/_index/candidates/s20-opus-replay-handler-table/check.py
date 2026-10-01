"""S-20: execute the battle-action handler-table dispatch 00305080 (CONTRACT-battle-action-handler-table.md HT-1..HT-6) as shipped
code over every id of the table and past both ends (OPUS, 2026-09-25, block 350).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code. No application
stub. STOP BOUNDARIES (recorded, never stubbed): the entry of each handler the dispatcher tail-jumps to - the contract's subject
ends at that `jmp rdx`, and the handlers' bodies belong to other contracts; at each stop rcx and the entry are recorded.
Fixtures: six idle objects at 0x76300000, the unit (+0x10 a zeroed handle object, +0x698 battle-state row 0 with +4 type and +5
kind, +0x714 the order id), the battle-state block's +0x5AE0 bit 1 where a case sets it.
Writes result.json next to this file.
"""
import json
import os
import struct

import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
DISPATCH, AVAIL, POST, TABLE = 0x305080, 0x301830, 0x3299B0, 0x1EEC460
pe = pefile.PE(W.EXE, fast_load=True)
IMG = 0x120000
ENTRIES = [struct.unpack_from("<Q", pe.get_data(TABLE - IMG + 8 * i, 8))[0] for i in range(0x167)]
PAST = struct.unpack_from("<Q", pe.get_data(TABLE - IMG + 8 * 0x167, 8))[0]
HANDLERS = sorted({e for e in ENTRIES if e})
W.ALLOWED |= ({0x16D6A0} | SP.allowed(W) | W.closure(DISPATCH) | set(HANDLERS))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
UNIT, HANDLE = 0x76280000, 0x76290000
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
REC = BLOCK + 8


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


ev = {"posted": [], "stop": None}
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev["posted"].append(u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF), begin=POST, end=POST)


def _stop(u, x, n, _):
    ev["stop"] = {"at": x, "rcx": u.reg_read(UC_X86_REG_RCX)}
    u.emu_stop()


for h in HANDLERS:
    uc.hook_add(UC_HOOK_CODE, _stop, begin=h, end=h)


def dispatch(oid, typ=0, kind=0, bit=0):
    uc.mem_write(UNIT, bytes(0xF50))
    uc.mem_write(HANDLE, bytes(0x400))
    w(UNIT + 0x10, "<Q", HANDLE)
    w(UNIT + 0x698, "<Q", REC)
    w(REC + 4, "<BB", typ, kind)
    w(UNIT + 0x714, "<H", oid)
    w(BLOCK + 0x5AE0, "<B", bit)
    ev["posted"], ev["stop"] = [], None
    ok = S.call(DISPATCH, UNIT)
    return {"returned": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "stop": ev["stop"], "posted": list(ev["posted"]),
            "unit_5C": r(UNIT + 0x5C, "<I")[0], "faults": S.st["faults"][:1], "bad": S.st["bad"][:1]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- HT-1 / HT-2: the table read from the image ----
per = {}
for e in ENTRIES:
    if e:
        per["%08X" % e] = per.get("%08X" % e, 0) + 1
record("HT1_HT2_table_shape", len(ENTRIES) == 359 and sum(1 for e in ENTRIES if e) == 341 and len(HANDLERS) == 8
       and max(per.values()) == 249 and per.get("002FDDA0") == 249 and per.get("002FDA60") == 57
       and all(0x121000 <= e < 0x900000 for e in HANDLERS), non_null=sum(1 for e in ENTRIES if e), handlers=per,
       qword_past_the_end="%016X" % PAST,
       note="359 slots, 341 non-null, 8 distinct handlers (002FDDA0 x249, 002FDA60 x57), each a .text address; the qword past the "
            "bound is %016X" % PAST)

# ---- HT-3 / HT-5: every id reaches table[id - 0x4000] with only `this` in rcx; empty and out-of-range return -1 ----
sweep, bad = {}, []
for oid in list(range(0x4000, 0x4167)) + [0x3FFF, 0x4167, 0xFFFF, 0x0000]:
    d = dispatch(oid)
    i = oid - 0x4000
    want = ENTRIES[i] if 0 <= i < 0x167 else 0
    if want:
        good = d["stop"] is not None and d["stop"]["at"] == want and d["stop"]["rcx"] == UNIT and not d["faults"]
    else:
        good = d["returned"] and d["ret"] == 0xFFFFFFFF and d["stop"] is None
    sweep["%04X" % oid] = "%08X" % want if want else "-1"
    if not good:
        bad.append({"id": "%04X" % oid, **{k: v for k, v in d.items() if k != "posted"}})
record("HT3_HT5_tail_call_and_minus_one", not bad, ids=len(sweep), mismatches=bad[:4],
       note="all 359 ids plus 0x3FFF / 0x4167 / 0xFFFF / 0: a non-empty slot reaches exactly table[id - 0x4000] with rcx = the unit "
            "and nothing else passed (the tail-call); an empty slot or an id out of range returns -1 from the dispatcher itself")

# ---- HT-6: the presentation event is posted before the dispatch, and chosen by the battle-state block ----
h6 = {}
for label, typ, kind, bit in (("party type 0x1A, block bit set", 0x1A, 0, 2), ("party type 0x1A, bit clear", 0x1A, 0, 0),
                              ("party type 0x19, bit set", 0x19, 0, 2), ("kind 1, type 0x1A, bit set", 0x1A, 1, 2)):
    d = dispatch(0x4000, typ, kind, bit)
    h6[label] = {"posted": ["%X" % p for p in d["posted"]], "unit_5C": "%X" % d["unit_5C"], "reached_handler": d["stop"] is not None}
record("HT6_event_before_dispatch", [v["posted"] for v in h6.values()] == [["2010"], ["2001"], ["2001"], ["2001"]]
       and all(v["reached_handler"] and v["unit_5C"] == v["posted"][0] for v in h6.values()), cases=h6,
       note="003299B0 posts before the tail-call: 0x2010 only for a party record (kind 0) of type 0x1A with bit 1 of the "
            "battle-state block's +0x5AE0, otherwise 0x2001; the event lands in unit +0x5C")

# ---- HT-4: both consumers use the same table and bound (read from their instructions) ----
def rip_target(at, length, disp_off):
    d = struct.unpack_from("<i", pe.get_data(at - IMG + disp_off, 4))[0]
    return at + length + d


dispatch_table = rip_target(0x3050E1, 7, 3)
avail_table = rip_target(0x3018F0, 7, 3)
bounds = [struct.unpack_from("<I", pe.get_data(a - IMG + 1, 4))[0] for a in (0x3050D8, 0x3018E3)]
record("HT4_one_table_one_bound", dispatch_table == avail_table == TABLE and bounds == [0x166, 0x166],
       dispatch_table="%08X" % dispatch_table, availability_table="%08X" % avail_table, bounds=["%X" % b for b in bounds],
       note="the dispatcher (003050E1) and the availability check (003018F0) resolve the same table 01EEC460 and both bound the "
            "index at 0x166 (003050D8, 003018E3) - static, read from the instructions; the availability body is not executed")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results, "table": sweep},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
