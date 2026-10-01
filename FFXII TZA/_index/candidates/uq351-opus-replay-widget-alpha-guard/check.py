"""UQ-351 (OPUS, 2026-09-25): what makes `word [rcx+0x58]` non-zero for the nine-patch guard 00392A00.

Static claim tested. Every one of the guard's four callers (002A62DF, 002C0916, 002C0D5A, 00573F6D) passes
`[widget + 0x38]`. That qword is written only by the widget-tree draw pass 00245E60: 00245EB0 stores the address of a
0xA0-byte stack draw record that 002D8C00 has just built, and 002463BE zeroes it when the node's draw ends.
- 002D8C00 zero-fills the record and sets +0x5A (the RGB scale) to 0x80, so +0x58 (the alpha scale, the fourth channel
  on the rectangle page) starts at 0.
- For a ROOT node (widget +0x10 parent null), 00245ED3/00245EF0 copies the node's byte +0xA0 into the record's +0x58.
- For a CHILD, 00246480 puts the node's +0xA0 into its out-record +0x24 (002464F5), and 00245F81..00245F9C stores
  (parent record +0x58 * that) >> 7. +0x5A composes the same way from byte +0xA1 (00245F38..00245F49).
So the guard's word is the node's composed opacity: non-zero exactly while every ancestor's and the node's own +0xA0 is
non-zero (the constructor 002465F0 sets 0x80 = 1.0 at 0024670A), before any message-3 handler modulation.

Evidence class: NATIVE-REPLAY (unicorn), live_game false, via world.py's Session. No application stub. The guard's
taken branch into 00392A10 is a recorded STOP BOUNDARY (outside the allowed set), not a stub.
Cases:
 A  002D8C00 over a 0xA5-poisoned record: +0x58 == 0 is an explicit write, +0x5A == 0x80.
 B  00392A00 with record +0x58 = 0 returns without entering 00392A10; with 0x80 it enters 00392A10.
 C  00245E60 over a two-node tree (root R, child C, no handlers): the record each node publishes at +0x38 is captured at
    the recursion / child-loop point, and its +0x58 / +0x5A are checked against R.A0, (R.A0 * C.A0) >> 7 and
    (0x80 * C.A1) >> 7, over a grid that includes 0 and a root +0xA1 other than 0x80 (the root arm leaves +0x5A at 0x80).
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
INIT, GUARD, BODY, PASS = 0x2D8C00, 0x392A00, 0x392A10, 0x245E60
W.ALLOWED |= W.closure(INIT) | {GUARD} | W.closure(PASS) | W.closure(0x217150)   # 00217150: the matrix multiply, reached by a thunk's tail jmp
W.ALLOWED.discard(BODY)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
BUF = 0x76280000
rd16 = lambda a: struct.unpack("<h", bytes(uc.mem_read(a, 2)))[0]
rd64 = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]

# A - the record builder
uc.mem_write(BUF, b"\xA5" * 0xA0)
okA = S.call(INIT, BUF)
A = {"returned": okA, "+0x58": rd16(BUF + 0x58), "+0x5A": rd16(BUF + 0x5A), "+0x5C": "%08X" % struct.unpack("<I", bytes(uc.mem_read(BUF + 0x5C, 4)))[0]}
passA = okA and A["+0x58"] == 0 and A["+0x5A"] == 0x80

# B - the guard, both ways
B = {}
for alpha in (0, 0x80, 1, -1):
    uc.mem_write(BUF + 0x58, struct.pack("<h", alpha))
    ok = S.call(GUARD, BUF, 0, 0)
    B[str(alpha)] = {"returned": ok, "entered_body": BODY in [int(x, 16) for x in S.st["bad"]]}
passB = (B["0"] == {"returned": True, "entered_body": False}
         and all(B[k]["entered_body"] and not B[k]["returned"] for k in ("128", "1", "-1")))

# C - the draw pass over a two-node tree
R, C, PARENT_RECT = 0x76290000, 0x76291000, 0x76292000
seen = {}


def grab(tag):
    def h(u, a, n, _):
        from unicorn.x86_const import UC_X86_REG_RBX
        node = u.reg_read(UC_X86_REG_RBX)
        rec = rd64(node + 0x38)
        if rec:
            seen[(tag, "%X" % node)] = (rd16(rec + 0x58), rd16(rec + 0x5A))
    return h


uc.hook_add(UC_HOOK_CODE, grab("root, at the child loop"), begin=0x24635C, end=0x24635C)
uc.hook_add(UC_HOOK_CODE, grab("after the +0x58 store"), begin=0x245FA0, end=0x245FA0)   # the instruction after 00245F9C
# STOP BOUNDARY (recorded, not stubbed): after its record is composed, the child's draw reaches the screen-configuration
# getter 001DDAB0 (-> [01F82D18]) through 001844D0, and 001DD8C4 reads the first dword of that singleton, which this world
# does not build. The record is complete before that point; nothing is fabricated to run past it, so the end-of-draw
# clear `mov qword [rbx+0x38], 0` at 002463BE is STATIC evidence here, not executed.
BOUNDARY = ["001DD8C0", "001DD8C4"]
in_stack = lambda v: W.STACK <= v < W.STACK + W.STACK_SZ
cases = []
grid = [(0x80, 0x80, 0x80, 0x80), (0x40, 0x40, 0x80, 0x80), (0x80, 0x20, 0x40, 0x80), (0, 0x80, 0x80, 0x80), (0x80, 0, 0x80, 0x80),
        (0x7F, 0x7F, 0xFF, 0x80), (0x80, 0x80, 0x40, 0x20)]   # the last varies R.A1: the root arm does not read it
for ra0, ca0, ca1, ra1 in grid:
    for base in (R, C):
        uc.mem_write(base, bytes(0x200))
    # tree links (CONTRACT-widget-object: +0x10 parent, +0x18 first child, +0x20 next sibling), flags bits 0 and 2
    uc.mem_write(R + 0x40, struct.pack("<I", 5)); uc.mem_write(C + 0x40, struct.pack("<I", 5))
    uc.mem_write(R + 0x18, struct.pack("<Q", C)); uc.mem_write(C + 0x10, struct.pack("<Q", R))
    for node, a0, a1 in ((R, ra0, ra1), (C, ca0, ca1)):
        uc.mem_write(node + 0x9C, struct.pack("<HH", 0x40, 0x20))       # own size, so the clip has an area
        uc.mem_write(node + 0xA0, bytes([a0, a1 & 0xFF, 0xFF]))
    xform = PARENT_RECT
    uc.mem_write(xform, struct.pack("<16f", 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
    seen.clear()
    ok = S.call(PASS, R, xform)
    rp, cp = rd64(R + 0x38), rd64(C + 0x38)
    cases.append({"R.A0": ra0, "R.A1": ra1, "C.A0": ca0, "C.A1": ca1, "returned": ok, "faults": list(S.st["faults"]), "bad": list(S.st["bad"]),
                  "last pcs": ["%08X" % x for x in list(S.st["trace"])[-2:]],
                  "root record (+0x58, +0x5A)": seen.get(("root, at the child loop", "%X" % R)),
                  "child record (+0x58, +0x5A)": seen.get(("after the +0x58 store", "%X" % C)),
                  "expected root": [ra0, 0x80], "expected child": [(ra0 * ca0) >> 7, (0x80 * ca1) >> 7],
                  "R+0x38 is a stack record": in_stack(rp), "C+0x38 is a stack record": in_stack(cp), "distinct records": rp != cp})
passC = all(c["last pcs"] == BOUNDARY and c["faults"][:1] == ["00000000"] and not c["bad"]
            and list(c["root record (+0x58, +0x5A)"] or ()) == c["expected root"]
            and list(c["child record (+0x58, +0x5A)"] or ()) == c["expected child"]
            and c["R+0x38 is a stack record"] and c["C+0x38 is a stack record"] and c["distinct records"] for c in cases)
ok = passA and passB and passC
res = {"ok": ok, "A_record_builder": A, "B_guard": B, "C_draw_pass": cases, "pass": {"A": passA, "B": passB, "C": passC}}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
print("ok" if ok else "NOT ok", json.dumps(res["pass"]))
print(json.dumps(A), json.dumps(B))
for c in cases:
    print(json.dumps(c))
