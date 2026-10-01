"""rule0_apply.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
Applies FABLE's rule-0 shared-storage ruling (_index/candidates/rule0-shared-storage-ruling/, 5604b7413) to the AB30 union.

  D  own decode of the two orderings the ruling rests on:
     00290630 tests +0x10F68 bit 0x2000 (00290640) before it tail-jumps to 00296490, whose 002964BA writes +0x710; and
     002906D0 reads singleton + 0xB240 at 002906FF after 00273A20 (the `[rcx] != 0` liveness test) and BEFORE its bit test
     at 00290707 - so 002906FF proves only that some occupant is live
  A  applied: ManagerSingleton0209BE80 gains an OVERLAY row at +0xAB30 for Widget0720At0209BE80_AB30 (0x720), tagged by
     +0x10F68 bit 0x2000; the Widget0720 +0x710 row keeps 002964BA / 0029696A and drops 002906FF; the union (the embeddedAB30
     row) records 002906FF with both readings
  W  REGRESSION (FAILS before): the three store changes are present; types_index accepts the overlay
Usage: python rule0_apply.py [--patch]
"""
import hashlib, os, subprocess, sys
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
check("D", has(0x290630, 0x290679, [(0x290640, ("test", "dword ptr [rcx + 0x10f68], 0x2000")), (0x29064A, ("je", "0x290674")), (0x29066F, ("jmp", "0x296490"))])
      and has(0x2906D0, 0x290730, [(0x2906EE, ("call", "0x273a20")), (0x2906FA, ("cmp", "eax, 1")), (0x2906FF, ("cmp", "dword ptr [rcx + 0xb240], eax")),
                                   (0x290707, ("test", "dword ptr [rcx + 0x10f68], 0x2000"))])
      and has(0x273A20, 0x273A29, [(0x273A22, ("cmp", "qword ptr [rcx], rax"))]) and 0x2906FF < 0x290707,
      "002964BA sits behind the bit test 00290640; 002906FF follows only the liveness test 00273A20 and precedes the bit test 00290707")
FI = os.path.join(DB, "_types", "fields.tsv")
REC = "_index/candidates/battle-menu-child-base-opus/rule0_apply.py"; RUL = "FABLE rule-0 shared-storage ruling 5604b7413"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
SG, AB, W7 = "ManagerSingleton0209BE80", "ManagerSub0209BE80_AB30", "Widget0720At0209BE80_AB30"
OV = [SG, "0xAB30", "1824", "overlayWidget0720AB30", W7,
      "OVERLAY embeddedAB30 +0xAB30..+0xB24F (tag: +0x10F68 bit 0x2000): the 0x720 widget 00290707 builds here (00296940) while the bit is clear, then sets it; the battle menu (embeddedAB30) occupies the same storage in the other mode. Accesses are placed in the occupant their own path proves (%s)" % RUL,
      "TYPE RESOLVED", "PROVEN", "APPLIED 2026-09-28 (OPUS, %s A; %s; battle_menu_child_base.py X). %s" % (REC, RUL, EXE)]
UNION = (" || UNION ACCESS 2026-09-28 (OPUS, %s A; %s): 002906FF reads singleton + 0xB240 after only the liveness test 00273A20 and before the bit test 00290707, so it proves neither occupant - "
         "under the 0x720 widget it is Widget0720At0209BE80_AB30 +0x710, under the battle menu it is inside BattleMenuChildWidget1620 records[1].textDraw (+0x340 of the first child)" % (REC, RUL))
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; added = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == SG and c[1] == "0xAB30" and c[3] == "embeddedAB30":
            if REC not in c[5]: c[5] += UNION
            out.append("\t".join(c) + e)
            if not any(cells(x)[0] == SG and cells(x)[3] == "overlayWidget0720AB30" for x in fl): out.append("\t".join(OV) + e)
            continue
        if c[0] == W7 and int(c[1], 16) == 0x710 and REC not in c[8]:
            c[5] = ("set to 1 by 00296490 (002964BA, reached from 00290630 behind its bit test 00290640) and compared with 0 by 00296960 (0029696A, reached behind the bit test 00290694 and from this widget's own handler at 002986B4). "
                    "The read at 002906FF (singleton + 0xB240) is not this row's: it proves only liveness and is recorded on the union (%s)" % RUL)
            c[8] += " || NARROWED 2026-09-28 (OPUS, %s A): 002906FF moved to the union per %s" % (REC, RUL)
            out.append("\t".join(c) + e); continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
ov = [c for c in F if c[0] == SG and c[3] == "overlayWidget0720AB30"]
ab = next(c for c in F if c[0] == SG and c[3] == "embeddedAB30")
w7 = next(c for c in F if c[0] == W7 and int(c[1], 16) == 0x710)
v = subprocess.run([sys.executable, os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "types_index.py"), "--validate"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=os.path.dirname(DB)).stdout
errs = [l for l in v.splitlines() if SG in l and ("overlap" in l or "overrun" in l)]
check("W", len(ov) == 1 and ov[0][5].startswith("OVERLAY ") and "bit 0x2000" in ov[0][5] and "002906FF" in ab[5] and "UNION ACCESS" in ab[5]
      and "not this row's" in w7[5] and not errs, "overlay row present and tagged; 002906FF on the union; +0x710 narrowed; types_index reports no overlap for the singleton")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
