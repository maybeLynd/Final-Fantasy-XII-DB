"""widget_singleton_nested.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
CORRECTION of OPUS's own 'no access by either body installed' rows on WidgetSingleton02B47758 and two of its children:
each of them holds a nested widget at its +0xC0, which the installed handlers construct or drive through the shared widget
routines. The earlier census treated those calls' receivers as outside the object.

  N  WidgetSingleton02B47758_0460's handler 003CAE00 (rdi = this), on message 14, builds a 0xD0-byte widget at this + 0xC0
     (`lea rcx, [rdi + 0xc0]`, `mov edx, 0xd0`, handler `lea r8 -> 003CA530`, `call 00245000`) and attaches it (00244960) -
     0xC0 + 0xD0 = 0x190, the child's whole tail
  F  WidgetSingleton02B47758_05F0's handler 003CA310 (rdi = this) hands this + 0xC0 to 00244F00 (twice), 00273A20 and
     00241C90; the singleton's handler 003CA860 (rdi = this) hands this + 0xC0 to 00273A20 (twice) and 00244F00
  W  those routines treat their argument as a widget: 00273A20 tests the qword at +0 (the handler slot), 00244F00 ORs 0x40
     into the dword at +0x40, calls the handler at +0, and 00244DD0 (reached from it) writes the float at +0xB8 and the
     flags at +0x7C - Widget header fields. So +0xC0 holds a widget header in both; the store's 'qword00C0' is its handler
     slot. Neither construction site is read here, so the nested widget's full extent past its 0xC0 header stays open
  P  REGRESSION (FAILS before): the three nested rows are in the store and no absence row starts at +0xC0 / +0xC8
Usage: python widget_singleton_nested.py [--patch]
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.skipdata = True
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    return all(A.get(a) == v for a, v in pairs)
check("N", has(0x3CAE00, 0x3CAE65, [(0x3CAE06, ("mov", "rdi, rcx")), (0x3CAE0B, ("sub", "ecx, 1")), (0x3CAE10, ("cmp", "ecx, 0xd")), (0x3CAE22, ("lea", "rcx, [rdi + 0xc0]")),
                                     (0x3CAE31, ("lea", "r8, [rip - 0x908]")), (0x3CAE38, ("mov", "edx, 0xd0")), (0x3CAE3D, ("call", "0x245000")), (0x3CAE45, ("mov", "rcx, rdi")),
                                     (0x3CAE4B, ("call", "0x244960"))]) and 0x3CAE38 - 0x908 == 0x3CA530,
      "_0460 handler: message 14 builds a 0xD0 widget (handler 003CA530) at this + 0xC0 and attaches it")
check("F", has(0x3CA310, 0x3CA530, [(0x3CA32F, ("mov", "rdi, rcx")), (0x3CA37E, ("lea", "rcx, [rdi + 0xc0]")), (0x3CA385, ("call", "0x244f00")), (0x3CA3BA, ("lea", "rcx, [rdi + 0xc0]")),
                                     (0x3CA3C1, ("call", "0x244f00")), (0x3CA404, ("lea", "rcx, [rdi + 0xc0]")), (0x3CA40B, ("call", "0x273a20")), (0x3CA4EA, ("lea", "rcx, [rdi + 0xc0]"))])
      and has(0x3CA860, 0x3CAE00, [(0x3CA879, ("mov", "rdi, rcx")), (0x3CA9A0, ("lea", "rcx, [rdi + 0xc0]")), (0x3CA9CA, ("lea", "rcx, [rdi + 0xc0]")), (0x3CAA07, ("lea", "rcx, [rdi + 0xc0]"))]),
      "_05F0 and singleton handlers pass this + 0xC0 to the widget routines")
check("W", has(0x273A20, 0x273A29, [(0x273A22, ("cmp", "qword ptr [rcx], rax"))]) and has(0x244F00, 0x244F44, [(0x244F0A, ("or", "dword ptr [rcx + 0x40], 0x40")),
                                     (0x244F25, ("mov", "rax, qword ptr [rcx]")), (0x244F34, ("call", "rax")), (0x244F20, ("jmp", "0x244dd0"))])
      and has(0x244DD0, 0x244E30, [(0x244DDE, ("mov", "rbx, rcx")), (0x244DE1, ("mov", "dword ptr [rcx + 0xb8], 0x3f800000")), (0x244E17, ("mov", "edx, dword ptr [rbx + 0x40]")),
                                   (0x244E23, ("or", "dword ptr [rbx + 0x7c], 1"))]),
      "the routines read the handler slot +0 and write the header's +0x40 / +0x7C / +0xB8")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/widget-singleton-nested-opus/widget_singleton_nested.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
S0, S4, S5, NW = "WidgetSingleton02B47758", "WidgetSingleton02B47758_0460", "WidgetSingleton02B47758_05F0", "WidgetChild00D0At3CA530"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CORRECTED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-"): return [t, "0x%03X" % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
HDR = "the header of a widget embedded at +0xC0: the handler hands this + 0xC0 to 00273A20 / 00244F00, which test its handler slot and write its +0x40 / +0x7C / +0xB8. Its construction and its extent past 0xC0 are not read here"
def cuts(old):
    w = lambda t, o: "%s %s (%s)" % (old[(t, o)][3], old[(t, o)][4], old[(t, o)][5][:120])
    return {(S4, 0xC0): [r(S4, 0xC0, 0xD0, "nestedWidget0C0", NW, "a 0xD0 widget the handler builds here on message 14 (handler 003CA530) and attaches as a child", P, "N", w(S4, 0xC0))],
            (S5, 0xC0): [r(S5, 0xC0, 0xC0, "nestedWidget0C0", "Widget", HDR, P, "F W", "%s; %s" % (w(S5, 0xC0), w(S5, 0xC8))),
                         r(S5, 0x180, 784, "unobservedSpan180", "u8[784]", "after the nested widget's header; not read by the handler here", U, "F", w(S5, 0xC8))],
            (S0, 0xC0): [r(S0, 0xC0, 0xC0, "nestedWidget0C0", "Widget", HDR, P, "F W", "%s; %s" % (w(S0, 0xC0), w(S0, 0xC8))),
                         r(S0, 0x180, 264, "unobservedSpan180", "u8[264]", "after the nested widget's header; not read by the handler here", U, "F", w(S0, 0xC8))]}
DROP = {(S5, 0xC8), (S0, 0xC8)}
NWROWS = [r(NW, 0x00, 0xC0, "widgetBase0000", "Widget", "the shared Widget header 00245000 writes on construction", P, "N"),
          r(NW, 0xC0, 16, "unobservedSpan0C0", "u8[16]", "not read here", U, "N")]
NEWT = [NW, "0xD0", "16-UI", "one at WidgetSingleton02B47758_0460 +0xC0, built by that widget's handler on message 14",
        "IN PLACE - 00245000 at 003CAE3D", "00245000 at 003CAE3D (`mov edx, 0xd0` at 003CAE38; handler 003CA530)", "not read here", P[0], P[1], "L1",
        "DECLARED 2026-09-28 (OPUS, %s N). %s" % (REC, EXE), "16-UI/Widget-Object-Model/CONTRACT-widget-object.md", "EMBED WidgetSingleton02B47758_0460 +0xC0"]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    old = {(cells(l)[0], int(cells(l)[1], 16)): cells(l) for l in fl if cells(l)[0] in (S0, S4, S5)}
    assert old[(S4, 0xC0)][2] == "208" and old[(S5, 0xC8)][2] == "968" and old[(S0, 0xC8)][2] == "448"
    C = cuts(old); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        k = (c[0], int(c[1], 16)) if c[0] in (S0, S4, S5) else None
        if k in C: out += ["\t".join(x) + e for x in C[k]]; continue
        if k in DROP: continue
        out.append(l)
    idx = max(i for i, l in enumerate(out) if cells(l)[0] == S5)
    out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in NWROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == NW for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == S5); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = {(cells(l)[0], int(cells(l)[1], 16)): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in (S0, S4, S5, NW)}
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for k, c in F.items() if k[0] == t) == int(T[t][1], 16)
check("P", F.get((S4, 0xC0), [0] * 5)[4] == NW and F.get((S5, 0xC0), [0] * 5)[4] == "Widget" and F.get((S0, 0xC0), [0] * 5)[4] == "Widget"
      and (S5, 0xC8) not in F and (S0, 0xC8) not in F and all(tiles(t) for t in (S0, S4, S5, NW)),
      "nested widgets at +0xC0 of the singleton, _0460 (0xD0 child) and _05F0; the old absence spans are gone; the four types tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
