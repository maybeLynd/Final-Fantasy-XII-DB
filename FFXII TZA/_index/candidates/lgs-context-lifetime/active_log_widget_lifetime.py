"""active_log_widget_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. ActiveLogWidget40C8's
release cell read 'not established - ... presumably rides the widget hierarchy's recursive teardown'. The presumption is
checked from the bytes:

  W1 the builder 002BDCE0 attaches the new widget as a CHILD of the widget at the manager's +0x1080:
     mov rdx, [rbx+0x1058] / mov rcx, [rbx+0x1080] / call 00244960 (002BDFBA / 002BDFC1 / 002BDFC8)
  W2 the widget release 00245020, when +0x40 bit 5 is clear, tail-jumps to 002482E0 (00245072 test / 0024507E jne /
     00245085 jmp); with bit 5 set it takes the 002473F0 arm instead
  W3 002482E0 releases a SUBTREE: it recurses into every child first (+0x18 first child, +0x20 next sibling;
     002482EE..00248306), unlinks itself from its parent, frees its element block +0x60 through 003697F0 (0024838E), and
     frees the widget itself through 003697F0 (002483DE) when +0x40 bit 14 is clear
  So the widget's release is its parent's: freeing the +0x1080 widget through 00245020 with bit 5 clear frees this child.
  When the parent is released is not established here.
  S  REGRESSION: the dtor cell carries W1-W3 (FAILS before the patch)
Usage: python active_log_widget_lifetime.py [--patch]
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
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
check("W1", at(0x2BDFBA) == ("mov", "rdx, qword ptr [rbx + 0x1058]") and at(0x2BDFC1) == ("mov", "rcx, qword ptr [rbx + 0x1080]")
      and at(0x2BDFC8) == ("call", "0x244960"), "002BDCE0 attaches the widget under the manager's +0x1080 widget")
check("W2", at(0x245072) == ("test", "byte ptr [rdi + 0x40], 0x20") and at(0x24507E) == ("jne", "0x24508a")
      and at(0x245085) == ("jmp", "0x2482e0") and at(0x24508C) == ("call", "0x2473f0"),
      "00245020: bit 5 clear -> 002482E0; set -> the 002473F0 arm")
check("W3", at(0x2482EE) == ("mov", "rcx, qword ptr [rcx + 0x18]") and at(0x2482F7) == ("mov", "rbx, qword ptr [rcx + 0x20]")
      and at(0x2482FB) == ("call", "0x2482e0") and at(0x24838E) == ("call", "0x3697f0") and at(0x2483D5) == ("bt", "eax, 0xe")
      and at(0x2483D9) == ("jb", "0x2483e5") and at(0x2483DE) == ("call", "0x3697f0"),
      "002482E0 frees the children first, then its +0x60 block and itself")
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/lgs-context-lifetime/active_log_widget_lifetime.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
ADD = (" || CHECKED 2026-09-28 (OPUS, %s W1-W3): the presumption holds. 002BDCE0 attaches this widget as a child of the manager's "
       "+0x1080 widget (00244960 at 002BDFC8); the widget release 00245020, with +0x40 bit 5 clear, tail-jumps to 002482E0, which "
       "frees a whole subtree - children first, then each widget's +0x60 block and the widget itself through 003697F0 (when "
       "+0x40 bit 14 is clear). So this widget's release is its parent's; when the parent is released is not established" % REC)
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "ActiveLogWidget40C8" and REC not in c[6]:
            c[6] += ADD; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
check("S", REC in t["ActiveLogWidget40C8"][6], "the dtor cell carries W1-W3")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
