"""child_widget.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

MapScreenContainer (0x179E0, itself a widget; proc 002B7590 / 002BA700 / 003CB650) carries 30 rows over +0xC0..+0x17F -
three of them 'mixed ... NOT resolved' - that restate, offset for offset, the shared Widget header of a CHILD widget built
in place at +0xC0. And four of those rows are the only record of Widget +0x68..+0x78, which the Widget type lacks.

  C  the child: 002B79BD builds a 0xD0-byte widget at +0xC0 (`mov edx, 0xd0` / `lea rcx, [rbx+0xc0]` / call 00245000,
     whose initialiser 002465F0 lays the header); 002B788F / 002B78DC / 002B792F / 002B7967 null-test it through the
     widget predicate 00273A20. 0xC0 + 0xD0 = 0x190, the next row (qword0190)
  H  the header initialiser's own stores land on the container at +0xC0 + k: 002465F0's [rdi+0x40] / +0x44 / +0x9C /
     +0xA0 / +0xA1 are the census's +0x100 / +0x104 / +0x15C / +0x160 / +0x161
  G  Widget +0x68..+0x78, from the generic widget body 00244DD0 (the census's +0x128..+0x138 sites):
       +0x68 a record pointer: [+0x48] + 0x14 (00244E80 / 00244E84) or a static record, stored at 00244E88 and
             dereferenced as `movzx edi, word ptr [rcx+2]` (00244E9C)
       +0x70 a dword: the frame count ms * 60 / 1000 (00244EC2 imul 0x3c, 00244EC5 / 00244ECF / 00244ED1 the /1000
             multiply-shift), stored at 00244ED4; zeroed at 00244E6A and subtracted at 00244E75
       +0x74 a dword: the global frame clock 0208F570 (00244E8C / 00244E92), rebased at 00244E6D..00244E7B
       +0x78 a dword initialised to 0x3F800000 at 00244E95 - the bit pattern of 1.0f; no typed access here, so width only
  S  REGRESSION: Widget has +0x68 / +0x70 / +0x74 / +0x78; MapScreenContainer has one +0xC0 row typed Widget (192) and
     nothing else starting in +0xC0..+0x17F (FAILS before the patch)
Usage: python child_widget.py [--patch]
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.abspath(os.path.join(DB, ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
FIELDS = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/mapscreen-child-widget/child_widget.py"
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
MSC, W = "MapScreenContainer", "Widget"
NEW_W = [
    (0x68, 8, "timedRecord68", "void*", "a record pointer set by 00244DD0: [+0x48] + 0x14 (the class table's record) or a static "
     "record, then read as `movzx edi, word ptr [rcx+2]`. What the record describes is NOT claimed",
     "00244E80 / 00244E84 / 00244E88 store; 00244E9C dereference"),
    (0x70, 4, "timedFrames70", "uint32", "a frame count 00244DD0 computes as ms * 60 / 1000 (imul 0x3c, then the /1000 "
     "multiply-shift) - the same ms-to-60-Hz conversion as transitionDurationFrames +0x90; zeroed on one path and subtracted "
     "on another. MEANING beyond the conversion NOT claimed", "00244EC2 / 00244ED1 / 00244ED4; 00244E6A; 00244E75"),
    (0x74, 4, "timedStartFrame74", "uint32", "the global frame clock 0208F570 at the time 00244DD0 runs (as "
     "transitionStartFrame +0x94 is), or a value rebased from it (2 * clock - +0x70 - +0x74)", "00244E8C / 00244E92; 00244E6D..00244E7B"),
    (0x78, 4, "timedInit78", "uint32", "initialised to 0x3F800000 (the bit pattern of 1.0f) by 00244DD0; no typed access here, "
     "so the type is the width, not a claim of integer representation", "00244E95"),
]

if "--patch" in sys.argv:
    if any(cells(l)[0] == W and cells(l)[1] == "0x068" for l in fl): print("already"); sys.exit(0)
    inside = [i for i, l in enumerate(fl) if cells(l)[0] == MSC and 0xC0 <= int(cells(l)[1], 16) < 0x180]
    assert inside == list(range(inside[0], inside[-1] + 1)) and len(inside) == 30, len(inside)
    old = [cells(fl[i]) for i in inside]; wd = len(old[0]); eol = fl[inside[0]][len(fl[inside[0]].rstrip("\r\n")):]
    def frow(c): return "\t".join(list(c) + [""] * (wd - len(c))) + eol
    region = [MSC, "0x00C0", "192", "childWidgetHeader0C0", "Widget",
              "THE HEADER OF A CHILD WIDGET built in place here: 002B79BD constructs a 0xD0-byte widget at +0xC0 through "
              "00245000 / 002465F0, so +0xC0..+0x17F is Widget's shared header and +0x180..+0x18F its 0x10 bytes of content "
              "(the rows that follow). One region row under FABLE's rule 0; the header's fields are Widget's rows.",
              "TYPE RESOLVED", "PROVEN",
              "COLLAPSED 2026-09-28 (OPUS, " + REC + " C H): the construction size and the header initialiser's stores at "
              "+0xC0 + k. ABSORBED ROWS (name and old type verbatim; each restated a Widget header row at offset - 0xC0; "
              "the four at +0x128..+0x138 migrate into Widget +0x68..+0x78): " +
              "; ".join("%s %s %s %s" % (c[1], c[2], c[3], c[4]) for c in old)]
    fl[inside[0]:inside[-1] + 1] = [frow(region)]
    wi = [i for i, l in enumerate(fl) if cells(l)[0] == W]
    after = max(i for i in wi if int(cells(fl[i])[1], 16) < 0x68)
    migrated = {0x68: "0x0128", 0x70: "0x0130", 0x74: "0x0134", 0x78: "0x0138"}
    src = {c[1]: c for c in old}
    ww = len(cells(fl[wi[0]])); weol = fl[wi[0]][len(fl[wi[0]].rstrip("\r\n")):]
    newrows = []
    for o, s, nm, ct, mean, ev in NEW_W:
        m = src[migrated[o]]
        r = [W, "0x%03X" % o, str(s), nm, ct, mean, "TYPE RESOLVED", "PROVEN",
             "ADDED 2026-09-28 (OPUS, %s G): 00244DD0 %s. || MIGRATED from %s +%s (%s %s), evidence verbatim: %s | %s"
             % (REC, ev, MSC, m[1], m[3], m[4], m[5], m[8])]
        newrows.append("\t".join(r + [""] * (ww - len(r))) + weol)
    fl[after + 1:after + 1] = newrows
    open(FIELDS, "wb").write("".join(fl).encode("utf-8"))
    print("Widget +4 rows; MapScreenContainer 30 rows -> 1 region row"); sys.exit(0)

check("C", at(0x2B79A8) == ("mov", "edx, 0xd0") and at(0x2B79B1) == ("lea", "rcx, [rbx + 0xc0]")
      and at(0x2B79BD) == ("call", "0x245000")
      and all(at(l) == ("lea", "rcx, [rbx + 0xc0]") and at(c) == ("call", "0x273a20")
              for l, c in ((0x2B7888, 0x2B788F), (0x2B78D5, 0x2B78DC), (0x2B7928, 0x2B792F), (0x2B7960, 0x2B7967))),
      "002B79BD: 0xD0 widget at +0xC0 (mov edx, 0xd0 / lea rcx, [rbx+0xc0]); null-tested at four sites")
check("H", at(0x246660) == ("mov", "dword ptr [rdi + 0x40], ecx") and at(0x246670) == ("and", "dword ptr [rdi + 0x44], 0xfff8ffff")
      and at(0x246717) == ("mov", "dword ptr [rdi + 0x9c], 0x800080") and at(0x24670A) == ("mov", "byte ptr [rdi + 0xa0], 0x80")
      and at(0x2466E6) == ("mov", "word ptr [rdi + 0xa1], 0xff80"),
      "002465F0's header stores (+0x40 / +0x44 / +0x9C / +0xA0 / +0xA1) are the census's +0x100 / +0x104 / +0x15C / +0x160 / +0x161")
g = (at(0x244E80) == ("mov", "rcx, qword ptr [rbx + 0x48]") and at(0x244E84) == ("add", "rcx, 0x14")
     and at(0x244E88) == ("mov", "qword ptr [rbx + 0x68], rcx") and at(0x244E9C) == ("movzx", "edi, word ptr [rcx + 2]")
     and at(0x244EC2) == ("imul", "ecx, edi, 0x3c") and at(0x244EC5) == ("mov", "eax, 0x10624dd3") and at(0x244ED1) == ("shr", "edx, 6")
     and at(0x244ED4) == ("mov", "dword ptr [rbx + 0x70], edx") and at(0x244E75) == ("sub", "eax, dword ptr [rbx + 0x70]")
     and at(0x244E92) == ("mov", "dword ptr [rbx + 0x74], eax") and 0x244E8C + 6 + 0x1e4a6de == 0x208F570
     and at(0x244E8C) == ("mov", "eax, dword ptr [rip + 0x1e4a6de]") and at(0x244E95) == ("mov", "dword ptr [rbx + 0x78], 0x3f800000"))
check("G", g, "00244DD0: +0x68 record pointer, +0x70 ms->frames, +0x74 clock 0208F570, +0x78 = 0x3F800000")
Wr = {int(cells(l)[1], 16) for l in fl if cells(l)[0] == W}
Mr = [cells(l) for l in fl if cells(l)[0] == MSC and 0xC0 <= int(cells(l)[1], 16) < 0x180]
check("S", {0x68, 0x70, 0x74, 0x78} <= Wr and [(c[1], c[2], c[4]) for c in Mr] == [("0x00C0", "192", "Widget")],
      "Widget +0x68..+0x78 declared; MapScreenContainer +0xC0 is one Widget row (now %d rows there)" % len(Mr))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
