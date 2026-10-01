"""nav_mask_reset.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Independent derivation for
ASTRA-REQ-OPUS-NAV-MASK-RESET (_experiments/evidence/nav-mask-query-reset-boundary/), written without ASTRA's code, and the
correction of two OPUS claims.

  E  BMASK 003912E0 clears the working mask on EVERY entry, before any branch or other call: 003912F9 movsxd r8, [02AEE0B8]
     (cellBitsetBytes, NavGridParams +0x58), 00391302 mov rcx, [02AEE0B0] (workingCandidateMask, +0x50), 00391309 xor edx, edx,
     0039130E call 00861EC0 = VCRUNTIME140 memset. The instructions from the entry to that call are moves and the prologue only
  O  it then ORs into the same mask through the global cell - 003913B1 mov rdx, [02AEE0B0] / 003913C4 or [rdx + rax - 1], cl -
     and returns that pointer (003913E8 mov rax, [02AEE0B0]). The incoming ecx / edx / r8d / r9d are saved to esi / ebx / edi /
     ebp before the clear, and rcx is overwritten by the global: no destination argument
  M  mutant controls on copies of the image: the clear's `mov rcx, [..]` retargeted to rdx, and the memset call replaced by five
     NOPs, both make E fail
  So the mask is reset per query as well as by the builder's allocation memset (0039267E), and it is the pointer cell at
  NavGridParams +0x50, not a caller-supplied mask. Valid storage, the length and a conforming CRT memset are preconditions;
  concurrency, reentrancy and lifetime are not observed.
  S  REGRESSION: NavGridParams +0x50 no longer says 'zeroed once ... rather than per query', and the corridor contract no longer
     says 'a caller-supplied record mask' (FAILS before)
Usage: python nav_mask_reset.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(buf, a, stop):
    out = []
    for x in cs.disasm(buf[off(a):off(a) + 0x100], a):
        m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
        out.append((x.address, x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None))
        if x.address >= stop: break
    return out
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def E(buf):
    s = ins(buf, 0x3912E0, 0x39130E); by = {a: (m, o, t) for a, m, o, t in s}
    pre = [(m, o) for a, m, o, t in s if a < 0x39130E]
    return (by.get(0x3912F9, ("",))[0] == "movsxd" and by[0x3912F9][1].startswith("r8, dword ptr") and by[0x3912F9][2] == 0x2AEE0B8
            and by.get(0x391302, ("",))[0] == "mov" and by[0x391302][1].startswith("rcx, qword ptr") and by[0x391302][2] == 0x2AEE0B0
            and by.get(0x391309, ("", ""))[:2] == ("xor", "edx, edx") and by.get(0x39130E, ("", ""))[:2] == ("call", "0x861ec0")
            and all(m in ("mov", "push", "sub", "movsxd", "xor") for m, o in pre))
check("E", E(d), "003912E0 clears [02AEE0B0] for [02AEE0B8] bytes through memset before any branch or other call")
mem = ins(d, 0x861EC0, 0x861EC0)[0]
o1 = ins(d, 0x3913B1, 0x3913B1)[0]; o2 = ins(d, 0x3913C4, 0x3913C4)[0]; o3 = ins(d, 0x3913E8, 0x3913E8)[0]
pro = ins(d, 0x3912F4, 0x39130B)
check("O", mem[1] == "jmp" and mem[3] == 0x8C2A60 and o1[1:] == ("mov", "rdx, qword ptr [rip + 0x275ccf8]", 0x2AEE0B0)
      and o2[1:3] == ("or", "byte ptr [rdx + rax - 1], cl") and o3[1] == "mov" and o3[2].startswith("rax, qword ptr") and o3[3] == 0x2AEE0B0
      and [(m, o) for a, m, o, t in pro if a in (0x3912F4, 0x3912F7, 0x391300, 0x39130B)] == [("mov", "edi, r8d"), ("mov", "ebx, edx"), ("mov", "esi, ecx"), ("mov", "ebp, r9d")],
      "ORs through [02AEE0B0] and returns it; the four register arguments are saved elsewhere - no destination argument")
m1 = bytearray(d); i = off(0x391302); assert bytes(m1[i:i + 3]) == b"\x48\x8b\x0d"; m1[i + 2] = 0x15          # mov rcx,[rip+x] -> mov rdx,[rip+x]
m2 = bytearray(d); j = off(0x39130E); assert m2[j] == 0xE8; m2[j:j + 5] = b"\x90" * 5                      # drop the clear call
check("M", not E(bytes(m1)) and not E(bytes(m2)), "mutants rejected: clear register rcx -> rdx; memset call NOPed")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/nav-mask-reset-opus/nav_mask_reset.py"
CON = os.path.join(DB, "06-Movement-And-Navigation", "CONTRACT-corridor-query-family.md")
OLD_F = "INTERIOR storage, and zeroed once at 0039267E rather than per query - which a reconstruction must not assume away, since the query ORs into it."
NEW_F = ("INTERIOR storage, and ~~zeroed once at 0039267E rather than per query - which a reconstruction must not assume away, since "
         "the query ORs into it~~ cleared twice over: by the builder's allocation memset (0039267E) and again at EVERY entry of the "
         "query BMASK 003912E0, whose memset of cellBitsetBytes bytes (003912F9..0039130E) precedes every branch and loop before it "
         "ORs into the mask (Corrected 2026-09-28, OPUS, %s E O M; ASTRA nav-mask-query-reset-boundary). Valid storage, the length "
         "and a conforming CRT memset are preconditions; concurrency, reentrancy and lifetime are not observed." % REC)
OLD_C = "`BMASK` memsets and ORs a caller-supplied record mask"
NEW_C = ("`BMASK` memsets and ORs ~~a caller-supplied record mask~~ the mask behind the global pointer cell NavGridParams +0x50 "
         "(`[02AEE0B0]`): no destination argument, cleared on every entry (`003912F9`..`0039130E`), ORed (`003913C4`), and the same "
         "pointer returned (`003913E8`) - Corrected 2026-09-28 (OPUS, `%s`)" % REC)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for k, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and c[1] == "0x050" and OLD_F in c[5] and "~~zeroed once" not in c[5]:
            c[5] = c[5].replace(OLD_F, NEW_F); fl[k] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8"))
    raw = open(CON, "rb").read().decode("utf-8"); assert raw.count(OLD_C) == 1
    open(CON, "wb").write(raw.replace(OLD_C, NEW_C).encode("utf-8")); print("patched"); sys.exit(0)
row = next(cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "NavGridParams" and cells(l)[1] == "0x050")
con = open(CON, "rb").read().decode("utf-8")
live = re.sub(r"~~.*?~~", "", row[5])
check("S", "rather than per query" not in live and "EVERY entry" in row[5] and "caller-supplied record mask" not in re.sub(r"~~.*?~~", "", con),
      "NavGridParams +0x50 states the per-entry clear; the contract names the global cell, not a caller-supplied mask")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
