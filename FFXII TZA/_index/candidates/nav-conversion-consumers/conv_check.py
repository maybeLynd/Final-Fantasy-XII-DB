"""The corridor family's float-to-cell conversions, per function (OPUS, 2026-09-27), consuming ASTRA's
nav-conversion-domain (105677432) after a non-author re-read.
  X1 00383F10 (the grid region query): the four ordered bounds (ja at 00383F77 / 00383F93 / 00383FAF / 00383FCD) run
     BEFORE either conversion (cvttss2si at 00383FF7 / 00384020); origins are s16 (movsx), sizes and counts u8 (movzx),
     so for stable finite inputs the converted values are 0..65025 - an out-of-range coordinate exits early, it never
     becomes a negative index; the classifier branch (_fdclass result == 2, 00383F48 / 00383F5E) also exits before
  X2 no index-range guard after the conversion: add / cdqe / the word read at 00384027..0038402C, sentinel test after
  X3 00391410 (LQUERY) converts its box edges with no bounds before them (0039151F..0039152D) and hands them to 003912E0,
     which CLAMPS each: negative -> 0 (so 0x80000000 from an invalid conversion becomes 0), above count-1 -> count-1
  X4 (2026-09-28) all four negative paths of 003912E0 jump PAST their upper clamp: the rule is piecewise,
     i < 0 ? 0 : min_signed(i, count - 1), [0, count-1] only for positive counts; a NOPped-bypass mutant is rejected
  X5 (2026-09-28) the builder 003924B0 divides each extent by a TRUNCATED provisional count with no zero guard before
     floorf: positive extents do not ensure nonzero counts (contract section 10 item 9)
  S  REGRESSION: the contract's section 10 item 2 no longer says an out-of-range coordinate "is rejected downstream", and
     states both functions' behaviour (FAILS before)
"""
import os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
d = open(os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return (x.mnemonic, x.op_str)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
Q = [x for x in cs.disasm(d[off(0x383F10):off(0x383F10) + 542], 0x383F10)]
first_cvt = min(x.address for x in Q if x.mnemonic == "cvttss2si")
guards = [0x383F77, 0x383F93, 0x383FAF, 0x383FCD]
check("X1 the four bounds and the classifier exit precede the first conversion; s16 origins, u8 sizes/counts",
      first_cvt == 0x383FF7 and all(at(a)[0] == "ja" and a < first_cvt for a in guards)
      and at(0x383F44) == ("cmp", "ax, 2") and at(0x383F48)[0] == "je" and at(0x383F5A) == ("cmp", "ax, 2") and at(0x383F5E)[0] == "je"
      and at(0x383F64) == ("movsx", "edx, word ptr [rbx + 4]") and at(0x383F99) == ("movzx", "ecx, byte ptr [rbx + 2]")
      and at(0x383F9D) == ("movzx", "eax, byte ptr [rbx]"))
post = [x for x in Q if 0x384020 <= x.address < 0x38402C]
check("X2 no range test between the conversion and the cell read; the sentinel test follows the read",
      not any(x.mnemonic in ("cmp", "test") for x in post) and at(0x384027) == ("add", "eax, r8d") and at(0x38402A) == ("cdqe", "")
      and at(0x38402C) == ("movzx", "ecx, word ptr [r9 + rax*2]") and at(0x384031) == ("cmp", "ecx, 0xffff"))
L = [x for x in cs.disasm(d[off(0x3914C0):off(0x391536)], 0x3914C0)]
C = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x3912E0):off(0x3912E0) + 0x90], 0x3912E0)}
check("X3 LQUERY hands unguarded conversions to 003912E0, which clamps each index to [0, count-1]",
      [x.address for x in L if x.mnemonic == "cvttss2si"] == [0x39151F, 0x391524, 0x391529, 0x39152D] and at(0x391531) == ("call", "0x3912e0")
      and not any(x.mnemonic in ("cmp", "test", "comiss", "ucomiss") for x in L if x.address < 0x391531)
      and C[0x39131A] == ("test", "esi, esi") and C[0x39131E] == ("xor", "esi, esi") and C[0x391326] == ("cmp", "esi, eax")
      and C[0x391328] == ("cmovg", "esi, eax") and C[0x391355][0] == "jns" and C[0x391357] == ("xor", "ebp, ebp") and C[0x391360] == ("cmovg", "ebp, eax"))
