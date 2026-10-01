"""S-13 (OPUS, 2026-09-26): the actor record pool built and every record initialised with NO scripted callee.

S-13's runtime cell rests on EXP-107 (allocator 002679F0 real, but the per-record ctor 00266530 scripted and the allocator callback
q[mgr+0x88] planted as a fake returning the fixture pool) and EXP-112 (ctor real, but 00265FF0, 00265B60, 00268380 x2, 002681E0 and
003DBB60 x4 scripted). This harness runs the whole chain as shipped:
  002679F0 ActorStorage_AllocateAndInitializeRecords
    -> call [mgr+0x88]  = 00267930, the allocator the game installs by default (0026C8E3 lea r12 / 0026CAE6 mov [rdi+0x88], r12)
         -> the resource-arena path 0036C1D0 / 0036C750 / 0036A100 / 0036C660 / 0036C140 over arena 5
    -> memset (the import, bridged by name with library semantics - an import bridge, not an application stub)
    -> the carve (pointer table, +0x03 group/class byte), then 00266530 per record with ALL its callees real.
World: block 355's world.py (s29-opus-replay-inventory-rebase), its real initialisers built. Fixtures, all planted DATA:
  - arena 5 initialised by the shipped arena initialiser 00369D30(5, base, 0x400000, 32) over a mapped region poisoned 0xA5;
  - manager slot 0 at 02098E10 (the real BSS slot): +0x00 the descriptor pointer, +0x20 the record count, +0x28 the flag,
    +0x88 = 00267930;
  - a descriptor (the game binds one from a loaded definition payload): field count, group table (8 groups: 1,1,1,0,0,1,0,1
    records, so kinds 0, 1, 2, 5 and 7), per-record entries (record 3 linked 0x81, the rest 0xFF), an empty command table.
Evidence class NATIVE-REPLAY (unicorn), live_game false. No application stub; the allowed set is the static closures of the
entries plus tail-jump targets the graph lacks (TAILS, disclosed). Writes result.json.

Contract items (CONTRACT-actor-storage-record-initialisation.md AR-1..AR-5; CONTRACT-actor-record-pool-and-region-map.md):
  AR-1  the memory is zero when the ctor runs, because the caller memsets it
  AR-2  so the ctor's read-modify-write masks preserve nothing (shown against a control on poisoned memory)
  AR-3  +0x03 is an input: the carve writes it; nothing in the ctor's call tree writes it
  AR-4  the record stores its own slot index; the pointer table indexes records individually
  AR-5  +0x11C is a lower bound: the call tree writes past it inside the record's allocation; +0x24/+0x60/+0x88/+0x89 are written
        by callees; the gaps +0x84, +0x8A, +0x9C, +0xB0 are not written
  POOL  records are reached through the pointer table at block+8, the count at block+0, the second region published to
        mgr+0x1F0; the region map's interior pointers +0xA0/+0xA8/+0xB8/+0xC0 point inside the record
"""
import importlib.util
import json
import os
import struct
import sys

from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX

HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.join(HERE, "..", "s29-opus-replay-inventory-rebase")
sys.path.insert(0, WD)
spec = importlib.util.spec_from_file_location("world355", os.path.join(WD, "world.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
FX = json.load(open(os.path.join(WD, "world.json")))

ALLOC, CTOR, DEFALLOC, ARENA_INIT = 0x2679F0, 0x266530, 0x267930, 0x369D30
TAILS = [int(x, 16) for x in os.environ.get("TAILS", "").split(",") if x]
W.ALLOWED |= {0x16D6A0} | W.closure(ALLOC) | W.closure(CTOR) | W.closure(DEFALLOC) | W.closure(ARENA_INIT) | {DEFALLOC}
for t in TAILS:
    W.ALLOWED |= W.closure(t) | {t}
# strncpy (reached by the arena name-tag 0036C660) is bridged by name with library semantics, as SECTION-06/07 bridge it:
# world.py's generic path returns, and the hook below performs the copy at that import's own trap.
W.BRIDGED.add("strncpy")
W.OSRET["strncpy"] = 0
TRAP = {nm: W.BRIDGE + 4 * i for i, (slot, nm) in enumerate(W.import_slots())}
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
BRIDGE_CALLS = {"strncpy": 0}


def strncpy_hook(u, a, n, _):
    rr = __import__("unicorn").x86_const
    d, s, cnt = u.reg_read(rr.UC_X86_REG_RCX), u.reg_read(rr.UC_X86_REG_RDX), u.reg_read(rr.UC_X86_REG_R8)
    src = bytes(u.mem_read(s, cnt)) if cnt else b""
    k = src.find(b"\0")
    body = src if k < 0 else src[:k]
    u.mem_write(d, body + bytes(cnt - len(body)))
    u.reg_write(rr.UC_X86_REG_RAX, d)
    BRIDGE_CALLS["strncpy"] += 1


uc.hook_add(UC_HOOK_CODE, strncpy_hook, begin=TRAP["strncpy"], end=TRAP["strncpy"])
SLOT = 0x02098E10
SCR, ARENA = 0x72000000, 0x75000000
uc.mem_map(SCR, 0x100000)
uc.mem_map(ARENA, 0x400000)
DESC = SCR + 0x1000
# records per group; group index = record kind: kinds 0, 1, 2, 5, 7. residuals.py re-runs this file with S13_GROUPS /
# S13_LINKED / S13_FCOUNT / S13_RESULT set; the defaults below are the published run.
GROUPS = [int(x) for x in os.environ.get("S13_GROUPS", "1,1,1,0,0,1,0,1").split(",")]
LINKED = int(os.environ.get("S13_LINKED", "3"))   # this record (kind 5 by default) carries a valid kind link (entry byte +6 = 0x81)
NREC = sum(GROUPS)
OFFG, OFFE, FCOUNT = 0x200, 0x400, int(os.environ.get("S13_FCOUNT", "4"), 0)
RESULT = os.environ.get("S13_RESULT", "result.json")
STRIDE = 0x30 if FCOUNT >= 8 else 0x20


def w(a, f, *v):
    uc.mem_write(a, struct.pack(f, *v))


def r(a, f):
    return struct.unpack(f, bytes(uc.mem_read(a, struct.calcsize(f))))


def plant_descriptor():
    uc.mem_write(DESC, bytes(0x2000))
    w(DESC, "<H", FCOUNT)
    w(DESC + 0x14, "<I", OFFG)
    w(DESC + 0x18, "<I", OFFE)
    w(DESC + OFFG, "<H", len(GROUPS))
    for g, n in enumerate(GROUPS):
        w(DESC + OFFG + 2 + 2 * g, "<H", n)
    for i in range(NREC):
        ent = DESC + OFFE + 4 + i * STRIDE
        w(ent + 6, "<B", 0x81 if i == LINKED else 0xFF)   # 0x81: link 1; 0xFF: no link
        w(ent + 8, "<I", 0x1800)
        w(ent + 0x10, "<I", 0x1900)
        w(ent + 0x14, "<I", 0x1A00)
        w(ent + 0x18, "<I", 0x1B00)                # command table: length 0
    w(DESC + 0x1B00, "<H", 0)


writes = []


def mw(u, acc, a, n, v, _):
    if not (W.STACK <= a < W.STACK + W.STACK_SZ):
        writes.append((a, n, u.reg_read(__import__("unicorn").x86_const.UC_X86_REG_RIP)))


uc.hook_add(UC_HOOK_MEM_WRITE, mw)
ctor_calls = []


RECSZ = [(struct.unpack_from("<H", bytes(uc.mem_read(0x1E0C328 + k * 4 + 2, 2)))[0] + 0xF) & ~0xF for k in range(8)]
KINDS = [g for g, n in enumerate(GROUPS) for _ in range(n)]
pre = {}                                      # record index -> its bytes as the ctor finds them
phase = {"ctor_from": None}


def code(u, a, n, _):
    if a == CTOR:
        rr = __import__("unicorn").x86_const
        mgr, ptab, idx = u.reg_read(rr.UC_X86_REG_RCX), u.reg_read(rr.UC_X86_REG_RDX), u.reg_read(rr.UC_X86_REG_R8) & 0xFFFFFFFF
        ctor_calls.append((mgr, ptab, idx))
        if phase["ctor_from"] is None:
            phase["ctor_from"] = len(writes)
        rec = struct.unpack("<Q", bytes(u.mem_read(ptab + 8 + idx * 8, 8)))[0]
        pre[idx] = (rec, bytes(u.mem_read(rec, RECSZ[KINDS[idx]])))


uc.hook_add(UC_HOOK_CODE, code, begin=CTOR, end=CTOR)
SITE1 = []                                    # 002668EC: the instruction after the w[desc] >= 0xA gate (002668E7 / 002668EA)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: SITE1.append(a), begin=0x2668EC, end=0x2668EC)
memset_calls = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: memset_calls.append(tuple(u.reg_read(x) for x in (
    __import__("unicorn").x86_const.UC_X86_REG_RCX, __import__("unicorn").x86_const.UC_X86_REG_RDX,
    __import__("unicorn").x86_const.UC_X86_REG_R8))), begin=TRAP["memset"], end=TRAP["memset"])
uc.ctl_flush_tb()


def call(fn, *a):
    writes.clear()
    a = list(a) + [0] * (4 - len(a))
    ok = S.call(fn, *a)
    return ok, uc.reg_read(UC_X86_REG_RAX), list(S.st["bad"]), list(S.st["faults"])


res = {"live_game": False, "tails": ["%08X" % t for t in TAILS]}
# ---- world: arena 5 by the shipped initialiser ----
uc.mem_write(ARENA, b"\xA5" * 0x400000)
ok_ai, _, bad_ai, f_ai = call(ARENA_INIT, 5, ARENA, 0x400000, 32)
res["arena_init"] = {"ok": ok_ai, "bad": bad_ai, "faults": f_ai}
# ---- the manager slot ----
plant_descriptor()
uc.mem_write(SLOT, bytes(0x288))
w(SLOT, "<Q", DESC)
w(SLOT + 0x20, "<I", NREC)
w(SLOT + 0x28, "<I", 1)
w(SLOT + 0x88, "<Q", DEFALLOC)
ctor_calls.clear(); memset_calls.clear(); pre.clear(); phase["ctor_from"] = None
S.st["entered"] = set()
ok, block, bad, faults = call(ALLOC, SLOT)
all_w = list(writes)
ctor_w = all_w[phase["ctor_from"]:] if phase["ctor_from"] is not None else []
entered = set(S.st["entered"])
FORMERLY_SCRIPTED = {0x265FF0: "00265FF0", 0x265B60: "00265B60", 0x268380: "00268380", 0x2681E0: "002681E0", 0x3DBB60: "003DBB60"}
res["alloc"] = {"ok": ok, "block": "%X" % block, "bad": bad, "faults": faults, "ctor_calls": len(ctor_calls),
                "memset_calls": [["%X" % a, b, "%X" % c] for a, b, c in memset_calls], "strncpy_calls": BRIDGE_CALLS["strncpy"],
                "formerly_scripted_entered": sorted(v for k, v in FORMERLY_SCRIPTED.items() if k in entered),
                "functions_entered": len(entered)}
recs = [struct.unpack("<Q", bytes(uc.mem_read(block + 8 + i * 8, 8)))[0] for i in range(NREC)]
post = {i: bytes(uc.mem_read(recs[i], RECSZ[KINDS[i]])) for i in range(NREC)}
cases, detail = {}, {}
# ---- AR-1: the ctor finds the record zeroed, and the caller's memset did it (the arena was poisoned 0xA5) ----
ms_ok = bool(memset_calls) and memset_calls[0][0] == block and memset_calls[0][1] == 0
ar1 = {i: [o for o, b in enumerate(pre[i][1]) if b and o != 3] for i in pre}
detail["AR1_nonzero_bytes_at_ctor_entry_excluding_+3"] = {i: v[:8] for i, v in ar1.items()}
cases["AR1_memset_of_the_whole_block_by_the_caller"] = ok and ms_ok and memset_calls[0][2] >= sum(RECSZ[k] for k in KINDS)
cases["AR1_every_record_zero_when_its_ctor_runs_except_+3"] = ok and len(pre) == NREC and all(not v for v in ar1.values())
# ---- AR-3: +0x03 is written by the carve, never by the ctor's call tree ----
w3 = [("%X" % a, "%08X" % rip) for a, n_, rip in ctor_w for rc in recs if a <= rc + 3 < a + n_]
detail["AR3_ctor_tree_writes_covering_+3"] = w3
cases["AR3_+3_set_by_the_carve_and_never_written_by_the_ctor_tree"] = ok and not w3 and all(
    pre[i][1][3] & 0x1F == KINDS[i] for i in pre) and all(post[i][3] == pre[i][1][3] for i in pre)
# ---- AR-4 + POOL: count, pointer table, second region, slot index, interior pointers ----
esi = (NREC * 8 + 0x17) & ~0xF
mgr1f0 = r(SLOT + 0x1F0, "<Q")[0]
inside = {}
for i, rc in enumerate(recs):
    ptrs = {off: r(rc + off, "<Q")[0] for off in (0xA0, 0xA8, 0xB8, 0xC0)}
    inside[i] = {"%X" % off: ("%X" % (p - rc) if p else "0") for off, p in ptrs.items()}
    inside[i]["ok"] = all(p == 0 or rc < p < rc + RECSZ[KINDS[i]] for p in ptrs.values()) and ptrs[0xA0] != 0
detail["POOL_interior_pointers_rel_record"] = inside
cases["AR4_each_record_stores_its_slot_index_and_the_table_indexes_records"] = ok and r(block, "<I")[0] == NREC and all(
    r(rc, "<H")[0] == i for i, rc in enumerate(recs)) and len(set(recs)) == NREC and all(c[2] == i for i, c in enumerate(ctor_calls))
cases["POOL_second_region_published_to_mgr_1F0_and_records_follow_the_header"] = ok and mgr1f0 == block + esi and min(recs) >= block + 2 * esi
cases["POOL_region_map_pointers_point_inside_each_record"] = ok and all(v["ok"] for v in inside.values())
# ---- AR-5: callees write the +0x60..+0xB8 span; the four gaps stay unwritten; writes pass +0x11C ----
span_w, gap_w, past = {}, {}, {}
for i, rc in enumerate(recs):
    offs = sorted({a - rc + k for a, n_, rip in ctor_w for k in range(n_) if rc <= a + k < rc + RECSZ[KINDS[i]]})
    span_w[i] = [o for o in offs if 0x60 <= o < 0xB8]
    gap_w[i] = [o for o in offs if o in (0x84, 0x8A, 0x9C, 0xB0)]
    past[i] = [o for o in offs if o >= 0x11C][:1]
detail["AR5"] = {i: {"span_written_sample": ["%X" % o for o in span_w[i][:12]], "gap_written": gap_w[i], "first_past_11C": ["%X" % o for o in past[i]]} for i in span_w}
import bisect
FSTARTS = sorted(W.FSTARTS)
def fn_of(rip):
    return FSTARTS[bisect.bisect_right(FSTARTS, rip) - 1]
writers = {}
for i, rc in enumerate(recs):
    for off in (0x24, 0x60, 0x88, 0x89):
        writers.setdefault("%X" % off, set()).update("%08X" % fn_of(rip) for a, n_, rip in ctor_w if a <= rc + off < a + n_)
detail["AR5_writer_functions"] = {k: sorted(v) for k, v in writers.items()}
cases["AR5_callees_not_the_ctor_body_write_+24_+60_+88_+89"] = ok and all(writers[k] and "%08X" % CTOR not in writers[k] for k in writers)
cases["AR5_gaps_+84_+8A_+9C_+B0_not_written"] = ok and not any(gap_w.values())
cases["AR5_the_call_tree_writes_past_+11C_inside_the_allocation"] = ok and all(past.values())
# ---- the formerly scripted callees all ran ----
cases["all_five_formerly_scripted_callees_executed"] = ok and set(res["alloc"]["formerly_scripted_entered"]) == set(FORMERLY_SCRIPTED.values())
# ---- AR-2: masks preserve nothing on zeroed memory - control: the same ctor over a poisoned copy of record 0 ----
MASKED = {0x08: None, 0x09: None, 0x0B: None, 0x0D: None, 0x13: None, 0x14: None}
zero_vals = {o: post[0][o] for o in MASKED}
rc0 = recs[0]
uc.mem_write(rc0, bytes([0xA5]) * RECSZ[KINDS[0]])
uc.mem_write(rc0 + 3, bytes([pre[0][1][3]]))
okc, _, badc, fc = call(CTOR, SLOT, block, 0)
pois_vals = {o: r(rc0 + o, "<B")[0] for o in MASKED}
detail["AR2"] = {"zeroed": {"%X" % o: v for o, v in zero_vals.items()}, "poisoned_control": {"%X" % o: v for o, v in pois_vals.items()},
                 "control_ok": okc, "control_bad": badc, "control_faults": fc}
cases["AR2_masked_bytes_keep_poison_bits_in_the_control_so_zero_memory_is_what_makes_them_constants"] = ok and okc and any(
    zero_vals[o] != pois_vals[o] for o in MASKED)
res["cases"] = cases
res["detail"] = detail
res["ok"] = all(cases.values())
if RESULT != "result.json":                   # the variants also record the gate and each record's layout class
    res["variant"] = {"groups": GROUPS, "linked": LINKED, "fcount": FCOUNT, "site1_hits": len(SITE1),
                      "layout_class_by_record": [uc.mem_read(0x1E0C328 + 4 * k, 1)[0] for k in KINDS]}
json.dump(res, open(os.path.join(HERE, RESULT), "w"), indent=1, sort_keys=True, default=str)
print("alloc", {k: res["alloc"][k] for k in ("ok", "block", "bad", "faults", "ctor_calls", "memset_calls", "strncpy_calls", "formerly_scripted_entered")})
for k, v in cases.items():
    print("%-92s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
