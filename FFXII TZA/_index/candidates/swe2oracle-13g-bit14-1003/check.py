"""check.py (SWE2-ORACLE, 2026-10-03): 003138D0's sentinel bails, read at the bytes.
+0x714 == 0x113 bails unconditionally; +0xBA0 == 0x113 is tested only when dword [row] has bit 14 (0x4000).
Control: a model with an unconditional +0xBA0 test predicts no bt/jae guard before 0031390A - the bytes disagree.
Also checks the corrected contract bullet is present with the original struck. Exit 0 with FAILS 0."""
import os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
os.chdir(ROOT / "Database/Tools/work/FABLE/pub140-scratch")
exec(open("disw.py").read().split("fn = int")[0])
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ins = [(i.address, i.mnemonic, i.op_str) for i in Cs(CS_ARCH_X86, CS_MODE_64).disasm(bytes(d[off(0x003138D0):off(0x0031391E)]), 0x003138D0)]
at = {a: (m, o) for a, m, o in ins}
fails = 0


def ok(c, m):
    global fails
    print(("PASS  " if c else "FAIL  ") + m)
    fails += 0 if c else 1


ok(at.get(0x003138FE) == ("mov", "ebp, 0x113"), "1 ebp = 0x113 at 003138FE")
ok(at.get(0x00313903) == ("bt", "rdx, 0xe") and at.get(0x00313908) == ("jae", "0x313915"),
   "2 bt rdx,0xE / jae 00313915: the +0xBA0 test is skipped when bit 14 of dword [row] is clear")
ok(at.get(0x0031390A) == ("movzx", "ecx, word ptr [rax + 0xba0]") and at.get(0x00313913) == ("je", "0x313988"),
   "3 the +0xBA0 == 0x113 bail sits inside that guard")
ok(at.get(0x00313915) == ("cmp", "word ptr [rax + 0x714], bp") and at.get(0x0031391C) == ("je", "0x313988"),
   "4 the +0x714 == 0x113 bail is the jae target: unconditional")
guarded = any(m == "jae" and a < 0x0031390A for a, m, o in ins)
ok(guarded, "C control: an unconditional-+0xBA0 model predicts no jae before 0031390A; the bytes have one")
page = (ROOT / "Database/FFXII TZA/10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md").read_text(encoding="utf-8")
ok("~~`w[+0xBA0]==0x113`/`w[+0x714]==0x113`~~" in page and "only when `d[row] & 0x4000`" in page,
   "5 the 13g bullet carries the condition, the original struck")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