# X4 (2026-09-28, ASTRA-RETURN-OPUS-NAV-MASK-ZERO-COUNT): X3 tested the zeroing and the upper cmovg but not where each
# negative path GOES, so a copy with the bypass jmp NOPped still passed. X4 binds all four paths: test / jns into the
# upper clamp / xor / jmp to the instruction after that path's cmovg - a negative index SKIPS the upper clamp, so the rule
# is i < 0 ? 0 : min_signed(i, count - 1), which is [0, count-1] only for positive counts (count 0: non-negative -> -1).
PATHS = [(0x39131A, "esi", "r11"), (0x391332, "ebx", "rcx"), (0x391342, "edi", "r11"), (0x391353, "ebp", "rcx")]
def bypass_bound(buf):
    ok = True
    for a, reg, cnt in PATHS:
        ins = list(cs.disasm(buf[off(a):off(a) + 0x20], a))[:7]
        m = [(x.mnemonic, x.op_str) for x in ins]
        after_cmov = ins[6].address + ins[6].size
        ok &= (m[0] == ("test", "%s, %s" % (reg, reg)) and m[1] == ("jns", hex(ins[4].address)) and m[2] == ("xor", "%s, %s" % (reg, reg))
               and m[3][0] == "jmp" and m[3][1] == hex(after_cmov) and m[4] == ("lea", "eax, [%s - 1]" % cnt)
               and m[5] == ("cmp", "%s, eax" % reg) and m[6] == ("cmovg", "%s, eax" % reg))
    return ok
mut = bytearray(d); mut[off(0x391320):off(0x391320) + 2] = b"\x90\x90"      # ASTRA's mutant: the first bypass jmp NOPped
check("X4 all four negative paths jump PAST their upper clamp (the piecewise rule); the NOPped-bypass mutant is rejected",
      bypass_bound(d) and not bypass_bound(bytes(mut)))
# X5 (2026-09-28, ASTRA-RETURN-OPUS-NAV-GRID-INITIAL-TRUNCATION): the builder 003924B0's provisional counts are TRUNCATED
# conversions of extent / c0 (c0 = sqrtf(w*h/275), 00392587) and each extent is then divided by its count with no zero
# test between - so a thin positive rectangle (w 1, h 400: nx 0) sends +inf to floorf. Positive extents are not enough.
G = [x for x in cs.disasm(d[off(0x39258C):off(0x392607) + 5], 0x39258C)]
check("X5 builder: truncating provisional counts, divided into the extents with no zero guard before floorf",
      at(0x392587) == ("call", "0x861f14") and at(0x3925A9) == ("cvttss2si", "eax, xmm1") and at(0x3925CE) == ("cvttss2si", "eax, xmm1")
      and at(0x3925E9) == ("divss", "xmm4, xmm2") and at(0x3925FC) == ("divss", "xmm3, xmm2") and at(0x392600) == ("maxss", "xmm4, xmm3")
      and at(0x392607) == ("call", "0x861f86")
      and not any(x.mnemonic in ("test", "cmp", "comiss", "ucomiss") or x.mnemonic.startswith("j") for x in G if x.address < 0x392607))
page = open(os.path.join(DB, "06-Movement-And-Navigation", "CONTRACT-corridor-query-family.md"), encoding="utf-8").read()
live = re.sub(r"~~.*?~~", "", page, flags=re.S)
check("S item 2 corrected per function",
      "rejected downstream rather than at the conversion" not in live and "003912E0" in live and "clamps" in live
      and "exits before either conversion" in live
      and "i < 0 ? 0 : min_signed(i, count - 1)" in live and "only for positive counts" in live
      and "needs more than positive extents" in live and "not merely `w, h > 0`" in live)
print("FAILS", fails)
sys.exit(1 if fails else 0)
