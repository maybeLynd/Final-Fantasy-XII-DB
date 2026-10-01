"""S-08 I5 (OPUS, 2026-09-26): 'chunking is gate-dependent, not size-only' (CONTRACT-resource-request-queue.md I5), executed over
block 330's world (check.py, imported: its cases run first, unchanged) - the chunk-aware enqueue 0032E620(kind, id, dest, bytes,
desc) with its gate 003EB0D0 (is a BGM stream active: the byte +0x31 of the stream descriptor 02B5E0E0) and the requester
0032E870 as shipped.

The pool is filled with 0xAA before construction so the slot fields the constructor does not write (+0x30, +0x34; I1) carry a
known pattern. Cases:
 gate clear, large request (0x123456 bytes): the request stays whole (+0x28 = 0x123456), chunk-enable +0x22 = 0, and the unused
   cap / remaining storage +0x30 / +0x34 keep the 0xAA pattern;
 gate set, large request: chunk-enable 1, cap +0x30 = 0x80000, remaining +0x34 = the prior byte count, first part +0x28 =
   0x80000 (the signed minimum);
 gate set, small request (0x1000): first part 0x1000, remaining 0x1000, cap 0x80000;
 gate set, null descriptor: the local descriptor is zeroed and the chunked slot is still built.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes i5_result.json.
"""
import json
import os

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
ENQ, GATE, STREAM = 0x32E620, 0x3EB0D0, 0x2B5E0E0
W.ALLOWED |= W.closure(ENQ) | {ENQ} | W.closure(GATE) | {GATE}


def slot(rid, off, fmt):
    return C.r(C.POOL + (rid & 0x3F) * 0x80 + off, fmt)[0]


def enq(gate, nbytes, desc=True):
    uc.mem_write(C.POOL, b"\xAA" * 0x2000)
    C.run(C.CTOR)
    uc.mem_write(STREAM, bytes(0x70))
    C.w(STREAM + 0x31, "<B", 1 if gate else 0)
    C.w(C.DESC, "<iIIIQQ", 0x1234, 0, 0x55, 0, 0, 0)
    rid = C.run(ENQ, 0x24, 3, C.DEST, nbytes, stack=(C.DESC if desc else 0,)) & 0xFFFFFFFF
    return {"id": "%X" % rid, "part_28": "%X" % slot(rid, 0x28, "<I"), "chunk_22": slot(rid, 0x22, "<H"), "cap_30": "%X" % slot(rid, 0x30, "<I"),
            "remaining_34": "%X" % slot(rid, 0x34, "<I"), "offset_2C": "%X" % slot(rid, 0x2C, "<I")}


a = enq(False, 0x123456)
b = enq(True, 0x123456)
c = enq(True, 0x1000)
d = enq(True, 0x123456, desc=False)
cases = {
    "gate_clear_request_whole_and_unused_storage_untouched": a["part_28"] == "123456" and a["chunk_22"] == 0
        and a["cap_30"] == "AAAAAAAA" and a["remaining_34"] == "AAAAAAAA",
    "gate_set_large_request_chunked_at_0x80000": b["chunk_22"] == 1 and b["cap_30"] == "80000" and b["remaining_34"] == "123456"
        and b["part_28"] == "80000",
    "gate_set_small_request_first_part_is_the_whole": c["chunk_22"] == 1 and c["cap_30"] == "80000" and c["remaining_34"] == "1000"
        and c["part_28"] == "1000",
    "gate_set_null_descriptor_still_chunked": d["chunk_22"] == 1 and d["cap_30"] == "80000" and d["remaining_34"] == "123456",
}
res = {"ok": all(cases.values()), "cases": cases, "gate_clear": a, "gate_set_large": b, "gate_set_small": c, "gate_set_null_desc": d}
json.dump(res, open(os.path.join(HERE, "i5_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-58s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps([a, b, c, d]))
