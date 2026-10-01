"""S-41 (OPUS, 2026-09-26): CONTRACT-audio-bank-and-controller-family executed for the first time - the broadcast (AC-4), the slot-10
command mask per class (AC-6) and the id gate (AC-7), stub-free.

The contract had no execution record (s41-runtime-per-invariant-exposure.md: coverage, not exposure). AC-1/AC-2/AC-3/AC-5 are vtable
layout facts (static structure). World: block 355's world.py, plus two real initialiser steps (as in s41-opus-replay-spatial-sources):
the audio object's own initialiser 00210AF0 and the allocation-callback installer 007AD620(00210EC0, 00210EB0) with the library
init's own arguments. Planted data (disclosed): bank objects (0x2000 bytes, a real bank vtable at +0, the circular list sentinel at
+0x08, list nodes {+0 next, +0x10 payload}); the audio object's readiness dword +0x38 = 1 and command dword +0x3C; the game-mode byte
02064AD3 = 5 (00210930 requires +0x38 != 0 and 002287A0: mode 5 or 6); Seb's own bank +0x38; Sep's bank id +0x38, +0x50 and +0x49.
One disclosed PERTURBATION (the AC-4 control only): during the first slot-9 call the bank's vtable pointer is switched to another
real bank class's vtable. No application stub.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import importlib.util
import json
import os
import re
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RDX

HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.join(HERE, "..", "s29-opus-replay-inventory-rebase")
GRAPH = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "graph", "functions.tsv"))
sys.path.insert(0, WD)
spec = importlib.util.spec_from_file_location("world355", os.path.join(WD, "world.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
FX = json.load(open(os.path.join(WD, "world.json")))
BANKS = {"Audio": 0x9078B0, "Music": 0x907910, "Seb": 0x907D80, "Sep": 0x907B48, "Shout": 0x907F90, "Stream": 0x9081A0}
img = pefile.PE(W.EXE).get_memory_mapped_image(); IB = 0x120000
VTS = {n: [struct.unpack_from("<Q", img, v - IB + 8 * k)[0] for k in range(11)] for n, v in BANKS.items()}
for f in [0x210AF0, 0x7AD620, 0x210EB0, 0x222550] + [x for vt in VTS.values() for x in vt]:
    W.ALLOWED |= W.closure(f) | {f}
S = W.Session(FX["fixes"], FX["inits"]); uc = S.uc
init = {"audio": S.call(0x210AF0), "callbacks": S.call(0x7AD620, 0x210EC0, 0x210EB0)}
AUD = struct.unpack("<Q", bytes(uc.mem_read(0x1FD36A0, 8)))[0]
SIZES = {}
for l in open(GRAPH, encoding="utf-8", errors="replace"):
    c = l.split("\t")
    if c[0] and all(ch in "0123456789abcdefABCDEF" for ch in c[0]) and len(c) > 2 and c[2].strip().isdigit():
        SIZES[int(c[0], 16)] = int(c[2])
md = Cs(CS_ARCH_X86, CS_MODE_64)
RX_VT = re.compile(r"qword ptr \[r\w+(?: \+ (0x[0-9a-f]+))?\]$")
cur = {"disp": []}


def slot10_hook(u, a, n, _):
    ins = next(md.disasm(bytes(u.mem_read(a, 16)), a), None)
    if ins and ins.mnemonic in ("call", "jmp"):
        m = RX_VT.match(ins.op_str)
        if m and "rip" not in ins.op_str:
            cur["disp"].append("slot%d" % (int(m.group(1) or "0", 16) // 8))
        elif ins.op_str.startswith("0x"):
            t = int(ins.op_str, 16)
            if t not in (0x210B30, 0x210930):
                cur["disp"].append("direct %08X" % t)


for f in sorted({vt[10] for vt in VTS.values()}):
    uc.hook_add(UC_HOOK_CODE, slot10_hook, begin=f, end=f + max(SIZES.get(f, 0x40), 0x20) - 1)
s9 = []
switch = {"to": None}


def slot9_hook(u, a, n, _):
    s9.append(("%08X" % a, "%X" % u.reg_read(UC_X86_REG_RDX)))
    if switch["to"] is not None and len(s9) == 1:
        u.mem_write(BANK, struct.pack("<Q", switch["to"]))


for f in {VTS["Sep"][9], VTS["Seb"][9]}:
    uc.hook_add(UC_HOOK_CODE, slot9_hook, begin=f, end=f)
s0 = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: s0.append(1), begin=0x222550, end=0x222550)
uc.ctl_flush_tb()
BANK = 0x72000000
uc.mem_map(BANK, 0x10000)
PAY = BANK + 0x4000


def fresh(cls):
    uc.mem_write(BANK, bytes(0x2000))
    uc.mem_write(BANK, struct.pack("<Q", BANKS[cls]))
    uc.mem_write(BANK + 8, struct.pack("<QQ", BANK + 8, BANK + 8))


res = {"live_game": False, "init": init, "slot10": {n: "%08X" % vt[10] for n, vt in VTS.items()}}
cases = {"real_initialisers": all(init.values())}
# ---- AC-4: the broadcast calls slot 9 once per entry, and re-loads the vtable on every entry ----
def broadcast(switch_to=None):
    fresh("Sep")
    nodes = [BANK + 0x100 + 0x40 * i for i in range(3)]
    uc.mem_write(BANK + 8, struct.pack("<QQ", nodes[0], nodes[-1]))
    for i, nd in enumerate(nodes):
        nxt = nodes[i + 1] if i + 1 < len(nodes) else BANK + 8
        uc.mem_write(nd, struct.pack("<QQQ", nxt, 0, PAY + 0x40 * i))
    del s9[:]; switch["to"] = switch_to
    ok = S.call(0x222550, BANK, 0)
    switch["to"] = None
    return {"ok": ok, "halt": (S.st["faults"][:1] or S.st["bad"][:1]), "slot9_calls": list(s9)}


b1 = broadcast()
b2 = broadcast(switch_to=BANKS["Seb"])
res["AC4"] = {"plain": b1, "vtable_switched_after_first_entry": b2}
pays = ["%X" % (PAY + 0x40 * i) for i in range(3)]
cases["AC4_slot9_once_per_entry_in_list_order_with_the_payload"] = b1["ok"] and [c[1] for c in b1["slot9_calls"]] == pays \
    and all(c[0] == "%08X" % VTS["Sep"][9] for c in b1["slot9_calls"])
cases["AC4_control_vtable_reloaded_every_entry"] = b2["ok"] and b2["slot9_calls"][0] == ("%08X" % VTS["Sep"][9], pays[0]) \
    and [c[1] for c in b2["slot9_calls"] if c[0] == "%08X" % VTS["Seb"][9]] == pays[1:]
# ---- AC-6: slot 10 per class ----
def s10(cls, bits, seb_gate=1):
    fresh(cls)
    if cls == "Seb":
        uc.mem_write(BANK + 0x38, struct.pack("<I", seb_gate))
    uc.mem_write(PAY, bytes(0x100))
    uc.mem_write(AUD + 0x38, struct.pack("<I", 1)); uc.mem_write(0x2064AD3, bytes([5])); uc.mem_write(AUD + 0x3C, struct.pack("<I", bits))
    cur["disp"] = []; del s0[:]
    ok = S.call(VTS[cls][10], BANK, PAY)
    return {"ok": ok, "halt": (S.st["faults"][:1] or S.st["bad"][:1]), "dispatch": list(cur["disp"])}


matrix = {c: {"%02X" % b: s10(c, b) for b in (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x3F)} for c in ("Music", "Seb", "Sep", "Shout", "Stream")}
matrix["Seb_own_gate_clear"] = {"%02X" % b: s10("Seb", b, seb_gate=0) for b in (0x02, 0x08)}
audio_abstract = s10("Audio", 0x01)
res["AC6"] = {"matrix": matrix, "AudioBank_slot10": audio_abstract}
got = lambda c, b: matrix[c]["%02X" % b]["dispatch"]
EXPECT = {
    "Music": {1: ["slot0"], 2: [], 4: [], 8: [], 0x10: [], 0x20: []},
    "Seb": {1: [], 2: ["slot9"], 4: [], 8: ["direct 00224290"], 0x10: ["direct 002240B0"], 0x20: ["direct 00224470"]},
    "Sep": {1: [], 2: ["slot9"], 4: [], 8: ["slot3"], 0x10: ["slot4"], 0x20: ["slot5"]},
    "Shout": {1: [], 2: [], 4: ["slot9"], 8: [], 0x10: [], 0x20: []},
    "Stream": {1: [], 2: [], 4: ["slot9"], 8: [], 0x10: [], 0x20: []},
}
res["AC6_expected_from_the_bytes"] = {c: {"%02X" % b: v for b, v in d.items()} for c, d in EXPECT.items()}
cases["AC6_each_class_dispatches_its_own_subset_of_bits"] = all(got(c, b) == EXPECT[c][b] for c in EXPECT for b in EXPECT[c])
# the only non-returning rows: Seb's direct callees for bits 8 / 0x10 fault on the planted all-zero payload AFTER the dispatch observed
res["AC6_rows_not_returning"] = {"%s %s" % (c, k): v["halt"] for c in EXPECT for k, v in matrix[c].items() if not v["ok"]}
cases["AC6_only_non_returning_rows_are_seb_direct_callees_on_a_zero_payload"] = set(res["AC6_rows_not_returning"]) <= {"Seb 08", "Seb 10"}
cases["AC6_bit2_is_a_tail_jump_that_ends_slot10_in_Seb_and_Sep"] = got("Seb", 0x3F) == ["slot9"] and got("Sep", 0x3F) == ["slot9"]
cases["AC6_seb_also_gates_on_its_own_plus38"] = all(v["dispatch"] == [] for v in matrix["Seb_own_gate_clear"].values())
cases["AC6_AudioBank_slot10_is_purecall"] = audio_abstract["halt"] == ["import _purecall"]
cases["AC6_contract_reading_every_bank_maps_every_bit_is_contradicted"] = any(got(c, b) != [] for c in EXPECT for b in (1, 2, 4, 8, 0x10, 0x20)) \
    and not all(got(c, 1) == ["slot0"] for c in EXPECT)
# ---- AC-7: Sep slot 3 gates the id band [150000, 151000) ----
def sep3(bank_id):
    fresh("Sep")
    uc.mem_write(BANK + 0x38, struct.pack("<I", bank_id))
    uc.mem_write(BANK + 0x50, struct.pack("<Q", 0x7C000000))
    uc.mem_write(BANK + 0x49, bytes([0x01]))
    del s0[:]
    ok = S.call(VTS["Sep"][3], BANK)
    return {"ok": ok, "halt": (S.st["faults"][:1] or S.st["bad"][:1]), "slot0_reached": bool(s0)}


ids = {i: sep3(i) for i in (149999, 150000, 150999, 151000, 152000)}
res["AC7_sep_slot3"] = {str(k): v for k, v in ids.items()}
# sub eax, 0x249F0 (= 150000) / cmp eax, 0x3E8 / jb -> ret: the band [150000, 151000) is skipped; below and above proceed
cases["AC7_sep_slot3_skips_the_band_150000_to_150999_only"] = [ids[i]["slot0_reached"] for i in (149999, 150000, 150999, 151000, 152000)] == [True, False, False, True, True] \
    and all(v["ok"] for v in ids.values())
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print({c: {b: v["dispatch"] for b, v in d.items()} for c, d in matrix.items()})
print("AC7", {k: v["slot0_reached"] for k, v in ids.items()}, "AC4", b2["slot9_calls"])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
