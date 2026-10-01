"""S-51 (OPUS, 2026-09-26): CONTRACT-navigation-search-and-follow's NV-1, NV-2 and NV-3 executed over a SHIPPED navigation mesh,
bound by its own binder - the contract's own invariants, not consumer anchors.

World: block 345's (s25-opus-replay-enmity/check.py, imported; its cases run first, unchanged) - battle units installed by the
shipped installer. The mesh is slot 4 of the shipped map pack ps2data/plan_master/map_ctrl/frs01/frs0101/bin/frs0101.mpk (cut
exactly as the navigation census cuts it; 22 regions in two connected components), copied to memory and bound by
00384160, which stores [02AEDFB0] and rebases the offsets in place (the navigation page section 1). Start and goal points are
region centroids computed from the mesh's own triangles (each maps back to its region through 00383F10 - checked).
Import bridges by name, library semantics: _fdclass (float class from xmm0) and _hypotf (xmm0, xmm1 -> xmm0). No application stub.
The NavPath is initialised by the game's own wipers 003839F0 / 003839C0. A hook at 0038319D (the Dijkstra array set-up, past
every early exit) counts searches that ran Dijkstra.
Cases:
 R0  the mesh binds (root = the section, header offsets rebased) and every region's centroid resolves to that region.
 N1  NV-3 outcome 1 - same region: returns 0, no Dijkstra; the route holds only the goal (next[goal] = 0xFF).
 N2  a connected pair (region 0 -> 21): Dijkstra runs once, returns 0, and next[] chains from the start to the goal.
 N3  NV-3 outcome 3 - the goal moved inside its region: returns 0 with NO Dijkstra, and only the goal's waypoint changes.
 N4  an unreachable pair (region 0 -> 10, the other component): Dijkstra runs, returns -1, start/goal reset to 0xFF, and the
     (start, goal) pair is written into the dead-end memory at +0x0C.
 N5  NV-3 outcome 2 - the same unreachable pair again: returns -1 with NO Dijkstra.
 N6  NV-1: the locomotion reset BattleLocomotion_ResetPathAndSetTargets 003291B0 (on unit + 0x80, whose +0x180 is the NavPath at
     unit + 0x200) wipes the route and KEEPS the dead-end memory: afterwards the connected pair runs Dijkstra again, and the
     unreachable pair is still refused with no Dijkstra.
 N7  NV-2: 003278D0 wipes BOTH caches on every unit whose byte 0 bit 4 is set, and leaves a unit without it untouched. The two
     wipers write exactly next[0..127] = 0xFF (003839F0) and the two dead-end pairs at +0x0C = 0xFFFF (003839C0); neither touches
     the start / goal words at +4 / +8.
 N8  NV-2's re-read bound (00327910 calls the count 00236850 inside the loop): with the count cell lowered by one, the last
     slot is NOT visited (control); with the same lowering and a disclosed perturbation that raises it back during the walk,
     the last slot IS wiped - the bound is re-read, not hoisted.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import collections
import contextlib
import hashlib
import io
import json
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s25-opus-replay-enmity"))
MPK = r"D:\FFXII_TZA_extract\ps2data\plan_master\map_ctrl\frs01\frs0101\bin\frs0101.mpk"
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as E                                     # block 345 (its cases run first, unchanged)
os.chdir(cwd)
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_XMM0, UC_X86_REG_XMM1

W, uc, S = E.W, E.uc, E.S
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
BIND, REGION, SEARCH, WROUTE, WDEAD, LRESET, INVAL, COUNT = 0x384160, 0x383F10, 0x382FF0, 0x3839F0, 0x3839C0, 0x3291B0, 0x3278D0, 0x236850
for f in (BIND, REGION, SEARCH, WROUTE, WDEAD, LRESET, INVAL):
    W.ALLOWED |= W.closure(f) | {f}
pe = pefile.PE(W.EXE)
IAT = {(imp.name or b"").decode(): imp.address for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
f32 = lambda r: struct.unpack("<f", struct.pack("<I", uc.reg_read(r) & 0xFFFFFFFF))[0]
for nm in ("_fdclass", "_hypotf"):
    W.OSRET[nm] = 0
    W.BRIDGED.add(nm)


def fdclass(u, a, n, _):
    x = f32(UC_X86_REG_XMM0)
    u.reg_write(UC_X86_REG_RAX, 2 if math.isnan(x) else 1 if math.isinf(x) else 0 if x == 0 else (0xFFFFFFFE if abs(x) < 1.1754943508222875e-38 else 0xFFFFFFFF))


def hypotf(u, a, n, _):
    u.reg_write(UC_X86_REG_XMM0, struct.unpack("<I", struct.pack("<f", math.hypot(f32(UC_X86_REG_XMM0), f32(UC_X86_REG_XMM1))))[0])


uc.hook_add(UC_HOOK_CODE, fdclass, begin=q(IAT["_fdclass"]), end=q(IAT["_fdclass"]))
uc.hook_add(UC_HOOK_CODE, hypotf, begin=q(IAT["_hypotf"]), end=q(IAT["_hypotf"]))
DIJ = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: DIJ.append(1), begin=0x38319D, end=0x38319D)
uc.ctl_flush_tb()


def slot4(d):
    count = struct.unpack_from("<I", d, 0)[0]
    sizes = struct.unpack_from("<%dI" % count, d, 4)
    pos = ((count + 1) * 4 + 0x3F) & ~0x3F
    for i, s in enumerate(sizes):
        if not s:
            continue
        pos += 0x40
        if i == 4:
            return d[pos:pos + s]
        pos += s


raw = open(MPK, "rb").read()
sec = slot4(raw)
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
nreg, vo, to, ro, ao = u16(sec, 0xA), u32(sec, 0xC), u32(sec, 0x10), u32(sec, 0x18), u32(sec, 0x1C)
NAV = 0x7A000000
uc.mem_map(NAV, 0x10000)
uc.mem_write(NAV, sec)
okb = S.call(BIND, NAV)
hdr = bytes(uc.mem_read(NAV, 0x30))
cent = {}
for r in range(nreg):
    t = u16(sec, ro + r * 0x22 + 0x14)
    vs = [struct.unpack_from("<ff", sec, vo + u16(sec, to + t * 8 + 2 * k) * 8) for k in range(3)]
    cent[r] = (sum(x for x, z in vs) / 3, sum(z for x, z in vs) / 3)
A, B = NAV + 0x9000, NAV + 0x9010
back = []
for r in range(nreg):
    uc.mem_write(A, struct.pack("<ff", *cent[r]))
    S.call(REGION, A)
    back.append(uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)
comp = list(range(nreg))


def root(x):
    while comp[x] != x:
        comp[x] = comp[comp[x]]
        x = comp[x]
    return x


for i in range(nreg):
    for j in range(nreg):
        if u16(sec, ao + 2 * (i * nreg + j)):
            a, b = root(i), root(j)
            if a != b:
                comp[a] = b
parts = collections.defaultdict(list)
for r in range(nreg):
    parts[root(r)].append(r)
G = sorted(parts.values(), key=len, reverse=True)


def state(np_):
    b = bytes(uc.mem_read(np_, 0x490))
    return {"start": u32(b, 4), "goal": u32(b, 8), "dead": b[0xC:0x10].hex(), "next": b[0x10:0x10 + nreg].hex(),
            "wp": [b[0x90 + 8 * r:0x98 + 8 * r].hex() for r in range(nreg)]}


def search(np_, s, g):
    uc.mem_write(A, struct.pack("<ff", *s))
    uc.mem_write(B, struct.pack("<ff", *g))
    del DIJ[:]
    ok = S.call(SEARCH, A, B, np_, 0)
    return {"ok": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "dijkstra": len(DIJ), "halt": (S.st["bad"] or S.st["faults"])[:1], "after": state(np_)}


def chain(st, s, g):
    nxt = bytes.fromhex(st["next"])
    path, cur = [s], s
    for _ in range(nreg):
        if cur == g:
            return path
        cur = nxt[cur]
        if cur == 0xFF:
            return None
        path.append(cur)
    return None


NP = NAV + 0xA000
S.call(WROUTE, NP)
S.call(WDEAD, NP)
s0, g0, far = G[0][0], G[0][-1], G[1][0]
n1 = search(NP, cent[s0], cent[s0])
n2 = search(NP, cent[s0], cent[g0])
wp_before = n2["after"]["wp"]
n3 = search(NP, cent[s0], (cent[g0][0] + 0.01, cent[g0][1] + 0.01))
n4 = search(NP, cent[s0], cent[far])
n5 = search(NP, cent[s0], cent[far])
# ---- NV-1 on a real unit: the locomotion reset wipes the route, keeps the dead ends ----
E.world()
U = E.unit(E.NFOE + 0)
UNP = U + 0x200
S.call(WROUTE, UNP)
S.call(WDEAD, UNP)
search(UNP, cent[s0], cent[g0])
search(UNP, cent[s0], cent[far])
before_reset = state(UNP)
okr = S.call(LRESET, U + 0x80, 0, 0)
after_reset = state(UNP)
n6a = search(UNP, cent[s0], cent[g0])
n6b = search(UNP, cent[s0], cent[far])
# ---- NV-2: 003278D0 wipes both caches on flagged units only; the count is re-read ----
E.world()
units = [E.unit(i) for i in range(E.NFOE + E.NPARTY)]
seeded = {}
for i, u in enumerate(units):
    S.call(WROUTE, u + 0x200)
    S.call(WDEAD, u + 0x200)
    search(u + 0x200, cent[s0], cent[g0])
    search(u + 0x200, cent[s0], cent[far])
    b0 = uc.mem_read(u, 1)[0]
    uc.mem_write(u, bytes([(b0 | 0x10) if i != 1 else (b0 & ~0x10 & 0xFF)]))
    seeded[i] = state(u + 0x200)
calls = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: calls.append(a), begin=COUNT, end=COUNT)
uc.ctl_flush_tb()
oki = S.call(INVAL)
post = {i: state(u + 0x200) for i, u in enumerate(units)}
wiped = lambda st: st["dead"] == "ffffffff" and set(bytes.fromhex(st["next"])) == {0xFF}   # exactly what 003839C0 / 003839F0 write
# perturbation: the real count is NFOE+NPARTY; run again with the count lowered by one, raised back at the first in-loop call
for i, u in enumerate(units):
    search(u + 0x200, cent[s0], cent[g0])
last = len(units) - 1
cnt_cell = 0x208E6A0
uc.mem_write(cnt_cell, struct.pack("<I", len(units) - 1))       # control first: lowered, no bump -> the last slot is not visited
okc = S.call(INVAL)
control_last = state(units[last] + 0x200)
for i, u in enumerate(units):
    search(u + 0x200, cent[s0], cent[g0])
uc.mem_write(cnt_cell, struct.pack("<I", len(units) - 1))
del calls[:]
bumped = []


def bump(u, a, n, _):
    if len(calls) == 2 and not bumped:
        u.mem_write(cnt_cell, struct.pack("<I", len(units)))
        bumped.append(1)


h = uc.hook_add(UC_HOOK_CODE, bump, begin=0x327910, end=0x327910)
uc.ctl_flush_tb()
okp = S.call(INVAL)
uc.hook_del(h)
perturbed_last = state(units[last] + 0x200)
R = {"mesh": {"file": "frs0101.mpk", "slot4_sha256": hashlib.sha256(sec).hexdigest()[:16], "regions": nreg, "components": G,
              "bind_ok": okb, "root": "%X" % q(0x2AEDFB0), "hdr_0C": "%X" % u32(hdr, 0xC), "region_lookup": back},
     "N1": n1["ret"], "N2": {"ret": n2["ret"], "dijkstra": n2["dijkstra"], "route": chain(n2["after"], s0, g0)},
     "N3": {"ret": n3["ret"], "dijkstra": n3["dijkstra"], "waypoints_changed": [r for r in range(nreg) if n3["after"]["wp"][r] != wp_before[r]]},
     "N4": {"ret": "%X" % n4["ret"], "dijkstra": n4["dijkstra"], "start": n4["after"]["start"], "goal": n4["after"]["goal"], "dead": n4["after"]["dead"]},
     "N5": {"ret": "%X" % n5["ret"], "dijkstra": n5["dijkstra"]},
     "N6": {"reset_ok": okr, "before": {k: before_reset[k] for k in ("start", "goal", "dead")}, "after": {k: after_reset[k] for k in ("start", "goal", "dead")},
            "next_after_all_ff": set(bytes.fromhex(after_reset["next"])) == {0xFF}, "connected_dijkstra": n6a["dijkstra"],
            "unreachable": ["%X" % n6b["ret"], n6b["dijkstra"]]},
     "N7": {"inval_ok": oki, "wiped": {i: wiped(post[i]) for i in post}, "unit1_untouched": post[1] == seeded[1]},
     "N8": {"control_ok": okc, "control_last_slot_wiped": wiped(control_last), "perturbed_ok": okp, "bumped": bool(bumped), "extra_slot_wiped": wiped(perturbed_last)}}
cases = {
    "R0_mesh_bound_by_00384160_and_regions_resolve": okb and q(0x2AEDFB0) == NAV and u32(hdr, 0xC) == NAV + vo and back == list(range(nreg)),
    "N1_same_region_returns_0_no_dijkstra": n1["ok"] and n1["ret"] == 0 and n1["dijkstra"] == 0,
    "N2_connected_pair_dijkstra_once_route_chains": n2["ok"] and n2["ret"] == 0 and n2["dijkstra"] == 1 and R["N2"]["route"] is not None,
    "N3_held_route_no_dijkstra_only_goal_waypoint_refreshed": n3["ok"] and n3["ret"] == 0 and n3["dijkstra"] == 0 and R["N3"]["waypoints_changed"] == [g0],
    "N4_unreachable_dijkstra_minus1_dead_end_recorded": n4["ok"] and n4["ret"] == 0xFFFFFFFF and n4["dijkstra"] == 1 and n4["after"]["start"] == 0xFF
        and n4["after"]["dead"][:4] == "%02x%02x" % (s0, far),
    "N5_dead_end_refused_without_dijkstra": n5["ok"] and n5["ret"] == 0xFFFFFFFF and n5["dijkstra"] == 0,
    "N6_NV1_locomotion_reset_wipes_route_keeps_dead_ends": okr and R["N6"]["next_after_all_ff"] and after_reset["dead"] == before_reset["dead"]
        and before_reset["dead"][:4] == "%02x%02x" % (s0, far) and n6a["dijkstra"] == 1 and n6b["ret"] == 0xFFFFFFFF and n6b["dijkstra"] == 0,
    "N7_NV2_flagged_units_both_wiped_unflagged_untouched": oki and all(R["N7"]["wiped"][i] for i in post if i != 1) and R["N7"]["unit1_untouched"],
    "N8_NV2_count_reread_each_iteration_perturbation_covers_the_extra_slot": okc and not R["N8"]["control_last_slot_wiped"] and okp and bool(bumped)
        and R["N8"]["extra_slot_wiped"],
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("N2", "N3", "N4", "N5", "N6", "N7", "N8")}, default=str)[:2000])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
