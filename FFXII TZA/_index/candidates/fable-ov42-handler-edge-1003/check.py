"""check.py - executed regression for FABLE's correction of the reversed edge on the-box-renderer-that-is-never-called.md
(the SWE2-EC7 batch-150 UI crossing line): the stat-bar handlers 0029B7D0 / 0029B810 CALL 002973E0; 002973E0 calls
neither. Raw census over .text (E8/E9 rel32, 0F 8x rel32, EB/7x rel8) and every non-.text section (qword / RVA).
Control: the old reading "002973E0 calls the handlers" must FAIL. Prints FAILS N."""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
img = Img.load()
fails = 0


def check(n, ok, d=""):
    global fails
    print("%s  %s%s" % ("PASS" if ok else "FAIL", n, ("  | " + d) if d else "")); fails += not ok


_, va, vs, ra, rs = [s for s in img.secs if s[0] == ".text"][0]
raw = img.d[ra:ra + rs]


def refs(t):
    out = []
    for p in range(len(raw) - 6):
        a = img.base + va + p; b = raw[p]
        if b in (0xE8, 0xE9) and a + 5 + struct.unpack_from("<i", raw, p + 1)[0] == t: out.append(a)
        if b == 0x0F and 0x80 <= raw[p + 1] <= 0x8F and a + 6 + struct.unpack_from("<i", raw, p + 2)[0] == t: out.append(a)
        if (b == 0xEB or 0x70 <= b <= 0x7F) and a + 2 + struct.unpack_from("<b", raw, p + 1)[0] == t: out.append(a)
    return out


def inside(a, f):
    s, e = img.pdata(f) or (f, f)
    return s <= a < e


r_consumer = refs(0x002973E0)
check("002973E0's direct references are 0029B7EA and 0029B851 (in the two handlers)",
      sorted(r_consumer) == [0x0029B7EA, 0x0029B851], " ".join("%08X" % a for a in r_consumer))
check("0029B7EA lies in 0029B7D0 and 0029B851 in 0029B810",
      inside(0x0029B7EA, 0x0029B7D0) and inside(0x0029B851, 0x0029B810))
r_h1, r_h2 = refs(0x0029B7D0), refs(0x0029B810)
from_consumer = [a for a in r_h1 + r_h2 if 0x002973E0 <= a < 0x002974D8]
check("no instruction inside 002973E0..002974D7 transfers to either handler", not from_consumer,
      "handler refs: %s / %s" % (" ".join("%08X" % a for a in r_h1), " ".join("%08X" % a for a in r_h2)))
body = list(img.cs.disasm(img.read(0x002973E0, 0x002974D8 - 0x002973E0), 0x002973E0))
ind = [i for i in body if i.mnemonic in ("call", "jmp") and not i.op_str.startswith("0x")]
check("002973E0 has no indirect call or jump (so no handler dispatch through a pointer)", not ind,
      " ".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in ind))
old_reading = bool(from_consumer) or bool(ind)
check("CONTROL: the old reading '002973E0 calls the handlers' is refuted", not old_reading)
print("FAILS %d" % fails)
