"""widget0720_child.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
Follow-up to battle_menu_child_base.py X: the span OPUS declared on Widget0720At0209BE80_AB30 today (+0xC0, 0x650 bytes,
'reached by its methods; not typed here') is a nested widget its own handler builds.

  N  the handler 002985D0 (rbx = rcx) on message 1 does `lea r8 -> 00298250`, `mov edx, 0x650`, `lea rcx, [rbx + 0xc0]`,
     `call 00245000` (00298686) - a 0x650-byte widget at this + 0xC0, ending at +0x710 where dword0710 begins; on messages
     2 and 0x12 it tests (00273A20) and destroys (00245020) that child. 00296960's reads at +0x180 / +0x414 / +0x648
     (CONTRACT-per-frame-update-gate) are inside it
  W  REGRESSION (FAILS before): Widget0720At0209BE80_AB30 +0xC0 is WidgetChild0650At298250, which exists and tiles
Usage: python widget0720_child.py [--patch]
"""
import hashlib, os, sys
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
    return all(A.get(a) == v for a, v in pairs)
check("N", has(0x2985D0, 0x29868B, [(0x2985D6, ("mov", "rbx, rcx")), (0x2985DB, ("sub", "ecx, 1")), (0x2985DE, ("je", "0x298644")), (0x2985F7, ("lea", "rcx, [rbx + 0xc0]")),
                                     (0x2985FE, ("call", "0x273a20")), (0x29860C, ("lea", "rcx, [rbx + 0xc0]")), (0x298613, ("call", "0x245020")),
                                     (0x298673, ("lea", "r8, [rip - 0x42a]")), (0x29867A, ("mov", "edx, 0x650")), (0x29867F, ("lea", "rcx, [rbx + 0xc0]")), (0x298686, ("call", "0x245000"))])
      and 0x29867A - 0x42A == 0x298250 and 0xC0 + 0x650 == 0x710,
      "002985D0 builds a 0x650 widget (handler 00298250) at this + 0xC0, ending at +0x710")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/battle-menu-child-base-opus/widget0720_child.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
W7, CH = "Widget0720At0209BE80_AB30", "WidgetChild0650At298250"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def cells(l): return l.rstrip("\r\n").split("\t")
CHROWS = [[CH, "0x000", "192", "widgetBase0000", "Widget", "the shared Widget header 00245000 writes on construction", P[0], P[1], "DECLARED 2026-09-28 (OPUS, %s N). %s" % (REC, EXE)],
          [CH, "0x0C0", "1424", "unobservedSpan0C0", "u8[1424]", "the child's own fields (its handler 00298250 is not read here); 00296960 reads the parent's +0x414 / +0x648 = this +0x354 / +0x588", U[0], U[1], "DECLARED 2026-09-28 (OPUS, %s N). %s" % (REC, EXE)]]
NEWT = [CH, "0x650", "16-UI", "one at Widget0720At0209BE80_AB30 +0xC0, built by that widget's handler on message 1", "IN PLACE - 00245000 at 00298686",
        "00245000 at 00298686 (`mov edx, 0x650` at 0029867A; handler 00298250)", "00245020 on message 2 (0029860C)", P[0], P[1], "L1",
        "DECLARED 2026-09-28 (OPUS, %s N). %s" % (REC, EXE), "00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md", "EMBED Widget0720At0209BE80_AB30 +0xC0"]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]; out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == W7 and int(c[1], 16) == 0xC0 and c[3] == "unobservedSpan0C0":
            out.append("\t".join([W7, "0x0C0", "1616", "childWidget0C0", CH, "a 0x650 widget the handler builds here on message 1 and destroys on message 2", P[0], P[1],
                                  "CARVED 2026-09-28 (OPUS, %s N). was unobservedSpan0C0 u8[1616] (%s). %s" % (REC, c[5][:140], EXE)]) + e); continue
        out.append(l)
    if not any(cells(l)[0] == CH for l in out):   # idempotent: the child's rows are added once
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == W7); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in CHROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == CH for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == W7); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
row = next((c for c in F if c[0] == W7 and int(c[1], 16) == 0xC0), None)
check("W", row is not None and row[4] == CH and CH in T and sum(int(c[2]) for c in F if c[0] == CH) == 0x650 and sum(int(c[2]) for c in F if c[0] == W7) == 0x720,
      "Widget0720At0209BE80_AB30 +0xC0 is the 0x650 child; both types tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
