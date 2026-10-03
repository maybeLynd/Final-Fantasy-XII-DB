"""S-29: execute CONTRACT-equipment-compatibility.md's entries - the partner test 002F7EC0, the eligibility chain 00317930, its
by-stats-index wrapper 00317B20, the licence gate 00323C60 (with the board lookup 00323BB0 it tail-jumps to) and the recommender
002F9F20 - as shipped code in one built world, and test EQ-1..EQ-8 (OPUS, 2026-09-25, block 323).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; block 323 adds stack
arguments to Session.call) supplies the image, the IAT traps and the named bridges; its world is built once. No application
stub and no stop boundary: every body, callee and validator runs as shipped. The authored tables are planted fixtures (the
engine loads them from its data files at runtime; in the image the cells are null):
  [02EBF0F8] equipment-definition header {+4 count, +8 u16 stride, +0xC offset}; the codec base [01F83530] is 0 in the built
             world, so the offset is the table's address. Records: +7 packed slot/exemption, +9 class, +0x11 partner class.
  [02EBF130] the character-class header, records (stride 4) = the FORBIDDEN-class mask, selected by stats[+4].
  [02EBF038] the licence header, records {+5 kind, +8 u16 ids[8]}; kind 1 maps to licence class 0 (003241D0 -> 00323890).
  the stats records in the 02EBF190 block (+8 + i*0x1C8; +4 index, +5 selector, +0x50..+0x58 equipment, +0x194 licence bits),
  the mode-3 character -> stats-index bytes at +0x5A7E, and the owned counts behind the id family's +0x08 (01EEBD20).
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
PARTNER, CHAIN, WRAP, LICENCE, BOARD, RECOMMEND, VALIDATE = 0x2F7EC0, 0x317930, 0x317B20, 0x323C60, 0x323BB0, 0x2F9F20, 0x322C50
COMPARE = 0x2F7A10
W.ALLOWED |= {0x16D6A0, BOARD, 0x2FD8D0} | set().union(*(W.closure(f) for f in (PARTNER, CHAIN, WRAP, LICENCE, BOARD, RECOMMEND)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc

EQ_CELL, CLASS_CELL, LIC_CELL, STATS_CELL, FAM1_COUNTS = 0x2EBF0F8, 0x2EBF130, 0x2EBF038, 0x2EBF190, 0x1EEBD20
BASE = 0x76380000
EQH, CLH, LIH = BASE, BASE + 0x100, BASE + 0x200
EQT, CLT, LIT, OWNED, OUT, MAIN = BASE + 0x10000, BASE + 0x20000, BASE + 0x21000, BASE + 0x22000, BASE + 0x23000, BASE + 0x23100
STRIDE, COUNT = 0x40, 0x1A4
STATS_BLOCK = struct.unpack("<Q", bytes(uc.mem_read(STATS_CELL, 8)))[0]


def stats(i):
    return STATS_BLOCK + 8 + i * 0x1C8


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def rec(i):
    return EQT + (i - 0x1000) * STRIDE


def define(i, slot, cls, partner=0xFF, exempt=False):
    w(rec(i) + 7, "<B", (slot << 5) | (0x10 if exempt else 0))
    w(rec(i) + 9, "<B", cls & 0xFF)
    w(rec(i) + 0x11, "<B", partner & 0xFF)


def world_reset():
    """Every table fresh: all records slot 7 (never a slot), class 31 (forbidden below), no partner; one owned of each."""
    uc.mem_write(BASE, bytes(0x24000))
    w(EQH, "<IIHHI", 0, COUNT, STRIDE, 0, EQT)
    w(CLH, "<IIHHI", 0, 0x28, 4, 0, CLT)
    w(LIH, "<IIHHI", 0, 4, 0x18, 0, LIT)
    for c, h in ((EQ_CELL, EQH), (CLASS_CELL, CLH), (LIC_CELL, LIH)):
        w(c, "<Q", h)
    for i in range(0x1000, 0x1000 + COUNT):
        define(i, 7, 31)
    for k in range(0x28):
        w(CLT + 4 * k, "<I", 1 << 31)
    for n in range(0x1000):
        w(OWNED + 2 * n, "<H", 1)
    w(FAM1_COUNTS, "<Q", OWNED)
    uc.mem_write(STATS_BLOCK, bytes(0x6000))
    for k in range(0x28):
        w(stats(k) + 4, "<B", k)
    for li in range(4):                                  # licence records: kind 1 (licence class 0), no ids yet
        w(LIT + li * 0x18 + 5, "<B", 1)
        w(LIT + li * 0x18 + 8, "<8H", *([0xFFFF] * 8))


calls = []


def watch(a, name, regs):
    def on(u, addr, n, _):
        calls.append((name,) + tuple(u.reg_read(r) & 0xFFFFFFFF for r in regs))
    uc.hook_add(UC_HOOK_CODE, on, begin=a, end=a)


watch(VALIDATE, "validate", (UC_X86_REG_RCX, UC_X86_REG_RDX))
watch(0x322D02, "class6_arm", ())
watch(BOARD, "board", (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8))
watch(WRAP, "wrap", (UC_X86_REG_RCX, UC_X86_REG_R8, UC_X86_REG_R9))
watch(PARTNER, "partner", (UC_X86_REG_RCX, UC_X86_REG_RDX))
watch(COMPARE, "compare", (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8))


def run(fn, *args, stack=()):
    del calls[:]
    ok = S.call(fn, *args, stack=stack)
    assert ok, (hex(fn), (S.st["bad"] or S.st["faults"])[:2])
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def partner(a, b):
    return run(PARTNER, a, b)


def chain(st, main, slot, item, owned=0):
    w(MAIN, "<H", main)
    return run(CHAIN, st, MAIN, slot, item, stack=(owned,))


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


ST = stats(0)
FREE = 0                                                 # an allowed class: bit 0 clear in the forbidden mask

# ---- EQ-1: asymmetric partner test, arg1 = off-hand, arg2 = main hand ----
world_reset()
MAIN_A, OFF_B = 0x1010, 0x10D0
define(MAIN_A, 0, 2, partner=5)                          # main hand: own class 2, requires partner class 5
define(OFF_B, 1, 5, partner=0xFF)                        # off-hand: own class 5
e1 = {"(off, main)": partner(OFF_B, MAIN_A), "(main, off)": partner(MAIN_A, OFF_B),
      "(0xFFFF, main)": partner(0xFFFF, MAIN_A), "(off, 0xFFFF)": partner(OFF_B, 0xFFFF)}
record("EQ1_partner_test_asymmetric", e1 == {"(off, main)": 1, "(main, off)": 0, "(0xFFFF, main)": 1, "(off, 0xFFFF)": 1},
       results=e1, note="record(arg2)[+0x11] == record(arg1)[+0x09]: 1 with (off-hand, main); swapping gives 0; either side 0xFFFF gives 1")

# ---- EQ-2: two implementations; the chain exempts shields, the standalone does not ----
world_reset()
w(CLT, "<I", 0)                                          # stats index 0 forbids nothing
w(ST + 5, "<B", 1)                                       # selector non-zero: mask and licence skipped (EQ-6 isolates them)
MAIN_BOW, SHIELD, OFF_OK, OFF_BAD = 0x1020, 0x10D5, 0x10D6, 0x10D7
define(MAIN_BOW, 0, 3, partner=23)                       # requires ammunition (23)
define(SHIELD, 1, 0x12)
define(OFF_OK, 1, 23)
define(OFF_BAD, 1, 24)
e2 = {"chain(shield | bow)": chain(ST, MAIN_BOW, 1, SHIELD), "partner(shield, bow)": partner(SHIELD, MAIN_BOW),
      "chain(ammo23 | bow)": chain(ST, MAIN_BOW, 1, OFF_OK), "chain(ammo24 | bow)": chain(ST, MAIN_BOW, 1, OFF_BAD),
      "chain(ammo24 | empty main)": chain(ST, 0xFFFF, 1, OFF_BAD), "partner(ammo24, 0xFFFF)": partner(OFF_BAD, 0xFFFF)}
record("EQ2_shield_exempt_only_inline", e2 == {"chain(shield | bow)": 1, "partner(shield, bow)": 0, "chain(ammo23 | bow)": 1,
                                                "chain(ammo24 | bow)": 0, "chain(ammo24 | empty main)": 1, "partner(ammo24, 0xFFFF)": 1},
       results=e2, note="the chain admits a shield whatever the main hand requires; the standalone refuses it; the non-shield partner "
                        "rule agrees in both; an empty main hand passes both")

# ---- EQ-3: +0x07 bits 7..5 = slot, bit 4 = licence exemption ----
world_reset()
w(CLT, "<I", 0)
ITEM = 0x1030
define(ITEM, 2, FREE)
w(ST + 5, "<B", 1)
e3_slot = {"in slot 2": chain(ST, 0x1000, 2, ITEM), "in slot 1": chain(ST, 0x1000, 1, ITEM), "in slot 3": chain(ST, 0x1000, 3, ITEM)}
w(ST + 5, "<B", 0)
lic_plain = run(LICENCE, ST, ITEM)
plain_board = [c for c in calls if c[0] == "board"]
define(ITEM, 2, FREE, exempt=True)
lic_exempt = run(LICENCE, ST, ITEM)
exempt_board = [c for c in calls if c[0] == "board"]
record("EQ3_packed_slot_and_exemption", e3_slot == {"in slot 2": 1, "in slot 1": 0, "in slot 3": 0} and lic_plain == 0
       and len(plain_board) == 1 and lic_exempt == 1 and not exempt_board,
       slot=e3_slot, licence_without_exemption=lic_plain, licence_with_bit4=lic_exempt,
       note="bits 7..5 = 2 is eligible in slot 2 only; with no licence bits the gate returns 0 through the board lookup; bit 4 set "
            "returns 1 without the board lookup")

# ---- EQ-5: the class mask forbids ----
world_reset()
w(ST + 5, "<B", 0)
LICENSED = 0x1040
define(LICENSED, 0, 7)
w(LIT + 8, "<H", LICENSED)                              # licence record 0 grants it; stats bit 0 of +0x194 holds record 0
w(ST + 0x194, "<B", 1)
w(CLT, "<I", 0)
e5 = {"mask 0": chain(ST, 0xFFFF, 0, LICENSED)}
w(CLT, "<I", 1 << 7)
e5["bit 7 set (item class 7)"] = chain(ST, 0xFFFF, 0, LICENSED)
w(CLT, "<I", ~(1 << 7) & 0xFFFFFFFF)
e5["all bits but 7"] = chain(ST, 0xFFFF, 0, LICENSED)
w(CLT, "<I", 0)
w(ST + 0x194, "<B", 0)
e5["mask 0, licence bit clear"] = chain(ST, 0xFFFF, 0, LICENSED)
record("EQ5_forbidden_mask", e5 == {"mask 0": 1, "bit 7 set (item class 7)": 0, "all bits but 7": 1, "mask 0, licence bit clear": 0},
       results=e5, note="the bit for the item's class SET rejects; every other bit set still admits; the licence board is the last test")

# ---- EQ-6: stats[+5] non-zero bypasses mask and licence; stats[+4] > 6 bypasses the licence ----
world_reset()
w(CLT, "<I", 0xFFFFFFFF)
define(LICENSED, 0, 7)
e6 = {}
w(ST + 5, "<B", 0)
e6["selector 0, all forbidden"] = chain(ST, 0xFFFF, 0, LICENSED)
w(ST + 5, "<B", 2)
e6["selector 2, all forbidden, no licence"] = chain(ST, 0xFFFF, 0, LICENSED)
e6["licence gate, selector 2"] = run(LICENCE, ST, LICENSED)
w(ST + 5, "<B", 0)
e6["licence gate, index 0, no licence"] = run(LICENCE, ST, LICENSED)
lic_idx = {}
for k in (6, 7, 0x27):
    lic_idx[k] = run(LICENCE, stats(k), LICENSED)
e6["licence gate by stats[+4]"] = lic_idx
record("EQ6_selector_and_index_bypass", e6 == {"selector 0, all forbidden": 0, "selector 2, all forbidden, no licence": 1,
                                                "licence gate, selector 2": 1, "licence gate, index 0, no licence": 0,
                                                "licence gate by stats[+4]": {6: 0, 7: 1, 0x27: 1}},
       results=e6, note="selector non-zero admits past a mask that forbids everything and an empty licence board; the gate alone also "
                        "returns 1 for it and for stats[+4] > 6 (6 still needs the board)")

# ---- EQ-7: class 6 in the chain, class 1 in the gate; class 1 re-dispatches to 6 for 0x1xxx ids; the gate's one 0 exit ----
world_reset()
w(CLT, "<I", 0)
define(LICENSED, 0, 7)
w(LIT + 8, "<H", LICENSED)
w(ST + 0x194, "<B", 1)
chain(ST, 0xFFFF, 0, LICENSED)
seq = [c for c in calls if c[0] in ("validate", "class6_arm")]
beyond = 0x1000 + COUNT
out_of_range = {"chain": chain(ST, 0xFFFF, 0, beyond), "gate": run(LICENCE, ST, beyond)}
e7_ok = (seq == [("validate", 6, LICENSED), ("class6_arm",), ("validate", 1, LICENSED), ("class6_arm",)]
         and out_of_range == {"chain": 0, "gate": 0})
record("EQ7_two_classes_one_range", e7_ok, validator_sequence=[list(map(str, c)) for c in seq], id_past_count=out_of_range,
       note="the chain validates class 6 and the gate class 1; class 1 on a 0x1xxx id is looked up (00309440: family code 6) and "
            "re-dispatched to the SAME class-6 range test; an id past the header count fails both, and that is the gate's 0 exit")

# ---- the wrapper 00317B20: stats by index, and the owned test always on (kind 0 = total - reserved) ----
world_reset()
w(CLT, "<I", 0)
w(ST + 5, "<B", 1)
OWNED_ITEM = 0x1050
define(OWNED_ITEM, 0, FREE)
own = {}
for label, word in (("total 1, reserved 0", 0x0001), ("total 1, reserved 1", 0x0401), ("total 0", 0), ("total 3, reserved 2", 0x0803)):
    w(OWNED + 2 * (OWNED_ITEM - 0x1000), "<H", word)
    own[label] = {"wrapper": run(WRAP, 0, MAIN, OWNED_ITEM, 0), "chain, owned test off": chain(ST, 0xFFFF, 0, OWNED_ITEM, 0),
                  "chain, owned test on": chain(ST, 0xFFFF, 0, OWNED_ITEM, 1)}
own["wrapper, index 0x28"] = run(WRAP, 0x28, MAIN, OWNED_ITEM, 0)
record("wrapper_owned_test_always_on", own == {
    "total 1, reserved 0": {"wrapper": 1, "chain, owned test off": 1, "chain, owned test on": 1},
    "total 1, reserved 1": {"wrapper": 0, "chain, owned test off": 1, "chain, owned test on": 0},
    "total 0": {"wrapper": 0, "chain, owned test off": 1, "chain, owned test on": 0},
    "total 3, reserved 2": {"wrapper": 1, "chain, owned test off": 1, "chain, owned test on": 1},
    "wrapper, index 0x28": 0}, results=own,
       note="the wrapper always passes 1 as the chain's fifth argument; the count tested is 002FD8D0 mode 0 = (word & 0x3FF) - "
            "(word >> 10), the inventory contract's kind-0 'available' = total - reserved, and must be >= 1; an index above 0x27 is refused before the chain")

# ---- EQ-8 and EQ-4: the recommender ----
def trace():
    """The recommender's calls in order, runs of eligibility calls in one slot compressed to [slot, first, last, n]."""
    out = []
    for c in calls:
        if c[0] == "wrap":
            if out and out[-1][0] == "wrap" and out[-1][1] == c[3]:
                out[-1][3], out[-1][4] = "%04X" % c[2], out[-1][4] + 1
            else:
                out.append(["wrap", c[3], "%04X" % c[2], "%04X" % c[2], 1])
        elif c[0] in ("partner", "compare"):
            out.append([c[0]] + ["%04X" % x for x in c[1:3]] + list(c[3:]))
    return out


