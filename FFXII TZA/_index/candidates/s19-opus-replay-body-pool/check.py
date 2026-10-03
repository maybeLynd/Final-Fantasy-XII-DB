"""S-19: CONTRACT-movement-body-pool.md executed as shipped code with NO stubbed predicate (OPUS, 2026-09-26).

S-19's runtime cell: "CONTRACT-movement-body-pool's invariants rest on EXP-087's stubbed guards". EXP-087 patched two predicates
reached by consumer 2 (00265680 and 0037C860) to `ret` with scripted return values. This harness maps the whole SHA-asserted image
and runs the creator 002E3500, the allocator / release, all five consumers and both predicates as shipped.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. NO application stub, no stop boundary. Every IAT slot is a trap; exactly
three imports are bridged by name with their library semantics - memset, cosf, sinf; any other import fails the case. ALLOWED =
the static closures of the creator and the five consumers plus the tail-jump targets the graph lacks (TAILS); entering anything
else fails the case.
Planted data only: a context (+3 kind, +0xB8 param block, +0xC0 actor), the actor (+0x138 body, +0x140..+0x152), a param block,
the real pool array 02B4E4C0 (128 x 0x130; self index at +4, free / active chains through +0/+2), the free head 02B57CC4 and
active head 02B57CC0, the battle state block behind [02EBF190] (zeroed - read by 0037C860 -> 00303EC0's ladder), and manager
slot 0's flags (02098E20, read by 00265680).
Cases (the contract's precondition, invariant, postcondition and central universal):
 K1  precondition: with ctx+0xC0 null the creator returns at once - no allocation, the heads unchanged, no consumer entered.
 K2  fresh create (4 free): +0x138 = body 0, free head 1, active head 0; all five consumers run; no fault.
 K3  at most one body per record: with body 120 already attached (active), create releases it and the allocator re-pops it -
     +0x138 = body 120 again, the active head 120, no second body taken.
 K4  postcondition + the universal: with the pool exhausted, the allocator's NULL is stored untested (+0x138 = 0) and all five
     consumers still run - with consumer 2 on its predicate arm (actor+0x152 = 0) so 00265680 / 0037C860 execute as shipped -
     and none of them faults or writes the pool or actor+0x153.
 K5  each consumer alone with the body null, and with the actor null: returns, no fault, nothing written to the pool.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import math
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RAX,
                               UC_X86_REG_XMM0)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, FIX, TRAP = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
CREATE = 0x2E3500
CONSUMERS = {0x269EC0: "c1", 0x2681D0: "c2", 0x2682D0: "c3", 0x2685F0: "c4", 0x268380: "c5"}
PRED = {0x265680: "pred_00265680", 0x37C860: "pred_0037C860"}
TAILS = {0x303EC0, 0x30D9A0, 0x377C20, 0x2681E0}
POOL, FREE_H, ACTV_H = 0x2B4E4C0, 0x2B57CC4, 0x2B57CC0
CTX, ACT, PB, STATE = FIX, FIX + 0x1000, FIX + 0x2000, FIX + 0x10000
BRIDGED = {"memset", "cosf", "sinf"}

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


ALLOWED = closure({CREATE} | set(CONSUMERS) | TAILS) | TAILS
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
for base, size in ((STACK, STACK_SZ), (RET, 0x1000), (FIX, 0x20000), (TRAP, 0x4000)):
    uc.mem_map(base, size)
uc.mem_write(RET, b"\xF4")
uc.mem_write(TRAP, b"\xC3" * 0x4000)


def r2o(rva):
    for v, vs, ra, rs in secs:
        if v - IMG <= rva < v - IMG + max(vs, rs):
            return ra + rva - (v - IMG)


TRAPS, dd, k = {}, r2o(struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]), 0
while True:
    oft, _, _, name, ft = struct.unpack_from("<IIIII", raw, dd)
    if not (oft or name or ft):
        break
    th, i = r2o(oft or ft), 0
    while True:
        e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
        if not e:
            break
        nm = "ord%d" % (e & 0xFFFF) if e >> 63 else raw[r2o(e) + 2:raw.index(b"\x00", r2o(e) + 2)].decode()
        uc.mem_write(IMG + ft + 8 * i, struct.pack("<Q", TRAP + 4 * k))
        TRAPS[TRAP + 4 * k] = nm
        i += 1
        k += 1
    dd += 20
st = {"bad": [], "faults": [], "entered": [], "imports": []}


def xf(v):
    return struct.unpack("<f", struct.pack("<I", v & 0xFFFFFFFF))[0]


def on_code(u, a, n, _):
    if a in TRAPS:
        nm = TRAPS[a]
        st["imports"].append(nm)
        if nm not in BRIDGED:
            st["bad"].append("import " + nm)
            u.emu_stop()
            return
        if nm == "memset":
            d, c, cnt = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF, u.reg_read(UC_X86_REG_R8)
            u.mem_write(d, bytes([c]) * cnt)
            u.reg_write(UC_X86_REG_RAX, d)
        else:
            x = xf(u.reg_read(UC_X86_REG_XMM0))
            y = (math.cos if nm == "cosf" else math.sin)(x)
            u.reg_write(UC_X86_REG_XMM0, struct.unpack("<I", struct.pack("<f", y))[0])
        return
    if a in CONSUMERS or a in PRED:
        st["entered"].append(CONSUMERS.get(a) or PRED[a])
    if a in FSTARTS and a not in ALLOWED:
        st["bad"].append("%08X" % a)
        u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_code)
pool_w, act153_w = [], []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: pool_w.append("%08X" % u.reg_read(UC_X86_REG_RIP)), begin=POOL, end=POOL + 128 * 0x130 - 1)
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: act153_w.append(v), begin=ACT + 0x153, end=ACT + 0x153)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))[0]


def body(i):
    return POOL + i * 0x130


def world(n_free=4, active=None, attached=None, actor=True, a152=2, kind=0x60):
    for i in range(128):
        uc.mem_write(body(i), b"\xCC" * 0x130)
        w(body(i) + 4, "<H", i)
    w(ACTV_H, "<H", 0xFFFF if active is None else active)
    w(FREE_H, "<H", 0 if n_free else 0xFFFF)
    for i in range(n_free):
        w(body(i), "<HH", 0xFFFF, i + 1 if i + 1 < n_free else 0xFFFF)
    if active is not None:
        w(body(active), "<HH", 0xFFFF, 0xFFFF)
    uc.mem_write(FIX, bytes(0x20000))
    w(CTX + 3, "<B", kind)
    w(CTX + 0xC, "<B", 0x10)
    w(CTX + 0x18, "<B", 1)
    w(CTX + 0xB8, "<Q", PB)
    w(CTX + 0xC0, "<Q", ACT if actor else 0)
    w(ACT + 0x138, "<Q", attached or 0)
    w(ACT + 0x140, "<fff", 2.0, 3.0, 9.5)
    w(ACT + 0x151, "<BB", 0, a152)
    for o, f in ((0x24, 4.0), (0x38, 5.0), (0x50, 6.0), (0x54, 7.0), (0x68, 8.0), (0xA8, 10.0), (0xC0, 11.0)):
        w(PB + o, "<f", f)
    w(0x2EBF190, "<Q", STATE)
    w(0x2098E20, "<B", 1)


def call(entry, rcx=CTX, rdx=0):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    st.update(bad=[], faults=[], entered=[], imports=[])
    del pool_w[:], act153_w[:]
    try:
        uc.emu_start(entry, RET, count=2000000)
    except UcError as e:
        st["faults"].append(str(e))
    return {"ok": uc.reg_read(UC_X86_REG_RIP) == RET and not st["bad"] and not st["faults"], "halt": (st["bad"] or st["faults"])[:2],
            "entered": list(st["entered"]), "imports": sorted(set(st["imports"])), "act138": "%X" % r(ACT + 0x138, "<Q"),
            "free_h": r(FREE_H, "<H"), "actv_h": r(ACTV_H, "<H"), "pool_writes": len(pool_w), "act153_writes": list(act153_w)}


ALL5 = ["c1", "c2", "c3", "c4", "c5"]
res, cases = {}, {}
world(actor=False)
k1 = call(CREATE)
cases["K1_null_actor_returns_before_allocation"] = k1["ok"] and k1["entered"] == [] and k1["free_h"] == 0 and k1["actv_h"] == 0xFFFF \
    and k1["pool_writes"] == 0
world()
k2 = call(CREATE)
cases["K2_fresh_create_attaches_body0_and_runs_all_consumers"] = k2["ok"] and k2["act138"] == "%X" % body(0) and k2["free_h"] == 1 \
    and k2["actv_h"] == 0 and [e for e in k2["entered"] if e.startswith("c")] == ALL5
world(n_free=4, active=120, attached=body(120))
k3 = call(CREATE)
cases["K3_one_body_per_record_release_then_re_pop"] = k3["ok"] and k3["act138"] == "%X" % body(120) and k3["actv_h"] == 120 \
    and k3["free_h"] == 0
world(n_free=0, a152=0)
w(0x22C7FE0, "<I", 0)                                     # consumer 2's compare global: no match with the planted handle
k4 = call(CREATE)
cases["K4_exhausted_null_stored_untested_every_consumer_guards"] = k4["ok"] and k4["act138"] == "0" and k4["free_h"] == 0xFFFF \
    and [e for e in k4["entered"] if e.startswith("c")] == ALL5 and k4["pool_writes"] == 0 and k4["act153_writes"] == []
k5 = {}
for ent, nm in CONSUMERS.items():
    world(n_free=0)
    nb = call(ent, rdx=0xAB)
    world(n_free=0, actor=False)
    na = call(ent, rdx=0xAB)
    k5[nm] = {"body_null": nb, "actor_null": na}
cases["K5_each_consumer_guards_null_body_and_null_actor"] = all(v["body_null"]["ok"] and v["actor_null"]["ok"] and v["body_null"]["pool_writes"] == 0
                                                                 and v["actor_null"]["pool_writes"] == 0 for v in k5.values())
res.update(K1=k1, K2=k2, K3=k3, K4=k4, K5=k5)
preds_run = sorted({e for x in (k2, k4) for e in x["entered"] if e.startswith("pred")})
out = {"ok": all(cases.values()), "cases": cases, "predicates_executed": preds_run, "allowed_functions": len(ALLOWED), **res}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True)
for k2_, v in cases.items():
    print("%-58s %s" % (k2_, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED", "predicates executed:", preds_run)


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
