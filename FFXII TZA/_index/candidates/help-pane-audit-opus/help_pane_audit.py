"""help_pane_audit.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The last two types of the 'no access by either body installed' audit (after dc2bcc912, 4250ca069, 6a597a1a0).

  H  HelpMessageSlotRecord0100 is built whole by 00245000 at 002BFCCA (`mov edx, 0x100` at 002BFCC2, handler 002BF8C0) -
     so its first 0xC0 bytes are the shared Widget header. The re-described header rows are replaced by widgetBase0000,
     including six absence spans inside it; one of them (+0x08) was contradicted by 00247930, which reads the header's
     +0x10 (Widget.parent) on the element. The census hit at +0x60 (002BFBFC) is not the element's: that code's rdi is
     the parent HelpMessageWidget0500 (it steps the parent's +0x4E8 cursor), so no row changes for it
  P  PaneListWidget0B68: 0029C850 (rdi = this) builds a 0xC0-byte widget at this + 0xC0 (`lea rsi, [rcx + 0xc0]`,
     `mov edx, 0xc0`, `call 00245000` at 0029C93A) and otherwise drives it (00273A20 / 00244F00 / 002468A0); the rows
     qword00C0 (its handler slot), dword013C (its +0x7C) and the two spans between are that widget's header
  S  0029C850 reads the dword at +0xB58 as a pane-slot index: `imul rcx, rax, 0x160` and the word at
     [this + 0x160k + 0x2DA] = paneSlots0240[k] + 0x9A
  W  REGRESSION (FAILS before): the rows are in the store; both types tile; neither re-describes a header
Usage: python help_pane_audit.py [--patch]
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
check("H", has(0x2BFCBB, 0x2BFCCF, [(0x2BFCBB, ("lea", "r8, [rip - 0x402]")), (0x2BFCC2, ("mov", "edx, 0x100")), (0x2BFCCA, ("call", "0x245000"))]) and 0x2BFCC2 - 0x402 == 0x2BF8C0
      and has(0x247930, 0x24794A, [(0x247935, ("mov", "rax, qword ptr [rcx + 0x10]"))])
      and has(0x2BFBE0, 0x2BFC04, [(0x2BFBE0, ("cmp", "byte ptr [rdi + 0x4e8], 4")), (0x2BFBFC, ("mov", "rax, qword ptr [rdi + 0x60]"))]),
      "the element is built whole at 002BFCCA; 00247930 reads Widget.parent; 002BFBFC's rdi is the parent (its +0x4E8 cursor)")
check("P", has(0x29C850, 0x29C940, [(0x29C85A, ("lea", "rsi, [rcx + 0xc0]")), (0x29C861, ("mov", "rdi, rcx")), (0x29C867, ("call", "0x273a20")), (0x29C8BF, ("call", "0x244f00")),
                                     (0x29C919, ("mov", "rcx, rsi")), (0x29C91C, ("call", "0x2468a0")), (0x29C932, ("mov", "edx, 0xc0")), (0x29C937, ("mov", "rcx, rsi")),
                                     (0x29C93A, ("call", "0x245000"))]),
      "0029C850 builds and drives a 0xC0 widget at this + 0xC0")
check("S", has(0x29C8D1, 0x29C904, [(0x29C8D1, ("movsxd", "rax, dword ptr [rdi + 0xb58]")), (0x29C8E5, ("imul", "rcx, rax, 0x160")), (0x29C8FB, ("movsx", "r8d, word ptr [rcx + rdi + 0x2da]"))])
      and 0x2DA - 0x240 == 0x9A, "+0xB58 is a pane-slot index (x 0x160 into paneSlots0240, reading each slot's +0x9A)")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/help-pane-audit-opus/help_pane_audit.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
HM, PL = "HelpMessageSlotRecord0100", "PaneListWidget0B68"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CORRECTED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    hm = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == HM}
    pl = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == PL}
    assert sum(int(c[2]) for o, c in hm.items() if o < 0xC0) == 0xC0 and pl[0xC0][3] == "qword00C0" and pl[0x13C][3] == "dword013C" and pl[0xB4C][2] == "28"
    hmwas = "; ".join("+0x%X %s %s" % (o, c[3], c[4]) for o, c in sorted(hm.items()) if o < 0xC0)
    plwas = "; ".join("+0x%X %s %s" % (o, c[3], c[4]) for o, c in sorted(pl.items()) if 0xC0 <= o < 0x180)
    out = []; hdone = pdone = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == HM and int(c[1], 16) < 0xC0:
            if not hdone:
                out.append("\t".join([HM, "0x000", "192", "widgetBase0000", "Widget", "the shared Widget header 00245000 / 002465F0 write on every constructed widget (the element is built whole at 002BFCCA)", P[0], P[1], ev("H", "the header rows " + hmwas)]) + e); hdone = True
            continue
        if c[0] == PL and 0xC0 <= int(c[1], 16) < 0x180:
            if not pdone:
                out.append("\t".join([PL, "0x0C0", "192", "nestedWidget0C0", "Widget", "a 0xC0-byte widget 0029C850 builds here (00245000 at 0029C93A) and drives through 00273A20 / 00244F00 / 002468A0; the old rows were its handler slot and its +0x7C", P[0], P[1], ev("P", plwas)]) + e); pdone = True
            continue
        if c[0] == PL and int(c[1], 16) == 0xB4C:
            w = "%s %s (%s)" % (c[3], c[4], c[5][:120])
            out += ["\t".join(x) + e for x in [[PL, "0xB4C", "12", "unobservedSpan0B4C", "u8[12]", "not read by the bodies read here", U[0], U[1], ev("S", w)],
                                                [PL, "0xB58", "4", "selectedSlot", "int32", "a pane-slot index: 0029C850 multiplies it by 0x160 into paneSlots0240 and reads that slot's +0x9A", P[0], P[1], ev("S", w)],
                                                [PL, "0xB5C", "12", "unobservedTail0B5C", "u8[12]", "not read by the bodies read here", U[0], U[1], ev("S", w)]]]
            continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); to = []
    for l in tl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == HM and "00245000 at 002BFCCA" not in c[5]:
            c[5] = "built whole by 00245000 at 002BFCCA (`mov edx, 0x100` at 002BFCC2, handler 002BF8C0) - " + c[5]
            c[10] += " || HEADER EMBEDDED 2026-09-28 (OPUS, %s H)" % REC
        to.append("\t".join(c) + e)
    open(TY, "wb").write("".join(to).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def rows(t): return {int(c[1], 16): c for c in F if c[0] == t}
H_, L_ = rows(HM), rows(PL)
check("W", [o for o in H_ if o < 0xC0] == [0] and H_[0][3:5] == ["widgetBase0000", "Widget"] and L_.get(0xC0, [0] * 5)[3:5] == ["nestedWidget0C0", "Widget"]
      and not any(0xC0 < o < 0x180 for o in L_) and L_.get(0xB58, [0] * 4)[3] == "selectedSlot"
      and sum(int(c[2]) for c in H_.values()) == 0x100 and sum(int(c[2]) for c in L_.values()) == 0xB68,
      "HelpMessageSlotRecord0100's header is widgetBase0000; PaneListWidget0B68 has nestedWidget0C0 and selectedSlot; both tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
