"""S-39: execute CONTRACT-render-command-list-and-graphics-handshake.md's entries as shipped code - both list constructors, the
enqueue, the forward and reverse walks, the marks, the clear, the owner's destroy, the flush and the handshake wait - and test
I-1 .. I-10 by call counting and memory diff (OPUS, 2026-09-25, block 312).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub; entering a
function outside ALLOWED fails the case. IMPORT BRIDGES by name, through the real IAT slots (the import directory is parsed from the
SHA-asserted image and EVERY slot points at a unique trap; an import without a bridge fails the case by name): malloc and
_aligned_malloc (a bump heap; one case makes malloc return 0), free and _aligned_free (recorded), memmove.
Command objects: the real enqueue 0018C610 builds its own class (vtable 009031D0); for the walks, the flush and the destroy
the harness plants objects of the shipped MapOrderedObject class (vtable 009010D8: slot 0 001E11D0, slot 1 00212C60 - a
null-gated delegate that returns when +0x08 is null - slot 2 0016EE70 'mov eax, 4') so every indirect call runs shipped
code that has no side effect beyond the one measured.
Fixtures (planted data only): the planted objects, the render-params singleton [01F7F5F0] (+0x49C), the device holder
[01F7F598], the walk-abort bytes [01DF08FC] / [01F7F594], the handshake word [02EBA3F8].
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
STACK, STACK_SZ, RET, WORLD, HEAP, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x73000000, 0x74000000
PARAMS, DEVHOLD, OBJS = WORLD, WORLD + 0x1000, WORLD + 0x2000
G_ORDERED, G_OWNER, G_PARAMS, G_DEVHOLD, G_ABORT_A, G_ABORT_B, G_HANDSHAKE, G_ENQ_COUNTER = (
    0x1F7F5E0, 0x1F7F5E8, 0x1F7F5F0, 0x1F7F598, 0x1DF08FC, 0x1F7F594, 0x2EBA3F8, 0x1F82EC0)
F = {"make_ordered": 0x18B480, "ordered_ctor": 0x18AD00, "make_owner": 0x18C9E0, "enqueue": 0x18C610, "walk_fwd": 0x18B100,
     "walk_rev": 0x18B1B0, "clear": 0x18B040, "destroy_owner": 0x18B810, "flush": 0x18C8F0, "handshake_wait": 0x36F2C0,
     "set_split": 0x18B510, "set_reverse_mark": 0x18B030, "toggle_mask_bit1": 0x18B070}
VT_MAP, SLOT0_MAP, SLOT1_MAP, SLOT2_MAP = 0x9010D8, 0x1E11D0, 0x212C60, 0x16EE70
BRIDGED = {"malloc", "_aligned_malloc", "free", "_aligned_free", "memmove"}

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


ALLOWED = set()
for e in list(F.values()) + [SLOT0_MAP, SLOT1_MAP, SLOT2_MAP, 0x193D50, 0x18D630, 0x189120, 0x809950, 0x210EB0, 0x19C590,
                             0x85E730, 0x18B3F0, 0x1AB570, 0x1F1B80, 0x212C50,
                             0x16D680, 0x1EDF10, 0x1EDF80, 0x1EDFE0, 0x16D690]:   # + the EASTL allocator vtable 00902720's slots (indirect)
    ALLOWED |= closure(e)
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

uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x10000)
uc.mem_map(HEAP, 0x100000)
uc.mem_map(BRIDGE, 0x2000)
uc.mem_write(RET, bytes([0xF4]))


def import_slots():
    """(slot VA, dll, name) for every IAT slot, from the PE import directory of the mapped image."""
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
        dll = raw[r2o(name):raw.index(b"\0", r2o(name))].decode()
        th, i = r2o(oft or ft), 0
        while True:
            e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
            if e == 0:
                break
            nm = "ord%d" % (e & 0xFFFF) if e >> 63 else raw[r2o(e) + 2:raw.index(b"\0", r2o(e) + 2)].decode()
            out.append((IMG + ft + 8 * i, dll, nm))
            i += 1
        dd += 20


BR = {}
uc.mem_write(BRIDGE, bytes([0xC3]) * 0x1000)
for i, (slot, dll, name) in enumerate(import_slots()):
    uc.mem_write(slot, struct.pack("<Q", BRIDGE + 0x4 * i))
    BR[BRIDGE + 0x4 * i] = name
state = {"bad": [], "faults": [], "calls": [], "heap": HEAP, "allocs": [], "frees": [], "fail_next_malloc": False}


def on_code(u, a, n, _):
    if a in BR:
        nm = BR[a]
        rcx, rdx, r8 = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        if nm not in BRIDGED:
            state["bad"].append("import " + nm)
            u.emu_stop()
            return
        if nm == "_aligned_malloc":
            state["heap"] = (state["heap"] + rdx - 1) & ~(rdx - 1)
            p = state["heap"]
            state["heap"] += (rcx + 0xF) & ~0xF
            state["allocs"].append([hex(rcx), hex(p), "aligned %d" % rdx])
            u.reg_write(UC_X86_REG_RAX, p)
        elif nm == "malloc":
            if state["fail_next_malloc"]:
                state["fail_next_malloc"] = False
                p = 0
            else:
                p = state["heap"]
                state["heap"] += (rcx + 0xF) & ~0xF
            state["allocs"].append([hex(rcx), hex(p)])
            u.reg_write(UC_X86_REG_RAX, p)
        elif nm in ("free", "_aligned_free"):
            state["frees"].append(rcx)
        else:
            data = bytes(u.mem_read(rdx, r8)) if r8 else b""
            u.mem_write(rcx, data)
            u.reg_write(UC_X86_REG_RAX, rcx)
        return
    if a in (SLOT1_MAP, SLOT2_MAP, SLOT0_MAP):
        state["calls"].append(({SLOT0_MAP: "slot0", SLOT1_MAP: "slot1", SLOT2_MAP: "slot2"}[a], u.reg_read(UC_X86_REG_RCX)))
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def call(entry, rcx=0, rdx=0, r8=0, r9=0):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
        uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    state.update(bad=[], faults=[], calls=[], allocs=[], frees=[])
    try:
        uc.emu_start(entry, RET, count=2000000)
    except UcError as e:
        state["faults"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]


def q(a):
    return struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]


def d(a):
    return struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]


def entries(lst):
    b, e = q(lst), q(lst + 8)
    return [q(b + 8 * i) for i in range((e - b) // 8)]


def set_entries(lst, ptrs):
    b = q(lst)
    for i, p in enumerate(ptrs):
        uc.mem_write(b + 8 * i, struct.pack("<Q", p))
    uc.mem_write(lst + 8, struct.pack("<Q", b + 8 * len(ptrs)))


def map_objs(n, sel=None):
    out = []
    for i in range(n):
        o = OBJS + 0x40 * i
        uc.mem_write(o, struct.pack("<QQB", VT_MAP, 0, 1 if sel is None else sel[i]) + bytes(0x40 - 17))
        out.append(o)
    return out


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-32s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


uc.mem_write(G_PARAMS, struct.pack("<Q", PARAMS))
uc.mem_write(G_DEVHOLD, struct.pack("<Q", DEVHOLD))
uc.mem_write(DEVHOLD + 8, struct.pack("<Q", 0xD0D0D0D0))

# A. construction (section 3, I-3)
ok1 = call(F["make_ordered"])
allocs_ordered = list(state["allocs"])
L = q(G_ORDERED)
ok2 = call(F["make_owner"])
allocs_owner = list(state["allocs"])
O = q(G_OWNER)
lay = {"classMask": hex(d(L + 0x20)), "forwardSplit": d(L + 0x24), "splitArmed": uc.mem_read(L + 0x28, 1)[0],
       "reverseMark": hex(d(L + 0x2C)), "reserve_entries": (q(L + 0x10) - q(L)) // 8, "count": (q(L + 8) - q(L)) // 8,
       "allocator_vtable": "%08X" % q(L + 0x18), "owner_allocator_vtable": "%08X" % q(O + 0x18),
       "owner_count": (q(O + 8) - q(O)) // 8}
a_ok = (ok1 and ok2 and lay["classMask"] == "0xffffffff" and lay["forwardSplit"] == 0 and lay["reverseMark"] == "0xffffffff"
        and lay["reserve_entries"] == 5000 and lay["count"] == 0 and lay["allocator_vtable"] == "00902720"
        and lay["owner_allocator_vtable"] == "00902720" and allocs_ordered[0][0] == "0x30" and allocs_owner[0][0] == "0x20")
record("A_construction", a_ok, layout=lay, ordered_mallocs=allocs_ordered, owner_mallocs=allocs_owner,
       note="0x30 ordered list (mask -1, split 0, reverse mark -1, 5,000-entry reserve), 0x20 owner vector")

# B. enqueue: the same pointer on both lists (I-1); a failed malloc appends a null to both (I-9)
made = []
for arg in (1, 0, 5):
    ok = call(F["enqueue"], O, arg)
    made.append([ok, state["allocs"], d(G_ENQ_COUNTER)])
state["fail_next_malloc"] = True
okf = call(F["enqueue"], O, 7)
own, ordl = entries(O), entries(L)
objs = [p for p in own if p]
lay_objs = [{"vtable": "%08X" % q(p), "+08": q(p + 8), "+10": uc.mem_read(p + 0x10, 1)[0], "+18": d(p + 0x18)} for p in objs]
b_ok = (all(m[0] for m in made) and okf and own == ordl and len(own) == 4 and own[3] == 0 and len(objs) == 3
        and all(o["vtable"] == "009031D0" and o["+08"] == 0 and o["+10"] == 1 for o in lay_objs)
        and [o["+18"] for o in lay_objs] == [1, 0, 5] and all(m[1][0][0] == "0x20" for m in made))
record("B_enqueue_both_lists", b_ok, owner_list=[hex(x) for x in own], ordered_list=[hex(x) for x in ordl], objects=lay_objs,
       counter_after_each=[m[2] for m in made],
       note="every enqueue appends ONE pointer to BOTH lists; malloc(0x20); a failed malloc appends null to both")

# C. the walks over planted MapOrderedObject entries plus a null, with a forward split after two entries
def reset_ordered(n_before_split, n_after, null_at=None):
    call(F["clear"], L)
    objs = map_objs(n_before_split + n_after)
    ptrs = list(objs)
    if null_at is not None:
        ptrs.insert(null_at, 0)
    set_entries(L, ptrs[:n_before_split])
    call(F["set_split"], L, 0)                   # unarmed: split = current count
    set_entries(L, ptrs)
    return ptrs


walk = {}
ptrs = reset_ordered(2, 3, null_at=3)
uc.mem_write(G_ABORT_A, b"\x01")
uc.mem_write(G_ABORT_B, b"\x00")
for part in (1, 0):
    ok = call(F["walk_fwd"], L, part, 0xDEAD)
    walk["fwd_part%d" % part] = {"ok": ok, "slot2": [hex(x) for s, x in state["calls"] if s == "slot2"],
                                 "slot1": [hex(x) for s, x in state["calls"] if s == "slot1"]}
split = d(L + 0x24)
exp1, exp0 = [p for p in ptrs[:split] if p], [p for p in ptrs[split:] if p]
fwd_ok = (walk["fwd_part1"]["slot1"] == [hex(x) for x in exp1] and walk["fwd_part0"]["slot1"] == [hex(x) for x in exp0]
          and walk["fwd_part1"]["slot2"] == walk["fwd_part1"]["slot1"] and walk["fwd_part0"]["slot2"] == walk["fwd_part0"]["slot1"])
# I-4: the key is a mask - clear bit 2 of the list mask and nothing executes
uc.mem_write(L + 0x20, struct.pack("<I", 0xFFFFFFFB))
call(F["walk_fwd"], L, 0, 0xDEAD)
masked = {"slot2": len([1 for s, x in state["calls"] if s == "slot2"]), "slot1": len([1 for s, x in state["calls"] if s == "slot1"])}
uc.mem_write(L + 0x20, struct.pack("<I", 0xFFFFFFFF))
# I-7: [01DF08FC] == 0 and [01F7F594] != 0 -> the walk exits at the first masked-in entry
uc.mem_write(G_ABORT_A, b"\x00")
uc.mem_write(G_ABORT_B, b"\x01")
call(F["walk_fwd"], L, 0, 0xDEAD)
aborted = {"slot2": len([1 for s, x in state["calls"] if s == "slot2"]), "slot1": len([1 for s, x in state["calls"] if s == "slot1"])}
uc.mem_write(G_ABORT_A, b"\x01")
uc.mem_write(G_ABORT_B, b"\x00")
# the reverse walk, both r9b arms, params +0x49C = 0; I-5 - slot 2 twice per entry
rev = {}
for r9b in (0, 1):
    uc.mem_write(PARAMS + 0x49C, struct.pack("<I", 0))
    ok = call(F["walk_rev"], L, 0xDEAD, 0xFFFFFFFF, r9b)
    rev["r9b_%d" % r9b] = {"ok": ok, "slot2_calls": len([1 for s, x in state["calls"] if s == "slot2"]),
                           "slot1_order": [hex(x) for s, x in state["calls"] if s == "slot1"]}
nonnull = [p for p in ptrs if p]
rev_ok = all(v["ok"] for v in rev.values()) and rev["r9b_0"]["slot2_calls"] == 2 * len(nonnull)
c_ok = fwd_ok and masked == {"slot2": len(exp0), "slot1": 0} and aborted["slot1"] == 0 and aborted["slot2"] == 1 and rev_ok
record("C_walks_I4_I5_I7", c_ok, list=[hex(x) for x in ptrs], forward_split=split, forward=walk, masked_out=masked, abort_I7=aborted,
       reverse=rev, note="forward: part 1 = [0, split), part 0 = [split, count), null skipped, key called once; masked-out: key "
                         "called, nothing executed; I-7 exits at the first masked-in entry; reverse: key twice per entry")

# D. marks and clear (I-8), and the clear touches no object (I-1)
call(F["set_split"], L, 1)
armed = (uc.mem_read(L + 0x28, 1)[0], d(L + 0x24))
call(F["set_split"], L, 0)
unarmed = (uc.mem_read(L + 0x28, 1)[0], d(L + 0x24))
call(F["set_reverse_mark"], L)
rmark = d(L + 0x2C)
call(F["toggle_mask_bit1"], L, 0)
m0 = d(L + 0x20)
call(F["toggle_mask_bit1"], L, 1)
m1 = d(L + 0x20)
objs_before = bytes(uc.mem_read(OBJS, 0x200))
okc = call(F["clear"], L)
cleared = {"count": (q(L + 8) - q(L)) // 8, "split": d(L + 0x24), "reverseMark": hex(d(L + 0x2C)), "frees": len(state["frees"]),
           "slot0_calls": len([1 for s, x in state["calls"] if s == "slot0"]), "objects_unchanged": bytes(uc.mem_read(OBJS, 0x200)) == objs_before}
d_ok = (armed == (1, 0) and unarmed == (0, len(ptrs)) and rmark == len(ptrs) and m0 == 0xFFFFFFFD and m1 == 0xFFFFFFFF and okc
        and cleared == {"count": 0, "split": 0, "reverseMark": "0xffffffff", "frees": 0, "slot0_calls": 0, "objects_unchanged": True})
record("D_marks_and_clear_I8_I1", d_ok, split_armed=armed, split_unarmed=unarmed, reverse_mark=rmark, mask_after_toggle_0=hex(m0),
       mask_after_toggle_1=hex(m1), after_clear=cleared, note="the clear resets both marks and frees nothing")

# E. the owner's destroy (I-1): slot 0 with the free bit on every non-null entry
call(F["clear"], L)
objs3 = map_objs(3)
set_entries(O, [objs3[0], 0, objs3[1], objs3[2]])
oke = call(F["destroy_owner"], O)
e_ok = oke and state["frees"] == objs3 and [x for s, x in state["calls"] if s == "slot0"] == objs3 and (q(O + 8) - q(O)) // 8 == 0
record("E_owner_destroys_I1", e_ok, frees=[hex(x) for x in state["frees"]], owner_count_after=(q(O + 8) - q(O)) // 8,
       note="slot 0 (scalar-deleting) on each non-null entry frees it; the vector is emptied")

# F. the flush (I-6): executes the entries whose +0x10 is ZERO, then destroys every entry
objs3 = map_objs(3, sel=[1, 0, 1])
set_entries(O, objs3)
okf = call(F["flush"], O)
executed = [x for s, x in state["calls"] if s == "slot1"]
f_ok = okf and executed == [objs3[1]] and state["frees"] == objs3 and (q(O + 8) - q(O)) // 8 == 0
record("F_flush_I6", f_ok, executed=[hex(x) for x in executed], frees=[hex(x) for x in state["frees"]],
       note="executes only +0x10 == 0 (one of three), then destroys all three and empties the vector")

# G. the handshake wait never waits (I-10)
uc.mem_write(G_HANDSHAKE, struct.pack("<I", 0xFFFF))
okg = call(F["handshake_wait"])
hw = d(G_HANDSHAKE)
record("G_handshake_I10", okg and hw == 0xFFFF & 0xFFFFFEF3, word_after=hex(hw), note="returns at once and clears bits 2, 3 and 8")

json.dump({"pass": sum(1 for v in results.values() if v["pass_"]), "total": len(results), "ok": allok, "allowed_functions": len(ALLOWED),
           "results": results}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("%d/%d pass (allowed %d functions)" % (sum(1 for v in results.values() if v["pass_"]), len(results), len(ALLOWED)))
