"""putility.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
Phyre::PUtility, the 0x20-byte base of the fifteen module objects on the registry chain at 02CACC90. The page
(22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md, FABLE's answers of 2026-09-14) has the
mechanism in prose; the type store had no row. Every fact below is re-read from the bytes here.

  I  THE IMAGE: the fourteen .data module objects each begin {vtable 00D26BC0, next 0, a pointer to their module-name string,
     dword 0xFF, dword 0}; the name strings read Serialization, Scene, Animation, Rendering, PostProcessing, Geometry,
     Scripting, Physics, DynamicGeometry, LOD, Inputs, Game, Hierarchy, DeveloperExtensions
  Z  THE SIZE: slot 0 of the base vtable, 005A0CB0, is the scalar deleting destructor; it re-stamps 00D26BC0, unlinks this from
     02CACC90 and, for flags bit 0, frees with an explicit size 0x20 (005A0D01 mov edx, 0x20; 005A0D06 call 00809950). Two
     pairs of module objects sit exactly 0x20 apart (01F2EE60 / 01F2EE80, 01F47550 / 01F47570), the second's base vtable
     starting where the first's +0x20 would be
  C  CONSTRUCTION AND TEARDOWN: each of the fourteen .data registrars links the object into the chain, writes its derived
     vtable and tail-jumps atexit (00808B90) with its paired teardown in rcx; each teardown re-stamps 00D26BC0 and unlinks.
     The fifteenth, PText at 02E5BE88 (.bss), is built by 006CCC10 through 00167B90, which stores +0x18 = 0xFF (006CCC17) and
     +0x10 = "Text" and registers 008B6F00
  W  REGRESSION (FAILS before): PUtility (0x20) in the store, tiled, with its fifteen static instances
Not claimed: what the key would mean below 0xFF; the derived classes' sizes (only two are bounded at 0x20); what reads +0x10.
Usage: python putility.py [--patch]
"""
import hashlib, os, re, struct, sys
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
def dis(lo, hi): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)]
def cstr(v): o = off(v); return d[o:d.index(b"\0", o)].decode()
def ripv(a, m, o, nxt):
    mm = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", o)
    return nxt + int(mm.group(2), 16) * (1 if mm.group(1) == "+" else -1) if mm else None
BASE_VT, HEAD, ATEXIT = 0xD26BC0, 0x2CACC90, 0x808B90
# (object, registrar, teardown, name) - the page's table; the names are read below, not trusted
MODS = [(0x1F2CD80, 0x160320, 0x8A8CE0, "Serialization"), (0x1F2CDF8, 0x160380, 0x8A8DC0, "Scene"), (0x1F2CE20, 0x1610E0, 0x8AAD40, "Animation"),
        (0x1F2D680, 0x162B70, 0x8AE6D0, "Rendering"), (0x1F2E800, 0x165420, 0x8B0B40, "PostProcessing"), (0x1F2E9B8, 0x165EA0, 0x8B1A60, "Geometry"),
        (0x1F2EAC8, 0x166210, 0x8B2670, "Scripting"), (0x1F2EB00, 0x166C30, 0x8B3E30, "Physics"), (0x1F2EE60, 0x167810, 0x8B6A40, "DynamicGeometry"),
        (0x1F2EE80, 0x167870, 0x8B6AA0, "LOD"), (0x1F44D70, 0x16AB40, 0x8B9890, "Inputs"), (0x1F44FE8, 0x16AEC0, 0x8BA260, "Game"),
        (0x1F47550, 0x16D5B0, 0x8C1580, "Hierarchy"), (0x1F47570, 0x16D610, 0x8C15E0, "DeveloperExtensions")]
img = []
for obj, reg, td, nm in MODS:
    vt, nx, name, key = struct.unpack_from("<QQQQ", d, off(obj))
    img.append(vt == BASE_VT and nx == 0 and key == 0xFF and cstr(name) == nm)
check("I", all(img), "%d of 14 .data module objects read {00D26BC0, 0, &name, 0xFF (dword, then 0)} with the expected name" % sum(img))
Dd = dis(0x5A0CB0, 0x5A0D14); DA = {a: (m, o) for a, m, o in Dd}
check("Z", DA.get(0x5A0CB6) == ("lea", "rax, [rip + 0x785f03]") and 0x5A0CBD + 0x785F03 == BASE_VT and DA.get(0x5A0CC0) == ("mov", "qword ptr [rcx], rax")
      and DA.get(0x5A0CC3) == ("lea", "r8, [rip + 0x270bfc6]") and 0x5A0CCA + 0x270BFC6 == HEAD and DA.get(0x5A0CF4) == ("mov", "qword ptr [rcx + 8], 0")
      and DA.get(0x5A0CFC) == ("test", "dl, 1") and DA.get(0x5A0D01) == ("mov", "edx, 0x20") and DA.get(0x5A0D06) == ("call", "0x809950")
      and struct.unpack_from("<Q", d, off(BASE_VT))[0] == 0x5A0CB0
      and struct.unpack_from("<Q", d, off(0x1F2EE80))[0] == BASE_VT and struct.unpack_from("<Q", d, off(0x1F47570))[0] == BASE_VT,
      "base vtable slot 0 = 005A0CB0: re-stamp, unlink from 02CACC90, sized free 0x20; 01F2EE80 and 01F47570 begin 0x20 after their neighbours")
