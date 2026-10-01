"""S-37 I-4 (OPUS, 2026-09-26): "measurement and drawing are the same code path, and the recursion is the mechanism" -
CONTRACT-text-control-codes-and-dyngeo-draw.md I-4, executed over block 313's harness (check.py, imported: its six cases run
first, unchanged).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub; ALLOWED = block 313's closures (002B2150 is in
the interpreter's closure). Planted data only: the singleton [01F81200] that the lead-token arms query through 001B5FB0 ->
001B51C0 (a map lookup at +0x30 / +0x40), as an object whose map is empty - block 313's arms 01, 02, 04-07 and 0A stopped on
its absence (a read of 0x40). Observation hooks record each entry of 002AC5F0 (I), 002B2150 (B, with its text argument as an
offset into the input) and 002A9F00 (A), with rsp, so nesting is visible.
Cases:
 S   static, from the image: 002AC5F0 calls 002B2150 at 7 sites and 002A9F00 at 4; 002B2150 calls 002AC5F0 (002B2393) and so
     does 002A9F00 (002AA6A8) - both are callers and callees of the interpreter.
 R1  tokens 02, 05, 0A followed by `09 00`: the interpreter calls 002B2150 on the text after the token (cursor + 1), which
     calls the interpreter again one frame deeper on the `09`; everything returns.
 R4  `02 05 0A 09 00`: I -> B -> I -> B -> I -> B -> I, strictly nested (rsp decreasing at each level), every level
     returning - the spliced text is interpreted by the machinery that is interpreting it, to depth four.
 T   002B2150's stop set: a 0x02 in the spliced text ends the splice with no inner call (`02 02 09 00`).
Not executed: 002A9F00's re-entry - its loop reaches the glyph measure 002AC2F0 first, which needs the font object
0039C4A0 returns (not planted); printable spliced bytes likewise stop at the font.
Writes i4_result.json.
"""
import json
import os
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RDX, UC_X86_REG_RSP

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
INTERP, BSPLICE, ADRAW, G_MGR, MGR = 0x2AC5F0, 0x2B2150, 0x2A9F00, 0x1F81200, C.WORLD + 0x38000


def body(a, n):
    code = C.raw[[ra + a - v for v, vs, ra, rs in C.secs if v <= a < v + rs][0]:][:n]
    return list(Cs(CS_ARCH_X86, CS_MODE_64).disasm(code, a))


sizes = {}
for line in open(C.GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace"):
    p = line.split("\t")
    if p[0] in ("002AC5F0", "002B2150", "002A9F00"):
        sizes[int(p[0], 16)] = int(p[2])
calls = {f: [("%08X" % i.address, i.op_str) for i in body(f, sizes[f]) if i.mnemonic == "call"] for f in sizes}
static = {
    "interp_calls_B": [a for a, t in calls[INTERP] if t == "0x2b2150"],
    "interp_calls_A": [a for a, t in calls[INTERP] if t == "0x2a9f00"],
    "B_calls_interp": [a for a, t in calls[BSPLICE] if t == "0x2ac5f0"],
    "A_calls_interp": [a for a, t in calls[ADRAW] if t == "0x2ac5f0"],
}

seq = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: seq.append(["I", u.reg_read(UC_X86_REG_RSP)]), begin=INTERP, end=INTERP)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: seq.append(["B", u.reg_read(UC_X86_REG_RSP), u.reg_read(UC_X86_REG_RDX) - C.TEXT]),
            begin=BSPLICE, end=BSPLICE)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: seq.append(["A", u.reg_read(UC_X86_REG_RSP)]), begin=ADRAW, end=ADRAW)
uc.ctl_flush_tb()


def run(text):
    C.world()
    uc.mem_write(G_MGR, struct.pack("<Q", MGR))
    del seq[:]
    ok, eax, adv, o2, _ = C.interp(text)
    return {"text": text.hex(), "ok": ok, "eax": eax, "advance": adv, "stopped_at": (C.state["bad"] or C.state["faults"])[:2],
            "sequence": [[x[0], "%X" % x[1]] + x[2:] for x in seq]}


def nested(r, want):
    s = r["sequence"]
    kinds = [x[0] for x in s][:len(want)]
    rsps = [int(x[1], 16) for x in s][:len(want)]
    return kinds == want and all(rsps[i + 1] < rsps[i] for i in range(len(want) - 1))


r1 = {"%02X" % t: run(bytes([t, 0x09, 0x00])) for t in (0x02, 0x05, 0x0A)}
r4 = run(bytes([0x02, 0x05, 0x0A, 0x09, 0x00]))
tstop = run(bytes([0x02, 0x02, 0x09, 0x00]))
cases = {
    "S_static_mutual_calls": len(static["interp_calls_B"]) == 7 and len(static["interp_calls_A"]) == 4
        and static["B_calls_interp"] == ["002B2393"] and len(static["A_calls_interp"]) >= 1,
    "R1_token_splices_cursor_plus_1_and_the_interpreter_reenters": all(
        v["ok"] and nested(v, ["I", "B", "I"]) and v["sequence"][1][2] == 1 for v in r1.values()),
    "R4_mutual_recursion_to_depth_four": r4["ok"] and nested(r4, ["I", "B", "I", "B", "I", "B", "I"])
        and [x[2] for x in r4["sequence"] if x[0] == "B"][:3] == [1, 2, 3],
    "T_a_02_in_the_splice_ends_it_without_an_inner_call": tstop["ok"] and [x[0] for x in tstop["sequence"]] == ["I", "B"],
}
res = {"ok": all(cases.values()), "cases": cases, "static": static, "R1": r1, "R4": r4, "T": tstop}
json.dump(res, open(os.path.join(HERE, "i4_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-64s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
print(json.dumps(r4["sequence"]))
