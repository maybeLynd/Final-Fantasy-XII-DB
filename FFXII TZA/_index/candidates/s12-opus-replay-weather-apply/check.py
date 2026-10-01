"""S-12: execute the weather apply 0026D910 as shipped code over the shipped map_ref.bin / gramap_weatherinfo.bin
(OPUS, 2026-09-25, block 303). CONTRACT-weather.md section 13 is "Empty"; this is the first execution of the apply.

Evidence class: NATIVE-REPLAY (unicorn), live_game false.
- Whole SHA-asserted image mapped. NOTHING is stubbed. The run stops (does not stub) when the tail chain
  0026D910 -> jmp 002E3D40 -> jmp 0040AAD0 enters the presentation body 0040AAD0; its entry registers are recorded.
- Any entry into a function outside ALLOWED fails the case (the set below is the apply's static reach, read 2026-09-25).
- Fixtures (planted data, disclosed): the lazy singletons [01F81428] (debug block, 0x10E8 zeroed; +0xAAC = override),
  [01F82EA8] (0xB08 zeroed) and [01F81168] (0x400 zeroed; +0x398 = 0 so 001F08A0's sqrtf arm is not taken); the context
  payload 0x2164480 (+0x1044 field index, +0x1060 committed slot, +0x1061 restore gate) is the image's own .bss;
  [02099D88] = map_ref.bin (in locale), [02099D90] = 1 (loaded guard), [02ADD0B0] = gramap_weatherinfo.bin (in locale),
  both files loaded verbatim from the vbf extract (their SHA-256 is recorded).
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP,
                               UC_X86_REG_RBX, UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP, UC_X86_REG_RAX)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
MAPREF = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common\map_ref.bin"
MWEATHER = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common\gramap_weatherinfo.bin"
IMG = 0x120000
APPLY, STOP, EXTRACT, PRES = 0x26D910, 0x40AAD0, 0x3777C0, 0x377850
ALLOWED = {APPLY, 0x17D490, 0x1D50D0, 0x2EF2B0, 0x2EF640, 0x180620, 0x1A9930, 0x1A7E40, 0x1F0850, 0x3148F0,
           0x377850, 0x3777C0, 0x3777A0, 0x3777B0, 0x2E3D40, 0x264F10, 0x265920, STOP}
PAYLOAD = 0x2164480
STACK, STACK_SZ, RET = 0x70000000, 0x100000, 0x71000000
DBG, OBJ1, OBJ2, MRF, MWT = 0x72000000, 0x72100000, 0x72200000, 0x72300000, 0x72400000

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
mrf, mwt = open(MAPREF, "rb").read(), open(MWEATHER, "rb").read()
assert mrf[:4] == b"MRF\x02", "map_ref magic"
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")


def run(entry, regs, field, committed, gate, override=0):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for v, vs, ra, rs in secs:
        lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
        uc.mem_map(lo, hi - lo)
        uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
    for base, sz in ((STACK, STACK_SZ), (RET, 0x1000), (DBG, 0x2000), (OBJ1, 0x1000), (OBJ2, 0x1000), (MRF, 0x4000), (MWT, 0x2000)):
        uc.mem_map(base, sz)
    uc.mem_write(RET, b"\xF4")
    uc.mem_write(MRF, mrf)
    uc.mem_write(MWT, mwt)
    uc.mem_write(DBG + 0xAAC, struct.pack("<i", override))
    for cell, val in ((0x1F81428, DBG), (0x1F82EA8, OBJ2), (0x1F81168, OBJ1), (0x2099D88, MRF), (0x2099D90, 1), (0x2ADD0B0, MWT)):
        uc.mem_write(cell, struct.pack("<Q", val))
    uc.mem_write(PAYLOAD + 0x1044, struct.pack("<i", field))
    uc.mem_write(PAYLOAD + 0x1060, bytes([committed & 0xFF, gate]))
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in regs.items():
        uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    L = {"entered": [], "bad": [], "calls": [], "faults": [], "stop": None, "writes": []}

    def on_code(u, a, n, _):
        if a in FSTARTS:
            L["entered"].append("%08X" % a)
            if a not in ALLOWED:
                L["bad"].append("%08X" % a)
                u.emu_stop()
                return
        if a in (PRES, EXTRACT, 0x180620):
            L["calls"].append(["%08X" % a, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                               u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF])
        if a == STOP:
            L["stop"] = [u.reg_read(r) & 0xFFFFFFFF for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)]
            u.emu_stop()

    def on_w(u, ac, a, n, v, _):
        if 0x2099D80 <= a < 0x2099DC0 or PAYLOAD + 0x1040 <= a < PAYLOAD + 0x1070:
            L["writes"].append(["%08X" % a, n, v & 0xFFFFFFFF])

    def on_bad(u, ac, a, n, v, _):
        L["faults"].append([ac, "%08X" % a])
        return False

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    try:
        uc.emu_start(entry, RET, count=200000)
    except UcError as e:
        L["faults"].append(["uc", str(e)])
    L["rip"] = "%08X" % uc.reg_read(UC_X86_REG_RIP)
    L["rax"] = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    L["slot_after"], L["gate_after"] = struct.unpack("<bB", bytes(uc.mem_read(PAYLOAD + 0x1060, 2)))
    L["pub"] = {k: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0] for k, a in
                (("DA8", 0x2099DA8), ("DAC", 0x2099DAC), ("DB0", 0x2099DB0), ("DBC", 0x2099DBC))}
    return L


# fast extractor: ONE unicorn instance running the shipped 003777C0 repeatedly (used only to choose fixtures from the data)
_fx = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    _fx.mem_map(lo, hi - lo)
    _fx.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
_fx.mem_map(STACK, STACK_SZ); _fx.mem_map(RET, 0x1000); _fx.mem_map(MWT, 0x2000)
_fx.mem_write(RET, bytes([0xF4])); _fx.mem_write(MWT, mwt); _fx.mem_write(0x2ADD0B0, struct.pack("<Q", MWT))


def fx(sel, slot, bitoff, width):
    sp = STACK + STACK_SZ - 0x1000 - 8
    _fx.mem_write(sp, struct.pack("<Q", RET))
    _fx.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, sel), (UC_X86_REG_RDX, slot), (UC_X86_REG_R8, bitoff), (UC_X86_REG_R9, width)):
        _fx.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    _fx.emu_start(EXTRACT, RET, count=10000)
    return _fx.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


rows_off = struct.unpack_from("<i", mrf, 4)[0]
nsel = struct.unpack_from("<H", mwt, 6)[0]
FIELD = None
for fid in range(1315):
    sel, blk = struct.unpack_from("<Hh", mrf, rows_off + 8 * fid)
    if 0 < sel < nsel and blk >= 0:
        p1, p3 = fx(sel, 1, 0, 3), fx(sel, 3, 0, 3)
        a1, a3 = fx(sel, 1, 3, 4), fx(sel, 3, 3, 4)
        if p1 != p3 and (p1 or p3) and a1 != a3:
            FIELD = fid
            break
assert FIELD is not None
SEL, BLK = struct.unpack_from("<Hh", mrf, rows_off + 8 * FIELD)
I5SEL = None
for t in range(2, nsel - 1):
    v0, vp, v4, vn = fx(t, 0, 0, 3), fx(t - 1, 3, 0, 3), fx(t, 4, 0, 3), fx(t + 1, 1, 0, 3)
    if v0 and v4 and fx(t, 1, 0, 3) != v0:
        I5SEL = t
        break
assert I5SEL is not None

results, ok_all = {}, True
clean = lambda L: not L["faults"] and not L["bad"] and L["stop"] is not None


def rec(name, ok, L, extra=None):
    global ok_all
    ok_all &= bool(ok)
    d = {k: v for k, v in L.items() if k != "mem"}
    d.update(extra or {})
    d["pass"] = bool(ok)
    results[name] = d
    print("%-34s %s" % (name, "PASS" if ok else "FAIL"))


def pres_calls(L):
    return [c for c in L["calls"] if c[0] == "%08X" % PRES]


# 1. ungated apply of slot 3 from committed slot 1 (index 0): commit 2, both extractions use slot 3, gate stays 0
L = run(APPLY, {UC_X86_REG_RCX: 3}, FIELD, 0, 0)
pc = pres_calls(L)
rec("ungated-commit", clean(L) and L["slot_after"] == 2 and L["gate_after"] == 0 and len(pc) == 2 and pc[0][2] == 3 and pc[1][2] == 3, L,
    {"presentation_calls": pc})

# 2. I-3 + I-7: gate armed, committed slot 1, request slot 3 -> discarded (slot stays 0), gate cleared once,
#    gameplay extraction uses the requested slot (edx = 3), presentation extraction the committed one (edx = 1)
L = run(APPLY, {UC_X86_REG_RCX: 3}, FIELD, 0, 1)
pc = pres_calls(L)
rec("gated-discard-and-split-slots", clean(L) and L["slot_after"] == 0 and L["gate_after"] == 0 and len(pc) == 2
    and pc[0][2] == 3 and pc[1][2] == 1, L, {"presentation_calls": pc})

# 3. I-2 saturation: requests 0, 1 -> slot index 0; 9 -> 2; -5 -> 0
sat = {}
for req, want in ((0, 0), (1, 0), (9, 2), (-5, 0), (2, 1)):
    L = run(APPLY, {UC_X86_REG_RCX: req}, FIELD, 1, 0)
    sat[req] = (L["slot_after"], clean(L))
rec("i2-saturation", all(v == (w, True) for (req, w), v in zip(((0, 0), (1, 0), (9, 2), (-5, 0), (2, 1)), sat.values())), L, {"saturation": sat})

# 4. debug override: +0xAAC = 2 forces the requested slot to 2 whatever the argument
L = run(APPLY, {UC_X86_REG_RCX: 3}, FIELD, 0, 0, override=2)
rec("debug-override-forces-slot", clean(L) and L["slot_after"] == 1, L)

# 5. I-5: 003777C0 bounds only the selector. selector >= count -> 0; slot 0 / 4 are not checked and read the
#    neighbour selector's lanes: extract(sel, 0) == extract(sel-1, 3) and extract(sel, 4) == extract(sel+1, 1)
def ext(sel, slot, bitoff=0, width=3):
    L = run(EXTRACT, {UC_X86_REG_RCX: sel, UC_X86_REG_RDX: slot, UC_X86_REG_R8: bitoff, UC_X86_REG_R9: width}, FIELD, 0, 0)
    return L["rax"], (not L["faults"] and not L["bad"] and L["rip"] == "%08X" % RET)


oob = ext(nsel, 1)
a0, b0 = ext(I5SEL, 0), ext(I5SEL - 1, 3)
a4, b4 = ext(I5SEL, 4), ext(I5SEL + 1, 1)
rec("i5-selector-bound-slot-unchecked", oob == (0, True) and a0[1] and a0 == b0 and a4 == b4, L,
    {"i5_selector": I5SEL, "slot1_value": fx(I5SEL, 1, 0, 3), "oob": oob, "slot0_vs_prev_slot3": [a0, b0], "slot4_vs_next_slot1": [a4, b4], "nsel": nsel})

json.dump({"pass": sum(1 for v in results.values() if v["pass"]), "total": len(results), "ok": ok_all, "field": FIELD, "selector": SEL, "i5_selector": I5SEL,
           "block": BLK, "map_ref_sha256": hashlib.sha256(mrf).hexdigest(), "mweather_sha256": hashlib.sha256(mwt).hexdigest(),
           "results": results}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("%d/%d pass (field %d, selector %d, block %d)" % (sum(1 for v in results.values() if v["pass"]), len(results), FIELD, SEL, BLK))
