"""Regression for the encoded-id query dispatch 00309EC0 (OPUS, 2026-09-26): which table it indexes and which arguments it passes.

The claim (CONTRACT-encoded-id-space-and-class-registry.md, the 00309EC0 paragraph): the class nibble selects a 0x58-stride row of
the registry at 01EEBCC0, and a non-null row +0x50 is tail-called as handler(id, 0) - ECX = the zero-extended encoded id, EDX = 0.
Two wrong readings this regression must reject:
  WRONG_BASE  the table is 01EC81F0 (FRONTIER-REQ-OPUS-VERIFY-01EC81F0-VS-01EEBCC0-S05-MERGE, after 69e9cad19) - REFUTED
  SWAPPED     the handler is called with (0, id)   (the contract's former '(0, cx)') - CORRECTED
These controls prove the DISPATCH and its ABI. They do not prove what any inventory callback means.

Parts:
  A  identity: the image file's SHA-256 is the authority's; the 00309EC0 body bytes (0x66) are compared with the expected bytes, and the
     operands are decoded from them: the lea at 00309EF4 (disp 0x01BE1DC5, next ip 00309EFB -> 01EEBCC0), 00309F1A xor edx,edx,
     00309F1C movzx ecx,r8w, 00309F20 jmp rax; 0030944F lea -> 01EEBCF8 = 01EEBCC0 + 0x38.
  B  executed discriminator (NATIVE-REPLAY, block 355's world, no application stub): the storage is bound by the shipped rebase
     0030B6A0; a DECOY table is planted at 01EC81F0 - in emulator memory only, its original bytes saved and restored. In the image
     that span is referenced by no instruction, read as fifteen 0x58 rows every +0x3C count is 0, and from +0x2F0 it holds an
     unrelated pointer table. The decoy rows get count 0xFFF and point +0x50 at the OTHER query handler; ARGUMENT CAPTURE at both query handlers' entries records (ecx, edx); a read hook records which +0x50 cell
     the dispatcher fetched. Each interpretation is a predicate over the observation. The shipped image must pass VALID and fail
     WRONG_BASE and SWAPPED, for five ids across packed and bitset classes.
  C  mutants of a private image copy, each restored: M_BASE retargets the lea to 01EC81F0; M_SWAP replaces the argument setup with
     movzx edx,r8w / xor ecx,ecx (same 6 bytes). Each must FAIL VALID and PASS exactly its own wrong reading - the checker is shown
     to discriminate both ways.
  D  text regression over the current consumers: no current (unstruck) statement may give 00309EC0 the base 01EC81F0 or the
     argument order (0, cx)/(0, id); self-test: the contract's verbatim pre-repair sentence is rejected, the repaired one accepted.
Writes result.json. live_game false.
"""
import hashlib
import importlib.util
import json
import os
import re
import struct
import sys

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
WD = os.path.join(HERE, "..", "s29-opus-replay-inventory-rebase")
sys.path.insert(0, WD)
spec = importlib.util.spec_from_file_location("world355", os.path.join(WD, "world.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
FX = json.load(open(os.path.join(WD, "world.json")))
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
DISP, REBASE, CLSID = 0x309EC0, 0x30B6A0, 0x309440
REG, DECOY = 0x1EEBCC0, 0x1EC81F0
QH_PACKED, QH_BITSET = 0x2FD8D0, 0x2FD970
res = {"live_game": False}

# ---- A: identity and operands ----
raw = open(W.EXE, "rb").read()
res["A"] = {"exe_sha256": hashlib.sha256(raw).hexdigest()}
EXPECT = bytes.fromhex(
    "b8ffff0000440fb7c1663bc8750483c8ffc3b900f00000410fb7c06623c1b900e00000663bc177e6410fb7c048c1e80c486bd058488d05c51dbe01"
    "410fb7c84803d081e1ff0f00008b423cffc83bc87f12488b42504885c0740933d2410fb7c848ffe033c0c3")
W.ALLOWED |= {0x16D6A0, QH_PACKED, QH_BITSET} | W.closure(REBASE) | W.closure(DISP) | W.closure(QH_PACKED) | W.closure(QH_BITSET)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
body = bytes(uc.mem_read(DISP, len(EXPECT)))
lea_disp = struct.unpack("<i", body[0x37:0x3B])[0]
lea_next = DISP + 0x3B
cls_disp = struct.unpack("<i", bytes(uc.mem_read(0x30944F + 3, 4)))[0]
res["A"].update({"body_bytes_equal_expected": body == EXPECT, "lea_at": "00309EF4", "lea_disp": "%08X" % lea_disp,
                 "lea_target": "%08X" % (lea_next + lea_disp), "tail": body[0x5A:0x63].hex(),
                 "classid_lea_target": "%08X" % (0x309456 + cls_disp)})
A_ok = (res["A"]["exe_sha256"] == EXE_SHA and body == EXPECT and lea_next + lea_disp == REG and body[0x5A:0x63] == bytes.fromhex("33d2410fb7c848ffe0")
        and 0x309456 + cls_disp == REG + 0x38)

# ---- B: the executed discriminator ----
BLOCK, SIZE = 0x76280000, 0x7410
uc.mem_write(BLOCK, bytes(SIZE))
assert S.call(REBASE, BLOCK)
decoy_orig = bytes(uc.mem_read(DECOY, 15 * 0x58))     # the image's own bytes there: zero to +0x2F0, then an unrelated pointer table
res["A"]["decoy_span_as_rows"] = [{"row": c, "count_3C": struct.unpack_from("<I", decoy_orig, c * 0x58 + 0x3C)[0],
                                   "slot_50": "%X" % struct.unpack_from("<Q", decoy_orig, c * 0x58 + 0x50)[0]} for c in range(15)]
A_ok = A_ok and all(r_["count_3C"] == 0 for r_ in res["A"]["decoy_span_as_rows"])
real50 ={c: struct.unpack("<Q", bytes(uc.mem_read(REG + c * 0x58 + 0x50, 8)))[0] for c in range(15)}
for c in range(15):                                   # the decoy: same counts, the OTHER query handler, no storage
    other = QH_BITSET if real50[c] == QH_PACKED else QH_PACKED
    uc.mem_write(DECOY + c * 0x58 + 0x3C, struct.pack("<I", 0xFFF))
    uc.mem_write(DECOY + c * 0x58 + 0x50, struct.pack("<Q", other))
obs = {"entries": [], "reads50": []}


def on_code(u, a, n, _):
    if a in (QH_PACKED, QH_BITSET) and obs.get("armed"):
        obs["entries"].append({"handler": "%08X" % a, "ecx": u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, "edx": u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF})


def on_read(u, acc, a, n, v, _):
    if obs.get("armed") and n == 8 and ((REG <= a < REG + 15 * 0x58) or (DECOY <= a < DECOY + 15 * 0x58)) and (a - (REG if a >= REG else DECOY)) % 0x58 == 0x50:
        obs["reads50"].append("%08X" % a)


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_READ, on_read)
uc.ctl_flush_tb()
IDS = [0x0005, 0x1007, 0x2003, 0x3004, 0xC001]


def observe(idv):
    obs.update(entries=[], reads50=[], armed=True)
    ok = S.call(DISP, idv, 0x5A5A)                      # a junk RDX: the dispatcher must set EDX itself
    obs["armed"] = False
    first = obs["entries"][0] if obs["entries"] else None
    return {"id": "%04X" % idv, "ok": ok, "read50": obs["reads50"][:1], "entered": first and first["handler"],
            "ecx": first and "%X" % first["ecx"], "edx": first and "%X" % first["edx"]}


def pred(o, kind):
    idv, c = int(o["id"], 16), int(o["id"], 16) >> 12
    if not (o["ok"] and o["entered"] and o["read50"]):
        return False
    if kind == "VALID":
        return o["read50"] == ["%08X" % (REG + c * 0x58 + 0x50)] and o["entered"] == "%08X" % real50[c] and o["ecx"] == "%X" % idv and o["edx"] == "0"
    if kind == "WRONG_BASE":
        return o["read50"] == ["%08X" % (DECOY + c * 0x58 + 0x50)]
    if kind == "SWAPPED":
        return o["ecx"] == "0" and o["edx"] == "%X" % idv


def verdicts(tag):
    rows = [observe(i) for i in IDS]
    return {"observations": rows, "VALID": all(pred(o, "VALID") for o in rows),
            "WRONG_BASE": all(pred(o, "WRONG_BASE") for o in rows), "SWAPPED": all(pred(o, "SWAPPED") for o in rows)}


res["B_shipped"] = verdicts("shipped")

# ---- C: mutants of the private image ----
def mutate(at, new, tag):
    old = bytes(uc.mem_read(at, len(new)))
    uc.mem_write(at, new)
    uc.ctl_flush_tb()
    v = verdicts(tag)
    uc.mem_write(at, old)
    uc.ctl_flush_tb()
    v["patch"] = {"at": "%08X" % at, "old": old.hex(), "new": new.hex()}
    return v


res["C_M_BASE"] = mutate(0x309EF7, struct.pack("<i", DECOY - lea_next), "M_BASE")
res["C_M_SWAP"] = mutate(0x309F1A, bytes.fromhex("410fb7d031c9"), "M_SWAP")     # movzx edx, r8w / xor ecx, ecx
res["C_restored"] = bytes(uc.mem_read(DISP, len(EXPECT))) == EXPECT
res["B_after_restore"] = verdicts("after")
uc.mem_write(DECOY, decoy_orig)
res["decoy_restored"] = bytes(uc.mem_read(DECOY, 15 * 0x58)) == decoy_orig

# ---- D: text regression over the current consumers ----
CONSUMERS = ["00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md", "00-Engine-Core-Runtime/the-encoded-id-class-registry.md",
             "00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md",
             "00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md"]
STRUCK = re.compile(r"~~.*?~~", re.S)
BAD_BASE = re.compile(r"01EC81F0", re.I)
BAD_ORDER = re.compile(r"\(\s*0\s*,\s*(?:cx|ecx|id|the id)\s*\)|\(\s*edx\s*=\s*0\s*,\s*ecx\s*=\s*0\s*\)", re.I)


def violations(text):
    out = []
    for para in re.split(r"\n\s*\n", STRUCK.sub("", text)):
        if "00309EC0" not in para and "00309F20" not in para:
            continue
        if BAD_BASE.search(para):
            out.append(("WRONG_BASE", para[:160]))
        if BAD_ORDER.search(para) and re.search(r"jmp|dispatch|tail", para, re.I):
            out.append(("SWAPPED", para[:160]))
    return out


PRE = ("`00309EC0` (102 B) is the encoded-id class dispatcher: `cx == 0xFFFF` returns `-1`, `(cx & 0xF000) > 0xE000` returns `-1`; the top "
       "nibble selects `01EEBCC0 + class*0x58`, `cx & 0xFFF` bounds-checks against `dword[+0x3C]-1`, and `qword[+0x50]` non-null "
       "tail-dispatches `jmp rax` with `(0, cx)` - the class registry's second-level resolve.")
PRE_69E = ("the class nibble `cx >> 12` selects a\n0x58-stride row in the `01EC81F0` table, `cx & 0xFFF` is bounds-checked against\n`[row+0x3C]`, and on "
           "success `jmp qword[row+0x50]`\n([`00309F20`](../_index/ADDRESS-INDEX.md)) tail-dispatches")
res["D"] = {"selftest_pre_repair_contract_rejected": [v[0] for v in violations(PRE)] == ["SWAPPED"],
            "selftest_69e9cad19_token_rejected": [v[0] for v in violations(PRE_69E)] == ["WRONG_BASE"],
            "consumers": {}}
for rel in CONSUMERS:
    res["D"]["consumers"][rel] = violations(open(os.path.join(ROOT, rel), encoding="utf-8").read())
D_ok = res["D"]["selftest_pre_repair_contract_rejected"] and res["D"]["selftest_69e9cad19_token_rejected"] and not any(res["D"]["consumers"].values())

sh, mb, ms = res["B_shipped"], res["C_M_BASE"], res["C_M_SWAP"]
cases = {
    "A_image_identity_body_bytes_and_operands": A_ok,
    "B_shipped_passes_VALID": sh["VALID"],
    "B_shipped_fails_WRONG_BASE_and_SWAPPED": not sh["WRONG_BASE"] and not sh["SWAPPED"],
    "C_M_BASE_fails_VALID_passes_only_WRONG_BASE": not mb["VALID"] and mb["WRONG_BASE"] and not mb["SWAPPED"],
    "C_M_SWAP_fails_VALID_passes_only_SWAPPED": not ms["VALID"] and ms["SWAPPED"] and not ms["WRONG_BASE"],
    "C_image_restored_and_VALID_again": res["C_restored"] and res["B_after_restore"]["VALID"],
    "D_text_regression_selftests_and_current_consumers_clean": D_ok,
}
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("A:", json.dumps({k: res["A"][k] for k in ("lea_target", "classid_lea_target", "tail")}))
print("shipped:", json.dumps(sh["observations"][:2]))
print("D consumers:", json.dumps({k: len(v) for k, v in res["D"]["consumers"].items()}))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
