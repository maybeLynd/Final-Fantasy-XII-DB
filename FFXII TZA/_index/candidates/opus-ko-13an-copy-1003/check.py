"""check.py (OPUS, 2026-10-03): CONTRACT-auto-status-rebuild 13an's 0030EDA0 copy, read at the bytes.
1. 0030EDA0 copies [+0x6B0, +0xBA0): 0030EDA7 add rcx,0x6b0, edx = 9 iterations of 0x80, then 7 movups tail stores
   (0x70) - 0x480 + 0x70 = 0x4F0.
   Control: the old '0x480 at +0x730' model predicts add rcx,0x730 and no tail; the bytes disagree.
2. Section 13an carries the correction with the old span struck, exactly once; the old unstruck line is gone.
   Control: the pre-correction text (git show HEAD~ of the contract when run before publish) is rejected by the same
   test - checked here against the literal old line.
Exit 0 with FAILS 0."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GFZ = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, GFZ)
os.chdir(GFZ)
import retool  # noqa: E402

R = retool.R
fails = 0


def ok(c, m):
    global fails
    print(("PASS  " if c else "FAIL  ") + m)
    fails += 0 if c else 1


ins = [(i.address, i.mnemonic, i.op_str) for i in R.md.disasm(R.at(0x0030EDA0, 0xA8), 0x0030EDA0)]
m = {a: (n, o) for a, n, o in ins}
ok(m.get(0x0030EDA7) == ("add", "rcx, 0x6b0"), "1 0030EDA7 add rcx,0x6b0: the copy starts at +0x6B0")
ok(m.get(0x0030EDB1) == ("mov", "edx, 9"), "1 0030EDB1 mov edx,9: nine 0x80-byte iterations")
tail = [a for a, n, o in ins if a >= 0x0030EE09 and n == "movups" and o.startswith("xmmword ptr [rcx")]
ok(len(tail) == 7, "1 tail: 7 x 0x10 stores after the loop -> 0x4F0 in all, ending at +0xBA0 (got %d)" % len(tail))
ok(m.get(0x0030EDA7) != ("add", "rcx, 0x730"), "1C control: the old '+0x730' model predicts add rcx,0x730; the bytes disagree")

P = os.path.normpath(os.path.join(HERE, "..", "..", "..", "10-Status-Periodic-Terminal", "CONTRACT-auto-status-rebuild.md"))
t = open(P, encoding="utf-8").read()
OLD = "  `q[obj+0xB88]`→`obj+0x730` (0x480) → `q[obj] &="


def corrected(text):
    return (text.count("~~`obj+0x730` (0x480)~~ `obj+0x6B0` (0x4F0") == 1 and OLD not in text)


ok(corrected(t), "2 contract 13an: '+0x730 (0x480)' struck once, '+0x6B0 (0x4F0)' stated, the old line gone")
ok(not corrected(t.replace(t[t.index("  `q[obj+0xB88]`→~~"):].split("\n", 1)[0], OLD) if "~~`obj+0x730`" in t else t),
   "2C control: the same test rejects the contract with the old 13an line restored")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
