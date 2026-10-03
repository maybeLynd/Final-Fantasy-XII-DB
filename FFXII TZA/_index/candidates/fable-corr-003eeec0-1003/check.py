"""check.py - executed regression for this correction: which value of byte +0xC8 reaches the call at 003EEEC0+0xB4.
Decodes 003EEEC0+0x93 .. +0xB4 from the shipping image and steps the decrement chain (test / sub / cmp, je / jne) for
states 0..15, recording which states reach the call. Expected: exactly {4}.
Control (the defect this correction fixes): the same stepping with every `sub` ignored - the miscount that named the
`cmp ecx, 2` state directly - must give a different answer ({2}), so the check is sensitive to the miscount.
Prints FAILS N last."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
F = 0x003EEEC0
START, CALL = F + 0x93, F + 0xB4
img = Img.load()
ins = list(img.cs.disasm(img.read(START, CALL - START + 5), START))
assert ins[0].op_str == "ecx, byte ptr [rbx + 0xc8]", ins[0].op_str
assert ins[-1].address == CALL and ins[-1].mnemonic == "call", (hex(ins[-1].address), ins[-1].mnemonic)
for i in ins:
    print("%08X %s %s" % (i.address, i.mnemonic, i.op_str))


def reaches(state, honour_sub=True):
    ecx, zf = state, None
    for i in ins[1:]:
        m, o = i.mnemonic, i.op_str
        if m == "test" and o == "ecx, ecx":
            zf = ecx == 0
        elif m == "sub" and o == "ecx, 1":
            if honour_sub:
                ecx -= 1
            zf = ecx == 0 if honour_sub else (ecx - 1 == 0)
        elif m == "cmp" and o.startswith("ecx, "):
            zf = ecx == int(o.split(", ")[1], 0)
        elif m == "je":
            if zf:
                return False
        elif m == "jne":
            if not zf:
                return False
        elif m == "call":
            return i.address == CALL
    return False


got = {s for s in range(16) if reaches(s)}
miscount = {s for s in range(16) if reaches(s, honour_sub=False)}
print("states reaching %08X: %s (expected {4})" % (CALL, sorted(got)))
print("control, subs ignored (the miscount): %s (expected {2})" % sorted(miscount))
fails = (got != {4}) + (miscount != {2})
print("FAILS %d" % fails)
