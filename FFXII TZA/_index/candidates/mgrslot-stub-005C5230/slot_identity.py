"""slot_identity.py - control for the manager-slot owed item 3 (FABLE, Claude Opus 5.5, 2026-09-26): side B is always
handed exactly the slot 002640C0 returns, the slot side A's reset obtains itself.

S1 002640C0 is `mov rax, [02099D70] / ret` (the current manager slot).
S2 each side-B entry has only verb-handler callers (raw call index, checked separately: 003DD230 <- 003492F0/00349730,
   003DCF60 <- 0034B100, 003DD320 <- 00349ED0/0034A370, 003DD350 <- 0034B610), and each handler calls 002640C0 and
   hands that result to the entry as rcx.
S3 between that call and the transfer the handlers call only VMValueStack_PopInt32CoerceFloat32 (00267E10), which calls
   only 008620C0; neither is among the writers of 02099D70 (the mov-store census here finds 15 writing functions;
   ripscan's all-forms list has 16, and neither contains them), so the slot cannot change in between.
Known positive: S3's writer list must contain the actor-manager pass 0025D9E0, a known writer of 02099D70.
"""
import bisect, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))
def off(v):
    for nm, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
funcs = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
               errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
g = ins(0x2640C0, 8)
check("S1 002640C0 = mov rax,[rip->02099D70] / ret",
      g[0].mnemonic == "mov" and g[0].address + g[0].size + int(g[0].op_str.split("+ ")[1].rstrip("]"), 16) == 0x2099D70 and g[1].mnemonic == "ret")
HANDLERS = {0x3492F0: 0x3DD230, 0x349730: 0x3DD230, 0x34B100: 0x3DCF60, 0x349ED0: 0x3DD320, 0x34A370: 0x3DD320, 0x34B610: 0x3DD350}
between_calls = set()
for h, entry in HANDLERS.items():
    L = ins(h, 0x80)
    i0 = next(i for i, x in enumerate(L) if x.mnemonic == "call" and x.op_str == "0x2640c0")
    it = next(i for i, x in enumerate(L) if x.mnemonic in ("call", "jmp") and x.op_str == hex(entry))
    reg = None
    for x in L[i0 + 1:it]:
        if x.mnemonic == "mov" and x.op_str.endswith(", rax") and reg is None: reg = x.op_str.split(",")[0]
        if x.mnemonic == "call": between_calls.add(x.op_str)
    rcx_src = [x for x in L[i0 + 1:it] if x.mnemonic == "mov" and x.op_str.startswith("rcx, ")]
    ok = reg is not None and rcx_src and rcx_src[-1].op_str in ("rcx, " + reg, "rcx, rax") and (reg != "rcx" or rcx_src[-1].op_str == "rcx, rax")
    check("S2 %08X hands 002640C0()'s result (%s) to %08X as rcx" % (h, reg, entry), bool(ok))
check("S3 between the call and the transfer the handlers call only 00267E10", between_calls <= {"0x267e10"}, str(between_calls))
pop_calls = {x.op_str for x in ins(0x267E10, 0x40) if x.mnemonic == "call"}
check("S3 00267E10 calls only 008620C0", pop_calls == {"0x8620c0"}, str(pop_calls))
# writers of 02099D70: every rip-relative store to it, by containing function
writers = set()
_, vs, va, rs, ro = [s for s in secs if s[0] == ".text"][0]
cur = BASE + va; end = cur + rs
for f in funcs:
    if f < BASE + va or f >= end: continue
    for x in cs.disasm(d[off(f):off(f) + 0x3000], f):
        if x.mnemonic == "ret" and x.address > f + 0x2000: break
        m = re.match(r"qword ptr \[rip \+ (0x[0-9a-f]+)\], ", x.op_str)
        if x.mnemonic == "mov" and m and x.address + x.size + int(m.group(1), 16) == 0x2099D70:
            writers.add(funcs[bisect.bisect_right(funcs, x.address) - 1])
check("known positive: 0025D9E0 is found as a writer of 02099D70", 0x25D9E0 in writers, "(%d writers)" % len(writers))
check("S3 neither 00267E10 nor 008620C0 writes 02099D70", not ({0x267E10, 0x8620C0} & writers))
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
