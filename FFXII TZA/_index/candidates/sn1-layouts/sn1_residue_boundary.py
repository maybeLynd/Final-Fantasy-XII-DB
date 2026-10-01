"""sn1_residue_boundary.py - SN-1 (OPUS, Claude Opus 5.5, 2026-09-28): the evidence a disposition ruling on SN-1's last
residue needs. The residue is what the .dbg q3 listA / listB cut marks; this check makes no claim about its meaning.

  B1 no reader in the shipping image: the PC image names none of the companions - zero '.dbg' / '.sbn' / '.msb' strings
     in either width - while its file-name table carries 10,380 '.ebp' paths (planted positive: the same pass finds the
     scripts the companions accompany)
  B2 the ATEL sibling loader's size query 0032E400 returns -1 for selector 0xFF (`cmp ecx, 0xff` / `je` / `or eax, -1`)
     before any table lookup
  R1 the residue, reproduced from the files: all 50 scopes' q3 tables are {u32 countA; u32 0xFFFFFFFF; u32 listA[countA];
     u32 listB[]; zero pad}; in 49 the cut is positional (listA and listB each ascending, max(listA) < min(listB)); the
     one exception is btlctrl scope 19, whose listA is {0x0B, 0} - the case the page records
  P  (2026-09-28) the page map: q3 = {u32 X; u32 map[E]; zero pad}, map[j] = the last instruction starting before byte 32j,
     map[0] = -1 - re-derived here from q0's flag bytes on all 50 scopes. R1's bytes stand but its listA / listB READING IS
     SUPERSEDED (README Part 4): one ascending array cut by the head word X, and the sc19 'exception' is padding
Not claimed: what the head word X counts.
Usage: python sn1_residue_boundary.py [dir]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def runs(ext):
    a = [m.group(0) for m in re.finditer(rb"[\x20-\x7e]{3,120}", d) if re.search(rb"\." + ext + rb"\b", m.group(0), re.I)]
    w = [m.group(0) for m in re.finditer(rb"(?:[\x20-\x7e]\x00){3,120}", d)
         if re.search(r"\." + ext.decode() + r"\b", m.group(0).decode("utf-16le"), re.I)]
    return len(a), len(w)
n = {e: runs(e) for e in (b"dbg", b"sbn", b"msb", b"ebp")}
check("B1", n[b"dbg"] == n[b"sbn"] == n[b"msb"] == (0, 0) and n[b"ebp"][0] == 10380,
      "strings naming .dbg / .sbn / .msb (ascii, utf-16): %s; .ebp paths: %s" % ([n[e] for e in (b"dbg", b"sbn", b"msb")], n[b"ebp"]))
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; k = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(k)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
at = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x32E400):off(0x32E400) + 0x50], 0x32E400)}
check("B2", at.get(0x32E404) == ("cmp", "ecx, 0xff") and at.get(0x32E40A) == ("je", "0x32e438")
      and at.get(0x32E438) == ("or", "eax, 0xffffffff") and at.get(0x32E43D) == ("jle", "0x32e44b"),
      "0032E400(0xFF, ...) returns -1 before any table lookup")
tot = cut = 0; odd = []
for m in ("ctrl", "btlctrl", "evctrl", "mapctrl"):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    for i in range(ns):
        q3 = offs[4 * i + 3]; end = offs[4 * i + 4] if i < ns - 1 else o0
        cA, ff = struct.unpack_from("<II", b, q3)
        vals = list(struct.unpack_from("<%dI" % ((end - q3) // 4 - 2), b, q3 + 8))
        A = vals[:cA]; Bl = []
        for v in vals[cA:]:
            if v == 0: break
            Bl.append(v)
        tail = vals[cA + len(Bl):]
        tot += 1
        good = ff == 0xFFFFFFFF and not any(tail) and A == sorted(A) and Bl == sorted(Bl) and (not A or not Bl or max(A) < min(Bl))
        cut += good
        if not good: odd.append((m, i, [hex(x) for x in A][:4]))
check("R1", tot == 50 and cut == 49 and odd == [("btlctrl", 19, ["0xb", "0x0"])],
      "%d scopes, %d positional cuts; exceptions %s" % (tot, cut, odd))
# P (2026-09-28, FABLE-NOTICE-OPUS-SN1-Q3-PAGEMAP; re-derived here independently of FABLE's sn1_q3_pagemap.py). R1's bytes stand,
# but its READING is superseded: the q3 table is {u32 X; u32 map[E]; zero pad}, where map[j] is the index of the last instruction
# that starts before byte 32j of the scope's code (map[0] = -1: none starts before byte 0) and E = 1 + floor((codeLen - 1) / 32).
# R1's '0xFFFFFFFF' is map[0], 'countA' is X, and listA + listB are map[1..] - one ascending array cut by the head word, so
# 'max(listA) < min(listB)' holds for any cut and was never evidence of two lists. Instruction starts are the q0 entries whose
# flag byte (+3) is 1, one q0 entry per code byte and then 0-3 all-zero pad entries up to a multiple of 4 (sn1_q0_domain.py Z,
# 2026-09-28: pad entries describe no byte of the script; E is the same over either length, check E there). The 'btlctrl scope 19 exception' is padding: its map is {-1, 0x0B} and the
# 0 R1 took as a second listA entry is the pad word, which appears because its X (2) exceeds its one real entry.
okP = 0; totP = 0; padX = []
for m in ("ctrl", "btlctrl", "evctrl", "mapctrl"):
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read()
    o0 = struct.unpack_from("<I", b, 0)[0]; ns = struct.unpack_from("<I", b, o0)[0]
    offs = struct.unpack_from("<%dI" % (4 * ns + 1), b, o0 + 4)
    for i in range(ns):
        q0, q1, q2, q3 = offs[4 * i:4 * i + 4]; end = offs[4 * i + 4] if i < ns - 1 else o0
        codelen = (q1 - q0) // 4
        starts = [k for k in range(codelen) if b[q0 + 4 * k + 3] == 1]
        E = 1 + (codelen - 1) // 32
        want = [0xFFFFFFFF] + [sum(1 for s in starts if s < 32 * j) - 1 for j in range(1, E)]
        X = struct.unpack_from("<I", b, q3)[0]
        words = list(struct.unpack_from("<%dI" % ((end - q3) // 4 - 1), b, q3 + 4))
        totP += 1; okP += words[:E] == want and not any(words[E:])
        if X > E - 1: padX.append((m, i, X, E - 1))
check("P", totP == 50 and okP == 50 and [(m_, i_) for m_, i_, x_, e_ in padX] == [("ctrl", 5), ("btlctrl", 2), ("btlctrl", 19)],
      "%d / %d scopes: q3 = {X; map[E]} with map[j] = last instruction starting before byte 32j, map[0] = -1, zero pad after; "
      "scopes whose head word X exceeds the real entries (the padding cases): %s" % (okP, totP, padX))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
