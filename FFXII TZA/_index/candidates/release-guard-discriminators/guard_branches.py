"""guard_branches.py - which ecx values take each release guard's deeper call (FABLE, Claude Opus 5.5, 2026-09-28).

Executes ONLY the guard thunks' original bytes from the shipping image under unicorn, one ecx value at a time, and records
whether control returns or leaves for the deeper release. The deeper releases (003DC780, 0042FCC0) are NOT executed: a
hook stops the run at their entry. This is an original-code execution of the guards' branch, not of any release.

  G1  00325A00: the deeper call 003DC780 is taken for every tested ecx except 0, 0x80000000 and 0x80000001;
      ecx == 1 takes it (the cmp ecx,1 arm), and the row reset's sentinel 0x80000000 skips it
  G2  00317EC0: 0042FCC0 is taken for every tested ecx except 0 and 0xFFFFFFFF (-1)
  C   control: the harness distinguishes the outcomes - a planted 'ret' stub reports RETURN, a planted 'jmp' reports
      the target, and an out-of-guard fetch would stop as ERROR
Reads the shipping image (FFXII_EXE).
"""
import os, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RSP, UC_X86_REG_RIP
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, vs, ra, rs)); o += 40
def image_bytes(va, n):
    r = va - 0x120000
    for sva, vs, ra, rs in secs:
        if sva <= r < sva + rs: return d[ra + r - sva: ra + r - sva + n]
    raise ValueError(hex(va))
RET_SENTINEL = 0x0DEAD000
def run(code_va, code, ecx, stops):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    base = code_va & ~0xFFF
    mu.mem_map(base, 0x2000); mu.mem_write(code_va, code)
    mu.mem_map(0x7F0000, 0x10000); mu.mem_map(RET_SENTINEL & ~0xFFF, 0x1000)
    sp = 0x7F8000; mu.mem_write(sp, struct.pack("<Q", RET_SENTINEL))
    mu.reg_write(UC_X86_REG_RSP, sp); mu.reg_write(UC_X86_REG_RCX, ecx)
    outcome = {}
    def hook(uc, addr, size, _):
        if addr == RET_SENTINEL: outcome["r"] = "RETURN"; uc.emu_stop()
        elif addr in stops: outcome["r"] = "DEEPER %08X" % addr; uc.emu_stop()
        elif not (code_va <= addr < code_va + len(code)): outcome["r"] = "ERROR %08X" % addr; uc.emu_stop()
    mu.hook_add(UC_HOOK_CODE, hook)
    for t in stops: mu.mem_map(t & ~0xFFF, 0x1000) if not (base <= t < base + 0x2000) else None
    try: mu.emu_start(code_va, 0, count=64)
    except Exception as e: outcome.setdefault("r", "ERROR " + str(e)[:40])
    return outcome.get("r", "ERROR no stop")
VALS = [0, 1, 2, 3, 0x7FFFFFFE, 0x7FFFFFFF, 0x80000000, 0x80000001, 0x80000002, 0xFFFFFFFE, 0xFFFFFFFF]
g1 = {v: run(0x00325A00, image_bytes(0x00325A00, 19), v, {0x003DC780}) for v in VALS}
skip1 = sorted(v for v, r in g1.items() if r == "RETURN")
ok("G1", skip1 == [0, 0x80000000, 0x80000001] and all(r == "DEEPER 003DC780" for v, r in g1.items() if v not in skip1),
   "00325A00 returns for %s; every other tested value leaves for 003DC780 (1 -> %s)" % ([hex(v) for v in skip1], g1[1]))
g2 = {v: run(0x00317EC0, image_bytes(0x00317EC0, 13), v, {0x0042FCC0}) for v in VALS}
skip2 = sorted(v for v, r in g2.items() if r == "RETURN")
ok("G2", skip2 == [0, 0xFFFFFFFF] and all(r == "DEEPER 0042FCC0" for v, r in g2.items() if v not in skip2),
   "00317EC0 returns for %s; every other tested value leaves for 0042FCC0" % [hex(v) for v in skip2])
c_ret = run(0x00400000, b"\xc3", 5, {0x00400100})
c_jmp = run(0x00400000, b"\xe9\xfb\x00\x00\x00", 5, {0x00400100})
c_err = run(0x00400000, b"\xe9\xfb\x01\x00\x00", 5, {0x00400100})
ok("C", c_ret == "RETURN" and c_jmp == "DEEPER 00400100" and c_err.startswith("ERROR"), "control: ret -> %s, jmp -> %s, stray -> %s" % (c_ret, c_jmp, c_err))
for v in VALS: print("  ecx %08X: 00325A00 %-16s 00317EC0 %s" % (v, g1[v], g2[v]))
print("FAILS", fails); sys.exit(1 if fails else 0)
