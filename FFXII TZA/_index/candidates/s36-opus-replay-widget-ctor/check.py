"""S-36: execute the widget constructor 002465F0 as shipped code (OPUS, 2026-09-25, block 298).

No record executes CONTRACT-widget-object.md's subject: EXP-069 / EXP-068 stub the factory 00244F50, and the
spawn-widget-* evidence is static. This narrow harness maps the whole SHA-asserted image and runs 002465F0 with:
  real:     002465F0, the default handler 005C5230, 001EDDA0, 00314960, the CRT cookie check 00808C40
  bridged:  00861EC0 = jmp [008C2A60] = VCRUNTIME140!memset (import) - memset(rcx, dl, r8), returns rcx
  planted:  a recording handler (the CALLER's handler argument - an input by the contract's own interface), which logs
            (rcx, the 24-byte message at [rdx]) and a call count, returns 0
Any other function entry fails the case. Signature read from the body: 002465F0(rcx = self, edx = size,
r8 = handler (NULL -> 005C5230), r9 = locals record (payload source), stack arg 5 = flag (bit 0 -> +0x40 bit 14)).
Evidence class: NATIVE-REPLAY (unicorn), live_game false. Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RAX,
                               UC_X86_REG_RIP, UC_X86_REG_RBX, UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
IMG = 0x120000
CTOR, DEFAULT, MEMSET = 0x2465F0, 0x5C5230, 0x861EC0
REAL = {CTOR, DEFAULT, 0x1EDDA0, 0x314960, 0x808C40}
STACK, STACK_SZ, RET = 0x70000000, 0x100000, 0x71000000
SELF, LOCALS, FIX, LOG = 0x72000000, 0x72100000, 0x73000000, 0x73100000

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")

# recording handler: log[0]=rcx, log[8..0x20)=message qwords, dword log[0x20]+=1; xor eax,eax; ret
HANDLER = (b"\x48\xB8" + struct.pack("<Q", LOG) + bytes.fromhex(
    "488908" "4c8b02" "4c894008" "4c8b4208" "4c894010" "4c8b4210" "4c894018" "ff4020" "31c0" "c3"))


def run(size, handler, locals_ab, flag, prefill=0xCC):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for v, vs, ra, rs in secs:
        lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
        uc.mem_map(lo, hi - lo)
        uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
    for base, sz in ((STACK, STACK_SZ), (RET, 0x1000), (SELF, 0x10000), (LOCALS, 0x1000), (FIX, 0x1000), (LOG, 0x1000)):
        uc.mem_map(base, sz)
    uc.mem_write(RET, b"\xF4")
    uc.mem_write(FIX, HANDLER)
    uc.mem_write(SELF, bytes([prefill]) * 0x400)
    if locals_ab is not None:
        uc.mem_write(LOCALS + 8, struct.pack("<QQ", *locals_ab))
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.mem_write(sp + 0x28, struct.pack("<Q", flag))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for r, v in ((UC_X86_REG_RCX, SELF), (UC_X86_REG_RDX, size), (UC_X86_REG_R8, FIX if handler else 0),
                 (UC_X86_REG_R9, LOCALS if locals_ab is not None else 0),
                 (UC_X86_REG_RBX, 0x1111), (UC_X86_REG_RSI, 0x2222), (UC_X86_REG_RDI, 0x3333), (UC_X86_REG_RBP, 0x4444)):
        uc.reg_write(r, v)
    L = {"entered": [], "outside_fail": [], "writes": set(), "memset": [], "faults": [], "default_ran": False}

    def on_code(u, a, n, _):
        if a == MEMSET:
            dst = u.reg_read(UC_X86_REG_RCX)
            val = u.reg_read(UC_X86_REG_RDX) & 0xFF
            cnt = u.reg_read(UC_X86_REG_R8)
            u.mem_write(dst, bytes([val]) * cnt)
            L["memset"].append(["%08X" % dst, val, cnt])
            u.reg_write(UC_X86_REG_RAX, dst)
            rsp = u.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", bytes(u.mem_read(rsp, 8)))[0]
            u.reg_write(UC_X86_REG_RSP, rsp + 8)
            u.reg_write(UC_X86_REG_RIP, ret)
            return
        if a == DEFAULT:
            L["default_ran"] = True
        if a in FSTARTS:
            L["entered"].append("%08X" % a)
            if a not in REAL:
                L["outside_fail"].append("%08X" % a)
                u.emu_stop()

    def on_w(u, ac, a, n, v, _):
        if SELF <= a < SELF + 0x10000:
            for i in range(n):
                L["writes"].add(a - SELF + i)

    def on_bad(u, ac, a, n, v, _):
        L["faults"].append([ac, "%08X" % a])
        return False

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    try:
        uc.emu_start(CTOR, RET, count=100000)
    except UcError as e:
        L["faults"].append(["uc", str(e)])
    L["returned"] = uc.reg_read(UC_X86_REG_RIP) == RET
    L["nonvol"] = [uc.reg_read(r) for r in (UC_X86_REG_RBX, UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_RBP)] == [0x1111, 0x2222, 0x3333, 0x4444]
    L["self"] = bytes(uc.mem_read(SELF, 0x100))
    L["log"] = bytes(uc.mem_read(LOG, 0x28))
    return L


def q(b, o):
    return struct.unpack_from("<Q", b, o)[0]


def d(b, o):
    return struct.unpack_from("<I", b, o)[0]


results, allok = {}, True


def rec(name, ok, L, extra):
    global allok
    allok &= ok
    r = {"pass": ok, "returned": L["returned"], "nonvol": L["nonvol"], "faults": L["faults"], "entered": sorted(set(L["entered"])),
         "memset": L["memset"], "default_ran": L["default_ran"], "self_0x100": L["self"].hex(), "log": L["log"].hex()}
    r.update(extra)
    results[name] = r
    print("%-34s %s" % (name, "PASS" if ok else "FAIL"))


clean = lambda L: L["returned"] and L["nonvol"] and not L["faults"] and not L["outside_fail"]


def header_ok(s):
    return (d(s, 0xB8) == 0x3F800000 and struct.unpack_from("<H", s, 0x44)[0] == 100 and s[0xA0] == 0x80
            and d(s, 0x9C) == 0x800080 and d(s, 0x98) == 0 and q(s, 0x48) == 0x915198
            and struct.unpack_from("<H", s, 0xA1)[0] == 0xFF80)


# 1. null handler, null locals: self[0] = default 005C5230, header invariants, default handler actually runs
L = run(0xD8, False, None, 0)
s = L["self"]
unwritten_nonzero = [o for o in range(0xD8) if o not in L["writes"] and s[o] != 0] if L["self"] else []
rec("null-handler-default", clean(L) and q(s, 0) == DEFAULT and header_ok(s) and L["default_ran"]
    and L["memset"] == [["%08X" % SELF, 0, 0xD8]] and not unwritten_nonzero,
    L, {"self0": "%08X" % q(s, 0), "unwritten_nonzero": unwritten_nonzero})

# 2. planted handler, payload a/b: called once with {1, a, b}, rcx = self
A, B = 0x1111222233334444, 0x5555666677778888
L = run(0xD8, True, (A, B), 0)
s, lg = L["self"], L["log"]
rec("handler-message-1-payload", clean(L) and q(s, 0) == FIX and header_ok(s) and q(lg, 0) == SELF
    and d(lg, 8) == 1 and q(lg, 0x10) == A and q(lg, 0x18) == B and d(lg, 0x20) == 1 and not L["default_ran"],
    L, {"msg_id": d(lg, 8), "a": "%016X" % q(lg, 0x10), "b": "%016X" % q(lg, 0x18), "calls": d(lg, 0x20)})

# 3. planted handler, NULL locals: message {1, 0, 0}
L = run(0xD8, True, None, 0)
lg = L["log"]
rec("handler-null-locals-zero-payload", clean(L) and d(lg, 8) == 1 and q(lg, 0x10) == 0 and q(lg, 0x18) == 0 and d(lg, 0x20) == 1,
    L, {"a": "%016X" % q(lg, 0x10), "b": "%016X" % q(lg, 0x18)})

# 4. stack flag bit 0 -> +0x40 bit 14
L1 = run(0xD8, True, None, 1)
L0 = run(0xD8, True, None, 0)
rec("flag-bit14", clean(L1) and clean(L0) and (d(L1["self"], 0x40) >> 14) & 1 == 1 and (d(L0["self"], 0x40) >> 14) & 1 == 0,
    L1, {"f40_flag1": "%08X" % d(L1["self"], 0x40), "f40_flag0": "%08X" % d(L0["self"], 0x40)})

# 5. measurement: a size below the fixed header - memset covers `size`, the constructor still writes up to +0xBB
L = run(0x40, True, None, 0)
beyond = sorted(o for o in L["writes"] if o >= 0x40)
rec("small-size-measurement", clean(L), L, {"memset": L["memset"], "writes_beyond_size": [min(beyond), max(beyond)] if beyond else []})

json.dump({"pass": sum(1 for v in results.values() if v["pass"]), "total": len(results), "ok": allok, "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
print("%d/%d pass" % (sum(1 for v in results.values() if v["pass"]), len(results)))