cok = []
for obj, reg, td, nm in MODS:
    R = dis(reg, reg + 0x60)
    last = next((k for k, (a, m, o) in enumerate(R) if m == "jmp"), None)
    rcx = None
    for k in range(last - 1, -1, -1):
        a, m, o = R[k]
        if o.startswith("rcx, [rip"): rcx = ripv(a, m, o, R[k + 1][0]); break
    links = any(o.startswith("qword ptr [rax], rcx") for a, m, o in R[:last])
    T = dis(td, td + 0x60)
    restamp = any(ripv(a, m, o, T[k + 1][0]) == BASE_VT for k, (a, m, o) in enumerate(T[:-1]) if m == "lea")
    cok.append(R[last][2] == hex(ATEXIT) and rcx == td and links and restamp)
Pt = dis(0x6CCC10, 0x6CCC70); PA = {a: (m, o) for a, m, o in Pt}
ptext = PA.get(0x6CCC17) == ("mov", "dword ptr [rcx + 0x18], 0xff") and cstr(0xD89C80) == "Text" and any(ripv(a, m, o, Pt[k + 1][0]) == 0xD89C80 for k, (a, m, o) in enumerate(Pt[:-1]) if m == "lea")
Rt = dis(0x167B90, 0x167BB0)
ptext = ptext and any(ripv(a, m, o, Rt[k + 1][0]) == 0x2E5BE88 for k, (a, m, o) in enumerate(Rt[:-1]) if o.startswith("rcx, [rip")) \
    and any(ripv(a, m, o, Rt[k + 1][0]) == 0x8B6F00 for k, (a, m, o) in enumerate(Rt[:-1]) if o.startswith("rcx, [rip"))
check("C", all(cok) and ptext, "%d of 14 registrars link, install and tail-jump atexit with their paired teardown, each teardown re-stamps 00D26BC0; "
      "PText: 00167B90 -> 006CCC10 on 02E5BE88 (key 0xFF at 006CCC17, name \"Text\"), atexit 008B6F00" % sum(cok))
REC = "_index/candidates/phyre-putility-opus/putility.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
PV, DU = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
T = "PUtility"
ROWS = [(0x00, 8, "vtable", "void*", "00D26BC0 (PUtility's own) in the image and after teardown; the static constructor installs the derived module vtable. Slot 0 = 005A0CB0 (scalar deleting destructor), slot +0x08 init, slot +0x10 shutdown (the page's walkers 005A08E0 / 005A0840)", PV),
        (0x08, 8, "next", "PUtility*", "the registry chain link from the head 02CACC90: constructors splice in, 005A0CB0 and the atexit teardowns unlink and clear it", PV),
        (0x10, 8, "moduleName", "char*", "the module's name string in the image (\"Serialization\" ... \"DeveloperExtensions\"; \"Text\" stored by 006CCC10) - no reader established here", PV),
        (0x18, 4, "orderKey", "uint32", "the insertion key: constructors walk the chain while node key < 0xFF; 0xFF in every module (image; 006CCC17), so every module splices at the head. What a lower key would mean is not established", PV),
        (0x1C, 4, "unobservedSpan1C", "u8[4]", "zero in the fourteen .data images; no access found", DU)]
INST = ("fifteen static module objects: .data 01F2CD80 Serialization, 01F2CDF8 Scene, 01F2CE20 Animation, 01F2D680 Rendering, 01F2E800 PostProcessing, "
        "01F2E9B8 Geometry, 01F2EAC8 Scripting, 01F2EB00 Physics, 01F2EE60 DynamicGeometry, 01F2EE80 LOD, 01F44D70 Inputs, 01F44FE8 Game, 01F47550 Hierarchy, "
        "01F47570 DeveloperExtensions; .bss 02E5BE88 Text - each the base of its PUtility<Module> object")
TROW = [T, "0x20", "22-Middleware-PhyreEngine", INST,
        "IMAGE - fourteen initialised in .data (vtable 00D26BC0, key 0xFF), PText zero-initialised in .bss; the size from 005A0CB0's sized free (0x20)",
        "per-module static initialisers (e.g. 00166210; PText 00167B90 -> 006CCC10): link into 02CACC90, install the derived vtable, register the teardown with atexit",
        "the atexit teardowns (008A8CE0 ... 008C15E0, PText 008B6F00: re-stamp 00D26BC0 and unlink); 005A0CB0 is the virtual scalar deleting destructor (sized free 0x20)",
        PV[0], PV[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s I Z C). Mechanism in prose: FABLE's answers of 2026-09-14 on the page (DB-1..DB-5, UQ-294, UQ-295). %s" % (REC, EXE),
        "22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md", "STATIC - the chain head 02CACC90 and the fixed object addresses"]
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); e = fl[1][len(fl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == T for l in fl):
        fl += ["\t".join([T, "0x%02X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s). %s" % (REC, EXE)]) + e for o, n, nm, ct, m, rd in ROWS]
    open(FI, "wb").write("".join(fl).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == T for l in tl): tl.append("\t".join(TROW) + te)
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
Tt = [cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
check("W", len(Tt) == 1 and Tt[0][1] == "0x20" and sum(int(c[2]) for c in F) == 0x20 and len(F) == len(ROWS) and "02E5BE88" in Tt[0][3],
      "PUtility (0x20) is in the store, tiles, and lists its fifteen static instances")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
