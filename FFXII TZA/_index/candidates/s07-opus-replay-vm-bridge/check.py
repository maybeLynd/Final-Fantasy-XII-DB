"""S-07: CONTRACT-script-to-native-bridge.md's value-stack helpers and result writers executed as shipped code, stub-free - the
error reporter 008620C0 included, which EXP-013 replaced with a `ret` (OPUS, 2026-09-26).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The whole SHA-asserted image is mapped. NO application stub, no stop
boundary, no bridged import: every IAT slot points at a trap and reaching one fails the case. ALLOWED = the static closures of
the seven entries plus 0016D6A0, the reporter's tail-jump target (the call graph has no tail-jump edges).
Entries: pop int32 00267E10, pop float32 00267DB0, push int32 00267F90, push float32 00267F60, write int32 result 0026B4E0,
write float32 result 0026B4C0, the reporter 008620C0.
Fixtures: planted data only - a VmValueStack (0x284) and an ActorStorageRecord with its wait-slot array.
Cases:
 L   LIFO: pushes 11, 22, 33 pop back as 33, 22, 11; a pop decrements first and reads the tag at the new depth.
 K   coercion: an int slot popped as float is cvtdq2ps (7 -> 7.0); a float slot popped as int is cvttss2si (2.9 -> 2,
     -2.9 -> -2). The tag decides the conversion, not legality.
 W   a push writes all four arrays: tag 1 / 2, source kind 6, +0x84 = 0, the value at +0x184; an int push and a float push
     of the same bits leave identical bytes apart from the tag.
 G   the push guard: at depth 0x3F neither push writes anything and depth stays 0x3F; the highest slot a push fills is 62.
 U   underflow: the int pop on depth 0 returns 0 WITHOUT calling 008620C0; the float pop calls 008620C0(1) and returns 0.0;
     depth stays 0 in both.
 T   an unknown tag (3): the int pop calls 008620C0(1) and returns 0; the float pop returns 0.0 WITHOUT the call; depth is
     decremented in both.
 E   the reporter: 008620C0 is `lea rdx, msg; xor ecx, ecx; jmp 0016D6A0` and 0016D6A0 is `ret 0` in the shipping image -
     run as shipped it writes nothing outside the stack. EXP-013's `ret` stub therefore stood for exactly what ships.
 R   the result writers: entry = [rec+0xA8] + (int8)[rec+0x11] * 40; the int writer stores +0x0C and +0x15 = 2, the float
     writer +0x0C and +0x15 = 3; with [rec+0x11] = -1 (0xFF, read with movsx) they write the entry BEFORE the array.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP,
                               UC_X86_REG_RAX, UC_X86_REG_XMM0, UC_X86_REG_XMM1)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, BUF, TRAP = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
POPI, POPF, PUSHI, PUSHF, WRI, WRF, REPORT, ASSERT = 0x267E10, 0x267DB0, 0x267F90, 0x267F60, 0x26B4E0, 0x26B4C0, 0x8620C0, 0x16D6A0

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for row in csv.DictReader(open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8"), delimiter="\t"):
    if row["callee_external"] != "true":
        graph[int(row["caller"], 16)].add(int(row["callee"], 16))


def closure(s):
    seen, st_ = set(), [s]
    while st_:
        x = st_.pop()
        if x not in seen:
            seen.add(x)
            st_.extend(graph[x])
    return seen


ALLOWED = set().union(*(closure(e) for e in (POPI, POPF, PUSHI, PUSHF, WRI, WRF, REPORT, ASSERT)))
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
for base, size in ((STACK, STACK_SZ), (RET, 0x1000), (BUF, 0x10000), (TRAP, 0x4000)):
    uc.mem_map(base, size)
uc.mem_write(RET, b"\xF4")
uc.mem_write(TRAP, b"\xC3" * 0x4000)
imp_rva = struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]


def r2o(rva):
    for v, vs, ra, rs in secs:
        if v - IMG <= rva < v - IMG + max(vs, rs):
            return ra + rva - (v - IMG)


TRAPS, dd, k = {}, r2o(imp_rva), 0
while True:
    oft, _, _, name, ft = struct.unpack_from("<IIIII", raw, dd)
    if not (oft or name or ft):
        break
    i = 0
    while struct.unpack_from("<Q", raw, r2o(oft or ft) + 8 * i)[0]:
        uc.mem_write(IMG + ft + 8 * i, struct.pack("<Q", TRAP + 4 * k))
        TRAPS[TRAP + 4 * k] = True
        i += 1
        k += 1
    dd += 20
st = {"bad": [], "faults": [], "reports": []}


def on_code(u, a, n, _):
    if a in TRAPS:
        st["bad"].append("import trap %X" % a)
        u.emu_stop()
    elif a == REPORT:
        st["reports"].append(u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF)
    elif a in FSTARTS and a not in ALLOWED:
        st["bad"].append("%08X" % a)
        u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_code)
writes = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: writes.append((a, n)))


def call(entry, rcx=0, rdx=0, xmm1=None):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_XMM0, 0x7FC00000)               # a NaN, so an unwritten xmm0 is visible
    if xmm1 is not None:
        uc.reg_write(UC_X86_REG_XMM1, struct.unpack("<I", struct.pack("<f", xmm1))[0])
    st.update(bad=[], faults=[], reports=[])
    del writes[:]
    try:
        uc.emu_start(entry, RET, count=100000)
    except UcError as e:
        st["faults"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not st["bad"] and not st["faults"]


STK, REC, SLOTS = BUF, BUF + 0x1000, BUF + 0x2000
eax = lambda: uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
seax = lambda: struct.unpack("<i", struct.pack("<I", eax()))[0]
xmm0 = lambda: struct.unpack("<f", struct.pack("<I", uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]
depth = lambda: struct.unpack("<i", bytes(uc.mem_read(STK, 4)))[0]


def fresh(d=0):
    uc.mem_write(STK, b"\xEE" * 0x284)
    uc.mem_write(STK, struct.pack("<i", d))


results, cases = {}, {}
# L
fresh()
for v in (11, 22, 33):
    call(PUSHI, STK, v)
pops = []
for _ in range(3):
    okp = call(POPI, STK)
    pops.append([okp, seax(), depth()])
results["lifo"] = pops
cases["L_lifo_decrement_then_read"] = [p[1:] for p in pops] == [[33, 2], [22, 1], [11, 0]] and all(p[0] for p in pops)
# K
fresh()
call(PUSHI, STK, 7)
call(POPF, STK)
k_if = xmm0()
fresh()
call(PUSHF, STK, xmm1=2.9)
call(POPI, STK)
k_fi = seax()
fresh()
call(PUSHF, STK, xmm1=-2.9)
call(POPI, STK)
k_fin = seax()
results["coerce"] = {"int7_as_float": k_if, "float2.9_as_int": k_fi, "float-2.9_as_int": k_fin}
cases["K_pops_coerce_by_tag"] = k_if == 7.0 and k_fi == 2 and k_fin == -2
# W
fresh()
call(PUSHI, STK, 0x40490FDB)
wi = bytes(uc.mem_read(STK, 0x284))
fresh()
call(PUSHF, STK, xmm1=struct.unpack("<f", struct.pack("<I", 0x40490FDB))[0])
wf_ = bytes(uc.mem_read(STK, 0x284))
diff = [i for i in range(0x284) if wi[i] != wf_[i]]
results["push_arrays"] = {"int_tag": wi[4], "float_tag": wf_[4], "kind": [wi[0x44], wf_[0x44]], "reserved": [wi[0x84:0x88].hex(), wf_[0x84:0x88].hex()],
                          "value": [wi[0x184:0x188].hex(), wf_[0x184:0x188].hex()], "differing_offsets": diff}
cases["W_push_writes_all_four_arrays"] = wi[4] == 1 and wf_[4] == 2 and wi[0x44] == wf_[0x44] == 6 and wi[0x84:0x88] == wf_[0x84:0x88] == bytes(4) \
    and wi[0x184:0x188] == wf_[0x184:0x188] == struct.pack("<I", 0x40490FDB) and diff == [4] and wi[0:4] == struct.pack("<i", 1)
# G
fresh(0x3F)
gi = call(PUSHI, STK, 5)
gwi = [(a, n) for a, n in writes if not (STACK <= a < STACK + STACK_SZ)]
gf = call(PUSHF, STK, xmm1=1.5)
gwf = [(a, n) for a, n in writes if not (STACK <= a < STACK + STACK_SZ)]
fresh()
for v in range(70):
    call(PUSHI, STK, v)
top = depth()
last_slot_tag = [uc.mem_read(STK + 4 + s, 1)[0] for s in (61, 62, 63)]
results["guard"] = {"writes_at_3F": [gwi, gwf], "depth_after_70_pushes": top, "tags_61_62_63": last_slot_tag}
cases["G_push_guard_63_usable_slots"] = gi and gf and gwi == [] and gwf == [] and depth() == 0x3F and top == 0x3F \
    and last_slot_tag == [1, 1, 0xEE]
# U
fresh(0)
ui = call(POPI, STK)
u_int = [ui, eax(), list(st["reports"]), depth()]
uf = call(POPF, STK)
u_flt = [uf, xmm0(), list(st["reports"]), depth()]
results["underflow"] = {"int": u_int, "float": u_flt}
cases["U_underflow_int_silent_float_reports"] = u_int == [True, 0, [], 0] and u_flt == [True, 0.0, [1], 0]
# T
fresh()
call(PUSHI, STK, 9)
uc.mem_write(STK + 4, b"\x03")
ti = call(POPI, STK)
t_int = [ti, eax(), list(st["reports"]), depth()]
fresh()
call(PUSHI, STK, 9)
uc.mem_write(STK + 4, b"\x03")
tf = call(POPF, STK)
t_flt = [tf, xmm0(), list(st["reports"]), depth()]
results["unknown_tag"] = {"int": t_int, "float": t_flt}
cases["T_unknown_tag_int_reports_float_silent"] = t_int == [True, 0, [1], 0] and t_flt == [True, 0.0, [], 0]
# E
body = bytes(uc.mem_read(REPORT, 14))
assert_body = bytes(uc.mem_read(ASSERT, 3))
er = call(REPORT, 1)
ew = [(hex(a), n) for a, n in writes if not (STACK <= a < STACK + STACK_SZ)]
results["reporter"] = {"008620C0": body.hex(), "0016D6A0": assert_body.hex(), "writes_outside_stack": ew}
cases["E_reporter_is_a_no_op_in_the_shipping_image"] = er and ew == [] and assert_body == bytes.fromhex("c20000") \
    and body[7:9] == b"\x33\xc9" and body[9] == 0xE9


# R
def writer(fn, idx, val=None, fval=None):
    uc.mem_write(REC, bytes(0x100))
    uc.mem_write(SLOTS - 0x40, b"\xEE" * 0x200)
    uc.mem_write(REC + 0x11, bytes([idx & 0xFF]))
    uc.mem_write(REC + 0xA8, struct.pack("<Q", SLOTS))
    okw = call(fn, REC, val or 0, xmm1=fval)
    touched = sorted({a - SLOTS for a, n in writes if SLOTS - 0x40 <= a < SLOTS + 0x1C0})
    return okw, touched


r_i = writer(WRI, 2, val=0x1234)
r_f = writer(WRF, 1, fval=3.5)
r_neg = writer(WRI, -1, val=77)
e2 = SLOTS + 2 * 40
results["result_writers"] = {"int_idx2_offsets": r_i[1], "float_idx1_offsets": r_f[1], "int_idx_minus1_offsets": r_neg[1]}
cases["R_result_writers_signed_index_and_phase_byte"] = r_i[0] and r_i[1] == [80 + 0x0C, 80 + 0x15] \
    and r_f[0] and r_f[1] == [40 + 0x0C, 40 + 0x15] and r_neg[0] and r_neg[1] == [-40 + 0x0C, -40 + 0x15]
writer(WRI, 2, val=0x1234)
ri_vals = [struct.unpack("<I", bytes(uc.mem_read(e2 + 0x0C, 4)))[0], uc.mem_read(e2 + 0x15, 1)[0]]
writer(WRF, 1, fval=3.5)
rf_vals = [struct.unpack("<f", bytes(uc.mem_read(SLOTS + 40 + 0x0C, 4)))[0], uc.mem_read(SLOTS + 40 + 0x15, 1)[0]]
results["result_values"] = {"int": ri_vals, "float": rf_vals}
cases["R_result_writers_signed_index_and_phase_byte"] &= ri_vals == [0x1234, 2] and rf_vals == [3.5, 3]

out = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(ALLOWED), **results}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k2, v2 in cases.items():
    print("%-50s %s" % (k2, "PASS" if v2 else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED", "(allowed %d functions)" % len(ALLOWED))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
