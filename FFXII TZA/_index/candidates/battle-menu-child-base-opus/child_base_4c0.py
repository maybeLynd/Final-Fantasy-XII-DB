"""child_base_4c0.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The battle-menu child base is a widget of its own, 0x4C0 bytes: WidgetChild0650At298250 builds one standalone at its +0xC0, and
BattleMenuChildWidget1620's first 0x4C0 bytes are the same object. So the layout moves to one type both embed.

  B  00298250 (the 0x650 child's handler) builds, at this + 0xC0, `00245000(this + 0xC0, 0x4C0, 002985C0)` (00298488..0029849E),
     and 002985C0 is `jmp 003EE420` - the base handler battle_menu_child_base.py J/R/W read on the 0x1620 widget; then it calls
     003EE8C0(this + 0xC0, ..) (002984C0), which counts the word +0x4B0 (003EE8DA / 003EE900 / 003EE907)
  E  BattleMenuChildWidget1620's rows below +0x4C0 tile exactly 0x4C0 and hold nothing but what 003EE420 reaches (header,
     BattleMenuChildRecord1E0[2] at +0xC0, +0x480..+0x4B8); the 0x1620 widget's own fields start at +0x4C0
  N  the 0x650 child's own fields: int16 +0x580 / +0x582 copied from a layout element's +0x0C / +0x0E (0029835E / 00298369; +0x582
     read with movsx at 00298541), +0x584 / +0x586 = a coordinate minus them (0029844F / 00298464), a bare 0xC0 Widget at +0x588
     (`00245000(this + 0x588, 0xC0, 0017CDE0)` at 002982AE), and int16 +0x648..+0x64E copied from an element's +0x0C..+0x12
  W  REGRESSION (FAILS before): BattleMenuChildBase4C0 exists and tiles; BattleMenuChildWidget1620 embeds it at +0 with no row
     below +0x4C0 besides it; the 0x650 child embeds it at +0xC0; BattleMenuChildRecord1E0 is routed through it
Not claimed: what the 0x650 child's int16 fields position; the +0x588 widget's role.
Usage: python child_base_4c0.py [--patch]
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
check("B", has(0x298488, 0x2984C5, [(0x29848B, ("lea", "r8, [rip + 0x12e]")), (0x298492, ("mov", "edx, 0x4c0")), (0x298497, ("lea", "rcx, [rsi + 0xc0]")),
                                     (0x29849E, ("call", "0x245000")), (0x2984B3, ("lea", "rcx, [rsi + 0xc0]")), (0x2984C0, ("call", "0x3ee8c0"))])
      and 0x298492 + 0x12E == 0x2985C0 and has(0x2985C0, 0x2985C5, [(0x2985C0, ("jmp", "0x3ee420"))])
      and has(0x3EE8C0, 0x3EE910, [(0x3EE8DA, ("movzx", "eax, word ptr [rcx + 0x4b0]")), (0x3EE900, ("inc", "word ptr [rcx + 0x4b0]")), (0x3EE907, ("cmp", "word ptr [rcx + 0x4b0], 2"))]),
      "00298250 builds a 0x4C0 widget at this + 0xC0 with the handler 002985C0 = jmp 003EE420, then 003EE8C0 on it")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
BM, BASE, CH, RC = "BattleMenuChildWidget1620", "BattleMenuChildBase4C0", "WidgetChild0650At298250", "BattleMenuChildRecord1E0"
low = sorted((int(c[1], 16), int(c[2])) for c in F if c[0] == BM and int(c[1], 16) < 0x4C0)
cur = sorted((int(c[1], 16), int(c[2])) for c in F if c[0] in (BM, BASE) and int(c[1], 16) < 0x4C0)
check("E", (sum(n for o, n in low) == 0x4C0 and all(a[0] + a[1] == b[0] for a, b in zip(low, low[1:]))) or low == [(0, 0x4C0)],
      "BattleMenuChildWidget1620's rows below +0x4C0 tile exactly 0x4C0 (or are the one embed row)")
check("N", has(0x298340, 0x2983C4, [(0x29835A, ("movzx", "eax, word ptr [rcx + 0xc]")), (0x29835E, ("mov", "word ptr [rsi + 0x580], ax")), (0x298365, ("movzx", "eax, word ptr [rcx + 0xe]")),
                                     (0x298369, ("mov", "word ptr [rsi + 0x582], ax")), (0x298398, ("movzx", "eax, word ptr [rcx + 0xc]")), (0x29839C, ("mov", "word ptr [rsi + 0x648], ax")),
                                     (0x2983A7, ("mov", "word ptr [rsi + 0x64a], ax")), (0x2983B2, ("mov", "word ptr [rsi + 0x64c], ax")), (0x2983BD, ("mov", "word ptr [rsi + 0x64e], ax"))])
      and has(0x298443, 0x298470, [(0x298448, ("sub", "ax, word ptr [rsi + 0x580]")), (0x29844F, ("mov", "word ptr [rsi + 0x584], ax")), (0x29845D, ("sub", "ax, word ptr [rsi + 0x582]")),
                                   (0x298464, ("mov", "word ptr [rsi + 0x586], ax"))])
      and has(0x298284, 0x2982B3, [(0x298284, ("lea", "rcx, [rsi + 0x588]")), (0x298290, ("lea", "r8, [rip - 0x11b4b7]")), (0x2982A4, ("mov", "edx, 0xc0")), (0x2982AE, ("call", "0x245000"))])
      and 0x298297 - 0x11B4B7 == 0x17CDE0 and has(0x298530, 0x298550, [(0x298541, ("movsx", "r8d, word ptr [rsi + 0x582]"))]),
      "the 0x650 child's +0x580..+0x586, the 0xC0 widget at +0x588 and +0x648..+0x64E")
REC = "_index/candidates/battle-menu-child-base-opus/child_base_4c0.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
P = ("TYPE RESOLVED", "PROVEN")
def r(t, o, n, nm, ct, m, w=3, rd=P, tag="N", was="-"): return [t, ("0x%0" + str(w) + "X") % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)]
def child_rows(was):
    return [r(CH, 0xC0, 0x4C0, "battleMenuBase0C0", BASE, "a BattleMenuChildBase4C0 built here by the handler (00245000 at 0029849E, handler 002985C0 = jmp 003EE420)", tag="B", was=was),
            r(CH, 0x580, 2, "posX580", "int16", "copied from a layout element's +0x0C (0029835E)", was=was),
            r(CH, 0x582, 2, "posY582", "int16", "copied from the element's +0x0E (00298369); read signed at 00298541", was=was),
            r(CH, 0x584, 2, "deltaX584", "int16", "a coordinate minus +0x580 (0029844F)", was=was),
            r(CH, 0x586, 2, "deltaY586", "int16", "a coordinate minus +0x582 (00298464)", was=was),
            r(CH, 0x588, 0xC0, "widget588", "Widget", "a bare 0xC0 Widget built here (00245000 at 002982AE, handler 0017CDE0)", was=was),
            r(CH, 0x648, 8, "rect648", "int16[4]", "four int16 copied from a layout element's +0x0C..+0x12 (0029839C..002983BD)", was=was)]
BASEROW = [BASE, "0x4C0", "16-UI", "one per BattleMenuChildWidget1620 (at +0) and one at WidgetChild0650At298250 +0xC0", "EMBEDDED (constructed in place)",
           "00245000 at 0029849E (`mov edx, 0x4c0` at 00298492; handler 002985C0 = jmp 003EE420)", "not read here", "TYPE RESOLVED", "PROVEN", "L1",
           "CARVED 2026-09-28 (OPUS, %s B E). The layout battle_menu_child_base.py read on BattleMenuChildWidget1620's first 0x4C0 bytes, moved here: a "
           "standalone 0x4C0 construction proves the extent. %s" % (REC, EXE), "", "EMBED BattleMenuChildWidget1620 +0x0000"]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; moved = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == BM and int(c[1], 16) < 0x4C0:
            c2 = list(c); c2[0] = BASE; c2[8] += " || RE-HOMED 2026-09-28 (OPUS, %s E): from BattleMenuChildWidget1620 at the same offset" % REC
            moved.append("\t".join(c2) + e)
            if int(c[1], 16) == 0:
                out.append("\t".join([BM, "0x0000", str(0x4C0), "base0000", BASE, "the battle-menu child base (header, two records, +0x480..+0x4B8) that 003EE420 handles; "
                                      "the 0x1620 widget's own fields start at +0x4C0", P[0], P[1], "RE-HOMED 2026-09-28 (OPUS, %s E): the rows below +0x4C0 now belong to %s. %s" % (REC, BASE, EXE)]) + e)
            continue
        if c[0] == CH and c[1] == "0x0C0" and c[2] == "1424":
            out += ["\t".join(x) + e for x in child_rows("%s %s (%s)" % (c[3], c[4], c[5][:160]))]; continue
        out.append(l)
    assert len(moved) >= 10
    idx = max(i for i, l in enumerate(out) if cells(l)[0] == BM); out[idx + 1:idx + 1] = moved
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == RC:
            c[3] = "two per BattleMenuChildBase4C0, at +0xC0"; c[4] = "EMBEDDED in BattleMenuChildBase4C0"
            c[12] = "EMBED BattleMenuChildBase4C0 +0x00C0 stride=0x1E0 count=2"; c[10] += " || RE-ROUTED 2026-09-28 (OPUS, %s): the records' parent is the 0x4C0 base" % REC
            BASEROW[11] = c[11]; tl[i] = "\t".join(c) + e
    if not any(cells(l)[0] == BASE for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == BM); tl[ti + 1:ti + 1] = ["\t".join(BASEROW) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
base = sorted((int(c[1], 16), int(c[2])) for c in F if c[0] == BASE)
bm_low = [(int(c[1], 16), c[4]) for c in F if c[0] == BM and int(c[1], 16) < 0x4C0]
ch = {int(c[1], 16): c for c in F if c[0] == CH}
check("W", BASE in T and sum(n for o, n in base) == 0x4C0 and all(a[0] + a[1] == b[0] for a, b in zip(base, base[1:])) and bm_low == [(0, BASE)]
      and ch.get(0xC0, [""] * 5)[4] == BASE and T.get(RC, [""] * 13)[12].startswith("EMBED " + BASE),
      "BattleMenuChildBase4C0 tiles; BattleMenuChildWidget1620 embeds it at +0; the 0x650 child at +0xC0; the records route through it")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
