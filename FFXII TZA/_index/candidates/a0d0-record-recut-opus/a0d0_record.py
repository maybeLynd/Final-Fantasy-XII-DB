"""a0d0_record.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
CORRECTION of OPUS's own ManagerSubA0D0Record rows (2026-09-22). Their 'no access at these displacements by either body
installed on this element' spans were censused before the census walked the control flow (FRONTIER 57f9d58ab); the
element's own handler 003F8250 and its callees read and write most of them.

  S  the construction site: 003F7F0D `call 00245000` with `mov edx, 0x110` (003F7EFE) and handler `lea r8 -> 003F8250`
     (003F7F03) - the whole element is a widget built by the widget constructor, so its first 0xC0 bytes are the shared
     Widget header (the header rows it re-described are replaced by widgetBase0000, as on 71 other widget types)
  H  003F8250 (rdi = this; message in [rdx]): message 4 copies [[this + 0xE0] + 0x754] to +0x108 and draws through the
     header's +0x38; message 2 takes an index from 003F8790(this, 1) and, when it differs from +0x104, stores it, zeroes
     the float +0x100, copies the 8 bytes at +0xE8 to +0xF8 and recomputes the word +0xF2 from the index, then runs
     003F8140; message 1 stores [msg + 8] at +0xE0, sets +0x104 from 003F8790(this, 0), zeroes +0xE8, writes 0x5000B4 at
     +0xEC, 1.0 at +0x100, the word at +0xEA, and copies the 8 bytes at +0xE8 to +0xF0 and +0xF8
  I  003F8140: while +0x100 is below 1.0 it adds a step and clamps to 1.0, then sets each int16 of +0xE8..+0xEE to
     from + (target - from) * t with from = +0xF8..+0xFE and target = +0xF0..+0xF6
  C  003F8790 walks four pointers at this + 0xC0 (stride 8, `cmp ebp, 4`), comparing each one's +0xE0 against the table
     [this + 0xE0] + 0x740
  W  REGRESSION (FAILS before): widgetBase0000 Widget, children at +0xC0 and the rect / animation rows are in the store;
     no absence row remains over an accessed displacement
Usage: python a0d0_record.py [--patch]
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
check("S", has(0x3F7EF9, 0x3F7F12, [(0x3F7EFE, ("mov", "edx, 0x110")), (0x3F7F03, ("lea", "r8, [rip + 0x346]")), (0x3F7F0D, ("call", "0x245000"))]) and 0x3F7F0A + 0x346 == 0x3F8250,
      "003F7F0D builds the 0x110 element in place (00245000) with handler 003F8250")
check("H", has(0x3F8250, 0x3F847D, [(0x3F8265, ("mov", "r8, qword ptr [rcx + 0xe0]")), (0x3F826C, ("mov", "rdi, rcx")), (0x3F82BF, ("mov", "ecx, dword ptr [r8 + 0x754]")),
                                     (0x3F82C6, ("mov", "dword ptr [rdi + 0x108], ecx")), (0x3F82DA, ("mov", "rbx, qword ptr [rdi + 0x38]")), (0x3F8333, ("cmp", "dword ptr [rdi + 0x108], 0")),
                                     (0x3F8362, ("call", "0x3f8790")), (0x3F8367, ("cmp", "dword ptr [rdi + 0x104], eax")), (0x3F8371, ("mov", "dword ptr [rdi + 0x104], eax")),
                                     (0x3F8377, ("mov", "dword ptr [rdi + 0x100], ecx")), (0x3F8382, ("mov", "rcx, qword ptr [rdi + 0xe8]")), (0x3F838C, ("mov", "qword ptr [rdi + 0xf8], rcx")),
                                     (0x3F83A0, ("mov", "word ptr [rdi + 0xf2], dx")), (0x3F83B0, ("call", "0x3f8140")), (0x3F83BA, ("mov", "rax, qword ptr [rdx + 8]")),
                                     (0x3F83C6, ("mov", "qword ptr [rdi + 0xe0], rax")), (0x3F83F8, ("mov", "dword ptr [rdi + 0x104], eax")), (0x3F8400, ("mov", "word ptr [rdi + 0xe8], cx")),
                                     (0x3F840F, ("mov", "dword ptr [rdi + 0xec], 0x5000b4")), (0x3F841C, ("mov", "dword ptr [rdi + 0x100], 0x3f800000")),
                                     (0x3F8430, ("mov", "word ptr [rdi + 0xea], dx")), (0x3F843E, ("mov", "qword ptr [rdi + 0xf0], rax")), (0x3F8445, ("mov", "qword ptr [rdi + 0xf8], rax"))]),
      "003F8250: +0xE0 bound object, +0x104 index, +0x100 t, +0xE8 / +0xF0 / +0xF8 rects, +0x108 flag, header +0x38")
check("I", has(0x3F8140, 0x3F8250, [(0x3F8140, ("movss", "xmm0, dword ptr [rcx + 0x100]")), (0x3F8171, ("mov", "dword ptr [rcx + 0x100], 0x3f800000")),
                                     (0x3F817B, ("movsx", "ecx, word ptr [rcx + 0xf8]")), (0x3F8182, ("movsx", "eax, word ptr [rdx + 0xf0]")), (0x3F8199, ("mulss", "xmm1, dword ptr [rdx + 0x100]")),
                                     (0x3F81A9, ("mov", "word ptr [rdx + 0xe8], ax")), (0x3F81B0, ("movsx", "ecx, word ptr [rdx + 0xfa]")), (0x3F81DE, ("mov", "word ptr [rdx + 0xea], ax")),
                                     (0x3F8213, ("mov", "word ptr [rdx + 0xec], ax")), (0x3F821A, ("movsx", "ecx, word ptr [rdx + 0xfe]")), (0x3F8221, ("movsx", "eax, word ptr [rdx + 0xf6]")),
                                     (0x3F8248, ("mov", "word ptr [rdx + 0xee], ax"))]),
      "003F8140: current rect +0xE8 = from +0xF8 + (target +0xF0 - from) * t +0x100")
check("C", has(0x3F8790, 0x3F8940, [(0x3F87C1, ("mov", "r15, rcx")), (0x3F87C9, ("mov", "r14, r15")), (0x3F87CC, ("lea", "rcx, [rsp + 0x40]")), (0x3F87D1, ("sub", "r14, rcx")),
                                     (0x3F87D4, ("lea", "rdi, [rsp + 0x40]")), (0x3F87F0, ("mov", "rcx, qword ptr [r14 + rdi + 0xc0]")), (0x3F880D, ("mov", "r9d, dword ptr [rcx + 0xe0]")),
                                     (0x3F8820, ("cmp", "r9d, dword ptr [r8 + rdx*4 + 0x740]")), (0x3F8927, ("add", "rdi, 8")), (0x3F892B, ("cmp", "ebp, 4"))]),
      "003F8790: four child pointers at +0xC0 (this - local + local + 0xC0), matched to [this + 0xE0] + 0x740")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/a0d0-record-recut-opus/a0d0_record.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
T = "ManagerSubA0D0Record"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CORRECTED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(o, sz, nm, ct, mean, rd, tag, was): return [T, "0x%03X" % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
def cells(l): return l.rstrip("\r\n").split("\t")
def new_rows(old):
    hdr = "; ".join("+0x%X %s %s" % (o, c[3], c[4]) for o, c in sorted(old.items()) if o < 0xC0)
    tail = "; ".join("+0x%X %s %s" % (o, c[3], c[4]) for o, c in sorted(old.items()) if o >= 0xC0)
    return [r(0x000, 0xC0, "widgetBase0000", "Widget", "the shared Widget header 00245000 / 002465F0 write on every constructed widget (the element is built whole at 003F7F0D)", P, "S", "the header rows " + hdr),
            r(0x0C0, 32, "children", "void*[4]", "four child widget pointers 003F8790 walks, matching each one's +0xE0 against the bound object's +0x740 table", P, "C", tail),
            r(0x0E0, 8, "boundObject", "void*", "stored from the create message's second qword (003F83C6); its +0x754 is copied to flag108 and its +0x740 table indexes the children", P, "H C", tail),
            r(0x0E8, 8, "rectCurrent", "int16[4]", "the element's rect: zeroed / set on create (+0xEC = 0x5000B4: 180 x 80), then interpolated each update by 003F8140", P, "H I", tail),
            r(0x0F0, 8, "rectTarget", "int16[4]", "the interpolation target: a copy of the create rect, whose word +0xF2 the update recomputes from the new index", P, "H I", tail),
            r(0x0F8, 8, "rectFrom", "int16[4]", "the interpolation start: the current rect copied when the index changes", P, "H I", tail),
            r(0x100, 4, "t", "float", "the interpolation parameter: 1.0 on create, 0 when the index changes, stepped up and clamped to 1.0 by 003F8140", P, "H I", tail),
            r(0x104, 4, "selectedIndex", "int32", "the index 003F8790 returns; a change restarts the interpolation", P, "H", tail),
            r(0x108, 4, "flag108", "uint32", "copied from the bound object's +0x754 on draw; non-zero selects 0x80 over 0x30 for the draw record's +0x5A", P, "H", tail),
            r(0x10C, 4, "unobservedSpan10C", "u8[4]", "not read by 003F8250, 003F8140 or 003F8790", U, "H", tail)]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    old = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == T}
    assert sum(int(c[2]) for c in old.values()) == 0x110 and old[0xE0][3] == "qword00E0"
    out = []; placed = False
    for l in fl:
        if cells(l)[0] == T:
            if not placed: out += ["\t".join(x) + eol for x in new_rows(old)]; placed = True
            continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); to = []
    for l in tl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == T and "00245000 at 003F7F0D" not in c[5]:
            c[5] = "built whole by 00245000 at 003F7F0D (`mov edx, 0x110` at 003F7EFE, handler 003F8250 at 003F7F03) - " + c[5]
            c[10] += " || HEADER EMBEDDED AND TAIL CORRECTED 2026-09-28 (OPUS, %s)" % REC
        to.append("\t".join(c) + e)
    open(TY, "wb").write("".join(to).encode("utf-8")); print("patched"); sys.exit(0)
F = {int(cells(l)[1], 16): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T}
ACCESSED = [0x10, 0x18, 0x30, 0x38, 0xC0, 0xE8, 0xEA, 0xEC, 0xEE, 0xF0, 0xF2, 0xF4, 0xF6, 0xF8, 0xFA, 0xFC, 0xFE, 0x100, 0x104, 0x108]
def row_at(o): return next((c for s, c in F.items() if s <= o < s + int(c[2])), None)
check("W", F.get(0, [0] * 5)[3:5] == ["widgetBase0000", "Widget"] and F.get(0xC0, [0] * 4)[3] == "children" and F.get(0x100, [0] * 4)[3] == "t"
      and all(row_at(o) and not row_at(o)[3].startswith("unobserved") for o in ACCESSED) and sum(int(c[2]) for c in F.values()) == 0x110,
      "header embedded; no absence row over the %d accessed displacements; the element tiles 0x110" % len(ACCESSED))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
