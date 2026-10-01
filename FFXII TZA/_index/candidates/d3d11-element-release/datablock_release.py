"""datablock_release.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The data-block half of the D3D11 element
release (element_release.py covers the five texture / buffer classes). PDataBlockD3D11 (vertex) and PIndexDataBlockD3D11 (index)
had an unreduced destroy and an unregistered 'gap' dword; their elements PDataBlockBufferD3D11 / PIndexDataBlockBufferD3D11 kept
+0x10..+0x23 as 'no reader found in reach'.

  B  bound flag, bit 0 of vertex +0x74 / index +0x6C: the four creators set it after building the element buffers - or dword
     [rbx+0x74], 1 at 0066FA79 (0066F970) and 00670275 (00670070); or dword [rbx+0x6C], 1 at 0066FBB9 (0066FAB0) and 00670025
     (0066FE20). The unbind 00674230 / 00674420 tests it first and, when clear, passes 'Trying to unbind a data block which is
     not currently bound...' (00D69130; the index twin's own message at 00D68FE0) to 005CDAA0 and returns; at its end it clears it (and ..., 0xFFFFFFFE at 00674403 /
     006745F3). The destroy tests it before calling the unbind (00662F9D / 0065FC3A)
  D  the destroys: vertex 0065FEE0 -> 00662F80 = drain 00673780; unbind when bound; free the external m_buffers array (count
     +0x20, array +0x28) when count > 1 and bit 31 clear; free the base's +0x10 array unless +0x08 bit 31 is set. Index 0065FC20
     = drain 006737F0; unbind when bound; free the external array (+0x18 / +0x20) the same way
  W  the drains Sleep(1) while element +0x20 is > 0 (getters 00670D80 / 00670DC0: index*0x48 + 0x20; a signed test)
  U  the unbind walks every element (stride 0x48): when +0x40 (pendingUploadSource) is non-null it removes the element's queued
     update (+0x28) from the scheduler (0062EC70) and frees +0x40 through 00584730; it releases +0x08, +0x00 and +0x18 through
     vtable slot +0x10, nulling each
  So element +0x18 is an object released like the views, +0x20 a count the destroy waits on, +0x10 stays unread; owner bit 0
  is 'bound'. The other bits of +0x74 / +0x6C, and who raises the counts, are not established.
  S  REGRESSION: the spans are re-cut and the cells reduced (FAILS before)
Usage: python datablock_release.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
pd = next(s for s in SECS if s[0] == b".pdata")
def func_of(v):
    """the root function of the .pdata entry holding v, following UNW_FLAG_CHAININFO (a split function's later chunks chain to
    their primary entry)"""
    r = v - B
    for i in range(pd[4], pd[4] + pd[3], 12):
        b0, e0, u = struct.unpack_from("<III", d, i)
        if b0 <= r < e0: break
    else: return None
    while True:
        ui = off(u + B); flags = d[ui] >> 3; ncodes = d[ui + 2]
        if not flags & 4: return b0 + B
        ch = ui + 4 + 2 * (ncodes + (ncodes & 1)); b0, e0, u = struct.unpack_from("<III", d, ch)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
MSG = b"Trying to unbind a data block which is not currently bound"; MSGI = b"Trying to unbind an index data block which is not currently bound"
b = (all(at(a)[:2] == ("or", "dword ptr [rbx + 0x%x], 1" % o) and func_of(a) == f
         for a, o, f in ((0x66FA79, 0x74, 0x66F970), (0x670275, 0x74, 0x670070), (0x66FBB9, 0x6C, 0x66FAB0), (0x670025, 0x6C, 0x66FE20)))
     and at(0x674236)[:2] == ("test", "byte ptr [rcx + 0x74], 1") and at(0x67423D)[:2] == ("jne", "0x674258") and at(0x67423F)[2] == 0xD69130
     and at(0x67424B)[:2] == ("call", "0x5cdaa0") and at(0x674403)[:2] == ("and", "dword ptr [rbx + 0x74], 0xfffffffe")
     and at(0x674426)[:2] == ("test", "byte ptr [rcx + 0x6c], 1") and at(0x67442F)[2] == 0xD68FE0 and d[off(0xD68FE0):off(0xD68FE0) + len(MSGI)] == MSGI and at(0x67443B)[:2] == ("call", "0x5cdaa0")
     and at(0x6745F3)[:2] == ("and", "dword ptr [rbx + 0x6c], 0xfffffffe") and d[off(0xD69130):off(0xD69130) + len(MSG)] == MSG
     and at(0x662F9D)[:2] == ("test", "byte ptr [rbx + 0x74], 1") and at(0x662FA6)[:2] == ("call", "0x674230")
     and at(0x65FC3A)[:2] == ("test", "byte ptr [rbx + 0x6c], 1") and at(0x65FC43)[:2] == ("call", "0x674420"))
check("B", b, "bit 0 of vertex +0x74 / index +0x6C: set by the four creators, tested and cleared by the unbind, tested by the destroy")
dd = (at(0x65FEE7)[:2] == ("call", "0x662f80") and at(0x662F97)[:2] == ("call", "0x673780")
      and at(0x662FAC)[:2] == ("mov", "ecx, dword ptr [rbx + 0x20]") and at(0x662FBE)[:2] == ("cmp", "ecx, 1") and at(0x662FC3)[:2] == ("mov", "rcx, qword ptr [rbx + 0x28]")
      and at(0x662FCC)[:2] == ("call", "0x584730") and at(0x662FDB)[:2] == ("mov", "eax, dword ptr [rbx + 8]") and at(0x662FE7)[:2] == ("mov", "rcx, qword ptr [rbx + 0x10]")
      and at(0x662FF0)[:2] == ("call", "0x584730")
      and at(0x65FC35)[:2] == ("call", "0x6737f0") and at(0x65FC49)[:2] == ("mov", "ecx, dword ptr [rbx + 0x18]") and at(0x65FC60)[:2] == ("mov", "rcx, qword ptr [rbx + 0x20]")
      and at(0x65FC69)[:2] == ("call", "0x584730"))
check("D", dd, "destroys: drain, unbind when bound, external element array freed; vertex also frees the base's +0x10 array")
def getter(g, cnt, arr):
    return (at(g)[:2] == ("mov", "eax, dword ptr [rcx + 0x%x]" % cnt) and at(g + 0xC)[:2] == ("mov", "r8, qword ptr [rcx + 0x%x]" % arr)
            and at(g + 0x12)[:2] == ("lea", "rax, [rax + rax*8]") and at(g + 0x16)[:2] == ("lea", "rax, [rax + 4]") and at(g + 0x1A)[:2] == ("lea", "rax, [r8 + rax*8]"))
w = (getter(0x670D80, 0x20, 0x28) and getter(0x670DC0, 0x18, 0x20) and at(0x6737A5)[:2] == ("call", "0x670d80") and at(0x6737AC)[:2] == ("test", "ecx, ecx")
     and at(0x6737AE)[0] == "jle" and at(0x6737B5)[:2] == ("call", "0x5ccb80") and at(0x673815)[:2] == ("call", "0x670dc0") and at(0x673825)[:2] == ("call", "0x5ccb80")
     and at(0x5CCB80)[2] == 0x8C21B0)
check("W", w, "drains Sleep(1) while element +0x20 > 0 (index*0x48 + 0x20)")
def unbind(base):
    L = {0: ("cmp", "qword ptr [rsi + rax + 0x40], r15"), 0x4F: ("call", "0x62ec70"), 0x71: ("mov", "rcx, qword ptr [rsi + rcx + 0x40]"),
         0x76: ("call", "0x584730"), 0xBA: ("mov", "rcx, qword ptr [rsi + rax + 8]"), 0xCB: ("call", "qword ptr [rax + 0x10]"),
         0xEF: ("cmp", "qword ptr [rsi + rax], r15"), 0xF9: ("mov", "rcx, qword ptr [rdi]"), 0xFF: ("call", "qword ptr [rax + 0x10]"),
         0x122: ("mov", "rcx, qword ptr [rsi + rax + 0x18]"), 0x133: ("call", "qword ptr [rax + 0x10]"), 0x13C: ("add", "rsi, 0x48")}
    return all(at(base + k)[:2] == v for k, v in L.items())
check("U", unbind(0x6742B0) and unbind(0x6744A0), "unbind: free +0x40 after removing the queued update; release +0x08, +0x00, +0x18")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/datablock_release.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
EL = {"PDataBlockBufferD3D11": ("PDataBlockD3D11", "00674230", "00673780", "00670D80"), "PIndexDataBlockBufferD3D11": ("PIndexDataBlockD3D11", "00674420", "006737F0", "00670DC0")}
OW = {"PDataBlockD3D11": (0x74, "0066F970 / 00670070 (0066FA79 / 00670275)", "00674230", "00662F80 (via 0065FEE0)", "00673780", "+0x20 / +0x28", "00674403"),
      "PIndexDataBlockD3D11": (0x6C, "0066FAB0 / 0066FE20 (0066FBB9 / 00670025)", "00674420", "0065FC20", "006737F0", "+0x18 / +0x20", "006745F3")}
def ev(was): return "RE-CUT 2026-09-28 (OPUS, %s). was part of %s. %s" % (REC, was, EXE)
def new_rows(t, was):
    o, un, dr, g = EL[t]
    return [[t, "0x0010", "8", "unobservedSpan0010", "u8[8]", "a qword the element constructor zeroes and the copies and assignments move; not read by the drain or the unbind either", "DISCOVERED", "UNKNOWN", ev(was) + " (D W U)"],
            [t, "0x0018", "8", "releasedObject18", "void*", "an object released like the views: the owner's unbind %s calls its vtable slot +0x10 (the IUnknown Release position) and nulls it; which object it is and who stores it are not established" % un, "TYPE RESOLVED", "PROVEN", ev(was) + " (U)"],
            [t, "0x0020", "4", "pendingCount", "uint32", "a count the owner's destroy waits on: the drain %s reads it through %s and calls Sleep(1) while it is above 0 (a signed test, jle), before the unbind. Who raises and lowers it is not established" % (dr, g), "TYPE RESOLVED", "PROVEN", ev(was) + " (W)"]]
def flag_row(t, was):
    o, cr, un, dt, dr, arr, clr = OW[t]
    return [t, "0x%04X" % o, "4", "boundFlags", "uint32", "bit 0 = bound: the creators %s set it after building the element buffers; the unbind %s tests it first - when it is clear it passes its 'Trying to unbind ... not currently bound' message to 005CDAA0 and returns - and clears it at its end (%s); the destroy %s calls the unbind only when it is set. The other 31 bits are not read here" % (cr, un, clr, dt), "TYPE RESOLVED", "PROVEN", ev(was) + " (B)"]
UP = " || LIFETIME 2026-09-28 (OPUS, %s U): the owner's unbind frees it through 00584730 when non-null, after removing the element's queued update (+0x28) from the scheduler (0062EC70), and nulls it" % REC
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in EL and c[1] == "0x0010" and c[3] == "unobservedSpan0010" and c[2] == "20":
            out += ["\t".join(r) + e for r in new_rows(c[0], "%s %s (%s)" % (c[3], c[4], c[5]))]; continue
        if c[0] in OW and c[1].startswith("0x") and int(c[1], 16) == OW[c[0]][0] and c[3].startswith("unobservedSpan") and c[2] == "4":
            out.append("\t".join(flag_row(c[0], "%s %s (%s)" % (c[3], c[4], c[5][:200]))) + e); continue
        if c[0] in EL and c[1] == "0x0040" and c[3] == "pendingUploadSource" and REC not in c[5]:
            c[5] += UP; l = "\t".join(c) + e
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in EL and REC not in c[6]:
            o, un, dr, g = EL[c[0]]
            c[6] += (" || RELEASED BY THE OWNER 2026-09-28 (OPUS, %s U W): the element's own destroy slot is a no-op, but %s's unbind %s "
                     "releases +0x00 +0x08 +0x18 through vtable +0x10 and frees +0x40 after removing its queued update; the owner's destroy "
                     "first waits (%s) until +0x20 is not above 0" % (REC, o, un, dr))
            tl[i] = "\t".join(c) + e
        if c[0] in OW and REC not in c[6]:
            o, cr, un, dt, dr, arr, clr = OW[c[0]]
            tail = ", then frees the base's +0x10 array unless +0x08 bit 31 is set" if c[0] == "PDataBlockD3D11" else ""
            c[6] = c[6].replace("form not reduced", "~~form not reduced~~ reduced") + (
                " || READ 2026-09-28 (OPUS, %s B D): %s runs the drain %s, calls the unbind %s when bit 0 of +0x%X (bound) is set, and "
                "frees the external m_buffers array (count / array %s) through 00584730 when the count is above 1 and bit 31 is clear%s"
                % (REC, dt, dr, un, o, arr, tail))
            tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
have = {(r[0], int(r[1], 16)): r for r in F if r[0] in EL or r[0] in OW}
ok = all(have.get((t, o), [0, 0, 0, ""])[3] == nm for t in EL for o, nm in ((0x10, "unobservedSpan0010"), (0x18, "releasedObject18"), (0x20, "pendingCount")))
ok &= all(have.get((t, OW[t][0]), [0, 0, 0, ""])[3] == "boundFlags" for t in OW)
ok &= all(sum(int(r[2]) for k, r in have.items() if k[0] == t) == int(T[t][1], 16) for t in list(EL) + list(OW))
ok &= all(REC in T[t][6] for t in list(EL) + list(OW)) and all(REC in have[(t, 0x40)][5] for t in EL)
check("S", ok, "element spans re-cut (+0x18 released object, +0x20 count), owner bound flag typed, cells reduced, tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
