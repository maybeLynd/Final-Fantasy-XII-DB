"""S-12 P-1, the fresh arm to its end (OPUS, 2026-09-26): 002620E0 with dword[mgr+0x28] == 0 and byte[mgr+0x10] bit 2 clear, run
through the presentation body 0040AAD0 that p12.py keeps as its recorded boundary, to the bit-set 002621A4 and the notifies.

Imports p12.py (with its default boundary): p12's cases run first, unchanged, and rewrite p12_result.json identically. Then
this file lifts that one boundary - 0040AAD0 and its static closure join ALLOWED - and plants the one object the presentation
reaches that this world lacks: the 0x80-record pool (stride 0x70) behind [02B3F528], which 003AB960 scans for a free slot,
as a zeroed block (planted data). No application stub.
Evidence class: NATIVE-REPLAY (unicorn), live_game false.
Case:
 P1  the fresh arm runs the roll 0025ACA0, the apply 0026D910, the presentation 0040AAD0, then SETS byte[mgr+0x10] bit 2 at
     002621A4 itself, and still notifies 003601C0(0x0B) then (0x0C) - the call returns normally.
Writes p1fresh_result.json.
"""
import json
import os
import struct

os.environ["P12_PRESENT_BOUNDARY"] = "1"
import p12 as P
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc = P.uc
W.ALLOWED |= W.closure(P.PRESENT) | {P.PRESENT}
POOL, G_POOL = 0x76600000, 0x2B3F528
uc.mem_map(POOL, 0x4000)
uc.mem_write(POOL, bytes(0x4000))
uc.mem_write(G_POOL, struct.pack("<Q", POOL))
fr = P.arm(0, 0)
names = [e[0] for e in fr["events"]]
notifies = [e for e in fr["events"] if e[0] == "notify 003601C0"]
cases = {"P1_fresh_arm_sets_the_bit_itself_and_notifies":
         fr["returned"] and names[:4] == ["roll 0025ACA0", "apply 0026D910", "presentation 0040AAD0", "set bit 002621A4"]
         and (fr["b10_after"] & 4) == 4 and notifies == [["notify 003601C0", 0xB], ["notify 003601C0", 0xC]]}
res = {"ok": all(cases.values()), "cases": cases, "fresh": fr, "pool_slot0_after": bytes(uc.mem_read(POOL, 0x10)).hex()}
json.dump(res, open(os.path.join(HERE, "p1fresh_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-50s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", names)
