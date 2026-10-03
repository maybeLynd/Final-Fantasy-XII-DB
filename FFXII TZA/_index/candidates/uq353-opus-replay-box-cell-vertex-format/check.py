"""UQ-353 (OPUS, 2026-09-26): the exact vertex format the box cell drawer 002DC7F0 emits.

Evidence class: NATIVE-REPLAY (unicorn), live_game false, world.py's Session (the world of blocks 318-353), no
application stub. 002DC7F0 runs with every callee real up to 00181460, which is a RECORDED STOP BOUNDARY (discarded
from the allowed set; its callee 001B06D0 writes into the immediate renderer singleton [01F811E8], which this world does
not build). The vertex array is read from rcx at that boundary, with the count from edx.

Arguments (MS x64): rcx unused, rdx = 4x4 float matrix, r8 = four packed colours, r9d = x, then y, w, h, flags.
Cases:
 Q  flags 0, identity matrix: one strip of 4 vertices TL, BL, TR, BR = (x,y) (x,y+h) (x+w,y) (x+w,y+h); z 0, w 1.0;
    channels +0x10..+0x1C = the colour's bytes 0..3 (R,G,B,A); u,v 0; flags 0.
 F  flags 4 -> the same strip with bit 2 cleared (0x14 -> 0x10); flags 0x10 -> carried unchanged.
 B  flags 8 (bit 2 clear) -> the corner-blend path: the first strip is TL, BL, CENTRE, BR, the centre colour is
    ((c0 + c1) / 2 + c2) / 2 + c3) / 2 per channel, and bit 3 is cleared (0x18 -> 0x10). The second strip of this path
    is after the boundary and is STATIC evidence here.
 M  matrix {scale x 2, translate (5,7), w 2} -> x = (2x + 5) / 2, y = (y + 7) / 2: row vector times matrix, then x/w
    and y/w; the stored z, w stay 0 and 1.0.
Writes result.json.
"""
import json
import os
import struct

import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
X, Y, WD, HT = 100, 50, 20, 30
C = [0x44332211, 0x88776655, 0xCCBBAA99, 0x10FFEEDD]
ident = struct.pack("<16f", 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
res, ok = {}, {}


def bytes_of(c):
    return ["%X" % ((c >> (8 * k)) & 0xFF) for k in range(4)]


def quad_ok(r, flags_out, pos=None):
    pos = pos or [(X, Y), (X, Y + HT), (X + WD, Y), (X + WD, Y + HT)]
    if r.get("count") != 4 or r["stop"] != ["00181460"]:
        return False
    vs = r["vertices"]
    return all(tuple(v["xyzw"]) == (float(pos[i][0]), float(pos[i][1]), 0.0, 1.0) and v["rgba"] == bytes_of(C[i])
               and tuple(v["uv"]) == (0.0, 0.0) and v["flags"] == "%X" % flags_out for i, v in enumerate(vs))


P.uc.mem_write(P.MAT, ident)
res["Q_flags0"] = P.run(X, Y, WD, HT, 0)
ok["Q_plain_quad_is_a_4_vertex_strip_TL_BL_TR_BR"] = quad_ok(res["Q_flags0"], 0)
res["F_flags14"] = P.run(X, Y, WD, HT, 0x14)
ok["F_bit2_selects_the_plain_quad_and_is_cleared"] = quad_ok(res["F_flags14"], 0x10)
res["F_flags10"] = P.run(X, Y, WD, HT, 0x10)
ok["F_other_bits_are_carried"] = quad_ok(res["F_flags10"], 0x10)

res["B_flags18"] = P.run(X, Y, WD, HT, 0x18)
b = res["B_flags18"]
blend = []
for k in range(4):
    ch = [(c >> (8 * k)) & 0xFF for c in C]
    blend.append("%X" % ((((ch[0] + ch[1]) >> 1) + ch[2] >> 1) + ch[3] >> 1))
vs = b.get("vertices", [])
ok["B_bit3_draws_to_the_centre_with_the_halving_blend_and_is_cleared"] = (
    b.get("count") == 4 and len(vs) == 4
    and tuple(vs[0]["xyzw"]) == (X, Y, 0.0, 1.0) and vs[0]["rgba"] == bytes_of(C[0])
    and tuple(vs[1]["xyzw"]) == (X, Y + HT, 0.0, 1.0) and vs[1]["rgba"] == bytes_of(C[1])
    and tuple(vs[2]["xyzw"]) == (X + WD / 2, Y + HT / 2, 0.0, 1.0) and vs[2]["rgba"] == blend
    and tuple(vs[3]["xyzw"]) == (X + WD, Y + HT, 0.0, 1.0) and vs[3]["rgba"] == bytes_of(C[3])
    and all(v["flags"] == "10" for v in vs))
res["B_expected_centre_rgba"] = blend

P.uc.mem_write(P.MAT, struct.pack("<16f", 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 5, 7, 0, 2))
res["M_matrix"] = P.run(X, Y, WD, HT, 0)
f = lambda x, y: ((2 * x + 5) / 2, (y + 7) / 2)
ok["M_row_vector_times_matrix_then_divide_by_w"] = quad_ok(
    res["M_matrix"], 0, [f(X, Y), f(X, Y + HT), f(X + WD, Y), f(X + WD, Y + HT)])
P.uc.mem_write(P.MAT, ident)

out = {"ok": all(ok.values()), "cases": ok, "runs": res}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in ok.items():
    print("%-70s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
