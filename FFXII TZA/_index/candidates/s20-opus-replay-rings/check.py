"""S-20 CS-3 (OPUS, 2026-09-26): the native command seam's two 64-entry rings (CONTRACT-native-command-seam.md) - structural twins
whose DRAINS differ - executed as shipped code.

The action-selection ring: read / write byte indices 022BE980 / 022BE981, entries (dword handles) at 022BE984 + 8*i, drained by
00313CD0. The presentation ring: 022BEDA0 / 022BEDA1, entries at 022BEDA4, drained by 00313DB0. Same shape, mod-64 advance.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image; NO application stub, no bridged import (every
IAT slot a trap); ALLOWED = the two drains' closures (+ 00263E30, 0031B7E0's tail target). Planted data only: the rings, the
leader gate byte [02089340] (clear, so 0031B7E0 resolves nothing; bit 0x20 for case G) and the presentation drain's current-object
cell [02089350] = 0.
Cases (entries whose handles do not resolve, so no unit is acted on - the drain loops themselves are measured):
 A  the action ring drains AT MOST EIGHT entries per call: 10 queued -> read index 0 -> 8 -> 10 -> 10 over three calls; 3 queued
    -> 3 in one call (CS-3's "drained up to eight entries per call").
 P  the presentation ring's drain is NOT the same loop: it stops at the first entry that does not resolve - one entry per call
    (read index 0 -> 1 -> 2).
 G  the action drain does nothing at all while [02089340] bit 0x20 is set (00313CD4).
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RAX

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, FIX, TRAP = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
ACT_DRAIN, PRES_DRAIN = 0x313CD0, 0x313DB0
A_RI, A_WI, A_ENT = 0x22BE980, 0x22BE981, 0x22BE984
P_RI, P_WI, P_ENT, P_CUR = 0x22BEDA0, 0x22BEDA1, 0x22BEDA4, 0x2089350

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for row in csv.DictReader(open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8"), delimiter="\t"):
    if row["callee_external"] != "true":
        graph[int(row["caller"], 16)].add(int(row["callee"], 16))


def closure(starts):
    seen, todo = set(), list(starts)
    while todo:
        x = todo.pop()
        if x not in seen:
            seen.add(x)
            todo.extend(graph[x])
    return seen


ALLOWED = closure({ACT_DRAIN, PRES_DRAIN}) | {0x263E30}
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(os.path.join(GRAPH, "functions.tsv"), encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec, optsz = struct.unpack_from("<H", raw, pe + 6)[0], struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
for base, size in ((STACK, STACK_SZ), (RET, 0x1000), (FIX, 0x1000), (TRAP, 0x4000)):
    uc.mem_map(base, size)
uc.mem_write(RET, b"\xF4")
uc.mem_write(TRAP, b"\xC3" * 0x4000)


def r2o(rva):
    for v, vs, ra, rs in secs:
        if v - IMG <= rva < v - IMG + max(vs, rs):
            return ra + rva - (v - IMG)


TRAPS, dd, k = set(), r2o(struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]), 0
while True:
    oft, _, _, name, ft = struct.unpack_from("<IIIII", raw, dd)
    if not (oft or name or ft):
        break
    i = 0
    while struct.unpack_from("<Q", raw, r2o(oft or ft) + 8 * i)[0]:
        uc.mem_write(IMG + ft + 8 * i, struct.pack("<Q", TRAP + 4 * k))
        TRAPS.add(TRAP + 4 * k)
        i += 1
        k += 1
    dd += 20
st = {"bad": []}


def on_code(u, a, n, _):
    if a in TRAPS or (a in FSTARTS and a not in ALLOWED):
        st["bad"].append("%08X" % a)
        u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_code)


def call(entry, r8=0):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_R8, r8)
    st["bad"] = []
    try:
        uc.emu_start(entry, RET, count=100000)
    except UcError as e:
        st["bad"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not st["bad"]


def fill(ri, wi, ent, n, handle=0x00F12345):
    for i in range(64):
        uc.mem_write(ent + 8 * i, struct.pack("<Q", 0))
    for i in range(n):
        uc.mem_write(ent + 8 * i, struct.pack("<I", handle))
    uc.mem_write(ri, bytes([0]))
    uc.mem_write(wi, bytes([n]))


def idx(ri):
    return uc.mem_read(ri, 1)[0]


res, cases = {}, {}
uc.mem_write(0x2089340, bytes([0]))                      # leader gate clear: no handle resolves (0031B7E0 returns 0)
uc.mem_write(P_CUR, struct.pack("<Q", 0))
fill(A_RI, A_WI, A_ENT, 10)
a1 = [call(ACT_DRAIN), idx(A_RI)]
a2 = [call(ACT_DRAIN), idx(A_RI)]
a3 = [call(ACT_DRAIN), idx(A_RI)]
fill(A_RI, A_WI, A_ENT, 3)
a4 = [call(ACT_DRAIN), idx(A_RI)]
res["action_ring"] = {"10_entries_call1": a1, "call2": a2, "call3_empty": a3, "3_entries": a4}
cases["A_action_ring_drains_at_most_eight_per_call"] = a1 == [True, 8] and a2 == [True, 10] and a3 == [True, 10] and a4 == [True, 3]
fill(P_RI, P_WI, P_ENT, 10)
p1 = [call(PRES_DRAIN), idx(P_RI)]
p2 = [call(PRES_DRAIN), idx(P_RI)]
res["presentation_ring"] = {"10_entries_call1": p1, "call2": p2}
cases["P_presentation_ring_stops_at_the_first_unresolved_entry"] = p1 == [True, 1] and p2 == [True, 2]
uc.mem_write(0x2089340, bytes([0x20]))
fill(A_RI, A_WI, A_ENT, 10)
g = [call(ACT_DRAIN), idx(A_RI)]
res["action_ring_gate_bit_0x20"] = g
cases["G_action_drain_skips_entirely_under_02089340_bit_0x20"] = g == [True, 0]
out = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(ALLOWED), **res}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True)
for k2, v2 in cases.items():
    print("%-58s %s" % (k2, "PASS" if v2 else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED", json.dumps(res))