world_reset()
w(CLT, "<I", 0)
w(ST + 5, "<B", 1)                                       # selector: the mask and licence are EQ-5/EQ-6's; here only the order
w(STATS_BLOCK + 0x5A7E, "<B", 0)                         # character 0 -> stats index 0 (mode 3)
w(ST + 0x50, "<5H", 0xFFFF, SHIELD, 0xFFFF, 0xFFFF, 0x1234)
define(MAIN_BOW, 0, 3, partner=23)                       # the only slot-0 candidate besides 0x1000's short-circuit
define(SHIELD, 1, 0x12)                                  # slot 1, a shield: the chain admits it (EQ-2)
define(OFF_OK, 1, 23)                                    # slot 1, ammunition class 23
define(0x1190, 1, 23)                                    # slot 1, class 23, inside 0x1184..0x11A3
del calls[:]
ok8 = S.call(RECOMMEND, 0, OUT)
out8 = ["%04X" % v for v in struct.unpack("<5H", bytes(uc.mem_read(OUT, 10)))]
t8 = trace()
want8 = [["wrap", 0, "1000", "1000", 1], ["compare", "FFFF", "1000", 0], ["wrap", 0, "1001", "1020", 32],
         ["compare", "1000", "1020", 0],
         ["wrap", 1, "1184", "1190", 13], ["compare", "FFFF", "1190", 0], ["wrap", 1, "1191", "11A3", 19],
         ["wrap", 0, "1021", "10C7", 167],
         ["partner", "10D5", "1020"],
         ["wrap", 1, "10C8", "10D5", 14], ["partner", "10D5", "1020"],
         ["wrap", 1, "10D6", "10D6", 1], ["partner", "10D6", "1020"], ["compare", "FFFF", "10D6", 1],
         ["wrap", 1, "10D7", "1190", 186], ["partner", "1190", "1020"], ["compare", "10D6", "1190", 0],
         ["wrap", 1, "1191", "11A3", 19],
         ["wrap", 2, "10DC", "1117", 60], ["wrap", 3, "1118", "1153", 60]]
