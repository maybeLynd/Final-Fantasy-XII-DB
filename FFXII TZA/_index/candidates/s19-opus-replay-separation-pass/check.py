"""S-19: execute CONTRACT-separation-pass.md's six bodies - the reset 003DAA40, the walk 003DAC70, the pair set 003DAAB0, the visit
003DAB50, the resolver 00314F50 (through the pass callback 00314F30) and the clear 003DA9F0 - over bodies allocated by the shipped
pool allocator 003DA8A0 and registered by the shipped 003DB020, and test P-1..P-7 (OPUS, 2026-09-25, block 337).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The contract's section 13: "No experiment executes these six bodies".
world.py (block 318/319's builder - it runs the body-pool initialiser 003DAE30 -, Session; block 337 adds faithful named bridges
for the CRT's double sqrt, _isnan and _finite, which the resolver imports) supplies the image, the IAT traps and the named
bridges. No application stub and no stop boundary.
Fixtures: the bodies' authored fields (layer +6, weight +8, position +0x30, heights +0xE0/+0xE4, radii +0xF0/+0xF4, masks
+0x110/+0x114, owner +0x119), the radii handed to the registration, and the two globals 02B40530 / 02B40534 whose conjunction
003B7730 gates the cell step of the registration.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ALLOC, REGISTER, RESET, WALK, CALLBACK, RESOLVE, CLEAR = 0x3DA8A0, 0x3DB020, 0x3DAA40, 0x3DAC70, 0x314F30, 0x314F50, 0x3DA9F0
for f in (ALLOC, REGISTER, RESET, WALK, CALLBACK, RESOLVE, CLEAR):
    W.ALLOWED |= {f} | W.closure(f)
W.ALLOWED |= {0x16D6A0}
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
RAD = 0x76300000


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


w(0x2B40530, "<I", 1)
w(0x2B40534, "<I", 1)
w(RAD, "<ff", 1.0, 1.0)
bodies = []
for _ in range(3):
    assert S.call(ALLOC)
    bodies.append(uc.reg_read(UC_X86_REG_RAX))
A, B, C = bodies

resolver_calls = []


def on_resolve(u, a, n, _):
    x, y = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
    resolver_calls.append({"A": bodies.index(x) if x in bodies else "%X" % x, "B": bodies.index(y) if y in bodies else "%X" % y,
                           "mode": u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF,
                           "A_push_at_entry": list(r(x + 0x100, "<f")) if x in bodies else None,
                           "B_push_at_entry": list(r(y + 0x100, "<f")) if y in bodies else None})


uc.hook_add(UC_HOOK_CODE, on_resolve, begin=RESOLVE, end=RESOLVE)


def setup(xs, weights=(1.0, 1.0, 1.0), masks=(0, 0, 0), owners=(0, 0, 0), layers=(0, 0, 0)):
    for i, b in enumerate(bodies):
        uc.mem_write(b + 0x6, bytes(2))
        w(b + 6, "<B", layers[i])
        w(b + 8, "<f", weights[i])
        uc.mem_write(b + 0x18, bytes(16))
        w(b + 0x30, "<fff", xs[i], 0.0, 0.0)
        w(b + 0xE0, "<ff", 2.0, 0.0)
        uc.mem_write(b + 0xE8, bytes(8))
        w(b + 0xF0, "<ff", 1.0, 1.0)
        uc.mem_write(b + 0x100, bytes(12))
        w(b + 0x110, "<II", masks[i], 0)
        w(b + 0x119, "<B", owners[i])


def tick(registered=(0, 1, 2)):
    del resolver_calls[:]
    assert S.call(RESET)
    for i in registered:
        b = bodies[i]
        assert S.call(REGISTER, b, 0, 0, RAD, xmm={1: r(b + 0x30, "<f")[0], 2: 0.0})
    assert S.call(WALK, CALLBACK)


def state(i):
    b = bodies[i]
    return {"push_x": r(b + 0x100, "<f")[0], "pushed": r(b + 0xEC, "<B")[0], "contacts": r(b + 0xED, "<B")[0],
            "immovable": r(b + 0xEE, "<B")[0], "pairbits": "%X" % r(b + 0x18, "<Q")[0], "active": r(b + 7, "<B")[0]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- P-2 / P-5: three overlapping bodies; each pair once, and later pairs read earlier pushes ----
setup((0.0, 0.5, 1.0))
tick()
pairs = [(c["A"], c["B"]) for c in resolver_calls]
p2 = sorted(pairs) == [(0, 1), (0, 2), (1, 2)] and len(pairs) == 3
later_sees_earlier = any((c["A_push_at_entry"] and c["A_push_at_entry"][0] != 0.0) or (c["B_push_at_entry"] and c["B_push_at_entry"][0] != 0.0)
                         for c in resolver_calls[1:])
record("P2_each_pair_once", p2, pairs=pairs, note="three mutually overlapping bodies: the resolver runs for (0,1), (0,2), (1,2), once each")
record("P5_order_dependent", p2 and later_sees_earlier and resolver_calls[0]["A_push_at_entry"] == [0.0], calls=resolver_calls,
       final=[state(i) for i in range(3)],
       note="the first pair sees zero accumulators; a later pair's resolver entry already holds a push written by an earlier pair "
            "in the same pass - read-then-write on the same accumulators")

# ---- P-1 / P-3: an unregistered body is not active; and WHEN a remembered pair is visited ----
# 003DAB50 walks the CANDIDATE set byte by byte (003DAB94-003DAC48); inside a non-zero candidate byte it steps bit by bit only
# while candidate bits remain (shr rbp,1 / jne 003DAC11), calling the resolver where the candidate bit OR the remembered bit
# (+0x18) is set (003DABCF-003DABDD). Three cases pin that down.
def reset_push():
    for b_ in bodies:
        uc.mem_write(b_ + 0x100, bytes(12))


p3 = {}
# (a) remembered B, candidate set empty
setup((0.0, 0.5, 5.0))
tick(registered=(0, 1))
rem_a = state(0)["pairbits"]
reset_push()
tick(registered=(0,))
p3["a: remembered B, no candidate"] = {"remembered": rem_a, "calls": [(c_["A"], c_["B"]) for c_ in resolver_calls],
                                       "pairbits_after": state(0)["pairbits"], "B_active": state(1)["active"]}
# (b) remembered B (bit 1) below a candidate C (bit 2) in the same byte
setup((0.0, 0.5, 0.5))
tick(registered=(0, 1))
rem_b = state(0)["pairbits"]
reset_push()
tick(registered=(0, 2))
p3["b: remembered B below candidate C"] = {"remembered": rem_b, "calls": [(c_["A"], c_["B"]) for c_ in resolver_calls],
                                            "pairbits_after": state(0)["pairbits"]}
# (c) remembered C (bit 2) above the only candidate B (bit 1)
setup((0.0, 0.5, 0.5))
tick(registered=(0, 2))
rem_c = state(0)["pairbits"]
reset_push()
tick(registered=(0, 1))
p3["c: remembered C above candidate B"] = {"remembered": rem_c, "calls": [(c_["A"], c_["B"]) for c_ in resolver_calls],
                                            "pairbits_after": state(0)["pairbits"]}
pa, pb, pc = p3["a: remembered B, no candidate"], p3["b: remembered B below candidate C"], p3["c: remembered C above candidate B"]
record("P1_unregistered_not_active", pa["B_active"] == 0, note="after the reset, a body that did not register has +7 = 0 and no cell bit")
record("P3_remembered_pairs_visited_only_under_candidates",
       pa["remembered"] == "2" and pa["calls"] == [] and pa["pairbits_after"] == "2"
       and pb["remembered"] == "2" and [x for x in pb["calls"] if x[0] == 0] == [(0, 1), (0, 2)] and pb["pairbits_after"] == "4"
       and (1, 2) in pb["calls"]
       and pc["remembered"] == "4" and pc["calls"] == [(0, 1)] and pc["pairbits_after"] == "6", cases=p3,
       note="(a) with no candidate the remembered pair is NOT retried and its bit PERSISTS; (b) a remembered bit below a candidate in "
            "the same byte is retried (refused: not active) and dropped; (c) a remembered bit above the highest candidate is never "
            "visited and persists beside the new pair. The walk also initiates from an UNREGISTERED body still on the allocated "
            "list: in (b) B, with last tick's cell bits, gets C as a candidate, and the resolver refuses (B, C)")

# ---- P-4: mode 0 skips the active test; mode 1 does not ----
setup((0.0, 0.5, 5.0))
tick(registered=(0,))                         # B inactive this tick
OUT = 0x76310000
p4 = {}
for mode in (1, 0):
    uc.mem_write(OUT, bytes(0x40))
    w(A + 0x100, "<fff", 0.0, 0.0, 0.0)
    w(B + 0x100, "<fff", 0.0, 0.0, 0.0)
    S.call(RESOLVE, A, B, mode, OUT)
    p4[mode] = {"returned": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "A_push": r(A + 0x100, "<f")[0]}
record("P4_mode_selects_active_test", p4[1]["returned"] == 0 and p4[0]["returned"] != 0, cases=p4,
       note="B not active this tick: in push mode (1) the resolver refuses; in query mode (0) the active test is skipped and the pair "
            "resolves")

# ---- P-4 refusals: layer and owner ----
ref = {}
for label, kw in (("layers differ", dict(layers=(0, 1, 0))), ("equal non-zero owners", dict(owners=(7, 7, 0))),
                  ("owners both zero", dict(owners=(0, 0, 0)))):
    setup((0.0, 0.5, 5.0), **kw)
    tick(registered=(0, 1))
    ref[label] = {"A_push": state(0)["push_x"], "pairbits": state(0)["pairbits"]}
record("P4_layer_and_owner_refusals", ref["layers differ"]["A_push"] == 0.0 and ref["equal non-zero owners"]["A_push"] == 0.0
       and ref["owners both zero"]["A_push"] != 0.0, cases=ref,
       note="different layers, or equal non-zero owner bytes, refuse the pair; two zero owners do pair")

# ---- P-7: the weight split's three outcomes ----
p7 = {}
for label, masks in (("A mask byte greater (w = 0)", (1, 0, 0)), ("A mask byte smaller (w = 1)", (0, 1, 0)), ("equal (shared)", (0, 0, 0))):
    setup((0.0, 0.5, 5.0), masks=masks)
    tick(registered=(0, 1))
    p7[label] = {"A": state(0), "B": state(1)}
g0, g1, sh = p7["A mask byte greater (w = 0)"], p7["A mask byte smaller (w = 1)"], p7["equal (shared)"]
p7_ok = (sh["A"]["contacts"] == 1 and sh["B"]["contacts"] == 1 and sh["A"]["immovable"] == 0 and sh["B"]["immovable"] == 0
         and sh["A"]["push_x"] == -sh["B"]["push_x"] != 0
         and sorted([g0["A"]["contacts"], g0["B"]["contacts"]]) == [0, 1] and sorted([g1["A"]["contacts"], g1["B"]["contacts"]]) == [0, 1]
         and (g0["A"]["push_x"] == 0.0) != (g0["B"]["push_x"] == 0.0) and (g1["A"]["push_x"] == 0.0) != (g1["B"]["push_x"] == 0.0))
record("P7_three_weight_outcomes", p7_ok, cases=p7,
       note="equal masks: the push is shared and BOTH contact counters advance, both immovable markers clear; a strictly larger or "
            "smaller mask byte puts the whole push on one body and advances ONE body's counter and marker")

# ---- P-6: the clear zeroes exactly the push accumulators and flags ----
b = A
uc.mem_write(b, b"\xAA" * 0x130)
assert S.call(CLEAR, b)
after = bytes(uc.mem_read(b, 0x130))
zeroed = sorted(i for i in range(0x130) if after[i] == 0)
spans = []
for i in zeroed:
    if spans and spans[-1][1] == i:
        spans[-1][1] = i + 1
    else:
        spans.append([i, i + 1])
record("P6_clear_extent", spans == [[0xE8, 0xEF], [0x100, 0x10C]],
       zeroed=["+%X..+%X" % (a, e - 1) for a, e in spans],
       note="003DA9F0 zeroes +0xE8..+0xEE (push length, pushed, contacts, immovable) and +0x100..+0x10B (the push), nothing else")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
