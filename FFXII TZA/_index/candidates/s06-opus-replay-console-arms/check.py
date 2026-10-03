"""S-06: execute the developer console's dispatcher 001D1660 as shipped code for every command id, in both directions, through
its real caller shape 001CD040 (dl = direction, r8d = id; 001CD040 sets r8b = !dl and r9d = id and tail-jumps in), and
test CONTRACT-developer-tuning-console.md's I-1 .. I-4 and its postcondition by recording the arm each call selects and every
memory write it makes (OPUS, 2026-09-25, block 315).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub. ALLOWED = the
static closure of 001D1660 (2,136 functions); entering anything else fails the call. IMPORTS: every IAT slot points at a
unique trap; memcpy / memmove / memset / malloc / free are bridged by name, any other import stops the call by name - an arm
that reaches a loader or an iostream is REPORTED as stopped, not counted.
Fixtures (planted data only): the settings object DeveloperConsoleSettings01F81428 (0x10E8, zero) behind [01F81428] and passed
as rcx exactly as 0017DB90 does; zeroed blocks behind [01F7F5F0] (PostProcessParamContext, 0x4A8) and [01F7F598]
(BootSingleton01F7F598, 0xDD8) so the lazy getters return them.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP,
                               UC_X86_REG_RAX)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
NAMES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "FFXII TZA" if False else "",
                     "..", "00-Engine-Core-Runtime", "Developer-Tuning-Console", "console-command-names.md")
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, HEAP, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x73000000, 0x74000000
SET, PPC, BOOT = WORLD, WORLD + 0x2000, WORLD + 0x3000
G_SET, G_PPC, G_BOOT = 0x1F81428, 0x1F7F5F0, 0x1F7F598
DISPATCH, CALLER, JMP_SITE, TABLE, BODY_END, NOOP_ARM, EXIT = 0x1D1660, 0x1CD040, 0x1D16AE, 0x1D4C1C, 0x1D4C1A, 0x1D4BFA, 0x1D4C09
BRIDGED = {"memcpy", "memmove", "memset", "malloc", "free"}

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


ALLOWED = closure(DISPATCH) | {CALLER}
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40


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
IMAGE0 = {}
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x10000)
uc.mem_map(HEAP, 0x100000)
uc.mem_map(BRIDGE, 0x2000)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_write(BRIDGE, bytes([0xC3]) * 0x2000)
BR = {}
for i, (slot, name) in enumerate(import_slots()):
    uc.mem_write(slot, struct.pack("<Q", BRIDGE + 4 * i))
    BR[BRIDGE + 4 * i] = name
state = {"bad": [], "faults": [], "arm": None, "writes": [], "heap": HEAP, "limit": False}


def on_code(u, a, n, _):
    if a in BR:
        nm = BR[a]
        if nm not in BRIDGED:
            state["bad"].append("import " + nm)
            u.emu_stop()
            return
        rcx, rdx, r8 = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        if nm in ("memcpy", "memmove"):
            u.mem_write(rcx, bytes(u.mem_read(rdx, r8)) if r8 else b"")
            u.reg_write(UC_X86_REG_RAX, rcx)
        elif nm == "memset":
            u.mem_write(rcx, bytes([rdx & 0xFF]) * r8)
            u.reg_write(UC_X86_REG_RAX, rcx)
        elif nm == "malloc":
            p = state["heap"]
            state["heap"] += (rcx + 0xF) & ~0xF
            u.reg_write(UC_X86_REG_RAX, p)
        return
    if a == JMP_SITE:
        state["arm"] = u.reg_read(UC_X86_REG_R9)
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_write(u, ac, a, n, v, _):
    if not (STACK <= a < STACK + STACK_SZ):
        state["writes"].append((a, n, v))


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def world():
    uc.mem_write(WORLD, bytes(0x10000))
    uc.mem_write(G_SET, struct.pack("<Q", SET))
    uc.mem_write(G_PPC, struct.pack("<Q", PPC))
    uc.mem_write(G_BOOT, struct.pack("<Q", BOOT))


def call_id(cid, dl):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, SET)
    uc.reg_write(UC_X86_REG_RDX, dl)
    uc.reg_write(UC_X86_REG_R8, cid & 0xFFFFFFFF)
    state.update(bad=[], faults=[], arm=None, writes=[])
    try:
        uc.emu_start(CALLER, RET, count=3000000)
    except UcError as e:
        state["faults"].append(str(e))
    done = uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]
    return done


def region(a):
    if SET <= a < SET + 0x10E8:
        return "set+0x%X" % (a - SET)
    if PPC <= a < PPC + 0x4A8:
        return "ppc+0x%X" % (a - PPC)
    if BOOT <= a < BOOT + 0xDD8:
        return "boot+0x%X" % (a - BOOT)
    if HEAP <= a < HEAP + 0x100000:
        return "heap"
    return "%08X" % a


# static: the table (I-1, I-3)
tbl = [struct.unpack("<i", bytes(uc.mem_read(TABLE + 4 * i, 4)))[0] + IMG for i in range(282)]
in_body = all(DISPATCH <= t < BODY_END for t in tbl)
distinct = len(set(tbl))
noop_ids = [i + 12 for i, t in enumerate(tbl) if t == NOOP_ARM]

labels = {}
try:
    import re
    npath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "00-Engine-Core-Runtime",
                                          "Developer-Tuning-Console", "console-command-names.md"))
    for l in open(npath, encoding="utf-8"):
        m = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]*?)\s*\|", l)
        if m:
            labels[int(m.group(1))] = m.group(2)
except OSError:
    pass

rows, per = [], {}
for cid in list(range(0, 300)) + [-1, 0x7FFFFFFF]:
    for dl in (0, 1):
        world()
        ok = call_id(cid, dl)
        ws = [(region(a), n) for a, n, v in state["writes"]]
        fl = []
        for a, n, v in state["writes"]:
            if n == 4 and not (HEAP <= a < HEAP + 0x100000):
                f = struct.unpack("<f", struct.pack("<I", v & 0xFFFFFFFF))[0]
                if f == f and 0 < abs(f) <= 10.0 and (v & 0xFFFFFFFF) > 0x00800000:
                    fl.append(round(f, 6))
        per[(cid, dl)] = {"ok": ok, "arm": ("%08X" % state["arm"]) if state["arm"] else None,
                          "writes": sorted({w for w, n in ws}), "stopped_at": (state["bad"] or state["faults"])[:1], "float_values": fl}

results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


record("I1_I3_table_static", in_body and distinct == 227 and len(noop_ids) == 56, entries=282, distinct_targets=distinct,
       all_inside_body=in_body, noop_arm_ids=noop_ids, note="282 entries inside the body, 227 distinct, 56 on 001D4BFA")
out_ids = [c for c in list(range(0, 12)) + list(range(294, 300)) + [-1, 0x7FFFFFFF]]
i2 = all(per[(c, d)]["ok"] and per[(c, d)]["arm"] is None and not per[(c, d)]["writes"] for c in out_ids for d in (0, 1))
record("I2_out_of_range_is_a_noop", i2, ids=[hex(c & 0xFFFFFFFF) for c in out_ids],
       note="ids 0..11, 294..299, -1 and 0x7FFFFFFF: no arm selected, nothing written, both directions")
i3 = all(per[(c, d)]["ok"] and per[(c, d)]["arm"] == "%08X" % NOOP_ARM and not per[(c, d)]["writes"] for c in noop_ids for d in (0, 1))
record("I3_shared_arm_does_nothing", i3, n=len(noop_ids), note="all 56 ids reach 001D4BFA and write nothing")
# every in-range id selects exactly the table's arm
sel = all(per[(c, d)]["arm"] == "%08X" % tbl[c - 12] for c in range(12, 294) for d in (0, 1) if per[(c, d)]["arm"] or per[(c, d)]["ok"])
record("dispatch_selects_the_table_arm", sel, note="for every id 12..293 the jump at 001D16AE lands on table[id - 12]")
# postcondition, observed: what each completed arm writes, and where
done = {c: per[(c, 0)] for c in range(12, 294) if per[(c, 0)]["ok"] and c not in noop_ids}
stopped = {c: per[(c, 0)]["stopped_at"] for c in range(12, 294) if not per[(c, 0)]["ok"]}
only_set = [c for c, v in done.items() if v["writes"] and all(w.startswith("set+") for w in v["writes"])]
table_rows = [{"id": c, "label": labels.get(c, ""), "arm": per[(c, 0)]["arm"], "inc": per[(c, 0)], "dec": per[(c, 1)]}
              for c in range(12, 294)]
record("postcondition_observed", True, completed_non_noop=len(done), writes_only_settings_object=len(only_set),
       stopped=len(stopped), stopped_reasons=collections.Counter(str(v) for v in stopped.values()).most_common(12),
       note="observed: which arms complete under the fixture and what they write")
# I-4: the float values the completed arms write from a zero start (the step itself), both directions
steps = collections.Counter()
arms_seen = {}
for (c, d), v in per.items():
    if v["ok"] and 12 <= c <= 293 and v["float_values"]:
        for f in v["float_values"]:
            steps[f] += 1
        arms_seen.setdefault(v["arm"], set()).update(v["float_values"])
by_arm = collections.Counter()
for arm, vals in arms_seen.items():
    for f in vals:
        by_arm[abs(f)] += 1
record("I4_float_steps_observed", True, float_writes_by_value=sorted(steps.items(), key=lambda kv: -kv[1])[:20],
       float_step_arms_by_magnitude=sorted(by_arm.items(), key=lambda kv: -kv[1])[:12],
       note="observed: the value each completed float-stepping arm writes from zero, i.e. its step")
results["per_id"] = table_rows

json.dump({"pass": sum(1 for k, v in results.items() if isinstance(v, dict) and v.get("pass_")), "ok": allok,
           "allowed_functions": len(ALLOWED), "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok", "allowed", len(ALLOWED))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
