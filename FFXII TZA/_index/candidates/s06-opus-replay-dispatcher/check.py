"""S-06 runtime: execute the developer tuning console dispatcher 001D1660 as shipped code, stub-free
(OPUS, 2026-09-25, block 291). Plan: candidates/s06-runtime-what-execution-would-test.md (block 252).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The whole image is mapped from the SHA-asserted EXE.
Nothing is stubbed. Every case must leave 001D1660 through its own `ret` with no function other than 001D1660
entered (any call would be recorded and fail the case).

Signature read from the prologue: 001D1660(rcx, dl, r8b, r9d = id). r9d -= 0xC; unsigned compare with 0x119; above
-> 001D4C09 (the pop-and-return tail); else jump through the dword table at 001D4C1C (image-base-relative, base
00120000). 001D4BFA is the shared epilogue (restore xmm6 / rbp / xmm7, fall into 001D4C09).

Cases:
  I-2  ids 0, 5, 11, 294, 0xFFFFFFFF: must take 001D4C09 directly (no table read), write nothing outside the stack.
  I-3  every id whose table entry IS 001D4BFA: must write nothing outside the stack.
  I-4  every id whose arm is a pure stepper - straight-line code from the table target to 'jmp 001D4BFA' containing
       an addss/subss/movss store to a rip-relative global and no call: the global must change by exactly the
       arm's own constant operand (read from the image), and nothing else outside the stack may be written.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
                               UC_X86_REG_RIP, UC_X86_REG_RBX, UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG = 0x120000
FN, TAIL, EPI, TABLE = 0x1D1660, 0x1D4C09, 0x1D4BFA, 0x1D4C1C
FN_END = 0x1D4C19
STACK, STACK_SZ = 0x70000000, 0x100000
RET = 0x71000000
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs = []
off = pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")


def img_bytes(va, n):
    for v, vs, ra, rs in secs:
        if v <= va < v + max(vs, rs):
            o = va - v
            return raw[ra + o:ra + o + n] if o < rs else b"\0" * n
    raise KeyError(hex(va))


def table_target(i):
    return IMG + struct.unpack("<I", img_bytes(TABLE + 4 * i, 4))[0]


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def arm_shape(t):
    """straight-line decode from t to the first jmp EPI; returns (store_insn, const_va, op) for a pure stepper."""
    code = img_bytes(t, 0x80)
    stores, consts, mnems = [], [], []
    for ins in md.disasm(code, t):
        mnems.append(ins.mnemonic)
        if ins.mnemonic == "jmp":
            ok = ins.operands[0].imm == EPI if ins.operands and ins.operands[0].type == 2 else False
            return (stores, consts, mnems) if ok else None
        if ins.mnemonic in ("call", "ret") or ins.mnemonic.startswith("j") or ins.mnemonic.startswith("cmov"):
            return None
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                va = ins.address + ins.size + op.mem.disp
                if ins.mnemonic in ("movss",) and ins.operands[0].type == X86_OP_MEM:
                    stores.append(va)
                elif ins.mnemonic in ("addss", "subss", "movss"):
                    consts.append((ins.mnemonic, va))
    return None


def run(idv):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for v, vs, ra, rs in secs:
        lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
        uc.mem_map(lo, hi - lo)
        uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
    uc.mem_map(STACK, STACK_SZ)
    uc.mem_map(RET, 0x1000)
    uc.mem_write(RET, b"\xF4")
    sp = STACK + STACK_SZ - 0x1000 - 8   # rsp = 8 mod 16 at entry, as after a call
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, 0x72000000), (UC_X86_REG_RDX, 0), (UC_X86_REG_R8, 0), (UC_X86_REG_R9, idv & 0xFFFFFFFF),
                 (UC_X86_REG_RBX, 0x1111), (UC_X86_REG_RSI, 0x2222), (UC_X86_REG_RDI, 0x3333), (UC_X86_REG_RBP, 0x4444)):
        uc.reg_write(r, v)
    log = dict(writes=[], entered=[], outside=[], faults=[], visited_tail=False, visited_epi=False, visited_table=False)

    def on_code(u, a, n, _):
        if a == TAIL:
            log["visited_tail"] = True
        if a == EPI:
            log["visited_epi"] = True
        if a == 0x1D1696:
            log["visited_table"] = True
        if a in FSTARTS and a != FN:
            log["entered"].append("%08X" % a)
        if not (FN <= a < FN_END) and a != RET:
            log["outside"].append("%08X" % a)
            u.emu_stop()

    def on_w(u, ac, a, n, v, _):
        if not (STACK <= a < STACK + STACK_SZ):
            log["writes"].append(["%08X" % a, n, v & 0xFFFFFFFFFFFFFFFF])

    def on_bad(u, ac, a, n, v, _):
        log["faults"].append([ac, "%08X" % a])
        return False

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    try:
        uc.emu_start(FN, RET, count=200000)
    except UcError as e:
        log["faults"].append(["uc", str(e)])
    log["returned"] = uc.reg_read(UC_X86_REG_RIP) == RET
    log["nonvol"] = [uc.reg_read(r) for r in (UC_X86_REG_RBX, UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP)] == [0x1111, 0x2222, 0x3333, 0x4444]
    log["mem"] = uc
    return log


results = {}
ok_all = True


def rec(name, passed, log, extra=None):
    global ok_all
    ok_all &= passed
    d = {k: v for k, v in log.items() if k != "mem"}
    if extra:
        d.update(extra)
    d["pass"] = passed
    results[name] = d
    print("%-28s %s" % (name, "PASS" if passed else "FAIL"))


base_clean = lambda L: L["returned"] and L["nonvol"] and not L["faults"] and not L["entered"] and not L["outside"]

# I-2: out-of-range ids take the tail directly, no table read, no write
for idv in (0, 5, 11, 294, 0xFFFFFFFF):
    L = run(idv)
    rec("i2-id-%X" % idv, base_clean(L) and L["visited_tail"] and not L["visited_table"] and not L["writes"], L)

# I-3 / I-4: classify every in-range id by its table target
epi_ids, steppers = [], []
for i in range(0x11A):
    t = table_target(i)
    if t == EPI:
        epi_ids.append(i + 0xC)
    else:
        s = arm_shape(t)
        if s and len(s[0]) == 1 and len(s[1]) >= 1 and set(s[2]) <= {"movss", "addss", "subss", "jmp"}:
            steppers.append((i + 0xC, t, s))
for idv in epi_ids:
    L = run(idv)
    rec("i3-epi-id-%d" % idv, base_clean(L) and L["visited_table"] and L["visited_epi"] and not L["writes"], L)


# I-4 survey (measurement, not pass/fail): every non-epilogue id, once with dl=1 (up) and once with r8b=1 (down),
# over a zeroed 0x10000-byte context at CTX. Records: clean return, functions entered, and every non-stack write with
# its before / after value (floats decoded for 4-byte writes).
CTX = 0x72000000


def run2(idv, dl, r8):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for v, vs, ra, rs in secs:
        lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
        uc.mem_map(lo, hi - lo)
        uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
    uc.mem_map(STACK, STACK_SZ)
    uc.mem_map(RET, 0x1000)
    uc.mem_map(CTX, 0x10000)
    uc.mem_write(RET, b"\xF4")
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, CTX), (UC_X86_REG_RDX, dl), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, idv),
                 (UC_X86_REG_RBX, 0x1111), (UC_X86_REG_RSI, 0x2222), (UC_X86_REG_RDI, 0x3333), (UC_X86_REG_RBP, 0x4444)):
        uc.reg_write(r, v)
    L = dict(writes=[], entered=[], faults=[])

    def on_code(u, a, n, _):
        if a in FSTARTS and a != FN:
            L["entered"].append("%08X" % a)
            u.emu_stop()

    def on_w(u, ac, a, n, v, _):
        if not (STACK <= a < STACK + STACK_SZ):
            before = bytes(u.mem_read(a, n))
            L["writes"].append([a, n, before, v & ((1 << (8 * n)) - 1)])

    def on_bad(u, ac, a, n, v, _):
        L["faults"].append([ac, "%08X" % a])
        return False

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    try:
        uc.emu_start(FN, RET, count=200000)
    except UcError as e:
        L["faults"].append(["uc", str(e)])
    L["returned"] = uc.reg_read(UC_X86_REG_RIP) == RET and not L["entered"]
    out = []
    for a, n, b, v in L["writes"]:
        e = {"va": "%08X" % a, "n": n, "before": b.hex(), "after": v.to_bytes(n, "little").hex()}
        if n == 4:
            e["f_before"] = struct.unpack("<f", b)[0]
            e["f_after"] = struct.unpack("<f", v.to_bytes(4, "little"))[0]
            e["delta"] = e["f_after"] - e["f_before"]
        out.append(e)
    L["writes"] = out
    return L


survey = {}
for i in range(0x11A):
    if table_target(i) == EPI:
        continue
    idv = i + 0xC
    survey[idv] = {"target": "%08X" % table_target(i), "up": run2(idv, 1, 0), "down": run2(idv, 0, 1)}
clean = [k for k, v in survey.items() if v["up"]["returned"] and v["down"]["returned"]]
calls = [k for k, v in survey.items() if v["up"]["entered"] or v["down"]["entered"]]
deltas = {}
for k in clean:
    for d in ("up", "down"):
        for w in survey[k][d]["writes"]:
            if "delta" in w and w["delta"] == w["delta"] and abs(w["delta"]) < 1e6 and w["delta"] != 0:
                key = round(abs(w["delta"]), 6)
                deltas[key] = deltas.get(key, 0) + 1
print("survey: %d non-epilogue ids; %d return clean with no call both ways; %d enter a function" % (len(survey), len(clean), len(calls)))
print("float step magnitudes among clean ids:", sorted(deltas.items(), key=lambda x: -x[1])[:8])
results["_survey"] = {"pass": True, "note": "measurement", "clean_ids": clean, "call_ids": calls,
                      "float_step_counts": {str(k): v for k, v in deltas.items()}, "per_id": {str(k): v for k, v in survey.items()}}

for idv, t, (stores, consts, mnems) in steppers:
    gva = stores[0]
    before = struct.unpack("<f", img_bytes(gva, 4))[0]
    step_ops = [(m, struct.unpack("<f", img_bytes(va, 4))[0], "%08X" % va) for m, va in consts if va != gva]
    L = run(idv)
    after = struct.unpack("<f", bytes(L["mem"].mem_read(gva, 4)))[0]
    only_global = all(w[0] == "%08X" % gva for w in L["writes"])
    expect = before
    for m, c, _ in step_ops:
        expect = (expect + c) if m == "addss" else (expect - c) if m == "subss" else expect
    exp32 = struct.unpack("<f", struct.pack("<f", expect))[0]
    rec("i4-step-id-%d" % idv, base_clean(L) and only_global and after == exp32, L,
        dict(target="%08X" % t, global_va="%08X" % gva, before=before, after=after, expected=exp32, ops=step_ops, mnems=mnems))

summary = {"pass": sum(1 for v in results.values() if v["pass"]), "total": len(results), "ok": ok_all,
           "epi_ids": epi_ids, "stepper_ids": [s[0] for s in steppers], "results": results}
json.dump(summary, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("%d/%d pass" % (summary["pass"], summary["total"]))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
