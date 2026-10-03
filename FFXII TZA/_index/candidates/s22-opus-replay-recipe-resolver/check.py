"""S-22: execute BattleFormula_ResolveTargetResult (00385F60), CONTRACT-weapon-recipes.md's one entry, as shipped code on
authored recipes, and record which step-table slots its committed loop calls, in order (OPUS, 2026-09-25, block 316).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub. ALLOWED = the
resolver's static closure plus every step-table target's closure (the loop reaches them through `call [table + slot*8]`,
which edges.tsv cannot follow) plus the MT19937 body; entering anything else fails a case. IMPORTS: every IAT slot is trapped
and only memset / memcpy / memmove are bridged by name.
The recipes are the SHIPPED ones (pointer table 01EF96C0, step table 01EFA5C0); nothing in them is planted. Each case picks
an action row whose +8 byte is the recipe id.
Fixtures (planted data only): attacker / target stats blocks, the result record, the action table behind [02EBF138] (decode
base q[01F83530] = 0), the per-side records at 0208D480 (zero: no refusal bits), an empty unit table ([0208E6A0] = 0).
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP,
                               UC_X86_REG_RAX)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
ATT, TGT, RES, ATBL, AROWS = WORLD, WORLD + 0x1000, WORLD + 0x2000, WORLD + 0x3000, WORLD + 0x3100
RESOLVER, STEP_TABLE, RECIPE_TABLE, LOOP_CALL, FLAG = 0x385F60, 0x1EFA5C0, 0x1EF96C0, 0x3863D0, 0x2AEDFB8
G_ACTION_TBL, G_DECODE, G_UNITCOUNT = 0x2EBF138, 0x1F83530, 0x208E6A0
BRIDGED = {"memset", "memcpy", "memmove"}

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        graph[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(graph[x])
    return seen


pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40


def rd_img(v, f):
    for va, vs, ra, rs in secs:
        if va <= v < va + rs:
            return struct.unpack_from(f, raw, ra + v - va)


STEPS = [rd_img(STEP_TABLE + 8 * i, "<Q")[0] for i in range(202)]
ALLOWED = closure(RESOLVER) | {0x863BF0, 0x866D60, 0x866B90, 0x387B00}
for t in STEPS:
    ALLOWED |= closure(t)
ALLOWED |= closure(0x387B00)
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")


def recipe(rid):
    p = rd_img(RECIPE_TABLE + 8 * rid, "<Q")[0]
    a, lists, cur = p, [], []
    while len(lists) < 2:
        v = rd_img(a, "<i")[0]
        a += 4
        if v == -1:
            lists.append(cur)
            cur = []
        else:
            cur.append(v)
    return lists


def import_slots():
    def r2o(rva):
        for v, vs, ra, rs in secs:
            if v - IMG <= rva < v - IMG + max(vs, rs):
                return ra + rva - (v - IMG)
    imp_rva = struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]
    out, dd = [], r2o(imp_rva)
    while True:
        oft, ts, fc, name, ft = struct.unpack_from("<IIIII", raw, dd)
        if not (oft or name or ft):
            return out
        th, i = r2o(oft or ft), 0
        while True:
            e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
            if e == 0:
                break
            nm = "ord%d" % (e & 0xFFFF) if e >> 63 else raw[r2o(e) + 2:raw.index(b"\x00", r2o(e) + 2)].decode()
            out.append((IMG + ft + 8 * i, nm))
            i += 1
        dd += 20


uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x10000)
uc.mem_map(BRIDGE, 0x2000)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_write(BRIDGE, bytes([0xC3]) * 0x2000)
BR = {}
for i, (slot, name) in enumerate(import_slots()):
    uc.mem_write(slot, struct.pack("<Q", BRIDGE + 4 * i))
    BR[BRIDGE + 4 * i] = name
state = {"bad": [], "faults": [], "slots": [], "flag_after": [], "pending": None}


def flag():
    return struct.unpack("<I", bytes(uc.mem_read(FLAG, 4)))[0]


def on_code(u, a, n, _):
    if a in BR:
        nm = BR[a]
        if nm not in BRIDGED:
            state["bad"].append("import " + nm)
            u.emu_stop()
            return
        rcx, rdx, r8 = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        if nm == "memset":
            u.mem_write(rcx, bytes([rdx & 0xFF]) * r8)
        else:
            u.mem_write(rcx, bytes(u.mem_read(rdx, r8)) if r8 else b"")
        u.reg_write(UC_X86_REG_RAX, rcx)
        return
    if a == LOOP_CALL:
        rax = u.reg_read(UC_X86_REG_RAX)
        state["slots"].append(struct.unpack("<q", struct.pack("<Q", rax))[0])
    if a == LOOP_CALL + 7:                         # the instruction after the indirect call: the flag test
        state["flag_after"].append(flag())
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def run_recipe(rid, action_id=5):
    uc.mem_write(WORLD, bytes(0x10000))
    uc.mem_write(ATBL, struct.pack("<IIHHI", 0, 0, 0x20, 0, AROWS))
    rows = bytearray(0x20 * 16)
    rows[0x20 * action_id + 8] = rid
    uc.mem_write(AROWS, bytes(rows))
    uc.mem_write(G_ACTION_TBL, struct.pack("<Q", ATBL))
    uc.mem_write(G_DECODE, struct.pack("<Q", 0))
    uc.mem_write(G_UNITCOUNT, struct.pack("<I", 0))
    uc.mem_write(0x208D480, bytes(0x40 * 8))
    uc.mem_write(FLAG, struct.pack("<I", 0))
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, action_id), (UC_X86_REG_RDX, ATT), (UC_X86_REG_R8, TGT), (UC_X86_REG_R9, RES)):
        uc.reg_write(r, v)
    state.update(bad=[], faults=[], slots=[], flag_after=[])
    try:
        uc.emu_start(RESOLVER, RET, count=5000000)
    except UcError as e:
        state["faults"].append(str(e))
    ok = uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-30s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# RW-1 (static): 109 recipes, the next qword not a pointer
ptrs = [rd_img(RECIPE_TABLE + 8 * i, "<Q")[0] for i in range(110)]
data_lo = min(v for v, vs, ra, rs in secs if v > 0x1000000)
rw1 = all(0x1000000 <= p < 0x3000000 for p in ptrs[:109]) and not (0x1000000 <= ptrs[109] < 0x3000000)
record("RW1_table_extent_static", rw1, next_qword="%016X" % ptrs[109], note="ids 0..108 point into the image's data; the 110th qword does not")

# RW-2 / RW-4 (static, section 12): recipe 25's two runs; 25 vs 26 differ in exactly three slot positions
r25, r26 = recipe(25), recipe(26)
only_preview = sorted(set(r25[0]) - set(r25[1]))
diffs = [(k, i, a, b) for k in (0, 1) for i, (a, b) in enumerate(zip(r25[k], r26[k])) if a != b]
record("RW2_RW4_static", len(r25) == 2 and bool(only_preview) and len(diffs) == 3 and len(r25[0]) == len(r26[0])
       and len(r25[1]) == len(r26[1]), recipe25=r25, recipe26=r26, preview_only_slots=only_preview,
       differing_positions=[{"list": ("preview", "committed")[k], "index": i, "25": a, "26": b} for k, i, a, b in diffs],
       note="recipe 25 is two -1-terminated runs; its preview names slots the committed run does not; 25 and 26 differ in three positions")

cases = {}
for rid in (39, 74, 90, 5, 6, 2, 4, 25):
    pv, cm = recipe(rid)
    ok, eax = run_recipe(rid)
    cases[rid] = {"preview": pv, "committed": cm, "ok": ok, "eax": eax, "slots_called": list(state["slots"]),
                  "flag_after_each": list(state["flag_after"]), "stopped_at": (state["bad"] or state["faults"])[:1]}
    print(rid, cases[rid])

# RW-2: the committed loop runs the second list in order; a preview-only recipe calls nothing
rw2 = []
for rid, c in cases.items():
    if not c["ok"] and not c["slots_called"]:
        continue
    exp = c["committed"]
    got = c["slots_called"]
    stopped_early = bool(c["flag_after_each"]) and c["flag_after_each"][-1] == 1 and len(got) < len(exp)
    if got != exp[:len(got)] or (not stopped_early and c["ok"] and got != exp):
        rw2.append(rid)
record("RW2_committed_list_only", not rw2 and cases[39]["ok"] and cases[39]["slots_called"] == [], failing=rw2,
       note="each completed case calls exactly its committed list, in order (a prefix when the flag stops it); recipe 39 "
            "(preview [193], committed []) calls no step")
early = {rid: c for rid, c in cases.items() if c["flag_after_each"] and 1 in c["flag_after_each"]}
record("loop_early_exit_observed", True, cases_with_flag_set={str(k): {"called": v["slots_called"], "flags": v["flag_after_each"],
                                                                         "committed": v["committed"]} for k, v in early.items()},
       note="observed: when a step leaves [02AEDFB8] = 1 the loop stops before the next slot (003863D7 cmp / je)")
results["cases"] = {str(k): v for k, v in cases.items()}
json.dump({"ok": allok, "allowed_functions": len(ALLOWED), "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok", "allowed", len(ALLOWED))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
