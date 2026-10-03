"""check.py (SWE2-ORACLE, 2026-10-03): the three KO-partition consumer corrections, read at the bytes.
1. 00310780 admits the target release only with bit 22 CLEAR: 003107BE bt rcx,0x16 / 003107C3 jb skips when SET.
   Control: a 'bit 22 set admits' model predicts jae (or jnc) at 003107C3; the bytes have jb.
2. 0030EDA0 copies [+0x6B0, +0xBA0): add rcx,0x6b0, 9 x 0x80 bytes (edx = 9), then a 0x70-byte tail (7 movups stores).
   Control: the old '0x480 at +0x730' model predicts add rcx,0x730 and no tail; the bytes disagree.
3. The three documents carry the corrections with the originals struck. Exit 0 with FAILS 0."""
import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
os.chdir(ROOT / "Database/Tools/work/FABLE/pub140-scratch")
exec(open("disw.py").read().split("fn = int")[0])
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def ok(c, m):
    global fails
    print(("PASS  " if c else "FAIL  ") + m)
    fails += 0 if c else 1


def dis(s, e):
    return [(i.address, i.mnemonic, i.op_str) for i in md.disasm(bytes(d[off(s):off(e)]), s)]


a = {x[0]: (x[1], x[2]) for x in dis(0x00310780, 0x00310861)}
ok(a.get(0x003107BE) == ("bt", "rcx, 0x16") and a.get(0x003107C3) == ("jb", "0x310803"),
   "1 003107BE bt rcx,0x16 / 003107C3 jb 0x310803: bit 22 SET skips the target release")
ok(a.get(0x003107C3, ("", ""))[0] not in ("jae", "jnb", "jnc"), "1C control: a 'set admits' model predicts jae; the bytes do not")
b = dis(0x0030EDA0, 0x0030EE48)
bm = {x[0]: (x[1], x[2]) for x in b}
ok(bm.get(0x0030EDA7) == ("add", "rcx, 0x6b0") and bm.get(0x0030EDB1) == ("mov", "edx, 9"), "2 copy starts at +0x6B0, 9 iterations of 0x80")
tail = [x for x in b if x[0] >= 0x0030EE09 and x[1] == "movups" and x[2].startswith("xmmword ptr [rcx")]
ok(len(tail) == 7, "2 tail: 7 x 0x10 stores after the loop -> 0x480 + 0x70 = 0x4F0, ending at +0xBA0 (got %d)" % len(tail))
ok(bm.get(0x0030EDA7) != ("add", "rcx, 0x730"), "2C control: the old '+0x730' model predicts add rcx,0x730; the bytes disagree")
DB = ROOT / "Database/FFXII TZA"
t198 = (DB / "_experiments/EXP-198-unlink-carrier-family-exec.md").read_text(encoding="utf-8")
tcon = (DB / "10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md").read_text(encoding="utf-8")
t231 = (DB / "_experiments/EXP-231-detach-siblings-exec.md").read_text(encoding="utf-8")
ok("bit22\n  ~~set~~ **clear**" in t198.replace("\r\n", "\n"), "3 EXP-198: 'set' struck, 'clear' stated")
ok("bit22 ~~and~~ **clear**" in tcon, "3 contract 13g: the predicate states clear")
ok("~~0x480-byte `movups` snapshot copy" in t231 and "0x4F0-byte `movups` snapshot copy" in t231, "3 EXP-231: 0x480 struck, 0x4F0 at +0x6B0 stated")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
