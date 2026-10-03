"""S-22: RW-5 (the severe-weather accuracy gate, CONTRACT-weapon-recipes.md) and WE-3 (the MWeather class is consumed already banded,
CONTRACT-environmental-element-scaling.md) executed as shipped code (OPUS, 2026-09-26).

The gate lives in the step targets themselves: step 35 = 003895D0 and step 36 = 00389610 (step table 01EFA5C0). Each tests
context byte +0x1A bit 0x04, then calls 003214A0 (= jmp 00263E20, which returns [02099DAC], the banded weather gameplay class) and,
only when that is 2, scales the accuracy word [02AEDFE0] by 0.8 (step 35, constant 008F3108) or 0.5 (step 36, 01CEBB70).
Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image; NO application stub, no bridged import (every
IAT slot a trap); ALLOWED = the two steps' closures plus 00263E20 (the tail target of 003214A0). Planted data only: the context
record (r8), the class word [02099DAC], the accuracy word [02AEDFE0].
Cases:
 R1  byte +0x1A bit 0x04 clear and class 2: accuracy 100 -> 80 (step 35), 100 -> 50 (step 36).
 R2  bit 0x04 set: unchanged, whatever the class.
 R3  class 0 or 1: unchanged with the bit clear.
 R4  only bit 0x04 of the context gates: with every other bit of +0x18..+0x1B set (byte +0x1A = 0xFB), both steps still scale -
     so no other context bit (the element bypass included) opens or closes this gate.
 W3  00263E20 returns [02099DAC] verbatim for 0, 1, 2 and 5: the stage reads a class somebody else computed; nothing here
     re-bands it.
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
STEP35, STEP36, WEATHER_GET, CLASS, ACC = 0x3895D0, 0x389610, 0x263E20, 0x2099DAC, 0x2AEDFE0

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


ALLOWED = closure({STEP35, STEP36, WEATHER_GET}) | {WEATHER_GET}
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


def step(entry, ctx_bytes, cls, acc=100):
    uc.mem_write(FIX, bytes(0x100))
    uc.mem_write(FIX + 0x18, bytes(ctx_bytes))
    uc.mem_write(CLASS, struct.pack("<I", cls))
    uc.mem_write(ACC, struct.pack("<i", acc))
    ok = call(entry, FIX)
    return [ok, struct.unpack("<i", bytes(uc.mem_read(ACC, 4)))[0]]


res, cases = {}, {}
g = {}
for nm, e in (("step35", STEP35), ("step36", STEP36)):
    g[nm] = {"clear_class2": step(e, [0, 0, 0, 0], 2), "bit4_class2": step(e, [0, 0, 4, 0], 2), "clear_class1": step(e, [0, 0, 0, 0], 1),
             "clear_class0": step(e, [0, 0, 0, 0], 0), "others_set_class2": step(e, [0xFF, 0xFF, 0xFB, 0xFF], 2),
             "bit4_class1": step(e, [0, 0, 4, 0], 1)}
res["steps"] = g
cases["R1_bit_clear_class2_scales_08_and_05"] = g["step35"]["clear_class2"] == [True, 80] and g["step36"]["clear_class2"] == [True, 50]
cases["R2_bit4_set_leaves_accuracy"] = all(g[s][c] == [True, 100] for s in g for c in ("bit4_class2", "bit4_class1"))
cases["R3_class_0_or_1_leaves_accuracy"] = all(g[s][c] == [True, 100] for s in g for c in ("clear_class1", "clear_class0"))
cases["R4_only_that_bit_gates"] = g["step35"]["others_set_class2"] == [True, 80] and g["step36"]["others_set_class2"] == [True, 50]
w3 = {}
for v in (0, 1, 2, 5):
    uc.mem_write(CLASS, struct.pack("<I", v))
    ok = call(WEATHER_GET)
    w3[v] = [ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF]
res["weather_getter"] = w3
cases["W3_the_class_is_read_verbatim_not_rebanded"] = all(w3[v] == [True, v] for v in w3)
out = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(ALLOWED), **res}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k2, v2 in cases.items():
    print("%-46s %s" % (k2, "PASS" if v2 else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED", json.dumps(res))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
