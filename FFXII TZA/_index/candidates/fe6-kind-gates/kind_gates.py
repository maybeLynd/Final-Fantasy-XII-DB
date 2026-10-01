"""kind_gates.py - which stats-record word writers test the record kind (FABLE, Claude Opus 5.5, 2026-09-26).

  K1 the result applier's step 16 (003112F0) is gated: `cmp byte ptr [rdi + 5], 1` / `jne` at 0031189B skips all four
     i16 delta adds (+0x08, +0x0A, +0x12, +0x14) unless the target stats kind is 1. That is FE-6's answered first half.
  K2 the direct-state order arms do not test the kind: 0x4158 (002FE12B) and the 0x4159.. run reached through the table
     at 002FE628 each load the stats record [unit + 0x698], add a clamped signed word to one i16 field and call the
     recompute 0030FED0, with no `[reg + 5]` compare anywhere in the arm (planted positive for the matcher: K1's arm has
     one).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, bisect
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
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return ["%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(b)], a)]
KIND = re.compile(r"^cmp byte ptr \[r[a-z0-9]+ \+ 5\], ")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

A = dis(0x31189B, 0x311919)
check("K1 applier step 16: kind test first, then the four i16 adds",
      KIND.match(A[0]) is not None and A[1] == "jne 0x311919"
      and all(any(s == "add word ptr [rdi + %s], cx" % f for s in A) for f in ("8", "0xa", "0x12", "0x14")), A[0])
arms = [(0x4158, 0x2FE12B)]
for k in range(12):
    arms.append((0x4159 + k, BASE + struct.unpack_from("<I", d, off(BASE + 0x1DE628) + 4 * k)[0]))
checked = 0
for code, a in arms:
    S = []
    for x in cs.disasm(d[off(a):off(a) + 0x80], a):
        S.append("%s %s" % (x.mnemonic, x.op_str))
        if x.mnemonic == "ret": break
    if not any(s == "mov rdx, qword ptr [rbx + 0x698]" for s in S): continue      # not a stats-word arm (the table's default)
    checked += 1
    check("K2 arm %#x (%08X): stats word add + recompute, no kind test" % (code, a),
          any(re.match(r"mov word ptr \[rdx \+ (0x[0-9a-f]+|\d+)\], cx", s) for s in S) and "call 0x30fed0" in S
          and not any(KIND.match(s) for s in S))
check("K2 at least the two arms the page names were checked", checked >= 2, "%d arms" % checked)
print("FAILS", fails)
sys.exit(1 if fails else 0)
