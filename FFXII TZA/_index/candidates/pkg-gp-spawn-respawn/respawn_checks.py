"""respawn_checks.py - PKG-GP-SPAWN-RESPAWN: the bytes behind its first corrections (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  N  NATIVE CODE DOES READ THE RESPAWN FIELDS: the automatic spawn selector 00235720 reads the keep entry's death limit +0x0A
     (002358A1) against the death count +0x08 (002358AB, jae = died out), then - for an entry that is committed and not range
     re-entry pending - the cooldown +0x10 (002358C1) and the death stamp +0x0C: seconds - stamp (002358D1) compared with the
     cooldown, skipping while below (jb 002359C4). So re-entry is allowed at elapsed >= cooldown; the scripts' own checks are
     btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i). Rejected: "no native code reads the death count, the death stamp or
     the cooldown" (the three ACCESSORS 00235F50 / 00235FB0 / 002366E0 are script-only; the selector reads the fields directly)
  W  THE COOLDOWN IS WRITTEN: the entry initialiser 002395A0 stores +0x10 = row word +2 + rand % (row word +4 + 1), or 0 when the
     base is 0 (00239628..00239652), and zeroes the stamp +0x0C (00239657). Rejected: "+0x10 is still not seen written"
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(a) + (b - a)], a)}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
sel = dis(0x2358A1, 0x2358DD)
N = {0x2358A1: "movzx eax, word ptr [r14 + 0xa]", 0x2358AB: "cmp word ptr [r14 + 8], ax", 0x2358B0: "jae 0x2359c4",
     0x2358C1: "movzx eax, word ptr [r14 + 0x10]", 0x2358D1: "sub ecx, dword ptr [r14 + 0xc]", 0x2358D5: "cmp ecx, eax",
     0x2358D7: "jb 0x2359c4"}
def allowed(seconds, stamp, cooldown): return not (cooldown and (seconds - stamp) < cooldown)   # the selector's gate
check("N", at(sel, N) and allowed(110, 100, 10) and not allowed(109, 100, 10) and allowed(5, 0, 0),
      "00235720 reads +0x0A/+0x08/+0x10/+0x0C directly; re-entry at elapsed >= cooldown (10 s cooldown: t+10 allowed, t+9 not)")
w = dis(0x239628, 0x23965E)
W = {0x239628: "movzx r14d, word ptr [rbx + 4]", 0x23962D: "inc r14d", 0x239637: "call 0x328370", 0x239644: "idiv r14d",
     0x239647: "movzx eax, word ptr [rbx + 2]", 0x23964B: "add eax, edx", 0x239652: "mov word ptr [rdi + rcx + 0x10], ax",
     0x239657: "mov dword ptr [rdi + rcx + 0xc], r15d"}
check("W", at(w, W), "002395A0 writes +0x10 = base + rand %% (range + 1) and zeroes +0x0C: %s" % at(w, W))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