record("EQ8_EQ4_recommender_order", ok8 and out8 == ["1020", "1190", "FFFF", "FFFF", "1234"] and t8 == want8, out=out8, trace=t8,
       note="slot 0 is decided first (0x1020 beats 0x1000); the slot-0 epilogue drops nothing new but tests the CARRIED off-hand "
            "0x10D5 against 0x1020 before slot 1 starts; slot 1 walks 0x10C8..0x11A3 (EQ-4's 0x11A4 bound) and every candidate the "
            "chain admits, the shield included, is re-tested by 002F7EC0 at 002FA013 against out[0]; ids 0x1184..0x11A3 compare in "
            "mode 0; slots 2/3 walk their ranges; out[4] = 0x1234 is passed through")

# EQ-8b: nothing eligible in slot 0 (stats[+4] = 0x28 makes the wrapper refuse every id) -> the epilogue forces 0x1000
world_reset()
w(STATS_BLOCK + 0x5A7E + 2, "<B", 1)                     # character 1 -> stats index 1
w(stats(1) + 4, "<B", 0x28)
w(stats(1) + 0x50, "<5H", 0xFFFF, SHIELD, 0xFFFF, 0xFFFF, 0xFFFF)
define(SHIELD, 1, 0x12)
del calls[:]
ok8b = S.call(RECOMMEND, 1, OUT)
out8b = ["%04X" % v for v in struct.unpack("<5H", bytes(uc.mem_read(OUT, 10)))]
t8b = trace()
record("EQ8b_empty_main_forced_then_offhand_dropped", ok8b and out8b == ["1000", "FFFF", "FFFF", "FFFF", "FFFF"]
       and t8b[0] == ["wrap", 0, "1000", "10C7", 200] and ["partner", "10D5", "1000"] in t8b, out=out8b, trace=t8b,
       note="no slot-0 candidate is admitted: the epilogue writes 0x1000, then 002F7EC0(0x10D5, 0x1000) fails and the carried shield "
            "becomes 0xFFFF")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
