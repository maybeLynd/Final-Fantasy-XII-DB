"""fw1_tunable_consumers.py - FW-1: the consumers of the battle unit's cached FCP tunables +0x164 .. +0x1F5
(FABLE, Claude Opus 5.5, 2026-09-26; found by a delegated read-only pass with an interprocedural tracker, whose
sensitivity control found all six published +0x16C readers; each site re-checked here).

  C1 the route the access census never followed: the solver-context builder 00336710 stores its source argument, the
     unit + 0x80, at ctx +0x108 and +0x100 (003367B4, 003367BB). A solver reads a tunable at unit offset U as
     [ [ctx+0x108] + (U - 0x80) ].
  C2 one consumer per tunable. For each site: the instruction reads the expected field, and the base register's last
     write before it in the same function is a load from [x + 0x108] (the ctx pointer). The exceptions are the two
     unit-direct readers, 00233A20 and 0023A006.
       +0x164 at st +0xE4, 0033CE1B  fast-moving turn step (taken when ctx +0xB0 is above +0x184, 0033CE0A)
       +0x168 at st +0xE8, 0033CE2C  the turn step otherwise
       +0x178 at st +0xF8, 00339C76  minimum step length (the step-distance function returns it outright)
       +0x180 unit-direct, 00233A32  the getter 00233A20 returns it scaled by 1.0, 1.5 or 1.2, and its one caller
                                     stores that at +0x17C, the maximum step length (002363FA, 002363FF)
       +0x184 at st +0x104, 0033CE0A the step-length threshold between the two turn steps
       +0x198 at st +0x118, 0033D0A7 the bound on the limited heading's distance from the desired heading
       +0x1AC at st +0x12C, 00334680 the avoidance sweep angle
       +0x1B0 at st +0x130, 0033444F the avoidance chance divisor (-1 disables it)
       +0x1F5 at st +0x175, 00339E0B profile index into the table 01EED4C0
     (+0x16C and +0x170 already have published readers: 00336595, 0033658B.)
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
funcs = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
starts = sorted(funcs)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def body(a):
    s = starts[bisect.bisect_right(starts, a) - 1]
    return list(cs.disasm(d[off(s):off(s) + funcs[s]], s))
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
FAM = {"rax": "eax", "rbx": "ebx", "rcx": "ecx", "rdx": "edx", "rsi": "esi", "rdi": "edi", "r8": "r8d", "r9": "r9d",
       "r10": "r10d", "r11": "r11d", "r12": "r12d", "r13": "r13d", "r14": "r14d", "r15": "r15d"}
def last_write(site, reg):
    """the last instruction before `site` in its function (address order) whose explicit destination is `reg`."""
    L = body(site); w = None
    for x in L:
        if x.address >= site: break
        dst = x.op_str.split(",")[0].strip()
        if x.mnemonic in ("mov", "lea", "movzx", "movsxd", "pop", "xor") and dst in (reg, FAM.get(reg)): w = x
    return w
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("C1 00336710 stores unit+0x80 at ctx +0x108 and +0x100",
      at(0x3367B4) == "mov qword ptr [rcx + 0x108], rdx" and at(0x3367BB) == "mov qword ptr [rcx + 0x100], rdx")
SITES = [("+0x164", 0x33CE1B, "movss xmm2, dword ptr [rdx + 0xe4]", "rdx", True),
         ("+0x168", 0x33CE2C, "movss xmm2, dword ptr [rdx + 0xe8]", "rdx", True),
         ("+0x178", 0x339C76, "movss xmm0, dword ptr [rdx + 0xf8]", "rdx", True),
         ("+0x180", 0x233A32, "movss xmm0, dword ptr [rbx + 0x180]", "rbx", False),
         ("+0x184", 0x33CE0A, "comiss xmm2, dword ptr [rdx + 0x104]", "rdx", True),
         ("+0x184", 0x23A006, "movss xmm1, dword ptr [rdi + 0x184]", "rdi", False),
         ("+0x198", 0x33D0A7, "movss xmm5, dword ptr [rdi + 0x118]", "rdi", True),
         ("+0x1AC", 0x334680, "movss xmm0, dword ptr [rax + 0x12c]", "rax", True),
         ("+0x1B0", 0x33444F, "cmp dword ptr [rax + 0x130], -1", "rax", True),
         ("+0x1F5", 0x339E0B, "movzx eax, byte ptr [r9 + 0x175]", "r9", True)]
bad = []
for field, site, want, reg, via in SITES:
    got = at(site); w = last_write(site, reg)
    wtxt = "%s %s" % (w.mnemonic, w.op_str) if w else None
    ok = got == want and (not via or (wtxt is not None and re.search(r"qword ptr \[\w+ \+ 0x108\]$", wtxt) is not None))
    print("   %-7s %08X %-40s base <- %s" % (field, site, got, wtxt))
    if not ok: bad.append("%s@%08X" % (field, site))
check("C2 each tunable has a consumer, and the ctx-routed ones load their base from [x + 0x108]", not bad, str(bad))
G = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body(0x233A20)}
check("C2 00233A20 returns +0x180 scaled by 1.0, 1.5 or 1.2; its caller stores the result at +0x17C (002363FF)",
      G.get(0x233A72) == "mulss xmm0, dword ptr [rbx + 0x180]" and G.get(0x233A88) == "mulss xmm0, dword ptr [rbx + 0x180]"
      and at(0x2363FA) == "call 0x233a20" and at(0x2363FF) == "movss dword ptr [rbx + 0x17c], xmm0")
print("FAILS", fails)
sys.exit(1 if fails else 0)
